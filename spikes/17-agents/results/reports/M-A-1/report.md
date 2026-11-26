# Adversarial verification: scripts/check.py, scripts/check_facts.py, scripts/pre-commit, scripts/test_check.py

**Cost estimate (large request, cost accepted, every choice settled, so the verification ran without asking first):** 4 files in scope (531 + 117 + 18 + 621 = 1,287 lines), 5 domains (Code, Tests, Documentation, Data, UX), about 70 claims, nothing run.

## INTAKE
- **Target:** every domain detected in the four files: **Code** (check.py, check_facts.py, pre-commit), **Tests** (test_check.py, plus pre-commit as the CI-like gate), **Documentation** (module docstrings, usage text, comments, error messages), **Data** (the file formats these scripts define and parse: evals.json shape, `facts/NOT_COMPUTABLE`, the `prompt-sha256:` header, `.check-private-terms`), **UX** (command-line and terminal output). Set by the request.
- **Depth:** standard (set by the request).
- **Scope:** the whole of the four files, with no diff and no history (set by the request). Other files in `./tree` were read only as ground truth.
- **Execution mode:** reasoning only (set by the request). Nothing was run. Every result below comes from tracing the code. Any claim that only a run can decide is capped at 79 and listed under PROPOSED EXECUTABLE CHECKS.
- Reference files read: `references/ux.md`, because UX is in the target. `pre-code.md` was not needed because no artifact proposes future work. `execution.md` was not needed because nothing was approved to run.
- To change any of this, say for example "approved: run the unit tests" or "deep".

---

# DOMAIN 1: CODE (scripts/check.py, scripts/check_facts.py, scripts/pre-commit)

## VERIFICATION DOMAIN
Code

## GROUND TRUTH
- The module docstring of scripts/check.py:2-50, which is the spec of the seven checks.
- The docstring of scripts/check_facts.py:2-18.
- The comments in scripts/pre-commit:2-5 and 10-11.
- README.md:244-263, the "Repository checks" section. It is user-facing documentation of the same scripts.
- The tests in scripts/test_check.py, which show the intended behavior.
- The repository data the scripts read: README.md:1 (the only `badge/skill-v` badge), CHANGELOG.md:5, 10 (`## Unreleased`, then `## 4.2`), .claude-plugin/plugin.json:3, .gitignore:1-2, skills/adversarial-verify/evals/facts/NOT_COMPUTABLE:1-12, the fact files 37.py, 38.py, 40.py, 49.py, 51.py, 52.rs and 53.ts, and evals.json:380-381 and 462-463.

## INVARIANTS
**Where I looked:** scripts/check.py:2-50, scripts/check_facts.py:2-14, scripts/pre-commit:2-11, scripts/test_check.py:1-5, README.md:244-263, skills/adversarial-verify/evals/facts/NOT_COMPUTABLE:1-3. The tree has no CLAUDE.md, AGENTS.md or CONTRIBUTING.md (file listing of ./tree).

**Result:** 9 invariants found. All 9 are touched, because these files are the mechanisms that enforce them.

| # | Invariant | Source | Touched by | Enforced by (file:line / test name) | Bites on changed path? |
|---|-----------|--------|------------|-------------------------------------|------------------------|
| I1 | evals.json: 4 keys, integer ids 1..n in order, tags from 21 | scripts/check.py:6-9 | check_evals | scripts/check.py:163-207; EvalsTest (scripts/test_check.py:104-163) | **Yes** |
| I2 | SKILL version = **every** README skill badge = plugin.json = newest CHANGELOG entry | scripts/check.py:10-12, README.md:249 | check_version | scripts/check.py:212-241; `test_second_badge_mismatch` | **No, for every badge after the first** (scripts/check.py:223), see FAIL C-F5 |
| I3 | No private term in content or names; the parts may be joined by any non-alphanumeric characters | scripts/check.py:13-18, README.md:250 | check_private | scripts/check.py:259-323; PrivateTest | **Partly:** at most one separator character between parts (scripts/check.py:90), see C-F2 |
| I4 | Terms are never printed; any output line containing one is masked | scripts/check.py:22-23, test_check.py:4-5, README.md:250 | mask | scripts/check.py:397-414; `test_whole_word_term_glued_in_output_is_still_masked` | **No, for `=` terms** (scripts/check.py:400), see C-F1 |
| I5 | Tables well-formed; fenced blocks skipped | scripts/check.py:30-33 | check_tables | scripts/check.py:353-381; TablesTest | **Partly:** fences close on any fence character (scripts/check.py:363-366), see C-F6 |
| I6 | Every stated fact has a fact file or a reason, bound by sha256 and true when run | scripts/check.py:34-38, README.md:254 | check_facts, check_facts.py | scripts/check.py:457-501; check_facts.py:76-113; FactsTest | **Partly:** the hash binding bites, but a missing toolchain skips with exit 0 (check_facts.py:91-93), see C-F4 |
| I7 | Every `references/*.md` named exists and every file is named in SKILL.md | scripts/check.py:39-44 | check_references | scripts/check.py:506-520; ReferencesTest | **Yes** |
| I8 | The hook runs `--strict --staged`, so it fails without private terms | README.md:260, scripts/pre-commit:5 | pre-commit | scripts/pre-commit:9 | **No:** `--strict` is not passed, see C-F3 |
| I9 | A missing toolchain is an error, never a silent skip | scripts/check_facts.py:8, README.md:254 | check_facts.py | scripts/check_facts.py:90-93 | **No**, see C-F4 |

