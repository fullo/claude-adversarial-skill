#!/usr/bin/env python3
"""Score one verification report against the answer key of its case (spike #17).

  python3 spikes/17-agents/score.py --tree DIR/L --key DIR/keys/L.json report.md [--json]

Everything here is mechanical, and fixed before any run:

1. Findings. Rows of the report's tables that have a location column ("File:Line" or
   "Location"). A table with a "Fix" column is FAIL; one with "Advertised" is HIDDEN
   BEHAVIORS; rows of HYPOTHESES count only as "hypothesis only".
2. Match. A finding matches a known defect when it cites the defect's file and either a line
   within LINE_WINDOW lines of the inserted text, or one of the defect's keywords in the row.
   By its line a finding matches one defect only, the nearest: two defects a few lines apart
   are not both found by one row, unless the row also names the other by a keyword.
   A defect is `found` (a FAIL row matches), `hidden` (only a HIDDEN BEHAVIORS row),
   `hypothesis` (only a HYPOTHESES row names the file and a keyword) or `missed`.
   Recall = found / defects. `hidden` and `hypothesis` are reported, never counted as found.
3. Citations. For every row with a file, a line and a quote: the quote must be in that file
   within QUOTE_WINDOW lines of the cited line (`verified`); if it is elsewhere in the file
   the line is wrong (`wrong_line`); if it is nowhere, or the file does not exist, the
   citation is `unverifiable`. Quotes are compared after collapsing white space; a quote cut
   with "..." or "…" is checked piece by piece. When the Quote cell mixes code spans with a
   comment (`code`: what is wrong with it), only the code spans are the quote.
4. Unmatched findings. FAIL rows that match no known defect are listed, not judged: the base
   repository may hold real defects that are not in the key. Whether each one is a false
   positive is decided by a person who does not know which mode produced the report.
"""

import argparse
import json
import os
import re
import sys

LINE_WINDOW = 5
QUOTE_WINDOW = 3
MIN_PIECE = 8  # a piece of a cut quote shorter than this proves nothing

LOCATION = re.compile(r"([\w./-]*[\w-]+\.(?:py|md|json|rs|ts|sh|toml|yml|yaml)|[\w./-]*(?:pre-commit|NOT_COMPUTABLE))"
                      r"(?::(\d+)(?:\s*[-–]\s*(\d+))?)?")
DELIM = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")


