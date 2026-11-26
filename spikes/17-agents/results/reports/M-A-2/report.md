# Adversarial verification — `scripts/check.py`, `scripts/check_facts.py`, `scripts/pre-commit`, `scripts/test_check.py`

**Cost estimate (large request, cost accepted, every choice settled):** 4 files in scope (check.py 532 lines, check_facts.py 118, pre-commit 19, test_check.py 622, 1,291 lines in all); 5 domains detected (Code, Tests, Documentation, Data, UX); about 60 claims; nothing run.

## INTAKE

- **Target:** every domain Step 0 detects in the four files: **Code** (the logic of check.py, check_facts.py and pre-commit), **Tests** (test_check.py), **Documentation** (module docstrings, the hook's comments, usage lines, error messages, test comments), **Data** (the file formats these scripts define and enforce: `evals.json`, `facts/NOT_COMPUTABLE`, the `prompt-sha256:` binding, `.check-private-terms`), and **UX** (the command-line and terminal output of the checks and of the hook). The request named the target.
- **Depth:** standard, as requested.
- **Scope:** all of these four files. There is no diff and no history, so every line is in scope. Other files of `./tree` were read only to establish ground truth.
- **Execution mode:** reasoning only, as requested. Nothing was run and nothing was written except this report. Each claim that only a run can decide stays at 79 or below and is listed under PROPOSED EXECUTABLE CHECKS.
- No choice used a default. To change one, say for example "deep" or "approved checks: the unit test suite".
- Reference files read: `references/ux.md`, because UX is in the target. `references/pre-code.md` was not read because nothing here proposes work not yet done. `references/execution.md` was not read because no run was approved.

---

# DOMAIN 1 — CODE

## VERIFICATION DOMAIN
Code: `scripts/check.py`, `scripts/check_facts.py`, `scripts/pre-commit`.

## GROUND TRUTH
- The scripts' own contracts: the `scripts/check.py:1-51` docstring, the `scripts/check_facts.py:1-19` docstring, and the comments at `scripts/pre-commit:2-5` and `:10-11`.
- The tests that state the expected behaviour: `scripts/test_check.py` (as a specification only; nothing was run).
- The repository description of the checks: `README.md:244-263` and `CHANGELOG.md:3`.
- The data the checks run on: `.claude-plugin/plugin.json`, `README.md:1` (the badge), `CHANGELOG.md:5-10` (an `## Unreleased` entry comes before `## 4.2`), `skills/adversarial-verify/evals/facts/*` (`35.py`–`57.py`, `52.rs`, `53.ts`, `_parse_day.py`, `NOT_COMPUTABLE`), and `.gitignore`.
- Python semantics (re, unicodedata, argparse, subprocess) and POSIX `sh` semantics, traced by reasoning.

## INVARIANTS
**Where I looked:** no `CLAUDE.md`, `AGENTS.md` or `CONTRIBUTING.md` exists anywhere in `./tree` (I listed every file). The project states its invariants in `scripts/check.py:2-47` ("the repository's own invariants"), `scripts/check_facts.py:10-14`, `scripts/pre-commit:2-5`, `README.md:244-263`, `CHANGELOG.md:3` and `.gitignore:1`. **Found: 11. Touched: 11.** All of them are touched because these files are the mechanisms that enforce them.

| # | Invariant | Source | Touched by | Enforced by (file:line / test name) | Bites on changed path? |
|---|-----------|--------|------------|-------------------------------------|------------------------|
| I1 | evals.json has exactly 4 keys, integer ids 1..n in order, non-empty fields, tags from eval 21 on | scripts/check.py:6-9 | check_evals | scripts/check.py:163-207; EvalsTest (scripts/test_check.py:104-163) | Yes |
| I2 | SKILL.md's version equals **every** skill badge in the README, plugin.json and the newest CHANGELOG entry | scripts/check.py:10-12, CHANGELOG.md:3 | check_version | scripts/check.py:212-241; test_second_badge_mismatch (scripts/test_check.py:171-173) | **No for every badge after the first**: scripts/check.py:223 compares only `badges[:1]` (FAIL C-F3). The test would bite. |
| I3 | No private term in any file content or name, whatever the separator between its parts | scripts/check.py:13-19 | check_private, term_patterns | scripts/check.py:259-323; test_two_words_joined_any_way (scripts/test_check.py:284-289) | **No for separators of 2+ characters** (FAIL C-F2) |
| I4 | Terms are never printed: every output line containing one is masked | scripts/check.py:22-23, scripts/test_check.py:4-5 | mask | scripts/check.py:397-414; test_whole_word_term_glued_in_output_is_still_masked (scripts/test_check.py:341-344) | **No for `=` terms** (FAIL C-F1) |
| I5 | The terms list is never committed | scripts/check.py:423 comment, README.md:250, .gitignore:1 | check_private | .gitignore:1; test_terms_file_is_gitignored (scripts/test_check.py:365-366) | **No against `git add -f`**: scripts/check.py:301-302 skips the file by name in every mode, including `--staged` (FAIL C-P1) |
| I6 | Technology-bound terms are warned about | scripts/check.py:27-29 | check_neutral | scripts/check.py:328-336; NeutralTest | Yes (warnings only, by design) |
| I7 | Table rows have as many cells as their header | scripts/check.py:30-33 | check_tables | scripts/check.py:341-381; TablesTest | Yes, with two gaps (C-P3, C-P4) |
| I8 | Each eval ≥29 that states facts has a fact file or a reason, and each fact file carries the hash of its prompt | scripts/check.py:34-38 | check_facts (check.py) | scripts/check.py:457-501; FactsTest | Yes |
| I9 | A fact file must assert and print `ok <id>`; **a missing toolchain is an error, never a silent skip** | scripts/check_facts.py:10-14 | check_facts.py main | scripts/check_facts.py:88-111; nothing tests a missing toolchain | **No**: scripts/check_facts.py:91-93 skips and does not count a failure (FAIL C-F4) |
| I10 | The hook runs `--strict --staged`, which fails without private terms | scripts/pre-commit:5, README.md:260 | pre-commit | scripts/pre-commit:9; no test of the hook | **No**: the hook omits `--strict` (FAIL C-F5) |
| I11 | Reference files named in SKILL.md exist and every file in references/ is named | scripts/check.py:39-44 | check_references | scripts/check.py:506-520; ReferencesTest | Yes |

## DECOMPOSED CLAIMS
1. The version check compares SKILL.md's version with every README skill badge — Deductive
2. plugin.json and the first numeric CHANGELOG heading are compared with SKILL.md — Deductive
3. A term's parts match when joined by any run of non-alphanumeric characters, or by nothing — Deductive
4. An `=` term matches only as a whole word — Deductive
5. Output masking hides every configured term, including `=` terms glued to other letters — Deductive
6. JSON string escapes are decoded and scanned — Deductive
7. Files that are not UTF-8 are still scanned (UTF-16 with BOM, otherwise Latin-1) — Deductive
8. The terms file is never committed and never scanned — Deductive
9. Terms come from CHECK_PRIVATE_TERMS or `.check-private-terms` — Deductive
10. `--staged` checks exactly the staged content — Deductive
11. The temporary staged tree is always removed — Deductive
12. Fenced code blocks are skipped by the table check — Deductive
13. The table check's cell counting matches how the tables render — Abductive (GFM is not in the tree)
14. Named references exist and every reference file is named — Deductive
15. Fact files belong to existing evals; a file and a reason for the same eval is an error — Deductive
16. check_facts.py treats a missing toolchain as an error — Deductive
17. check_facts.py requires a real assertion outside comments and strings — Deductive
18. check_facts.py requires the last line to be `ok <id>`; no files means failure — Deductive
19. The pre-commit hook runs check.py with `--strict --staged` — Deductive
20. The hook runs the fact files on exactly the staged files when evals change — Deductive
21. A missing core file (README, plugin.json, CHANGELOG, SKILL.md) is reported as an ERROR line — Deductive
22. The neutral-wording check gives warnings only and never fails — Deductive

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| **Missing completeness** (a flag or loop that does not reach every case the contract names) | `badges[:1]` (C-F3); `mask` without `substring=True` (C-F1); force-added terms file not covered (C-P1) | scripts/check.py |
| **Silent fallthrough** (a failure condition turned into success) | toolchain skip that counts as a pass (C-F4); the hook without `--strict` turns "terms not checked" into a warning (C-F5); an empty CHECK_PRIVATE_TERMS silently disables the terms file (C-P2) | scripts/check_facts.py, scripts/pre-commit, scripts/check.py |
| **Assumed environment** | LF-only line breaks between the parts of a term (C-F2, CRLF case); `python3` on Windows (UX-P1) | scripts/check.py, scripts/pre-commit |
| **Stated-versus-enforced drift** (a docstring or comment promises a behaviour the code does not have; the tests side with the promise) | C-F1, C-F2, C-F3, C-F4, C-F5: five instances, all in code that guards a commit | all three code files |

## OUT OF SCOPE (listed, not verified)
Statements in files outside the scope that describe the drifted behaviours:
- `README.md:249`: "every skill badge in the README". The code checks only the first (C-F3).
- `README.md:250`: "Matching ignores … how the parts of a term are joined". False for multi-character joins (C-F2). "any output line containing a term is masked" is false for `=` terms (C-F1).
- `README.md:254`: check_facts.py "fails … if a needed toolchain … is missing". It skips (C-F4).
- `README.md:260`: the hook "runs --strict --staged before every commit". It runs without `--strict` (C-F5).
- `CHANGELOG.md:3`: "`scripts/check.py` fails if they differ". Not for a second badge (C-F3).

## VERIFICATION RESULTS

### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| 2 | plugin.json and the newest CHANGELOG entry are compared | scripts/check.py:226-241: a non-dict or non-string version is an error (232-234), and the first `^## +[0-9]` heading is compared (237-241). `## Unreleased` (CHANGELOG.md:5) is correctly skipped because the regex needs a digit. Conf 90 |
| 4 | `=` terms match whole words only | scripts/check.py:265,275: lookarounds `(?<![^\W_])…(?![^\W_])` reject a neighbouring letter or digit and accept `_` and punctuation. Conf 90 |
| 6 | JSON escapes are decoded | scripts/check.py:313-323: `json.loads`, then every key and value through `json_strings` (279-289), normalized and searched. Conf 90 |
| 7 | Non-UTF-8 files are scanned | scripts/check.py:112-122: `decode` never raises (Latin-1 is total), and `utf-8-sig` strips a BOM. Conf 90 |
| 10 | `--staged` checks the staged content | scripts/check.py:386-394: `checkout-index -a` into tmp, then the file list from `ls-files`, and `root = tmp` (433) for every check, so reference_files and the facts dir are read from the staged tree. The terms come from the working repo (423), which is intended. Conf 88 |
| 11 | The staged tmp dir is always removed | scripts/check.py:426-440: `try/finally` with `rmtree(..., ignore_errors=True)` covers exceptions inside run_checks. Conf 90 |
| 14 | References exist and are named | scripts/check.py:506-520: names are collected from SKILL.md and from every reference file, but only SKILL.md's names count as "named" (515-516), matching the docstring at :41-43. Conf 90 |
| 15 | Fact files belong to evals; a file plus a reason is an error | scripts/check.py:467-473 (non-digit stem or unknown id is an error), :495-496 (intersection). Conf 90 |
| 17a | The Python assertion gate ignores comments and strings | scripts/check_facts.py:45-50: `ast.walk` sees only statements, so comments and string contents never count. Conf 90 (see C-P5 for what it does count) |
| 18 | The ok-line rule and the no-files rule | scripts/check_facts.py:106-109: the last non-blank stdout line must equal `ok <stem>`; :113 returns 1 when `files` is empty (for example an unknown id). Conf 90 |
| 20 | The hook runs facts on the staged files | scripts/pre-commit:12-17: `git checkout-index -a --prefix="$tmp/"` and then `--root "$tmp"`. check_facts.py runs with `cwd=FACTS` under that root (scripts/check_facts.py:82,100). Conf 85 (see hidden behavior HB-2: the *scripts* come from the working tree) |
| 22 | Neutral wording never fails | scripts/check.py:328-336 only calls `rep.warning`. Conf 92 |

### FALSIFIED HYPOTHESES
| # | Location | Suspected defect | Check (quote) | Status | Could it have failed? | Paths not covered | Mode | Confidence |
|---|----------|------------------|-------|--------|------------------------|-------------------|------|------------|
| FH1 | scripts/check.py:321 | NFKD and casefold change string length, so the reported line number is wrong | `body.count(chr(10), 0, m.start()) + 1` | falsified | Yes: it would be wrong if the count ran on the original `text` with an offset from `body`. Both come from the same `body`, and normalization never adds or removes `\n` | Lines separated only by `\r` or U+2028 (counted as one line) | Deductive | 85 |
| FH2 | scripts/pre-commit:15 | `rc=$?` captures the status of the assignment, not of check_facts.py | `out="$(...)"; rc=$?` | falsified | Yes: in POSIX `sh` the status of an assignment that holds only a command substitution is the substitution's status | Shells that do not follow POSIX (none expected for `#!/bin/sh`) | Deductive | 88 |
| FH3 | scripts/check_facts.py:99-111 | A failed compile step leaves a stale `r` that the ok-line check reads | `for step in steps: … break` / `else:` | falsified | Yes, if the `else` ran after a `break`. Python runs a loop's `else` only when no `break` happened | none | Deductive | 92 |
| FH4 | scripts/check.py:186 | `true` is accepted as id 1 because bool is a subclass of int | `if type(i) is not int:` | falsified | Yes, had it used `isinstance`; `type(...) is` rejects bool. test_boolean_id (scripts/test_check.py:125-127) asserts it | none | Deductive | 92 |

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| C-F1 | scripts/check.py:399-400 | `# substring patterns: when hiding output, err on the side of hiding too much` / `pats = term_patterns(terms)` | Demonstrated defect | high | `term_patterns` defaults to `substring=False` (scripts/check.py:259), so an `=` term gets the whole-word pattern in `mask` too (:265). With `CHECK_PRIVATE_TERMS==acme`, an eval key `acmelabs` produces `ERROR …evals.json eval #57: unexpected keys ['acmelabs'] …` (:182). The lookahead fails on `l`, so the line is printed **unmasked** and the private name reaches the terminal or CI log. This is exactly the case test_whole_word_term_glued_in_output_is_still_masked (scripts/test_check.py:341-344) builds. The docstring promise at scripts/check.py:22-23 is broken | Deductive | 92 | `pats = term_patterns(terms, substring=True)` at scripts/check.py:400 |
| C-F2 | scripts/check.py:90 (used at :274) | `SEP = r"[\W_]?"  # anything that is not a letter or digit, possibly nothing` | Demonstrated defect | high | `?` allows **at most one** separator character. The parts of the term `quillane dorvex` are not matched in `quillane  dorvex` (two spaces), `quillane - dorvex`, `quillane, dorvex`, or `quillane\r\ndorvex` (a CRLF line break, which is the norm in working-tree files on Windows with `core.autocrlf=true`). The docstring at scripts/check.py:16-18 promises "anything that is not a letter or digit … line breaks". The two-space subtest of test_two_words_joined_any_way (scripts/test_check.py:286) builds this case. A private name gets committed undetected | Deductive | 92 | `SEP = r"[\W_]*"`. Add `a - b` and `a\r\nb` variants to scripts/test_check.py:286 |
| C-F3 | scripts/check.py:223 | `for b in badges[:1]:` | Demonstrated defect | medium | README.md holds badge `skill-v4.2` at line 1. Appending a second `badge/skill-v2.0` (as test_second_badge_mismatch, scripts/test_check.py:171-173, does) gives `badges == ['4.2','2.0']`, but only `'4.2'` is compared, so there is no error. Contradicts scripts/check.py:10 ("every skill badge") and CHANGELOG.md:3 | Deductive | 95 | `for b in badges:` |
| C-F4 | scripts/check_facts.py:91-93 | `if steps is None: print(f"skip {name}: toolchain not found"); continue` | Demonstrated defect | high | On a machine without `rustc` or `node`, 52.rs and 53.ts print `skip …`, `failed` stays 0, `files` is non-empty, and :113 returns **0**. A false fact in a Rust or TypeScript file passes. The docstring at scripts/check_facts.py:10 says "A missing toolchain is an error, never a silent skip". Through the hook, the skip line is also never shown (UX-F1) | Deductive | 95 | Count it: `print(f"FAIL {name}: toolchain not found ({ext})"); failed += 1; continue` |
| C-F5 | scripts/pre-commit:9 | `"$py" -I "$root/scripts/check.py" --staged --root "$root" \|\| exit 1` | Demonstrated defect | high | With no `.check-private-terms` file and no `CHECK_PRIVATE_TERMS` (a fresh clone, or a machine where the developer forgot), check_private only warns (scripts/check.py:297) and the commit goes through **with private names not checked**. The hook's own comment (scripts/pre-commit:5) and README.md:260 say it runs `--strict` | Deductive | 95 | Add `--strict` to scripts/pre-commit:9 |
| C-P1 | scripts/check.py:301-302 | `if os.path.basename(rel) == TERMS_FILE: continue` | Preventive measure | medium | Turns into a defect if someone runs `git add -f .check-private-terms` (`.gitignore:1` does not stop a forced add). `--staged` lists it, skips it, and reports nothing, so the list of private names is committed and pushed, contradicting "the list is never committed" (scripts/check.py:423, README.md:250). Likelihood: low, but the impact is total | Deductive | 88 | In `--staged` mode (and in tracked-file mode), report `ERROR .check-private-terms: the private terms list is tracked or staged`; add a StagedTest case |
| C-P2 | scripts/check.py:247-250 | `raw = os.environ.get("CHECK_PRIVATE_TERMS")` / `if raw is not None: terms = raw.split(",")` | Preventive measure | medium | Turns into a defect if `CHECK_PRIVATE_TERMS` is set but empty (for example `export CHECK_PRIVATE_TERMS=` in a profile or CI template). The file is then ignored, `terms == []`, and without `--strict` (C-F5) the run passes with only a warning | Deductive | 88 | Treat an empty or blank variable as unset (`if raw and raw.strip():`), or merge both sources; document the precedence |
| C-P3 | scripts/check.py:361-366 | `if fence is None: fence = f.group(1)[0] else: fence = None` | Preventive measure | low | The stored fence character is never compared, so a `~~~` line inside a ```` ``` ```` block (or a shorter fence) closes it. Lines after it are then table-checked while still inside a code block, or a real table after it is skipped. Turns into a defect when a doc shows a fence inside a fence | Deductive | 88 | Close only on a line starting with the same character and at least the same length (CommonMark) |
| C-P4 | scripts/check.py:345 | ``s = re.sub(r"`[^`]*`", "x", line)`` | Preventive measure | low | In GitHub-flavoured Markdown an unescaped `\|` inside a code span still splits the cell; only `\\\|` protects it. A row the check accepts (test_escaped_pipe_and_code_span_are_not_separators, scripts/test_check.py:441-443) can render with an extra cell on GitHub. Turns into a defect when a table cell holds code with a pipe | Abductive (the GFM spec is not in the tree) | 65 | Count unescaped pipes inside code spans as separators, or document that the check follows a non-GFM rule |
| C-P5 | scripts/check_facts.py:50 | `return any(isinstance(n, (ast.Assert, ast.Raise)) for n in ast.walk(tree))` | Preventive measure | low | A `raise` in the *reproduced code under test* (like `raise ValueError('bad day')` in skills/adversarial-verify/evals/facts/_parse_day.py:11), copied into a fact file that asserts nothing, passes the gate. So does an `assert` in a function that is never called. No current fact file does this (I grepped every facts/*.py) | Deductive | 85 | Require an `assert` (or a `raise` of `AssertionError`/`SystemExit`) at module level or reachable from it; keep the ok-line rule as the second guard |
| C-P6 | scripts/check_facts.py:37 | `".rs": re.compile(r'//[^\n]*\|/\*.*?\*/\|"(?:\\.\|[^"\\])*"', re.S)` | Preventive measure | low | A char literal `'"'` opens a "string" that swallows code up to the next `"`, and raw strings `r#"…"#` are not handled. Both can hide a real `assert!` (false FAIL, the safe direction) or expose one inside a raw string (false pass). Turns into a defect with a fact file holding `'"'` or `r#"assert!"#` | Deductive | 80 | Strip char literals and raw strings first, or compile with a `#[deny]` lint marker convention |
| C-P7 | scripts/check.py:214, 217, 227-230, 237 | `plugin = json.loads(read_text(root, PLUGIN, rep))` / `except ValueError` | Preventive measure | low | A staged deletion or rename of README.md, CHANGELOG.md, plugin.json or SKILL.md raises an uncaught `FileNotFoundError`. The run stops with a traceback and no summary line. It still exits non-zero (fails closed), but the remaining checks never run and the message names no invariant | Deductive | 90 | Catch `OSError` in check_version (and check_neutral, check_tables) and report `ERROR <file>: missing` |

## STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|
| S1 | Scale Shift | Claim 10 (`--staged`) at zero and at 10× | yes | 82 | Zero: an empty index gives `files == []` and :436 skips the checks, exit 0, which is right for an empty commit. Not a git repo gives an explicit ERROR (:430-432). 10×: `checkout-index -a` copies the whole index on every commit, a linear cost with no correctness change |
| S2 | Time Travel | Claim 15 plus the hash binding, in 6 months | yes | 80 | Someone edits `facts/_parse_day.py` (a shared helper with no hash). The hook still reruns every fact because the trigger is the `evals/` path (scripts/pre-commit:12). Someone edits only a prompt: the hash mismatch fails (scripts/check.py:481-482). Open: an edit to scripts/check_facts.py alone does not rerun the facts |
| S3 | Existence Question | Claim 18 (the `ok <id>` last-line rule) | yes | 85 | Delete it mentally: a fact file that calls `sys.exit(0)`, or a Rust `main` that returns before its `assert_eq!`, would pass. The rule is the only guard against early exit, so it should exist |
| S4 | Requirement Inversion | The consecutive-ids rule (scripts/check.py:206-207) when someone wants to *remove* an eval | yes | 80 | Removing eval k forces renumbering. Fact files keep their old names, so `facts/<old>.py` then points at another eval's prompt: hash mismatch (:481) or orphan (:471). Both fail loudly, so the inversion cannot silently corrupt the bindings |

## HYPOTHESES (Abductive — require further investigation)
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| HY1 | scripts/check_facts.py:63 compiles Rust with `-O` | Release mode turns off integer-overflow panics, so a future fact that relies on an overflow panic would pass | No fact relies on overflow (52.rs uses only `assert_eq!`/`assert_ne!`) | Add a fact `let x: u8 = 255; let _ = x + 1;` and run with and without `-O` |
| HY2 | scripts/check.py:389 passes `--prefix=tmp + os.sep` | On Windows git receives `C:\…\check-staged-x\` and writes correctly | git mishandles the backslash prefix and writes elsewhere or fails, so `--staged` reports "not a git repository" | `py -3 scripts/check.py --staged` on Windows with a staged file |
| HY3 | scripts/pre-commit:12 greps `git diff --cached --name-only` for `^skills/…` | With the default `core.quotePath=true`, a staged non-ASCII path under evals/ prints as `"skills/…"` with a leading quote, so it is missed | Every eval file name is ASCII, so this never happens in practice | Stage `skills/adversarial-verify/evals/facts/é.py` and run the hook |

## HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| HB-1 | scripts/check.py:247-250 | "Terms come from CHECK_PRIVATE_TERMS … or the untracked file" (:14-15) | The variable takes precedence whenever it is set, even when empty, and the file is then never read | see C-P2 | 90 |
| HB-2 | scripts/pre-commit:9, :15 | "run the repository invariant checks on exactly what is staged" (:2) | The *content* is staged, but the *checker* (check.py, check_facts.py) is the working-tree copy, so a staged change to the checker is not what runs, and a broken but unstaged checker decides the commit | Preventive (low) | 88 |
| HB-3 | scripts/pre-commit:6-18 | — | The hook never runs `scripts/test_check.py`, so C-F1/C-F2/C-F3, which the unit tests would catch, can be committed | Preventive (medium), cross-ref T-F3 | 90 |
| HB-4 | scripts/check.py:301 | The terms file is excluded from scanning | It is also excluded from *any* report when tracked or staged | see C-P1 | 88 |
| HB-5 | scripts/check_facts.py:50 | "an assert or raise statement" (:12) | Any `raise` anywhere in the file, including in code under test or dead code | see C-P5 | 85 |
| HB-6 | scripts/check.py:82-88, :330 | "technology-bound terms" | Case-sensitive, mostly without word boundaries: `React` matches "Reaction", `Spring` matches "Springboard", and `python`/`docker` in lower case are missed | — (warnings only) | 85 |
| HB-7 | scripts/check.py:147-152, :306-310 | "files tracked by git" | A tracked file deleted from the working tree but not staged gives `ERROR …: unreadable file`. This fails closed and is acceptable | — | 85 |

## ADVERSARIAL SCAFFOLD FINDINGS
- **Reviewer blind spots:** a single default argument (`term_patterns(terms)` vs `substring=True`), a slice `[:1]`, and a `?` quantifier. Each is one or two characters, sits under a comment or docstring that describes the intended behaviour, and is easy to read as correct.
- **Highest-risk claims:** (1) C-F2 and C-F1 together: private names can be committed (multi-character separators) and printed (`=` terms); (2) C-F5: the hook does not enforce `--strict`, so on a machine without terms nothing about private names is enforced; (3) C-F4: eval facts in Rust and TypeScript pass silently without toolchains.
- **Multi-step traces:** empty `CHECK_PRIVATE_TERMS` (HB-1) → terms `[]` → hook without `--strict` (C-F5) → only a warning → commit with private names unchecked. Missing `rustc` → `skip` (C-F4) → rc 0 → the hook prints `out` only on failure (scripts/pre-commit:17) → nobody sees the skip. Hook does not run the unit tests (HB-3) → regressions C-F1..C-F3 enter the repo although three tests (scripts/test_check.py:171, :286, :341) would catch them.
- **Subtlety flags:** scripts/check.py:90 (the comment says "anything", the regex says one character); scripts/check.py:399-400 (the comment says substring, the call says the default); scripts/check.py:223 (a slice that looks like a guard); scripts/check_facts.py:92 (`skip` printed in the same style as `ok`).

### SUMMARY
- Domain: Code
- Claims: 12 verified (PASS), 12 in FAIL (5 demonstrated defects, 7 preventive measures), 4 falsified
- Survived: 4/4 stress tests passed
- Failure categories: 4 systemic patterns
- Invariants: 11 found, 11 touched, 5 enforced by a mechanism that bites on the path (I1, I6, I7, I8, I11); 6 do not bite (I2, which checks the first badge only, and I3, I4, I5, I9, I10)
- Hypotheses: 3 requiring further investigation
- Hidden behaviors: 7 detected
- Findings by type: 5 demonstrated defects, 7 preventive measures, 4 falsified hypotheses (0 conditionally)
- Critical issues: 0 demonstrated defects of critical severity (preventive critical: 0); 4 demonstrated defects of high severity
- Pre-code: not applicable
- Executed: 0 tests run
- Proposed: see the closing section
- Recommendation: do not trust the pre-commit hook as a privacy guard until C-F1, C-F2 and C-F5 are fixed; fix C-F4 before relying on the facts gate on machines without `rustc`/`node`.

---

# DOMAIN 2 — TESTS

## VERIFICATION DOMAIN
Tests: `scripts/test_check.py`.

## GROUND TRUTH
The production code under test (`scripts/check.py`, `scripts/check_facts.py`), the hook (`scripts/pre-commit`), and the "production" environment: a developer's clone running the hook (with an arbitrary shell environment, possibly Windows and possibly CRLF) and CI. For the bootstrap: `Base.setUp`/`run_check` (scripts/test_check.py:29-52), which copies the repo to a temp dir and runs check.py with `-I` in a subprocess and with the caller's environment.

## INVARIANTS
Same as Domain 1. The Tests-side question is whether a test bites: I2 test_second_badge_mismatch, I3 test_two_words_joined_any_way and I4 test_whole_word_term_glued_in_output_is_still_masked do bite (they would be red today). **I9 and I10 have no test** (T-F2, T-F3).

## DECOMPOSED CLAIMS
1. test_second_badge_mismatch fails when only the first badge is compared — Deductive
2. test_two_words_joined_any_way fails when the separator is limited to one character — Deductive
3. test_whole_word_term_glued_in_output_is_still_masked fails when masking uses whole-word patterns — Deductive
4. test_file_nobody_names can fail — Deductive
5. A missing toolchain is covered by a test — Deductive
6. The pre-commit hook is covered by a test — Deductive
7. Test results do not depend on the developer's shell environment — Deductive
8. Test results are the same on Windows and POSIX — Abductive
9. "No private test term may ever be printed" (:4-5) is asserted for every run — Deductive
10. Each private-term test asserts the specific invariant it names — Deductive
11. The bootstrap reproduces production: it copies the repo, runs as a subprocess with `-I`, and exits — Deductive
12. test_staged_leak_with_clean_working_tree distinguishes staged content from the working tree — Deductive
13. The .rs/.ts assertion-stripping regexes are covered — Deductive

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Tautological test | 1 (T-F1) | scripts/test_check.py |
| Missing negative tests / missing completeness | 3 (T-F2 toolchain, T-F3 hook, T-P5 .rs/.ts regexes) | scripts/test_check.py |
| Test-environment artifact | 2 (T-P1 inherited env, T-P2 Windows false reds) | scripts/test_check.py |
| Weak assertion | 2 (T-P3, T-P4) | scripts/test_check.py |

## VERIFICATION RESULTS
### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| 1 | test_second_badge_mismatch bites on C-F3 | scripts/test_check.py:171-173 appends `skill-v2.0` and expects "version mismatch". With scripts/check.py:223 nothing else errors, so it is red today. No fixture changes the result, so it would be the same in production. Conf 78 (a test result: run-only cap) |
| 2 | test_two_words_joined_any_way bites on C-F2 | The variant `f"{a.upper()}  {b}"` (scripts/test_check.py:286) has two spaces, which `[\W_]?` cannot join, so the subtest is red today. Conf 78 (run-only) |
| 3 | test_whole_word_term_glued_in_output_is_still_masked bites on C-F1 | scripts/test_check.py:341-344: the key `<T1>labs` with `=<T1>` produces an unmasked "unexpected keys" message, so "message hidden" is absent and the test is red. Conf 78 (run-only) |
| 11 | The bootstrap reproduces the production path | scripts/test_check.py:31-37, :49-52: a full copy of the repo files the checks read, and check.py run as a separate process with `-I` and `--root`, which is the hook's path (scripts/pre-commit:9) minus `--staged`. `--staged` has its own class (:369-402). Conf 85 |
| 12 | Staged and working tree are distinguished | scripts/test_check.py:382-387: the term is staged and then the working tree is cleaned. `--staged` fails and the working tree passes, so the test could fail either way. Conf 85 |
| 10 | Most private-term tests assert the named invariant | scripts/test_check.py:233-298 assert `"private term #1/#2"` plus `assert_no_leak` (:62). Conf 85 (exceptions: T-P3) |

### FALSIFIED HYPOTHESES
| # | Location | Suspected defect | Check (quote) | Status | Could it have failed? | Paths not covered | Mode | Confidence |
|---|----------|------------------|-------|--------|------------------------|-------------------|------|------------|
| TF-H1 | scripts/test_check.py:547-552 | test_prompt_changed_after_its_facts passes vacuously if `"day > 31"` is not in eval 37's prompt | `.replace("day > 31", "day > 28")` with no guard | conditionally falsified | If the text were absent the prompt would not change, check.py would pass, and `assert_fails` would go **red**, not falsely green. So the missing guard cannot produce a false pass. evals.json contains `day > 31` 3 times, but I could not see the line of eval 37 (truncated by the reader) | Complete it with `self.assertIn("day > 31", d["evals"][36]["prompt"])` | Deductive | 75 |

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| T-F1 | scripts/test_check.py:475-479 | `self.assertIn("orphan.md", r.stdout + self.ref("orphan.md"))` | Demonstrated defect (tautological test) | low | `self.ref("orphan.md")` itself contains `orphan.md`, so the assertion is always true. The return code is never checked either. Removing check_references entirely leaves this test green. (The same invariant is covered for real by :481-485 and :502-510) | Deductive | 95 | `self.assert_fails(r, "orphan.md", "never named in SKILL.md")` |
| T-F2 | scripts/test_check.py:575-578 | `self.assertEqual(r.returncode, 0, …)` / `\d+ fact file\(s\), 0 failed` | Demonstrated defect (missing negative test; a test that passes on the defect) | medium | Without `rustc`/`node` the runner prints `skip 52.rs`/`skip 53.ts` and still reports `13 fact file(s), 0 failed`, exit 0, so this test is green on the defect C-F4. No test removes a toolchain from PATH. The invariant scripts/check_facts.py:10 has no mechanism that bites | Deductive | 88 | A test that runs check_facts.py with `env=dict(os.environ, PATH=<dir with only python>)` and asserts a non-zero exit and "toolchain"; make test_runner_passes_on_the_repo assert `"skip" not in r.stdout` |
| T-F3 | scripts/test_check.py (whole file) | — (no test mentions `pre-commit`; I searched the file) | Demonstrated defect (missing completeness: touched invariant I10 with nothing that bites, and it is actually violated, C-F5) | medium | The hook's `--strict` promise is broken (scripts/pre-commit:9) and no test fails | Deductive | 90 | Add a StagedTest that runs `sh scripts/pre-commit` in the temp repo with no terms and asserts non-zero, and one that stages a fact change with a false fact |
| T-P1 | scripts/test_check.py:43-45 | `env = dict(os.environ)` | Preventive measure (test-environment artifact: changed defaults) | medium | Turns into a defect when the developer has `CHECK_PRIVATE_TERMS` exported. Every test that passes `terms=None` inherits it, and the variable overrides the terms file (HB-1). test_terms_file_with_bom_and_comments (:318-321) then checks the env terms, not the file, and goes red. test_missing_terms_is_said_not_silent and test_missing_terms_fails_in_strict_mode (:354-360) go red. With an **empty** exported variable they become false greens for the file path | Deductive | 85 | `env.pop("CHECK_PRIVATE_TERMS", None)` in run_check before applying `terms` |
| T-P2 | scripts/test_check.py:351, :83-85 | `os.symlink(...)` / `open(..., "a")` then `f.write("\n" + text + "\n")` | Preventive measure (test-environment artifact: false red) | low | On Windows without symlink privilege, test_unreadable_file_is_an_error errors in `os.symlink` (a false red). Text-mode append writes `\r\n`, so the `f"{a}\n{b}"` variant of :286 becomes `a\r\nb` and is red on Windows **only**. That variant is, however, a real defect (C-F2), so here the false red is a true red. The repo supports Windows (scripts/check.py:50, scripts/pre-commit:4) | Deductive | 75 | `skipUnless` symlink support; write with `newline=""` and add an explicit `\r\n` variant |
| T-P3 | scripts/test_check.py:300-302, :311-316 | `self.assert_fails(..., "notes16.txt")` / `self.assert_fails(..., "plugin.json")` | Preventive measure (weak assertion) | low | Any ERROR that mentions the file passes the test. For example, if plugin.json were broken by the edit, the "not valid JSON" error would satisfy test_json_escape without any private-term detection | Deductive | 85 | Also assert `"private term #1"` (and `"after decoding JSON escapes"` for :316) |
| T-P4 | scripts/test_check.py:64-68 | `def assert_passes(self, r): …` (no `assert_no_leak`) | Preventive measure | low | The docstring promises "no private test term may ever be printed" (:4-5), but passing runs are never leak-checked. Example: test_whole_word_opt_in (:257) passes with `=<T1>` while a warning could echo the term | Deductive | 85 | Call `self.assert_no_leak(r)` in `assert_passes` |
| T-P5 | scripts/test_check.py:580-617 | — (only .py fact files are mutated) | Preventive measure (coverage gap) | low | The regexes `ASSERTS`/`STRIP` for `.rs`/`.ts` (scripts/check_facts.py:34-39) are never exercised by a negative test. A broken `STRIP` (C-P6) would pass the suite | Deductive | 85 | Tests that comment out every `assert*!` in 52.rs and every `throw` in 53.ts and expect "no assertion". The gate runs only after `command` finds the toolchain (scripts/check_facts.py:90-95), so skip these tests when `shutil.which` finds no toolchain |
| T-P6 | scripts/test_check.py:32 | `for item in ("README.md", "CHANGELOG.md", "skills", ".claude-plugin", "scripts", ".gitignore"):` | Preventive measure (test-environment artifact: different resources), from stress row TS2 | low | Turns into a defect when check.py starts reading a new top-level file or folder (for example LICENSE or `docs/`): the temp copy lacks it, so the tests fail falsely or check nothing | Deductive | 80 | Copy the whole tree except `.git` and `__pycache__`, or build the list from `git ls-files` |

## STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|
| TS1 | Requirement Inversion | Claim 12: what if the user wants the working tree, not the index, checked? | yes | 80 | The same test asserts both directions (scripts/test_check.py:386-387), so inverting the requirement makes it go red in a known place |
| TS2 | Time Travel | Claim 11: in 6 months a new top-level file the checks read (say `docs/`) is added | no | 75 | `Base.setUp` copies a fixed list (scripts/test_check.py:32). A new file read by the checks is missing in the copy, and its tests then fail or prove nothing. Reported as T-P6 |
| TS3 | Scale Shift | Claim 10 at zero terms and at many | yes | 78 | Zero: :354-363. One: most tests. Two: :284. Short and symbol-only terms: :264-276 |

## HYPOTHESES
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| TH1 | scripts/test_check.py:320 shows `("﻿" + …` and the character between the quotes is not visible | It is a literal U+FEFF, so the test covers a BOM in the terms file | It is an empty string, so the test does not test a BOM (the explicit `"\ufeff"` at :325 covers it anyway) | `python3 -c "print(repr(open('scripts/test_check.py',encoding='utf-8').read().splitlines()[319]))"` |
| TH2 | scripts/test_check.py:371-380, :503-505 run `git commit` with the user's global config | A global `commit.gpgsign=true` or `core.hooksPath` makes setUp fail or run the user's hooks (a false red) | Clean CI configs never trigger it | Run StagedTest with `GIT_CONFIG_GLOBAL=/dev/null` vs default |

## HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| THB-1 | scripts/test_check.py:571-573 | `run_facts` tests the runner | It runs without `--root` and relies on `ROOT` computed from the *copied* script path (scripts/check_facts.py:31), which is correct but implicit. It also runs without `-I`, unlike the hook | — | 80 |

## ADVERSARIAL SCAFFOLD FINDINGS
- Reviewer blind spots: an assertion whose haystack contains the needle (T-F1); a "passes on the repo" test that also passes when the runner skips half the files (T-F2).
- Highest-risk: T-F3 (the hook is unguarded), T-F2, T-P1.
- Multi-step trace: the developer's env → inherited by run_check → overrides the terms file → tests of the file path test the env instead.
- Subtlety flag: `r.stdout + self.ref(...)` at :479.

### SUMMARY
- Domain: Tests
- Claims: 6 verified, 9 in FAIL (3 demonstrated defects, 6 preventive measures), 1 falsified (conditionally)
- Survived: 2/3 stress tests
- Failure categories: 4
- Invariants: same 11; the tests bite for I1–I8 and I11 (I2–I4 would be red today); nothing bites for I9 and I10
- Hypotheses: 2
- Hidden behaviors: 1
- Findings by type: 3 demonstrated defects, 6 preventive measures, 1 falsified hypothesis (1 conditionally)
- Critical issues: 0
- Recommendation: the suite is mostly honest and would already catch C-F1..C-F3 if it ran. It needs tests for the hook and for missing toolchains, and environment isolation.

---

# DOMAIN 3 — DOCUMENTATION

## VERIFICATION DOMAIN
Documentation: docstrings, usage text, comments and error messages in the four files.

## GROUND TRUTH
The code those texts describe (traced above).

## INVARIANTS
Same as Domain 1. A docstring that restates an invariant passes if it states it correctly. The docstrings state I2, I3, I4, I9 and I10 correctly; it is the code that breaks them, so those findings are in Code.

## DECOMPOSED CLAIMS
1. scripts/check.py:46-47 file selection is described correctly — Deductive
2. scripts/check.py:49-50 usage and the Python/Windows note — Deductive
3. scripts/check.py:13-15 the source of the terms is fully described — Deductive
4. scripts/check_facts.py:11-14 assertion rule is described correctly — Deductive
5. scripts/check_facts.py:16-18 usage lines — Deductive
6. scripts/pre-commit:3-4 install instructions — Deductive
7. scripts/test_check.py:3 run command — Deductive
8. Table error messages give the right header line — Deductive
9. scripts/test_check.py:336-339 the comment describes the test — Deductive

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Stale or incomplete text | 2 (D-F1, D-P1) | scripts/test_check.py, scripts/check.py |

## VERIFICATION RESULTS
### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| 1 | File selection | scripts/check.py:145-158 (git ls-files, else a walk without .git) and :386-394 (staged). Conf 88 |
| 2 | Usage | argparse flags at scripts/check.py:419-421 match :49. No syntax newer than 3.8 found. Conf 85 |
| 4 | Assertion rule | scripts/check_facts.py:34, :50 match :11-14 (it says "raise statement", which is what C-P5 exploits: documented, but weak). Conf 88 |
| 5 | Usage lines | `ids` positional (:78), `--root` (:79); test :604-607 shows ids before `--root`. Conf 85 |
| 6 | Install | From `.git/hooks/`, `../../scripts/pre-commit` resolves to `<repo>/scripts/pre-commit`. Conf 88 |
| 7 | Run command | `python3 -m unittest scripts/test_check.py` (path form, accepted by unittest in Python 3). Conf 80 |
| 8 | Error line numbers | scripts/check.py:373: the header at 0-based `i-1` is 1-based `i`; :378: `start == i` at the delimiter, so the header is 1-based `start`. Conf 90 |

### FALSIFIED HYPOTHESES
None.

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| D-F1 | scripts/test_check.py:337 | `# whole-word detection does not flag "<term>labs", but the evals check prints the key name` | Demonstrated defect (stale comment) | low | The test (:338-339) passes the plain term `T1`, which is **substring** by default (scripts/check.py:265), so detection does flag `<term>labs`. The comment describes the `=` case of the next test (:341-344) | Deductive | 90 | Change the comment to "substring detection flags it in the file; the evals check also prints the key name, which must be masked" |
| D-P1 | scripts/check.py:13-15 | `Terms come from CHECK_PRIVATE_TERMS (comma-separated) or the untracked file .check-private-terms (one per line, # for comments)` | Preventive measure | low | It does not say that the variable takes precedence even when empty (HB-1), or that `#` starts a comment only at the start of a line (DA-P3). A user who writes `acme  # client` gets a term that never matches | Deductive | 88 | State the precedence and "a `#` only at the start of a line" |

## STRESS TEST RESULTS
None: the stress techniques were applied in Domain 1 to the same behaviours. No separate run here, to avoid repeating a technique on the same claim.

## HYPOTHESES
None.

## HIDDEN BEHAVIORS DETECTED
None beyond Domain 1.

## ADVERSARIAL SCAFFOLD FINDINGS
- Reviewer blind spot: the docstrings are accurate *specifications*, which makes the code look right on a quick read (stated-versus-enforced drift).

### SUMMARY
- Domain: Documentation
- Claims: 7 verified, 2 in FAIL (1 demonstrated, 1 preventive), 0 falsified
- Survived: n/a
- Failure categories: 1
- Invariants: restated correctly in all docstrings (11/11 respected)
- Hypotheses: 0
- Hidden behaviors: 0
- Findings by type: 1 demonstrated defect, 1 preventive measure, 0 falsified
- Critical issues: 0
- Recommendation: fix the code, not the docstrings. The docstrings are the better source of truth here.

---

# DOMAIN 4 — DATA

## VERIFICATION DOMAIN
Data: the formats these scripts define and enforce: `evals.json`, `facts/NOT_COMPUTABLE`, the `prompt-sha256:` line of fact files, and `.check-private-terms`.

## GROUND TRUTH
skills/adversarial-verify/evals/facts/NOT_COMPUTABLE:1-12 (its own format comment), the fact files' first lines (for example skills/adversarial-verify/evals/facts/49.py:1), and evals.json (ids 20 and 21 at lines 265 and 278).

## INVARIANTS
I1, I5 and I8 (Domain 1).

## DECOMPOSED CLAIMS
1. evals.json's shape is fully enforced — Deductive
2. The hash binds each fact file to exactly its eval's prompt — Deductive
3. Every NOT_COMPUTABLE line refers to a real eval that needs it — Deductive
4. "States facts" is detected reliably — Deductive
5. The terms-file format handles a BOM and comment lines — Deductive
6. The terms-file format handles comments after a term — Deductive

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Constraint gap (asymmetric validation) | 2 (DA-P1, DA-P2) | scripts/check.py |
| Silent fallthrough | 1 (DA-P3) | scripts/check.py |

## VERIFICATION RESULTS
### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| 1 | evals.json shape | scripts/check.py:170-207: keys (180-184), int id (186), non-empty strings (191-193), assertions (194-202), duplicates and ordering (203-207). Eval 20 untagged and eval 21 tagged (evals.json:265, :278) match `TAGGED_FROM = 21`. Conf 90 |
| 2 | Hash binding | scripts/check.py:474-482: `sha256(str(prompt).encode("utf-8"))` compared with the first `prompt-sha256:` in the first 2000 characters. Each fact file is named by a single id. Conf 88 |
| 5 | BOM and comment lines | scripts/check.py:255 decodes through `decode` (utf-8-sig strips the BOM), then filters lines starting with `#`. Conf 88 |

### FALSIFIED HYPOTHESES
None.

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| DA-P1 | scripts/check.py:483-496 | `reasons[int(m.group(1))] = m.group(2)` | Preventive measure | low | A reason for an eval that does not exist, for one below 29, or for one whose prompt no longer has `(Facts` is accepted silently, while an orphan *fact file* is an error (:470-471). Turns into a defect when an eval is renumbered or its facts removed: the stale reason hides that the new eval at that id needs a fact file | Deductive | 88 | Report reasons whose id is not an existing eval ≥ FACTS_FROM that states facts |
| DA-P2 | scripts/check.py:500 | `if "(Facts" in str(e.get("prompt", ""))` | Preventive measure | low | `(facts:`, `( Facts`, or facts given without a parenthesis bypass the requirement. Turns into a defect at the first new eval written differently | Deductive | 85 | Use a case-insensitive regex `\(\s*facts\b`, and document the marker in scripts/check.py:34 |
| DA-P3 | scripts/check.py:255-256 | `if not l.strip().startswith("#")` | Preventive measure (silent fallthrough) | medium | `acme  # our client` becomes one term with the parts `acme`, `our`, `client`, joined by at most one character each (C-F2). It never matches the plain `acme`, so the user believes the name is protected and it is not. No warning is given | Deductive | 88 | Strip ` #…` after a term, or warn when a term contains `#` |

## STRESS TEST RESULTS
None: no stress techniques beyond Domain 1 (S2 and S4 covered the hash and id formats).

## HYPOTHESES
None.

## HIDDEN BEHAVIORS DETECTED
None beyond HB-1.

## ADVERSARIAL SCAFFOLD FINDINGS
- Subtlety flag: the asymmetry between fact files (validated both ways) and reasons (validated one way).

### SUMMARY
- Domain: Data
- Claims: 3 verified, 3 in FAIL (0 demonstrated, 3 preventive), 0 falsified
- Invariants: I1 and I8 respected and enforced; I5 see C-P1
- Hypotheses: 0
- Hidden behaviors: 0
- Findings by type: 0 demonstrated defects, 3 preventive measures, 0 falsified
- Recommendation: the formats are sound. Tighten the reasons file and the terms-file comment rule.

---

# DOMAIN 5 — UX (command-line and terminal output)

## VERIFICATION DOMAIN
UX: what a developer sees from `check.py`, `check_facts.py` and the hook. Target formats: a POSIX terminal, the Git for Windows `sh`, and CI logs. The input method is the keyboard. Checks from `references/ux.md`: states (error/success), sensitive data, real content.

## GROUND TRUTH
`references/ux.md` (the states and sensitive-data items), the platform notes in scripts/check.py:50 and scripts/pre-commit:4, and README.md:263.

## INVARIANTS
I4 (sensitive data) and I10.

## DECOMPOSED CLAIMS
1. Each error names a location first (`ERROR path[:line]: message`) — Deductive
2. A summary line ends every completed run — Deductive
3. Private terms never reach the screen (sensitive data) — Deductive
4. The hook shows the user every warning that affects the verdict — Deductive
5. The hook works out of the box on Windows — Abductive

## VERIFICATION RESULTS
### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| 1 | Location-first errors | scripts/check.py:105-109 and every call site use repo-relative paths, with `:line` for content hits (:321, :336, :373, :378, :518). Conf 88 |
| 2 | Summary line | scripts/check.py:523-527, printed after every completed run, with the counts and the scope (staged/working tree). Not printed on a crash (C-P7). Conf 85 |
| 3 | Masking for non-`=` terms | scripts/check.py:404-413 masks the location and the message separately, so the useful part stays visible. Conf 85 (the `=` case fails: C-F1, counted in Code) |

### FALSIFIED HYPOTHESES
None.

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| UX-F1 | scripts/pre-commit:15-17 | `out="$(…check_facts.py…)"; rc=$?` / `[ $rc -eq 0 ] \|\| { printf "%s\n" "$out"; exit 1; }` | Demonstrated defect (state not shown) | medium | On success the runner's output is discarded, including `skip 52.rs: toolchain not found` (C-F4). The developer sees a clean commit and no sign that two fact files never ran. The warning is not shown where it is seen | Deductive | 92 | Always print `out` (or at least the `skip`/summary lines), and fix C-F4 so a skip is a failure |
| UX-P1 | scripts/pre-commit:7-8 | `py=python3` / `command -v "$py" >/dev/null 2>&1 \|\| py=python` | Preventive measure | low | On Windows, `python3` can be the Microsoft Store alias: `command -v` finds it, it prints an install hint and exits non-zero, and every commit is blocked with a message that names no check. scripts/check.py:50 and README.md:263 say to use `py -3` on Windows, which the hook never tries | Abductive | 60 | Try `py -3` first when `uname` reports MINGW/MSYS, and probe with `"$py" -c 'import sys'` instead of `command -v` |

## STRESS TEST RESULTS
None: not applied in this domain (no claim here is independent of Domain 1).

## HYPOTHESES
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| UH1 | UX-P1 | The Store alias makes the hook fail on a stock Windows 11 with Git for Windows | Most developers have a real python3 on PATH first | Run the hook on a clean Windows 11 VM with only the py launcher installed |

## HIDDEN BEHAVIORS DETECTED
Covered by HB-2, HB-3 and UX-F1.

### SUMMARY
- Domain: UX
- Claims: 3 verified, 2 in FAIL (1 demonstrated, 1 preventive), 0 falsified
- Hypotheses: 1
- Findings by type: 1 demonstrated defect, 1 preventive measure
- Recommendation: make the hook show the facts runner's output.

---

## CROSS-DOMAIN SUMMARY
- Domains: Code, Tests, Documentation, Data, UX
- Claims: **31 verified** (12 + 6 + 7 + 3 + 3), **28 in FAIL** (10 demonstrated defects, 18 preventive measures), **5 falsified** (4 + 1, of which 1 conditionally)
- Survived: 6/7 stress tests passed (Code 4/4, Tests 2/3)
- Failure categories: missing completeness, silent fallthrough, assumed environment, test-environment artifact, tautological or weak tests, and stated-versus-enforced drift (the dominant pattern: 5 code defects where an accurate docstring or comment sits above code that does something else, and in 3 of them a test that would catch it already exists)
- Invariants: 11 found, 11 touched; 5 bite in the code (I1, I6, I7, I8, I11); 6 do not (I2, I3, I4, I5, I9, I10). For I2–I4 the unit tests would bite, but the hook never runs them (HB-3)
- Hypotheses: 6 (Code 3, Tests 2, UX 1)
- Hidden behaviors: 8 (7 Code, 1 Tests)
- Findings by type: **10 demonstrated defects** (C-F1..C-F5, T-F1..T-F3, D-F1, UX-F1), **18 preventive measures**, **5 falsified hypotheses (1 conditionally)**
- Critical issues: 0 demonstrated defects of critical severity; 0 critical preventive measures. **5 high**: C-F1, C-F2, C-F4, C-F5 (privacy and facts gates); C-F3 is medium
- Changes touching several domains: C-F4 + UX-F1 + T-F2 (the toolchain skip is in code, hidden by the hook, and unguarded by tests); C-F5 + T-F3 (the hook's `--strict`); C-P2 + T-P1 + D-P1 (precedence of the environment variable)
- Pre-code: not applicable
- Executed: 0 tests run (reasoning only)
- Proposed: 6 checks and 11 writes awaiting an answer
- Recommendation: **lower trust in the commit gate.** The private-names guard leaks `=` terms to output, misses names split by more than one character, and is not strict in the hook. The facts gate passes silently without toolchains. All five high-severity fixes are one line each (C-F1, C-F2, C-F3, C-F5) or three lines (C-F4). Running `scripts/test_check.py` before every commit (or in CI) would have caught three of them.

## PROPOSED EXECUTABLE CHECKS
| # | Claim | Confidence now | Check (command, test or query) | Confirms if | Refutes if | Cost and side effects | Status |
|---|-------|----------------|--------------------------------|-------------|------------|-----------------------|--------|
| P1 | C-F1, C-F2, C-F3 are live, and the suite's own tests catch them (Tests PASS 1-3) | 78 | `python3 -m unittest scripts/test_check.py -v` from the tree root | test_second_badge_mismatch, test_two_words_joined_any_way (two-space subtest) and test_whole_word_term_glued_in_output_is_still_masked fail, and nothing else does (on POSIX) | they pass | Runs the suite: about 80 subprocess runs of check.py, a temp copy of the repo per test, `git init/commit` in temp dirs, and rustc/node if present. Reads the tree, writes only under the system temp dir | proposed |
| P2 | C-F4: a missing toolchain passes | 79 | In a temp copy: `env PATH=<dir containing only python3> python3 scripts/check_facts.py; echo $?` | prints `skip 52.rs`, `skip 53.ts`, `… 0 failed`, exit 0 | exit non-zero | Runs 11 Python fact files; writes a temp dir only | proposed |
| P3 | C-F5 + UX-F1: the hook is not strict and hides skips | 79 | In a temp clone with no `.check-private-terms` and `CHECK_PRIVATE_TERMS` unset: stage a one-line change, `sh scripts/pre-commit; echo $?` | exit 0 with a "private names were NOT checked" WARNING | exit 1 | Runs check.py and possibly check_facts.py in a temp clone; no change to the user's repo | proposed |
| P4 | C-P1: a force-added terms file is committed silently | 79 | In a temp clone: `printf 'zz\n' > .check-private-terms; git add -f .check-private-terms; python3 scripts/check.py --strict --staged; echo $?` | exit 0, no mention of the file | an ERROR naming the file | Temp clone only | proposed |
| P5 | DA-P3 + C-F2: a trailing comment or a multi-character join defeats a term | 79 | In a temp copy: append `acme - corp` to SKILL.md; run `CHECK_PRIVATE_TERMS="acme corp" python3 scripts/check.py`, then use a terms file containing `acme  # client` with `acme` in SKILL.md | exit 0 in both | an ERROR | Temp copy only | proposed |
| P6 | Mutation probe of check.py and check_facts.py against test_check.py: do the tests protect every line in scope? | — | Hand mutations (3-5 on the riskiest lines: scripts/check.py:90, :223, :400, scripts/check_facts.py:92, :107) or `mutmut run` limited to `scripts/check.py` | survivors show untested lines | all killed | **Writes:** mutates a separate copy and restores it. About 5 mutants × the full suite (~80 subprocesses each). Suggestion: keep the copy on a memory-backed filesystem (tmpfs or a RAM disk), which needs your separate consent to create and enough free memory for the copy (under 2 MB here); the copy is removed at the end | proposed |

Proposed writes:
1. scripts/check.py:400: `pats = term_patterns(terms, substring=True)` (C-F1)
2. scripts/check.py:90: `SEP = r"[\W_]*"` (C-F2)
3. scripts/check.py:223: `for b in badges:` (C-F3)
4. scripts/check_facts.py:91-93: count a missing toolchain as a failure (C-F4)
5. scripts/pre-commit:9: add `--strict`; :15-17: always print the facts runner's output (C-F5, UX-F1)
6. scripts/check.py: error when `.check-private-terms` is tracked or staged; treat an empty `CHECK_PRIVATE_TERMS` as unset; catch `OSError` in check_version (C-P1, C-P2, C-P7)
7. scripts/test_check.py:479: replace the tautology with `assert_fails(r, "orphan.md", "never named in SKILL.md")` (T-F1)
8. scripts/test_check.py: new tests for a missing toolchain, the hook (`--strict`, facts), and a force-added terms file; `env.pop("CHECK_PRIVATE_TERMS")` in run_check; `assert_no_leak` in assert_passes (T-F2, T-F3, T-P1, T-P4)
9. scripts/test_check.py:337: correct the comment (D-F1)
10. scripts/check.py:13-15: document the precedence and the comment rule (D-P1)
11. Step 5: CHANGELOG.md `## Unreleased`: an entry for the fixes above. README.md:249-260 already states the intended behaviour, so no README change is needed once the code is fixed

**Which of P1–P6 may I run, and which of writes 1–11 may I make?** (Nothing runs and nothing is written until you answer. For P6, also say whether to use a memory-backed filesystem.)
