#!/usr/bin/env python3
"""Run the files that check the facts stated in the evals (skills/adversarial-verify/evals/facts).

Each file reproduces what an eval's prompt states as fact (a run's result, a
computed value, which mutants a test kills) and exits non-zero if the fact is
false. Python files run with the interpreter that runs this script; .rs files
are compiled with rustc; .ts files run with node --experimental-strip-types.
A missing toolchain is an error, never a silent skip.

  python3 scripts/check_facts.py            # all files
  python3 scripts/check_facts.py 38 49      # only these eval ids
"""

import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS = os.path.join(ROOT, "skills", "adversarial-verify", "evals", "facts")
EXTS = (".py", ".rs", ".ts")


def command(path, tmp):
    ext = os.path.splitext(path)[1]
    if ext == ".py":
        return [[sys.executable, "-E", "-s", path]]
    if ext == ".rs":
        rustc = shutil.which("rustc")
        if not rustc:
            return None
        exe = os.path.join(tmp, os.path.basename(path) + ".bin")
        return [[rustc, "--edition", "2021", "-O", "-o", exe, path], [exe]]
    node = shutil.which("node")
    if not node:
        return None
    return [[node, "--experimental-strip-types", "--no-warnings", path]]


def main(ids):
    files = sorted(f for f in os.listdir(FACTS) if f.endswith(EXTS) and not f.startswith("_"))
    if ids:
        files = [f for f in files if os.path.splitext(f)[0] in ids]
    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        for name in files:
            path = os.path.join(FACTS, name)
            steps = command(path, tmp)
            if steps is None:
                print(f"FAIL {name}: toolchain not found")
                failed += 1
                continue
            for step in steps:
                r = subprocess.run(step, cwd=FACTS, capture_output=True, text=True)
                if r.returncode != 0:
                    print(f"FAIL {name}: {(r.stderr or r.stdout).strip().splitlines()[-1:] }")
                    failed += 1
                    break
            else:
                print(f"ok   {name}")
    print(f"{len(files)} fact file(s), {failed} failed")
    return 1 if failed or not files else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
