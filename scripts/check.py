#!/usr/bin/env python3
"""Check the repository's own invariants before a commit.

Errors make the exit code non-zero; warnings are printed but do not block.

  1. evals.json: valid JSON, exactly the keys id/prompt/expected_output/assertions,
     ids unique and consecutive from 1, no empty assertion, and every assertion of
     eval TAGGED_FROM or later starts with [substance] or [format].
  2. The version in SKILL.md's frontmatter matches the README badge.
  3. No private term appears in the repository files. The terms are read from the
     environment variable CHECK_PRIVATE_TERMS (comma-separated) or from the
     untracked file .check-private-terms (one per line, # for comments). They are
     never printed. Without terms the check says so; with --strict it fails.
  4. Neutral wording: technology-bound terms in SKILL.md and README.md are reported
     as warnings (they may appear legitimately in a list of varied examples).
     evals.json is excluded: concrete cases are allowed there.
  5. Markdown tables in SKILL.md and README.md: every row has as many cells as the
     header (escaped pipes and pipes inside inline code do not count).

Usage: python3 scripts/check.py [--strict] [--root PATH]
"""

import argparse
import json
import os
import re
import sys

SKILL = os.path.join("skills", "adversarial-verify", "SKILL.md")
EVALS = os.path.join("skills", "adversarial-verify", "evals", "evals.json")
README = "README.md"
TERMS_FILE = ".check-private-terms"

EVAL_KEYS = {"id", "prompt", "expected_output", "assertions"}
TAGGED_FROM = 21  # evals written with the evals-first method carry [substance]/[format] tags
TAGS = ("[substance]", "[format]")

# Terms that tie the text to one language, technology or kind of software.
# Warnings only: some may appear inside a list of varied examples.
STACK_TERMS = [
    r"NOT NULL", r"\bFK\b", r"foreign key", r"\bORM\b", r"@Ignore", r"switch/when",
    r"null checks?", r"\bSQL\b", r"MySQL", r"PostgreSQL", r"SQLite", r"MongoDB",
    r"Laravel", r"Django", r"Rails", r"Spring", r"React", r"Angular", r"Vue",
    r"\bPHP\b", r"\bJava\b", r"Kotlin", r"JavaScript", r"TypeScript", r"Python",
    r"Unity", r"Godot", r"Unreal", r"\bDocker\b", r"Kubernetes", r"\bAWS\b",
]


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.checked = []

    def error(self, where, msg):
        self.errors.append(f"ERROR {where}: {msg}")

    def warning(self, where, msg):
        self.warnings.append(f"WARNING {where}: {msg}")


def read(root, path):
    with open(os.path.join(root, path), encoding="utf-8") as f:
        return f.read()


def check_evals(root, rep):
    rep.checked.append("evals")
    try:
        data = json.loads(read(root, EVALS))
    except (OSError, ValueError) as e:
        rep.error(EVALS, f"not valid JSON ({e.__class__.__name__}: {e})")
        return
    evals = data.get("evals") if isinstance(data, dict) else None
    if not isinstance(evals, list) or not evals:
        rep.error(EVALS, "no 'evals' list")
        return
    seen = set()
    ids = []
    for n, e in enumerate(evals, 1):
        where = f"{EVALS} eval #{n}"
        if not isinstance(e, dict):
            rep.error(where, "not an object")
            continue
        keys = set(e)
        if keys != EVAL_KEYS:
            extra = sorted(keys - EVAL_KEYS)
            missing = sorted(EVAL_KEYS - keys)
            if extra:
                rep.error(where, f"unexpected keys {extra} (put facts in the prompt)")
            if missing:
                rep.error(where, f"missing keys {missing}")
        i = e.get("id")
        if not isinstance(i, int):
            rep.error(where, "id is not an integer")
            continue
        where = f"{EVALS} id {i}"
        if i in seen:
            rep.error(where, "duplicate id")
        seen.add(i)
        ids.append(i)
        assertions = e.get("assertions")
        if not isinstance(assertions, list) or not assertions:
            rep.error(where, "no assertions")
            continue
        for a in assertions:
            if not isinstance(a, str) or not a.strip():
                rep.error(where, "empty assertion")
            elif i >= TAGGED_FROM and not a.startswith(TAGS):
                rep.error(where, f"assertion does not start with [substance] or [format]: {a[:60]!r}")
    if sorted(ids) != list(range(1, len(ids) + 1)) and len(ids) == len(seen):
        rep.error(EVALS, f"ids are not consecutive from 1 (found {sorted(ids)[:3]}...{sorted(ids)[-3:]})")