## DECOMPOSED CLAIMS
1. C1: evals.json is checked for type, key set, integer non-bool ids, duplicates and consecutive order. Mode: Deductive.
2. C2: assertions of eval ≥ 21 must start with `[substance]`/`[format]` followed by text. Mode: Deductive.
3. C3: the SKILL.md version matches **every** skill badge in the README. Mode: Deductive.
4. C4: the plugin.json `version` must be a string equal to the SKILL version. Mode: Deductive.
5. C5: the first `## <version>` heading of CHANGELOG.md is compared, and non-version headings are skipped. Mode: Deductive.
6. C6: the parts of a term may be joined by any run of non-alphanumeric characters, or by nothing. Mode: Deductive.
7. C7: a term prefixed with `=` matches only as a whole word. Mode: Deductive.
8. C8: strings in JSON files are scanned after escapes are decoded. Mode: Deductive.
9. C9: non-UTF-8 files are still scanned (UTF-16 with a BOM, otherwise Latin-1). Mode: Deductive.
10. C10: no output line ever shows a private term. Mode: Deductive.
11. C11: with no terms the check says so, and `--strict` fails. Mode: Deductive.
12. C12: fenced code blocks are skipped by the table check. Mode: Deductive.
13. C13: escaped pipes and pipes in code spans are not counted as separators. Mode: Deductive.
14. C14: fact files: orphan files are rejected, a file plus a reason is rejected, `(Facts` without a file or reason is rejected, and the prompt hash is enforced. Mode: Deductive.
15. C15: reference names resolve, and every reference file is named in SKILL.md. Mode: Deductive.
16. C16: `--staged` checks exactly the index content, and the temporary directory is always removed. Mode: Deductive.
17. C17: every run ends with the masked report and summary (errors are collected, no traceback). Mode: Deductive.
18. C18: a missing toolchain is an error in check_facts.py. Mode: Deductive.
19. C19: a fact file without any assert or raise outside comments and strings fails. Mode: Deductive.
20. C20: a fact file that passes has actually executed an assertion. Mode: Deductive.
21. C21: the last output line must be `ok <id>`. Mode: Deductive.
22. C22: selecting no files exits non-zero. Mode: Deductive.
23. C23: Python fact files cannot have their asserts stripped by the environment. Mode: Deductive. Moved to FALSIFIED HYPOTHESES.
24. C24: the fact runner always terminates. Mode: Deductive.
25. C25: the pre-commit hook runs check.py with `--strict`. Mode: Deductive.
26. C26: the hook checks exactly the staged content, for both check.py and the facts. Mode: Deductive.
27. C27: the hook runs the facts whenever the staged change touches `skills/adversarial-verify/evals/`. Mode: Deductive and Abductive.
28. C28: the hook removes its temporary directory. Mode: Deductive.
29. C29: the CHANGELOG check reads the newest entry, whatever the heading style. Mode: Deductive (from stress S6).
30. C30: bool ids are rejected even though bool is a subclass of int. Mode: Deductive. Moved to FALSIFIED HYPOTHESES.

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Missing completeness (a documented rule enforced only partly) | 5: first badge only (scripts/check.py:223); one separator character (scripts/check.py:90); fence character stored but never compared (scripts/check.py:364-366); masking not in substring mode (scripts/check.py:400); `## v4.3` headings skipped (scripts/check.py:237) | scripts/check.py |
| Silent fallthrough | 3: toolchain "skip" with exit 0 (scripts/check_facts.py:91-93); hook drops fact output on success (scripts/pre-commit:15-17); a dead-code `assert` counts as an assertion (scripts/check_facts.py:50) | scripts/check_facts.py, scripts/pre-commit |
| Doc-to-code drift on a safety gate | 2: `--strict` promised but not passed (scripts/pre-commit:5 vs :9; README.md:260); "never a silent skip" (scripts/check_facts.py:8) | scripts/pre-commit, scripts/check_facts.py |
| Unguarded input (crash instead of report) | 2 groups: missing SKILL/README/plugin/CHANGELOG (scripts/check.py:214, 217, 227, 237); `"evals": null` (scripts/check.py:460-463) | scripts/check.py |
| Assumed environment | 2: a single-character separator breaks on CRLF line breaks (scripts/check.py:90); git `core.quotePath` quoting in the hook grep (scripts/pre-commit:12) | scripts/check.py, scripts/pre-commit |

## OUT OF SCOPE (listed, not verified)
- README.md:260 states that the hook "runs --strict --staged before every commit". This is the same drift as C-F3, seen from the docs side.
- README.md:254 states that check_facts "fails ... if a needed toolchain ... is missing". This is the same drift as C-F4.
- README.md:250 states "how the parts of a term are joined (space, hyphen, underscore, line break, or nothing)". With CRLF files the line break is two characters, so this is the same as C-F2.
- README.md:254 says "each fact file carries the sha256 of the prompt of every eval it covers", which implies one file can cover several evals. The code binds exactly one file to one eval (scripts/check.py:468-478).

## VERIFICATION RESULTS
### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| C1 | evals shape | scripts/check.py:170-207. A non-dict entry → error, then continue. Extra and missing keys are reported separately (:180-184). A non-int id → error and it is left out of `ids` (:186-188). Duplicates (:203-205) and order (:206-207) are both reported. Tests at scripts/test_check.py:109-135. |
| C2 | tags from 21 | scripts/check.py:74-75, :198-202. `elif`, so an empty assertion gets a single error. The regex needs `\s+\S` after the tag. The boundary is tested on both sides at scripts/test_check.py:149-159. |
| C4 | plugin version | scripts/check.py:226-236. A non-dict or non-str version → "no version (a string)". A float 4.1 is covered at scripts/test_check.py:202-206. |
| C5 | newest CHANGELOG entry | scripts/check.py:237. `^## +([0-9]…)` skips `## Unreleased` (CHANGELOG.md:5) and finds `## 4.2` (CHANGELOG.md:10) = plugin.json:3 = README.md:1. |
| C7 | `=` whole-word | scripts/check.py:265, 275. The lookarounds `(?<![^\W_])`/`(?![^\W_])` reject a neighbouring letter or digit. Tested at scripts/test_check.py:252-262. |
| C8 | JSON decoded strings | scripts/check.py:279-289, 313-323. Keys and values are both yielded. `elif` avoids a double report. |
| C9 | non-UTF-8 scanned | scripts/check.py:112-122. Decoding never raises: Latin-1 accepts every byte. |
| C11 | no terms → said / strict fails | scripts/check.py:294-298. An empty env value `" , "` gives `[]` after the strip filter at :256. |
| C13 | escaped pipes / code spans | scripts/check.py:345 replaces code spans first, then `\|`. |
| C14 | fact binding | scripts/check.py:465-501. Orphan → :470-471. Hash missing or different → :479-482. File plus reason → :495-496. `(Facts` without either → :497-501. Fixture preconditions hold: evals.json:381 (id 30 states facts), NOT_COMPUTABLE:4. |
| C15 | references | scripts/check.py:506-520. Names are collected from SKILL.md and from every reference file. Only SKILL.md names count as "named" (:515-516). |
| C16 | staged = index content; temporary directory removed | scripts/check.py:386-394 (`checkout-index -a` into tmp, `ls-files` for the list), :427-433, and `finally: rmtree` at :438-440. In the hook, git sets `GIT_INDEX_FILE` for `commit -a`/paths, and the child `git` inherits it, so the to-be-committed index is the one read. |
| C19 | no assertion → FAIL | scripts/check_facts.py:42-51, 95-98. Python uses an AST walk, so asserts in comments and strings do not count (tested at scripts/test_check.py:595-602). |
| C21 | `ok <id>` last line | scripts/check_facts.py:106-107. `out[-1:]` handles empty output (`[] != [...]` → FAIL). |
| C22 | no files → exit 1 | scripts/check_facts.py:113. |
| C26 | hook checks staged content | scripts/pre-commit:9 (`--staged`), :14-15 (`checkout-index -a --prefix="$tmp/"`, `--root "$tmp"`). |
| C28 | hook removes tmp | scripts/pre-commit:14 (on failure), :16 (always after the run). There is no `set -e`, so :16 runs even when :15 fails. Only an interrupt (signal) leaves it behind, because there is no `trap`. |