def cells(line):
    """Split a table row; escaped pipes and pipes inside code spans are not separators."""
    out, cur, i, code = [], "", 0, False
    s = line.strip()
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s) and s[i + 1] == "|":
            cur += "|"; i += 2; continue
        if ch == "`":
            code = not code
        if ch == "|" and not code:
            out.append(cur.strip()); cur = ""
        else:
            cur += ch
        i += 1
    out.append(cur.strip())
    if s.startswith("|"):
        out = out[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        out = out[:-1]
    return out


def tables(text):
    """Every Markdown table of the report as (header cells, list of row dicts)."""
    lines = text.splitlines()
    i = 0
    while i < len(lines) - 1:
        if "|" in lines[i] and DELIM.match(lines[i + 1]) and "|" in lines[i + 1]:
            header = cells(lines[i])
            rows, j = [], i + 2
            while j < len(lines) and lines[j].strip() and "|" in lines[j]:
                c = cells(lines[j])
                rows.append({h: (c[k] if k < len(c) else "") for k, h in enumerate(header)})
                j += 1
            yield header, rows
            i = j
        else:
            i += 1


def kind(header):
    h = [x.lower() for x in header]
    if "fix" in h and any(x.startswith("file") or x == "location" for x in h):
        return "fail"
    if "advertised" in h:
        return "hidden"
    if "hypothesis" in h and "observation" in h:
        return "hypothesis"
    if any(x.startswith("file:") or x == "location" for x in h):
        return "other"
    return None


def findings(text):
    out = []
    for header, rows in tables(text):
        k = kind(header)
        if k is None:
            continue
        for r in rows:
            out.append(finding_of(header, r, k))
    return out


def finding_of(header, r, k):
    """One table row as a finding: where it points, what it quotes."""
    loc_col = next((h for h in header if h.lower().startswith("file") or h.lower() == "location"), None)
    quote_col = next((h for h in header if h.lower().startswith("quote") or "(quote)" in h.lower()), None)
    whole = " | ".join(r.values())
    m = LOCATION.search(r.get(loc_col, "")) if loc_col else LOCATION.search(whole)
    return {"kind": k, "file": m.group(1) if m else None,
            "line": int(m.group(2)) if m and m.group(2) else None,
            "last": int(m.group(3)) if m and m.group(3) else None,
            "quote": r.get(quote_col, "") if quote_col else "", "text": whole}


def same_file(cited, known):
    if not cited:
        return False
    cited, known = cited.strip("./"), known.strip("./")
    return cited == known or known.endswith("/" + cited) or os.path.basename(cited) == os.path.basename(known) and "/" not in cited


def distance(f, d):
    """Lines between the cited range and the inserted text (0 when they overlap); None if not the same file or no line."""
    if f["kind"] == "hypothesis" or f["line"] is None or not same_file(f["file"], d["file"]):
        return None
    lo, hi = f["line"], f["last"] or f["line"]
    return max(0, d["first_line"] - hi, lo - d["last_line"])


def matches(f, d, nearest):
    """How a finding matches a defect: 'line', 'keyword' or None. `nearest`: the id of the defect closest to its line."""
    if f["kind"] == "hypothesis":
        named = os.path.basename(d["file"]).lower() in f["text"].lower()
        return "keyword" if named and any(k.lower() in f["text"].lower() for k in d["keywords"]) else None
    if not same_file(f["file"], d["file"]):
        return None
    if nearest == d["id"]:
        return "line"
    return "keyword" if any(k.lower() in f["text"].lower() for k in d["keywords"]) else None


def squash(s):
    return re.sub(r"\s+", " ", s).strip()


def citation(f, tree):
    """'verified', 'wrong_line', 'unverifiable' or None (nothing to check)."""
    raw = f["quote"].strip()
    spans = [s for s in re.findall(r"`([^`]+)`", raw) if len(squash(s)) >= MIN_PIECE]
    quote = " ... ".join(spans) if spans else raw.strip("`").strip()
    quote = re.sub(r"^[\"“']|[\"”']$", "", quote).replace("`", "")
    if not f["file"] or f["line"] is None or not quote:
        return None
    path = None
    for root, _, files in os.walk(tree):
        for name in files:
            rel = os.path.relpath(os.path.join(root, name), tree).replace(os.sep, "/")
            if same_file(f["file"], rel):
                path = os.path.join(root, name)
    if path is None:
        return "unverifiable"
    lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    pieces = [squash(p) for p in re.split(r"\.\.\.|…", quote)]
    pieces = [p for p in pieces if len(p) >= MIN_PIECE] or [squash(quote)]
    hi = (f["last"] or f["line"]) + QUOTE_WINDOW + quote.count("\n")
    near = squash(" ".join(lines[max(0, f["line"] - 1 - QUOTE_WINDOW):hi]))
    everywhere = squash(" ".join(lines))
    if all(p in near for p in pieces):
        return "verified"
    return "wrong_line" if all(p in everywhere for p in pieces) else "unverifiable"


def score(report, key, tree):
    fs = findings(report)
    status, how = {}, {}
    used = set()
    rank = {"fail": "found", "hidden": "hidden", "hypothesis": "hypothesis"}
    order = ["found", "hidden", "hypothesis", "missed"]
    nearest = []
    for f in fs:
        near = [(distance(f, d), d["id"]) for d in key["defects"]]
        near = sorted((x, i) for x, i in near if x is not None and x <= LINE_WINDOW)
        nearest.append(near[0][1] if near else None)
    for d in key["defects"]:
        best = "missed"
        for n, f in enumerate(fs):
            m = matches(f, d, nearest[n]) if f["kind"] in rank else None
            if m:
                used.add(n)
                s = rank[f["kind"]]
                if order.index(s) < order.index(best):
                    best, how[d["id"]] = s, m
        status[d["id"]] = best
    cites = [citation(f, tree) for f in fs]
    unmatched = [f for n, f in enumerate(fs) if f["kind"] == "fail" and n not in used]
    total = len(key["defects"])
    found = sum(1 for s in status.values() if s == "found")
    return {
        "case": key["case"], "defects": total, "found": found,
        "hidden": sum(1 for s in status.values() if s == "hidden"),
        "hypothesis_only": sum(1 for s in status.values() if s == "hypothesis"),
        "missed": sum(1 for s in status.values() if s == "missed"),
        "recall": round(found / total, 3) if total else None,
        "status": status, "matched_by": how,
        "rows": len(fs), "fail_rows": sum(1 for f in fs if f["kind"] == "fail"),
        "citations_checked": sum(1 for c in cites if c), "citations_verified": cites.count("verified"),
        "citations_wrong_line": cites.count("wrong_line"), "citations_unverifiable": cites.count("unverifiable"),
        "unmatched_fail_rows": [{"file": f["file"], "line": f["line"], "text": f["text"][:300]} for f in unmatched],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("report")
    ap.add_argument("--tree", required=True, help="the case tree the report was written about")
    ap.add_argument("--key", required=True, help="the answer key of that case")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    key = json.load(open(a.key, encoding="utf-8"))
    r = score(open(a.report, encoding="utf-8").read(), key, a.tree)
    if a.json:
        print(json.dumps(r, indent=2, ensure_ascii=False))
        return 0
    print(f"case {r['case']}: found {r['found']} of {r['defects']} (recall {r['recall']}); "
          f"hidden {r['hidden']}, hypothesis only {r['hypothesis_only']}, missed {r['missed']}")
    for i, s in r["status"].items():
        print(f"  {i}: {s}" + (f" (by {r['matched_by'][i]})" if i in r["matched_by"] else ""))
    print(f"rows {r['rows']} (FAIL {r['fail_rows']}); citations checked {r['citations_checked']}: "
          f"verified {r['citations_verified']}, wrong line {r['citations_wrong_line']}, unverifiable {r['citations_unverifiable']}")
    print(f"FAIL rows that match no known defect, to be judged blind: {len(r['unmatched_fail_rows'])}")
    for u in r["unmatched_fail_rows"]:
        print(f"  {u['file']}:{u['line']} {u['text'][:140]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
