# Adversarial verification report — repository checks, docs, manifest and eval facts

**Cost estimate (large request, cost accepted by the request, every choice settled):** 23 files in scope (7 top-level/script files, `evals.json`, 13 fact files, `NOT_COMPUTABLE`, `_parse_day.py`); 4 domains detected (Code, Tests, Data, Documentation); about 75 claims; nothing run (reasoning only). Started without asking, as the request allows.

**Reference files of the skill:** none of the three was needed, so none was read. `references/pre-code.md`: no artifact in scope proposes work not yet done (the CHANGELOG "Unreleased" section describes work already written) and none is a spike report. `references/ux.md`: UX not in the target (see VERIFICATION DOMAIN). `references/execution.md` (of the skill): no run was approved. The tree's own copy, `skills/adversarial-verify/references/execution.md`, was read only as **ground truth** for the CHANGELOG and evals 56/57.

## INTAKE

- **Target:** every domain the skill detects in the 23 listed files (from the request). Detected: **Code** (`scripts/check.py`, `scripts/check_facts.py`, `scripts/pre-commit`), **Tests** (`scripts/test_check.py`, the fact files `evals/facts/*.py|.rs|.ts` and `_parse_day.py`), **Data** (`evals/evals.json`, `.claude-plugin/plugin.json`, `evals/facts/NOT_COMPUTABLE`), **Documentation** (`README.md`, `CHANGELOG.md`, docstrings, comments and error messages). The only interface is the scripts' console output. Under the overlap rule (Step 0), what that text *says* is Documentation. Nothing in scope is a screen, template, style or mock-up, so UX is not a target.
- **Depth:** standard (from the request).
- **Scope:** all of these files (from the request; there is no diff and no history, so "changed path" means the code path as written).
- **Execution mode:** reasoning only (from the request). Nothing was run or written except this report.
- Nothing used a default. To change a choice, say "deep" or "approved checks: …". This consent covers only this verification.

All paths below are relative to `./tree`.

---

# DOMAIN 1 — CODE (`scripts/check.py`, `scripts/check_facts.py`, `scripts/pre-commit`)

## VERIFICATION DOMAIN
Code

## GROUND TRUTH
- The scripts' own contracts: `scripts/check.py:2-50` (docstring, items 1–7), `scripts/check_facts.py:2-19` (docstring).
- What the project promises users: `README.md:245-264` ("Repository checks").
- The tests that encode intended behavior: `scripts/test_check.py` (read as a spec, its results are not used as evidence).
- The data the checks run on: `skills/adversarial-verify/evals/evals.json`, `evals/facts/*`, `SKILL.md:20`, `.claude-plugin/plugin.json:3`, `CHANGELOG.md:5-10`, `.gitignore:1-2`.

## INVARIANTS
Where I looked: every file of `./tree` (Glob listing). There is no `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, `SPEC.md`, `PLAN.md`, ADR folder or `.claude/` in the tree. The project's invariants are stated in `scripts/check.py:2-44` ("Check the repository's own invariants"), `README.md:247-255` and `CHANGELOG.md:3`. Found: 9. Touched by the code in scope: all 9 (the code in scope is the enforcement mechanism).

| # | Invariant | Source | Touched by | Enforced by (file:line / test name) | Bites on changed path? |
|---|-----------|--------|------------|-------------------------------------|------------------------|
| I1 | The skill version agrees in SKILL.md frontmatter, **every** README skill badge, plugin.json and the newest CHANGELOG entry | `scripts/check.py:10-12`, `README.md:250`, `CHANGELOG.md:3` | `check_version` | `scripts/check.py:212-241`; `test_check.py` `VersionTest` | **Partly.** Frontmatter, plugin.json and CHANGELOG are checked. For badges, only the first is checked (`scripts/check.py:223` `badges[:1]`). See C1 |
| I2 | Private terms are never printed: "any output line containing one is masked" | `scripts/check.py:22-23`, `README.md:251` | `mask`, `print_report` | `scripts/check.py:397-414`, `:523-525`; tests `test_whole_word_term_glued_in_output_is_still_masked` | **No for `=` terms**: the masking patterns are built whole-word (`scripts/check.py:400`). See C2 |
| I3 | A term's parts match whatever joins them (space, hyphen, underscore, line break, nothing) | `scripts/check.py:16-17`, `README.md:251` | `term_patterns` | `scripts/check.py:90`, `:274`; test `test_two_words_joined_any_way` | **Only for single-character joins**. See C3 |
| I4 | Every eval ≥ 29 that states facts has a fact file **or** a reason, not both; fact files carry the prompt's sha256 | `scripts/check.py:34-38`, `README.md:255` | `check_facts` | `scripts/check.py:457-501`; `FactsTest` | Yes, it bites (and it currently fires on the tree: Data D1) |
| I5 | A missing toolchain is an error, never a silent skip | `scripts/check_facts.py:8`, `README.md:255` | `main` of check_facts | `scripts/check_facts.py:90-93` | **No**: it prints "skip" and does not count a failure. See C4 |
| I6 | A fact file must assert something outside comments and end with `ok <id>` | `scripts/check_facts.py:11-14` | `has_assertion`, `main` | `scripts/check_facts.py:42-51`, `:105-111`; tests `test_runner_fails_on_a_file_that_asserts_nothing`, `test_runner_fails_without_the_ok_line` | Yes |
| I7 | evals.json format (keys, ids 1..n, tags from 21) | `scripts/check.py:6-9`, `README.md:249` | `check_evals` | `scripts/check.py:163-207`; `EvalsTest` | Yes |
| I8 | Each `references/<name>.md` named exists, and each existing one is named in SKILL.md | `scripts/check.py:39-44`, `README.md:254` | `check_references` | `scripts/check.py:506-520`; `ReferencesTest` | Yes (one test is tautological, Tests T1) |
| I9 | With `--staged`, exactly the staged content is checked | `scripts/check.py:47`, `scripts/pre-commit:2` | `staged_tree`, `main`, hook | `scripts/check.py:386-394`, `:426-437`; `StagedTest` | Yes for check.py. The hook runs the working-tree copy of `check.py` and `check_facts.py`, not the staged copy (Hidden behaviors HB-C4) |

## DECOMPOSED CLAIMS
1. `check_version` compares every README skill badge with the frontmatter (`check.py:10`) — Deductive
2. The frontmatter version is read only from the frontmatter (`check.py:215-216`) — Deductive
3. The newest numbered CHANGELOG entry is the one compared, so "Unreleased" is skipped (`check.py:237`) — Deductive
4. plugin.json version must be a string equal to the frontmatter (`check.py:226-236`) — Deductive
5. Output masking covers every configured term, including `=` terms in glued forms (`check.py:397-400`, `:22-23`) — Deductive
6. Term parts match when joined by a line break, spaces or punctuation (`check.py:16-17`, `:90`) — Deductive
7. Whole-word terms do not match inside other words (`check.py:275`) — Deductive
8. JSON strings are scanned after decoding escapes (`check.py:312-323`) — Deductive
9. Non-UTF-8 files are still scanned (`check.py:112-122`) — Deductive
10. The terms file is never scanned and is gitignored (`check.py:301`, `.gitignore:1`) — Deductive
11. `--strict` fails without terms (`check.py:294-297`) — Deductive
12. `--staged` checks exactly the index and cleans its temp dir (`check.py:386-394`, `:426-440`) — Deductive
13. `--staged` outside git is a clear error, not a traceback (`check.py:392-393`, `:430-432`) — Deductive
14. Neutral-wording check covers SKILL.md, reference files, README, not evals.json (`check.py:140-142`, `:328-336`) — Deductive
15. Table check counts cells correctly with escaped pipes, code spans, no outer pipes, skips fences (`check.py:341-381`) — Deductive
16. `check_facts` (check.py) rejects orphan fact files, missing/old hashes, file+reason, malformed reasons, facts without file/reason (`check.py:457-501`) — Deductive
17. The fact-file hash protects what the fact file reproduces (`check.py:474-482`) — Deductive
18. `check_references` catches missing and unnamed reference files (`check.py:506-520`) — Deductive
19. check_facts.py fails on a missing toolchain (`check_facts.py:8`) — Deductive
20. check_facts.py rejects files without assertions outside comments/strings (`check_facts.py:42-51`) — Deductive
21. Python fact files cannot have their asserts disabled by the environment (`check_facts.py:57`) — Deductive
22. Rust fact files keep their asserts in the `-O` build (`check_facts.py:63`) — Deductive
23. check_facts.py requires `ok <id>` as last output line (`check_facts.py:105-111`) — Deductive
24. check_facts.py fails with no files (`check_facts.py:113`) — Deductive
25. The hook checks the staged content and runs the facts only when evals change (`pre-commit:9-18`) — Deductive
26. The hook shows the facts output when they fail (`pre-commit:15-17`) — Deductive
27. Every error path ends with the summary line (no traceback) — Deductive
28. Exit code is non-zero iff there are errors (`check.py:442`) — Deductive

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Missing completeness (a promise covers N cases, code handles a subset) | 5: only first badge (C1); `=` terms not masked (C2); only 1-char joins (C3); hash binds prompt but not assertions/expected output (C5); NOT_COMPUTABLE reasons not checked against existing evals (C6) | `scripts/check.py` |
| Silent fallthrough | 3: missing toolchain → skip (C4); empty index with `--staged` → no checks, exit 0 (C7); hook discards the facts output on exit 0 (`pre-commit:17`) | `scripts/check_facts.py`, `scripts/check.py`, `scripts/pre-commit` |
| Stale state (comment/doc kept after code changed) | 2: comment "substring patterns" over a whole-word call (`check.py:399-400`); docstring "never a silent skip" (`check_facts.py:8`) | `scripts/check.py`, `scripts/check_facts.py` |
| Assumed environment | 2: `OSError` on a missing plugin.json/CHANGELOG/README not caught → traceback (C8); Windows `python3` store alias (`pre-commit:7-8`, hypothesis) | `scripts/check.py`, `scripts/pre-commit` |

## VERIFICATION RESULTS
### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| 2 | Frontmatter-only version | `check.py:215` anchors `\A---\n(.*?)\n---\n` after CRLF normalization; `:216` searches only `fm.group(1)`. Score 90 |
| 3 | Newest numbered CHANGELOG entry | `check.py:237` `^## +([0-9][0-9.]*)\b` skips `## Unreleased` (`CHANGELOG.md:5`), matches `## 4.2` (`CHANGELOG.md:10`) = `SKILL.md:20` "4.2". Score 90 |
| 4 | plugin.json version string | `check.py:232-236`. `plugin.json:3` "4.2" is a string equal to the frontmatter. Score 90 |
| 7 | Whole-word terms | `check.py:275` lookarounds `(?<![^\W_])…(?![^\W_])` reject a letter/digit on either side. Score 88 |
| 8 | JSON escapes decoded | `check.py:313-323` `json_strings(json.loads(text))` normalized and searched. Score 88 |
| 9 | Non-UTF-8 scanned | `check.py:112-122`: UTF-16 with BOM, else UTF-8-sig, else Latin-1 (never raises). Score 88 |
| 10 | Terms file skipped and ignored | `check.py:301`, `.gitignore:1`; `load_terms` reads from `args.root` (`check.py:423`), never from the staged copy. Score 90 |
| 11 | `--strict` without terms fails | `check.py:294-297`; an env of only separators gives `[]` (`check.py:256`). Score 90 |
| 12 | `--staged` checks the index, cleans up | `check.py:389` `checkout-index -a --prefix`, `:433` `root = tmp`, `:438-440` `rmtree` in `finally`. Score 85 |
| 13 | `--staged` outside git → clear error | `check.py:392-393` catches `CalledProcessError`/`OSError`, `:431` error, summary printed `:441`. Score 88 |
| 14 | Neutral wording scope | `check.py:140-142` (SKILL + refs + README), `:331`; evals.json not in the list. Score 90 |
| 15 | Table cell counting | `check.py:344-350` (code spans and `\|` replaced before counting, outer pipes stripped); fences `:361-368`; delimiter count `:372-373`. Score 85 (closing fence of the other kind also closes, low) |
| 16 | check_facts (check.py) branches | orphan `:469-471`; no hash `:479-480`; stale hash `:481-482`; malformed reason `:490-493`; both `:495-496`; neither `:497-501`. Score 90 |
| 18 | Reference files | `check.py:508-520`, regex `:67`. Names only in SKILL count as "named" (`:515-516`). Score 90 |
| 20 | Assertion detection | `.py` via AST `Assert`/`Raise` (`check_facts.py:45-50`), `.rs`/`.ts` regex after stripping comments and strings (`:34-39`, `:51`). Score 85 (Rust raw strings `r"…"` not stripped: a `panic!` inside one would count, low) |
| 23 | `ok <id>` required | `check_facts.py:106-109`; empty output gives `[] != ["ok N"]`, so it is a FAIL. Score 90 |
| 24 | No files → exit 1 | `check_facts.py:113` `failed or not files`. Score 90 |
| 25 | Hook on staged content, facts when evals change | `pre-commit:9` `--staged --root "$root"`; `:12` `git diff --cached --name-only \| grep -q '^skills/adversarial-verify/evals/'`; `:14` checkout of the index into a temp dir; `:15` `--root "$tmp"`. Score 85 |
| 28 | Exit code | `check.py:442`, `:531`. Score 92 |

