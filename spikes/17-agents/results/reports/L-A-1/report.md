# Adversarial verification report

**Cost estimate (large request: 4 domains, whole-file scope, cost accepted in the request, every choice settled):** 21 files in scope (5 Python scripts/tests and a shell hook, 2 docs, 2 JSON files, 13 eval-fact files, 1 reason list), 4 domains (Code, Tests, Data, Documentation), about 75 claims, **nothing run**.

## INTAKE

- **Target:** every domain Step 0 detects in the 21 files. Detected: **Code** (`scripts/check.py`, `scripts/check_facts.py`, `scripts/pre-commit`), **Tests** (`scripts/test_check.py`, the fact files `skills/adversarial-verify/evals/facts/*`, and the content of `evals.json` as the skill's eval suite), **Data** (`.claude-plugin/plugin.json`, the format of `evals.json` and `facts/NOT_COMPUTABLE`), **Documentation** (`README.md`, `CHANGELOG.md`). The UX domain was not detected: the terminal output of `check.py` is assessed for what it says, which is Documentation, and for what it leaks (Code), not for its layout.
- **Depth:** standard (stated in the request). **Scope:** the whole of the 21 files (stated: no diff, no history). **Execution mode:** reasoning only (stated). None of these were defaults.
- **Reference files of the skill:** none read. No file in scope proposes work not yet done or is a spike report (`references/pre-code.md`), UX is not in the target (`references/ux.md`), and no run was approved (`references/execution.md`).
- To change: say "deep", name a subset of files, or approve some of the checks listed under PROPOSED EXECUTABLE CHECKS. Consent lasts for this verification only.
- Files read outside the scope to establish ground truth: `skills/adversarial-verify/SKILL.md` (frontmatter, and `### Where the runs happen` at :321), `skills/adversarial-verify/references/execution.md` (grep only), `.gitignore`. As instructed, I read nothing outside `./tree` and `./skill`, so no external URL in the README (tool documentation, shields, the marketplace) was opened.

---

## VERIFICATION DOMAIN: Code

### GROUND TRUTH
- Each script's own contract: the `check.py` docstring (`scripts/check.py:2-50`) and the `check_facts.py` docstring (`scripts/check_facts.py:2-19`).
- `README.md:245-264` (Repository checks) and `CHANGELOG.md:3`, `CHANGELOG.md:24`, `CHANGELOG.md:45`.
- `scripts/test_check.py`, as the stated expectation of each check. Its results are *predicted by trace, not observed*, because nothing was run.
- The repository data the scripts read: `evals.json`, `facts/*`, `plugin.json`, `CHANGELOG.md`, `README.md`, `SKILL.md`.

### INVARIANTS
Where I looked: the file list of `./tree` (it has no `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, ADR or SPEC). I looked in the docstrings of `scripts/check.py:2-50` and `scripts/check_facts.py:2-19`, and in `README.md:245-264` ("enforces the repository's own invariants"), `CHANGELOG.md:3` and `.gitignore`. I found **8 invariants**, and the whole-file scope touches all of them.

| # | Invariant | Source | Touched by | Enforced by (file:line / test name) | Bites on changed path? |
|---|-----------|--------|------------|-------------------------------------|------------------------|
| I1 | The version is the same in SKILL.md frontmatter, every README skill badge, plugin.json, and the newest CHANGELOG entry | `CHANGELOG.md:3`, `README.md:250`, `scripts/check.py:10-12` | check.py, README, CHANGELOG, plugin.json | `scripts/check.py:212-241`; `test_check.py` VersionTest | **Partly.** Only the **first** badge is compared (`scripts/check.py:223`). The prose version at `README.md:125` is outside the check, and it is wrong (D-F1). |
| I2 | Every eval from 29 on that states facts has a fact file **or** a reason, not both | `scripts/check.py:34-38`, `README.md:255` | NOT_COMPUTABLE, facts/52.rs | `scripts/check.py:495-496`; `test_file_and_reason_both` | **Bites. It is violated in the tree today:** eval 52 has both (DA-F1). |
| I3 | No private term in any tracked file or name, or in any output line | `scripts/check.py:13-26`, `README.md:251` | check.py | `scripts/check.py:259-323`, `:397-414`; PrivateTest | **Partly.** There are two gaps: separators of more than one character (C-F3), and output masking of `=` terms (C-F2). |
| I4 | A missing toolchain is an error, never a silent skip | `scripts/check_facts.py:8`, `README.md:255` | check_facts.py, pre-commit | none found (I searched `scripts/check_facts.py` and `scripts/test_check.py:516-617`) | **No.** It is violated (C-F1, C-F4). |
| I5 | A fact file asserts something outside comments/strings and its last output line is `ok <id>` | `scripts/check_facts.py:11-14` | check_facts.py, facts/* | `scripts/check_facts.py:42-51`, `:105-111`; `test_runner_fails_on_a_file_that_asserts_nothing`, `test_runner_fails_without_the_ok_line`, `test_runner_ignores_assertions_in_comments` | **Bites.** One gap: a `panic!` inside the function under test counts as an assertion (C-F7). |
| I6 | Every `references/<name>.md` named exists, and every reference file is named in SKILL.md | `scripts/check.py:39-44`, `README.md:254` | check.py | `scripts/check.py:506-520`; ReferencesTest | **Bites** (`test_name_without_a_file`, `test_file_named_only_by_another_reference_file_is_still_unnamed`, `test_removed_reference_file`). |
| I7 | Every table row has as many cells as its header | `scripts/check.py:30-33`, `README.md:253` | check.py | `scripts/check.py:353-381`; TablesTest | **Bites.** One gap: fence matching (C-F8). |
| I8 | evals.json format: 4 keys, ids 1..n in order, tags from eval 21 | `scripts/check.py:6-9`, `README.md:249` | check.py, evals.json | `scripts/check.py:163-207`; EvalsTest | **Bites.** |

### DECOMPOSED CLAIMS
1. `check_evals` rejects bad JSON, extra or missing keys, non-integer or boolean ids, duplicates, gaps, wrong order, empty fields, and untagged assertions from 21 on. Mode: Deductive.
2. `check_version` compares the frontmatter version with **every** README skill badge (`scripts/check.py:10`). Mode: Deductive.
3. `check_version` takes the newest *numbered* CHANGELOG entry, so `## Unreleased` does not break it. Mode: Deductive.
4. Private-term matching ignores case and accents, and treats any separator as joining the parts (`scripts/check.py:15-17`). Mode: Deductive.
5. Output masking hides any line containing a term, substring-wise, including `=` terms (`scripts/check.py:399`). Mode: Deductive.
6. JSON escapes are decoded before matching. Mode: Deductive.
7. Non-UTF-8 files are scanned (UTF-16 with BOM, otherwise Latin-1). Mode: Deductive.
8. `--staged` checks exactly the index content, and cleans up its temp directory. Mode: Deductive.
9. The table check counts cells correctly, skipping code spans, escaped pipes, and fenced blocks. Mode: Deductive.
10. The facts check binds each fact file to its prompt's sha256, flags orphans, and flags file+reason. Mode: Deductive.
11. The reference-file check works in both directions. Mode: Deductive.
12. `check_facts.py` fails on a missing toolchain (`scripts/check_facts.py:8`). Mode: Deductive.
13. `check_facts.py` fails on a file with no assertion, or without the final `ok <id>`. Mode: Deductive.
14. `check_facts.py` runs Python facts in a way that lets `_parse_day` be imported without letting the environment interfere. Mode: Deductive.
15. The pre-commit hook runs check.py on the staged content, and runs the facts on the staged eval files when the evals change. Mode: Deductive.
16. The pre-commit hook never lets a skipped fact pass silently. Mode: Deductive, scaffolded from claims 12 and 15.

### FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Silent fallthrough | A missing toolchain prints `skip` and counts as a pass (`scripts/check_facts.py:91-93`). The hook then swallows that line (`scripts/pre-commit:15-17`). | check_facts.py, pre-commit |
| Missing completeness | `badges[:1]` checks only one badge (`scripts/check.py:223`). `mask` does not pass `substring=True` (`scripts/check.py:400`). Facts are bound to the prompt only, not to the assertions (`scripts/check.py:474-482`, see T-F4). | check.py |
| Assumed environment | `SEP` assumes at most one separator character, so `\r\n` and double spaces are missed (`scripts/check.py:90`). | check.py |
| Stale state | The `currently 4.1` prose (`README.md:125`). The reason for 52 is kept after 52.rs was added (`skills/adversarial-verify/evals/facts/NOT_COMPUTABLE:13`). | README.md, NOT_COMPUTABLE |

### VERIFICATION RESULTS

#### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| 1 | check_evals rejects every listed defect | Traced in `scripts/check.py:163-207`. A boolean id is rejected by `type(i) is not int` at :186. Duplicates and gaps are reported independently at :203-207. Exercised by EvalsTest (`scripts/test_check.py:104-163`). Score 88. |
| 3 | `## Unreleased` does not break the version check | The regex at `scripts/check.py:237` requires a digit after `## `, so `CHANGELOG.md:5` is skipped and `CHANGELOG.md:10` (`## 4.2`) is taken. That equals `SKILL.md:20` (`"4.2"`) and `.claude-plugin/plugin.json:3`. Score 88. |
| 6 | JSON escapes decoded | `scripts/check.py:313-317` and `:322-323`. Covered by `test_json_escaped_key` and `test_json_escape`. Score 85. |
| 7 | Non-UTF-8 scanned | `decode` at `scripts/check.py:112-122`. Covered by `test_latin1_file` and `test_utf16_file`. Score 85. |
| 8 | `--staged` = index content, with temp cleanup | `checkout-index -a` into the temp dir (`scripts/check.py:386-394`), with `root = tmp` (:433) and `rmtree` in `finally` (:438-440). Covered by `test_staged_leak_with_clean_working_tree` and `test_staged_outside_git_is_a_clear_error`. Score 85. |
| 9 | Table cell counting | `count_cells` replaces code spans and `\|` before counting (`scripts/check.py:344-350`). `DELIM` accepts rows with or without outer pipes (:341). Score 82. |
| 10 | Facts binding, orphans, file+reason | `scripts/check.py:457-501`. The hash is taken over `prompt.encode("utf-8")` and must sit in the first 2000 chars (:476-482). Score 85. |
| 11 | Reference files in both directions | `scripts/check.py:506-520`. `named_in_skill` only grows from SKILL.md (:515-516). Score 88. |
| 13 | No assertion, or no `ok <id>` line, fails | Python: AST `Assert`/`Raise` (`scripts/check_facts.py:45-50`). Rust and TS: regex after stripping comments and strings (:51). Last-line check at :106-108. Score 85. |
| 14 | Python facts run with `-E -s` and `cwd=FACTS` | `scripts/check_facts.py:57`, `:100`. `-I` would also stop the script's directory from being prepended (Python ≥3.11), which would break `from _parse_day import …` (`facts/35.py:3`). `-E -s` keeps that import working and still blocks PYTHON* variables and user site-packages. Score 82. |
| 15 | The hook checks the staged content, and runs facts on the staged files | `scripts/pre-commit:9` (`--staged`). `scripts/pre-commit:12-15` checks out the index to `$tmp` and passes `--root "$tmp"`. Score 82. |

#### FALSIFIED HYPOTHESES
| # | Location | Suspected defect | Check (quote) | Status (falsified / conditionally) | Could it have failed? (how shown, or the check that would complete it) | Paths not covered | Mode | Confidence |
|---|----------|------------------|-------|------------------------------------|------------------------------------------------------------------------|-------------------|------|------------|
| FH1 | `scripts/check.py:237` | The `## Unreleased` heading added at `CHANGELOG.md:5` makes the version check fail or read "Unreleased" | `re.search(r"^## +([0-9][0-9.]*)\b", …)` | conditionally | Traced only. It is completed by "`python3 scripts/check.py` prints no CHANGELOG error" (P3). | A CHANGELOG whose first numbered heading is an older version placed above the current one (`test_changelog_older_entry_does_not_count` covers that). | Deductive | 75 |
| FH2 | `scripts/check_facts.py:57`, `:100` | The facts directory as cwd lets a fact file shadow a stdlib module | `[sys.executable, "-E", "-s", path]`, `cwd=FACTS` | falsified for the current files | Shown by listing the directory: it holds only `35…57` and `_parse_day.py`, and no name collides with a stdlib module imported by these files. | A future fact file named like a stdlib module (e.g. `json.py`). Only digit stems are allowed (`scripts/check.py:470`), which makes this unlikely. | Deductive | 80 |

#### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| C-F1 | `scripts/check_facts.py:91-93` | `if steps is None: print(f"skip {name}: toolchain not found"); continue` | Demonstrated defect | medium | On a machine without `rustc`, `52.rs` is skipped, `failed` stays 0, and the script returns 0 (`scripts/check_facts.py:113`), so the run "passes". This contradicts its own docstring "A missing toolchain is an error, never a silent skip" (`scripts/check_facts.py:8`) and `README.md:255` ("fails … if a needed toolchain … is missing"). If every file is skipped, it still exits 0 because `files` is non-empty. | Deductive | 92 | Replace the `skip` with `print(f"FAIL {name}: toolchain not found"); failed += 1`. If skipping is wanted, add an explicit `--allow-missing-toolchain` flag and document it. |
| C-F2 | `scripts/check.py:399-400` | `# substring patterns: …` / `pats = term_patterns(terms)` | Demonstrated defect | high | `term_patterns` defaults to `substring=False` (`scripts/check.py:259`), so a term written `=zqvorblax` is masked only as a whole word. With that term, an eval key `zqvorblaxlabs` is not detected by `check_private`, because whole-word matching fails. `check_evals` prints it in the clear: `unexpected keys ['zqvorblaxlabs']` (`scripts/check.py:182`). `mask` misses it, so the private name reaches stdout or CI logs. `test_whole_word_term_glued_in_output_is_still_masked` (`scripts/test_check.py:341-344`) expects "message hidden", so by trace it is red. | Deductive | 90 | `pats = term_patterns(terms, substring=True)`. |
| C-F3 | `scripts/check.py:90` | `SEP = r"[\W_]?"  # anything that is not a letter or digit, possibly nothing` | Demonstrated defect | high | The separator matches at most one character. The docstring (`scripts/check.py:16-17`) and `README.md:251` promise any join (space, hyphen, underscore, line break). Missed: `QUILLANE  dorvex` (two spaces), the very subtest at `scripts/test_check.py:286`, which by trace is red. Also missed is a term split across a CRLF line break (`\r\n` is two characters), which a Windows checkout with `core.autocrlf` produces. `README.md:264` explicitly supports Windows. A private name passes the check. | Deductive | 88 | `SEP = r"[\W_]*"`. If unbounded runs are a concern, use `r"[\W_]{0,3}"`. Add a CRLF subtest. |
| C-F4 | `scripts/pre-commit:15-17` | `out="$("$py" -I …check_facts.py --root "$tmp")"; rc=$?` … `[ $rc -eq 0 ] \|\| { printf "%s\n" "$out"; exit 1; }` | Demonstrated defect | medium | The trace chains C-F1 into this hook. The hook captures stdout and prints it only on failure. With `rustc` missing, check_facts exits 0 (C-F1), so the `skip 52.rs` line is discarded and the commit passes with **no** output. The skip that the script at least prints becomes fully silent in the place it is used most. | Deductive | 88 | Fix C-F1. Independently, print `$out` whenever it contains a line starting `skip`. |
| C-F5 | `scripts/check.py:222-225` | `for b in badges[:1]:` | Demonstrated defect | medium | `README.md:250` and the docstring `scripts/check.py:10` say "every skill badge". Only the first is compared. A second stale badge (`badge/skill-v2.0`) passes. `test_second_badge_mismatch` (`scripts/test_check.py:171-173`) expects "version mismatch", so by trace it is red. | Deductive | 92 | `for b in badges:`. |
| C-F6 | `scripts/pre-commit:9`, `:12`, `:15` | `"$root/scripts/check.py"`; `grep -q '^skills/adversarial-verify/evals/'` | Preventive measure | low | The hook runs the **working-tree** versions of `check.py` and `check_facts.py`, not the staged ones, and it re-runs the facts only when the evals change. Likelihood: low but real. A commit that changes only `scripts/check_facts.py` (for example, breaking the runner) never runs the facts. A commit with a fixed `check.py` staged but a broken working copy is checked with the broken copy. | Deductive | 75 | Run the scripts from `$tmp/scripts/` after `checkout-index`. Extend the grep to `^scripts/check_facts.py`. |
| C-F7 | `scripts/check_facts.py:34` | `".rs": re.compile(r"\b(assert\|assert_eq\|assert_ne\|panic)!")` | Preventive measure | low | `facts/52.rs:9` has `panic!("bad month")` inside the function under test. If every `assert…!` in `main` (`facts/52.rs:14-17`) were removed, `has_assertion` would still pass, the file would print `ok 52`, and it would verify nothing. Not happening today. | Deductive | 85 | Count only assertions inside `fn main`, or require at least one `assert*!` and drop `panic!`. |
| C-F8 | `scripts/check.py:361-368` | `if fence is None: fence = f.group(1)[0] else: fence = None` | Preventive measure | low | Any fence closes any open fence, whatever its character or length. A `~~~` line inside a ```` ``` ```` block ends the block early, and a later broken table inside it is then counted, or the reverse. Likelihood: low in these docs. | Deductive | 80 | Close only on a fence of the same character and at least the same length. |
| C-F9 | `scripts/check.py:467-473` | `with_file[int(stem)] = name` | Preventive measure | low | `40.py` and `40.ts` would both exist. The later name overwrites the earlier, so only one hash is checked, while `check_facts.py` runs both. A stale second file escapes the prompt-binding check. | Deductive | 80 | Error when a stem appears with two extensions. |

### STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|
| S1 | Scale Shift (zero, 10x) | `check_evals` id checks (PASS 1) | yes | 82 | Zero evals gives `no 'evals' list` (`scripts/check.py:171-173`). 570 evals: `ids.count` is O(n²), about 3×10⁵ operations, which is harmless. |
| S2 | Time Travel | prompt-sha256 binding (PASS 10) | **no** | 85 | Six months on, a maintainer edits an eval's **assertion** numbers. The hash covers only the prompt (`scripts/check.py:474-478`), so nothing fails. That is exactly how `evals.json:705` came to say 11 where the facts say 12 (T-F1). Reported as T-F4. |
| S3 | Requirement Inversion | reference-file check (PASS 11) | yes | 85 | Inverted: "a file named only by another reference file is enough". The code refuses it (`scripts/check.py:515-520`) and a test pins that (`scripts/test_check.py:481-485`). The current requirement is the one implemented. |
| S4 | Existence Question | `-E -s` instead of `-I` (PASS 14) | yes | 80 | Delete it mentally and use `-I`. On Python ≥3.11, `-I` stops prepending the script's directory, so `from _parse_day import` fails for 35, 37 and 39. The choice has a reason. |

### HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| HB1 | `scripts/check_facts.py:91-93` | "never a silent skip" (:8) | prints `skip` and exits 0 | Demonstrated defect (C-F1) | 92 |
| HB2 | `scripts/pre-commit:15-17` | runs the facts | discards all output on rc 0, so a skip is invisible | Demonstrated defect (C-F4) | 88 |
| HB3 | `scripts/check.py:223` | every badge | first badge only | Demonstrated defect (C-F5) | 92 |
| HB4 | `scripts/check.py:400` | substring masking | whole-word masking for `=` terms | Demonstrated defect (C-F2) | 90 |
| HB5 | `scripts/check.py:90` | any separator | at most one separator character | Demonstrated defect (C-F3) | 88 |
| HB6 | `scripts/check.py:483-494` | reasons are for evals that state facts | a reason for a non-existent eval, or for an eval without facts, is never flagged | Preventive measure (low; not tabled separately) | 80 |

---

## VERIFICATION DOMAIN: Tests

### GROUND TRUTH
- Production code: `scripts/check.py` and `scripts/check_facts.py`.
- The eval prompts in `evals.json`, which the fact files must reproduce.
- My own recomputation of each stated fact (arithmetic, WCAG luminance, calendar days, mutant kill tables).

Test-environment notes:
- `test_check.py` copies the repo into a `mkdtemp` dir that is **not** a git repo, so `list_files` takes the `os.walk` fallback (`scripts/check.py:153-158`) where production takes `git ls-files`.
- The fact runner without `--root` uses the copy's own `ROOT`.

### INVARIANTS
Same as I2, I4 and I5 in the Code domain. The test-side gap: **no test** exercises the missing-toolchain path of I4. I looked through `scripts/test_check.py:516-617` (FactsTest) and found none.

### DECOMPOSED CLAIMS
1. `test_check.py` fails when each invariant is broken, and passes on the repo. Mode: Deductive.
2. Each assertion in `test_check.py` can fail. Mode: Deductive.
3. The tests give the same result on the supported platforms (README: Windows supported). Mode: Deductive/Abductive.
4. `facts/35.py` and `facts/37.py`: `parse_day('2026-02-31')` returns `(2026, 2, 31)`. Mode: Deductive.
5. `facts/38.py`: new discount is always 2 decimals for k/100, k ≤ 10000; old one first fails at k=1; `round(10.05*0.9,2)==9.05`. Mode: Deductive.
6. `facts/39.py`: 31 April rejected by both versions; 29 Feb 2024 separates them; 2026 and 2100 rejected. Mode: Deductive.
7. `facts/40.py`: tests kill `<`, `<=`, `return True`; boundary tests kill the rest. Mode: Deductive.
8. `facts/42.py`: the three named mutants pass both tests. Mode: Deductive.
9. `facts/48.py`: contrast ratios. Mode: Deductive.
10. `facts/49.py`: usable widths and clipped labels. Mode: Deductive.
11. `facts/51.py`: 44 → 24 px. Mode: Deductive.
12. `facts/52.rs`: `days_in_month(2024,2)==28`. Mode: Deductive.
13. `facts/53.ts`: survivors are `day === 0 → false` and `0 → 1`; Sunday kills both. Mode: Deductive.
14. `facts/56.py`: 104+5+8+3=120; 108 measured; 12 excluded; 96%. Mode: Deductive.
15. `facts/57.py`: 239+9+12=260; 1 discarded; 2 unaccounted. Mode: Deductive.
16. The expected outputs and assertions of evals 29–57 agree with their facts. Mode: Deductive.
17. Every fact file's prompt-sha256 matches its eval's current prompt. Mode: Abductive (it cannot be computed by reasoning).

### FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Tautological test | `self.assertIn("orphan.md", r.stdout + self.ref("orphan.md"))` (`scripts/test_check.py:479`) | test_check.py |
| Missing negative tests | No test for a missing toolchain. No test binding assertion text to the facts. | test_check.py, check.py |
| Test-environment artifact | `os.symlink` needs a privilege on Windows (`scripts/test_check.py:351`). On machines without `rustc`/`node`, `test_runner_passes_on_the_repo` passes because of the silent skip (`scripts/test_check.py:575-578`, C-F1). | test_check.py |
| Test-code drift | A comment states a premise that is no longer true (`scripts/test_check.py:337`). | test_check.py |
| Missing completeness | An eval's expected text contradicts its own facts (`evals.json:612`, `:705`). | evals.json |

### VERIFICATION RESULTS

#### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| 4 | 35/37: 31 Feb accepted | `facts/_parse_day.py:5-12` is identical to the prompts `evals.json:440`, `:463`. The day check is `1..31` only. Score 92. |
| 6 | 39: separation by 29 Feb 2024 | `facts/_parse_day.py:15-35`. Parent: `DAYS[1]=28` rejects 29. Fixed: `leap(2024)` is true. `leap(2100)`: 2100%100==0 and 2100%400≠0, so false, rejected. Score 92. |
| 7 | 40: kill table | Tests (30,T),(5,F). `<`: 30→F, killed. `<=`: 30→F, killed. `True`: 5→T, killed. `>`, `>=19`, `>=17` survive. Boundary (18,T),(17,F) kills `>` (18→F), `>=19` (18→F) and `>=17` (17→T). Matches `evals.json:499`. 3/6 = 50% matches `evals.json:500`. Score 92. |
| 8 | 42: three surviving changes | `100*0.9` is 90.0 in binary64 (the error 2.2×10⁻¹⁵ is under half an ulp at 90, which is 7.1×10⁻¹⁵). `round(90.0,0)==90`. `''` is falsy, so it returns `t`. Score 85. |
| 9 | 48: contrast ratios | Recomputed by hand with the WCAG formula: #333/#fff 12.635, so 12.63. #6b6b6b/#fff 5.33. #2563eb/#fff 5.17. #d0d0d0/#1e1e1e 10.81. #6b6b6b/#1e1e1e 3.13. #2563eb/#1e1e1e 3.23. #3a3a3a/#1e1e1e 1.47. #8a8a8a/#1e1e1e 4.83. All match `facts/48.py:17-21` and the "about" values at `evals.json:599-605`. Hand arithmetic at 2-decimal boundaries is fragile, so the run P2 would confirm. Score 78. |
| 10 | 49: widths | 375/4−16 = 77.75, 320/4−16 = 64.0, 430/4−16 = 91.5. Clipped sets {Bestellungen 79, Einstellungen 82} at 375 and at 320, empty at 430. Matches `facts/49.py:12-14`. Score 92. |
| 11 | 51: heights | 20+24 = 44, 16+8 = 24 (`facts/51.py:3-6`), matching `evals.json:637`. Score 95. |
| 12 | 52: Rust | `facts/52.rs:3-11` is identical to `evals.json:648`. `2 => 28` ignores the year. Score 90. |
| 13 | 53: TS survivors | 1 Jan 2026 is a Thursday. 24 Oct is day 297, 296 days on, 296 mod 7 = 2, so Saturday. 21 Oct is Wednesday (3) and 25 Oct is Sunday (0). Mutant results on (6,T),(3,F): `false‖day===6` survives, `day===0‖false` is killed, `&&` is killed, `day===1‖day===6` survives. The sorted order `"0 -> 1"` < `"day…"` holds. On Sunday both survivors give false≠true. Score 90. |
| 14 | 56 arithmetic | 104+5+8+3 = 120. One survivor ran 0 tests (log line 1630). Measured = 104+4 = 108. Excluded = 8+3+1 = 12. 100·104/108 = 96.3, so 96 (`facts/56.py:3-14`). Score 95. |
| 15 | 57 arithmetic | 239+9+12 = 260. 8−7 = 1. 9−7 = 2 (`facts/57.py:3-8`). Score 95. |
| 1a | Most invariants have a test that bites | EvalsTest, VersionTest (except the second badge), ReferencesTest, TablesTest, and FactsTest (`test_runner_fails_on_a_false_fact` edits `facts/38.py:21` exactly; `test_prompt_changed_after_its_facts` replaces `day > 31`, present in `evals.json:463`; `d["evals"][36]` is id 37). Score 85. |

#### FALSIFIED HYPOTHESES
| # | Location | Suspected defect | Check (quote) | Status (falsified / conditionally) | Could it have failed? (how shown, or the check that would complete it) | Paths not covered | Mode | Confidence |
|---|----------|------------------|-------|------------------------------------|------------------------------------------------------------------------|-------------------|------|------------|
| FH3 | `scripts/test_check.py:550` | The prompt edit is a no-op, so the test passes for the wrong reason | `.replace("day > 31", "day > 28")` on `d["evals"][36]` | falsified | Shown: `evals.json:462-463` (index 36 is id 37) contains `day > 31`, so the replacement changes the prompt and the hash must differ. | Other fact files' hashes (see H1). | Deductive | 85 |
| FH4 | `skills/adversarial-verify/evals/facts/38.py:21` | The "real value" 9.05 is itself wrong | `assert round(10.05 * 0.9, 2) == 9.05` | conditionally | By hand: the exact product of the two doubles is 9.045 + 8.6×10⁻¹⁶, which rounds to the double above 9.045 (≈9.0450000000000017), so it rounds to 9.05. Completed by running `facts/38.py` (P2). | The loop at `facts/38.py:17` (10,001 values), not traced by hand. | Deductive | 75 |

#### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| T-F1 | `skills/adversarial-verify/evals/evals.json:705` | `"…says that 11 are excluded: 8 timed out, 3 skipped, 1 not measured"` | Demonstrated defect | medium | 8+3+1 = 12, and the assertion's own list sums to 12. The eval's expected output says "with 12 excluded" (`evals.json:699`), and the fact file asserts `excluded == 12` (`facts/56.py:11-12`). A grader holding the assertion literally marks a correct answer ("12 excluded") as wrong, or passes a wrong "11". | Deductive | 95 | Change to "says that 12 are excluded: 8 timed out, 3 skipped, 1 not measured". |
| T-F2 | `skills/adversarial-verify/evals/evals.json:612` | `"…and that at 320 px (80 px buttons, 64 px usable) more labels are clipped"` | Demonstrated defect | low | At 320 px the same two labels are clipped as at 375 px: 61 and 50 both fit in 64 (`facts/49.py:13`). The eval's own assertion says so (`evals.json:615`). The expected output claims "more labels". | Deductive | 92 | "…the same two labels are clipped by more (15 and 18 px), and Startseite has 3 px to spare". |
| T-F3 | `scripts/test_check.py:479` | `self.assertIn("orphan.md", r.stdout + self.ref("orphan.md"))` | Demonstrated defect | low | `self.ref("orphan.md")` itself contains `orphan.md`, so the assertion is always true. The test never checks that an unnamed reference file fails. Delete `scripts/check.py:519-520` and this test still passes. | Deductive | 95 | `self.assert_fails(r, "orphan.md", "never named in SKILL.md")`. |
| T-F4 | `scripts/check.py:474-482` | `want = hashlib.sha256(prompts[i].encode("utf-8")).hexdigest()` | Preventive measure | medium | The facts are bound only to the prompt. Numbers in `expected_output` and `assertions` can drift from the fact file without failing, and T-F1 and T-F2 are such drifts. Stress test S2 did not survive. | Deductive | 85 | Hash prompt + expected_output + assertions. Or let fact files assert the numbers quoted in the assertions (e.g. a test that each "N are excluded" equals the computed value). |
| T-F5 | `scripts/test_check.py:516-617` | (absence) no test of `check_facts.py` with a missing toolchain | Preventive measure | medium | I searched FactsTest. No test hides `rustc` or `node` (e.g. `PATH` without them), so C-F1 went unnoticed. Worse, on a machine without `rustc` `test_runner_passes_on_the_repo` (`:575-578`) passes because of the skip: a test-environment artifact that hides the defect. | Deductive | 85 | Add a test that runs `check_facts.py 52` with `PATH` emptied of `rustc` and expects a non-zero exit. |
| T-F6 | `scripts/test_check.py:350-352` | `os.symlink(os.path.join(self.tmp, "does-not-exist"), self.path("dangling.md"))` | Preventive measure | low | On Windows (supported, `README.md:264`), `os.symlink` needs Developer Mode or admin rights and otherwise raises `OSError`. The test errors (a false red) for a reason unrelated to `check.py`. | Deductive | 70 | Skip when `os.symlink` is unavailable, or make the file unreadable another way (`chmod 0` on POSIX). |
| T-F7 | `scripts/test_check.py:336-339` | `# whole-word detection does not flag "<term>labs", …` with `terms=T1` | Preventive measure | low | The comment is stale: with a plain term, detection is substring by default (`scripts/check.py:265`), so `<term>labs` **is** detected and the test does not exercise "masked even if not detected". The real case is the next test (`:341-344`), which is red by C-F2. A future reader trusting this test believes the gap is covered. | Deductive | 85 | Delete this test, or rename it and fix its comment. Keep `:341-344` as the guard. |

### STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|
| S5 | Scale Shift (10x range) | `facts/49.py` widths | yes | 85 | At 4× more labels or narrower screens, `clipped()` scales linearly with no hidden constant other than `padding`. 430 px is covered. |
| S6 | Requirement Inversion | `facts/40.py` boundary claim | yes | 85 | Inverted: "the boundary tests kill **none** of the survivors". `facts/40.py:12` would fail, so the assertion genuinely discriminates. |
| S7 | Existence Question | `facts/_parse_day.py` | yes | 82 | Without it, 35, 37 and 39 would duplicate the functions. It is excluded from the eval mapping by the `_` prefix (`scripts/check.py:469`, `scripts/check_facts.py:83`). It should exist. |
| S8 | Time Travel | `facts/52.rs:14` comment-justified assertion | yes | 80 | `assert_eq!(…, 28)` plus `assert_ne!(…, 29)` state the fact directly, so a maintainer cannot misread it. |

### HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| HB7 | `scripts/test_check.py:479` | tests that an unnamed reference file is reported | asserts nothing that can fail | Demonstrated defect (T-F3) | 95 |
| HB8 | `scripts/test_check.py:37-40` vs `scripts/check.py:145-152` | the copy is checked like the repo | the copy is not a git repo, so the `os.walk` fallback runs, not `git ls-files` (a different path into the code). StagedTest covers the git path. | none (noted) | 80 |

---

## VERIFICATION DOMAIN: Data

### GROUND TRUTH
- The consumers of each format: `scripts/check.py:163-207` (evals.json), `:212-241` (plugin.json), `:483-501` (NOT_COMPUTABLE).
- The docstring `scripts/check.py:34-38`, and `README.md:249`, `README.md:255`.

### INVARIANTS
I2 (file **or** reason, not both) and I8 (evals format). See the Code domain table.

### DECOMPOSED CLAIMS
1. plugin.json is valid JSON with a string `version` equal to the skill's. Mode: Deductive.
2. evals.json has ids 1..57 in order, with four keys each. Mode: Deductive (ids) / Inductive (keys, sampled).
3. Every eval from 29 with `(Facts` has exactly one of a fact file or a reason. Mode: Deductive.
4. Every NOT_COMPUTABLE line is in `<id>: <reason>` form for an eval that states facts. Mode: Deductive.

### FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Stale state | A reason kept after its fact file was added (`skills/adversarial-verify/evals/facts/NOT_COMPUTABLE:13` and `facts/52.rs`) | NOT_COMPUTABLE |

### VERIFICATION RESULTS

#### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| 1 | plugin.json version | `.claude-plugin/plugin.json:3` `"4.2"`, a string, equal to `skills/adversarial-verify/SKILL.md:20`. The repository URL equals `README.md:95`. The license is MIT, matching `README.md:309`. Score 92. |
| 2 | evals ids | The `"id":` lines are 1..57 in file order (from a grep of `evals.json`). Keys sampled in evals 29–57 (`evals.json:368-723`): exactly id, prompt, expected_output, assertions. Score 85 (ids) / Pattern 75 (keys, sampled). |
| 3a | Facts coverage, except 52 | Evals from 29 whose prompt contains `(Facts`: 30, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 43, 45, 48 (`Facts,`), 49 (`Facts,`), 50, 51, 52, 53, 56, 57. Each has a file (35, 37, 38, 39, 40, 48, 49, 51, 53, 56, 57) or a reason (30, 32, 33, 34, 36, 41, 43, 45, 50). 42 has a file with no `(Facts`, which is allowed. Score 85. |

#### FALSIFIED HYPOTHESES
None.

#### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| DA-F1 | `skills/adversarial-verify/evals/facts/NOT_COMPUTABLE:13` | `52: the compiler is not installed on every machine` | Demonstrated defect | high | `facts/52.rs` exists, so `with_file[52]` is set (`scripts/check.py:473`) and `reasons[52]` is set (`:494`). `:495-496` then reports `eval 52 has a fact file and a reason not to have one`. Traced consequences: `check.py` exits 1 on the tree as it is. The pre-commit hook (`scripts/pre-commit:9`) blocks **every** commit. Every `assert_passes` test of `test_check.py` (e.g. `test_repo_passes`, `test_repo_passes_strict`, `test_old_untagged_eval_is_accepted`, NeutralTest, `test_short_term_warns`) is red. The reason also contradicts `README.md:247`, which makes `rustc` a requirement. (The test outcomes are predicted by trace, not run: P1.) | Deductive | 88 | Delete line 13 of NOT_COMPUTABLE, and fix C-F1 so that a missing `rustc` is reported rather than excused. |
| DA-F2 | `scripts/check.py:483-494` | `reasons[int(m.group(1))] = m.group(2)` | Preventive measure | low | A reason for an id that does not exist, or that states no facts, is accepted silently (HB6), so stale reasons accumulate. DA-F1 is the same staleness that happened to be caught. | Deductive | 80 | Error on a reason whose eval does not exist or has no `(Facts`. |

### STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|
| S9 | Requirement Inversion | plugin.json `version` type | yes | 85 | Inverted: a numeric `4.2`. Rejected by `isinstance(pv, str)` (`scripts/check.py:233`), and pinned by `test_plugin_version_not_a_string`. |
| S10 | Scale Shift (zero) | NOT_COMPUTABLE missing entirely | yes | 80 | `os.path.isfile(nc)` is false, so `reasons = {}` and each eval with facts and no file errors (`scripts/check.py:485`, `:500-501`). It fails loudly, not silently. |
| S11 | Time Travel | evals.json key set | yes | 80 | A maintainer adding a `context` key is stopped with "put facts in the prompt" (`scripts/check.py:182`, `test_extra_key`). |

### HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| HB6 | `scripts/check.py:483-494` | reasons justify a missing fact file | orphan reasons accepted | Preventive measure (DA-F2) | 80 |

---

## VERIFICATION DOMAIN: Documentation

### GROUND TRUTH
- The actual scripts and data, as above.
- `skills/adversarial-verify/SKILL.md` (version, reference-file table, `### Where the runs happen` at :321).
- `references/execution.md`, grep only: it has *Where the runs happen* at :33 and the separate copy at :27 and :39.
- The external documentation cited by `README.md:226-241` was **not** read (the instructions forbid reading outside `./tree`).

### INVARIANTS
I1 (version agreement) is restated by both docs, `CHANGELOG.md:3` and `README.md:250`. I9 is a doc-only rule, `README.md:117`: "Copy the whole folder: `SKILL.md` alone would send the verifier to files that are not there". The README's own instructions contradict it (DO-F2).

### DECOMPOSED CLAIMS
1. The README's statements of the version match 4.2. Mode: Deductive.
2. The install instructions produce a working skill (with `references/`). Mode: Deductive.
3. `README.md:245-264` describes what `check.py` and `check_facts.py` do. Mode: Deductive.
4. The README's method summary matches SKILL.md (failure categories, stress rules, confidence bands). Mode: Deductive.
5. CHANGELOG 4.2 and Unreleased describe files that exist (references/*, evals 54–57). Mode: Deductive.
6. CHANGELOG:3 describes the version rule as `check.py` implements it. Mode: Deductive.
7. CHANGELOG:14 sizes (57.3 kB, 46.4 kB, 62.5 kB). Mode: Abductive (they need a measurement).
8. The mutation-tool table reflects the tools' official documentation. Mode: not verifiable within the allowed sources.

### FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Stale state / version mismatch | `README.md:125` | README.md |
| Broken instructions | `README.md:87-90` vs `README.md:117` | README.md |
| API drift (doc promises the code does not keep) | `README.md:250` (C-F5), `README.md:251` (C-F3), `README.md:255` (C-F1) | README.md (counted in Code, their primary domain) |

### VERIFICATION RESULTS

#### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| 1a | Badge version | `README.md:1` `skill-v4.2` equals `SKILL.md:20`. Score 92. |
| 3a | Checks list (evals, tables, references) | `README.md:249`, `:253`, `:254` match `scripts/check.py:163-207`, `:353-381`, `:506-520`. Score 85. |
| 3b | Python 3.8+ suffices | The scripts use f-strings, `capture_output` and `text=` (3.7) and no walrus or `match` (`scripts/check.py`, `scripts/check_facts.py`, read in full). Score 80. |
| 3c | Hook install | `README.md:261` `ln -s ../../scripts/pre-commit .git/hooks/pre-commit` resolves from `.git/hooks/`. This matches `scripts/pre-commit:3`. Score 85. |
| 4 | Method summary | Failure categories (`README.md:63`) are the seven of `SKILL.md`. Stress rules (`README.md:72`) and confidence bands (`README.md:78`) match the SKILL.md I read (`skill/SKILL.md:290`, `:333-343`). Score 85. |
| 5 | Changelog targets exist | `references/pre-code.md`, `ux.md` and `execution.md` exist. Evals 54–57 exist (`evals.json:671-723`). *Where the runs happen* exists (`SKILL.md:321`, `references/execution.md:33`). Score 88. |
| 6a | The version rule is enforced, apart from wording (see DO-F3) | `scripts/check.py:237-241`. Score 85. |

#### FALSIFIED HYPOTHESES
None.

#### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| DO-F1 | `README.md:125` | `The plugin declares its version in .claude-plugin/plugin.json (currently 4.1), the same number as the skill's frontmatter and the badge above.` | Demonstrated defect | low | `plugin.json:3`, `SKILL.md:20` and the badge at `README.md:1` all say 4.2. The sentence contradicts itself and invariant I1, and check.py does not see prose (it reads badges only, `scripts/check.py:217`). | Deductive | 95 | Drop the number ("…declares its version in `.claude-plugin/plugin.json`, the same number as…") so it cannot go stale. Or say 4.2 and add the prose to the version check. |
| DO-F2 | `README.md:87-90` | `mkdir -p ~/.claude/skills/adversarial-verify` / `cp skills/adversarial-verify/SKILL.md ~/.claude/skills/adversarial-verify/` | Demonstrated defect | medium | The first install method copies only SKILL.md. SKILL.md then sends the verifier to `references/pre-code.md`, `ux.md` and `execution.md` (`SKILL.md` reference table), which are not there. `README.md:117` itself says this breaks the skill. | Deductive | 92 | `cp -r skills/adversarial-verify ~/.claude/skills/` (as at `README.md:96`), or delete the first method. |
| DO-F3 | `CHANGELOG.md:3` | `…the README badge, .claude-plugin/plugin.json and the first entry below; scripts/check.py fails if they differ.` | Demonstrated defect | low | The first entry below is `## Unreleased` (`CHANGELOG.md:5`). The check uses the first **numbered** entry (`scripts/check.py:237`). It also says "the README badge" where the check promises every badge (`scripts/check.py:10`), and it compares only the first (C-F5). A reader adding a version above Unreleased, or expecting Unreleased to be compared, is misled. | Deductive | 85 | "…every README skill badge, plugin.json and the newest numbered entry below (an `Unreleased` section is skipped)". |

### STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|
| S12 | Time Travel | `README.md:109-117` reference-file table | yes | 82 | It lists the three files with the same conditions as SKILL.md. A maintainer adding a fourth file is forced by `scripts/check.py:519-520` to name it in SKILL.md, though not in the README (minor). |
| S13 | Existence Question | `README.md:241` "the skill mutates a separate copy" paragraph | yes | 80 | Remove it and the user cannot tell whether their working copy is touched. It matches `references/execution.md:27`. It should exist. |
| S14 | Requirement Inversion | `README.md:259` "fails without private terms" | yes | 85 | Inverted (strict mode passes without terms). The code refuses it (`scripts/check.py:294-297`), pinned by `test_missing_terms_fails_in_strict_mode`. |

### HIDDEN BEHAVIORS DETECTED
None beyond the drift between documentation and code reported in the Code domain (C-F1, C-F3, C-F5).

---

## OUT OF SCOPE (listed, not verified)
- `skills/adversarial-verify/examples/agent-trust.json`: the same trust format as `README.md:276-283`. Not compared.
- `skills/adversarial-verify/SKILL.md` and `references/*.md`: read only for ground truth. Their tables and neutral wording are checked by `check.py`, not by this report.

## HYPOTHESES (Abductive — require further investigation)
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| H1 | Each fact file carries a 64-hex `prompt-sha256` (e.g. `facts/56.py:1`) that cannot be recomputed by reasoning | All 11 hashes match the current prompts | One or more prompts were edited after their fact file. Watch eval 56: its assertion was edited (T-F1), though the assertion is not hashed. | P1 (`check.py` prints any "prompt changed" error) |
| H2 | DA-F1, C-F2, C-F3, C-F5 and T-F3 trace to specific test outcomes | `python3 -m unittest scripts/test_check.py` is red on: every `assert_passes` test (DA-F1), `test_whole_word_term_glued_in_output_is_still_masked`, the two-space subtest of `test_two_words_joined_any_way`, and `test_second_badge_mismatch`. `test_file_nobody_names` is green regardless. | The repo is in a deliberately broken state for an exercise, or a local `.check-private-terms` changes outcomes (the tests set `CHECK_PRIVATE_TERMS`, which takes precedence: `scripts/check.py:247-249`) | P1 |
| H3 | `CHANGELOG.md:14` states 57.3 kB, 46.4 kB and 62.5 kB | The sizes are those of SKILL.md before and after the split, and SKILL.md plus the three references | The sizes were measured on a draft, or in another unit (KiB) | P4 (byte counts of the files) |
| H4 | `facts/38.py:17` loops over 10,001 values, and `:19` asserts `repr(old(0.01)) == '0.009000000000000001'` | Both hold (typical binary64 behaviour) | Some k/100 ×0.9 rounded to 2 places misses 1e-9 after ×100 | P2 |
| H5 | `README.md:226-241` cites external tool documentation "read on 2026-10-21" | The table is accurate | A tool changed flags (e.g. Infection's deprecated `--filter`) | Read the cited pages. That needs your approval, because the instructions limit reading to `./tree` and `./skill`. |
| H6 | NOT_COMPUTABLE keeps 52, and `check_facts.py` skips a missing toolchain | Line 13 predates `52.rs` (#25, `CHANGELOG.md:25`) and was never removed. The skip was kept so machines without `rustc` stay green. | Both were left on purpose to tolerate machines without `rustc`, which contradicts `README.md:247` and `:255` | Version history (not available: no git in `./tree`) |

## ADVERSARIAL SCAFFOLD FINDINGS
- **Reviewer blind spots:**
  - A self-contradiction in a reason file (DA-F1) silently turns the whole guard red.
  - A 1-character regex quantifier (`?` vs `*`, C-F3) defeats the privacy check the README advertises.
  - A default argument (`substring=False`) contradicts the comment directly above the call (C-F2).
  - A test whose assertion includes its own expected string (T-F3).
- **Highest-risk claims (blast radius × probability):**
  - DA-F1: every commit blocked, every passing-check test red.
  - C-F3 together with C-F2: private names pass the scan, or are printed into logs.
  - C-F1 together with C-F4: fact checks skipped with no trace in the hook.
- **Multi-step traces:**
  - `facts/52.rs` exists → `NOT_COMPUTABLE:13` names 52 → `scripts/check.py:495` error → `scripts/pre-commit:9` exits 1 → no commit possible.
  - `rustc` missing → `scripts/check_facts.py:91-93` skip → exit 0 → `scripts/pre-commit:17` does not print `$out` → commit passes silently.
  - `=term` configured → `check_private` whole-word misses `termlabs` → `check_evals` prints the key (`scripts/check.py:182`) → `mask` whole-word misses (`:400`) → term in stdout.
- **Subtlety flags:**
  - `badges[:1]` (`scripts/check.py:223`): a slice that reads like a loop.
  - `SEP = r"[\W_]?"` with the comment "anything" (`scripts/check.py:90`).
  - `panic!` counted as an assertion (`scripts/check_facts.py:34`).
  - The "currently 4.1" prose (`README.md:125`).

---

## CROSS-DOMAIN SUMMARY
- **Domains:** Code, Tests, Data, Documentation.
- **Claims:** 26 verified (PASS), 21 in FAIL (C 9, T 7, DA 2, DO 3), 4 falsified (all four tabled).
- **Survived:** 13/14 stress tests passed. S2 (Time Travel on prompt binding) did not, and is reported as T-F4.
- **Failure categories:** 7 systemic patterns: silent fallthrough, missing completeness, assumed environment, stale state, tautological test, missing negative tests, test-environment artifact, plus test-code drift.
- **Invariants:** 9 found (I1–I8 and the doc rule I9), 9 touched. 4 are enforced by a mechanism that bites (I5–I8, each with a minor gap). I2 bites but is violated today. I1 and I3 are partial. I4 has no mechanism. I9 is not respected (DO-F2).
- **Hypotheses:** 6 requiring further investigation.
- **Hidden behaviors:** 8 detected (HB1–HB8; 7 are problems).
- **Findings by type:** **12 demonstrated defects, 9 preventive measures, 4 falsified hypotheses (2 of them conditionally).**
  - Demonstrated defects: C-F1, C-F2, C-F3, C-F4, C-F5, T-F1, T-F2, T-F3, DA-F1, DO-F1, DO-F2, DO-F3.
  - Preventive measures: C-F6, C-F7, C-F8, C-F9, T-F4, T-F5, T-F6, T-F7, DA-F2.
  - Falsified: FH2 and FH3. Conditionally falsified: FH1 and FH4.
- **Critical issues:** 0 demonstrated defects of critical severity. High severity: DA-F1, C-F2, C-F3. Preventive measures of critical severity: 0.
- **Pre-code:** not applicable (no artifact proposes work not yet done).
- **Executed:** 0 tests run (reasoning only).
- **Proposed:** 5 checks and 6 writes awaiting an answer.
- **Changes touching several domains:**
  - The facts registry: DA-F1 (data) breaks the Code check, the Tests baseline, and the README's toolchain promise.
  - C-F1, C-F3 and C-F5: code drifts from what `README.md:250-255` promises.
  - T-F1 and T-F2: eval text drifts from the fact files.
- **Recommendation:** do not trust the repository guard as it stands. It currently fails on its own tree (DA-F1). Two privacy gaps (C-F2, C-F3) and one silent skip (C-F1, C-F4) undermine what the README promises. Fix those four first; all are one-line changes. Then correct the two eval texts, the two README errors and the tautological test.

## PROPOSED EXECUTABLE CHECKS
| # | Claim | Confidence now | Check (command, test or query) | Confirms if | Refutes if | Cost and side effects |
|---|-------|----------------|--------------------------------|-------------|------------|-----------------------|
| P1 | DA-F1, C-F2, C-F3, C-F5, T-F3, H1, H2 | 88 / 90 / 88 / 92 / 95 / H | `python3 scripts/check.py`, then `python3 -m unittest scripts/test_check.py` from the repo root | check.py prints `eval 52 has a fact file and a reason`. The predicted tests are red (H2). No `prompt changed` errors. | check.py exits 0, or the predicted tests are green | Runs 2 Python processes. Reads the tree. The unit tests copy the repo into temp dirs, and some run `git init` and commit **inside those temp copies** (never your working copy). It writes only under the system temp dir and removes it. Needs `git`; the facts tests need `rustc` and `node`. |
| P2 | Fact files 35–57 hold (PASS 4–15, FH4, H4) | 75–95 | `python3 scripts/check_facts.py` | `13 fact file(s), 0 failed` with no `skip` lines | any `FAIL`, or a `skip` (which also confirms C-F1 on that machine) | Runs each fact file. `rustc` compiles `52.rs` into a temp dir, and `node` runs `53.ts`. Read-only on the tree. |
| P3 | FH1: `## Unreleased` does not break the version check | 75 | covered by P1 (no CHANGELOG line in check.py's output) | no CHANGELOG error | a CHANGELOG version error | none beyond P1 |
| P4 | H3: CHANGELOG sizes | H | `wc -c skills/adversarial-verify/SKILL.md skills/adversarial-verify/references/*.md` (byte count only) | 46.4 kB for SKILL.md and 62.5 kB in total, in the stated unit | other sizes | Read-only, one command. 57.3 kB needs the pre-split version, which `./tree` does not have. |
| P5 | C-F1 on a machine without `rustc` | 92 | `PATH=<dir without rustc> python3 scripts/check_facts.py 52; echo $?` | prints `skip 52.rs` and exit 0 | exit non-zero | Read-only. Runs one process with a reduced PATH. |

Proposed writes (none made; each needs its own approval):
1. `skills/adversarial-verify/evals/facts/NOT_COMPUTABLE:13`: delete the `52:` line (DA-F1).
2. `scripts/check_facts.py:91-93`: count a missing toolchain as `FAIL` and `failed += 1` (C-F1). Add a test in `scripts/test_check.py` with `rustc` removed from `PATH` (T-F5).
3. `scripts/check.py`:
   - `:90` → `SEP = r"[\W_]*"`, plus a CRLF subtest (C-F3).
   - `:400` → `term_patterns(terms, substring=True)` (C-F2).
   - `:223` → `for b in badges:` (C-F5).
4. `scripts/test_check.py:479`: replace with `self.assert_fails(r, "orphan.md", "never named in SKILL.md")` (T-F3). Fix or remove `:336-339` (T-F7).
5. `skills/adversarial-verify/evals/evals.json:705`: change "11 are excluded" to "12 are excluded" (T-F1). At `:612`, change "more labels are clipped" to "the same two labels are clipped, by more" (T-F2).
6. `README.md`:
   - `:87-90` → copy the whole folder (DO-F2).
   - `:125` → remove "(currently 4.1)" or make it 4.2 (DO-F1).
   - `CHANGELOG.md:3` → "the newest numbered entry … every README skill badge" (DO-F3).

**Which of the checks P1–P5 may I run, and which of the writes 1–6 may I make?** Nothing runs and nothing is written until you answer.
