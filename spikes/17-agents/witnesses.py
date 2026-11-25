"""One witness per defect: witness(tree) is True when the defect can be observed in that tree.

build.py requires every witness to be False on the base tree, True on the base plus that
defect alone, and True on every case tree that carries the defect. A witness works on a
throwaway copy of the tree and never changes the tree it is given.
"""

import ast
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

PY = sys.executable
EVALS = "skills/adversarial-verify/evals/evals.json"
SKILL = "skills/adversarial-verify/SKILL.md"
TERM = "zq" + "vorblax"  # not a word of the repository


class Copy:
    """A throwaway copy of a tree."""

    def __init__(self, tree):
        self.tmp = tempfile.mkdtemp(prefix="bench-witness-")
        self.root = os.path.join(self.tmp, "t")
        shutil.copytree(tree, self.root, ignore=shutil.ignore_patterns("__pycache__", ".git"))

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def path(self, rel):
        return os.path.join(self.root, rel)

    def read(self, rel):
        return open(self.path(rel), encoding="utf-8", newline="").read()

    def write(self, rel, text):
        open(self.path(rel), "w", encoding="utf-8", newline="").write(text)

    def append(self, rel, text):
        self.write(rel, self.read(rel) + "\n" + text + "\n")

    def replace(self, rel, old, new):
        s = self.read(rel)
        assert s.count(old) == 1, (rel, old[:40], s.count(old))
        self.write(rel, s.replace(old, new))

    def check(self, *args, terms=None, env=None):
        e = {k: v for k, v in os.environ.items() if k != "CHECK_PRIVATE_TERMS"}
        e.update(env or {})
        if terms is not None:
            e["CHECK_PRIVATE_TERMS"] = terms
        return subprocess.run([PY, "-I", self.path("scripts/check.py"), "--root", self.root, *args],
                              capture_output=True, text=True, env=e)

    def unittest(self, name, env=None):
        """Run the tests of the tree's own suite whose name contains `name`."""
        e = dict(os.environ)
        e.update(env or {})
        # discover puts the folder on the path itself: with -I a plain "unittest test_check" cannot import it
        r = subprocess.run([PY, "-I", "-m", "unittest", "discover", "-s", self.path("scripts"),
                            "-p", "test_check.py", "-k", name], capture_output=True, text=True, env=e)
        assert "Ran 1 test" in r.stderr and "ImportError" not in r.stderr and "ModuleNotFound" not in r.stderr, r.stderr
        return r


def S1(tree):
    with Copy(tree) as c:
        c.write("notes.md", f"Seen at {TERM} - labs.\n")
        r = c.check(terms=f"{TERM} labs")
        assert "checked (" in r.stdout, r.stdout + r.stderr
        return "private term #" not in r.stdout  # not "private terms", which is in the summary line


def S2(tree):
    with Copy(tree) as c:
        d = json.loads(c.read(EVALS))
        d["evals"][0]["x" + TERM + "y"] = "extra"
        c.write(EVALS, json.dumps(d, indent=2, ensure_ascii=False) + "\n")
        r = c.check(terms="=" + TERM)
        assert "unexpected keys" in r.stdout or "hidden" in r.stdout, r.stdout + r.stderr
        return TERM in (r.stdout + r.stderr).lower()


def S3(tree):
    with Copy(tree) as c:
        c.append("README.md", "[![Old](https://img.shields.io/badge/skill-v9.9-blue)](x)")
        r = c.check(terms="nosuchterm7f3a")
        assert "checked (" in r.stdout, r.stdout + r.stderr
        return "version mismatch" not in r.stdout


def S4(tree):
    with Copy(tree) as c:
        c.append("README.md", "```\n~~~\n| a | b |\n|---|---|\n| 1 |\n```")
        r = c.check(terms="nosuchterm7f3a")
        assert "checked (" in r.stdout, r.stdout + r.stderr
        return "table row" in r.stdout


