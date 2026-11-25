#!/usr/bin/env python3
"""Prepare the folder of one run: a copy of the case tree and of the skill, and the prompts filled in.

  python3 prepare.py --bench DIR --case L --mode A --run 1 --runs RUNS

DIR is the output of build.py. Modes: A (one agent), B (a coordinator that launches agents),
F (the coordinator taken apart in steps, protocol/coordinator-flat.md). Creates
RUNS/<case>-<mode>-<run>/ with tree/, skill/, out/ and one prompt file per agent to launch.
The answer keys are never copied: a run folder holds nothing a verifier must not see.

With --relative the prompts name tree/, skill/ and out/ relative to the run folder, which is
then the directory the session must start in: use it when the folders are prepared on one
machine and run on another (the absolute paths would be wrong there).
"""

import argparse
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import defects as D  # noqa: E402


def blocks(path):
    """The fenced blocks of a protocol file as (heading above it, text), in order. Read line by line."""
    out, heading, inside, cur = [], None, False, []
    for line in open(path, encoding="utf-8").read().split("\n"):
        if not inside and line.startswith("## "):
            heading = line[3:].strip()
        elif line.strip() == "```":
            if inside:
                out.append((heading, "\n".join(cur) + "\n"))
                cur = []
            inside = not inside
        elif inside:
            cur.append(line)
    return out


def files_of(tree, scope):
    found = []
    for s in scope:
        p = os.path.join(tree, s)
        if os.path.isdir(p):
            for r, _, fs in os.walk(p):
                found += [os.path.relpath(os.path.join(r, f), tree).replace(os.sep, "/") for f in fs]
        else:
            found.append(s)
    return sorted(found)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--bench", required=True)
    ap.add_argument("--case", required=True, choices=sorted(D.SCOPES))
    ap.add_argument("--mode", required=True, choices=["A", "B", "F"])
    ap.add_argument("--run", required=True, type=int)
    ap.add_argument("--runs", required=True)
    ap.add_argument("--relative", action="store_true", help="relative paths in the prompts")
    a = ap.parse_args()
    run = os.path.join(os.path.abspath(a.runs), f"{a.case}-{a.mode}-{a.run}")
    if os.path.exists(run):
        sys.exit(f"{run} exists")
    tree, skill, out = (os.path.join(run, x) for x in ("tree", "skill", "out"))
    shutil.copytree(os.path.join(a.bench, a.case), tree)
    shutil.copytree(os.path.join(a.bench, "base", "skills", "adversarial-verify"), skill)
    os.makedirs(out)
    files = "\n".join(files_of(tree, D.SCOPES[a.case]))
    names = ("tree", "skill", "out", ".") if a.relative else (tree, skill, out, run)
    fill = lambda t: (t.replace("{TREE}", names[0]).replace("{SKILL}", names[1]).replace("{OUT}", names[2])
                      .replace("{RUN}", names[3]).replace("{FILES}", files))
    proto = {"A": "single.md", "B": "coordinator.md", "F": "coordinator-flat.md"}[a.mode]
    src = os.path.join(HERE, "protocol", proto)
    if a.mode == "B":
        text = open(src, encoding="utf-8").read()
        open(os.path.join(run, "PROTOCOL.md"), "w", encoding="utf-8").write(
            fill("# Coordinator protocol\n\n" + text[text.index("## Roles"):]))
        for d in ("briefs", "returns"):
            os.makedirs(os.path.join(out, d))
    if a.mode == "F":
        for d in ("returns", "checked"):
            os.makedirs(os.path.join(out, d))
    seen = {}
    for name, body in blocks(src):
        if "{TREE}" not in body and "{OUT}" not in body:
            continue  # not a prompt
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        seen[slug] = seen.get(slug, 0) + 1
        suffix = f"-{seen[slug]}" if seen[slug] > 1 else ""
        open(os.path.join(run, f"prompt-{slug}{suffix}.txt"), "w", encoding="utf-8").write(fill(body))
    print(run)
    for f in sorted(os.listdir(run)):
        print("  " + f)
    return 0


if __name__ == "__main__":
    sys.exit(main())