### FALSIFIED HYPOTHESES
| # | Location | Suspected defect | Check (quote) | Status | Could it have failed? | Paths not covered | Mode | Confidence |
|---|----------|------------------|-------|--------|------------------------|-------------------|------|------------|
| FH-C1 | `scripts/check_facts.py:57` | `PYTHONOPTIMIZE` in the environment turns every Python fact's `assert` into a no-op, so false facts pass | `[sys.executable, "-E", "-s", path]` | falsified (by reading) | Yes: without `-E` the variable would apply. `-E` makes the interpreter ignore every `PYTHON*` variable, `PYTHONOPTIMIZE` included. The suspicion would have held had the flag been absent | An interpreter started through a wrapper that adds `-O`. `sys.executable` pointing at such a wrapper is not covered | Deductive | 78 (language semantics, not a file in the tree; run-only cap not lifted) |
| FH-C2 | `scripts/check_facts.py:63` | `rustc -O` removes `assert!`, so `52.rs` asserts nothing in the release build | `[rustc, "--edition", "2021", "-O", …]` | falsified (by reading) | Yes: the suspicion holds for `debug_assert!`. `52.rs:14-17` uses `assert_eq!`/`assert_ne!`, which stay in optimized builds | `-C debug-assertions` flags from a user `RUSTFLAGS` do not apply to `rustc` directly, so they are not covered | Deductive | 75 |

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| C1 | `scripts/check.py:223` | `for b in badges[:1]:` | Demonstrated defect | medium | `README.md` gains a second badge `skill-v2.0` (exactly `test_check.py:171-173`). `badges == ['4.2','2.0']`, only `'4.2'` is compared, and no error results. This contradicts `check.py:10` ("every skill badge") and `README.md:250`. `test_second_badge_mismatch` would be red (prediction, see PROPOSED) | Deductive | 92 | `for b in badges:` |
| C2 | `scripts/check.py:399-400` | `# substring patterns: when hiding output, err on the side of hiding too much` / `pats = term_patterns(terms)` | Demonstrated defect | high (private names printed to the console/CI log) | `term_patterns` defaults to `substring=False` (`:259`, `:265`), so a `=acme` term masks only the whole word. A key `acmecorp_notes` in an eval (printed by `:182`) or a reference `references/acmecorp.md` (printed by `:518`) is output in clear. This breaks `check.py:22-23` and `README.md:251` ("any output line containing a term is masked"). `test_whole_word_term_glued_in_output_is_still_masked` (`test_check.py:341-344`) would be red | Deductive | 92 | `pats = term_patterns(terms, substring=True)` |
| C3 | `scripts/check.py:90` | `SEP = r"[\W_]?"  # anything that is not a letter or digit, possibly nothing` | Demonstrated defect | medium | `SEP` allows at most one character. Term `quillane dorvex` written `QUILLANE  dorvex` (two spaces, `test_check.py:286`), split over a CRLF line break (`\r\n` is two characters), or `quillane - dorvex` does not match. The scan (`:274`) and the masking (`:400`) both miss it. This contradicts `README.md:251` ("line break") and `check.py:16-17` ("anything") | Deductive | 90 | `SEP = r"[\W_]*"` (or a bounded `{0,3}`), and say in the docs which forms are covered |
| C4 | `scripts/check_facts.py:90-93` | `if steps is None: print(f"skip {name}: toolchain not found"); continue` | Demonstrated defect | medium | On a machine without `rustc` or `node`, `52.rs`/`53.ts` are skipped, `failed` stays 0 and the script exits 0. In the hook (`pre-commit:15-17`) the output is printed only when `rc != 0`, so the skip is fully silent and a commit with a false Rust/TS fact passes. This contradicts `check_facts.py:8` ("A missing toolchain is an error, never a silent skip") and `README.md:255` | Deductive | 92 | Print `FAIL {name}: toolchain not found`, `failed += 1` |
| C5 | `scripts/check.py:474-482` | `want = hashlib.sha256(prompts[i].encode("utf-8")).hexdigest()` | Preventive measure | medium | The hash binds the prompt only. An edit to `expected_output` or `assertions` that contradicts the fact file passes. This is already the case for eval 56 (Data D2: the assertion says 11 excluded, `56.py:12` proves 12). Likelihood: shown to occur once | Deductive | 85 | Hash `prompt + expected_output + assertions`, or add numeric-consistency checks for the stated assertions |
| C6 | `scripts/check.py:484-494` | `reasons[int(m.group(1))] = m.group(2)` | Preventive measure | low | A reason for an eval that does not exist, or whose prompt states no facts, is accepted silently. Fact files get that check (`:470-471`), reasons do not. Turns into a defect when an eval is renumbered | Deductive | 82 | Error when a reason's id is not an eval id ≥ `FACTS_FROM` stating facts |
| C7 | `scripts/check.py:436-437` | `if files or not args.staged: run_checks(...)` | Preventive measure | low | `--staged` in a repository whose index is empty (first commit before `git add`) runs no check and exits 0 with "0 error(s)". Turns into a defect only if a commit can be made with an empty index, which is rare | Deductive | 80 | Report "nothing staged" explicitly |
| C8 | `scripts/check.py:226-230`, `:237`, `:214`, `:217` | `except ValueError as e:` | Preventive measure | low | A missing `plugin.json`, `CHANGELOG.md` or `README.md` raises `FileNotFoundError` (an `OSError`, not caught), so the script dies with a traceback and no summary line. `check_evals` catches `OSError` (`:167`), these reads do not. The traceback holds only constant paths: no leak | Deductive | 85 | Catch `OSError` and report `rep.error(path, "missing")` |

## STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|
| S-C1 | Requirement Inversion | Claim 3 (newest numbered CHANGELOG entry): what if the project wants "Unreleased" first, as it does now? | yes | 88 | `check.py:237` needs a digit after `## `, so `CHANGELOG.md:5` is skipped and `:10` is used |
| S-C2 | Scale Shift | Claim 16 / `check_evals` at 10× evals (570) and at 0 | yes | 80 | Duplicate detection `ids.count(i)` (`check.py:203`) is O(n²): 570² ≈ 3·10⁵ operations, negligible. 0 evals gives the error "no 'evals' list" (`:171-173`) |
| S-C3 | Time Travel | Claim 18 (`check_references`) in 6 months when someone adds `references/glossary.md` named only by `ux.md` | yes | 88 | `check.py:515-520` counts only SKILL.md names, so it reports an error, as `test_check.py:481-485` intends |
| S-C4 | Existence Question | `check.py:399` comment and the `substring` parameter (`:259`) | no (see C2) | 90 | The parameter exists only for the masking, and the only caller that needs it does not pass it. Deleting it mentally changes nothing in behavior, which shows the mask does not use it |

## HYPOTHESES
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| HY-C1 | `pre-commit:7-8` picks `python3` when `command -v` finds it | On Windows, `python3` is the Store alias stub, which exists and fails, so every commit fails | The Git-for-Windows `sh` PATH does not include the WindowsApps alias, so `python` is used | Run the hook on a Windows machine with the alias enabled |
| HY-C2 | `check_facts.py:62` names the Rust binary `52.rs.bin` | On Windows, CreateProcess runs a PE file whatever its extension, so this works | Some environments (AppLocker, AV) block non-`.exe` executables | `python scripts/check_facts.py 52` on Windows |

## HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| HB-C1 | `scripts/check_facts.py:112` | "N fact file(s), M failed" | Skipped files are counted in N, as if they had run | Demonstrated defect (part of C4) | 90 |
| HB-C2 | `scripts/check.py:400` | substring masking (comment `:399`) | whole-word masking for `=` terms | Demonstrated defect (C2) | 92 |
| HB-C3 | `scripts/check.py:145-158` | "the files tracked by git (all files outside .git if git is not available)" (`:46-47`) | Also falls back to the full walk when the root is not a repository or has no tracked file, so untracked files (`.venv`, build output) are scanned | not a problem (stricter) | 85 |
| HB-C4 | `scripts/pre-commit:9`, `:15` | "run the checks on exactly what is staged" (`:2`) | The **content** checked is staged, but the **checker** scripts run from the working tree. A staged change to `check.py`/`check_facts.py` is not what runs, and a change only to `scripts/check_facts.py` does not trigger the facts run (`:12`) | Preventive measure (low) | 85 |

## ADVERSARIAL SCAFFOLD FINDINGS
- Reviewer blind spots: the comment at `check.py:399` says the opposite of the call under it. Default arguments (`substring=False`) hide the defect. `[:1]` reads like "the first badge is the badge".
- Highest-risk claims: (1) masking of private terms, C2 (leak to CI logs, irreversible); (2) the missing toolchain skip, C4 (false facts committed silently); (3) separator matching, C3 (a leak not detected).
- Multi-step traces: missing `rustc` → `check_facts.py:91-93` skip → `:113` exit 0 → `pre-commit:17` discards `$out` → commit accepted with an unexecuted `52.rs`. Also: `=` term → `check.py:265` whole-word → private scan misses `acmecorp_notes` → `check_evals` prints the key (`:182`) → `mask` whole-word (`:400`) → printed in clear.
- Subtlety flags: `check.py:90` (`?` vs `*`), `check.py:223` (`[:1]`), `check.py:400` (missing keyword argument).

### SUMMARY
- Domain: Code
- Claims: 18 verified, 8 in FAIL (4 defects, 4 preventive), 2 falsified
- Survived: 3/4 stress tests passed
- Failure categories: 4 systemic patterns
- Invariants: 9 found, 9 touched, 5 enforced by a mechanism that bites (I4, I6, I7, I8, I9). I1, I2, I3 and I5 only partly or not
- Hypotheses: 2
- Hidden behaviors: 4 detected
- Findings by type: 4 demonstrated defects, 4 preventive measures, 2 falsified hypotheses (0 conditionally)
- Critical issues: 0 demonstrated defects of critical severity (preventive critical: 0)
- Pre-code: not applicable
- Executed: 0 tests run
- Proposed: see the single PROPOSED EXECUTABLE CHECKS section
- Recommendation: do not trust the private-term guarantee for `=` terms or multi-character joins, nor the facts gate on machines without rustc/node, until C2, C3 and C4 are fixed.

---

# DOMAIN 2 — TESTS (`scripts/test_check.py`, `evals/facts/*`)

## VERIFICATION DOMAIN
Tests

## GROUND TRUTH
- Production code: `scripts/check.py`, `scripts/check_facts.py`.
- Production configuration: the pre-commit hook (`scripts/pre-commit`), which runs `check.py --staged` in a git repository with the developer's environment.
- The evals each fact file reproduces: `evals/evals.json:439-723` (prompts 35–57).
- `references/execution.md:31` (tree) for the exclusion rule of eval 56.

## INVARIANTS
Same sources as the Code domain. The test suite touches I1–I9 as their enforcing mechanism. Touched ones where the test is the mechanism:

| # | Invariant | Source | Touched by | Enforced by | Bites? |
|---|-----------|--------|------------|-------------|--------|
| I1 | Every badge agrees | `check.py:10` | `test_second_badge_mismatch` | `test_check.py:171-173` | Yes: the test would fail on the current code (it detects C1) |
| I2 | Terms never printed | `check.py:22-23` | `assert_no_leak`, `test_whole_word_term_glued_in_output_is_still_masked` | `test_check.py:70-73`, `:341-344` | Yes (detects C2) |
| I5 | Missing toolchain is an error | `check_facts.py:8` | `test_runner_passes_on_the_repo` | `test_check.py:575-578` | **No**: no test removes the toolchain, and the test passes without one (T2) |
| I8 | Unnamed reference file is an error | `check.py:43` | `test_file_nobody_names` | `test_check.py:475-479` | **No**: tautological (T1). `test_file_named_only_by_another_reference_file_is_still_unnamed` (`:481-485`) does bite |

