#!/usr/bin/env python3
"""Look up the quotes of returned rows in the case tree and drop the rows whose quote is not there.

  python3 lookup.py --tree TREE --out DIR return1.md [return2.md ...]

The mechanical part of the coordinator (protocol/coordinator-flat.md, step 2). For every table
row that has a file, a line and a quote, the quote must be at that line (score.citation:
'verified'). A row whose quote is elsewhere in the file or nowhere is dropped. Rows with no
quote or no line cannot be checked: they are kept and counted as such. Writes DIR/<name> for
each input and DIR/lookup.json with the counts per file. Reads only; runs nothing of the tree.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import score as S  # noqa: E402


def check(text, tree):
    lines = text.split("\n")
    out, stats = [], {"rows": 0, "verified": 0, "not_checkable": 0, "discarded": 0, "discarded_rows": []}
    i = 0
    while i < len(lines):
        if i + 1 < len(lines) and "|" in lines[i] and S.DELIM.match(lines[i + 1]) and "|" in lines[i + 1]:
            header = S.cells(lines[i])
            k = S.kind(header)
            out += [lines[i], lines[i + 1]]
            i += 2
            while i < len(lines) and lines[i].strip() and "|" in lines[i]:
                c = S.cells(lines[i])
                row = {h: (c[n] if n < len(c) else "") for n, h in enumerate(header)}
                verdict = S.citation(S.finding_of(header, row, k), tree) if k else None
                if k:
                    stats["rows"] += 1
                if verdict in ("wrong_line", "unverifiable"):
                    stats["discarded"] += 1
                    stats["discarded_rows"].append({"why": verdict, "row": lines[i].strip()[:240]})
                else:
                    stats["verified" if verdict == "verified" else "not_checkable"] += 1 if k else 0
                    out.append(lines[i])
                i += 1
            continue
        out.append(lines[i])
        i += 1
    return "\n".join(out), stats


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("returns", nargs="+")
    ap.add_argument("--tree", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    path = os.path.join(a.out, "lookup.json")
    all_stats = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
    for r in a.returns:
        text, stats = check(open(r, encoding="utf-8").read(), a.tree)
        name = os.path.basename(r)
        open(os.path.join(a.out, name), "w", encoding="utf-8").write(text)
        all_stats[name] = stats
        print(f"{name}: rows {stats['rows']}, verified {stats['verified']}, "
              f"not checkable {stats['not_checkable']}, discarded {stats['discarded']}")
    json.dump(all_stats, open(path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
