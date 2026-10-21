#!/usr/bin/env python3
"""Check the repository's own invariants before a commit.

Errors make the exit code non-zero; warnings are printed but do not block.

  1. evals.json: valid JSON; exactly the keys id/prompt/expected_output/assertions;
     integer ids 1..n in file order; non-empty prompt, expected output and
     assertions; every assertion of eval TAGGED_FROM or later starts with
     [substance] or [format] followed by text.
  2. The version in SKILL.md's frontmatter matches every skill badge in the README.
  3. No private term appears in any file content or file name. Terms come from
     CHECK_PRIVATE_TERMS (comma-separated) or the untracked file .check-private-terms
     (one per line, # for comments). Matching ignores case, accents and Unicode
     forms; the parts of a term may be joined by anything that is not a letter or
     digit (spaces, hyphens, underscores, line breaks) or by nothing. A term matches
     as a whole word (not preceded or followed by a letter or digit); a term ending
     with * also matches inside other words. Terms shorter than 4 characters give a
     warning; a term with no letters or digits is an error. JSON strings are also
     scanned after decoding escapes. A file that is not UTF-8 is still scanned
     (UTF-16 if it has a BOM, otherwise Latin-1). Terms are never printed: any
     output line containing one is masked. Without terms the check says so; with
     --strict it fails. Not caught: one word split across two lines, UTF-16 files
     without a BOM.
  4. Neutral wording: technology-bound terms in SKILL.md and README.md are warnings
     (they may appear in a list of varied examples). evals.json is excluded.
  5. Markdown tables in SKILL.md and README.md, with or without outer pipes: every
     row has as many cells as the header (escaped pipes and pipes inside inline
     code do not count; fenced code blocks are skipped).

Files checked: the files tracked by git (all files outside .git if git is not
available). With --staged, exactly the content staged for the next commit.

Usage: python3 scripts/check.py [--strict] [--staged] [--root PATH]
Requires Python 3.8 or later. On Windows use `py -3 scripts/check.py`.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata

SKILL = "skills/adversarial-verify/SKILL.md"
EVALS = "skills/adversarial-verify/evals/evals.json"
README = "README.md"
TERMS_FILE = ".check-private-terms"

EVAL_KEYS = {"id", "prompt", "expected_output", "assertions"}
TAGGED_FROM = 21  # evals written with the evals-first method carry [substance]/[format] tags
TAG_RE = re.compile(r"^\[(substance|format)\]\s+\S")

# Terms that tie the text to one language, technology or kind of software.
# Warnings only: some may appear inside a list of varied examples.
STACK_TERMS = [
    r"NOT NULL", r"\bFK\b", r"foreign key", r"\bORM\b", r"@Ignore", r"switch/when",
    r"null checks?", r"\bSQL\b", r"MySQL", r"PostgreSQL", r"SQLite", r"MongoDB",
    r"Laravel", r"Django", r"Rails", r"Spring", r"React", r"Angular", r"Vue",
    r"\bPHP\b", r"\bJava\b", r"Kotlin", r"JavaScript", r"TypeScript", r"Python",
    r"Unity", r"Godot", r"Unreal", r"\bDocker\b", r"Kubernetes", r"\bAWS\b",
]

SEP = r"[\W_]*"  # anything that is not a letter or digit, possibly nothing


def normalize(text):
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return text.casefold()


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.checked = []

    def error(self, where, msg):
        self.errors.append(f"ERROR {where}: {msg}")

    def warning(self, where, msg):
        self.warnings.append(f"WARNING {where}: {msg}")


def decode(data):
    """Decode bytes without ever giving up: UTF-8, UTF-16 with BOM, else Latin-1."""
    if data.startswith((b"\xff\xfe", b"\xfe\xff")):
        try:
            return data.decode("utf-16"), "utf-16"
        except UnicodeDecodeError:
            pass
    try:
        return data.decode("utf-8-sig"), "utf-8"
    except UnicodeDecodeError:
        return data.decode("latin-1"), "latin-1"


def read_text(root, rel, rep=None):
    with open(os.path.join(root, rel), "rb") as f:
        text, enc = decode(f.read())
    if enc != "utf-8" and rep is not None and rel in (SKILL, README, EVALS):
        rep.error(rel, f"not UTF-8 (read as {enc})")
    return text


def list_files(root):
    try:
        out = subprocess.run(["git", "-C", root, "ls-files", "-z"], capture_output=True, check=True)
        files = [f for f in out.stdout.decode("utf-8", "replace").split("\0") if f]
        if files:
            return files
    except (OSError, subprocess.CalledProcessError):
        pass
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for name in filenames:
            found.append(os.path.relpath(os.path.join(dirpath, name), root).replace(os.sep, "/"))
    return found


# 1 ---------------------------------------------------------------------------

def check_evals(root, rep):
    rep.checked.append("evals")
    try:
        data = json.loads(read_text(root, EVALS, rep))
    except (OSError, ValueError) as e:
        rep.error(EVALS, f"not valid JSON ({e.__class__.__name__}: {e})")
        return
    evals = data.get("evals") if isinstance(data, dict) else None
    if not isinstance(evals, list) or not evals:
        rep.error(EVALS, "no 'evals' list")
        return
    ids = []
    for n, e in enumerate(evals, 1):
        where = f"{EVALS} eval #{n}"
        if not isinstance(e, dict):
            rep.error(where, "not an object")
            continue
        extra, missing = sorted(set(e) - EVAL_KEYS), sorted(EVAL_KEYS - set(e))
        if extra:
            rep.error(where, f"unexpected keys {extra} (put facts in the prompt)")
        if missing:
            rep.error(where, f"missing keys {missing}")
        i = e.get("id")
        if type(i) is not int:  # bool is an int subclass: reject it
            rep.error(where, "id is not an integer")
            continue
        ids.append(i)
        where = f"{EVALS} id {i}"
        for key in ("prompt", "expected_output"):
            if key in e and (not isinstance(e[key], str) or not e[key].strip()):
                rep.error(where, f"empty {key}")
        assertions = e.get("assertions")
        if not isinstance(assertions, list) or not assertions:
            rep.error(where, "no assertions")
            continue
        for k, a in enumerate(assertions, 1):
            if not isinstance(a, str) or not a.strip():
                rep.error(where, f"empty assertion #{k}")
            elif i >= TAGGED_FROM and not TAG_RE.match(a):
                rep.error(where, f"assertion #{k} does not start with [substance] or [format] followed by text")
    dups = sorted({i for i in ids if ids.count(i) > 1})
    if dups:
        rep.error(EVALS, f"duplicate id {dups}")
    if ids != list(range(1, len(ids) + 1)):
        rep.error(EVALS, "ids are not consecutive from 1 in file order")


# 2 ---------------------------------------------------------------------------

def check_version(root, rep):
    rep.checked.append("version")
    skill = read_text(root, SKILL, rep)
    fm = re.match(r"\A---\n(.*?)\n---\n", skill.replace("\r\n", "\n"), re.S)
    m = re.search(r'^\s*version:\s*"?([0-9][0-9.]*)"?\s*$', fm.group(1), re.M) if fm else None
    badges = re.findall(r"badge/skill-v([0-9][0-9.]*)-", read_text(root, README, rep))
    if not m:
        rep.error(SKILL, "no version in the frontmatter")
    if not badges:
        rep.error(README, "no version badge")
    if m:
        for b in badges:
            if b != m.group(1):
                rep.error(README, f"version mismatch: SKILL.md says {m.group(1)}, a README badge says {b}")


# 3 ---------------------------------------------------------------------------

def load_terms(root):
    raw = os.environ.get("CHECK_PRIVATE_TERMS")
    if raw is not None:
        terms = raw.split(",")
    else:
        path = os.path.join(root, TERMS_FILE)
        if not os.path.exists(path):
            return []
        with open(path, "rb") as f:
            terms = [l for l in decode(f.read())[0].splitlines() if not l.strip().startswith("#")]
    return [t.strip() for t in terms if t.strip()]


def term_patterns(terms, rep=None, substring=False):
    """One pattern per term. By default a whole word: not preceded or followed by a
    letter or digit (hyphens, underscores, dots and slashes are boundaries). A term
    ending with * also matches inside other words."""
    pats = []
    for k, t in enumerate(terms, 1):
        whole_word = not (substring or t.endswith("*"))
        parts = re.findall(r"[^\W_]+", normalize(t.rstrip("*")))
        if not parts:
            if rep is not None:
                rep.error("private terms", f"term #{k} has no letters or digits and cannot be checked")
            continue
        if rep is not None and sum(len(p) for p in parts) < 4:
            rep.warning("private terms", f"term #{k} is shorter than 4 characters: expect false positives")
        body = SEP.join(re.escape(p) for p in parts)
        pats.append(re.compile(rf"(?<![^\W_]){body}(?![^\W_])" if whole_word else body))
    return pats


def json_strings(value):
    """Every key and string value of a JSON document, one by one."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for k, v in value.items():
            yield k
            yield from json_strings(v)
    elif isinstance(value, list):
        for v in value:
            yield from json_strings(v)