## DECOMPOSED CLAIMS
1. Every `assert_fails` test requires the script to reach its summary and name the failure (`test_check.py:54-62`) — Deductive
2. No test term appears literally in the repo (`test_check.py:22-26`) — Deductive
3. Each test fails when the invariant it covers is broken — Deductive, checked per test
4. `test_file_nobody_names` detects an unnamed reference file — Deductive
5. Tests that call `run_check()` without terms see "no terms configured" — Deductive
6. `test_runner_passes_on_the_repo` proves the facts pass with all toolchains — Deductive
7. `test_prompt_changed_after_its_facts` really changes eval 37's prompt — Deductive
8. Edit targets in fact-file tests exist (`38.py`, `40.py`, `49.py`, `51.py`) — Deductive
9. The test environment (no `.git`, `os.walk` listing) matches the production path (git `ls-files`) — Deductive
10. 35.py: `parse_day_v1('2026-02-31') == (2026,2,31)` — Deductive
11. 37.py: same as eval 37 facts — Deductive
12. 38.py: new rounding has two decimals for k ∈ [0,10000], old fails first at k=1, `0.01*0.9` repr, `round(10.05*0.9,2)==9.05` — Deductive
13. 39.py: parent and fixed both reject 31 April; 29 Feb 2024 separates them; fixed rejects 2026-02-29 and 2100-02-29 — Deductive
14. 40.py: tests kill exactly `<`, `<=`, `return True`; boundary tests kill the rest — Deductive
15. 42.py: four variants all pass the two tests — Deductive
16. 48.py: the contrast ratios — Deductive (hand computation)
17. 49.py: usable widths and clipped labels — Deductive
18. 51.py: heights 44 and 24 — Deductive
19. 52.rs: `days_in_month(2024,2) == 28` — Deductive
20. 53.ts: 24/21/25 Oct 2026 are Sat/Wed/Sun; survivors `0 -> 1`, `day === 0 -> false`; a Sunday kills both — Deductive
21. 56.py: counts reconcile; 108 measured, 12 excluded, 96% — Deductive
22. 57.py: counts reconcile; 2 survivors unaccounted — Deductive
23. Each fact file reproduces the function shown in its eval — Deductive
24. `_parse_day.py` header lists its users — Deductive

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Tautological test | 1 (T1) | `scripts/test_check.py` |
| Test-environment artifact (changed defaults, different path into the code, different resources) | 3: inherited `CHECK_PRIVATE_TERMS` (T3); suite runs the `os.walk` path while the hook runs git `ls-files`/`checkout-index` (T4); test green without rustc/node (T2) | `scripts/test_check.py` |
| Stale state (comments drifted from the code) | 2: `test_check.py:337` comment; `_parse_day.py:1` header (T5) | `scripts/test_check.py`, `evals/facts/_parse_day.py` |
| Assumed environment | 1: `os.symlink` (T6) | `scripts/test_check.py` |

## VERIFICATION RESULTS
### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| 1 | `assert_fails` is strict | `test_check.py:57-62`: non-zero exit, summary present, `ERROR`, each token, no leak. Score 88 |
| 2 | Test terms built at runtime | `test_check.py:24-26` concatenations; `"adver"+"saria"` `:260`. Score 85 |
| 7 | Eval 37 prompt really edited | `test_check.py:550` replaces `day > 31` in `evals[36]` (id 37, `evals.json:462`); the prompt contains `day > 31` (`evals.json:463`). Score 90 |
| 8 | Edit targets exist | `38.py:21` `assert round(10.05 * 0.9, 2) == 9.05`; `40.py:1` `# prompt-sha256:`, `:13` `print('ok 40')`; `49.py:12-14` the three `assert clipped(...)`; `51.py:1` hash line. Score 92 |
| 10–11 | 35.py, 37.py | `_parse_day.py:5-12` only checks `1 ≤ day ≤ 31`, so 31 Feb returns the tuple. Matches `evals.json:440`, `:463`. Score 79 (run-only cap: these are fact files whose result is a run) |
| 12 | 38.py | `0.01*0.9` is `0.009000000000000001` in binary64, so `first == 1` (k=0 gives 0.0, which is whole). `round(x,2)*100` lies within 1e-9 of an integer for x ≤ 90. `10.05` is stored slightly above 10.05 and `×0.9` gives ≈ 9.0450000000000009, so 9.05. Matches `evals.json:475`. Score 75 (run-only) |
| 13 | 39.py | `_parse_day.py:15-35`: DAYS[3]=30 rejects 04-31 in both. Parent DAYS[1]=28 rejects 2024-02-29; fixed `leap(2024)` gives 29 and accepts it. 2026 and 2100 are not leap years. Matches `evals.json:487`. Score 79 |
| 14 | 40.py | (30,T),(5,F): `<` fails 30, `<=` fails 30, `True` fails 5. `>`, `>=19`, `>=17` pass both. Boundary (18,T),(17,F) kills `>` (18), `>=19` (18), `>=17` (17). Matches `evals.json:499`. Score 79 |
| 15 | 42.py | `100*0.9` rounds to exactly 90.0 in binary64. `round(90.0,0)=90.0`. `''` is falsy. Matches `evals.json:527`. Score 79 |
| 16 | 48.py (all except the 3.23 boundary) | Hand computation of WCAG relative luminance: #333/#fff 12.63, #6b6b6b/#fff 5.33, #2563eb/#fff 5.17, #d0d0d0/#1e1e1e 10.81, #6b6b6b/#1e1e1e 3.13, #3a3a3a/#1e1e1e 1.47, #8a8a8a/#1e1e1e 4.83. All agree with `48.py:17-21` and `evals.json:599-605`. Score 72 (hand-computed, run-only) |
| 17 | 49.py | 375/4−16=77.75 (79, 82 > 77.75); 320/4−16=64 (61, 50 fit); 430/4−16=91.5. Matches `evals.json:611-615`. Score 79 |
| 18 | 51.py | 20+24=44, 16+8=24, 44 ≥ 44 > 24. Matches `evals.json:636-640`. Score 79 |
| 19 | 52.rs | `52.rs:3-11` is identical to `evals.json:648`; `2 => 28`. Score 79 |
| 20 | 53.ts | 1 Jan 2026 is a Thursday, and 24 Oct is day 297, so (297−1) mod 7 = 2, a Saturday. 21 Oct is a Wednesday and 25 Oct a Sunday. Survivors sort `"0 -> 1" < "day…"`. Only erasable TS syntax (type alias, annotations), valid under strip-types. Matches `evals.json:660`. Score 78 |
| 21 | 56.py | 104+5+8+3=120; 4 measured survivors; 108 measured; excluded 8+3+1=12; 100·104/108=96.3 rounds to 96. Matches `evals.json:698-699` and `references/execution.md:31`. Score 79 |
| 22 | 57.py | 239+9+12=260; 8−7=1 discarded; 9−7=2. Matches `evals.json:712-713`. Score 79 |
| 23 | Fact files reproduce the shown functions | `_parse_day.py:5-12` = `evals.json:370`/`:440`/`:463`; `:15-21` = `:487`; `38.py:5-10`, `42.py:5-6` = `:475`/`:523`; `40.py:5-6` = `:499`; `53.ts:4` = `:660`. Score 85 |

