## INTAKE

Request settles every choice, so nothing was asked and nothing is defaulted.

- Target: every domain Step 0 detects in `scripts/check.py`. Detected: **Code** (the script's logic) and **Documentation** (its module docstring, which is also the `--help` description via `argparse` at `scripts/check.py:418`, and its error and warning messages). Not detected: Tests (the file is not a test file), Data (it validates formats and defines none), Architecture, Analysis, UX.
- Depth: standard. Scope: the whole file. Execution mode: reasoning only. Nothing was run and nothing was written except this report.
- Cost estimate (accepted by the request): 1 file in scope, 2 domains, about 24 claims, nothing run.
- Reference files of the skill: none read, since no condition held (no plan or spike, no UX, no approved run).
- Consent lasts for this verification only; a later one starts at reasoning only.

## VERIFICATION DOMAIN

Domain 1 **Code**, Domain 2 **Documentation**. Each claim is counted once, in its primary domain.

## GROUND TRUTH

- The code itself, traced line by line: `scripts/check.py:1-531`.
- The script's stated contract: its docstring (`scripts/check.py:1-51`) and `README.md:244-263`.
- Intent encoded in the unit tests `scripts/test_check.py` (read as a spec; **not run**).
- Neighbouring files read: `scripts/check_facts.py:1-60`, `scripts/pre-commit:1-18`, `.gitignore:1-2`, `.claude-plugin/plugin.json:1-20`, `CHANGELOG.md` headings (lines 5, 10, 17, 28, 37), `skills/adversarial-verify/evals/facts/*` header lines.
- Not read: the repo's `skills/adversarial-verify/SKILL.md` and `evals.json` contents. Claims that depend on whether the repo itself passes are limited to that.

## INVARIANTS

Looked in: `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md` (none exist in the tree; file listing), the docstring `scripts/check.py:1-51`, `README.md:244-263`, `scripts/test_check.py:1-6`, `scripts/pre-commit:1-9`. The script is itself an invariant enforcer, so the invariants of the script were taken from there. 4 found, all touched.

| # | Invariant | Source | Touched by | Enforced by | Bites on changed path? / Respected? |
|---|-----------|--------|------------|-------------|--------------------------------------|
| 1 | "Terms are never printed: any output line containing one is masked" | `scripts/check.py:22-23`, `README.md:250`, `scripts/test_check.py:4-5` | `mask` and `term_patterns` | `mask` (`scripts/check.py:397-414`); `assert_no_leak` (`scripts/test_check.py:70-73`) | **No** for `=` (whole-word) terms: FAIL 1 |
| 2 | The list of private terms is never committed | comment `scripts/check.py:423`, `README.md:250` | `check_private` | `.gitignore:1` only; `check_private` skips the file (`scripts/check.py:301-302`) | **No**: nothing stops it once force-added: FAIL 4 |
| 3 | Any ERROR gives a non-zero exit code | `scripts/check.py:3-4` | `main` | `scripts/check.py:442`; `assert_fails` (`scripts/test_check.py:54-62`) | Yes (also on a crash, which exits 1 with a traceback) |
| 4 | Version agreement: SKILL.md, every README badge, plugin.json, newest CHANGELOG entry | `scripts/check.py:10-12`, `README.md:249` | `check_version` | `scripts/check.py:212-241` | **No** for a second badge: FAIL 2 |

## DECOMPOSED CLAIMS

Domain Code
1. C1 evals.json shape: exact keys, non-empty strings, tags from eval 21 (`:163-202`). Deductive
2. C2 ids are integers (bool rejected), unique and consecutive (`:186`, `:203-207`). Deductive
3. C3 The version is read only from the frontmatter, CRLF-safe (`:215-216`). Deductive
4. C4 Every README skill badge must equal the SKILL.md version (`:217-225`). Deductive
5. C5 plugin.json and the newest CHANGELOG entry are compared with it (`:226-241`). Deductive
6. C6 A multi-word term matches when its parts are joined by any non-alphanumerics or nothing (`:90`, `:274`). Deductive
7. C7 `=` whole-word detection, the short-term warning and the no-letter error (`:259-276`). Deductive
8. C8 File names, content, JSON-decoded strings and non-UTF-8 files are scanned (`:112-122`, `:300-323`). Deductive
9. C9 No output line shows a term (`:397-414`, `:523-527`). Deductive
10. C10 The terms file is never committed (`:301-302`). Deductive
11. C11 With no terms the check says so, and fails under `--strict` (`:292-298`). Deductive
12. C12 Neutral-wording hits are warnings only (`:328-336`). Deductive
13. C13 Table rows are compared with the header, escaped pipes and code spans excluded (`:341-350`). Deductive
14. C14 Every row of every table is checked and fenced blocks are skipped (`:353-381`). Deductive
15. C15 Eval facts: file or reason, not both, hash bound to the prompt (`:457-501`). Deductive
16. C16 NOT_COMPUTABLE lines are parsed strictly (`:483-494`). Deductive
17. C17 Referenced reference files exist and each is named in SKILL.md (`:506-520`). Deductive
18. C18 `--staged` checks exactly the index content and removes its temporary directory (`:386-394`, `:426-441`). Deductive
19. C19 The summary is always printed and the exit code follows the errors (`:441-442`, `:523-527`). Deductive
20. C20 Missing or unreadable inputs are reported as errors, not crashes. Deductive
21. C21 The script runs on Python 3.8 (docstring `:50`). Deductive (syntax and stdlib calls inspected; `capture_output` needs 3.7)
22. C22 Reported line numbers are right even after normalisation (`:311`, `:321`). Deductive

Domain Documentation
23. D1 The docstring describes what checks 2, 3 and masking do (`:10`, `:15-17`, `:22-23`). Deductive
24. D2 Check 7 and `--staged` as described in the docstring (`:42-44`). Deductive

## FAILURE CATEGORIES IDENTIFIED

| Category | Instances | Files affected |
|----------|-----------|----------------|
| Missing completeness | `substring=True` never passed (`:400`); only the first badge compared (`:223`); the terms file is exempt from the check that should flag it (`:301`); missing-file handling written in `check_evals` (`:167`) but not in the other checks | `scripts/check.py` |
| Silent fallthrough | a pipe-less row ends a table without a word (`:375`); fence toggling ignores type (`:361-366`) | `scripts/check.py` |
| Assumed environment | one-character separator assumes `\n` line breaks and single spaces (`:90`); CRLF on Windows breaks it | `scripts/check.py` |
| Cross-artifact drift | docstring and README claim more than the code does (`:10`, `:15-17`, `:22-23`, `:42-44`; `README.md:249-250`) | `scripts/check.py` |

## OUT OF SCOPE (listed, not verified)

- `README.md:249` repeats "every skill badge ... agree" (see FAIL 2); `README.md:250` repeats "any output line containing a term is masked" and "joined (space, hyphen, underscore, line break, or nothing)" (FAIL 1, FAIL 3).
- `scripts/test_check.py:171-173` (second badge), `:284-289` (double space, line break), `:341-344` (`=` term in output) assert behaviour the traced code does not have; by my trace each would be red (not run). `scripts/test_check.py:328-329` asserts the exemption of the terms file that FAIL 4 questions.
- `scripts/check_facts.py` and `scripts/pre-commit` were read only for context.

## VERIFICATION RESULTS

### PASS ✅

| # | Claim | Evidence |
|---|-------|----------|
| 1 | C1 | `:180-202`: `set(e) - EVAL_KEYS` and the reverse give extra and missing keys; empty strings caught by `.strip()` at `:192`, `:199`; tag regex `:75` applied from `TAGGED_FROM` at `:201`. Mode Deductive, 88 |
| 2 | C2 | `:186` `type(i) is not int` rejects `True`; `:203-207` duplicate and range check. Non-int ids are skipped from `ids`, so a gap is also reported (noisy, not silent). Deductive, 88 |
| 3 | C3 | `:215` normalises CRLF before the anchored frontmatter regex; `:216` searches only the group, so a `version:` in a code block does not count. Deductive, 88 |
| 5 | C5 | `plugin.json:3` is `"4.2"`, `README.md:1` is `v4.2`, `CHANGELOG.md:10` is the first numeric heading; `## Unreleased` (`CHANGELOG.md:5`) is skipped by the digit-first regex at `:237`. The repo SKILL.md was not read, so agreement of all four is not shown. Deductive, 85 |
| 7 | C7 | `:265` whole-word flag, `:275` look-arounds, `:271-273` length rule, `:267-270` no-letter error. Deductive, 88 |
| 8 | C8 | `:304-305` names; `:311-317` content and decoded JSON strings; `:112-122` UTF-16 with BOM, UTF-8 (with BOM), Latin-1. Deductive, 85 |
| 11 | C11 | `:293-298`. Deductive, 90 |
| 12 | C12 | `:332-336` only `rep.warning`. Unanchored words (`Spring`, `Unreal`, `React`, `Vue`, `Rails`, `:82-88`) can give false warnings; harmless by design. Deductive, 85 |
| 13 | C13 | `:344-350` strips code spans and escaped pipes, then outer pipes; header and delimiter compared at `:372-373`. Deductive, 85 |
| 15 | C15 | `:464-482` hash bound; `:495-496` both file and reason; `:497-501` missing both from `FACTS_FROM`. Deductive, 85 |
| 16 | C16 | `:490-492`: `77:` gives an error, comments and blanks skipped. Deductive, 88 |
| 17 | C17 | `:514-520` both directions; names only from SKILL.md count (`:515-516`). Deductive, 85 |
| 18 | C18 | `:389` index checked out into `tmp`; `:438-440` removed in `finally`; failure of git gives an error and skips checks (`:430-432`, `:436`). Deductive, 85 |
| 19 | C19 | `:441-442`, `:526-527`. Deductive, 90 |
| 21 | C21 | f-strings, `subprocess.run(capture_output=True)`, `yield from`, no 3.9+ syntax or `removeprefix`. Deductive, 80. A run on 3.8 would settle it |

### FALSIFIED HYPOTHESES

| # | Location | Suspected defect | Check (quote) | Status | Could it have failed? | Paths not covered | Mode | Confidence |
|---|----------|------------------|---------------|--------|-----------------------|-------------------|------|------------|
| 1 | `:237-241`, `CHANGELOG.md:5` | The `## Unreleased` heading above the newest version makes the CHANGELOG check compare the wrong entry | `re.search(r"^## +([0-9][0-9.]*)\b", ...)` against `CHANGELOG.md:5,10` | falsified | Yes: a pattern like `^## +(\S+)` would take `Unreleased`; the digit-first class at `:237` skips it and lands on `4.2` at `CHANGELOG.md:10` | An "Unreleased" heading that starts with a digit | Deductive | 85 |
| 2 | `:215` | A CRLF SKILL.md hides the frontmatter, giving "no version" | `skill.replace("\r\n", "\n")` before `\A---\n(.*?)\n---\n` | falsified | Yes: without the replace the `---\n` anchor fails on `---\r\n`; the replace is on the path | A lone `\r` line ending | Deductive | 85 |
| 3 | `:311`, `:321` | NFKD and casefold shift the line number reported for a private term | `body.count(chr(10), 0, m.start()) + 1` | conditionally falsified | NFKD and casefold change letters, not `\n`, so counts match for newline characters; I did not enumerate all of Unicode. Would be complete with: a run over a file with ligatures and `ß` before the match | Characters the normaliser might expand into line breaks | Deductive | 70 |

### FAIL ❌

| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| 1 | `scripts/check.py:400` (also `:399`, `:259`) | `pats = term_patterns(terms)` under the comment "substring patterns: when hiding output, err on the side of hiding too much" | Demonstrated defect | high | Terms `=zqvorblax`. An eval carries a key `zqvorblaxlabs`. `check_evals` prints `unexpected keys ['zqvorblaxlabs']` (`:181-182`). `mask` builds whole-word patterns (`substring` defaults to `False`, `:265`), the look-ahead fails on `l`, the line is not masked, and the term is printed. Not even detected by `check_private`, so only the output reveals it. Breaks invariant 1. | Deductive | 90 | `pats = term_patterns(terms, substring=True)` |
| 2 | `scripts/check.py:223` | `for b in badges[:1]:` | Demonstrated defect | medium | `README.md` gets a second badge `skill-v2.0-`. `badges` is `['4.2','2.0']`, only the first is compared, the stale one passes. The docstring (`:10`) and `README.md:249` say "every". Breaks invariant 4. | Deductive | 90 | `for b in badges:` |
| 3 | `scripts/check.py:90` | `SEP = r"[\W_]?"` | Demonstrated defect | high | Term `quillane dorvex` in a file as `quillane  dorvex` (two spaces), `quillane, dorvex`, `quillane - dorvex`, or wrapped over a CRLF line break (`\r\n` is two characters). The separator allows at most one character, so none match and the private name is committed. Docstring `:15-17` promises any joiner. | Deductive | 90 | `SEP = r"[\W_]*"` (still linear: no nested quantifier); update the "Not caught" note |
| 4 | `scripts/check.py:301-302` | `if os.path.basename(rel) == TERMS_FILE:` `continue` | Preventive measure | high (if it happens, the private list is published); likelihood low: needs `git add -f` past `.gitignore:1` | The terms file, tracked or staged, is skipped by the one check meant to catch leaks, and `pre-commit --strict` passes. Breaks invariant 2. | Deductive | 80 | Skip the content scan but report an ERROR when the file is in `files` ("private terms file is tracked") |
| 5 | `scripts/check.py:214`, `:217`, `:227-230`, `:237`, `:332`, `:356`, `:512` | `except ValueError as e:` (only `ValueError`, `:228`) | Preventive measure | low | A tracked file deleted from the working tree (a renamed CHANGELOG, a removed `plugin.json`) raises `FileNotFoundError`. The script dies with a traceback on stderr (not masked, `:524`), later checks do not run. `check_evals` already catches `OSError` (`:167`). Loud, not silent: exit 1. | Deductive | 85 | Catch `OSError` in `check_version`, or wrap each check in `run_checks` and report an ERROR |
| 6 | `scripts/check.py:375` | `while i < len(lines) and lines[i].strip() and "|" in lines[i]:` | Preventive measure | low | A table row that lost every pipe ends the table. It is not counted and later rows are not checked. | Deductive | 80 | Treat a non-blank line as a row until a blank line; report it |
| 7 | `scripts/check.py:361-366` | `f = re.match(r"^(`{3,}\|~{3,})", s)` ... `fence = None` | Preventive measure | low | While in a fence, any line that starts with three backticks or tildes closes it, even one of another kind, shorter, or with an info string. A table after a `~~~` line inside a ``` block is then checked as live, or the reverse. | Deductive | 78 | Remember the fence character and length, close only on the same character with at least that length and no info string |
| 8 | `scripts/check.py:42-44` (Documentation) | "The folder is read as it is on disk, tracked or not" | Demonstrated defect (the text contradicts the code) | low | With `--staged`, `root` is the checkout of the index (`:429-433`), so an untracked or unstaged reference file is not read. `scripts/test_check.py:507` expects this. | Deductive | 85 | "Without --staged the folder is read as it is on disk; with --staged, only the staged content" |