### FALSIFIED HYPOTHESES
| # | Location | Suspected defect | Check (quote) | Status (falsified / conditionally) | Could it have failed? (how shown, or the check that would complete it) | Paths not covered | Mode | Confidence |
|---|----------|------------------|-------|------------------------------------|------------------------------------------------------------------------|-------------------|------|------------|
| C30 | scripts/check.py:186 | `True` accepted as id 1 because bool subclasses int | `if type(i) is not int:  # bool is an int subclass: reject it` | falsified | Yes. An `isinstance` check would let `True` through, while `type(...) is` rejects it. `test_boolean_id` (scripts/test_check.py:125-127) asserts the error. | Bool ids in check_facts (scripts/check.py:463) still go into the id set, but they only matter after check 1 has already failed. | Deductive | 90 |
| C23 | scripts/check_facts.py:57 | `PYTHONOPTIMIZE` in the environment strips the `assert` statements of the fact files, so false facts pass | `[sys.executable, "-E", "-s", path]` | falsified | Yes. Without `-E` the child would honour `PYTHONOPTIMIZE` (Python documents `-E` as ignoring all `PYTHON*` variables), and every fact file's checks are bare `assert`s (for example 38.py:17-21). | A runner started with `python -O check_facts.py` does not pass `-O` to the child, so this path is also covered. | Deductive | 85 |

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| C-F1 | scripts/check.py:399-400 | `# substring patterns: when hiding output, err on the side of hiding too much` / `pats = term_patterns(terms)` | Demonstrated defect | **high** | `term_patterns` defaults to `substring=False` (:259, :265), so an `=acme` term is masked only as a whole word. With `CHECK_PRIVATE_TERMS="=acme"` and an eval key `acmelabs`: check 3 does not flag it (whole word), check 1 emits `unexpected keys ['acmelabs']` (:182), and `mask` does not match it, so the private term is printed to the terminal and the CI log. This breaks I4. It is exactly the case of `test_whole_word_term_glued_in_output_is_still_masked` (scripts/test_check.py:341-344). | Deductive | 95 | `pats = term_patterns(terms, substring=True)` |
| C-F2 | scripts/check.py:90 | `SEP = r"[\W_]?"  # anything that is not a letter or digit, possibly nothing` | Demonstrated defect | **high** | `?` allows at most one separator character. "Acme  Labs" (two spaces), "Acme, Labs", "Acme - Labs", and "Acme\r\nLabs" (a line break in any CRLF file) are not detected. This contradicts scripts/check.py:16-17 ("joined by anything… line breaks"). The `f"{a.upper()}  {b}"` subtest (scripts/test_check.py:286) uses two spaces and should be red. On Windows the `"\n"` subtest is also written as `\r\n` by text-mode `append` (scripts/test_check.py:84-85). | Deductive | 92 | `SEP = r"[\W_]*"`. The pattern stays linear because the parts are literals. |
| C-F3 | scripts/pre-commit:9 | `"$py" -I "$root/scripts/check.py" --staged --root "$root" \|\| exit 1` | Demonstrated defect | **high** | The comment at :5 and README.md:260 promise `--strict`. In a fresh clone `.check-private-terms` is gitignored (.gitignore:1) and therefore absent. With no env var, check 3 only warns (scripts/check.py:297), exit 0, and the commit goes through with private names unchecked. This breaks I8. | Deductive | 95 | Add `--strict` to :9. |
| C-F4 | scripts/check_facts.py:91-93 | `print(f"skip {name}: toolchain not found")` / `continue` | Demonstrated defect | medium | Without `rustc` (or `node`), 52.rs (or 53.ts) is skipped, `failed` stays 0, and the exit code is 0. This contradicts :8 "A missing toolchain is an error, never a silent skip", and README.md:254. In the hook the output is printed only on failure (scripts/pre-commit:17), so the skip is fully silent there and a false Rust or TS fact can be committed. | Deductive | 95 | `print(f"FAIL {name}: toolchain not found ({...})"); failed += 1; continue` |
| C-F5 | scripts/check.py:223 | `for b in badges[:1]:` | Demonstrated defect | medium | Only the first `badge/skill-v` badge is compared. The docstring (:10, "every skill badge") and README.md:249 say every badge. Appending `![old](…/badge/skill-v2.0-blue)` passes, so `test_second_badge_mismatch` (scripts/test_check.py:171-173) should be red. This breaks I2. | Deductive | 95 | `for b in badges:` |
| C-F6 | scripts/check.py:363-366 | `if fence is None: fence = f.group(1)[0]` / `else: fence = None` | Demonstrated defect | low | The opening fence character is stored but never compared, so any fence line closes any block. Inside a ```` ``` ```` block, a `~~~` line closes it. The rest of the code block is then checked as Markdown (false errors), and the real closing ```` ``` ```` reopens a "fence", so every real table after it is skipped (missed errors). CommonMark requires the same character, at least as long. | Deductive | 90 | Store the full run (`f.group(1)`) and close only on a line `^{char}{len,}\s*$` with the same character and at least the same length. |
| C-F7 | scripts/check.py:460-463 (also :214, :217, :227, :237, :512) | `evals = json.loads(...).get("evals", [])` … `ids = {e.get("id") for e in evals …}` | Demonstrated defect | low | With `{"evals": null}`, check 1 reports "no 'evals' list". Then check_facts iterates `None` (`TypeError` outside the `try`), the run dies with a traceback, every collected error is lost, and no summary is printed. The same happens when SKILL.md, README.md, CHANGELOG.md or plugin.json is missing (`read_text` raises `FileNotFoundError`, and only check_evals catches `OSError`). It fails closed (exit 1). | Deductive | 88 | `if not isinstance(evals, list): return` after :460. Wrap each `run_checks` call so that an exception becomes `rep.error(check, …)`. |
| C-F8 | scripts/check_facts.py:50 | `return any(isinstance(n, (ast.Assert, ast.Raise)) for n in ast.walk(tree))` | Preventive measure | low | Any assert anywhere counts, including one in a function that is never called or under `if False:`. A file `def _(): assert 0` plus `print('ok 49')` passes the "asserts something" rule while asserting nothing at run time. Likelihood: low (it needs a careless edit, and review is expected per scripts/pre-commit:11). | Deductive | 85 | State the limit in the docstring, or require at least one module-level `assert` (`tree.body`). |
| C-F9 | scripts/check_facts.py:100 | `r = subprocess.run(step, cwd=FACTS, capture_output=True, text=True)` | Preventive measure | low | There is no `timeout`. A fact file with an infinite loop, or a hung `rustc`/`node`, blocks the pre-commit hook forever. Likelihood: low. | Deductive | 85 | `timeout=120`, then `TimeoutExpired` → FAIL. |
| C-F10 | scripts/pre-commit:12 | `git diff --cached --name-only \| grep -q '^skills/adversarial-verify/evals/'` | Preventive measure | low | With git's default `core.quotePath`, a path with non-ASCII characters is printed quoted (`"skills/…\303\251.py"`). It does not start with `skills/`, so the fact run is not triggered. Likelihood: low (all current names are ASCII). | Abductive (git quoting behaviour recalled, not verified in ./tree) | 65 | `git -c core.quotePath=false diff --cached --name-only -z \| tr '\0' '\n' \| grep …` |
| C-F11 | scripts/check.py:237 | `re.search(r"^## +([0-9][0-9.]*)\b", …)` | Preventive measure | low | From stress S6. If someone writes the next entry as `## v4.3` or `## [4.3]`, the regex skips it and compares the old `## 4.2`, so a stale version passes silently. Likelihood: medium (both styles are common). | Deductive | 85 | Take the first `## ` heading that is not `Unreleased`, and error if it does not parse as a version. |

## STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|
| S1 | Scale Shift (zero) | C1, with an empty evals list | yes | 90 | `not evals` → "no 'evals' list" (scripts/check.py:171-173). An empty facts dir → `[]` (scripts/check.py:465). |
| S2 | Time Travel | C14, when the next developer adds eval 60 with `(Facts` | yes | 88 | Fails until a file or reason exists (scripts/check.py:497-501). Editing the prompt later fails on the hash (:481-482). |
| S3 | Existence Question | scripts/check.py:301 (skip the terms file by basename) | yes | 80 | Remove it, and in the `os.walk` fallback (:153-158) the gitignored terms file would be scanned and fail on itself. The skip is needed. It is broader than needed (any depth), but .gitignore:1 also ignores the file at any depth. |
| S4 | Requirement Inversion | C2, with the boundary moved (TAGGED_FROM 21 → 20) | yes | 85 | Both sides are locked by tests: scripts/test_check.py:149-153 (21 must fail) and :155-159 (20 must pass). |
| S5 | Scale Shift (empty output) | C21 | yes | 88 | `out[-1:]` on an empty list → `[]` ≠ `["ok N"]` → FAIL, with no IndexError (scripts/check_facts.py:106-107). |
| S6 | Time Travel | C5, six months later, with the heading style changed | **no** | 85 | See C-F11. |
| S7 | Scale Shift (10x separators) | C6 | **no** | 92 | See C-F2. Two or more separator characters defeat it. |

