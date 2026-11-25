"""The known defects of the bench (spike #17). ANSWER KEY: never give this file to a verifier.

Each defect is one replacement in one file of the base commit. `old` must occur exactly
once in that file. `cases` says which case trees carry it. `keywords`: any of them in a
finding's row counts as a match when the cited line is off (lower case, matched without case).
The proof that each one is a defect is its witness in witnesses.py.
"""

BASE = "cb75e4eab25d32d64f19ca5dcfa6c10cb385ae4d"  # main after PR #31

CHECK = "scripts/check.py"
TESTS = "scripts/test_check.py"
FACTS = "scripts/check_facts.py"
HOOK = "scripts/pre-commit"
README = "README.md"
EVALS = "skills/adversarial-verify/evals/evals.json"
NOT_COMPUTABLE = "skills/adversarial-verify/evals/facts/NOT_COMPUTABLE"

# What the verifier is asked to verify in each case (the whole tree is readable).
SCOPES = {
    "tuning": ["scripts/", README],
    "S": [CHECK],
    "M": ["scripts/"],
    "L": ["scripts/", README, "CHANGELOG.md", ".claude-plugin/plugin.json", "skills/adversarial-verify/evals/"],
}

DEFECTS = [
    # ---- S: in scripts/check.py, present in S, M and L (the same four defects at three sizes)
    dict(id="S1", cases=["S", "M", "L"], file=CHECK, domain="Code", category="spec drift",
         summary="A private term whose parts are joined by more than one separator character (e.g. ' - ', "
                 "a line break with indentation) is no longer found: the docstring promises any separators.",
         old='SEP = r"[\\W_]*"  # anything that is not a letter or digit, possibly nothing',
         new='SEP = r"[\\W_]?"  # anything that is not a letter or digit, possibly nothing',
         keywords=["sep", "separator"]),
    dict(id="S2", cases=["S", "M", "L"], file=CHECK, domain="Code", category="hidden behavior",
         summary="Output masking uses whole-word patterns for '=' terms, so a private term glued to other "
                 "letters is printed by another check's message: the comment above says to hide too much.",
         old="    pats = term_patterns(terms, substring=True)",
         new="    pats = term_patterns(terms)",
         keywords=["mask", "substring"]),
    dict(id="S3", cases=["S", "M", "L"], file=CHECK, domain="Code", category="missing completeness",
         summary="Only the first README badge is compared with the skill's version: the docstring says every badge.",
         old="        for b in badges:\n            if b != m.group(1):",
         new="        for b in badges[:1]:\n            if b != m.group(1):",
         keywords=["badges[:1]", "first badge", "every badge", "every skill badge"]),
    dict(id="S4", cases=["S", "M", "L"], file=CHECK, domain="Code", category="stale state",
         summary="Any fence line closes an open fenced block, also one of the other kind (~~~ inside ```), "
                 "so a table inside a code block is checked and reported.",
         old="                elif s.startswith(fence * 3):\n                    fence = None",
         new="                else:\n                    fence = None",
         keywords=["fence"]),
    # ---- M: the rest of scripts/, present in M and L
    dict(id="M1", cases=["M", "L"], file=HOOK, domain="Code", category="silent fallthrough",
         summary="The hook no longer passes --strict: with no private terms configured the commit goes "
                 "through unchecked, while the comment two lines above still says --strict fails.",
         old='"$py" -I "$root/scripts/check.py" --strict --staged --root "$root" || exit 1',
         new='"$py" -I "$root/scripts/check.py" --staged --root "$root" || exit 1',
         keywords=["--strict", "strict"]),
    dict(id="M2", cases=["M", "L"], file=TESTS, domain="Tests", category="tautological test",
         summary="test_file_nobody_names asserts that 'orphan.md' is in a string the test itself builds: "
                 "it passes whatever the check does.",
         old='            f.write("# Orphan\\n\\nNobody points here.\\n")\n'
             '        self.assert_fails(self.run_check(terms=NONE), "orphan.md", "never named in SKILL.md")',
         new='            f.write("# Orphan\\n\\nNobody points here.\\n")\n'
             '        r = self.run_check(terms=NONE)\n'
             '        self.assertIn("orphan.md", r.stdout + self.ref("orphan.md"))',
         keywords=["test_file_nobody_names", "tautolog", "always pass", "always true"]),
    dict(id="M3", cases=["M", "L"], file=TESTS, domain="Tests", category="test-environment artifact",
         summary="run_check no longer removes CHECK_PRIVATE_TERMS from the environment: tests that pass their "
                 "terms in a file get the developer's own terms instead, and their result depends on the shell.",
         old='        env = {k: v for k, v in os.environ.items() if k != "CHECK_PRIVATE_TERMS"}',
         new="        env = dict(os.environ)",
         keywords=["check_private_terms", "os.environ", "environment"]),
    dict(id="M4", cases=["M", "L"], file=FACTS, domain="Code", category="silent fallthrough",
         summary="A fact file whose toolchain is missing is skipped and not counted as failed: the docstring "
                 "says a missing toolchain is an error, never a silent skip.",
         old='                print(f"FAIL {name}: toolchain not found")\n                failed += 1\n                continue',
         new='                print(f"skip {name}: toolchain not found")\n                continue',
         keywords=["toolchain", "silent skip"]),
    # ---- L: docs and data, present in L only
    dict(id="L1", cases=["L"], file=README, domain="Documentation", category="broken instructions",
         summary="The first install command copies only SKILL.md, while the same section says that SKILL.md "
                 "alone sends the verifier to reference files that are not there.",
         old="```bash\ncp -r skills/adversarial-verify ~/.claude/skills/\n```",
         new="```bash\nmkdir -p ~/.claude/skills/adversarial-verify\n"
             "cp skills/adversarial-verify/SKILL.md ~/.claude/skills/adversarial-verify/\n```",
         keywords=["cp skills/adversarial-verify/skill.md", "install", "whole folder"]),
    dict(id="L2", cases=["L"], file=README, domain="Documentation", category="version mismatch",
         summary="The README says the plugin is currently 4.1; plugin.json, the badge, the frontmatter and "
                 "the changelog say 4.2, and check.py does not compare this sentence.",
         old="(currently 4.2)", new="(currently 4.1)",
         keywords=["currently 4.1"]),
    dict(id="L3", cases=["L"], file=EVALS, domain="Data", category="false fact in an eval",
         summary="Eval 56 rewards a wrong number: its assertion says 11 mutants are excluded, but lists "
                 "8 + 3 + 1 = 12, and its expected output says 12.",
         old="says that 12 are excluded: 8 timed out, 3 skipped, 1 not measured",
         new="says that 11 are excluded: 8 timed out, 3 skipped, 1 not measured",
         keywords=["11 are excluded", "eval 56", "id 56"]),
    dict(id="L4", cases=["L"], file=NOT_COMPUTABLE, domain="Data", category="schema inconsistency",
         summary="Eval 52 has both a fact file (52.rs) and a reason not to have one: the repository's own "
                 "check rejects that.",
         old="50: a console game menu described in words\n",
         new="50: a console game menu described in words\n52: the compiler is not installed on every machine\n",
         keywords=["52"]),
    # ---- tuning: a separate tree, for adjusting the coordinator's protocol. Never scored.
    dict(id="U1", cases=["tuning"], file=CHECK, domain="Code", category="boundary",
         summary="Eval 21 is no longer required to carry [substance]/[format] tags: the docstring says "
                 "'eval TAGGED_FROM or later'.",
         old="            elif i >= TAGGED_FROM and not TAG_RE.match(a):",
         new="            elif i > TAGGED_FROM and not TAG_RE.match(a):",
         keywords=["tagged_from"]),
    dict(id="U2", cases=["tuning"], file=TESTS, domain="Tests", category="tautological test",
         summary="assert_fails never looks at its tokens: every test that expects a failure for a named "
                 "reason accepts any failure.",
         old="        for t in tokens:\n            self.assertIn(t, r.stdout)\n        self.assert_no_leak(r)",
         new="        self.assert_no_leak(r)",
         keywords=["tokens", "assert_fails"]),
    dict(id="U3", cases=["tuning"], file=README, domain="Documentation", category="API drift",
         summary="The README says technology-bound terms are reported as errors; check.py reports warnings "
                 "and exits 0.",
         old="README.md are reported as warnings.", new="README.md are reported as errors.",
         keywords=["reported as errors", "neutral wording"]),
]
