"""Tests for scripts/check.py: the repo passes, and each invariant fails on a case built to break it.

Run from the repo root: python3 -m unittest scripts/test_check.py
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join("skills", "adversarial-verify", "SKILL.md")
EVALS = os.path.join("skills", "adversarial-verify", "evals", "evals.json")

# Built at run time so that no test term appears literally in any repo file,
# including this one (the check scans every file).
NONE = "-".join(["no", "such", "term", "7f3a"])
SECRET = "secret" + "proj"


class CheckTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        for item in ("README.md", "skills", ".claude-plugin", "scripts"):
            src = os.path.join(ROOT, item)
            dst = os.path.join(self.tmp, item)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy(src, dst)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def run_check(self, *args, env_terms=None, terms_file=None):
        env = {k: v for k, v in os.environ.items() if k != "CHECK_PRIVATE_TERMS"}
        if env_terms is not None:
            env["CHECK_PRIVATE_TERMS"] = env_terms
        if terms_file is not None:
            with open(os.path.join(self.tmp, ".check-private-terms"), "w") as f:
                f.write(terms_file)
        return subprocess.run(
            [sys.executable, "-I", os.path.join(self.tmp, "scripts", "check.py"), "--root", self.tmp, *args],
            capture_output=True, text=True, env=env,
        )

    def assert_fails(self, r, *tokens):
        """A failure counts only if the script ran, reported an ERROR and named what failed."""
        self.assertNotEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("checked:", r.stdout, "the script did not run to its summary")
        self.assertIn("ERROR", r.stdout)
        for t in tokens:
            self.assertIn(t, r.stdout)

    def assert_passes(self, r):
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("checked:", r.stdout, "the script did not run to its summary")
        self.assertNotIn("ERROR", r.stdout)

    def edit(self, path, old, new):
        p = os.path.join(self.tmp, path)
        s = open(p, encoding="utf-8").read()
        self.assertIn(old, s)
        open(p, "w", encoding="utf-8").write(s.replace(old, new, 1))

    def evals(self):
        p = os.path.join(self.tmp, EVALS)
        return p, json.load(open(p, encoding="utf-8"))

    # --- the repo as it is ---

    def test_repo_passes(self):
        self.assert_passes(self.run_check(env_terms=NONE))

    # --- 1. evals ---

    def test_broken_json_fails(self):
        p = os.path.join(self.tmp, EVALS)
        open(p, "a").write("{")
        self.assert_fails(self.run_check(env_terms=NONE), "evals.json")

    def test_duplicate_id_fails(self):
        p, d = self.evals()
        d["evals"][-1]["id"] = d["evals"][-2]["id"]
        json.dump(d, open(p, "w"), indent=2)
        self.assert_fails(self.run_check(env_terms=NONE), "duplicate id")

    def test_gap_in_ids_fails(self):
        p, d = self.evals()
        d["evals"][-1]["id"] += 5
        json.dump(d, open(p, "w"), indent=2)
        self.assert_fails(self.run_check(env_terms=NONE), "consecutive")

    def test_extra_key_fails(self):
        p, d = self.evals()
        d["evals"][-1]["context"] = "facts outside the prompt"
        json.dump(d, open(p, "w"), indent=2)
        self.assert_fails(self.run_check(env_terms=NONE), "context")

    def test_empty_assertion_fails(self):
        p, d = self.evals()
        d["evals"][0]["assertions"].append("  ")
        json.dump(d, open(p, "w"), indent=2)
        self.assert_fails(self.run_check(env_terms=NONE), "empty assertion")

    def test_untagged_assertion_in_new_eval_fails(self):
        p, d = self.evals()
        d["evals"][-1]["assertions"][0] = "Does something without a tag"
        json.dump(d, open(p, "w"), indent=2)
        self.assert_fails(self.run_check(env_terms=NONE), "[substance]")

    # --- 2. version ---

    def test_version_mismatch_fails(self):
        self.edit("README.md", "badge/skill-v", "badge/skill-v9")
        self.assert_fails(self.run_check(env_terms=NONE), "version")

    # --- 3. private names ---

    def test_private_term_from_env_fails(self):
        self.edit(SKILL, "## Overview", "## Overview\n\nSeen first in " + SECRET.capitalize() + ".")
        r = self.run_check(env_terms=SECRET + ", other")
        self.assert_fails(r, "SKILL.md", "private term")
        self.assertNotIn(SECRET, r.stdout.lower(), "the forbidden term itself must not be printed")

    def test_private_term_from_file_fails(self):
        self.edit("README.md", "## What it catches", "## What it catches\n\nAs in " + SECRET + "-x.")
        self.assert_fails(self.run_check(terms_file="# private\n" + SECRET + "-x\n"), "README.md", "private term")

    def test_missing_terms_is_said_not_silent(self):
        r = self.run_check()
        self.assert_passes(r)
        self.assertIn("no private terms configured", r.stdout)

    def test_missing_terms_fails_in_strict_mode(self):
        self.assert_fails(self.run_check("--strict"), "no private terms configured")

    def test_terms_file_is_gitignored(self):
        self.assertIn(".check-private-terms", open(os.path.join(ROOT, ".gitignore")).read())

    # --- 4. neutral wording: warning only ---

    def test_stack_term_warns_without_failing(self):
        self.edit(SKILL, "## Overview", "## Overview\n\nAdd a NOT NULL column.")
        r = self.run_check(env_terms=NONE)
        self.assert_passes(r)
        self.assertIn("WARNING", r.stdout)
        self.assertIn("NOT NULL", r.stdout)

    def test_stack_term_in_evals_is_ignored(self):
        # eval 16 names SQLite and PostgreSQL on purpose: they are examples, not guidance
        self.assertIn("SQLite", open(os.path.join(self.tmp, EVALS)).read())
        r = self.run_check(env_terms=NONE)
        self.assert_passes(r)
        self.assertNotIn("evals.json", r.stdout.split("checked:")[0])

    # --- 5. tables ---

    def test_broken_table_row_fails(self):
        self.edit(SKILL, "| **Frequency assumptions** |", "| **Frequency assumptions** ")
        self.assert_fails(self.run_check(env_terms=NONE), "table")

    def test_escaped_pipe_is_not_a_separator(self):
        self.edit(SKILL, "| **Frequency assumptions** |", "| **Frequency \\| assumptions** |")
        self.assert_passes(self.run_check(env_terms=NONE))


if __name__ == "__main__":
    unittest.main()