## HYPOTHESES
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| H1 | scripts/pre-commit:7-8 prefers `python3`. scripts/check.py:50 says `py -3` on Windows. | On Windows, `python3` resolves to the Microsoft Store alias stub, so `command -v` succeeds, the stub exits non-zero, and every commit is blocked. | Git for Windows' `sh` does not see the alias, or a real python3 is installed. | Run `command -v python3 && python3 -c 1; echo $?` in Git Bash on a stock Windows machine. |
| H2 | scripts/check.py:389-394 lists `ls-files` entries and reads them from the `checkout-index` copy. | A submodule (gitlink) is listed but not checked out, so "unreadable file, not checked" blocks every commit. | The repo has no submodules today, so this is latent only. | Add a submodule in a scratch repo, then run `check.py --staged`. |
| H3 | scripts/check.py:307-309 | In working-tree mode, a tracked file deleted from disk but not yet staged gives a false "unreadable file" error. | Intended: it reports what cannot be checked. | `rm README.md` in a scratch clone, then run check.py. |
| H4 | scripts/check_facts.py:62-63 writes the Rust binary as `52.rs.bin`. | On Windows, `CreateProcess` refuses or mis-resolves a PE file without `.exe`, so 52.rs FAILs there. | Windows runs PE images whatever their extension when given a full path. | Run `check_facts.py 52` on Windows with rustc. |
| H5 | scripts/pre-commit:9, 15 run the **working-tree** check.py and check_facts.py against the staged tree. | A staged-only change to the checkers is not what runs, so a broken checker can be committed while a good working copy runs. | Intentional (the checker should not judge itself). | Stage a breaking change to check.py, restore the working copy, then commit. |

## HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| HB1 | scripts/check.py:223 | every badge | first badge only | Demonstrated defect (C-F5) | 95 |
| HB2 | scripts/check.py:400 | "substring patterns" | whole-word patterns for `=` terms | Demonstrated defect (C-F1) | 95 |
| HB3 | scripts/check_facts.py:91-93 | "never a silent skip" | skip, exit 0 | Demonstrated defect (C-F4) | 95 |
| HB4 | scripts/check.py:364 | fence character tracked | stored, never compared | Demonstrated defect (C-F6) | 90 |
| HB5 | scripts/check.py:436-437 | `--staged` checks staged content | with an empty index, no check runs at all (not even strict) and the summary shows an empty list, exit 0 | none: an empty commit carries nothing to leak | 85 |
| HB6 | scripts/check.py:301 | the terms file is excluded | any file named `.check-private-terms` at any depth is excluded, even if force-added | none today (.gitignore:1) | 80 |

## ADVERSARIAL SCAFFOLD FINDINGS
- **Reviewer blind spots:** one-character idioms that read as correct: `[:1]` (scripts/check.py:223), `?` (:90), and a default argument left implicit (:400). The comments next to them say the opposite of what the code does.
- **Highest-risk claims:** C10 (masking, privacy leak), C25 (hook without `--strict`), C6 (separator).
- **Multi-step traces:** `=term` key in evals.json → check_evals prints the key (:182) → check_private stays silent (whole word) → mask uses whole-word patterns (:400) → term on stdout. Also: rustc missing → `skip` (check_facts.py:92) → exit 0 → hook discards `$out` (pre-commit:17) → a false fact is committed without trace.
- **Subtlety flags:** scripts/check.py:364 (dead variable), scripts/check.py:90 (the comment says "anything", the regex says one character).

### SUMMARY (Code)
- **Domain:** Code
- **Claims:** 18 verified, 11 in FAIL (7 defects, 4 preventive measures), 2 falsified
- **Survived:** 5 of 7 stress tests
- **Failure categories:** 5
- **Invariants:** 9 found, 9 touched. 2 bite fully (I1, I7), 3 bite partly (I3, I5, I6), 4 do not bite (I2, I4, I8, I9).
- **Hypotheses:** 5
- **Hidden behaviors:** 6 detected (4 of them problems)
- **Findings by type:** 7 demonstrated defects, 4 preventive measures, 2 falsified hypotheses (0 conditionally)
- **Critical issues:** 0. Three are of high severity: C-F1, C-F2, C-F3.

---

# DOMAIN 2: TESTS (scripts/test_check.py)

## VERIFICATION DOMAIN
Tests

## GROUND TRUTH
- The production code: scripts/check.py and scripts/check_facts.py, as traced above.
- The production configuration: the pre-commit path (scripts/pre-commit:9, 15, run through git, `--staged`, `-I`).
- The repository data: README.md:1, CHANGELOG.md:5-10, evals.json:381 and 462-463, NOT_COMPUTABLE:4, 38.py:21, 40.py:13, 49.py:12-14.
- The test bootstrap: `Base.setUp` and `run_check` (scripts/test_check.py:29-52).

**Invariants:** I4 and the test docstring rule "no private test term may ever be printed" (scripts/test_check.py:4-5) are enforced by `assert_no_leak` (:70-73), which every `assert_fails` calls (:62). It bites, but only in failing cases: `assert_passes` (:64-68) does not check for leaks. That is acceptable, because a pass prints no ERROR lines.

## DECOMPOSED CLAIMS
1. T1: `assert_fails` counts a failure only if the script ran to its summary, printed ERROR and the named tokens, and leaked nothing. Mode: Deductive.
2. T2: the suite is green on the repository as shipped. Mode: Deductive. This is run-only.
3. T3: `test_file_nobody_names` can fail. Mode: Deductive.
4. T4: the results do not depend on the developer's environment. Mode: Deductive.
5. T5: `test_runner_passes_on_the_repo` proves every fact file runs and passes. Mode: Deductive.
6. T6: every documented guarantee has a negative test. Mode: Deductive and Inductive.
7. T7: the tests are portable to Windows, which README.md:263 supports. Mode: Deductive.
8. T8: tests that need git skip without it. Mode: Deductive.
9. T9: the comments in tests describe what the test does. Mode: Deductive.
10. T10: both sides of the TAGGED_FROM boundary are tested. Mode: Deductive.
11. T11: every fixture precondition holds in the repo data. Mode: Deductive.
12. T12: the tests never touch the working repository, and the real private-terms file is not copied. Mode: Deductive. Moved to FALSIFIED HYPOTHESES.
13. T13: "only tracked files are scanned" is tested on the production path (git), not only on the `os.walk` fallback that every `Base` test uses. Mode: Deductive.

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Tautological test | 1 (scripts/test_check.py:479) | scripts/test_check.py |
| Test-environment artifact: changed defaults (inherited env) | 1 (scripts/test_check.py:43-45). It affects the 6 tests that pass `terms=None`: :320, :325, :329, :355, :360 | scripts/test_check.py |
| Test-environment artifact: different resources (toolchains) | 1 (scripts/test_check.py:575-578) | scripts/test_check.py |
| Missing negative tests | 5 guarantees untested (see T-F5) | scripts/test_check.py |
| Assumed environment (OS, git) | 2 (scripts/test_check.py:351, :502-505) | scripts/test_check.py |

