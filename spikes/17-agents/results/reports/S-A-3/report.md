# Adversarial verification: scripts/check.py

**Cost estimate (large request, cost accepted, every choice settled, so the verification started at once):** 1 file in scope (`scripts/check.py`, 532 lines); 4 domains detected (Code, Documentation, Data, UX); 32 claims; nothing run. Ground truth read only, not verified: `scripts/test_check.py`, `scripts/check_facts.py`, `scripts/pre-commit`, `README.md` (Repository checks section), `CHANGELOG.md`, `.claude-plugin/plugin.json`, `.gitignore`, `skills/adversarial-verify/evals/evals.json` (ids and the `(Facts` markers), `skills/adversarial-verify/evals/facts/NOT_COMPUTABLE`, `facts/37.py`, `facts/42.py`, `facts/_parse_day.py`.

Reference files: `references/ux.md` was read because UX (terminal output) is in the target. `references/pre-code.md` was not read: the file proposes no future work and is not a spike report. `references/execution.md` was not read: no run was approved.

## INTAKE

- **Target:** every domain the skill detects in `scripts/check.py` (as requested): **Code** (the checker's logic), **Documentation** (module docstring, usage/help text, error messages), **Data** (the file formats it enforces: `evals.json`, `facts/NOT_COMPUTABLE`, the fact-file header, the private-terms list), **UX** (its command-line output). Tests domain not detected: `check.py` is not a test file. `scripts/test_check.py` was read as ground truth, and what it reveals is listed under OUT OF SCOPE.
- **Depth:** standard (requested).
- **Scope:** the whole of `scripts/check.py` (requested; there is no diff and no history, so the "changed path" in the invariant checks is the file as it stands).
- **Execution mode:** reasoning only (requested). Nothing was run or written except this report. Every test result named below is predicted from the code, not observed.
- Consent applies to one verification only. A later verification starts at reasoning only again. To run the checks proposed at the end, approve them by name.

---

# DOMAIN 1: CODE

## VERIFICATION DOMAIN
Code

## GROUND TRUTH
- The module docstring as a specification: `scripts/check.py:2-50`.
- `README.md:244-263` (Repository checks), `CHANGELOG.md:3`, `CHANGELOG.md:14`, `CHANGELOG.md:24`, `CHANGELOG.md:26`, `CHANGELOG.md:45`.
- The test suite that specifies the behaviour: `scripts/test_check.py` (read, not run).
- Callers: `scripts/pre-commit:9` (`--strict --staged`). `scripts/check_facts.py` shares the facts layout.
- Data in the field: `.claude-plugin/plugin.json:3`, `README.md:1`, `CHANGELOG.md:5` (`## Unreleased` comes before `## 4.2`), the eval ids and the `(Facts` markers in `evals.json`, `facts/NOT_COMPUTABLE:4-12`.

## INVARIANTS
Where I looked: the tree has no `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, `SPEC.md`, `PLAN.md` or `ADR/` (full file listing of `./tree`). The project states its invariants in the `check.py` docstring (`scripts/check.py:2-47`), `README.md:244-254`, `CHANGELOG.md:3` and the `test_check.py` docstring (`scripts/test_check.py:1-5`). I found 9. All 9 are touched, because `check.py` is the mechanism that enforces them.

| # | Invariant | Source | Touched by | Enforced by (file:line / test name) | Bites on changed path? |
|---|-----------|--------|------------|-------------------------------------|------------------------|
| I1 | SKILL.md version = **every** skill badge in the README = plugin.json = newest CHANGELOG entry | scripts/check.py:10-12, README.md:249, CHANGELOG.md:3 | check_version | scripts/check.py:222-241; test `test_second_badge_mismatch` (scripts/test_check.py:171) | **No** for badges after the first: scripts/check.py:223 compares `badges[:1]` only (FAIL #1). Yes for plugin.json and CHANGELOG |
| I2 | No private term in any tracked file's content or name, whatever joins its parts and whatever its accents | scripts/check.py:13-19, README.md:250 | check_private, term_patterns, normalize | scripts/check.py:259-323; tests scripts/test_check.py:233-316 | **Partly**: one separator character at most (FAIL #2); letters with no decomposition are not folded (FAIL #5) |
| I3 | Terms are never printed: any output line containing one is masked | scripts/check.py:22-23, scripts/test_check.py:4-5 | mask | scripts/check.py:397-414; tests scripts/test_check.py:331-348 | **No** for `=` terms: scripts/check.py:400 builds whole-word patterns (FAIL #3) |
| I4 | The private-terms list is never committed | README.md:250 ("The list is never committed"), scripts/check.py:15 ("untracked file") | check_private | `.gitignore:1` only; test `test_terms_file_is_gitignored` (scripts/test_check.py:365) checks only the ignore entry | **No**: `git add -f` bypasses `.gitignore`, and scripts/check.py:301-302 skips the file by basename, so the hook passes (FAIL #4) |
| I5 | evals.json format: keys, integer ids 1..n in order, non-empty fields, tags from 21 | scripts/check.py:6-9 | check_evals | scripts/check.py:163-207; tests scripts/test_check.py:104-163 | Yes |
| I6 | Every eval from 29 on that states facts has a fact file or a reason, not both; fact files are bound by prompt sha256 | scripts/check.py:34-38 | check_facts | scripts/check.py:457-501; tests scripts/test_check.py:522-568 | Yes (gaps of form only, Data domain #10, #11) |
| I7 | Every named references/*.md exists; every .md in references/ is named in SKILL.md | scripts/check.py:39-44 | check_references | scripts/check.py:506-520; tests scripts/test_check.py:456-509 | Yes |
| I8 | Every Markdown table row has as many cells as its header; fenced blocks skipped | scripts/check.py:30-33 | check_tables | scripts/check.py:353-381; tests scripts/test_check.py:420-450 | **Partly**: a mismatched fence closes a block (FAIL #7); delimiters with fewer than 3 hyphens are not seen (FAIL #9) |
| I9 | The script always runs to its summary and reports through ERROR lines | scripts/test_check.py:55-58 ("the script did not run to its summary") | main, run_checks | none for missing files | **No**: an OSError on SKILL.md, README.md, plugin.json, CHANGELOG.md or a fact file escapes as a traceback (FAIL #6) |

## DECOMPOSED CLAIMS
1. C1: evals.json is checked for its key set, integer (non-bool) ids, consecutive ids in file order, duplicates and empty fields. Mode: Deductive
2. C2: Every assertion of an eval with id ≥ 21 must start with `[substance]` or `[format]` followed by text. Mode: Deductive
3. C3: The SKILL.md version matches every skill badge in the README. Mode: Deductive
4. C4: The SKILL.md version matches plugin.json and the newest numbered CHANGELOG entry. Mode: Deductive
5. C5: The parts of a term may be joined by anything that is not a letter or digit, or by nothing. Mode: Deductive
6. C6: Matching ignores case, accents and Unicode forms. Mode: Deductive
7. C7: JSON strings are scanned after decoding escapes. Mode: Deductive
8. C8: A file that is not UTF-8 is still scanned. Mode: Deductive
9. C9: No output line ever shows a private term. Mode: Deductive
10. C10: The terms list is skipped by the scan and never committed. Mode: Deductive
11. C11: Tables are checked outside fenced blocks, and every table is found. Mode: Deductive
12. C12: Reference files are checked in both directions. Mode: Deductive
13. C13: Fact files: orphans, hash binding, and file-and-reason conflicts are errors. Mode: Deductive
14. C14: `--staged` checks exactly the staged content and always removes its temporary copy. Mode: Deductive (Abductive on Windows)
15. C15: The exit code is non-zero exactly when there are errors, and the report always ends with the summary. Mode: Deductive
16. C16: Neutral wording gives warnings only, and evals.json is excluded. Mode: Deductive

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Missing completeness (a promise enforced on part of its domain) | 5: first badge only (scripts/check.py:223); one separator character (scripts/check.py:90); mask not substring (scripts/check.py:400); stroke letters not folded (scripts/check.py:93-96); terms-list file exempted, never refused (scripts/check.py:301-302) | scripts/check.py |
| Silent fallthrough | 3: a `~~~` line closes a ```` ``` ```` fence, so later tables are skipped silently (scripts/check.py:363-366); 1- and 2-hyphen delimiters are never seen as tables (scripts/check.py:341); duplicate or orphan NOT_COMPUTABLE lines are silently accepted (scripts/check.py:494) | scripts/check.py |
| Assumed environment | 3: LF line endings (a CRLF break is 2 separator characters, scripts/check.py:90); a console encoding that has `—` (scripts/check.py:527, hypothesis); a POSIX-style `--prefix` for checkout-index (scripts/check.py:389, hypothesis) | scripts/check.py |
| Inconsistent error handling (an instance of silent fallthrough's opposite: unhandled crash) | 1 pattern, 7 call sites: read_text without an OSError guard (scripts/check.py:214, 217, 227, 237, 332, 356, 476, 512) | scripts/check.py |

## OUT OF SCOPE (listed, not verified)
- `scripts/test_check.py:171-173` `test_second_badge_mismatch`: by trace of scripts/check.py:223 it should be **red** on the current code.
- `scripts/test_check.py:284-289` `test_two_words_joined_any_way`, variant `f"{a.upper()}  {b}"` (two spaces): by trace of scripts/check.py:90 it should be **red**. Variant `f"{a}\n{b}"` passes on POSIX only. On Windows, `append()` (scripts/test_check.py:83-85) writes in text mode, so `\n` becomes `\r\n`, two characters. That is a test-environment artifact: the result depends on the platform the test runs on.
- `scripts/test_check.py:341-344` `test_whole_word_term_glued_in_output_is_still_masked`: by trace of scripts/check.py:400 it should be **red**, and `assert_no_leak` should trip as well.
- `scripts/pre-commit:9-17` runs `check.py` and `check_facts.py` but not `test_check.py`. That is consistent with tests that are red but unnoticed (Hypothesis H1).
- `README.md:250` lists "line break" among the accepted joins, but a CRLF break is not accepted (same root cause as FAIL #2). `README.md:254` says a fact file carries "the sha256 of the prompt of every eval it covers", but the code binds a file to exactly one eval, by its stem (scripts/check.py:468-482). `README.md:253` says "every file in `references/`", but the code checks `.md` files only (scripts/check.py:137).

## VERIFICATION RESULTS

### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| C1 | Key set, id type, consecutiveness, duplicates, empty fields | scripts/check.py:180-184 (extra/missing keys), 186 (`type(i) is not int` rejects bool), 191-193, 203-207 (both duplicate and gap reported). Deductive, 92 |
| C2 | Tags from eval 21 | scripts/check.py:74-75, 201: `TAG_RE.match` anchors at `^`, requires `\s+\S` after the tag. Deductive, 92 |
| C4 | plugin.json and newest numbered CHANGELOG entry | scripts/check.py:231-236 (string type, exact compare); 237 `^## +([0-9][0-9.]*)\b` with `re.search` takes the first numbered heading, skipping `## Unreleased` (CHANGELOG.md:5) and landing on `## 4.2` (CHANGELOG.md:10) = plugin.json:3 = README.md:1 badge. Deductive, 90 |
| C7 | JSON escapes decoded | scripts/check.py:279-289 walks keys and values; 313-317, 322-323. Deductive, 90 |
| C8 | Non-UTF-8 scanned | scripts/check.py:112-122: Latin-1 decoding never fails, so every byte sequence yields text. Deductive, 88 (UTF-32 gap: Documentation FAIL #13) |
| C12 | References both ways | scripts/check.py:508-520: names from SKILL and refs vs on-disk `.md` set, and on-disk set minus names in SKILL. Deductive, 90 |
| C13 | Fact files | scripts/check.py:467-473 (orphan), 476-482 (hash in first 2000 chars vs sha256 of the prompt), 495-496 (both), 497-501 (neither). Cross-checked against the data: every eval ≥ 29 with `(Facts` (evals.json lines 381…712) has a file (35, 37-40, 48, 49, 51-53, 56, 57) or a NOT_COMPUTABLE line (30, 32-34, 36, 41, 43, 45, 50). Deductive, 88 |
| C16 | Neutral wording | scripts/check.py:328-336 only calls `rep.warning`; `skill_docs` (140-142) excludes evals.json. Deductive, 92 |

### FALSIFIED HYPOTHESES
| # | Location | Suspected defect | Check (quote) | Status (falsified / conditionally) | Could it have failed? (how shown, or the check that would complete it) | Paths not covered | Mode | Confidence |
|---|----------|------------------|-------|------------------------------------|------------------------------------------------------------------------|-------------------|------|------------|
| FH1 | scripts/check.py:255 | A UTF-8 BOM before a `#` comment line in `.check-private-terms` turns the comment into a term | Trace: `decode(f.read())` → `data.decode("utf-8-sig")` (scripts/check.py:120) strips the BOM before `l.strip().startswith("#")` | Conditionally | The trace exercises the suspected path. Completing check: `test_bom_before_a_comment_keeps_it_a_comment` (scripts/test_check.py:323) seen green, and red when `utf-8-sig` is changed to `utf-8` | UTF-16 terms file with BOM (decoded by scripts/check.py:116, not traced through the test) | Deductive | 82 |
| FH2 | scripts/check.py:426-440 | `--staged` leaves `check-staged-*` behind when the root is not a repository | Trace: `tmp` is created at 428, `staged_tree` returns None at 393, and `finally` at 438-440 removes `tmp` | Conditionally | Completing check: `test_staged_outside_git_is_a_clear_error` (scripts/test_check.py:389-396) seen green, and red with the `finally` removed | Process killed by a signal (the `finally` does not run) | Deductive | 85 |
| FH3 | scripts/check.py:186 | `true` as an id passes as integer 1 | `if type(i) is not int:  # bool is an int subclass: reject it` | Conditionally | `type(True) is bool`, so the check rejects it. Completing check: `test_boolean_id` (scripts/test_check.py:125) red when 186 is changed to `isinstance` | check_facts (scripts/check.py:463) still puts `True` in `ids`, but check 1 already fails the run | Deductive | 88 |
| FH4 | scripts/check.py:237 | `## Unreleased` above the newest release breaks the version check | `re.search(r"^## +([0-9][0-9.]*)\b", …, re.M)` requires a digit after `## ` | Conditionally | Trace on CHANGELOG.md:5 and :10 gives `4.2`. Completing check: run on the repo, then red with the regex loosened to `\S+` | A numbered heading inside a fenced block of CHANGELOG.md would count | Deductive | 86 |

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| 1 | scripts/check.py:223 | `for b in badges[:1]:` | Demonstrated defect | Medium | The docstring (scripts/check.py:10) and README.md:249 promise "every skill badge". README gains a second badge `badge/skill-v2.0-` (exactly what `test_second_badge_mismatch`, scripts/test_check.py:171-173, does). `badges` = `["4.2","2.0"]`, only `"4.2"` is compared, no error, exit 0. A stale version badge ships | Deductive | 95 | `for b in badges:` (one error per mismatching badge) |
| 2 | scripts/check.py:90 | `SEP = r"[\W_]?"  # anything that is not a letter or digit, possibly nothing` | Demonstrated defect | High | The comment and the docstring (scripts/check.py:16-18) say "anything", but the regex allows at most **one** character. Term `quillane dorvex`, text `QUILLANE  dorvex` (two spaces, scripts/test_check.py:286), `Quillane - Dorvex`, or a CRLF line break between the words (2 characters; Windows checkouts, Hypothesis H3): pattern `quillane[\W_]?dorvex` does not match, so the private name is committed. The same SEP is used in `mask`, so such a form is also printed unmasked when another check echoes it | Deductive | 92 | `SEP = r"[\W_]*"`; add the CRLF and `" - "` variants to `test_two_words_joined_any_way` |
| 3 | scripts/check.py:399-400 | `# substring patterns: when hiding output, err on the side of hiding too much` / `pats = term_patterns(terms)` | Demonstrated defect | High | The comment promises substring patterns, but the call omits `substring=True`, so for a term `=zqvorblax` the mask pattern is whole-word (scripts/check.py:265, 275). Key `zqvorblaxlabs` in an eval → check 1 prints `unexpected keys ['zqvorblaxlabs']` (scripts/check.py:182). Check 3 does not flag it (whole word). The mask does not hide it, so the private term is printed to the terminal or CI log. That breaks scripts/check.py:22-23 and is what scripts/test_check.py:341-344 asserts against | Deductive | 93 | `pats = term_patterns(terms, substring=True)` |
| 4 | scripts/check.py:301-302 | `if os.path.basename(rel) == TERMS_FILE:` / `continue` | Preventive measure | High | Nothing refuses a tracked or staged terms list. `git add -f .check-private-terms` (or any file of that name in any subdirectory) is in `files`, is skipped silently, and no other check looks at it, so the hook (scripts/pre-commit:9) passes and the commit publishes every private term at once. Likelihood: low (needs `-f` or a copy in a subfolder), impact: total. Invariant I4, category missing completeness | Deductive | 90 | Instead of skipping: `if os.path.basename(rel) == TERMS_FILE: rep.error(rel, "the private-terms list is tracked or staged: remove it from the index (git rm --cached)"); continue` |
| 5 | scripts/check.py:93-96 | `unicodedata.normalize("NFKD", text)` … `if not unicodedata.combining(c)` | Preventive measure | Medium | "Ignores … accents" (scripts/check.py:15-16, README.md:250) holds only for letters that decompose. `Ł`, `ø`, `đ`, `æ`, `œ`, `ı`, `þ` have no decomposition, so the term `Lukasz` misses `Łukasz`, and `Soren` misses `Søren`. Turns into a leak when a private name is configured in its ASCII form and written with its native letter (or the reverse) | Deductive | 85 | A fold table after NFKD: `str.maketrans({"ł":"l","ø":"o","đ":"d","æ":"ae","œ":"oe","ı":"i","þ":"th"})` applied in `normalize` (both sides use it); or list the gap in "Not caught" |
| 6 | scripts/check.py:214, 217, 227-229, 237, 332, 356, 476, 512 | `plugin = json.loads(read_text(root, PLUGIN, rep))` / `except ValueError as e:` | Demonstrated defect | Low | A commit that deletes or renames `.claude-plugin/plugin.json` (or CHANGELOG.md, README.md, SKILL.md, a fact file listed then unreadable): `FileNotFoundError` is not a `ValueError`, so it escapes `run_checks` and `main` (only a `finally`, scripts/check.py:438). The output is a traceback and no summary, and every error already collected (and masked) is lost. Fail-closed (exit 1), but it breaks I9 | Deductive | 90 | Catch `OSError` around each fixed-path read: `rep.error(rel, "missing or unreadable")` and skip that comparison. Alternatively, wrap `run_checks` in `except Exception as e: rep.error("internal", e.__class__.__name__)` |
| 7 | scripts/check.py:361-366 | `if fence is None: fence = f.group(1)[0]` / `else: fence = None` | Demonstrated defect | Low | Any fence line closes any open fence, but CommonMark closes only with the same character and at least the same length. Text: ```` ``` ```` / `~~~` / ```` ``` ```` / then a broken table. The `~~~` closes early, and the real closing ```` ``` ```` *opens* a new fence, so every later table in the file is skipped silently (false negative). Not triggered by any current file (none mixes fence types) | Deductive | 88 | Track `(char, length)`: close only on `s` starting with ≥ length of the same char and nothing else after it |
| 8 | scripts/check.py:341, 369 | `DELIM = re.compile(r"^\s*\|?\s*:?-{3,}…` / `and "\|" in lines[i] + lines[i - 1]` | Preventive measure | Low | A paragraph line with an inline pipe followed by `---` (a setext heading or thematic break): `---` matches DELIM, the header has 2 cells and the delimiter has 1, so the error "table delimiter has 1 cells" appears on valid Markdown and blocks the commit (false positive). Not triggered by the current files | Deductive | 78 | Require the delimiter to contain a `\|`, or at least 2 cells when the header has more than 1, before treating it as a table |
| 9 | scripts/check.py:341 | `-{3,}` | Preventive measure | Low | GFM accepts delimiter cells of one hyphen (`\|-\|-\|`). Such a table is never detected, so its rows are never counted (silent gap in I8). Turns into a defect when a contributor writes a compact delimiter | Deductive | 75 | `-{1,}` (the GFM rule; the spec citation is from memory: confirm it) |
| 16 | scripts/check.py:527 | `print(f"checked ({scope}): … — {len(rep.errors)} error(s)…")` | Preventive measure | Low | `—` (U+2014) printed to a stdout whose encoding lacks it (Windows with output piped or captured and a code page such as cp932) → `UnicodeEncodeError` after all checks: traceback, no summary. Unconfirmed: Hypothesis H2 | Abductive | 45 | Use `-` in the summary, or `sys.stdout.reconfigure(errors="replace")` at start |

## STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|
| S1 | Scale Shift | C1 evals check | Yes | 85 | Zero evals → "no 'evals' list" (scripts/check.py:171-173). Non-list `evals` → same. Hundreds of evals: `ids.count` is quadratic but trivial at this size (scripts/check.py:203) |
| S2 | Time Travel | C4 CHANGELOG/plugin compare | Yes | 82 | A future `## 4.3-rc1`: scripts/check.py:237 captures `4.3`, while a SKILL version `4.3-rc1` fails scripts/check.py:216 → "no version in the frontmatter". Fail-closed, so a mismatch cannot pass silently |
| S3 | Existence Question | C7 decoded-JSON scan | Yes | 88 | Remove scripts/check.py:313-317/322-323 and a `z…`-escaped term in plugin.json becomes invisible to the raw-text scan. The layer earns its place (scripts/test_check.py:304-316) |
| S4 | Requirement Inversion | C12 references | Yes | 85 | If an unnamed helper `.md` in references/ were wanted, only scripts/check.py:519-520 would break. That strictness is deliberate (scripts/check.py:41-43: "a file nobody names is never read") |
| S5 | Scale Shift | C13 facts | Yes | 85 | Facts dir absent → `files = []` (scripts/check.py:465), so every eval with `(Facts` needs a reason, giving loud errors and no silent pass. A hash line after 2000 chars → "no 'prompt-sha256:' line", fail-closed |
| S6 | Scale Shift | C8 non-UTF-8 scan | **No** | 85 | Widen to UTF-32: a BOM `FF FE 00 00` takes the UTF-16 branch (scripts/check.py:114-116), and `00 00 FE FF` falls to Latin-1. Either way, letters are interleaved with NULs and a one-word term is missed. Not in the "Not caught" list: Documentation FAIL #13 |
| S7 | Time Travel | C16 neutral wording | Yes | 80 | Case-sensitive substrings (`Spring`, `Rails`, `Unity`) will give false warnings on ordinary words, and new technologies are absent, but warnings never block (scripts/check.py:336) |

## HYPOTHESES (Abductive: require further investigation)
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| H1 | Three tests (scripts/test_check.py:171, 284-289, 341-344) assert behaviours that scripts/check.py:223, :90 and :400 do not have | The three tests are red today and went unnoticed because the hook runs check.py, not the suite (scripts/pre-commit:9) | The code was edited after the suite last ran green (a regression), or the tests are newer than the code | Run `python3 -m unittest scripts/test_check.py` on a copy (Proposed check P1) |
| H2 | `—` in the summary (scripts/check.py:527) | On Windows with stdout piped and an ANSI code page lacking U+2014, `print` raises `UnicodeEncodeError` | Python's UTF-8 mode or the console API (interactive) makes it safe; cp1252 has `—` | Run with output piped under a code page without `—` (P6) |
| H3 | Windows checkouts with `core.autocrlf=true`; `git checkout-index` (scripts/check.py:389) applies eol conversion | A two-word term split over a line break is `a\r\nb` both in working-tree and `--staged` mode, so it is missed (FAIL #2) | The index blobs are LF and checkout-index writes them as LF | Scratch repo with autocrlf on, stage a split term, run `--staged` (P7) |
| H4 | `--prefix=` + a Windows temp path with a drive letter and backslashes (scripts/check.py:389) | git accepts it and writes into `tmp` | git mishandles it, so `--staged` reports "not a git repository" (misleading, scripts/check.py:431) or writes elsewhere | Run `--staged` on Windows (P7) |
| H5 | `--staged` materialises symlinks from the index; `read_text` follows them (scripts/check.py:126) | A tracked symlink's blob (its target path, which may hold a term) is never scanned; the target file's content is scanned instead | On systems without symlink support git writes the link text as a file, which is then scanned correctly | Stage a symlink whose target path contains a test term (P7) |

## HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| HB1 | scripts/check.py:301 | The terms file in the root is untracked and not scanned (scripts/check.py:15) | Any file named `.check-private-terms` in **any** directory is skipped, tracked or not | Preventive measure (FAIL #4) | 90 |
| HB2 | scripts/check.py:247-249 | Terms come from the env var **or** the file | An env var set to an empty string wins and the file is ignored, so without `--strict` the result is only a warning | Preventive measure (Data FAIL #12) | 88 |
| HB3 | scripts/check.py:136, 465 | "Files checked: the files tracked by git" (scripts/check.py:46) | Checks 6 and 7 list directories on disk: an untracked fact file satisfies check 6 in working-tree mode | Demonstrated defect (Documentation FAIL #14) | 85 |
| HB4 | scripts/check.py:128 with 214 and 512 | One "not UTF-8" error per file | SKILL.md is read with `rep` twice, so the same error is reported twice | Not a problem (cosmetic) | 85 |
| HB5 | scripts/check.py:319-321 | "No private term appears" | Only the first occurrence per term per file is reported: fix, rerun, find the next | Not a problem (by design; UX note) | 90 |

## ADVERSARIAL SCAFFOLD FINDINGS
- **Reviewer blind spots:** `SEP` carries a comment ("anything … possibly nothing") that reads exactly like `*` but is `?`. `mask` carries a comment saying "substring" above a call that does not pass `substring=True`. `badges[:1]` sits inside a `for` loop, so it looks like iteration over every badge. In all three, the comment states the intent and the code does something else.
- **Highest-risk claims (blast radius × probability):** (1) C9 output never shows a term (FAIL #3: leaks the secret it guards, triggered by any `=` term); (2) C5 separators (FAIL #2: common forms, plus every CRLF split); (3) C10 terms list never committed (FAIL #4: total disclosure, low probability).
- **Multi-step traces:** `=term` configured → glued form `termlabs` as an evals.json key → check 3 whole-word: no hit → check 1 echoes the key (scripts/check.py:182) → `mask` whole-word (scripts/check.py:400): no hit → term printed. Windows autocrlf → `a\r\nb` → `[\W_]?` → miss in detection **and** in masking. `git add -f .check-private-terms` → in `files` → basename skip (scripts/check.py:301) → no other check → hook exit 0.
- **Subtlety flags:** the `?` in `SEP` (scripts/check.py:90); `[:1]` (scripts/check.py:223); the default argument `substring=False` (scripts/check.py:259) silently used by `mask`; `else: fence = None` (scripts/check.py:366) closing any fence type.

### SUMMARY (Code)
- Domain: Code
- Claims: 16. 8 verified (PASS), 7 claims in FAIL (10 findings: #1-#9, #16), 4 falsified (all conditionally; FH2 and FH3 are sub-claims of C14 and C1)
- Survived: 6/7 stress tests passed
- Failure categories: 4 systemic patterns
- Invariants: 9 found, 9 touched, 3 fully enforced by a mechanism that bites (I5, I6, I7); I1, I2, I8 partly; I3, I4, I9 not
- Hypotheses: 5
- Hidden behaviors: 5 detected (3 are problems)
- Findings by type: 5 demonstrated defects (#1, #2, #3, #6, #7), 5 preventive measures (#4, #5, #8, #9, #16), 4 falsified hypotheses (4 conditionally)
- Critical issues: 0 demonstrated defects of critical severity (preventive of critical severity: 0)
- Executed: nothing (reasoning only)
- Recommendation: do not rely on check 3 as the privacy guarantee until #2, #3 and #4 are fixed. #1 lets a stale badge through.

---

# DOMAIN 2: DOCUMENTATION

## VERIFICATION DOMAIN
Documentation: the module docstring (scripts/check.py:2-50), the argparse help (scripts/check.py:418-421) and the error messages.

## GROUND TRUTH
The code of scripts/check.py itself, README.md:244-263, scripts/test_check.py.

## INVARIANTS
Same nine as the Code domain. The docstring restates I1-I8 (it is their source). Respected? I1: yes, as text ("every skill badge"); the code is what fails it (Code #1). I3: the text says "never printed", and the code breaks it (Code #3). The rest are stated correctly.

## DECOMPOSED CLAIMS
1. Do1: The "Not caught" list (scripts/check.py:24-26) names every known gap of check 3. Mode: Deductive
2. Do2: "Files checked: the files tracked by git" (scripts/check.py:46-47) describes what is read. Mode: Deductive
3. Do3: The usage line (scripts/check.py:49) matches the flags parsed. Mode: Deductive
4. Do4: "Requires Python 3.8 or later" holds for the constructs used. Mode: Deductive
5. Do5: Error messages give the right line numbers and say how to fix the problem. Mode: Deductive
6. Do6: The docstring's description of checks 1, 2, 4-7 matches the code. Mode: Deductive

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Missing completeness (limits list) | 1 (Do1) | scripts/check.py |
| Stale or overbroad statement | 1 (Do2) | scripts/check.py |

## VERIFICATION RESULTS
### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| Do3 | Usage | scripts/check.py:49 `[--strict] [--staged] [--root PATH]` = scripts/check.py:419-421. Deductive, 92 |
| Do4 | Python 3.8 | Constructs used: f-strings with `!r`, `yield from`, `subprocess.run(capture_output=…)` (3.7), `str.casefold`. No walrus operator, no `match`, no 3.9+ string methods or generics found on a full read. Deductive, 82 |
| Do5 | Messages | Table messages: the 0-based index of the delimiter equals the 1-based header line (scripts/check.py:373, 378). The hash message gives the exact value to set (scripts/check.py:482). The facts message names both remedies (scripts/check.py:501). Deductive, 88 |
| Do6 | Checks 1, 2, 4-7 described | Each statement matched against scripts/check.py:163-207, 212-241, 328-336, 344-381, 457-501, 506-520; the only discrepancies are those of Code #1 (the code, not the text, is wrong) and Do2. Deductive, 85 |

### FALSIFIED HYPOTHESES
None.

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| 13 | scripts/check.py:24-26 | `Not caught: a one-word term written as two words (…), UTF-16 files without a BOM; with =, also forms glued to other letters or digits.` | Demonstrated defect | Low | The list omits gaps the code has: UTF-32 files (scripts/check.py:114-122, stress S6); letters with no decomposition (Code #5); non-UTF-8 file names, decoded with `"replace"` (scripts/check.py:148, 394); separators of more than one character (Code #2, until fixed). A maintainer reads the list to know what to check by hand, and misses these | Deductive | 88 | Add the missing items, or fix the code and drop those items |
| 14 | scripts/check.py:46-47 | `Files checked: the files tracked by git (all files outside .git if git is not available).` | Demonstrated defect | Low | True for check 3 only. Checks 1, 2, 4, 5 read fixed paths, and checks 6 and 7 list directories on disk (scripts/check.py:136, 465). An untracked `facts/58.py` satisfies check 6 in working-tree mode. The docstring says this for references (scripts/check.py:43-44) but not for facts | Deductive | 85 | "Check 3 scans the files tracked by git (…). The other checks read their fixed files and folders as they are on disk (with --staged: as staged)." |

## STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|
| S8 | Time Travel | Do5 hash message | Yes | 85 | A maintainer 6 months on, prompt edited: the message names the file, the eval and the exact hash, and tells them to re-check the facts first (scripts/check.py:482) |
| S9 | Existence Question | Do4 version note | Yes | 80 | Delete it and Windows/older-Python users lose the only hint. README.md:246 repeats it, so it stays useful |
| S10 | Requirement Inversion | Do3 usage | Yes | 82 | Invert: a user passes `--root` with `--staged` from another repo. Terms still come from `args.root` (scripts/check.py:423), as the comment says, so the text stays true |

## HYPOTHESES
None beyond the Code domain.

## HIDDEN BEHAVIORS DETECTED
HB3 (Code domain) is the documentation-relevant one.

## ADVERSARIAL SCAFFOLD FINDINGS
- Reviewer blind spots: a "Not caught" list reads as complete because it exists.
- Highest-risk claims: Do1, Do2.
- Multi-step traces: docstring "never printed" → Code #3.
- Subtlety flags: none beyond Code.

### SUMMARY (Documentation)
- Claims: 6. 4 verified, 2 in FAIL, 0 falsified. Survived: 3/3. Failure categories: 2. Invariants: as Code (text respects them). Hypotheses: 0. Hidden behaviors: 0 new. Findings: 2 demonstrated defects, 0 preventive, 0 falsified. Critical: 0.

---

# DOMAIN 3: DATA

## VERIFICATION DOMAIN
Data: the formats check.py enforces: `evals.json` (scripts/check.py:73-78, 163-207), `facts/NOT_COMPUTABLE` (scripts/check.py:483-494), the fact-file header `prompt-sha256:` (scripts/check.py:476-482), the private-terms sources (scripts/check.py:246-256), the version fields.

## GROUND TRUTH
Data already in the field: evals.json (57 evals; `(Facts` markers from 25 on), facts/NOT_COMPUTABLE:1-12, facts/37.py:1, facts/42.py:1, facts/_parse_day.py:1-5, plugin.json:3, README.md:1, CHANGELOG.md:5, :10.

## INVARIANTS
I5, I6 (see the Code domain). Both bite on the current data.

## DECOMPOSED CLAIMS
1. Da1: The evals.json schema is enforced exactly (key set, types). Mode: Deductive
2. Da2: Every NOT_COMPUTABLE line is a well-formed reason for a real eval, given once. Mode: Deductive
3. Da3: Every eval from 29 on that states facts is detected. Mode: Deductive
4. Da4: The terms-list formats (env, file) are read as documented. Mode: Deductive
5. Da5: The fact-file header binds the file to the current prompt. Mode: Deductive

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Constraint gap (format accepted too loosely) | 3 (Da2, Da3, Da4) | scripts/check.py |

## VERIFICATION RESULTS
### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| Da1 | Eval schema | Exact key set (scripts/check.py:180-184), string non-empty prompt and expected_output (191-193), non-empty list of non-empty strings (194-200). Not checked: top-level keys other than `evals` (harmless). Deductive, 88 |
| Da5 | Hash binding | sha256 of `str(prompt).encode("utf-8")` vs the header (scripts/check.py:477-482). facts/37.py:1 and facts/42.py:1 carry the line. Shared helpers (`_parse_day.py`) are excluded by the `_` prefix (scripts/check.py:469) and carry no hash; they are code that check_facts.py runs, not prompt-bound data. Deductive, 85 |

### FALSIFIED HYPOTHESES
None.

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| 10 | scripts/check.py:500 | `if "(Facts" in str(e.get("prompt", ""))` | Preventive measure | Low | Detection is a case-sensitive literal. A new eval written `(facts: …)` or `Facts:` without the parenthesis states facts, needs no file or reason, and passes. Today every fact-stating eval uses `(Facts` (evals.json `(Facts` at lines 324…712) | Deductive | 85 | `re.search(r"\(\s*facts\b", prompt, re.I)`, plus a warning for `Facts:` outside parentheses |
| 11 | scripts/check.py:490-494 | `reasons[int(m.group(1))] = m.group(2)` | Preventive measure | Low | A reason for a nonexistent eval (`99: …`), for an eval below 29, or for an eval with no `(Facts`, is accepted silently. A duplicated id overwrites without notice. Stale reasons pile up after evals are renumbered or edited | Deductive | 85 | Error on a duplicate id. Error (or warning) when the id is not an eval ≥ FACTS_FROM whose prompt states facts |
| 12 | scripts/check.py:247-256 | `if raw is not None:` / `terms = raw.split(",")` … `if not l.strip().startswith("#")` | Preventive measure | Low | (a) `CHECK_PRIVATE_TERMS=""` exported in a shell or CI overrides an existing `.check-private-terms`, so without `--strict` the check degrades to a warning (HB2). (b) An inline comment `Name # client` becomes the term `name client`, which needs a 1-character join and no longer finds `Name` alone. Nothing reports either | Deductive | 85 | (a) treat an empty or blank env var as unset, or say in the warning which source was used; (b) document "whole-line comments only", or strip ` #…` suffixes |

## STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|
| S11 | Scale Shift | Da1 | Yes | 85 | An eval with 0 assertions → "no assertions" (scripts/check.py:195-197). An id of 0 or a negative id → "not consecutive" (scripts/check.py:206) |
| S12 | Requirement Inversion | Da5 | Yes | 82 | Invert: the prompt is unchanged but the shared helper changes. No hash fails, but check_facts.py reruns the files (scripts/pre-commit:12-17 triggers on any path under evals/), so a false fact is still caught |
| S13 | Time Travel | Da5 | Yes | 80 | A hash written in uppercase hex by a future tool → "no 'prompt-sha256:' line" (regex `[0-9a-f]`, scripts/check.py:477): a misleading message, but fail-closed |

## HYPOTHESES / HIDDEN BEHAVIORS
HB2 (Code domain) belongs to Da4. No others.

## ADVERSARIAL SCAFFOLD FINDINGS
- Blind spot: an exact-substring marker (`(Facts`) used as a schema switch.
- Highest risk: Da4 (privacy), then Da3, then Da2.
- Subtlety: `raw is not None` treats "set but empty" as "configured".

### SUMMARY (Data)
- Claims: 5. 2 verified, 3 in FAIL, 0 falsified. Survived: 3/3. Failure categories: 1. Findings: 0 demonstrated, 3 preventive. Critical: 0.

---

# DOMAIN 4: UX (command-line output)

## VERIFICATION DOMAIN
UX: the terminal output of `check.py` (scripts/check.py:397-414, 523-527) and its arguments. ux.md targets adapted to a CLI. Contrast, targets, motion and render widths do not apply: the output is plain uncoloured text with no layout.

## GROUND TRUTH
references/ux.md (Sensitive data, States, Real content), README.md:256-263 (the documented invocations), scripts/pre-commit (the main context: a commit blocked in a terminal or GUI client).

## INVARIANTS
I3 (no term on screen) and I9 (summary always shown) are UX-relevant. Both fail: see Code #3 and #6.

## DECOMPOSED CLAIMS
1. U1: No private data is visible in the output. Mode: Deductive
2. U2: Every error says where and what, so the user can act on it. Mode: Deductive
3. U3: The output always ends with a summary of counts. Mode: Deductive
4. U4: Errors are distinguishable from warnings. Mode: Deductive
5. U5: The output can be encoded on every supported console. Mode: Abductive

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Sensitive data on screen | 1 (U1, counted in Code #3) | scripts/check.py |
| Error state without a handle | 1 (U2, masked location) | scripts/check.py |

## VERIFICATION RESULTS
### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| U4 | Errors vs warnings | Prefix `ERROR` / `WARNING`, errors first, counts of each in the final line (scripts/check.py:106, 109, 524-527). Deductive, 88 |

### FALSIFIED HYPOTHESES
None.

### FAIL ❌
U1 fails as Code #3, U3 as Code #6 and U5 as Code #16 (each counted once, in Code). New in this domain:

| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| 15 | scripts/check.py:409-412 | `where = "[location hidden: its path contains a private term]"` | Preventive measure | Low | A blocked commit says only that *some* file has a private term in its path (or message), with no handle to find it. Under `--strict --staged` in a GUI git client the user has to search the whole tree by hand. Turns into a defect when the repo has many files | Deductive | 70 | Alternative A: print the index of the file in `git ls-files` order (`file #123 of the tracked list`). Improves: findable with `git ls-files \| sed -n 123p`. Worse: indices shift between runs. Cost: 2 lines. Alternative B: print the sha256 prefix of the path. Improves: stable. Worse: needs a helper to look it up. Cost: ~5 lines. Recommend A |

## STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|
| S14 | Scale Shift | U4 | Yes | 78 | Many warnings (README.md has 6 stack-term lines) come after the errors, so in a short terminal the errors scroll off the top. The summary keeps the counts, so the user knows to scroll up. Survives, with a note: print warnings first, or errors last |

## HYPOTHESES
H2 (Code domain).

## HIDDEN BEHAVIORS DETECTED
HB5 (Code domain): one hit per term per file, so the fix loop takes several runs.

## ADVERSARIAL SCAFFOLD FINDINGS
- Blind spot: a masking layer judged by its message, not by the line it fails to mask.
- Highest risk: U1 (Code #3), U3 (Code #6), U2 (#15).

### SUMMARY (UX)
- Claims: 5. 1 verified, 4 in FAIL (3 counted in Code, 1 new: #15), 0 falsified. Survived: 1/1. Findings new here: 1 preventive.

---

## CROSS-DOMAIN SUMMARY
- Domains: Code, Documentation, Data, UX
- Claims: 32 (16 + 6 + 5 + 5). 15 verified (PASS), 15 claims in FAIL (16 findings, each counted once), 4 falsified (all conditionally)
- Survived: 13/14 stress tests passed (S6 did not)
- Failure categories: 8 rows; distinct systemic patterns: 5 (missing completeness, silent fallthrough, assumed environment, unguarded reads, sensitive data on screen)
- Invariants: 9 found, 9 touched, 3 fully enforced by a mechanism that bites (I5, I6, I7); I1, I2, I8 partly; I3, I4, I9 not
- Hypotheses: 5 requiring further investigation
- Hidden behaviors: 5 detected (3 are problems)
- Findings by type: **7 demonstrated defects** (#1, #2, #3, #6, #7, #13, #14), **9 preventive measures** (#4, #5, #8, #9, #10, #11, #12, #15, #16), **4 falsified hypotheses** (4 conditionally)
- Critical issues: 0 demonstrated defects of critical severity (preventive of critical severity: 0). High: #2, #3 (demonstrated), #4 (preventive)
- Changes touching several domains: #3 (Code + UX + the docstring's promise), #2 (Code + README.md:250 out of scope), #6 (Code + UX)
- Pre-code: not applicable
- Executed: 0 tests run (reasoning only); mutation probe not run
- Proposed: 8 checks and 6 writes awaiting an answer
- Recommendation: **do not trust** check 3 (private names) or the output masking as a guarantee until #2, #3 and #4 are fixed. Fix #1 before the next release (the version badge). The other checks (evals, facts, references, neutral wording) hold as traced.

## PROPOSED EXECUTABLE CHECKS
| # | Claim | Confidence now | Check (command, test or query) | Confirms if | Refutes if | Cost and side effects | Status |
|---|-------|----------------|--------------------------------|-------------|------------|-----------------------|--------|
| P1 | H1, and that the tests for #1, #2, #3 bite | 79 (run-only) | `python3 -m unittest scripts/test_check.py` from the repo root | `test_second_badge_mismatch`, `test_two_words_joined_any_way` (two-space variant), `test_whole_word_term_glued_in_output_is_still_masked` red; everything else green | Those three green (then my trace of 223/90/400 is wrong) | Runs check.py ~70 times; each test copies the repo into a fresh system temp dir and some run `git init` there; FactsTest also runs `check_facts.py`, which needs `rustc` and `node` ≥ 22.6 (README.md:246). Reads the repo, writes only temp dirs. Optional: put the temp dirs on a memory-backed filesystem (tmpfs/RAM disk): needs your separate consent to create one, and free memory above the repo size (a few MB) plus the Rust build output | proposed |
| P2 | #4 | 90 (risk), run would demonstrate | In a scratch clone: `echo zqvorblax > .check-private-terms && git add -f .check-private-terms && python3 scripts/check.py --strict --staged` | exit 0 with the list staged | an error naming the file | Scratch clone only; writes there; your working copy untouched | proposed |
| P3 | #5 | 85 | Copy; append `Łukasz` to README.md; `CHECK_PRIVATE_TERMS=Lukasz python3 scripts/check.py --root <copy>` | exit 0, no private-term error | "private term #1" error | Copy only | proposed |
| P4 | #6 | 90 | Copy; delete `.claude-plugin/plugin.json`; run check.py on it | traceback, no `checked (` line, exit 1 | an ERROR line and the summary | Copy only | proposed |
| P5 | #7 | 88 | Copy; append ```` ``` ````, `~~~`, ```` ``` ````, `\| a \| b \|`, `\|---\|---\|`, `\| 1 \|` to SKILL.md; run check.py | exit 0 (broken table missed) | "table row" error | Copy only | proposed |
| P6 | H2 / #16 | 45 | On Windows: `py -3 scripts/check.py \| more` under a code page without `—` (e.g. `chcp 932` with a matching system locale) | `UnicodeEncodeError`, no summary | Summary printed | Reads only; changes the console code page of that window | proposed |
| P7 | H3, H4, H5 | 40-50 | On Windows, scratch repo with `core.autocrlf=true`: stage a file with a two-word test term split over lines, and a symlink whose target path contains a test term; run `check.py --strict --staged` | Term missed (H3); `--staged` works (H4); symlink blob unscanned (H5) | The opposite of each | Scratch repo only | proposed |
| P8 | Mutation probe: do the tests protect check.py's key lines? | n/a | 5 hand mutations, each followed by `python3 -m unittest scripts/test_check.py`: scripts/check.py:186 `type(i) is not int` → `isinstance(i, int)`; :206 `!=` → `==`; :301 skip removed; :481 `!=` → `==`; :411 `hit(msg)` → `False`. (There is no diff, so the scope is these 5 lines and not the changed lines) | Each mutant killed by at least one test | A survivor: a missing test | Writes: mutates a **copy** (never your working copy), restored or discarded after; 5 full suite runs (see P1 for tools and memory); slow. Memory-backed filesystem suggested as in P1, with separate consent | proposed |

Proposed writes (Step 5; nothing is written without your confirmation):
- `scripts/check.py:223`: `for b in badges:` (fixes #1).
- `scripts/check.py:90`: `SEP = r"[\W_]*"` (fixes #2).
- `scripts/check.py:400`: `pats = term_patterns(terms, substring=True)` (fixes #3).
- `scripts/check.py:301-302`: report a tracked or staged terms list as an ERROR instead of skipping it (fixes #4).
- `scripts/check.py:93-96`, 361-366, 214-241, 527 and the docstring at 24-26, 46-47: fold table (#5), fence matching (#7), OSError guards (#6), ASCII summary (#16), docstring corrections (#13, #14).
- `scripts/test_check.py`: regression tests for #4 (force-added terms file), #5 (`Ł`), #6 (missing plugin.json reaches the summary), #7 (mixed fences), and the CRLF variant of #2. Plus `CHANGELOG.md` under `## Unreleased`: one entry for the check.py fixes.
- Not found in ./tree, so no update proposed: `TODO.md`, `SPEC.md`, `PLAN.md`, `ADR/`, `.claude/`, `AGENTS.md`.

**Which of P1-P8 may I run (and may the runs use a memory-backed filesystem), and which of the proposed writes should I make?**
