"""Tests for scripts/check.py: the repo passes, and each invariant fails on a case built to break it.

Run from the repo root: python3 -m unittest scripts/test_check.py
Every failing case must come from the script's own ERROR and summary, and no
private test term may ever be printed.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join("skills", "adversarial-verify", "SKILL.md")
EVALS = os.path.join("skills", "adversarial-verify", "evals", "evals.json")

# Built at run time so that no test term appears literally in any repo file,
# including this one (the check scans every file). Neither occurs in the repo.
NONE = "nosuch" + "term7f3a"  # a single word: separators inside a term match loosely
T1 = "zq" + "vorblax"                 # one-word private term
T2 = "quil" + "lane " + "dor" + "vex"  # two-word private term


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        for item in ("README.md", "skills", ".claude-plugin", "scripts", ".gitignore"):
            src, dst = os.path.join(ROOT, item), os.path.join(self.tmp, item)
            if os.path.isdir(src):
                shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))
            else:
                shutil.copy(src, dst)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_check(self, *args, terms=None, terms_file=None):
        env = {k: v for k, v in os.environ.items() if k != "CHECK_PRIVATE_TERMS"}
        if terms is not None:
            env["CHECK_PRIVATE_TERMS"] = terms
        if terms_file is not None:
            with open(os.path.join(self.tmp, ".check-private-terms"), "wb") as f:
                f.write(terms_file)
        return subprocess.run(
            [sys.executable, "-I", os.path.join(self.tmp, "scripts", "check.py"), "--root", self.tmp, *args],
            capture_output=True, text=True, env=env,
        )

    def assert_fails(self, r, *tokens):
        """A failure counts only if the script ran, reported an ERROR and named what failed."""
        out = r.stdout + r.stderr
        self.assertNotEqual(r.returncode, 0, out)
        self.assertIn("checked (", r.stdout, "the script did not run to its summary:\n" + out)
        self.assertIn("ERROR", r.stdout)
        for t in tokens:
            self.assertIn(t, r.stdout)
        self.assert_no_leak(r)

    def assert_passes(self, r):
        out = r.stdout + r.stderr
        self.assertEqual(r.returncode, 0, out)
        self.assertIn("checked (", r.stdout, "the script did not run to its summary:\n" + out)
        self.assertNotIn("ERROR", r.stdout)

    def assert_no_leak(self, r):
        low = (r.stdout + r.stderr).lower()
        for t in (T1, T2, T2.replace(" ", "")):
            self.assertNotIn(t, low, "a private term was printed")

    def path(self, rel):
        return os.path.join(self.tmp, rel)

    def edit(self, rel, old, new):
        s = open(self.path(rel), encoding="utf-8").read()
        self.assertIn(old, s)
        open(self.path(rel), "w", encoding="utf-8").write(s.replace(old, new, 1))

    def append(self, rel, text):
        with open(self.path(rel), "a", encoding="utf-8") as f:
            f.write("\n" + text + "\n")

    def evals(self):
        with open(self.path(EVALS), encoding="utf-8") as f:
            return json.load(f)

    def save_evals(self, d):
        with open(self.path(EVALS), "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2, ensure_ascii=False)


class RepoTest(Base):
    def test_repo_passes(self):
        self.assert_passes(self.run_check(terms=NONE))

    def test_repo_passes_strict(self):
        self.assert_passes(self.run_check("--strict", terms=NONE))


class EvalsTest(Base):
    def test_broken_json(self):
        open(self.path(EVALS), "a").write("{")
        self.assert_fails(self.run_check(terms=NONE), "not valid JSON")

    def test_duplicate_id(self):
        d = self.evals(); d["evals"][-1]["id"] = d["evals"][-2]["id"]; self.save_evals(d)
        self.assert_fails(self.run_check(terms=NONE), "duplicate id")

    def test_gap(self):
        d = self.evals(); d["evals"][-1]["id"] += 5; self.save_evals(d)
        self.assert_fails(self.run_check(terms=NONE), "consecutive")

    def test_duplicate_and_gap_both_reported(self):
        d = self.evals(); d["evals"][-1]["id"] = 1; d["evals"].append(dict(d["evals"][0], id=99)); self.save_evals(d)
        self.assert_fails(self.run_check(terms=NONE), "duplicate id", "consecutive")

    def test_swapped_order(self):
        d = self.evals(); d["evals"][0], d["evals"][1] = d["evals"][1], d["evals"][0]; self.save_evals(d)
        self.assert_fails(self.run_check(terms=NONE), "consecutive")

    def test_boolean_id(self):
        d = self.evals(); d["evals"][0]["id"] = True; self.save_evals(d)
        self.assert_fails(self.run_check(terms=NONE), "id is not an integer")

    def test_extra_key(self):
        d = self.evals(); d["evals"][-1]["context"] = "facts outside the prompt"; self.save_evals(d)
        self.assert_fails(self.run_check(terms=NONE), "context")

    def test_missing_key(self):
        d = self.evals(); del d["evals"][-1]["expected_output"]; self.save_evals(d)
        self.assert_fails(self.run_check(terms=NONE), "missing keys")

    def test_empty_prompt(self):
        d = self.evals(); d["evals"][3]["prompt"] = "   "; self.save_evals(d)
        self.assert_fails(self.run_check(terms=NONE), "empty prompt")

    def test_empty_assertion(self):
        d = self.evals(); d["evals"][0]["assertions"].append("  "); self.save_evals(d)
        self.assert_fails(self.run_check(terms=NONE), "empty assertion")

    def test_untagged_assertion_in_new_eval(self):
        d = self.evals(); d["evals"][-1]["assertions"][0] = "Does something"; self.save_evals(d)
        self.assert_fails(self.run_check(terms=NONE), "[substance]")

    def test_untagged_assertion_at_the_boundary(self):
        d = self.evals()
        e = [x for x in d["evals"] if x["id"] == 21][0]
        e["assertions"][0] = "Does something"; self.save_evals(d)
        self.assert_fails(self.run_check(terms=NONE), "id 21")

    def test_old_untagged_eval_is_accepted(self):
        d = self.evals()
        e = [x for x in d["evals"] if x["id"] == 20][0]
        self.assertFalse(e["assertions"][0].startswith("["), "eval 20 is untagged by design")
        self.assert_passes(self.run_check(terms=NONE))

    def test_tag_without_text(self):
        d = self.evals(); d["evals"][-1]["assertions"][0] = "[format]"; self.save_evals(d)
        self.assert_fails(self.run_check(terms=NONE), "followed by text")


class VersionTest(Base):
    def test_badge_mismatch(self):
        self.edit("README.md", "badge/skill-v", "badge/skill-v9")
        self.assert_fails(self.run_check(terms=NONE), "version mismatch")

    def test_second_badge_mismatch(self):
        self.append("README.md", "![old](https://img.shields.io/badge/skill-v2.0-blue)")
        self.assert_fails(self.run_check(terms=NONE), "version mismatch")

    def test_version_outside_frontmatter_does_not_count(self):
        s = open(self.path(SKILL), encoding="utf-8").read()
        v = re.search(r'version: "([0-9.]+)"', s).group(1)
        s = s.replace(f'  version: "{v}"\n', "", 1) + f'\n```\nversion: "{v}"\n```\n'
        open(self.path(SKILL), "w", encoding="utf-8").write(s)
        self.assert_fails(self.run_check(terms=NONE), "no version in the frontmatter")


class PrivateTest(Base):
    def leak(self, text, rel=SKILL):
        self.append(rel, text)
        return self.run_check(terms=f"{T1},{T2}")

    def test_exact(self):
        self.assert_fails(self.leak(f"Seen in {T1}."), "private term #1")

    def test_case(self):
        self.assert_fails(self.leak(f"Seen in {T1.upper()}."), "private term #1")

    def test_hyphen_suffix_and_prefix(self):
        self.assert_fails(self.leak(f"See {T1}-labs and my-{T1}."), "private term #1")

    def test_underscore(self):
        self.assert_fails(self.leak(f"{T1}_labs"), "private term #1")

    def test_glued_forms_caught_by_default(self):
        for form in (f"{T1.capitalize()}Labs", f"{T1}2026", f"{T1}s", f"my{T1}"):
            with self.subTest(form=form.lower().replace(T1, "T")):
                self.tearDown(); self.setUp()
                self.append(SKILL, form)
                self.assert_fails(self.run_check(terms=T1), "private term #1")

    def test_whole_word_opt_in(self):
        self.append(SKILL, f"{T1.capitalize()}Labs and {T1}-x")
        self.assert_fails(self.run_check(terms="=" + T1), "private term #1")  # the hyphenated form
        self.tearDown(); self.setUp()
        self.append(SKILL, f"{T1.capitalize()}Labs")
        self.assert_passes(self.run_check(terms="=" + T1))  # glued form: not a whole word

    def test_whole_word_avoids_false_positives(self):
        prefix = "adver" + "saria"  # a prefix of a word used all over the repo, built at run time
        self.assert_fails(self.run_check(terms=prefix), "private term #1")
        self.assert_passes(self.run_check(terms="=" + prefix))

    def test_short_term_warns(self):
        r = self.run_check(terms="zq" + "v")
        self.assert_passes(r)
        self.assertIn("shorter than 4 characters", r.stdout)

    def test_short_whole_word_term_gets_no_redundant_hint(self):
        r = self.run_check(terms="=" + "zq" + "v")
        self.assert_passes(r)
        self.assertIn("shorter than 4 characters", r.stdout)
        self.assertNotIn("prefix it with =", r.stdout)

    def test_term_without_letters_is_an_error(self):
        self.assert_fails(self.run_check(terms="--"), "no letters or digits")

    def test_inside_url(self):
        self.assert_fails(self.leak(f"https://example.com/{T1}-docs"), "private term #1")

    def test_accented(self):
        self.assert_fails(self.leak(f"Seen in {T1.replace('o', 'ó')}."), "private term #1")

    def test_two_words_joined_any_way(self):
        a, b = T2.split()
        for variant in (f"{a}-{b}", f"{a}_{b}", f"{a}{b}", f"{a}\n{b}", f"{a.upper()}  {b}"):
            with self.subTest(variant=variant.replace(a.upper(), "A").replace(a, "A").replace(b, "B")):
                self.tearDown(); self.setUp()
                self.assert_fails(self.leak(f"Seen in {variant}."), "private term #2")

    def test_file_name(self):
        name = os.path.join("skills", "adversarial-verify", f"{T1}-notes.md")
        open(self.path(name), "w").write("clean\n")
        self.assert_fails(self.run_check(terms=T1), "file name", "location hidden")

    def test_latin1_file(self):
        open(self.path("notes.txt"), "wb").write(f"caf\xe9 {T1}\n".encode("latin-1"))
        self.assert_fails(self.run_check(terms=T1), "notes.txt", "private term #1")

    def test_utf16_file(self):
        open(self.path("notes16.txt"), "wb").write(f"{T1}\n".encode("utf-16"))
        self.assert_fails(self.run_check(terms=T1), "notes16.txt")

    def test_json_escaped_key(self):
        escaped = "".join(f"\\u{ord(c):04x}" for c in T1)
        p = self.path(os.path.join(".claude-plugin", "plugin.json"))
        d = open(p, encoding="utf-8").read().replace('"name":', f'"{escaped}": 1, "name":', 1)
        open(p, "w", encoding="utf-8").write(d)
        self.assert_fails(self.run_check(terms=T1), "after decoding JSON escapes")

    def test_json_escape(self):
        escaped = "".join(f"\\u{ord(c):04x}" for c in T1)
        p = self.path(os.path.join(".claude-plugin", "plugin.json"))
        d = open(p, encoding="utf-8").read().replace('"description": "', f'"description": "{escaped} ', 1)
        open(p, "w", encoding="utf-8").write(d)
        self.assert_fails(self.run_check(terms=T1), "plugin.json")

    def test_terms_file_with_bom_and_comments(self):
        self.append(SKILL, f"Seen in {T1}.")
        r = self.run_check(terms_file=("﻿" + f"{T1}\n# a comment\n").encode("utf-8"))
        self.assert_fails(r, "private term #1")

    def test_bom_before_a_comment_keeps_it_a_comment(self):
        # with the BOM read as text, "# skill" would become the term "skill" and fail every file
        r = self.run_check("--strict", terms_file=("\ufeff# skill\n" + NONE + "\n").encode("utf-8"))
        self.assert_passes(r)

    def test_terms_file_itself_is_not_scanned(self):
        self.assert_passes(self.run_check(terms_file=f"{T1}\n".encode()))

    def test_leak_through_another_check_is_masked(self):
        # the evals check prints unexpected key names: a key named after the term must be masked
        d = self.evals(); d["evals"][-1][f"{T1}_notes"] = "x"; self.save_evals(d)
        self.assert_fails(self.run_check(terms=T1), "message hidden")

    def test_glued_term_in_output_is_masked_even_if_not_detected(self):
        # whole-word detection does not flag "<term>labs", but the evals check prints the key name
        d = self.evals(); d["evals"][-1][f"{T1}labs"] = "x"; self.save_evals(d)
        self.assert_fails(self.run_check(terms=T1), "message hidden")

    def test_whole_word_term_glued_in_output_is_still_masked(self):
        # "=" terms are detected as whole words only, but output masking must stay substring
        d = self.evals(); d["evals"][-1][f"{T1}labs"] = "x"; self.save_evals(d)
        self.assert_fails(self.run_check(terms="=" + T1), "message hidden")

    def test_assertion_text_is_never_printed(self):
        d = self.evals(); d["evals"][-1]["assertions"][0] = f"Mentions {T1} internals"; self.save_evals(d)
        self.assert_fails(self.run_check(terms=T1), "assertion #1")

    def test_unreadable_file_is_an_error(self):
        os.symlink(os.path.join(self.tmp, "does-not-exist"), self.path("dangling.md"))
        self.assert_fails(self.run_check(terms=T1), "unreadable file")

    def test_missing_terms_is_said_not_silent(self):
        r = self.run_check()
        self.assert_passes(r)
        self.assertIn("no private terms configured", r.stdout)

    def test_missing_terms_fails_in_strict_mode(self):
        self.assert_fails(self.run_check("--strict"), "no private terms configured")

    def test_empty_env_fails_in_strict_mode(self):
        self.assert_fails(self.run_check("--strict", terms=" , "), "no private terms configured")

    def test_terms_file_is_gitignored(self):
        self.assertIn(".check-private-terms", open(os.path.join(ROOT, ".gitignore")).read().split())


@unittest.skipUnless(shutil.which("git"), "git not available")
class StagedTest(Base):
    def git(self, *args):
        env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example.com",
                   GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@example.com")
        subprocess.run(["git", "-C", self.tmp, *args], check=True, capture_output=True, env=env)

    def setUp(self):
        super().setUp()
        self.git("init", "-q")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "base")

    def test_staged_leak_with_clean_working_tree(self):
        open(self.path("leak.md"), "w").write(f"{T1}\n")
        self.git("add", "leak.md")
        open(self.path("leak.md"), "w").write("clean\n")
        self.assert_fails(self.run_check("--staged", terms=T1), "leak.md")
        self.assert_passes(self.run_check(terms=T1))  # the working tree alone looks clean

    def test_staged_outside_git_is_a_clear_error(self):
        shutil.rmtree(self.path(".git"))
        before = {d for d in os.listdir(tempfile.gettempdir()) if d.startswith("check-staged-")}
        r = self.run_check("--staged", terms=T1)
        self.assert_fails(r, "not a git repository")
        self.assertNotIn("Traceback", r.stderr)
        after = {d for d in os.listdir(tempfile.gettempdir()) if d.startswith("check-staged-")}
        self.assertEqual(after - before, set(), "temporary directory left behind")

    def test_untracked_files_are_not_checked(self):
        os.makedirs(self.path(".venv"))
        open(self.path(os.path.join(".venv", "x.txt")), "w").write(f"{T1}\n")
        self.assert_passes(self.run_check(terms=T1))
        self.assert_passes(self.run_check("--staged", terms=T1))


class NeutralTest(Base):
    def test_stack_term_warns_without_failing(self):
        self.append(SKILL, "Add a NOT NULL column.")
        r = self.run_check(terms=NONE)
        self.assert_passes(r)
        self.assertIn("WARNING", r.stdout)
        self.assertIn("NOT NULL", r.stdout)

    def test_evals_are_excluded(self):
        self.assertIn("SQLite", open(self.path(EVALS)).read())
        r = self.run_check(terms=NONE)
        self.assert_passes(r)
        self.assertNotIn("evals.json", r.stdout.split("checked (")[0])


class TablesTest(Base):
    def test_row_missing_a_separator(self):
        self.edit(SKILL, "| **Frequency assumptions** |", "| **Frequency assumptions** ")
        self.assert_fails(self.run_check(terms=NONE), "table row")

    def test_row_lost_leading_pipe_and_a_cell(self):
        self.edit(SKILL, "| **Frequency assumptions** |", "**Frequency assumptions** ")
        self.assert_fails(self.run_check(terms=NONE), "table row")

    def test_table_without_outer_pipes(self):
        self.append(SKILL, "\nA | B | C\n--- | --- | ---\n1 | 2\n")
        self.assert_fails(self.run_check(terms=NONE), "table row")

    def test_delimiter_with_wrong_cell_count(self):
        self.append(SKILL, "\n| A | B | C |\n|---|---|\n| 1 | 2 | 3 |\n")
        self.assert_fails(self.run_check(terms=NONE), "table delimiter")

    def test_row_without_outer_pipes_in_a_piped_table_is_fine(self):
        self.append(SKILL, "\n| A | B | C |\n|---|---|---|\n1 | 2 | 3\n")
        self.assert_passes(self.run_check(terms=NONE))

    def test_escaped_pipe_and_code_span_are_not_separators(self):
        self.edit(SKILL, "| **Frequency assumptions** |", "| **Frequency \\| `a|b` assumptions** |")
        self.assert_passes(self.run_check(terms=NONE))

    def test_broken_table_inside_a_fence_is_ignored(self):
        for fence in ("```", "~~~"):
            with self.subTest(fence=fence):
                self.tearDown(); self.setUp()
                self.append(SKILL, f"\n{fence}\n| a | b |\n|---|---|\n| 1 |\n{fence}\n")
                self.assert_passes(self.run_check(terms=NONE))


FACTS = os.path.join("skills", "adversarial-verify", "evals", "facts")


class FactsTest(Base):
    def first_reasoned_id(self):
        for line in open(self.path(os.path.join(FACTS, "NOT_COMPUTABLE")), encoding="utf-8"):
            if line[:1].isdigit():
                return int(line.split(":")[0])
        self.fail("NOT_COMPUTABLE has no entry")

    def test_eval_with_facts_but_no_file_or_reason(self):
        i = self.first_reasoned_id()
        self.edit(os.path.join(FACTS, "NOT_COMPUTABLE"), f"{i}:", "# removed:")
        self.assert_fails(self.run_check(terms=NONE), f"id {i}", "no fact file")

    def test_new_eval_with_facts_needs_a_file(self):
        d = self.evals()
        n = len(d["evals"]) + 1
        d["evals"].append({"id": n, "prompt": "Verify it. (Facts: the test passes.)",
                           "expected_output": "x", "assertions": ["[substance] x"]})
        self.save_evals(d)
        self.assert_fails(self.run_check(terms=NONE), f"id {n}", "no fact file")

    def test_new_eval_with_a_file_passes(self):
        d = self.evals()
        n = len(d["evals"]) + 1
        d["evals"].append({"id": n, "prompt": "Verify it. (Facts: 1 + 1 is 2.)",
                           "expected_output": "x", "assertions": ["[substance] x"]})
        self.save_evals(d)
        import hashlib
        h = hashlib.sha256(d["evals"][-1]["prompt"].encode("utf-8")).hexdigest()
        open(self.path(os.path.join(FACTS, f"{n}.py")), "w").write(f"# prompt-sha256: {h}\nassert 1 + 1 == 2\n")
        self.assert_passes(self.run_check(terms=NONE))

    def test_prompt_changed_after_its_facts(self):
        # A prompt edited to contradict its fact file must fail until the facts are checked again.
        d = self.evals()
        d["evals"][36]["prompt"] = d["evals"][36]["prompt"].replace("day > 31", "day > 28")
        self.save_evals(d)
        self.assert_fails(self.run_check(terms=NONE), "37.py", "prompt changed since its facts were checked")

    def test_fact_file_without_hash(self):
        self.edit(os.path.join(FACTS, "40.py"), "# prompt-sha256:", "# no hash:")
        self.assert_fails(self.run_check(terms=NONE), "40.py", "no 'prompt-sha256:' line")

    def test_orphan_fact_file(self):
        open(self.path(os.path.join(FACTS, "999.py")), "w").write("pass\n")
        self.assert_fails(self.run_check(terms=NONE), "999.py", "does not exist")

    def test_file_and_reason_both(self):
        i = self.first_reasoned_id()
        open(self.path(os.path.join(FACTS, f"{i}.py")), "w").write("pass\n")
        self.assert_fails(self.run_check(terms=NONE), "NOT_COMPUTABLE", f"eval {i} has a fact file and a reason")

    def test_reason_without_text(self):
        self.append(os.path.join(FACTS, "NOT_COMPUTABLE"), "77:")
        self.assert_fails(self.run_check(terms=NONE), "NOT_COMPUTABLE:", "expected '<id>: <reason>'")

    def run_facts(self, *ids):
        return subprocess.run([sys.executable, os.path.join(self.tmp, "scripts", "check_facts.py"), *ids],
                              capture_output=True, text=True)

    def test_runner_passes_on_the_repo(self):
        r = self.run_facts()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertRegex(r.stdout, r"\d+ fact file\(s\), 0 failed")

    def test_runner_fails_on_a_false_fact(self):
        # The first draft of eval 38 stated round(10.05 * 0.9, 2) == 9.04: the runner must catch it.
        self.edit(os.path.join(FACTS, "38.py"), "assert round(10.05 * 0.9, 2) == 9.05", "assert round(10.05 * 0.9, 2) == 9.04")
        r = self.run_facts("38")
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertIn("FAIL 38.py", r.stdout)

    def test_runner_fails_on_a_file_that_asserts_nothing(self):
        self.edit(os.path.join(FACTS, "49.py"), "assert clipped(375)", "x = clipped(375)")
        self.edit(os.path.join(FACTS, "49.py"), "assert clipped(320)", "x = clipped(320)")
        self.edit(os.path.join(FACTS, "49.py"), "assert clipped(430)", "x = clipped(430)")
        r = self.run_facts("49")
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertIn("no assertion", r.stdout)

    def test_runner_fails_without_the_ok_line(self):
        self.edit(os.path.join(FACTS, "40.py"), "print('ok 40')", "print('done')")
        r = self.run_facts("40")
        self.assertNotEqual(r.returncode, 0, r.stdout)
        self.assertIn("not 'ok 40'", r.stdout)

    def test_runner_fails_on_no_files(self):
        r = self.run_facts("12345")
        self.assertNotEqual(r.returncode, 0, r.stdout)


if __name__ == "__main__":
    unittest.main()