Cross-reference: the Documentation side of FAIL 1, 2 and 3 (docstring `:10`, `:15-17`, `:22-23`, `README.md:249-250`) is counted once, in Code. Fix the text when the code is fixed.

## STRESS TEST RESULTS

| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|----------|
| 1 | Scale Shift (10x, zero) | C8, scanning a 10x larger or an empty file (`:311-323`) | yes | 78 | One `normalize` per file; the line count runs only on a match (`:321`); `SEP` is a single optional class, so no backtracking blow-up; empty text gives no match. No run for timing, so ≤ 79 |
| 2 | Time Travel (6 months) | `TAGGED_FROM`, `FACTS_FROM` constants (`:74`, `:77`) | yes | 80 | Each has a comment saying why and is exercised by `scripts/test_check.py:149-159`; the next developer adds evals with no change here |
| 3 | Existence Question | the `substring` parameter of `term_patterns` (`:259`, `:265`) | **no** | 90 | No call passes `True` (searched `scripts/check.py`: `:299`, `:400` only). Deleting it changes nothing, and that is the cause of FAIL 1. It exists on paper only |
| 4 | Requirement Inversion | `--strict` off in CI (`:292-298`, `scripts/pre-commit:9`) | yes | 82 | Without `--strict` the missing list is a warning, not silent; the hook always passes `--strict` |
| 5 | Scale Shift (zero) | C14, zero tables or a table on the last line (`:353-381`) | yes | 80 | The loop is bounded by `len(lines)` at `:359` and `:375`; no index read past the end |
| 6 | Time Travel (6 months) | docstring "Not caught" list (`:24-26`) | **no** | 85 | The list names two evasions; multi-character joiners (FAIL 3), UTF-32 BOM (HYPOTHESES 6) and glued `=` output (FAIL 1) are not in it, so the next developer trusts a stronger guarantee than exists |