def check_private(root, files, terms, rep, strict):
    rep.checked.append("private terms")
    if not terms:
        msg = (f"no private terms configured (set CHECK_PRIVATE_TERMS or create {TERMS_FILE}); "
               "private names were NOT checked")
        (rep.error if strict else rep.warning)("private terms", msg)
        return
    pats = term_patterns(terms, rep)
    for rel in files:
        if os.path.basename(rel) == TERMS_FILE:
            continue
        for k, p in enumerate(pats, 1):
            if p.search(normalize(rel)):
                rep.error(rel, f"private term #{k} in the file name")
        try:
            text = read_text(root, rel)
        except OSError:
            rep.error(rel, "unreadable file, not checked")
            continue
        body = normalize(text)
        strings = []
        if rel.endswith(".json"):
            try:
                strings = [normalize(x) for x in json_strings(json.loads(text))]
            except ValueError:
                pass
        for k, p in enumerate(pats, 1):
            m = p.search(body)
            if m:
                rep.error(f"{rel}:{body.count(chr(10), 0, m.start()) + 1}", f"private term #{k} of the configured list")
            elif any(p.search(x) for x in strings):
                rep.error(f"{rel}:decoded", f"private term #{k} of the configured list (after decoding JSON escapes)")


# 4 ---------------------------------------------------------------------------

