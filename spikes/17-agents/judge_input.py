#!/usr/bin/env python3
"""Build the input of the blind review for one case: the FAIL rows that match no known defect.

  python3 judge_input.py --case L --key DIR/keys/L.json --runs RUNS --out FILE.md

Scores every RUNS/<case>-<mode>-<n>/out/report.md, takes the FAIL rows that match no known
defect, drops the columns nobody needs, shuffles them with a fixed seed and numbers them.
Writes FILE.md (what the reviewer gets: no mode, no run, no key) and FILE.map.json (row number
-> run, for whoever counts the verdicts afterwards; never given to the reviewer).
"""

import argparse
import glob
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import score as S  # noqa: E402

SEED = 17


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--case", required=True)
    ap.add_argument("--key", required=True)
    ap.add_argument("--runs", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    key = json.load(open(a.key, encoding="utf-8"))
    rows = []
    for report in sorted(glob.glob(os.path.join(a.runs, f"{a.case}-*", "out", "report.md"))):
        run = os.path.basename(os.path.dirname(os.path.dirname(report)))
        tree = os.path.join(os.path.dirname(os.path.dirname(report)), "tree")
        r = S.score(open(report, encoding="utf-8").read(), key, tree)
        rows += [(run, u["text"]) for u in r["unmatched_fail_rows_full"]]
    random.Random(SEED).shuffle(rows)
    lines = [f"# Rows to review, case {a.case}", "",
             "Each row is a finding some verifier reported about the project. For each one answer: "
             "real defect, not a defect, or cannot tell, and cite the line of the project that shows it.", ""]
    mapping = {}
    for n, (run, text) in enumerate(rows, 1):
        lines.append(f"{n}. {text}")
        mapping[n] = run
    open(a.out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    json.dump(mapping, open(a.out + ".map.json", "w", encoding="utf-8"), indent=2)
    print(f"{len(rows)} rows from {len(set(mapping.values()))} runs -> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
