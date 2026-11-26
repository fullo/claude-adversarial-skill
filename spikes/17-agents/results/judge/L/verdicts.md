1: not a defect - tree/README.md:255 - The rule is documented as keyed on a `(Facts: …)` block, and evals 54/55 (evals.json:672, :686) have none, so leaving them out is the documented behaviour, not a missed case.
2: real defect - tree/skills/adversarial-verify/evals/facts/35.py:3 - 35.py imports parse_day_v1 from _parse_day, but the helper's header comment names only 37.py and 39.py.
3: not a defect - tree/scripts/check.py:34 - The docstring and README.md:255 define "states facts" as carrying the "(Facts" marker; CHANGELOG.md:24 is a loose history summary, and 54/55 carry no Facts block.
4: not a defect - tree/README.md:255 - The literal marker is the documented contract of the check, and evals 54/55/42 follow it (42 also has a fact file), so nothing escapes the check as specified.
5: real defect - tree/scripts/pre-commit:9 - Both checkers run from `$root/scripts/` (the working tree), not from the index copy, so a staged checker change is not the code that checks the commit.
6: real defect - tree/scripts/test_check.py:32 - setUp copies a fixed list without LICENSE into a folder that is not a git repo, so check.py takes the os.walk fallback (check.py:153) and the test never covers the git ls-files path or LICENSE.
7: real defect - tree/scripts/test_check.py:351 - os.symlink with no guard raises OSError on Windows without symlink privilege, and README.md:264 says Windows is supported; that is a false red.
8: real defect - tree/scripts/check.py:345 - count_cells treats code spans as opaque, but GFM splits cells on an unescaped pipe even inside backticks, so a row the check accepts (test at test_check.py:442) renders with extra cells.
9: real defect - tree/scripts/check_facts.py:50 - ast.walk counts any Assert/Raise node anywhere, including in functions that are never called, so a file that asserts nothing at run time passes the assertion check.
10: cannot tell - tree/scripts/test_check.py:414 - open() without encoding uses the locale codec on a UTF-8 file that has 11 non-ASCII characters; whether this raises depends on the machine's locale and the exact bytes.
11: real defect - tree/scripts/check.py:494 - Reasons are stored with no check that the id exists, is ≥29, states facts or is unique.
12: real defect - tree/scripts/test_check.py:337 - The test uses terms=T1 (a substring term, check.py:265), so "<term>labs" is detected; the comment describes the "=" case covered by the next test (:341-344).
13: real defect - tree/scripts/test_check.py:338 - With a plain T1 the glued key is detected as a substring, so this test duplicates :331-334 and its comment is wrong.
14: real defect - tree/scripts/check.py:433 - With --staged, root is the index export, so untracked reference files are not seen (test_check.py:508 asserts this); the docstring at :43-44 says "tracked or not".
15: real defect - tree/scripts/check.py:301 - Every file whose basename is .check-private-terms is skipped, at any depth and even when tracked, which goes against README.md:251 "The list is never committed".
16: real defect - tree/scripts/test_check.py:516 - None of the listed cases has a test (missing toolchain, .rs/.ts detection, no badge, no version entry, non-UTF-8 SKILL.md, FACTS_FROM boundary, mixed fences).
17: real defect - tree/scripts/test_check.py:351 - The unguarded os.symlink errors on Windows without symlink privilege, a false red on a supported platform (README.md:264).
18: real defect - tree/scripts/pre-commit:9 - The hook runs check.py with --staged but without --strict, while README.md:261 (and pre-commit:5) say it runs --strict --staged.
19: real defect - tree/skills/adversarial-verify/evals/facts/35.py:2 - The docstring states that the three valid-date tests do not cover the case, but the file only asserts the parse result, and that part of the prompt (evals.json:440) cannot be computed.
20: real defect - tree/scripts/check.py:341 - DELIM requires at least 3 hyphens per cell, while GFM accepts one, so such tables are never recognised or counted (no instance today).
21: real defect - tree/scripts/test_check.py:391 - The test compares check-staged-* entries in the shared system temp folder, so another run at the same time can make it fail.
22: real defect - tree/scripts/pre-commit:17 - $out is printed only when rc≠0, and check_facts.py exits 0 after printing "skip … toolchain not found" (check_facts.py:92, :113), so the skip is never seen.
23: real defect - tree/scripts/check.py:214 - read_text in check_version is not wrapped for OSError (only ValueError at :228), so a missing SKILL.md/README/plugin.json/CHANGELOG ends in a traceback with no summary.
24: real defect - tree/skills/adversarial-verify/evals/evals.json:329 - SKILL.md and references/*.md contain no rule about issue trackers, duplicates or issues, yet evals 25-26 grade that behaviour.
25: real defect - tree/scripts/check.py:478 - Only the prompt is hashed, and the drift already exists: evals.json:705 says 11 excluded while 8+3+1=12 (facts/56.py:12).
26: real defect - tree/README.md:46 - SKILL.md:462 also lists CHANGELOG.md, ADR/ and the agent instruction files, which the README list leaves out.
27: real defect - tree/scripts/test_check.py:503 - This test calls git with no skipUnless(shutil.which("git")) guard, unlike StagedTest at :369.
28: real defect - tree/scripts/check.py:43 - The docstring says the folder is read "tracked or not", but with --staged root is the index copy (:433), which test_check.py:508 relies on.
29: real defect - tree/scripts/test_check.py:571 - No test covers a missing toolchain, .rs/.ts detection, --staged with an empty index, the FACTS_FROM boundary, mixed fences or the hook, and the skip defect sits on one of these paths.
30: real defect - tree/scripts/pre-commit:17 - Output is shown only on failure, so the exit-0 toolchain skip from check_facts.py:92 is invisible at commit time.
31: real defect - tree/scripts/test_check.py:337 - The comment describes whole-word ("=") detection, but the test passes a plain term.
32: real defect - tree/skills/adversarial-verify/evals/facts/52.rs:9 - panic!("bad month") in the function under test matches the ASSERTS regex (check_facts.py:34), so the file would pass with every assert removed from main.
33: real defect - tree/scripts/check.py:473 - with_file is keyed by id, so a second fact file with the same stem replaces the first and only one hash is checked, while check_facts.py runs both.
34: real defect - tree/scripts/test_check.py:316 - The token "plugin.json" matches any error on that file (e.g. a version mismatch), so the test does not prove that the decoded-escape detection fired.
35: real defect - tree/scripts/check.py:301 - A file named .check-private-terms at any path, tracked or not, is exempt from the scan, which contradicts README.md:251.
36: real defect - tree/scripts/check_facts.py:37 - The Rust strip pattern ignores raw strings and '"' char literals, so a '"' can swallow code up to the next quote and detection can go wrong.
37: real defect - tree/scripts/test_check.py:64 - assert_passes never calls assert_no_leak (it is called only at :62), although :4-5 says no test term may ever be printed.
38: not a defect - tree/scripts/check.py:46 - Walking every file when git is unavailable is the documented behaviour, and "working tree" is still a true label for that scope.
39: real defect - tree/scripts/check.py:317 - A .json file that does not parse silently skips the decoded-escape scan, so a \uXXXX-escaped term goes unreported with no note.
40: not a defect - tree/scripts/check_facts.py:67 - A node too old for --experimental-strip-types exits non-zero and is reported as FAIL, so the run still fails as README.md:255 promises; only the message is generic.
41: real defect - tree/scripts/check.py:494 - Reasons are never checked against existing eval ids or against evals that state facts.
42: not a defect - tree/skills/adversarial-verify/evals/facts/52.rs:15 - A redundant assertion (implied by :14) is harmless and makes no false claim, and the other examples are not defects either.
43: real defect - tree/scripts/check.py:478 - Only the prompt is bound, and eval 56's assertion (evals.json:705, "11 excluded") already contradicts facts/56.py:12 (12).
44: real defect - tree/scripts/check.py:436 - With --staged and an empty index, files == [], so no check runs and the script exits 0 with "0 error(s)".
45: real defect - tree/skills/adversarial-verify/evals/evals.json:249 - The quoted summary line is the old one; SKILL.md:439 now reads "(code, data, tests, UX) … mock-ups".
46: real defect - tree/scripts/check.py:511 - Check 7 scans only SKILL.md and the reference files, so a rename would leave the reference-file table in README.md:113-115 stale without any report.
47: real defect - tree/scripts/test_check.py:503 - There is no git skip guard here and no symlink guard at :351, so both are false reds on machines without git or without symlink privilege.
48: real defect - tree/scripts/check.py:469 - The `_` helper carries no hash even though its comment (:5) says it copies functions from evals 29/35/37/39, which contradicts README.md:255 "every eval it covers".
49: real defect - tree/scripts/check_facts.py:85 - A requested id with no file is silently dropped from the list, and the run exits 0 if the other ids pass.
50: real defect - tree/scripts/check.py:436 - An empty staged list skips every check and returns 0.
51: real defect - tree/scripts/check.py:137 - Only .md files in references/ are considered, but README.md:254 says "every file in references/".
52: real defect - tree/scripts/pre-commit:15 - check_facts.py is run from the working tree against the staged copy (same for check.py at :9), so the committed checker code is not what ran.
53: real defect - tree/README.md:46 - Step 5 at SKILL.md:462 also covers CHANGELOG.md, ADR/ and the agent instruction files.
54: real defect - tree/scripts/check.py:473 - 35.py plus 35.ts would collide in with_file, so only the later file's prompt-sha256 is checked.
55: real defect - tree/scripts/test_check.py:503 - git is called with no skipUnless guard, unlike StagedTest at :369.
56: real defect - tree/scripts/check.py:477 - Each file is bound to one eval through its stem and one hash, so README.md:255 "every eval it covers" describes a multi-eval binding that does not exist.
57: real defect - tree/scripts/check.py:478 - Only the prompt is hashed, and evals.json:612 and :705 already drift from facts/49.py:13 and facts/56.py:12.
58: real defect - tree/scripts/check.py:248 - An exported but empty CHECK_PRIVATE_TERMS is "not None", so it replaces the terms file with an empty list, which the hook (no --strict, pre-commit:9) only warns about.
59: real defect - tree/scripts/pre-commit:9 - The hook does not pass --strict, contrary to README.md:261.
60: real defect - tree/skills/adversarial-verify/evals/facts/_parse_day.py:1 - 35.py:3 also imports parse_day_v1, and the function's own comment at :5 names eval 35.
61: real defect - tree/scripts/check.py:473 - Two fact files for one id overwrite each other in with_file, so only one hash is checked.
62: not a defect - tree/scripts/check.py:29 - evals.json is deliberately left out of the neutral-wording rule, and these assertions name concrete things to look for in a given target rather than skill wording.
63: real defect - tree/CHANGELOG.md:5 - The "first entry below" is "## Unreleased", while check.py:237 compares the first numbered entry.
64: real defect - tree/README.md:46 - The list leaves out CHANGELOG.md, ADR/ and the agent instruction files that SKILL.md:462 names.
65: not a defect - tree/README.md:247 - check.py itself runs on python3 alone (it falls back to walking files without git, check.py:151-158), and --staged/the hook only make sense inside a git checkout.
66: real defect - tree/scripts/check.py:301 - The basename match exempts a tracked .check-private-terms at any depth from the scan.
67: real defect - tree/scripts/test_check.py:32 - LICENSE and any new top-level file are not copied, so test_repo_passes does not cover the whole repository.
68: real defect - tree/scripts/pre-commit:17 - check_facts.py exits 0 on a missing toolchain (check_facts.py:92, :113, against its own docstring at :8), and the hook throws that output away, so the commit passes silently.
69: real defect - tree/scripts/check.py:478 - Only the prompt is bound, and the numbers restated at evals.json:612 and :705 contradict the fact files.
70: real defect - tree/scripts/check.py:494 - Duplicate, unknown, below-29 and fact-less ids in NOT_COMPUTABLE are all accepted with no message.
71: not a defect - tree/scripts/check.py:440 - Best-effort removal of a temp folder that only failed to clean up does not affect any check result, and test_check.py:396 covers the normal path.
72: real defect - tree/skills/adversarial-verify/evals/facts/49.py:13 - At 320 px the same two labels are clipped as at 375 px (the assertion at evals.json:615 agrees), so "more labels are clipped" (:612) is false.
73: real defect - tree/scripts/test_check.py:339 - terms=T1 is a substring term, so the case "masked even if not detected" is never exercised by this test.
74: cannot tell - tree/scripts/check_facts.py:100 - text=True decodes with the locale codec, so whether rustc/node output can raise UnicodeDecodeError depends on the platform and the output.
75: real defect - tree/scripts/check.py:433 - With --staged, root = tmp, so untracked reference files are not seen, which contradicts the docstring at :43.
76: real defect - tree/scripts/test_check.py:339 - The test runs with a plain term, so the whole-word case its name describes is never run, and it duplicates :331-334.
77: real defect - tree/scripts/check.py:473 - Same-stem fact files with two extensions overwrite each other, so one of them escapes the hash check.
78: not a defect - tree/scripts/check_facts.py:67 - An old node rejects --experimental-strip-types and the file is reported as FAIL, so the run fails as README.md:255 says.
79: real defect - tree/skills/adversarial-verify/evals/facts/35.py:3 - 35.py also imports _parse_day, which the header comment of _parse_day.py:1 leaves out.
80: real defect - tree/skills/adversarial-verify/evals/facts/35.py:2 - The docstring claims "the three valid-date tests do not cover" the case, which no line checks, and the body matches 37.py.
81: real defect - tree/skills/adversarial-verify/evals/facts/_parse_day.py:1 - The comment names only 37.py and 39.py, though 35.py:3 also depends on the helper.
82: not a defect - tree/scripts/check.py:500 - A misnamed file (42.PY, 53.mts) leaves its eval with no fact file, so a Facts eval is still reported, and the `_` exemption is the intended helper convention.
83: not a defect - tree/README.md:72 - The forced-variety rule requires at least 3 techniques at standard depth, so grading 3 while the prompt names 2 is consistent with the skill.
84: real defect - tree/scripts/check.py:473 - A second file for the same id overwrites the first in with_file, so only one is hash-checked.
85: not a defect - tree/scripts/test_check.py:604 - The test is named and meant to check that --root is accepted after positional ids (argument parsing), which it does check.
86: real defect - tree/scripts/check.py:436 - An empty index gives files == [], so no check runs and the script exits 0 with "0 error(s)".
87: not a defect - tree/scripts/test_check.py:604 - The test targets argument order (--root after ids), not whether --root is honoured, and it would fail if parsing rejected that order.
88: real defect - tree/scripts/check_facts.py:85 - A mistyped or zero-padded id matches no file and is dropped with no message.
89: real defect - tree/CHANGELOG.md:3 - The first entry below is "## Unreleased", while the check uses the first numbered entry (check.py:237) and compares only the first badge (check.py:223).
90: real defect - tree/scripts/check_facts.py:50 - `assert True`, or an assert inside a function that is never called, satisfies the AST walk.
91: real defect - tree/skills/adversarial-verify/evals/evals.json:249 - The quoted line is out of date against SKILL.md:439.
92: real defect - tree/skills/adversarial-verify/evals/evals.json:329 - No rule about issue trackers, duplicate search or issues exists in SKILL.md or references/*.md.
93: real defect - tree/scripts/check.py:341 - `-{3,}` rejects the 1- and 2-hyphen delimiter cells that GFM accepts, so such tables go unchecked.
94: real defect - tree/CHANGELOG.md:3 - "First entry below" points at the unnumbered "## Unreleased" (:5), while the check uses the first numbered entry.
95: real defect - tree/scripts/check.py:469 - `_`-prefixed helpers are exempt from any prompt hash, so _parse_day.py can drift from the prompts it copies.
96: real defect - tree/scripts/check.py:316 - A .json file that does not parse is scanned raw only, and nothing says that \u escapes were not decoded.
97: real defect - tree/scripts/check.py:248 - A set but empty CHECK_PRIVATE_TERMS overrides the terms file, and the hook (no --strict) only warns about it.
98: real defect - tree/CHANGELOG.md:5 - The first entry below is "## Unreleased", not the numbered entry that check.py:237 compares.
99: real defect - tree/scripts/check.py:477 - One hash per file, bound to the stem's eval, and the shared helper carries none, so README.md:255 overstates the binding.
100: real defect - tree/skills/adversarial-verify/evals/evals.json:249 - The quoted summary line differs from SKILL.md:439.
101: real defect - tree/scripts/check.py:317 - On invalid JSON the decoded-string scan is silently dropped.
102: real defect - tree/scripts/check.py:494 - A reason for a nonexistent or fact-less eval is stored without any check.
103: real defect - tree/scripts/check.py:151 - CalledProcessError (not a repo, dubious ownership, etc.) also falls back to walking every file, while :46 says the fallback happens only when git is unavailable.
104: real defect - tree/CHANGELOG.md:3 - The sentence points at "## Unreleased" (:5), but check.py:237 uses the first numbered entry.
105: real defect - tree/scripts/check_facts.py:92 - A missing rustc or node only prints "skip" and leaves failed at 0, so test_runner_passes_on_the_repo (test_check.py:575-578) stays green without running 52.rs or 53.ts.
106: real defect - tree/skills/adversarial-verify/evals/facts/35.py:3 - 35.py also uses the helper, which the header comment of _parse_day.py:1 does not mention.
107: real defect - tree/skills/adversarial-verify/evals/facts/49.py:13 - The clipped set at 320 px equals the one at 375 px, so "more labels are clipped" (evals.json:612) is wrong.
108: real defect - tree/scripts/test_check.py:372 - The env copies os.environ with no GIT_CONFIG_GLOBAL/NOSYSTEM override, so global git settings such as commit.gpgsign or hooksPath affect the test's commits.
109: real defect - tree/scripts/check_facts.py:83 - os.listdir on a missing facts directory raises FileNotFoundError, which is not caught, so the run ends in a traceback.
110: real defect - tree/scripts/check.py:436 - With an empty index run_checks is skipped, so even --strict passes with no private terms configured.
111: real defect - tree/scripts/check.py:478 - The binding covers the prompt only, and evals.json:705 already contradicts facts/56.py:12.
112: real defect - tree/scripts/pre-commit:1 - The tree has no .gitattributes, so with core.autocrlf the hook can be checked out with CRLF line endings, which sh does not accept.
113: real defect - tree/scripts/check.py:495 - Reasons are compared only with fact files, never with eval ids, FACTS_FROM or the Facts marker.
114: real defect - tree/scripts/test_check.py:617 - The test asserts only a non-zero exit, so a traceback would also pass, against the rule at :4.
115: real defect - tree/skills/adversarial-verify/evals/evals.json:249 - The quoted text differs from the current SKILL.md:439 summary line.
116: not a defect - tree/scripts/check.py:122 - decode never fails (it falls back to Latin-1), and the version and JSON checks on CHANGELOG.md and plugin.json work regardless of their encoding.
117: real defect - tree/CHANGELOG.md:5 - "The first entry below" is the unnumbered Unreleased section, which check.py:237 skips.
118: not a defect - tree/README.md:255 - The check is documented as keyed on a `(Facts: …)` block, and 54/55 do not carry one.
119: real defect - tree/skills/adversarial-verify/evals/evals.json:615 - The eval's own assertion and facts/49.py:13 say the same two labels are clipped at 320 px, which contradicts "more labels" at :612.
120: not a defect - tree/skills/adversarial-verify/evals/facts/52.rs:15 - A redundant but true assertion verifies nothing extra, but it does no harm and states nothing false.
121: real defect - tree/skills/adversarial-verify/evals/evals.json:612 - The expected output contradicts its own assertion at :615 and facts/49.py:13.
122: not a defect - tree/scripts/check.py:183 - Missing and extra keys are still reported before the `continue`; skipping the field checks of an eval whose id is invalid is a deliberate short-circuit.
123: real defect - tree/scripts/test_check.py:23 - The comment says "Neither" but three terms follow (NONE, T1, T2), and in a git repo only tracked files are scanned (check.py:147).
124: real defect - tree/scripts/check.py:436 - An empty index means no check runs at all, and the exit code is 0.
125: real defect - tree/skills/adversarial-verify/evals/facts/49.py:13 - At 320 px the clipped set is the same two labels, which contradicts evals.json:612.
126: not a defect - tree/scripts/check.py:50 - The script runs on python3 alone, and the `py -3` Windows form is already stated at README.md:264.
127: cannot tell - tree/skills/adversarial-verify/references/execution.md:48 - The claims cover several assertions (ORM model, list of choices, output-file placement) whose fit with the skill text is a judgement call rather than a clear contradiction.
128: real defect - tree/skills/adversarial-verify/SKILL.md:439 - The summary line now lists "(code, data, tests, UX) … mock-ups", unlike the quote in evals.json:249.
129: real defect - tree/scripts/check.py:330 - The patterns are compiled without re.I, so lowercase "python" or "docker" are never warned about.
130: real defect - tree/skills/adversarial-verify/evals/facts/NOT_COMPUTABLE:13 - Eval 52 has both a reason and facts/52.rs, so check.py:495-496 reports an error and "the repo passes" (test_check.py:1) is false today.
131: real defect - tree/scripts/test_check.py:505 - git is called with no skipUnless guard, unlike :369.
132: real defect - tree/scripts/check_facts.py:85 - Unknown ids are dropped silently, so `38 999` runs only 38 and exits 0.