def check_neutral(root, rep):
    rep.checked.append("neutral wording")
    patterns = [re.compile(t) for t in STACK_TERMS]
    for rel in (SKILL, README):
        for ln, line in enumerate(read_text(root, rel).splitlines(), 1):
            for p in patterns:
                m = p.search(line)
                if m:
                    rep.warning(f"{rel}:{ln}", f"technology-bound term {m.group(0)!r}: keep it only as one of varied examples")


# 5 ---------------------------------------------------------------------------

DELIM = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")


def count_cells(line):
    s = re.sub(r"`[^`]*`", "x", line).replace("\\|", "x").strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return s.count("|") + 1


def check_tables(root, rep):
    rep.checked.append("tables")
    for rel in (SKILL, README):
        lines = read_text(root, rel).splitlines()
        fence = None
        i = 0
        while i < len(lines):
            s = lines[i].strip()
            f = re.match(r"^(`{3,}|~{3,})", s)
            if f:
                if fence is None:
                    fence = f.group(1)[0]
                elif s.startswith(fence * 3):
                    fence = None
                i += 1
                continue
            if fence is None and i > 0 and DELIM.match(lines[i]) and "|" in lines[i] + lines[i - 1]:
                header = count_cells(lines[i - 1])
                start = i
                if count_cells(lines[i]) != header:
                    rep.error(f"{rel}:{i + 1}", f"table delimiter has {count_cells(lines[i])} cells, header at line {i} has {header}")
                i += 1
                while i < len(lines) and lines[i].strip() and "|" in lines[i]:
                    n = count_cells(lines[i])
                    if n != header:
                        rep.error(f"{rel}:{i + 1}", f"table row has {n} cells, header at line {start} has {header}")
                    i += 1
                continue
            i += 1


# ----------------------------------------------------------------------------

def staged_tree(root, tmp):
    """Write the staged content into tmp; return the staged file list, or None if root is not a git repository."""
    try:
        subprocess.run(["git", "-C", root, "checkout-index", "-a", "--prefix=" + tmp + os.sep],
                       check=True, capture_output=True)
        out = subprocess.run(["git", "-C", root, "ls-files", "-z"], capture_output=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return None
    return [f for f in out.stdout.decode("utf-8", "replace").split("\0") if f]


def mask(lines, terms):
    """Hide any part of an output line (location or message) that contains a private term."""
    # substring patterns: when hiding output, err on the side of hiding too much
    pats = term_patterns(terms, substring=True)
    hit = lambda s: any(p.search(normalize(s)) for p in pats)
    out = []
    for line in lines:
        m = re.match(r"^(ERROR|WARNING) (.*?): (.*)$", line)
        if not m:
            out.append("[line hidden: it contains a private term]" if hit(line) else line)
            continue
        level, where, msg = m.groups()
        if hit(where):
            where = "[location hidden: its path contains a private term]"
        if hit(msg):
            msg = "[message hidden: it contains a private term]"
        out.append(f"{level} {where}: {msg}")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--strict", action="store_true", help="fail when no private terms are configured")
    ap.add_argument("--staged", action="store_true", help="check the content staged for the next commit")
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    args = ap.parse_args()
    terms = load_terms(args.root)  # always from the working repo: the list is never committed
    rep = Report()
    root, tmp = args.root, None
    try:
        if args.staged:
            tmp = tempfile.mkdtemp(prefix="check-staged-")
            files = staged_tree(args.root, tmp)
            if files is None:
                rep.error("--staged", "not a git repository (or git is not available)")
                files = []
            root = tmp
        else:
            files = list_files(root)
        if files or not args.staged:
            run_checks(root, files, terms, rep, args.strict)
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)
    print_report(rep, terms, args.staged)
    return 1 if rep.errors else 0


def run_checks(root, files, terms, rep, strict):
    check_evals(root, rep)
    check_version(root, rep)
    check_private(root, files, terms, rep, strict)
    check_neutral(root, rep)
    check_tables(root, rep)


def print_report(rep, terms, staged):
    for line in mask(rep.errors + rep.warnings, terms):
        print(line)
    scope = "staged content" if staged else "working tree"
    print(f"checked ({scope}): {', '.join(rep.checked)} — {len(rep.errors)} error(s), {len(rep.warnings)} warning(s)")


if __name__ == "__main__":
    sys.exit(main())