def M1(tree):
    if shutil.which("sh") is None:
        # no shell to run the hook with (plain Windows): read the command line the hook would run
        hook = open(os.path.join(tree, "scripts/pre-commit"), encoding="utf-8").read()
        line = next(l for l in hook.splitlines() if "scripts/check.py" in l and not l.lstrip().startswith("#"))
        return "--strict" not in line
    with Copy(tree) as c:
        git = lambda *a: subprocess.run(["git", "-C", c.root, "-c", "user.name=t", "-c", "user.email=t@example.com", *a],
                                        check=True, capture_output=True)
        git("init", "-q"); git("add", "-A"); git("commit", "-q", "-m", "base")
        env = {k: v for k, v in os.environ.items() if k != "CHECK_PRIVATE_TERMS"}
        r = subprocess.run(["sh", c.path("scripts/pre-commit")], cwd=c.root, capture_output=True, text=True, env=env)
        out = r.stdout + r.stderr
        assert "no private terms configured" in out, out
        # with --strict the missing terms are an error; the exit code alone would also
        # reflect any other defect of the tree, so it is not what the witness reads
        return "ERROR private terms: no private terms configured" not in out


def M2(tree):
    with Copy(tree) as c:
        # the check that the test claims to cover is switched off: a test that bites turns red
        c.replace("scripts/check.py",
                  'rep.error(f"{REFS_DIR}/{name}", "reference file never named in SKILL.md: nothing tells the verifier to read it")',
                  "pass")
        r = c.unittest("test_file_nobody_names")
        return r.returncode == 0


def M3(tree):
    with Copy(tree) as c:
        # a term the developer could have in the shell, present all over the repository
        r = c.unittest("test_terms_file_itself_is_not_scanned", env={"CHECK_PRIVATE_TERMS": "adversarial"})
        return r.returncode != 0


def M4(tree):
    with Copy(tree) as c:
        env = dict(os.environ, PATH="")  # no rustc, no node
        r = subprocess.run([PY, "-I", c.path("scripts/check_facts.py"), "--root", c.root],
                           capture_output=True, text=True, env=env)
        assert "fact file(s)" in r.stdout, r.stdout + r.stderr
        return r.returncode == 0


def L1(tree):
    readme = open(os.path.join(tree, "README.md"), encoding="utf-8").read()
    install = readme.split("## Install", 1)[1].split("## Update", 1)[0]
    first = re.search(r"```bash\n(.*?)```", install, re.S).group(1)
    says_whole_folder = "Copy the whole folder" in install
    copies_folder = re.search(r"^cp -r \S*skills/adversarial-verify ", first, re.M) is not None
    return says_whole_folder and not copies_folder


def L2(tree):
    readme = open(os.path.join(tree, "README.md"), encoding="utf-8").read()
    plugin = json.load(open(os.path.join(tree, ".claude-plugin/plugin.json"), encoding="utf-8"))
    said = re.search(r"\(currently ([0-9.]+)\)", readme).group(1)
    return said != plugin["version"]


def L3(tree):
    evals = json.load(open(os.path.join(tree, EVALS), encoding="utf-8"))["evals"]
    e = next(x for x in evals if x["id"] == 56)
    a = next(x for x in e["assertions"] if "are excluded" in x)
    total, parts = re.search(r"that (\d+) are excluded: (.*)$", a).groups()
    return int(total) != sum(int(n) for n in re.findall(r"(\d+) ", parts))


def L4(tree):
    with Copy(tree) as c:
        r = c.check(terms="nosuchterm7f3a")
        assert "checked (" in r.stdout, r.stdout + r.stderr
        return "has a fact file and a reason" in r.stdout


def U1(tree):
    with Copy(tree) as c:
        d = json.loads(c.read(EVALS))
        e = next(x for x in d["evals"] if x["id"] == 21)
        e["assertions"][0] = re.sub(r"^\[(substance|format)\]\s+", "", e["assertions"][0])
        c.write(EVALS, json.dumps(d, indent=2, ensure_ascii=False) + "\n")
        r = c.check(terms="nosuchterm7f3a")
        assert "checked (" in r.stdout, r.stdout + r.stderr
        return "does not start with [substance]" not in r.stdout


def U2(tree):
    src = open(os.path.join(tree, "scripts/test_check.py"), encoding="utf-8").read()
    fn = next(n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.FunctionDef) and n.name == "assert_fails")
    used = {n.id for n in ast.walk(fn) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
    return "tokens" not in used


def U3(tree):
    readme = open(os.path.join(tree, "README.md"), encoding="utf-8").read()
    says_errors = re.search(r"\*\*Neutral wording\*\*:[^\n]*reported as errors", readme) is not None
    with Copy(tree) as c:
        c.append(SKILL, "Add a NOT NULL column.")
        r = c.check(terms="nosuchterm7f3a")
        assert "WARNING" in r.stdout, r.stdout + r.stderr
        return says_errors and r.returncode == 0


ALL = {name: fn for name, fn in globals().items() if re.fullmatch(r"[SMLU]\d", name)}
