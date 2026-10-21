#!/usr/bin/env python3
"""Run the files that check the facts stated in the evals (skills/adversarial-verify/evals/facts).

Each file reproduces what an eval's prompt states as fact (a run's result, a
computed value, which mutants a test kills) and exits non-zero if the fact is
false. Python files run with the interpreter that runs this script; .rs files
are compiled with rustc; .ts files run with node --experimental-strip-types.
A missing toolchain is an error, never a silent skip. TypeScript files are run
with their types stripped, not type-checked.

A fact file must contain at least one assertion outside comments and strings
(Python: an assert or raise statement; Rust: assert!, assert_eq!, assert_ne!,
panic!; TypeScript: throw), and its last line of output must be "ok <id>": a file
that asserts nothing or stops early fails.

  python3 scripts/check_facts.py                 # all files
  python3 scripts/check_facts.py 38 49           # only these eval ids
  python3 scripts/check_facts.py --root DIR      # the files under another checkout
"""

import argparse
import ast
import os
import shutil
import subprocess
import sys
import tempfile

import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACTS_REL = os.path.join("skills", "adversarial-verify", "evals", "facts")
EXTS = (".py", ".rs", ".ts")
ASSERTS = {".rs": re.compile(r"\b(assert|assert_eq|assert_ne|panic)!"), ".ts": re.compile(r"\bthrow\b")}
STRIP = re.compile(r'//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|`(?:\\.|[^`\\])*`', re.S)


def has_assertion(path):
    text = open(path, encoding="utf-8").read()
    ext = os.path.splitext(path)[1]
    if ext == ".py":
        try:
            tree = ast.parse(text)
        except SyntaxError:
            return True  # let the run report the syntax error
        return any(isinstance(n, (ast.Assert, ast.Raise)) for n in ast.walk(tree))
    return bool(ASSERTS[ext].search(STRIP.sub(" ", text)))


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


def tail(text, n=5):
    lines = [l for l in text.strip().splitlines() if l.strip()]
    errs = [l for l in lines if l.startswith("error")]
    return " | ".join((errs or lines)[-n:])


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("ids", nargs="*", help="eval ids to run (default: all)")
    ap.add_argument("--root", default=ROOT, help="checkout whose fact files to run")
    args = ap.parse_args(argv)
    root, ids = args.root, args.ids
    FACTS = os.path.join(root, FACTS_REL)
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
            stem = os.path.splitext(name)[0]
            if not has_assertion(path):
                print(f"FAIL {name}: no assertion outside comments and strings")
                failed += 1
                continue
            for step in steps:
                r = subprocess.run(step, cwd=FACTS, capture_output=True, text=True)
                if r.returncode != 0:
                    print(f"FAIL {name}: {tail(r.stderr or r.stdout)}")
                    failed += 1
                    break
            else:
                out = [l for l in r.stdout.strip().splitlines() if l.strip()]
                if out[-1:] != [f"ok {stem}"]:
                    print(f"FAIL {name}: last line of output is not 'ok {stem}'")
                    failed += 1
                else:
                    print(f"ok   {name}")
    print(f"{len(files)} fact file(s), {failed} failed")
    return 1 if failed or not files else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