## HYPOTHESES (Abductive: require further investigation)

| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|-----------------|
| 1 | `:247-249`: if `CHECK_PRIVATE_TERMS` is set at all, even empty, the terms file is never read | A CI that exports an empty variable silently turns the check off without `--strict` | Intended: `scripts/test_check.py:362-363` expects an empty variable to fail only under `--strict` | Run with `CHECK_PRIVATE_TERMS=` and a populated `.check-private-terms`, with and without `--strict` |
| 2 | `:389-391`: `checkout-index -a` and `ls-files` run with `-C root` | With `--root` a subdirectory of a larger repository the list (relative to `root`) and the checkout (all files) disagree | Git resolves both against `root` and they agree | Run `--staged --root sub/` in a nested repository |
| 3 | `:166`: `json.loads` keeps the last of duplicate keys | An eval with two `assertions` or two `id` keys passes check 1 with the first one lost | A hand-written file never duplicates keys | Add a duplicate key and run check 1 |
| 4 | `:468-473`: `with_file[int(stem)] = name` | `35.py` and `35.rs` both present: one overwrites the other and its prompt hash is never compared | Docstring `:34-36` implies one file per eval | Create both files, change the prompt, see which one fails |
| 5 | `:483-494`, `:495`: reasons are not matched to existing eval ids | `99: reason` for an eval that does not exist is accepted | Harmless clutter | Add the line and run |
| 6 | `:114-118`: a UTF-32 LE BOM starts with `ff fe` | The file is decoded as UTF-16 with NULs between letters, so one-word terms are missed | Such files are never in the repo | Encode a term file as UTF-32 with a BOM and scan |