### FALSIFIED HYPOTHESES
| # | Location | Suspected defect | Check (quote) | Status | Could it have failed? | Paths not covered | Mode | Confidence |
|---|----------|------------------|-------|--------|------------------------|-------------------|------|------------|
| FH-T1 | `scripts/test_check.py:550` | The edit is a no-op (target text absent), so the "prompt changed" test proves nothing | `replace("day > 31", "day > 28")` on `evals[36]` | falsified | Yes: had `evals.json:463` lacked `day > 31`, the prompt would be unchanged and the hash would still match. It contains the text, so the hash changes | Whether the error names `37.py` depends on `check.py:482` (traced: it does) | Deductive | 88 |

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| T1 | `scripts/test_check.py:478-479` | `r = self.run_check(terms=NONE)` / `self.assertIn("orphan.md", r.stdout + self.ref("orphan.md"))` | Demonstrated defect (tautological test) | medium | `self.ref("orphan.md")` always contains "orphan.md", so the assertion is true whatever `check.py` prints. Delete `check.py:519-520` and the test stays green | Deductive | 95 | `self.assert_fails(r, "orphan.md", "never named in SKILL.md")` |
| T2 | `scripts/test_check.py:575-578` | `r = self.run_facts()` / `self.assertEqual(r.returncode, 0, …)` / `assertRegex(… r"\d+ fact file\(s\), 0 failed")` | Demonstrated defect (test-environment artifact: different resources) | medium | On a machine without rustc/node, `52.rs`/`53.ts` are skipped (`check_facts.py:91-93`), the output still reads `13 fact file(s), 0 failed` and the test is green. The test cannot tell "all facts true" from "two not run". No test covers I5 | Deductive | 88 | Assert that no line starts with `skip`, and add a test that runs with a `PATH` lacking `rustc` and expects a failure (after C4) |
| T3 | `scripts/test_check.py:43-45` | `env = dict(os.environ)` / `if terms is not None: env["CHECK_PRIVATE_TERMS"] = terms` | Preventive measure (test-environment artifact: changed defaults) | low | A developer who exports `CHECK_PRIVATE_TERMS` (the README invites it, `README.md:251`) makes `test_missing_terms_is_said_not_silent` and `test_missing_terms_fails_in_strict_mode` (`:354-360`) red, and the run may match their real terms in the copied tree. Turns into a defect as soon as the variable is set | Deductive | 85 | `env.pop("CHECK_PRIVATE_TERMS", None)` before applying `terms` |
| T4 | `scripts/test_check.py:31-37` | `for item in ("README.md", "CHANGELOG.md", "skills", ".claude-plugin", "scripts", ".gitignore"):` | Preventive measure (test-environment artifact: different path into the code) | low | The copy has no `.git`, so every test except `StagedTest` and one `ReferencesTest` runs the `os.walk` fallback (`check.py:153-158`). Production (the hook) uses `git ls-files`/`checkout-index`. A defect only on the git path (e.g. ls-files paths with non-UTF-8 names, `check.py:148` `"replace"`) would go unseen | Deductive | 80 | Run the main private-term cases once more inside an initialised repository |
| T5 | `skills/adversarial-verify/evals/facts/_parse_day.py:1` | `# Shared by facts/37.py and facts/39.py` | Demonstrated defect (stale comment) | low | `facts/35.py:3` also imports `parse_day_v1` (the function's own comment `:5` says "evals 29, 35 and 37"). Someone editing the helper for 37/39 would not know 35 depends on it | Deductive | 92 | `# Shared by facts/35.py, 37.py and 39.py` |
| T6 | `scripts/test_check.py:351` | `os.symlink(os.path.join(self.tmp, "does-not-exist"), self.path("dangling.md"))` | Preventive measure (assumed environment) | low | On Windows without Developer Mode or admin rights, `os.symlink` raises `OSError` and the test errors, although `README.md:264` documents Windows use | Deductive | 78 | `skipUnless` symlinks can be created, or make the file unreadable another way |
| T7 | `scripts/test_check.py:336-337` | `# whole-word detection does not flag "<term>labs", but the evals check prints the key name` | Demonstrated defect (stale comment) | low | The test uses `terms=T1` (no `=`), which is a substring term (`check.py:265`), so detection does flag `zqvorblaxlabs`. The comment describes the next test (`:341-344`). A reader misjudges what each test covers | Deductive | 88 | Fix the comment, or make the test use `"=" + T1` and drop the duplicate |

## STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|
| S-T1 | Existence Question | `_parse_day.py` shared helper | yes | 85 | Deleting it duplicates three function bodies over 35/37/39.py. Sharing keeps them identical to the eval prompts. It is excluded from runs by `_` (`check_facts.py:83`, `check.py:469`) |
| S-T2 | Scale Shift | 38.py k-range at 10× (k ≤ 100000, totals up to 1000) | yes | 70 | `round(x,2)*100` stays within 1e-9 of an integer for x ≤ 900 (ulp at 9·10⁴ ≈ 1.5e-11). The fact still holds |
| S-T3 | Time Travel | 48.py `#2563eb` on `#1e1e1e` == 3.23 | no (fragile) | 60 | Hand computation gives 3.22551, about 1e-5 above the rounding boundary 3.225. A future change of the formula's constants (e.g. 0.03928 vs 0.04045, both in use) could change the second decimal. See HY-T1 |
| S-T4 | Requirement Inversion | `assert_passes` (`test_check.py:64-68`): what if a valid repo legitimately has errors elsewhere? | no | 85 | Every `assert_passes` test asserts that the **whole** run has no `ERROR`. With the current tree (Data D1) all of them would be red for a reason unrelated to the case they test: 18 tests depend on the repository being otherwise clean |

## HYPOTHESES
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| HY-T1 | `48.py:19` asserts `r('#2563eb','#1e1e1e') == 3.23`; the hand computation gives 3.22551 | binary64 gives ≥ 3.225, so it rounds to 3.23 and the fact holds | Accumulated float error lands below 3.225 and `48.py` fails | `python3 scripts/check_facts.py 48` |
| HY-T2 | Every fact file carries a `prompt-sha256` | The hashes match the current prompts (the tree is consistent) | One prompt was edited after its hash was set | `python3 scripts/check.py` (an error "prompt changed since its facts were checked" refutes) |
| HY-T3 | `test_check.py:320` `("﻿" + …)` | The literal holds an invisible U+FEFF, so the test covers a BOM | The character was lost in an edit and the test covers no BOM | Read the bytes of line 320 (e.g. `xxd`), or a test asserting `len("﻿") == 1` |

## HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| HB-T1 | `scripts/test_check.py:64-68` | "the repo passes" only in `RepoTest` | Every `assert_passes` call also re-asserts that the whole repo is clean, so one repo error turns ~18 unrelated tests red | not a defect by itself, but it amplifies D1 | 88 |
| HB-T2 | `scripts/test_check.py:571-573` | runs the facts of the copy | `run_facts` does not pass `-I`; the child processes still use `-E -s` (`check_facts.py:57`) | none | 80 |

## ADVERSARIAL SCAFFOLD FINDINGS
- Reviewer blind spots: `r.stdout + self.ref(...)` (T1) looks like a helpful message concatenation. The "0 failed" regex hides skips (T2).
- Highest-risk claims: T2 (the gate meant to catch false facts is green with no toolchain), T1 (reference-file invariant untested in practice), HB-T1 (a single data error turns the suite red wholesale, which trains people to ignore it).
- Multi-step traces: `NOT_COMPUTABLE:13` + `52.rs` → `check.py:495-496` ERROR → every `assert_passes` red → `test_repo_passes`, `test_repo_passes_strict` red.
- Subtlety flags: `test_check.py:479`; `48.py:19` value 1e-5 from a rounding boundary.

### SUMMARY
- Domain: Tests
- Claims: 17 verified (10 of them ≤ 79 under the run-only cap), 7 in FAIL (4 defects, 3 preventive), 1 falsified
- Survived: 2/4 stress tests passed
- Failure categories: 4 systemic patterns
- Invariants: 9 found, 4 touched as the tests' subject, 2 enforced by a test that bites (I1, I2), 2 not (I5, I8 via T1)
- Hypotheses: 3
- Hidden behaviors: 2 detected
- Findings by type: 4 demonstrated defects, 3 preventive measures, 1 falsified hypothesis (0 conditionally)
- Critical issues: 0 (preventive critical: 0)
- Pre-code: not applicable
- Executed: 0
- Proposed: see the closing section
- Recommendation: the fact files' arithmetic is sound by hand computation. The unit suite has one tautological test and one test that cannot see a missing toolchain. Fix T1 and T2 before relying on the suite as a gate.

---

# DOMAIN 3 — DATA (`evals/evals.json`, `.claude-plugin/plugin.json`, `evals/facts/NOT_COMPUTABLE`)

## VERIFICATION DOMAIN
Data

## GROUND TRUTH
- The format contracts enforced by `scripts/check.py:163-207` (evals), `:226-236` (plugin version), `:483-501` (NOT_COMPUTABLE).
- The current SKILL.md (`skills/adversarial-verify/SKILL.md:20`, `:439`) and `references/execution.md:28-31` (tree) for what eval assertions should expect.
- The fact files (Tests domain) as computed truths for eval numbers.

## INVARIANTS
| # | Invariant | Source | Touched by | Enforced by | Bites? |
|---|-----------|--------|------------|-------------|--------|
| I4 | An eval with facts has a fact file **or** a reason, not both | `check.py:34-38` | `NOT_COMPUTABLE:13` and `facts/52.rs` | `scripts/check.py:495-496` | Yes. It bites **now**: the data violates it (D1) |
| I7 | evals.json format | `check.py:6-9` | all 57 evals | `scripts/check.py:163-207` | Yes. Respected: ids 1..57 consecutive (`evals.json:5`…`:711`); every eval has the four keys; assertions from 21 on carry tags (`:282`…`:721`) |
| I1 | Version agreement | `check.py:10-12` | `plugin.json:3` | `scripts/check.py:226-236` | Yes; respected (`"4.2"` = `SKILL.md:20`) |

## DECOMPOSED CLAIMS
1. evals.json satisfies the format contract — Deductive
2. Every eval ≥ 29 with "(Facts" has exactly one of fact file / reason — Deductive
3. Each NOT_COMPUTABLE reason is true of its eval — Deductive
4. Each eval's expected_output and assertions agree with its own facts — Deductive
5. Eval assertions agree with the current SKILL.md — Inductive (sampled)
6. plugin.json is valid, its version is a string equal to the skill's, the repository URL matches the README — Deductive
7. plugin.json description matches the skill's capabilities — Deductive

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Missing completeness (a change made in one place but not in its paired place) | 2: `52.rs` added and `NOT_COMPUTABLE:13` left in (D1); 12 excluded in expected_output/fact vs 11 in an assertion (D2) | `NOT_COMPUTABLE`, `evals.json` |
| Stale state | 1: eval 18 assertion quotes an old summary line (D3) | `evals.json` |

## VERIFICATION RESULTS
### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| 1 | evals.json format | ids `evals.json:5`…`:711` are 1..57 in order; the sampled evals all have id/prompt/expected_output/assertions; tags present from 21 (`:282`) to 57 (`:721`); eval 20 untagged (`:269`), as `test_check.py:158` expects. Score 82 (format read for all 57; JSON validity itself is run-only, but the file reads as balanced) |
| 2 | Facts coverage (except 52) | "(Facts" evals ≥ 29: 30, 32, 33, 34, 36, 41, 43, 45, 50 have reasons (`NOT_COMPUTABLE:4-12`); 35, 37, 38, 39, 40, 48, 49, 51, 53, 56, 57 have files. 42 has a file without "(Facts", which is allowed. 31, 44, 46, 47, 54, 55 state no "(Facts" block. Score 85 |
| 3 | Reasons true (except 52) | e.g. 34: query plan (`evals.json:427`); 41: log described in words (`:511`); 50: a menu in words (`:623`). Score 80 |
| 6 | plugin.json | `plugin.json:1-20` is valid JSON by reading; `"version": "4.2"`; `repository` = `README.md:95` URL; `license` MIT = `README.md:3`, `:309`. Score 88 |
| 7 | Description | `plugin.json:4` lists the seven domains, typed findings, invariants, consent, plans/spikes/mock-ups, all in `SKILL.md:3-15`. Score 85 |

### FALSIFIED HYPOTHESES
None.

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| D1 | `skills/adversarial-verify/evals/facts/NOT_COMPUTABLE:13` | `52: the compiler is not installed on every machine` | Demonstrated defect | high | `facts/52.rs` exists and is bound to eval 52 (`52.rs:1`), so `check.py:466-473` puts 52 in `with_file`, `:486-494` puts it in `reasons`, and `:495-496` emits `ERROR …/NOT_COMPUTABLE: eval 52 has a fact file and a reason not to have one`. `python3 scripts/check.py` exits 1 on the tree. The hook (`pre-commit:9`) blocks **every** commit, and all `assert_passes` tests (Tests HB-T1) go red. The reason also contradicts I5 ("a missing toolchain is an error") | Deductive | 93 | Delete line 13 of `NOT_COMPUTABLE` |
| D2 | `skills/adversarial-verify/evals/evals.json:705` | `"… says that 11 are excluded: 8 timed out, 3 skipped, 1 not measured"` | Demonstrated defect | medium | 8+3+1 = 12. The same eval's expected_output (`:699`, "with 12 excluded"), its fact file (`facts/56.py:11-13`, `excluded == 12`, `measured + excluded == total`) and the rule (`references/execution.md:31`) all give 12. A grader following the assertion fails a correct answer, or passes an answer that miscounts | Deductive | 95 | `"… says that 12 are excluded: 8 timed out, 3 skipped, 1 not measured"` |
| D3 | `skills/adversarial-verify/evals/evals.json:249` | `"… 'Invariants: N found, M touched, K enforced by a mechanism that bites on the changed path (code, data) or respected (plans, specs, docs, analyses)'"` | Demonstrated defect (stale assertion) | low | `SKILL.md:439` now reads `(code, data, tests, UX) … (plans, specs, docs, analyses, mock-ups)`. A grader checking the literal line fails an answer that follows the current skill | Deductive | 90 | Quote the current line, or assert the presence of the summary line without its wording |

## STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|
| S-D1 | Time Travel | Claim 2 (facts coverage) when a reason's eval later gets a fact file | no | 93 | That happened to eval 52 (D1). Nothing removes the reason automatically; only the check catches it |
| S-D2 | Requirement Inversion | Claim 6: what if the plugin version were wanted ahead of the skill (pre-release)? | yes | 80 | `check.py:235` forbids any difference, which is consistent with `CHANGELOG.md:3`. The inversion is refused by design, not broken |
| S-D3 | Scale Shift | Claim 1 at 0 assertions / empty prompt | yes | 88 | `check.py:191-197` rejects empty prompt, expected_output and assertions |

## HYPOTHESES
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| HY-D1 | Line 13 of `NOT_COMPUTABLE` predates `52.rs` (the reason argues the compiler is missing) | `52.rs` was added with #25 (`CHANGELOG.md:25`) and the reason was not removed | The reason was added later to silence a failure on a machine without rustc (which C4's skip would make unnecessary) | `git log -p -- skills/adversarial-verify/evals/facts/NOT_COMPUTABLE` (no history in this tree) |

## HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type | Confidence |
|---|----------|-----------|--------|------|------------|
| HB-D1 | `evals.json` assertions/expected_output | "each fact file carries the sha256 of the prompt of every eval it covers, so editing such a prompt fails" (`README.md:255`) | Only the prompt is bound; assertions can drift from the facts (D2) | Preventive (C5) | 88 |

## ADVERSARIAL SCAFFOLD FINDINGS
- Reviewer blind spots: arithmetic in prose assertions ("11 are excluded") is never executed; a reason file looks inert.
- Highest-risk claims: D1 (blocks every commit), D2 (eval grades the wrong count), D3.
- Multi-step traces: `NOT_COMPUTABLE:13` → `check.py:495` → exit 1 → `pre-commit:9` `|| exit 1` → every commit refused until line 13 is removed.
- Subtlety flags: `NOT_COMPUTABLE:13` reads like documentation but is enforced data.

### SUMMARY
- Domain: Data
- Claims: 5 verified, 3 in FAIL (3 defects), 0 falsified
- Survived: 2/3 stress tests passed
- Failure categories: 2 systemic patterns
- Invariants: 3 touched; I1 and I7 respected and enforced; I4 enforced but violated by the data
- Hypotheses: 1
- Hidden behaviors: 1
- Findings by type: 3 demonstrated defects, 0 preventive, 0 falsified
- Critical issues: 0 (preventive critical: 0)
- Pre-code: not applicable
- Executed: 0
- Recommendation: remove `NOT_COMPUTABLE:13` first. The repository's own gate fails on it.

---

# DOMAIN 4 — DOCUMENTATION (`README.md`, `CHANGELOG.md`, docstrings and messages)

## VERIFICATION DOMAIN
Documentation

## GROUND TRUTH
- The actual code (`scripts/*`), the manifest (`plugin.json`), the skill folder as it exists (`skills/adversarial-verify/SKILL.md`, `references/{pre-code,ux,execution}.md`, `evals/`, `examples/agent-trust.json`).
- `references/execution.md` (tree) for CHANGELOG lines 7, 8, 15.
- No version history (stated by the request): history claims stay hypotheses.

## INVARIANTS
| # | Invariant | Source | Touched by | Enforced by | Respected? |
|---|-----------|--------|------------|-------------|------------|
| I1 | Version agreement | `CHANGELOG.md:3`, `README.md:250` | `README.md:1`, `:125`; `CHANGELOG.md:10` | `check.py:212-241` (badges, entries, not prose) | Badge and entry: yes. **Prose at `README.md:125`: no** (Doc1) |
| I2/I3/I5 | as in Code | `README.md:251`, `:255` | README restates them | — | The README states them correctly; the code does not keep them (C2, C3, C4). The contradiction is counted once, in Code |

## DECOMPOSED CLAIMS
1. README badge version = skill version (`README.md:1`) — Deductive
2. "currently 4.1" (`README.md:125`) — Deductive
3. The first install recipe produces a working skill (`README.md:87-90`) — Deductive
4. Clone-and-copy installs the whole folder (`README.md:95-96`) — Deductive
5. The reference-file table matches SKILL.md (`README.md:111-115`) — Deductive
6. Repository checks bullets match check.py (`README.md:249-255`) — Deductive
7. Commands at `README.md:258-261` work as described — Deductive
8. Python ≥ 3.8 and nothing else for check.py (`README.md:247`) — Deductive
9. Node 22.6+ for strip-types (`README.md:247`, `:255`) — Deductive (external fact)
10. Trust Integration matches SKILL.md (`README.md:268-283`) — Deductive
11. Mutation-tool table cells are correct per the cited docs (`README.md:226-241`) — Abductive (external, not read)
12. CHANGELOG:3 "the first entry below" carries the version — Deductive
13. CHANGELOG:7-8 match `references/execution.md` — Deductive
14. CHANGELOG:14 sizes 57.3 → 46.4 kB, 62.5 kB — run-only
15. CHANGELOG:14 "No rule changed by the split" — Abductive (needs history)
16. CHANGELOG:14 check.py "covers the reference files … fails on a named file that does not exist or a file nobody names" — Deductive
17. CHANGELOG:15 rules are in execution.md — Deductive
18. CHANGELOG:24 check.py requires a file or reason from eval 29 on — Deductive
19. CHANGELOG evals cited (54, 55, 56, 57) exist and match — Deductive
20. Docstrings of check.py/check_facts.py match behavior — Deductive (contradictions counted in Code)
21. README domain table and techniques match SKILL.md — Inductive (sampled)
22. README "Propose project doc updates — TODO.md, SPEC.md, PLAN.md" matches SKILL Step 5 — Deductive

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Stale instructions / version mismatch (prose not covered by a check) | 3: `README.md:125` (4.1), `README.md:87-90` (single-file install), `CHANGELOG.md:3` (first entry) | `README.md`, `CHANGELOG.md` |
| Docs promise more than the code does | 4 (counted in Code: C1, C2, C3, C4): `README.md:250`, `:251` ×2, `:255` | `README.md`, docstrings |
| Missing completeness (list shorter than the source) | 1: `README.md:46` (Doc4) | `README.md` |

## VERIFICATION RESULTS
### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| 1 | Badge | `README.md:1` `skill-v4.2` = `SKILL.md:20`. Score 92 |
| 4 | Clone and copy | `README.md:96` `cp -r …/skills/adversarial-verify ~/.claude/skills/` copies `SKILL.md` and `references/`. Score 88 |
| 5 | Reference table | `README.md:113-115` = `SKILL.md:49-51` (conditions match). Score 90 |
| 6 | Checks bullets (except C1–C4 contradictions) | evals `README.md:249` = `check.py:163-207`; neutral `:252` = `check.py:140-142`; tables `:253` = `check.py:341-381`; references `:254` = `check.py:506-520`; facts `:255` = `check.py:457-501`. Score 85 |
| 7 | Commands | `README.md:258-259` flags exist (`check.py:419-421`); `:260` `python3 -m unittest scripts/test_check.py` (a file path is accepted by unittest); `:261` the symlink `../../scripts/pre-commit` from `.git/hooks/` resolves to `scripts/pre-commit`. Score 80 (the exec bit is HY-Doc3) |
| 8 | Python 3.8 | check.py uses `capture_output`/`text` (3.7), f-strings, `yield from`; no 3.9+ API found in `scripts/check.py`. Score 82 |
| 10 | Trust | `README.md:270-272` = `SKILL.md:466`. Score 88 |
| 13 | CHANGELOG 7-8 | `references/execution.md:48-52` (file, short part first, search, path:line, reconcile, unread is not evidence); `:57-64` (brief, rows, quote lookup, discard, rest read, cap 79). Score 88 |
| 16 | CHANGELOG 14 check.py claims | `check.py:140-142` (neutral/tables over refs), `:517-520`. Score 90 |
| 17 | CHANGELOG 15 | `references/execution.md:38` (no privilege raise), `:39` (never the working copy), `:40` (size first; exhausted memory is not measured), `:41` (storage tests on disk), `:42` (remove, report where). Score 88 |
| 18 | CHANGELOG 24 | `check.py:77`, `:497-501`. Score 90 |
| 19 | Evals cited | 54 `evals.json:671`, 55 `:685`, 56 `:697`, 57 `:711` cover what `CHANGELOG.md:7`, `:8`, `:15` say. Score 88 |
| 21 | Domains / techniques | `README.md:50-58` vs `SKILL.md:96-104`, `:133-138`; stress rule `README.md:72` vs `SKILL.md:290`; confidence bands `README.md:78` vs `SKILL.md:333-343`. Score 72 (Inductive, 3+ instances) |

### FALSIFIED HYPOTHESES
None.

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| Doc1 | `README.md:125` | `The plugin declares its version in .claude-plugin/plugin.json (currently 4.1), the same number as the skill's frontmatter and the badge above.` | Demonstrated defect | low | `plugin.json:3` says 4.2, `SKILL.md:20` says 4.2, `README.md:1` badge says 4.2. The sentence contradicts itself and the manifest. `check.py:217` reads only badges, so it cannot catch this | Deductive | 95 | Drop the number ("the same number as …"), or write 4.2 and extend `check_version` to `currently X` |
| Doc2 | `README.md:87-90` | `mkdir -p ~/.claude/skills/adversarial-verify` / `cp skills/adversarial-verify/SKILL.md ~/.claude/skills/adversarial-verify/` | Demonstrated defect | medium | It copies only `SKILL.md`. `SKILL.md:49-51` sends the verifier to `references/*.md`, which are then missing. `README.md:117` itself says "`SKILL.md` alone would send the verifier to files that are not there". The first recipe shown produces the broken install the README warns against | Deductive | 95 | `cp -r skills/adversarial-verify ~/.claude/skills/` (as in `:96`) |
| Doc3 | `CHANGELOG.md:3` | `The version is the same in … the first entry below` | Demonstrated defect | low | The first entry below is `## Unreleased` (`:5`), which has no version. The check uses the first **numbered** entry (`check.py:11-12`, `:237`), and the README says "newest entry" (`README.md:250`) | Deductive | 88 | "… and the first numbered entry below" |
| Doc4 | `README.md:46` | `Propose project doc updates — TODO.md, SPEC.md, PLAN.md (with user confirmation)` | Demonstrated defect (incomplete list) | low | `SKILL.md:462` also checks `CHANGELOG.md`, `ADR/` and agent instruction files. A reader expects no CHANGELOG proposals | Deductive | 82 | List them, or say "project docs (e.g. …)" |

## STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|
| S-Doc1 | Time Travel | Claim 1 (badge) at the next release 4.3 | yes | 85 | The badge is checked (`check.py:217-225`); the prose number at `:125` is not, as Doc1 shows |
| S-Doc2 | Scale Shift | Claim 5 at 10× reference files | yes | 85 | The check (`check.py:519-520`) forces each file to be named in SKILL.md; the README table would drift, but nothing breaks at runtime |
| S-Doc3 | Existence Question | `README.md:87-90` first install recipe | no | 90 | Deleting it loses nothing: `:95-96` and `:99-107` cover the install correctly, and keeping it causes Doc2 |

## HYPOTHESES
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| HY-Doc1 | `CHANGELOG.md:14` gives 57.3 kB → 46.4 kB core, 62.5 kB with all three files | The figures are byte counts of SKILL.md (now and before the split) and SKILL+refs | They count something else (with frontmatter, kB vs KiB) or are stale after later edits ("Unreleased" changed `execution.md`) | `wc -c skills/adversarial-verify/SKILL.md skills/adversarial-verify/references/*.md` |
| HY-Doc2 | `CHANGELOG.md:14` "No rule changed by the split" | True (a move word for word) | A rule was reworded in the move | Diff of SKILL.md before the split vs SKILL.md + references (history not available here) |
| HY-Doc3 | `README.md:261` symlinks the hook | `scripts/pre-commit` has the exec bit in git (mode 100755) | Mode 100644: git ignores the hook with a warning | `git ls-files -s scripts/pre-commit` |
| HY-Doc4 | `README.md:226-241` cells "come from the tool's official documentation, read on 2026-10-21" | They match the docs | A flag was renamed since then (the README itself warns) | Open the 15 linked documentation pages (not done: outside `./tree`) |
| HY-Doc5 | `README.md:247` "node 22.6 or later" | `--experimental-strip-types` first shipped in Node 22.6.0 | A later minor version is needed for some syntax used in `53.ts` | `node --version` and `python3 scripts/check_facts.py 53` on Node 22.6 |

## HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type | Confidence |
|---|----------|-----------|--------|------|------------|
| HB-Doc1 | `README.md:250` | "Version: … every skill badge in the README" | Only badges are parsed, and only the first one (C1); prose versions are never parsed | Demonstrated (C1, Doc1) | 92 |

## ADVERSARIAL SCAFFOLD FINDINGS
- Reviewer blind spots: two install recipes that look like alternatives, where only one is correct; a version number in prose next to a checked badge.
- Highest-risk claims: Doc2 (a broken install that follows the first instructions), C2/C3/C4 as promised by `README.md:251`, `:255`, Doc1.
- Multi-step traces: user follows `README.md:88-89` → only `SKILL.md` installed → `SKILL.md:51` asks to read `references/execution.md` → file missing → `SKILL.md:53` "say so at the top of the report", so every approved run starts degraded.
- Subtlety flags: `README.md:125` "(currently 4.1)".

### SUMMARY
- Domain: Documentation
- Claims: 13 verified, 4 in FAIL (4 defects), 0 falsified (plus 4 README promises contradicted by code, counted in Code)
- Survived: 2/3 stress tests passed
- Failure categories: 3 systemic patterns
- Invariants: 2 groups touched; I1 respected by the badge, not by prose; I2/I3/I5 stated correctly by the docs and broken by the code
- Hypotheses: 5
- Hidden behaviors: 1
- Findings by type: 4 demonstrated defects, 0 preventive, 0 falsified
- Critical issues: 0
- Pre-code: not applicable
- Executed: 0
- Recommendation: fix Doc2 and Doc1. The README's description of the checks is accurate as intent, and the code has to catch up (C1–C4).

---

## OUT OF SCOPE (listed, not verified)
- `skills/adversarial-verify/SKILL.md:20`, `:49-51`, `:439`, `:462` and `references/execution.md` were read as ground truth only.
- `skills/adversarial-verify/examples/agent-trust.json` is named by no file in scope. Not read.

---

## CROSS-DOMAIN SUMMARY
- Domains: Code, Tests, Data, Documentation (UX not in the target, as stated in INTAKE)
- Claims: 53 verified, 22 in FAIL (15 demonstrated defects, 7 preventive measures), 3 falsified hypotheses
- Survived: 9/14 stress tests passed
- Failure categories: 13 rows across domains, 6 distinct patterns (missing completeness, silent fallthrough, stale state, assumed environment, test-environment artifact, tautological test)
- Invariants: 9 found; 9 touched; enforced and biting: I4, I6, I7, I8 (code), I9; not, or only partly: I1 (first badge only, prose unchecked), I2 (`=` terms), I3 (multi-character joins), I5 (toolchain skip); I4 is currently **violated by the data** (D1)
- Hypotheses: 11 requiring further investigation
- Hidden behaviors: 8 detected
- Findings by type: 15 demonstrated defects, 7 preventive measures, 3 falsified hypotheses (0 conditionally)
- Critical issues: 0 demonstrated defects of critical severity (preventive critical: 0). High: D1 (the gate fails on the tree, every commit blocked), C2 (private terms printed)
- Changes that touch several domains: the private-term guarantee (Code C2, C3 ↔ Documentation `README.md:251` ↔ Tests `test_check.py:286`, `:341-344`); the facts gate (Code C4 ↔ Data D1 ↔ Tests T2 ↔ Documentation `README.md:255`); the version rule (Code C1 ↔ Documentation Doc1, Doc3 ↔ Tests `test_check.py:171-173`)
- Pre-code: not applicable (no proposal of work not yet done)
- Executed: nothing was run
- Proposed: 9 checks and 13 writes awaiting an answer
- Recommendation: not ready for release as 4.2 "clean". Fix D1 first (one line); then C2, C4, C3, C1 with their tests (T1, T2); then the doc fixes. The eval-fact arithmetic is sound by hand computation, except one value close to a rounding boundary (HY-T1) that needs a run.

## PROPOSED EXECUTABLE CHECKS
| # | Claim | Confidence now | Check (command, test or query) | Confirms if | Refutes if | Cost and side effects | Status |
|---|-------|----------------|--------------------------------|-------------|------------|-----------------------|--------|
| P1 | D1: check.py fails on the tree | 93 (traced; outcome is a run) | `python3 scripts/check.py` | `ERROR …/NOT_COMPUTABLE: eval 52 has a fact file and a reason not to have one`, exit 1 | Exit 0 | Reads the tree, runs `git ls-files` (read-only); writes nothing | proposed |
| P2 | HY-T2 hashes match prompts; tables of README/SKILL/refs pass | 60 | Same run as P1 | No "prompt changed" and no "table row" errors | Either error appears | Same as P1 | proposed |
| P3 | Predicted red tests: C1 (`test_second_badge_mismatch`), C2 (`test_whole_word_term_glued_in_output_is_still_masked`), C3 (`test_two_words_joined_any_way`, two-space subtest), D1 (every `assert_passes` test); T1 stays green | 75 | `python3 -m unittest -v scripts/test_check.py` (with `CHECK_PRIVATE_TERMS` unset, T3) | Those tests fail with those messages | They pass | Creates temp copies of the repo under the system temp dir, runs `git init/commit` there and runs the fact files (needs rustc, node ≥ 22.6). Does not touch the working copy | proposed |
| P4 | C4/T2: missing toolchain is skipped, exit 0 | 92 | `PATH=<dir with python3 only> python3 scripts/check_facts.py 52 53` | Prints `skip 52.rs…`, `skip 53.ts…`, `2 fact file(s), 0 failed`, exit 0 | FAIL lines, exit 1 | Runs nothing else; writes a temp dir only | proposed |
| P5 | Fact files true, incl. HY-T1 (48.py, 3.23) | 72–79 | `python3 scripts/check_facts.py` | `13 fact file(s), 0 failed` | Any `FAIL` | **Executes the fact files** (Python, a Rust binary compiled into a temp dir, Node); reads `facts/` | proposed |
| P6 | HY-Doc1 sizes | 50 | `wc -c skills/adversarial-verify/SKILL.md skills/adversarial-verify/references/*.md` | ≈ 46.4 kB and ≈ 62.5 kB total | Different figures | Read-only | proposed |
| P7 | HY-Doc3 exec bit | 50 | `git ls-files -s scripts/pre-commit` | `100755` | `100644` | Read-only | proposed |
| P8 | HY-Doc4 mutation-tool table | 50 | Open the 15 documentation links of `README.md:230-239` and compare each cell | Every cell matches | A flag or behavior differs | Network reads of public documentation pages; no writes | proposed |
| P9 | Strength of the tests on the risky lines of `check.py` | — | Mutation probe, 4 hand mutations on `check.py:90`, `:223`, `:400`, `:495` (e.g. `?`→`*` reverted, `[:1]`→`[:2]`, `substring=True`, delete the "both" error), running `test_check.py` for each | Each mutant is killed by a named test | A mutant survives | 4 mutants × the full suite (≈ 90 tests, each copying the repo). It **mutates a separate copy** of the repository, restored after each mutant, and the working copy is untouched. Suggestion: keep that copy in a memory-backed filesystem (tmpfs / RAM disk). It needs your consent to create or mount one, separate from this probe. The repo is text only (a few MB at most), far below any free memory, and the copy is removed at the end. No test here has the storage itself as its subject | proposed |

Proposed writes (none made):
1. `skills/adversarial-verify/evals/facts/NOT_COMPUTABLE:13`: delete the line `52: the compiler is not installed on every machine` (D1).
2. `scripts/check.py:400`: `pats = term_patterns(terms, substring=True)` (C2).
3. `scripts/check.py:90`: `SEP = r"[\W_]*"` (C3). Update `README.md:251` and `check.py:16-17` with what exactly is joined.
4. `scripts/check.py:223`: `for b in badges:` (C1).
5. `scripts/check_facts.py:91-93`: count a missing toolchain as a failure (`FAIL {name}: toolchain not found`, `failed += 1`) (C4).
6. `scripts/check.py:474-482`: hash prompt + expected_output + assertions, and update the 13 fact-file hashes after re-checking (C5).
7. `scripts/check.py:484-494`: error on a reason for a non-existent or fact-less eval (C6). In `:226-241`, catch `OSError` (C8).
8. `scripts/test_check.py:479`: `self.assert_fails(r, "orphan.md", "never named in SKILL.md")` (T1). `:575-578`: assert no `skip` line, plus a new test with `rustc`/`node` hidden from `PATH` (T2). `:43`: `env.pop("CHECK_PRIVATE_TERMS", None)` (T3). `:337`: fix the comment (T7). `:351`: skip when symlinks cannot be created (T6).
9. `skills/adversarial-verify/evals/evals.json:705`: "11 are excluded" becomes "12 are excluded" (D2). `:249`: the current summary line from `SKILL.md:439` (D3).
10. `skills/adversarial-verify/evals/facts/_parse_day.py:1`: name 35.py too (T5).
11. `README.md:87-90`: replace with `cp -r skills/adversarial-verify ~/.claude/skills/` (Doc2). `:125`: drop "(currently 4.1)" or write 4.2 (Doc1). `:46`: complete the list (Doc4).
12. `CHANGELOG.md:3`: "the first numbered entry below" (Doc3).
13. Step 5, project discovery: `CHANGELOG.md` exists. Proposed: under `## Unreleased`, add one entry for the fixes above (D1, C1–C4, T1–T2, D2, Doc1–Doc2). I did not find `TODO.md`, `SPEC.md`, `PLAN.md`, `ADR/`, `.claude/` or `AGENTS.md` in `./tree` (full Glob listing of the tree), so nothing is proposed there.

**Which of the checks P1–P9 (P9 with or without the memory-backed filesystem) do you approve, and which of the writes 1–13 should I make? Nothing runs and nothing is written without your answer.**