## VERIFICATION RESULTS
### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| T1 | `assert_fails` is strict | scripts/test_check.py:54-62: non-zero exit, `"checked ("` in stdout, `"ERROR"`, every token, then `assert_no_leak`. A crash (C-F7) cannot pass as a failure because the summary is required. |
| T10 | boundary 20/21 | scripts/test_check.py:149-159. The precondition at :158 asserts that eval 20 is untagged. |
| T11 | fixtures hold | Index 36 is id 37, with "day > 31" (evals.json:462-463, ids consecutive per C1). 38.py:21 holds the edited string. 40.py:13 holds `print('ok 40')`. 49.py:12-14 holds exactly the 3 asserts the test removes. NOT_COMPUTABLE:4 starts with `30:`, and evals.json:381 shows that eval 30 states facts. README.md:1 is the only `badge/skill-v` badge. CHANGELOG.md:5 holds the first `\n## `. |
| T13 | tracked-only on the git path | `StagedTest.test_untracked_files_are_not_checked` (scripts/test_check.py:398-402) runs on a real git repo. Every other `Base` test uses the `os.walk` fallback (no `.git` in tmp, scripts/check.py:153-158), which scans more files than production. That is stricter, not weaker. |

### FALSIFIED HYPOTHESES
| # | Location | Suspected defect | Check (quote) | Status | Could it have failed? | Paths not covered | Mode | Confidence |
|---|----------|------------------|-------|--------|------------------------|-------------------|------|------------|
| T12 | scripts/test_check.py:32 | The developer's real `.check-private-terms` is copied into tmp, so tests run against real private terms | `for item in ("README.md", "CHANGELOG.md", "skills", ".claude-plugin", "scripts", ".gitignore"):` | falsified | Yes. The list is explicit, and the file sits at the root (load_terms reads `root/.check-private-terms`, scripts/check.py:251). Adding it to the list would have copied it. | The environment-variable route is **not** covered. See T-F3. | Deductive | 88 |

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| T-F1 | scripts/test_check.py:171-173, :286, :341-344 | `test_second_badge_mismatch`; the `f"{a.upper()}  {b}"` subtest; `test_whole_word_term_glued_in_output_is_still_masked` | Demonstrated defect | medium | Traced against the current code, these three tests should be **red**: C-F5 (only the first badge is checked), C-F2 (two spaces), C-F1 (key not masked, so `assert_no_leak` and "message hidden" both fail). The tests are right and the code is wrong, but the suite as shipped cannot pass, so the hook-plus-tests workflow is broken. On Windows the `"\n"` subtest is red as well (CRLF written by :84-85). | Deductive (run-only, capped) | 75 | Fix C-F1, C-F2 and C-F5. No test change is needed. |
| T-F2 | scripts/test_check.py:479 | `self.assertIn("orphan.md", r.stdout + self.ref("orphan.md"))` | Demonstrated defect | low | Tautological. `self.ref("orphan.md")` always contains "orphan.md", and the return code is never checked. The test passes even if check 7 is deleted. Coverage is rescued only by :481-485. | Deductive | 95 | `self.assert_fails(r, "orphan.md", "never named in SKILL.md")` |
| T-F3 | scripts/test_check.py:43-45 | `env = dict(os.environ)` / `if terms is not None: env["CHECK_PRIVATE_TERMS"] = terms` | Preventive measure | medium | A developer who configured terms the documented way (the env var, README.md:250) runs the suite. The env var wins over the terms file (scripts/check.py:247-249), so `test_missing_terms_is_said_not_silent` (:354-357), `test_missing_terms_fails_in_strict_mode` (:359-360) and the 3 `terms_file` tests (:318-329) test the developer's real terms instead of the fixture, and become false reds. This is a test-environment artifact (changed defaults). | Deductive | 90 | `env.pop("CHECK_PRIVATE_TERMS", None)` before the `if`. |
| T-F4 | scripts/test_check.py:575-578 | `test_runner_passes_on_the_repo` … `assertRegex(r.stdout, r"\d+ fact file\(s\), 0 failed")` | Preventive measure | medium | On a machine without `rustc`/`node`, 52.rs and 53.ts print `skip` and the run exits 0 (C-F4), so the test is green without running them. This is a test-environment artifact (different resources) that hides C-F4. | Deductive | 90 | Also assert `"skip" not in r.stdout`, or `skipUnless(shutil.which("rustc") and shutil.which("node"))` plus a separate test that a missing toolchain fails (a PATH without them). |
| T-F5 | scripts/test_check.py (whole file read) | (absence) | Preventive measure | medium | I found no test, anywhere in scripts/test_check.py, for: (a) a missing toolchain failing; (b) scripts/pre-commit itself (`--strict`, the evals trigger, tmp cleanup); (c) mismatched fence characters; (d) the `.rs`/`.ts` comment and string stripping of `has_assertion` (scripts/check_facts.py:35-51); (e) crash paths (C-F7). Three of the five gaps hide defects found above (C-F3, C-F4, C-F6). | Inductive (5 instances) | 78 | Add tests for (a)-(e). (b) can run the hook in StagedTest with `git commit`. |
| T-F6 | scripts/test_check.py:351 | `os.symlink(os.path.join(self.tmp, "does-not-exist"), self.path("dangling.md"))` | Preventive measure | low | On Windows without symlink privilege or Developer Mode, `os.symlink` raises `OSError`, so the test errors. That is a false red on a supported platform (README.md:263). | Deductive | 80 | Wrap it in `try/except OSError: self.skipTest(...)`. |
| T-F7 | scripts/test_check.py:502-505 | `git = lambda *a: subprocess.run(["git", …], check=True, …)` | Preventive measure | low | `ReferencesTest` has no `skipUnless(shutil.which("git"))`, unlike `StagedTest` (:369). Without git, this test errors (`FileNotFoundError`) instead of skipping. | Deductive | 90 | Add `@unittest.skipUnless(shutil.which("git"), …)` to this test. |
| T-F8 | scripts/test_check.py:336-339 | `# whole-word detection does not flag "<term>labs"` … `self.run_check(terms=T1)` | Demonstrated defect | low | Test-code drift. `T1` without `=` is a **substring** term (scripts/check.py:265), so check 3 does flag `zqvorblaxlabs`. The comment describes an older default. The test duplicates :331-334 and does not test what it says (that is done by :341-344). | Deductive | 90 | Fix the comment, or delete the test as a duplicate. |

## STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|
| S8 | Requirement Inversion | T1 (what if the script crashes instead of failing?) | yes | 88 | `"checked ("` is required (scripts/test_check.py:58), so a traceback never counts as a failure. |
| S9 | Time Travel | T11 (eval 37 renumbered) | yes | 80 | :550 does not assert its precondition, but if "day > 31" disappears the hash is unchanged and `assert_fails` goes red. It fails loudly, not silently. |
| S10 | Existence Question | `test_old_untagged_eval_is_accepted` (:155-159) | yes | 80 | Delete it mentally: the only lost check is the :158 precondition that eval 20 is untagged. Without it, :149-153 alone would not prove that ids < 21 are exempt. It earns its place. |

## HYPOTHESES
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| H6 | T-F1 is predicted by tracing. | The suite has 3 red tests today (4 on Windows). | Some earlier failure masks them (none seen in the trace). | `python3 -m unittest scripts/test_check.py` with `CHECK_PRIVATE_TERMS` unset. |

## HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| HB7 | scripts/test_check.py:43 | isolated runs (`-I`, :50) | `-I` isolates the interpreter, not `CHECK_PRIVATE_TERMS`, which is inherited | Preventive measure (T-F3) | 90 |

## ADVERSARIAL SCAFFOLD FINDINGS
- **Reviewer blind spots:** a test that concatenates its own expectation into the haystack (:479). The `-I` flag giving a false sense of isolation (:50 vs :43).
- **Highest-risk claims:** T2 (red suite), T5 (green without toolchains), T4 (environment dependence).
- **Multi-step traces:** missing toolchain → `skip` → exit 0 → `test_runner_passes_on_the_repo` green → C-F4 never surfaces.
- **Subtlety flags:** `self.tearDown(); self.setUp()` inside subtests (:248, :288, :448) resets the tmp correctly, but a failure inside one subtest leaves the next one to rebuild it. That is fine as written.

### SUMMARY (Tests)
- **Domain:** Tests
- **Claims:** 4 verified, 8 in FAIL (3 defects, 5 preventive measures), 1 falsified
- **Survived:** 3 of 3 stress tests
- **Failure categories:** 5
- **Invariants:** I4 is touched and enforced by `assert_no_leak`, which bites.
- **Hypotheses:** 1
- **Hidden behaviors:** 1
- **Findings by type:** 3 demonstrated defects, 5 preventive measures, 1 falsified hypothesis
- **Critical issues:** 0

---

# DOMAIN 3: DOCUMENTATION (docstrings, usage text, comments, error messages in the four files)

## VERIFICATION DOMAIN
Documentation

## GROUND TRUTH
- The code of the same files, as traced in Domain 1.
- README.md:244-263.

The invariants are the same as in Domain 1. The documentation restates I1-I9 correctly. The places where doc and code disagree were assigned to Code as their primary domain (C-F1 to C-F5), because the docstrings and the README agree with each other and the code is the outlier.

## DECOMPOSED CLAIMS
1. D1: scripts/check.py:42-44 says the references folder "is read as it is on disk, tracked or not". Mode: Deductive.
2. D2: the error "not valid JSON" (scripts/check.py:168) names the actual condition. Mode: Deductive.
3. D3: the error "not a git repository (or git is not available)" (scripts/check.py:431) names the actual condition. Mode: Deductive.
4. D4: "Matching ignores case, accents and Unicode forms" (scripts/check.py:15). Mode: Deductive.
5. D5: the usage text (scripts/check.py:49) matches argparse. Mode: Deductive.
6. D6: the usage text (scripts/check_facts.py:16-18) matches argparse. Mode: Deductive.
7. D7: the install instructions (scripts/pre-commit:3-4) work. Mode: Deductive.
8. D8: the run instruction (scripts/test_check.py:3) works. Mode: Deductive.
9. D9: the check 1 docstring (scripts/check.py:6-9) matches the code. Mode: Deductive.

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Misleading error message | 2 (scripts/check.py:168, :431) | scripts/check.py |
| Stale or partial rationale | 1 (scripts/check.py:42-44) | scripts/check.py |

## VERIFICATION RESULTS
### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| D5 | check.py usage | `--strict`, `--staged`, `--root` at scripts/check.py:419-421 match :49. |
| D6 | check_facts usage | `ids` (`nargs="*"`) and `--root` at scripts/check_facts.py:78-79 match :16-18. Root-after-ids is tested at scripts/test_check.py:604-607. |
| D7 | hook install | `ln -s ../../scripts/pre-commit .git/hooks/pre-commit` resolves relative to `.git/hooks/`, giving `<repo>/scripts/pre-commit`. The executable bit could not be verified because there is no git metadata in ./tree (see H7). |
| D8 | unittest command | `python3 -m unittest scripts/test_check.py`: unittest maps the path to `scripts.test_check`, which is importable as a namespace package. The tests use absolute paths from `ROOT` (scripts/test_check.py:17). |
| D9 | check 1 doc | Matches scripts/check.py:163-207 (see C1, C2). |

