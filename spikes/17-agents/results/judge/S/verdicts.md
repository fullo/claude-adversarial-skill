1: real defect - tree/scripts/check.py:46 - Only check 3 uses the tracked-file list (:300); checks 6 and 7 list directories on disk (:136, :465), so the docstring overstates what "files checked" means.
2: not a defect - tree/scripts/check.py:34 - The docstring defines the trigger as the literal "(Facts", and every current eval follows that convention; other spellings are outside the contract.
3: not a defect - tree/scripts/check.py:168 - The message includes the exception class and text (FileNotFoundError: No such file...), so the user is told the real cause.
4: real defect - tree/scripts/check.py:431 - staged_tree returns None on any git failure with stderr discarded (:390-393), so every failure is reported as "not a git repository".
5: not a defect - tree/scripts/check.py:436 - With an empty index nothing can be committed or leaked, and the summary lists no checks rather than claiming any passed.
6: not a defect - tree/scripts/check.py:67 - All current reference names fit the pattern, and an unusually named file on disk is still flagged as "never named" (:519-520).
7: real defect - tree/scripts/check.py:149 - The walk fallback also runs when git works but returns no tracked files or root is not a repository, which "if git is not available" does not say.
8: not a defect - tree/scripts/check.py:436 - Same as row 5: an empty index has nothing to commit, so skipping the checks has no effect.
9: real defect - tree/scripts/check.py:345 - The regex only treats single-backtick spans as code, so a pipe inside a ``double-backtick`` span is counted as a cell break, which goes against the docstring (:32-33).
10: not a defect - tree/scripts/check.py:305 - The whole path is matched and the location is masked anyway; "file name" loosely covers the path and does not change what is reported.
11: not a defect - tree/scripts/check.py:410 - Hiding the location is the intended privacy trade-off (terms are never printed, :22-23).
12: real defect - tree/scripts/check.py:301 - A tracked or staged file named .check-private-terms (force-added, or in a subfolder that .gitignore:1 does not stop when forced) is skipped silently, and the hook passes the commit.
13: not a defect - tree/scripts/check.py:494 - Leftover or duplicate reasons never let a fact-stating eval go unchecked. The docstring only requires a reason to exist (:34-36).
14: real defect - tree/scripts/check.py:392 - The function returns None on any git failure, not only when root is not a repository as its docstring (:387) says.
15: not a defect - tree/scripts/check.py:494 - Same as row 13: leftover reasons are harmless and no promise in the docstring is broken.
16: cannot tell - tree/scripts/check.py:345 - The row has no claim, so there is nothing to judge.
17: real defect - tree/scripts/check.py:122 - One invalid byte switches the whole file to Latin-1, so UTF-8 accented letters become mojibake and an accented term is missed. This case is not in the "Not caught" list (:24-26).
18: real defect - tree/scripts/check.py:463 - With "evals": null, :460 returns None and the set comprehension raises TypeError, so the comment at :462 is not true in every case.
19: not a defect - tree/scripts/check.py:462 - The early return only happens when check 1 has already logged an error, so the run is red anyway. In the empty-index case nothing is appended at all.
20: real defect - tree/scripts/check.py:270 - Dropping a term with no letters shifts the indexes in pats, so "private term #k" at :318/:321 points at the wrong configured term.
21: real defect - tree/scripts/check.py:369 - DELIM does not require a pipe, so a `---` line after a line containing `|` is treated as a 1-cell delimiter (false error). Also, `-{3,}` at :341 misses valid GFM delimiters with 1-2 dashes.
22: real defect - tree/scripts/check.py:463 - "evals": null, or an unhashable id, crashes here before print_report, so the comment at :462 is false.
23: real defect - tree/scripts/check.py:252 - os.path.exists is true for a directory, so open at :254 raises outside any try (called at :423) and the run ends in a traceback.
24: real defect - tree/scripts/check.py:473 - Two files that map to the same id overwrite each other in with_file, so only one is hash-checked, while check_facts.py:83 runs both.
25: not a defect - tree/scripts/check_facts.py:83 - check_facts.py uses the same case-sensitive extensions and the `_` exclusion, so ignored files are never run. Helper files are exempt by design.
26: real defect - tree/scripts/check.py:476 - A directory or unreadable file named like 40.py makes read_text raise OSError with no handler, and the report is lost.
27: real defect - tree/scripts/check.py:248 - An exported but empty CHECK_PRIVATE_TERMS gives [] and shadows an existing .check-private-terms. The message at :295 then tells the user to create a file that already exists.
28: not a defect - tree/scripts/check.py:166 - Check 1 promises valid JSON with the right keys; duplicate JSON keys are outside that contract.
29: real defect - tree/scripts/check.py:332 - splitlines() breaks on \x0b, \x0c, \x85, U+2028 and U+2029, while :321 counts only \n, so the same file gets different line numbers from different checks.
30: real defect - tree/scripts/check.py:433 - With --staged, root becomes the index checkout, so references/ is not "read as it is on disk, tracked or not" (:43-44). test_check.py:507 confirms this is intended.
31: not a defect - tree/scripts/check.py:321 - Only files with old CR-only line endings are affected; the hit is still reported, just with the wrong line number.
32: real defect - tree/scripts/check.py:129 - SKILL.md is read with rep at both :214 and :512, so a non-UTF-8 SKILL.md is reported twice.
33: not a defect - tree/scripts/check.py:215 - Only CR-only files, or a SKILL.md that ends at the frontmatter, are affected, and the result is a loud false error rather than a missed problem.
34: real defect - tree/scripts/check.py:214 - read_text raises OSError for a missing SKILL/README/CHANGELOG/plugin.json, and main has no except (:426-440), so the run ends in a traceback without printing the errors already found.
35: real defect - tree/scripts/check.py:369 - A line with a pipe followed by `---` matches DELIM with no pipe needed, which gives a false "table delimiter has 1 cells" error.
36: not a defect - tree/scripts/check.py:269 - "term #k" counts terms, and comment lines are not terms, so the numbering is consistent.
37: not a defect - tree/scripts/check.py:494 - Same as row 13: leftover reasons do no harm.
38: cannot tell - tree/scripts/check.py:356 - The row is a fragment with no number, location or full claim.
39: cannot tell - tree/scripts/check.py:525 - Whether print fails depends on the stdout encoding of the environment, which the project's files do not show.
40: real defect - tree/scripts/check.py:301 - Same as row 12: a force-added terms file is skipped silently and the commit passes.
41: real defect - tree/scripts/check.py:303 - Same as row 20: dropping a term with no letters shifts the numbers given to later terms.
42: real defect - tree/scripts/check.py:473 - Because of the overwrite at :473, not every fact file is hash-checked, so the docstring at :36-37 promises more than the code does.
43: real defect - tree/scripts/check.py:463 - .get("evals", []) returns None or a number, iterating it raises TypeError outside the try at :459-462, and check 1's error is lost.
44: real defect - tree/scripts/check.py:465 - Checks 6 and 7 read the disk directly, so the docstring at :46 is wrong for every check except 3.
45: not a defect - tree/scripts/check.py:462 - Same as row 19: check 1 already makes the run fail.
46: real defect - tree/scripts/check.py:512 - Same as row 32: SKILL.md is reported twice.
47: real defect - tree/scripts/check.py:470 - "²".isdigit() is True but int("²") raises ValueError, so the run crashes.
48: real defect - tree/scripts/check.py:341 - `-{3,}` rejects GFM delimiters with 1-2 dashes, so such a table is never checked, against the promise at :30-33.
49: not a defect - tree/scripts/check.py:46 - The walk fallback is documented, and scanning more files errs on the safe side for a leak check.
50: real defect - tree/scripts/check.py:375 - A row without pipes ends the table here, while in GFM it is still a table row, so it and the rows after it are never checked.
51: real defect - tree/scripts/check.py:473 - Same as row 24: two fact files for one id overwrite each other, so only one is hash-checked.
52: real defect - tree/scripts/check.py:254 - Same as row 23: an unreadable terms file or a directory with that name crashes the run before any report.
53: not a defect - tree/scripts/check.py:237 - The documented format is "## <version>" (:11-12), and CHANGELOG.md:10 follows it.
54: not a defect - tree/scripts/check.py:295 - The run prints a message saying "private names were NOT checked", so the user is not misled.
55: real defect - tree/scripts/check.py:248 - Same as row 27: an empty env var shadows the existing terms file, and the message is misleading.
56: real defect - tree/scripts/check.py:433 - Same as row 30: the docstring at :43-44 is wrong under --staged.
57: real defect - tree/scripts/check.py:473 - Part (a) is real: 035.py and 35.py both map to id 35, and one of them is never hash-checked. Part (b) on leftover reasons is not.
58: not a defect - tree/scripts/check.py:418 - The --help content is cosmetic; usage and configuration are in the module docstring.
59: real defect - tree/scripts/check.py:313 - Escape decoding only happens for lowercase ".json", so JSON content in .ipynb/.JSON files is not decoded, despite the general promise at :20-21.
60: real defect - tree/scripts/check.py:122 - Same as row 17: the Latin-1 fallback turns UTF-8 accents into mojibake and terms are missed.
61: real defect - tree/scripts/check.py:193 - A non-string prompt or expected_output is reported as "empty", which is the wrong cause.
62: real defect - tree/scripts/check.py:470 - Same as row 47: isdigit() accepts characters that int() rejects.
63: real defect - tree/scripts/check.py:433 - Same as row 30: the docstring is wrong under --staged.
64: real defect - tree/scripts/check.py:149 - Same as row 7: the fallback also runs when git is available but nothing is tracked.
65: not a defect - tree/scripts/check.py:410 - Hiding the path is the intended privacy design.
66: not a defect - tree/scripts/check.py:477 - The tool always tells the user the exact lowercase value to set (:482); requiring that format strictly is not a defect.
67: real defect - tree/scripts/check.py:512 - Same as row 32: the non-UTF-8 error for SKILL.md appears twice.
68: cannot tell - tree/scripts/check.py:527 - It depends on the console or pipe encoding at runtime, which nothing in the project shows. The row itself marks it as unconfirmed.
69: not a defect - tree/scripts/check.py:203 - Check 1 already fails the run on duplicate or boolean ids (:186, :203-205), so check 6's behavior there does not matter.
70: real defect - tree/scripts/check.py:345 - Same as row 9: double-backtick code spans are not recognized, so pipes inside them are counted, against :32-33.
71: not a defect - tree/scripts/check.py:137 - The docstring says ".md files in references/"; uppercase .MD and nested folders are outside that contract.
72: real defect - tree/scripts/check.py:255 - Only whole-line comments are removed, so "Name # client" becomes a term that no longer matches "Name" alone. An empty env var also shadows the file (:248).
73: real defect - tree/scripts/check.py:301 - Same as row 12: a tracked copy of the terms file is skipped silently.
74: real defect - tree/scripts/check.py:301 - Same as row 12: nothing stops a force-added terms file from being committed.
75: not a defect - tree/scripts/check.py:436 - Same as row 5: an empty index has nothing to check.
76: not a defect - tree/scripts/check.py:440 - The leftover temp copy holds only the user's own staged content; ignoring cleanup errors is acceptable.
77: not a defect - tree/scripts/check.py:500 - Same as row 2: "(Facts" is the documented trigger (:34).
78: not a defect - tree/scripts/check.py:207 - A less specific message is a cosmetic issue; the error is still reported correctly.
79: not a defect - tree/scripts/check.py:237 - Same as row 53: the "## <version>" format is documented and followed.
80: real defect - tree/scripts/check.py:341 - Same as row 48: tables with 1-2 dash delimiters are never checked.
81: real defect - tree/scripts/check.py:248 - Same as row 27: an empty env var disables the terms file.
82: not a defect - tree/scripts/check.py:319 - Reporting one hit per term per file is enough to block the commit; that is a design choice.
83: not a defect - tree/scripts/check.py:256 - Same as row 36: #k numbers the terms, not the lines.
84: real defect - tree/scripts/check.py:255 - An inline comment becomes part of the term, which silently weakens the match for the real term.
85: real defect - tree/scripts/check.py:301 - Same as row 12: the private list could be committed through a skipped tracked file.
86: real defect - tree/scripts/check.py:341 - Same as row 48: `-{3,}` misses compact GFM delimiters.
87: real defect - tree/scripts/check.py:114 - A UTF-32-LE BOM starts with FF FE, so the file is decoded as UTF-16 with NULs inside words and terms are missed. This case is not in the "Not caught" list (:24-26).
88: not a defect - tree/scripts/check.py:480 - Same as row 66: requiring the exact lowercase hash line is strict but intended.
89: not a defect - tree/scripts/check.py:67 - Same as row 6: such names are unusual, and an unnamed file on disk is still reported.
90: real defect - tree/scripts/check.py:463 - A None evals list or a list id raises TypeError outside the try, and check 1's report is lost.
91: real defect - tree/scripts/check.py:313 - Same as row 59: escapes are only decoded in lowercase .json files, against :20-21.
92: real defect - tree/scripts/check.py:392 - Same as rows 4 and 14: every git failure is reported as "not a git repository".
93: not a defect - tree/scripts/check.py:166 - Same as row 28: duplicate JSON keys are outside check 1's contract.
94: real defect - tree/scripts/check.py:214 - A nonexistent --root is not checked, so check 2's read_text raises and the run crashes (the help-text part is cosmetic).
95: real defect - tree/scripts/check.py:356 - splitlines() also splits on \x85 and U+2028/2029, so one table row can be split and give false cell-count errors.