## HIDDEN BEHAVIORS DETECTED

| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| 1 | `scripts/check.py:259`, `:399-400` | Output masking "errs on the side of hiding too much" | Whole-word for `=` terms | Demonstrated defect (FAIL 1) | 90 |
| 2 | `scripts/check.py:10`, `:223` | "every skill badge" | first badge only | Demonstrated defect (FAIL 2) | 90 |
| 3 | `scripts/check.py:301-302` | the file is "untracked" and "never committed" | the check exempts it by name, in any directory | Preventive measure (FAIL 4) | 80 |
| 4 | `scripts/check.py:247-249` | terms "from CHECK_PRIVATE_TERMS or the file" | an empty variable shadows the file | Hypothesis 1 | 55 |
| 5 | `scripts/check.py:128`, `:214`, `:217`, `:512` | one "not UTF-8" error per file | the same file is read with `rep` several times and can be reported 2-3 times | none: noise | 80 |

## ADVERSARIAL SCAFFOLD FINDINGS

- Reviewer blind spots: `mask` reads as fine because its comment says "substring"; the call passes no argument (`:399-400`). `badges[:1]` reads as "take the first for the message". The one-character `SEP` looks right next to a docstring that says "anything".
- Highest-risk claims, by blast radius × probability: (1) C9 masking, which is the tool's confidentiality guarantee; (2) C6 joiners, the main way a private name slips in (CRLF on Windows is common); (3) C10 the terms file exemption.
- Multi-step traces: `=` term in config → glued form in a message (`:181-182`) → `check_private` does not flag it (`:275`) → `mask` also does not (`:400`) → printed, in a hook or CI log. Staged leak: `git add -f .check-private-terms` → `--staged` checkout (`:389`) → skipped (`:301`) → exit 0.
- Subtlety flags: `term_patterns(terms)` with a defaulted `substring` (`:400`); `[:1]` at `:223`; `[\W_]?` at `:90`.