### FALSIFIED HYPOTHESES
None.

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| D-F1 | scripts/check.py:42-44 | "The folder is read as it is on disk, tracked or not, since copying the skill's folder ships every file in it." | Demonstrated defect | low | In `--staged` mode (the hook's mode), `root` is the `checkout-index` copy (scripts/check.py:433), so an untracked `references/orphan.md` in the working tree is **not** seen. The test asserts exactly that (scripts/test_check.py:502-510, "not staged: not part of the commit"). The stated rationale (copying ships every file) holds only in working-tree mode. | Deductive | 90 | "…read as it is on disk, tracked or not (with --staged: as it is in the index)." |
| D-F2 | scripts/check.py:167-168 | `except (OSError, ValueError) as e: rep.error(EVALS, f"not valid JSON ({…})")` | Demonstrated defect | low | A missing or unreadable evals.json is reported as "not valid JSON (FileNotFoundError: …)". The class name saves it, but the headline is wrong. | Deductive | 92 | Separate `OSError` → "cannot be read". |
| D-F3 | scripts/check.py:392-393, :431 | `except (OSError, subprocess.CalledProcessError): return None` → "not a git repository (or git is not available)" | Demonstrated defect | low | Any `checkout-index` failure (a full disk, a path too long on Windows, an unmerged index during a conflicted merge) is reported as "not a git repository". | Deductive | 88 | Include git's stderr in the message. |
| D-F4 | scripts/check.py:15 | "Matching ignores case, accents and Unicode forms" | Preventive measure | low | `normalize` (scripts/check.py:93-96) removes only **combining** marks after NFKD. Letters such as ø, ł, đ and æ have no decomposition, so a term "Søren" never matches "Soren" and the reverse. Likelihood: medium for names from Nordic or Slavic languages. | Deductive (Unicode decomposition facts recalled, not cited from ./tree) | 75 | Document the limit in the "Not caught" list, or add a small transliteration table (ø→o, ł→l, đ→d, æ→ae, œ→oe). |

## STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|
| S11 | Time Travel | D7 (a new developer on Windows) | yes | 78 | scripts/pre-commit:4 tells Windows users to copy rather than link, and README.md:263 agrees. Whether `python3` works there is H1. |

## HYPOTHESES
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| H7 | scripts/pre-commit has a `#!/bin/sh` shebang. Its file mode is not visible in ./tree. | The file is tracked as 100755, so the symlinked hook is executable. | It is tracked as 100644, so git silently ignores the hook ("hook was ignored because it's not set as executable" hint). | `git ls-files -s scripts/pre-commit`. |

## HIDDEN BEHAVIORS DETECTED
None beyond those listed under Code.

## ADVERSARIAL SCAFFOLD FINDINGS
- **Reviewer blind spots:** a rationale sentence that is true in one of the two modes (D-F1).
- **Highest-risk claims:** the doc claims behind C-F3 and C-F4 (counted under Code), then D-F1.
- **Multi-step traces:** none beyond those under Code.
- **Subtlety flags:** none.

### SUMMARY (Documentation)
- **Domain:** Documentation
- **Claims:** 5 verified, 4 in FAIL (3 defects, 1 preventive measure), 0 falsified
- **Survived:** 1 of 1 stress test
- **Failure categories:** 2
- **Invariants:** restated correctly, no contradiction
- **Hypotheses:** 1
- **Hidden behaviors:** 0
- **Findings by type:** 3 demonstrated defects, 1 preventive measure
- **Critical issues:** 0

---

# DOMAIN 4: DATA (formats defined and parsed by these scripts)

## VERIFICATION DOMAIN
Data

## GROUND TRUTH
- The format statements: NOT_COMPUTABLE:1-3, scripts/check.py:34-38, scripts/check.py:13-15.
- The existing files in the field: NOT_COMPUTABLE:4-12, the facts/*.py, *.rs and *.ts headers (for example 52.rs:1 and 53.ts:1, which use `//`, and 49.py:1, which uses `#`).

Invariant I6 is touched. The hash binding bites (C14).

## DECOMPOSED CLAIMS
1. DA1: NOT_COMPUTABLE entries are well-formed, unique, and refer to existing evals that state facts. Mode: Deductive.
2. DA2: there is exactly one fact file per eval id. Mode: Deductive.
3. DA3: `prompt-sha256` is computed over the prompt exactly as an eval consumer sees it, as UTF-8 of the decoded JSON string. Mode: Deductive.
4. DA4: the terms file format tolerates a BOM, comments and non-UTF-8 encodings. Mode: Deductive. Moved to FALSIFIED HYPOTHESES.
5. DA5: the hash header is found in every comment style in use. Mode: Deductive.

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Constraint gaps (uniqueness, references) | 2 (scripts/check.py:494, :469-473) | scripts/check.py |

## VERIFICATION RESULTS
### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| DA3 | hash over the decoded prompt | `hashlib.sha256(prompts[i].encode("utf-8"))` (scripts/check.py:478), so a reformatting of evals.json (indentation, escapes) does not invalidate it. Only the prompt's content does. |
| DA5 | header found in any comment style | The regex `prompt-sha256:\s*([0-9a-f]{64})` on the first 2000 characters (scripts/check.py:476-477) ignores the comment prefix. It is present in `#` (49.py:1) and `//` (52.rs:1, 53.ts:1) files. |

### FALSIFIED HYPOTHESES
| # | Location | Suspected defect | Check (quote) | Status | Could it have failed? | Paths not covered | Mode | Confidence |
|---|----------|------------------|-------|--------|------------------------|-------------------|------|------------|
| DA4 | scripts/check.py:255 | A BOM before `# comment` turns the comment into a term | `decode(f.read())[0]` → `data.decode("utf-8-sig")` (scripts/check.py:120) | falsified | Yes. With plain `utf-8`, the line would start with U+FEFF and `.strip().startswith("#")` would be false. `test_bom_before_a_comment_keeps_it_a_comment` (scripts/test_check.py:323-326) asserts that the comment stays a comment. | A UTF-16 terms file is covered by `decode`. A Latin-1 terms file is untested. | Deductive | 90 |

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| DA-F1 | scripts/check.py:494 | `reasons[int(m.group(1))] = m.group(2)` | Preventive measure | low | A duplicate id overwrites silently. A reason for an id that does not exist, is below 29, or no longer states `(Facts` is never reported, so stale exemptions pile up. If an eval is renumbered, an old line can exempt a different eval that does state facts. Likelihood: low to medium as evals are added and edited. | Deductive | 90 | Error on duplicates, and on ids not in `ids` or not stating facts. |
| DA-F2 | scripts/check.py:469-473 | `if not stem.isdigit() or int(stem) not in ids: … else: with_file[int(stem)] = name` | Preventive measure | low | `040.py` and `40.py` both map to id 40. The second one silently replaces the first in `with_file`, so only one is hash-checked. check_facts.py would expect `ok 040` from the first (scripts/check_facts.py:94, 107). `isdigit()` also accepts non-ASCII digits. | Deductive | 88 | Require `stem == str(int(stem))` and ASCII digits (`re.fullmatch(r"[1-9][0-9]*", stem)`). |

## STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|
| S12 | Requirement Inversion | DA3 (what if a prompt is only re-escaped, not changed?) | yes | 85 | The hash is over the decoded string, so it survives a re-escape. An edit to the prompt's content still fails (scripts/test_check.py:547-552). |

## HYPOTHESES
None.

## HIDDEN BEHAVIORS DETECTED
None.

## ADVERSARIAL SCAFFOLD FINDINGS
- **Reviewer blind spots:** exemptions that never expire (DA-F1).
- **Highest-risk claims:** DA1, then DA2.
- **Multi-step traces:** none.
- **Subtlety flags:** `isdigit()` vs `int()` (DA-F2).

### SUMMARY (Data)
- **Domain:** Data
- **Claims:** 2 verified, 2 in FAIL (0 defects, 2 preventive measures), 1 falsified
- **Survived:** 1 of 1 stress test
- **Failure categories:** 1
- **Invariants:** I6 touched, and its hash binding bites
- **Hypotheses:** 0
- **Hidden behaviors:** 0
- **Findings by type:** 0 demonstrated defects, 2 preventive measures, 1 falsified hypothesis
- **Critical issues:** 0

---

# DOMAIN 5: UX (command-line and terminal output)

## VERIFICATION DOMAIN
UX

## GROUND TRUTH
- references/ux.md: States, Sensitive data and Real content, adapted to a terminal interface.
- The output code: scripts/check.py:397-414 and :523-527, scripts/check_facts.py:92-112, scripts/pre-commit:15-17.

Contrast, targets, focus and motion do not apply to plain terminal text.

## DECOMPOSED CLAIMS
1. U1: no secret or personal data appears on screen. Mode: Deductive. This is cross-referenced to C-F1 and counted under Code.
2. U2: every outcome state is visible to the person committing (success, failure, skip). Mode: Deductive.
3. U3: every run ends with a summary line. Mode: Deductive. Normal paths pass. The crash path is C-F7, counted under Code.
4. U4: masked output says what kind of item was hidden. Mode: Deductive.
5. U5: fact failures name the file and show the relevant error. Mode: Deductive.

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Silent fallthrough (a state that is not shown) | 1 (scripts/pre-commit:15-17) | scripts/pre-commit |

## VERIFICATION RESULTS
### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| U3 | summary always printed (normal paths) | scripts/check.py:441, 527: `checked (<scope>): <checks> — N error(s), M warning(s)`. |
| U4 | informative masking | scripts/check.py:406-412 distinguishes a hidden location, message or line. |
| U5 | useful failure lines | scripts/check_facts.py:70-73 prefers `error…` lines (rustc), otherwise the last 5 non-blank lines. :102 prefixes `FAIL <name>:`. |

### FALSIFIED HYPOTHESES
None.

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| U-F1 | scripts/pre-commit:15-17 | `out="$(…check_facts.py…)"; rc=$?` … `[ $rc -eq 0 ] \|\| { printf "%s\n" "$out"; exit 1; }` | Demonstrated defect | low | On success the fact runner's output is discarded, including `skip <file>: toolchain not found` lines. The committer never learns that some facts were not checked. This compounds C-F4, but it is a separate state-visibility issue: it would still hide any future warning line. | Deductive | 90 | Always `printf "%s\n" "$out"`, or at least print the lines starting with `skip`. Alternatives: (a) always print the output, which is noisier but complete; (b) print only non-`ok` lines, which is quiet but shows skips and warnings. (b) is recommended. |

## STRESS TEST RESULTS
None: the claims that passed are small output formatting claims, already covered by S8 (summary required).

## HYPOTHESES
None.

## HIDDEN BEHAVIORS DETECTED
None beyond HB2 and HB3.

## ADVERSARIAL SCAFFOLD FINDINGS
- **Reviewer blind spots:** success paths that swallow output.
- **Highest-risk claims:** U1 (C-F1).
- **Multi-step traces:** see Code.
- **Subtlety flags:** none.

### SUMMARY (UX)
- **Domain:** UX
- **Claims:** 3 verified, 1 in FAIL (1 defect), 0 falsified
- **Survived:** 0 of 0 stress tests
- **Failure categories:** 1
- **Invariants:** I4 is relevant here, see Code
- **Hypotheses:** 0
- **Hidden behaviors:** 0
- **Findings by type:** 1 demonstrated defect
- **Critical issues:** 0

---

## CROSS-DOMAIN SUMMARY
- **Domains:** Code, Tests, Documentation, Data, UX
- **Claims:** 32 verified, 26 in FAIL (14 demonstrated defects, 12 preventive measures), 4 falsified (0 conditionally)
- **Survived:** 10 of 12 stress tests (S6 and S7 did not survive). 4 techniques were used: Scale Shift, Time Travel, Existence Question, Requirement Inversion.
- **Failure categories:** 11 rows in total. The main systemic patterns are: partial enforcement of a documented rule; silent fallthrough on a safety gate; doc-to-code drift; test-environment artifacts; crashes on unguarded input.
- **Invariants:** 9 found, 9 touched. 2 bite fully, 3 bite partly, 4 do not bite (I2, I4, I8, I9).
- **Hypotheses:** 7 (H1-H7)
- **Hidden behaviors:** 7 detected (5 of them problems)
- **Findings by type:** 14 demonstrated defects, 12 preventive measures, 4 falsified hypotheses (0 conditionally)
- **Critical issues:** 0 demonstrated defects of critical severity. Three are of high severity (C-F1 privacy leak in the output, C-F2 separator, C-F3 hook without `--strict`). Preventive measures of critical severity: 0.
- **Pre-code:** not applicable
- **Executed:** 0 tests run (reasoning only)
- **Proposed:** 8 checks and 10 writes awaiting an answer
- **Changes touching several domains:** C-F4 (Code) is hidden by T-F4 (Tests) and U-F1 (UX) and contradicted by README.md:254. C-F1 (Code) is U1 (UX) and the cause of T-F1 (Tests). C-F3 (Code) is contradicted by its own comment, scripts/pre-commit:5, and by README.md:260.
- **Recommendation:** do not trust the privacy gate as it stands. The hook does not enforce `--strict`, multi-character separators escape detection, and `=` terms can be printed. Fix C-F1, C-F2, C-F3, C-F4 and C-F5 first (each is a one-line change). Those five fixes should turn T-F1 green. Then fix T-F2, T-F3 and T-F4 so the suite can catch these regressions.

## PROPOSED EXECUTABLE CHECKS
Status of every row: **proposed** (nothing run).

| # | Claim | Confidence now | Check (command, test or query) | Confirms if | Refutes if | Cost and side effects |
|---|-------|----------------|--------------------------------|-------------|------------|-----------------------|
| P1 | T-F1 / H6: 3 tests red | 75 | `env -u CHECK_PRIVATE_TERMS python3 -m unittest scripts/test_check.py -v` | exactly `test_second_badge_mismatch`, the two-space subtest and `test_whole_word_term_glued_in_output_is_still_masked` fail | all pass | Runs the suite. Every test works in its own temporary copy (scripts/test_check.py:31). Runs git in tmp (StagedTest) and runs the fact files (needs rustc and node). No write to the working copy. |
| P2 | C-F4: missing toolchain skips with exit 0 | 95 (traced) | `PATH=<dir without rustc/node>:$(dirname $(which python3)) python3 scripts/check_facts.py 52; echo $?` | prints `skip 52.rs`, exit 0 | FAIL, exit 1 | Read-only. Runs only the runner, in its own temp dir. |
| P3 | C-F3: the hook passes without terms | 95 (traced) | In a scratch clone with the hook installed and no terms: `git commit --allow-empty -m t` after staging one file | commit succeeds, with a "private names were NOT checked" warning | commit refused | Writes a scratch clone in a temp dir only. |
| P4 | C-F1: `=` term leaked to output | 95 (traced) | In a scratch copy: add key `zqvorblaxlabs` to one eval, then `CHECK_PRIVATE_TERMS==zqvorblax python3 scripts/check.py --root <copy>` | the output contains `zqvorblaxlabs` | `[message hidden…]` | Scratch copy only. Uses a synthetic term, never a real private one. |
| P5 | C-F6: fence character mismatch | 90 (traced) | In a scratch copy, append ```` ``` ```` / `~~~` / a broken table / ```` ``` ```` to SKILL.md, then run check.py | false "table row" error | passes | Scratch copy only. |
| P6 | C-F7: crash on `"evals": null` | 88 (traced) | In a scratch copy, set `"evals": null`, then run check.py | Traceback (TypeError), no summary | summary with an ERROR | Scratch copy only. |
| P7 | H1, H4, T-F6: Windows behaviour | 40-55 | On Windows in Git Bash: `command -v python3 && python3 -c 1`. Also `python check_facts.py 52` with rustc, and the unittest suite | stub exits non-zero / `.bin` not executed / symlink test errors | all work | Read-only, on a Windows machine. |
| P8 | Mutation probe, scope the four files | n/a | 5 hand mutations on scripts/check.py:90, :223, :301, :400 and scripts/check_facts.py:91-93, each followed by the unit suite | survivors show untested lines (expected: :301, check_facts :91-93) | all killed | 5 mutants × the full suite. Mutates a **separate copy** and restores it afterwards. A memory-backed filesystem (tmpfs or RAM disk) is suggested for that copy. It needs your consent to create it, and enough free memory for about 1 MB of repo. |

**Proposed writes** (none made):
1. scripts/check.py:400: `term_patterns(terms, substring=True)` (C-F1).
2. scripts/check.py:90: `SEP = r"[\W_]*"` (C-F2).
3. scripts/pre-commit:9: add `--strict` (C-F3).
4. scripts/check_facts.py:91-93: report a missing toolchain as `FAIL` and count it (C-F4). Also scripts/pre-commit:17: print non-`ok` lines on success too (U-F1).
5. scripts/check.py:223: `for b in badges:` (C-F5).
6. scripts/check.py:361-366: match the fence character and length (C-F6). Also scripts/check.py:460-463: guard a non-list `evals`, and catch exceptions per check (C-F7).
7. scripts/test_check.py:479: replace with `assert_fails(r, "orphan.md", "never named in SKILL.md")` (T-F2). Also :43: `env.pop("CHECK_PRIVATE_TERMS", None)` (T-F3).
8. scripts/test_check.py: add the missing negative tests (T-F5 a-e). Add `skip "skip"` detection or a toolchain `skipUnless` (T-F4). Add `skipUnless(git)` on :502 (T-F7). Skip the symlink test on `OSError` (T-F6). Fix the comment at :337 (T-F8).
9. scripts/check.py:42-44, :168, :431 and the docstring "Not caught" list: wording fixes (D-F1 to D-F4). Also NOT_COMPUTABLE and stem validation (DA-F1, DA-F2).
10. Step 5, CHANGELOG.md under `## Unreleased` (CHANGELOG.md:5): one entry for the repository-check fixes above. No TODO.md, SPEC.md, PLAN.md, ADR/ or agent instruction files exist in ./tree.

**Which of P1-P8 may I run, and which of writes 1-10 may I make?** Nothing will run or be written without your answer.
