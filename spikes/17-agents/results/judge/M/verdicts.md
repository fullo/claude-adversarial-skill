1: real defect - tree/scripts/check.py:149-152 - Any git failure or an empty ls-files silently falls back to os.walk over every file on disk, which the docstring at :46-47 does not describe.
2: cannot tell - tree/scripts/check_facts.py:43-49 - Whether a leading U+FEFF makes ast.parse fail depends on the Python version, no fact file has a BOM, and the "ok <id>" rule still applies.
3: real defect - tree/scripts/check.py:149-151 - The fallback to every file also happens when root is not a repo or nothing is tracked, but the docstring at :46-47 names only "git not available".
4: not a defect - tree/skills/adversarial-verify/SKILL.md:20 - The frontmatter has exactly one `version:` line, so the first match is the right one. This is only a hypothetical hardening.
5: real defect - tree/scripts/test_check.py:595-602 - Only a .py fact file is mutated, so the .rs/.ts ASSERTS/STRIP paths (check_facts.py:34-39,51) have no test.
6: real defect - tree/scripts/check.py:433 - With --staged, root is the checkout-index copy, so "read as it is on disk, tracked or not" (:43-44) is false in the hook's mode (test_check.py:508 relies on this).
7: real defect - tree/scripts/pre-commit:9 - Both checkers run from "$root/scripts" (the working tree), not from the staged copy, so they do not check "exactly what is staged" (:2) when a checker itself is edited.
8: real defect - tree/scripts/check.py:473 - `with_file[int(stem)] = name` keeps only the last file per id, so a second fact file's prompt hash is never checked, against the docstring at :36-38.
9: not a defect - tree/scripts/check_facts.py:100 - Having no timeout only matters for a looping fact file. These files are reviewed code and the user can interrupt the run. No stated contract is broken.
10: real defect - tree/scripts/check_facts.py:82,89,100 - With a relative --root, `path` is relative to the caller but the child runs with cwd=FACTS, so the path resolves twice and every file FAILs.
11: real defect - tree/scripts/check.py:470 - `"²".isdigit()` is True but `int("²")` raises ValueError, so a file with that stem crashes the run with a traceback.
12: real defect - tree/scripts/check.py:301-302 - Any file named .check-private-terms, tracked or staged at any depth, is skipped without a message, so the private list itself can be committed with no error.
13: real defect - tree/scripts/check.py:226-228 - read_text raises OSError for a deleted plugin.json/README/CHANGELOG/SKILL.md, only ValueError is caught, and the run ends in a traceback with no ERROR or summary.
14: real defect - tree/skills/adversarial-verify/evals/evals.json:358-369 - Eval 28 states facts and eval 29 does not, so moving FACTS_FROM to 30 or using `<=` at check.py:498 breaks no test.
15: real defect - tree/scripts/test_check.py:64-68 - assert_passes never calls assert_no_leak, so passing runs are not leak-checked as :4-5 promise.
16: cannot tell - tree/scripts/check_facts.py:100 - The missing timeout is not a defect (see 9). Whether locale decoding of the child output actually fails depends on the system code page and the output, which cannot be shown here.
17: not a defect - tree/scripts/test_check.py:106 - On CPython the unreferenced file object is closed and flushed right away, which is what the suite runs on.
18: real defect - tree/scripts/check.py:470-473 - `040.py` and `40.py` both become id 40 and overwrite each other, while check_facts.py:94,107 would expect "ok 040" from the first.
19: real defect - tree/scripts/test_check.py:445-450 - No test covers the missing toolchain, the hook, mismatched fences (check.py:362-366 closes a ``` fence on ~~~), .rs/.ts stripping or crash paths.
20: real defect - tree/scripts/check.py:247-249 - A set CHECK_PRIVATE_TERMS, even an empty one, silently replaces .check-private-terms, although the docstring at :13-14 says only "or".
21: real defect - tree/scripts/test_check.py:580-617 - The check_facts tests assert only FAIL text or return codes, never ERROR, the summary or assert_no_leak, against the rule at :4.
22: real defect - tree/scripts/check.py:149-151 - Same as row 3: the fallback also happens when git fails or tracks nothing, which :46 does not say.
23: real defect - tree/scripts/check.py:433 - Same as row 6: under --staged an untracked references file is not seen, and test_check.py:508 asserts exactly that.
24: real defect - tree/scripts/test_check.py:264-267 - Only a 3-character term is tested. The 4-character boundary of :271, the reported line number (:321), an empty assertions list (:195), non-UTF-8 key files (:128) and an empty index (:436) have no test.
25: real defect - tree/scripts/test_check.py:615-617 - None of the listed cases (hook, missing toolchain, CRLF split, tracked terms file, relative --root, two files per id, inline # comment) has a test.
26: real defect - tree/scripts/check.py:433 - Same as row 6: with --staged the folder read is the staged copy, not the disk.
27: real defect - tree/scripts/test_check.py:351,390 - os.symlink needs a privilege on Windows, and rmtree of .git hits read-only objects. Windows is supported (README.md:263), so these tests can fail there with no real defect behind them.
28: real defect - tree/scripts/test_check.py:502-505 - Unlike StagedTest (:369) there is no skipUnless(git), so without git the test errors instead of skipping.
29: real defect - tree/scripts/test_check.py:64-68 - Same as row 15: assert_no_leak runs only in assert_fails (:62).
30: real defect - tree/scripts/check.py:460-463 - With `"evals": null`, `.get` returns None, and iterating it at :463 raises TypeError outside the try, so check 1's report is lost to a traceback.
31: real defect - tree/scripts/check_facts.py:91-93 - A missing toolchain prints "skip" and is not counted as failed, so the regex at test_check.py:578 passes even though 52.rs and 53.ts never ran (against check_facts.py:8).
32: real defect - tree/scripts/check.py:93-96 - Only combining marks are removed after NFKD, so letters such as ø, ł, đ and æ do not fold, despite "ignores ... accents" at :15.
33: real defect - tree/scripts/check.py:114-116 - A UTF-32-LE BOM starts with FF FE, so the file decodes as UTF-16 with NULs between letters and terms are silently missed, a case the docstring at :21-26 does not list.
34: real defect - tree/scripts/test_check.py:615-617 - The test asserts only a non-zero exit, so a crash would also pass it.
35: cannot tell - tree/scripts/check.py:527 - Whether the em dash fails to encode depends on the Windows code page. cp1252 has it, other code pages may not, and this can only be shown by running it.
36: real defect - tree/scripts/test_check.py:32-35 - The fixture copies the developer's working tree, untracked files included, so an untracked references/*.md makes test_repo_passes red.
37: real defect - tree/scripts/check.py:227-228,332,356 - A missing file raises OSError in check_version/check_neutral/check_tables (only ValueError is caught), so the run ends in a traceback with no ERROR or summary.
38: not a defect - tree/scripts/check.py:128 - The UTF-8 error is deliberately limited to the files a verifier reads. Nothing promises it for CHANGELOG, plugin.json or fact files.
39: real defect - tree/scripts/check.py:314-317 - A .json file that does not parse silently skips the escape-decoded scan, so a \u-escaped term passes, against :20-21.
40: not a defect - tree/scripts/test_check.py:31-37 - The fixture tests the scanner logic, which is the same on both paths, and the ls-files path is exercised at test_check.py:398-402.
41: real defect - tree/scripts/check.py:223,90,400 - Only `badges[:1]` is checked, SEP allows at most one separator, and mask uses whole-word patterns for "=" terms, so the tests at test_check.py:171-173, :286 (two spaces) and :341-344 are red.
42: not a defect - tree/scripts/check_facts.py:100 - Same as row 9: a missing timeout is hardening, not a broken contract.
43: cannot tell - tree/scripts/check.py:389-391 - How checkout-index treats skip-worktree entries in a sparse checkout is git behavior that cannot be checked from this folder.
44: real defect - tree/scripts/check.py:494 - Duplicate or unknown NOT_COMPUTABLE ids are accepted silently, so a stale reason would exempt a future eval with that id, while an orphan fact file is an error (:470-471).
45: real defect - tree/scripts/check.py:135-136 - Checks 4, 5 and 7 read references/ from disk, but check 3 scans only tracked files (:435), so an untracked reference file that ships with the folder is never scanned for terms.
46: real defect - tree/scripts/check.py:498 - Eval 29 does not state facts (evals.json:369), so moving FACTS_FROM to 30 changes no test result.
47: not a defect - tree/scripts/check.py:34 - The docstring documents the marker as the literal "(Facts", and every eval that states facts uses it.
48: real defect - tree/scripts/check_facts.py:84-85 - Requested ids with no file are silently dropped, so `38 999` reports success without mentioning 999.
49: real defect - tree/scripts/check_facts.py:43,83 - A wrong --root or a non-UTF-8 fact file raises an uncaught error, which aborts the run before the summary and before the remaining files.
50: real defect - tree/scripts/pre-commit:15-17 - On success $out is discarded, so "skip ...: toolchain not found" lines are never shown to the committer.
51: not a defect - tree/scripts/check_facts.py:11-14 - The rule as documented ("at least one assertion outside comments and strings") is exactly what the AST walk checks. The "ok <id>" line is the second guard.
52: real defect - tree/scripts/test_check.py:302,316 - Any ERROR that names the file satisfies these tests, so a broken plugin.json ("not valid JSON") would pass without private-term detection.
53: real defect - tree/scripts/check.py:341 - DELIM requires 3 or more dashes, but GFM accepts 1-2, so such tables are skipped without a message.
54: not a defect - tree/CHANGELOG.md:10 - The documented format is "## <version>" and the changelog follows it. A `## v4.3` entry would cause a mismatch error, not a silent pass.
55: real defect - tree/scripts/check.py:316-317 - Same as row 39: non-parsing .json files skip escape decoding silently.
56: real defect - tree/scripts/check.py:255,266 - Only whole-line comments are dropped, so `term  # note` becomes a multi-part term and the plain term is no longer detected.
57: real defect - tree/scripts/check.py:126 - open() follows a symlink, so the committed link text (its target path) is never scanned for terms. Low likelihood: no symlinks exist.
58: real defect - tree/scripts/check.py:494 - Same as row 44: unknown or duplicate reason ids are accepted silently.
59: real defect - tree/scripts/test_check.py:371-374,503-504 - The git helpers inherit the global config (commit.gpgsign, core.hooksPath), and :502 lacks the git skip guard, so tests can go red with no real defect.
60: cannot tell - tree/scripts/check.py:345 - The row has no claim, so there is nothing to judge.
61: real defect - tree/scripts/check.py:75 - TAG_RE requires whitespace after the tag, but :9 and the message at :202 say only "followed by text", so `[substance]text` is rejected with a confusing message.
62: real defect - tree/scripts/check.py:494 - Same as row 44: a stale `NN: reason` silently exempts a future eval NN.
63: real defect - tree/scripts/test_check.py:595-602 - Same as row 5: the Rust/TS stripping has no test.
64: real defect - tree/scripts/pre-commit:9 - The hook does not pass --strict, despite its comment at :5, and no test runs the hook, so the broken promise goes unnoticed.
65: real defect - tree/scripts/test_check.py:64-68 - Same as row 15.
66: real defect - tree/scripts/test_check.py:351 - os.symlink raises OSError on Windows without the privilege, and Windows is supported (README.md:263).
67: real defect - tree/scripts/test_check.py:1 - The docstring names only check.py, but the file also tests check_facts.py (:571-617), and check 4 only has warning cases.
68: real defect - tree/scripts/check_facts.py:43 - A non-UTF-8 fact file raises UnicodeDecodeError, which aborts the run before the summary (it still exits non-zero).
69: real defect - tree/scripts/check.py:248 - An empty but set CHECK_PRIVATE_TERMS ignores the terms file, and without --strict (which the hook does not pass) the run only warns.
70: not a defect - tree/scripts/check.py:476-477 - The convention is one hash per fact file in its header, and that is what is read.
71: real defect - tree/scripts/test_check.py:580-617 - Same as row 5: no negative test for .rs/.ts.
72: real defect - tree/scripts/check.py:223 - Same as row 41: the tests at :171, :286 and :341 are red against the code (badges[:1], one-char SEP, whole-word mask).
73: not a defect - tree/scripts/test_check.py:296-298 - The test shows that a non-UTF-8 file is still scanned rather than crashing, which is the documented promise.
74: real defect - tree/scripts/check.py:473 - Same as row 8: two fact files for one id leave one hash unchecked.
75: real defect - tree/scripts/check.py:465 - Check 6 lists facts/ from disk, so on a working-tree run an untracked fact file satisfies it, against "files tracked by git" (:46). The hook's --staged mode still catches it.
76: cannot tell - tree/scripts/check.py:525 - The UnicodeEncodeError depends on the Windows code page and the printed names, and can only be shown by running it.
77: not a defect - tree/scripts/test_check.py:50 - The scan logic tested is the same on both list paths, and the ls-files path has its own test (:398-402).
78: real defect - tree/scripts/check_facts.py:82,100 - Same as row 10: a relative --root makes every file FAIL.
79: not a defect - tree/scripts/check.py:34 - Same as row 47: the case-sensitive "(Facts" marker is documented.
80: cannot tell - tree/scripts/check.py:345 - The row has no claim, so there is nothing to judge.
81: real defect - tree/scripts/pre-commit:17 - Same as row 50: the runner's output, including skip lines, is discarded on success.
82: real defect - tree/scripts/check.py:301-302 - Same as row 12: a staged .check-private-terms is skipped by name and nothing reports it.
83: real defect - tree/scripts/pre-commit:9,15 - The checkers run from the working tree, so unstaged edits to them change the verdict on staged content.
84: real defect - tree/scripts/check.py:463 - Same as rows 30 and 37: `evals: null` or a missing core file crashes the run before the summary.
85: real defect - tree/scripts/test_check.py:390 - On Windows, rmtree of .git without an error handler fails on read-only git objects.
86: real defect - tree/scripts/check_facts.py:91-93 - The cited statements are contradicted by the code: skips are silent, only `badges[:1]` is checked (check.py:223), SEP allows one character (:90), and mask uses whole-word patterns (:400).
87: real defect - tree/scripts/check.py:375 - A non-blank line with no pipe ends the table, while GFM renders it as a row, so its cell count is never checked.
88: real defect - tree/scripts/test_check.py:302 - Same as row 52: the assertion only requires the file name.
89: real defect - tree/scripts/check.py:494 - Same as row 44: duplicate and stale reasons go unreported.
90: real defect - tree/scripts/test_check.py:617 - Same as row 34: a crash would also satisfy the assertion.
91: real defect - tree/scripts/check.py:46 - Same as row 3: the documented fallback condition is incomplete.
92: real defect - tree/scripts/check.py:301 - Same as row 12: a tracked or staged terms file is skipped without error.
93: real defect - tree/scripts/check.py:473 - Same as row 8: 38.py and 38.rs overwrite each other.
94: not a defect - tree/scripts/check_facts.py:100 - Same as row 9: a missing timeout is hardening only.
95: real defect - tree/scripts/check.py:255,266 - Same as row 56: an inline comment silently stops the term from being protected.
96: real defect - tree/scripts/check.py:316 - Same as row 39: non-strict JSON skips the decoded scan with no warning.
97: real defect - tree/scripts/check.py:375 - Same as row 87.
98: real defect - tree/scripts/check.py:255 - Same as row 56.
99: not a defect - tree/scripts/check_facts.py:12 - A raise statement is documented as an assertion, and the "ok <id>" line is the second guard. No current file is affected.
100: real defect - tree/scripts/test_check.py:23-26 - The comment says "Neither" but three constants follow. The defect is cosmetic.
101: not a defect - tree/scripts/test_check.py:323-326 - The BOM part of :320 is vacuous, but BOM handling is actually tested by test_bom_before_a_comment_keeps_it_a_comment.
102: not a defect - tree/scripts/check.py:82-88,330 - Case-sensitive matching is a reasonable choice for warnings-only terms that include common words such as "react".
103: real defect - tree/scripts/test_check.py:84-85 - Text mode writes \r\n on Windows, and SEP (check.py:90) allows only one character, so the "\n" variant at :286 is red on Windows.
104: real defect - tree/scripts/check.py:392-393,431 - Any checkout-index or ls-files failure is reported as "not a git repository", which hides the real cause.
105: real defect - tree/scripts/check.py:248 - Same as row 20: a set variable, even empty, replaces the file, and the hook does not pass --strict (pre-commit:9).
106: real defect - tree/scripts/test_check.py:337-339 - `terms=T1` is a substring term, so the "whole-word does not flag" comment is stale and the test duplicates :331-334.
107: real defect - tree/scripts/test_check.py:337 - Same as row 106.
108: real defect - tree/scripts/test_check.py:337 - Same as row 106.
109: real defect - tree/scripts/test_check.py:351 - Same as row 66.
110: real defect - tree/scripts/check.py:301-302 - Same as row 12.
111: real defect - tree/scripts/test_check.py:64 - Same as row 15.
112: real defect - tree/scripts/check_facts.py:18 - The documented `--root DIR` fails for any relative DIR because of the cwd=FACTS bug at :100.
113: real defect - tree/scripts/check.py:483-496 - Same as row 44.
114: real defect - tree/scripts/test_check.py:72 - The leak check looks only for T1, T2 and T2 without its space, so hyphen, underscore and newline forms of T2 would go unnoticed if printed.
115: real defect - tree/scripts/test_check.py:503 - Same as row 28: no skipUnless(git).
116: real defect - tree/scripts/test_check.py:302 - Same as row 52.
117: real defect - tree/skills/adversarial-verify/evals/evals.json:369 - Eval 29 does not state facts, so a `<=` mutant at check.py:498 survives every test.
118: real defect - tree/scripts/test_check.py:617 - A traceback satisfies :617. The other cited lines (:584, :592, :601, :612) are each followed by a message assertion, so they are fine.
119: not a defect - tree/CHANGELOG.md:10 - Same as row 54: the "## <version>" format is documented and followed.
120: not a defect - tree/scripts/check_facts.py:36-37 - The Rust stripping is a documented heuristic, and no fact file contains `'"'` or a raw string.
121: real defect - tree/scripts/test_check.py:337 - Same as row 106.
122: not a defect - tree/scripts/check_facts.py:37 - Same as row 120.
123: not a defect - tree/scripts/check.py:482 - The error message itself gives the lowercase hash to paste, so the format is self-documenting.
124: real defect - tree/scripts/test_check.py:337 - Same as row 106.
125: cannot tell - tree/scripts/check.py:345 - The row has no claim, so there is nothing to judge.
126: real defect - tree/scripts/test_check.py:502 - Same as row 28.
127: real defect - tree/scripts/test_check.py:336-337 - Same as row 106: the name and comment are stale for a substring term.
128: not a defect - tree/scripts/check_facts.py:100 - Same as row 9.
129: real defect - tree/scripts/check.py:43 - Same as row 6.
130: real defect - tree/scripts/check.py:473 - Same as row 8.
131: real defect - tree/scripts/test_check.py:578 - Same as row 31: green while 52.rs and 53.ts are skipped.
132: real defect - tree/scripts/test_check.py:85 - Same as row 103.
133: real defect - tree/scripts/check.py:295 - With an empty CHECK_PRIVATE_TERMS, the message says to create a terms file that may already exist and be ignored.
134: real defect - tree/scripts/check.py:121-122 - One invalid byte turns the whole file into Latin-1, so UTF-8 "ó" becomes "Ã³" and then "a3", and accented terms are missed silently.
135: real defect - tree/scripts/test_check.py:576-578 - Same as row 31.
136: real defect - tree/scripts/test_check.py:351 - Same as row 66.
137: real defect - tree/scripts/check.py:255-256 - Same as row 56.
138: real defect - tree/scripts/test_check.py:503 - Same as row 59: no git guard, and the global git config is inherited.
139: real defect - tree/scripts/test_check.py:64 - Same as row 15.
140: not a defect - tree/scripts/check.py:34 - Same as row 47.
141: real defect - tree/scripts/test_check.py:1 - Same as row 67: check_facts.py is not named.
142: not a defect - tree/scripts/test_check.py:31 - Same as row 40: the scan logic is path-independent, and the ls-files path is tested at :398-402.
143: not a defect - tree/README.md:246 - The node 22.6 requirement is documented in the README, the user's entry point.
144: not a defect - tree/scripts/check.py:168 - The message includes the exception class (FileNotFoundError), so the cause is visible.
145: not a defect - tree/scripts/test_check.py:604-607 - The test's purpose is that argparse accepts --root after the ids, and it checks that. Honoring --root is a separate concern.