## SUMMARY (per domain, then cross-domain)

Code
- Claims: 15 verified, 6 in FAIL (C4, C6, C9, C10, C14, C20; 7 findings), 1 falsified-only (C22)
- Findings by type: 3 demonstrated defects (FAIL 1, 2, 3), 4 preventive measures (FAIL 4, 5, 6, 7)

Documentation
- Claims: 0 verified, 1 in FAIL (D2, 1 finding), D1 counted in Code
- Findings by type: 1 demonstrated defect (FAIL 8)

CROSS-DOMAIN SUMMARY
- Domains: Code, Documentation
- Claims: 24 (15 verified, 7 in FAIL with 8 findings, 1 falsified-only, 1 counted through another claim)
- Survived: 4/6 stress tests passed
- Failure categories: 4 systemic patterns
- Invariants: 4 found, 4 touched, 1 enforced by a mechanism that bites on the changed path (invariant 3); 3 not (1, 2, 4)
- Hypotheses: 6 requiring further investigation
- Hidden behaviors: 5 detected (3 are problems typed as findings, 1 hypothesis, 1 noise)
- Findings by type: 4 demonstrated defects, 4 preventive measures, 3 falsified hypotheses (1 of them conditionally)
- Critical issues: 0 demonstrated defects of critical severity; preventive measures of critical severity: 0. Two demonstrated defects of high severity (FAIL 1, FAIL 3)
- Executed: nothing run (reasoning only). The claims below 80 and the tests said to be red rest on tracing only
- Proposed: 3 checks and 6 writes awaiting an answer
- Recommendation: do not rely on this script as the guard of private names until FAIL 1, 2 and 3 are fixed. The three one-line fixes are small, and `scripts/test_check.py` already holds a test for each, so by my trace they should turn green once fixed

