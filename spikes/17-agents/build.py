#!/usr/bin/env python3
"""Build the case trees of the bench (spike #17) and prove that every inserted defect is one.

  python3 spikes/17-agents/build.py --out DIR            # base, tuning, S, M, L and the answer keys
  python3 spikes/17-agents/build.py --out DIR --profile  # also: which defects the repository's own
                                                         # checks and tests already catch

DIR/base        the base commit, untouched
DIR/<case>      the base commit plus the defects of that case: this is what a verifier gets
DIR/keys/       the answer keys, one per case (never give them to a verifier)

Every witness must be False on the base, True on the base plus its defect alone and True on
each case that carries the defect; in a case that does not carry it, it must be False. If one
of these fails the build stops: a defect that cannot be shown is not part of the bench.
Run it from a clone that has the base commit. Requires git, python3, and rustc and node
(the repository's fact files use them).
"""

import argparse
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import defects as D  # noqa: E402
import witnesses as W  # noqa: E402

REPO = os.path.dirname(os.path.dirname(HERE))


def export(dst):
    os.makedirs(dst)
    # as committed: no line-ending conversion, whatever the machine's git settings are
    tar = subprocess.run(["git", "-C", REPO, "-c", "core.autocrlf=false", "-c", "core.eol=lf", "archive",
                          "--format=tar", D.BASE], capture_output=True, check=True).stdout
    with tarfile.open(fileobj=io.BytesIO(tar)) as t:
        t.extractall(dst)
    shutil.rmtree(os.path.join(dst, "spikes"), ignore_errors=True)  # the bench is never part of a case


def apply(tree, defect):
    """Apply one defect; return the 1-based first and last line of the inserted text."""
    path = os.path.join(tree, defect["file"])
    text = open(path, encoding="utf-8", newline="").read()  # newline="": the bytes stay as they are
    if text.count(defect["old"]) != 1:
        sys.exit(f"{defect['id']}: 'old' occurs {text.count(defect['old'])} times in {defect['file']}")
    start = text.index(defect["old"])
    open(path, "w", encoding="utf-8", newline="").write(text.replace(defect["old"], defect["new"]))
    first = text.count("\n", 0, start) + 1
    return first, first + defect["new"].rstrip("\n").count("\n")


def suite(tree, env):
    """The tree's own unit tests. discover puts the folder on the path: with -I a plain run cannot import them."""
    r = subprocess.run([sys.executable, "-I", "-m", "unittest", "discover", "-s", os.path.join(tree, "scripts"),
                        "-p", "test_check.py"], capture_output=True, text=True, env=env)
    if "ImportError" in r.stderr or "ModuleNotFound" in r.stderr or "Ran 0 tests" in r.stderr:
        sys.exit("the tree's test suite did not run:\n" + r.stderr[-600:])
    return r


def own_checks(tree):
    """Which of the repository's own mechanisms turn red on this tree (a throwaway copy: the suite writes into it)."""
    env = {k: v for k, v in os.environ.items() if k != "CHECK_PRIVATE_TERMS"}
    env.update(CHECK_PRIVATE_TERMS="nosuchterm7f3a", PYTHONDONTWRITEBYTECODE="1")
    chk = subprocess.run([sys.executable, "-I", os.path.join(tree, "scripts/check.py"), "--strict", "--root", tree],
                         capture_output=True, text=True, env=env)
    fct = subprocess.run([sys.executable, "-I", os.path.join(tree, "scripts/check_facts.py"), "--root", tree],
                         capture_output=True, text=True, env=env)
    tst = suite(tree, env)
    return {"check.py": chk.returncode != 0, "test_check.py": tst.returncode != 0, "check_facts.py": fct.returncode != 0}


def copy(src, dst):
    shutil.copytree(src, dst)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", required=True)
    ap.add_argument("--profile", action="store_true")
    args = ap.parse_args()
    out = os.path.abspath(args.out)
    if os.path.exists(out):
        sys.exit(f"{out} exists: give a new directory")
    base = os.path.join(out, "base")
    export(base)
    os.makedirs(os.path.join(out, "keys"))
    by_id = {d["id"]: d for d in D.DEFECTS}
    problems = []

    # 1. each defect alone
    alone = os.path.join(out, "_alone")
    profile = {}
    if args.profile:  # a profile means something only if the base is clean
        t = os.path.join(alone, "base")
        copy(base, t)
        red = [name for name, r in own_checks(t).items() if r]
        if red:
            sys.exit(f"the base tree is red on its own {red}: the profile would say that everything is caught")
        print("base: green on its own check.py, test_check.py and check_facts.py", flush=True)
    for d in D.DEFECTS:
        w = W.ALL[d["id"]]
        if w(base):
            problems.append(f"{d['id']}: the witness is already true on the base")
        t = os.path.join(alone, d["id"])
        copy(base, t)
        apply(t, d)
        if not w(t):
            problems.append(f"{d['id']}: the witness is false with the defect applied")
        if args.profile:
            profile[d["id"]] = own_checks(t)
            print(d["id"], "caught by:", [k for k, v in profile[d["id"]].items() if v] or "nothing", flush=True)
    shutil.rmtree(alone, ignore_errors=True)

    # 2. the cases
    for case, scope in D.SCOPES.items():
        tree = os.path.join(out, case)
        copy(base, tree)
        key = []
        for d in D.DEFECTS:
            if case not in d["cases"]:
                continue
            first, last = apply(tree, d)
            key.append({"id": d["id"], "file": d["file"], "first_line": first, "last_line": last,
                        "domain": d["domain"], "category": d["category"], "summary": d["summary"],
                        "keywords": d["keywords"], **({"caught_by": profile[d["id"]]} if args.profile else {})})
        # a later defect in the same file can move an earlier one: recompute the lines on the final tree
        for k in key:
            text = open(os.path.join(tree, k["file"]), encoding="utf-8", newline="").read()
            new = by_id[k["id"]]["new"]
            if text.count(new) != 1:
                problems.append(f"{case}/{k['id']}: the inserted text occurs {text.count(new)} times in the case tree")
                continue
            k["first_line"] = text.count("\n", 0, text.index(new)) + 1
            k["last_line"] = k["first_line"] + new.rstrip("\n").count("\n")
        for d in D.DEFECTS:
            seen = W.ALL[d["id"]](tree)
            if seen != (case in d["cases"]):
                problems.append(f"{case}/{d['id']}: witness is {seen}, expected {case in d['cases']}")
        size = 0
        for s in scope:
            p = os.path.join(tree, s)
            if os.path.isdir(p):
                size += sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(p) for f in fs)
            else:
                size += os.path.getsize(p)
        json.dump({"case": case, "base": D.BASE, "scope": scope, "scope_bytes": size, "defects": key},
                  open(os.path.join(out, "keys", case + ".json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"{case}: {len(key)} defects, scope {size} bytes ({', '.join(scope)})", flush=True)

    for case in list(D.SCOPES) + ["base"]:
        left = [r for r, ds, _ in os.walk(os.path.join(out, case)) if "__pycache__" in ds]
        if left:
            problems.append(f"{case}: files written by a run were left in the tree ({left[0]})")
    if problems:
        print("\n".join("PROBLEM " + p for p in problems))
        return 1
    print("every witness holds: false on the base, true with its defect, true only in its cases")
    return 0


if __name__ == "__main__":
    sys.exit(main())