def check_version(root, rep):
    rep.checked.append("version")
    m = re.search(r'^\s*version:\s*"?([0-9][0-9.]*)"?\s*$', read(root, SKILL), re.M)
    b = re.search(r"badge/skill-v([0-9][0-9.]*)-", read(root, README))
    if not m:
        rep.error(SKILL, "no version in the frontmatter")
    if not b:
        rep.error(README, "no version badge")
    if m and b and m.group(1) != b.group(1):
        rep.error(README, f"version mismatch: SKILL.md says {m.group(1)}, README badge says {b.group(1)}")


def load_terms(root):
    raw = os.environ.get("CHECK_PRIVATE_TERMS")
    if raw is not None:
        return [t.strip() for t in raw.split(",") if t.strip()]
    path = os.path.join(root, TERMS_FILE)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return [l.strip() for l in f if l.strip() and not l.strip().startswith("#")]
    return None


def repo_files(root):
    skip = {".git", "__pycache__"}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip]
        for name in filenames:
            if name == TERMS_FILE:
                continue
            p = os.path.join(dirpath, name)
            yield os.path.relpath(p, root)


def check_private(root, rep, strict):
    rep.checked.append("private terms")
    terms = load_terms(root)
    if not terms:
        msg = (f"no private terms configured (set CHECK_PRIVATE_TERMS or create {TERMS_FILE}); "
               "private names were NOT checked")
        (rep.error if strict else rep.warning)("private terms", msg)
        return
    patterns = [re.compile(r"(?<![\w-])" + re.escape(t) + r"(?![\w-])", re.I) for t in terms]
    for rel in repo_files(root):
        try:
            text = read(root, rel)
        except (UnicodeDecodeError, OSError):
            continue
        for ln, line in enumerate(text.splitlines(), 1):
            for k, p in enumerate(patterns, 1):
                if p.search(line):
                    # never print the term or the line: the list itself is private
                    rep.error(f"{rel}:{ln}", f"private term #{k} of the configured list")


def check_neutral(root, rep):
    rep.checked.append("neutral wording")
    patterns = [(t, re.compile(t)) for t in STACK_TERMS]
    for rel in (SKILL, README):
        for ln, line in enumerate(read(root, rel).splitlines(), 1):
            for t, p in patterns:
                m = p.search(line)
                if m:
                    rep.warning(f"{rel}:{ln}", f"technology-bound term {m.group(0)!r}: keep it only as one of varied examples")


def cells(line):
    # drop inline code spans and escaped pipes before counting separators
    line = re.sub(r"`[^`]*`", "", line).replace("\\|", "")
    return line.count("|")


def check_tables(root, rep):
    rep.checked.append("tables")
    for rel in (SKILL, README):
        lines = read(root, rel).splitlines()
        in_fence = False
        i = 0
        while i < len(lines):
            s = lines[i].strip()
            if s.startswith("```"):
                in_fence = not in_fence
            if not in_fence and s.startswith("|"):
                header = cells(s)
                start = i
                while i < len(lines) and lines[i].strip().startswith("|"):
                    n = cells(lines[i].strip())
                    if n != header:
                        rep.error(f"{rel}:{i + 1}", f"table row has {n} separators, header at line {start + 1} has {header}")
                    i += 1
                continue
            i += 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--strict", action="store_true", help="fail when no private terms are configured")
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    args = ap.parse_args()
    rep = Report()
    check_evals(args.root, rep)
    check_version(args.root, rep)
    check_private(args.root, rep, args.strict)
    check_neutral(args.root, rep)
    check_tables(args.root, rep)
    for line in rep.errors + rep.warnings:
        print(line)
    print(f"checked: {', '.join(rep.checked)} — {len(rep.errors)} error(s), {len(rep.warnings)} warning(s)")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