## PROPOSED EXECUTABLE CHECKS

| # | Claim | Confidence now | Check | Confirms if | Refutes if | Cost and side effects | Status |
|---|-------|----------------|-------|-------------|------------|-----------------------|--------|
| 1 | C9, FAIL 1 | 90 (the test result is run-only) | `python -I -m unittest scripts.test_check.PrivateTest.test_whole_term_glued_in_output_is_still_masked` (method name `test_whole_word_term_glued_in_output_is_still_masked`, `scripts/test_check.py:341`) | the test is red with "message hidden" missing or the term in the output | green | runs the script in a temp copy of the repo; writes only to the system temp dir | proposed |
| 2 | C4 and C6, FAIL 2 and 3 | 90 | `test_second_badge_mismatch` (`:171`) and `test_two_words_joined_any_way` (`:284`) | red | green (then re-check that the trace missed a path) | same; the second needs a writable temp dir, and on Windows the `\n` variant shows the CRLF case | proposed |
| 3 | C21, hypotheses 1-6 | 80 or lower | run the whole `scripts/test_check.py` on Python 3.8 and 3.12, plus the hypothesis cases above as new tests | as stated in HYPOTHESES | as stated | temp dirs; needs two interpreters; the symlink test needs privileges on Windows | proposed |

Proposed writes (none made):
1. `scripts/check.py:400`: `term_patterns(terms, substring=True)`.
2. `scripts/check.py:223`: `for b in badges:`.
3. `scripts/check.py:90`: `SEP = r"[\W_]*"`.
4. `scripts/check.py:301-302`: report the tracked terms file as an ERROR instead of skipping it silently.
5. Docstring `scripts/check.py:10`, `:15-17`, `:22-26`, `:42-44` and `README.md:249-250`: align with the code after the fixes (FAIL 8 needs only the text change).
6. `CHANGELOG.md`: an entry under `## Unreleased` (`CHANGELOG.md:5`) for these fixes.

Do you approve any of these checks or writes? Nothing is run or written without an answer.
