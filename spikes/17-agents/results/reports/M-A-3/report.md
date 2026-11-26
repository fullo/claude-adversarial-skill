# Adversarial verification — `scripts/check.py`, `scripts/check_facts.py`, `scripts/pre-commit`, `scripts/test_check.py`

**Cost estimate (large request, cost accepted, every choice settled, so the verification started at once):** 4 files in scope (about 1,070 lines), 5 domains (Code, Tests, Documentation, Data, UX). About 60 claims were decomposed. Nothing was run.

## INTAKE

- **Target:** every domain Step 0 detects in the four files. These are **Code** (the three scripts), **Tests** (`scripts/test_check.py`), **Documentation** (docstrings, comments, usage text and error messages in the four files), **Data** (the file formats the scripts parse and enforce: `evals.json`, `facts/NOT_COMPUTABLE`, the fact-file header, the private-terms list, CHANGELOG headings and badges) and **UX** (the terminal output of a command-line tool). The request named the target, so none of these is a default.
- **Depth:** standard (named in the request).
- **Scope:** the whole of the four files. There is no diff and no version history, so "changed path" below means "the path in these files".
- **Execution mode:** reasoning only (named in the request). The EXECUTED TESTS and MUTATION PROBE sections are omitted because nothing was approved to run.
- **Reference files of the skill:** I read `references/ux.md` because UX is in the target. I did not read `references/pre-code.md` because no artifact proposes work not yet done. I did not read `references/execution.md` because no run was approved.
- To change any of these, ask for a different depth, a narrower target or approved checks (for example: "run the unit tests in a copy"). Consent lasts for one verification, so any later verification starts at reasoning only again.

Severity scale: critical, high, medium, low. Every location is `path:line`, relative to `./tree`.

---

# DOMAIN 1 — CODE (`scripts/check.py`, `scripts/check_facts.py`, `scripts/pre-commit`)

## VERIFICATION DOMAIN
Code

## GROUND TRUTH
- The contract each script states for itself: the `scripts/check.py:2-50` docstring, the `scripts/check_facts.py:2-19` docstring and the comments at `scripts/pre-commit:2-5,10-11`.
- The repository's own description of the checks: `README.md:244-263` and `CHANGELOG.md:3,14,24,45`.
- The tests that encode the intended behaviour: `scripts/test_check.py` (all of it).
- The data the checks run on: `skills/adversarial-verify/SKILL.md:20`, `README.md:1-4`, `.claude-plugin/plugin.json:3`, `CHANGELOG.md:5,10`, `.gitignore:1-2`, `skills/adversarial-verify/evals/evals.json` (ids at lines 5…711), `skills/adversarial-verify/evals/facts/*` (37.py, 38.py, 40.py, 49.py, 51.py, 52.rs, 53.ts, NOT_COMPUTABLE).
- Python, git and POSIX `sh` semantics, reasoned from the code with no run (for example `re`, `subprocess.run(cwd=…)`, `git checkout-index --prefix`). No runtime traces were available.

## INVARIANTS
**Where I looked:** the whole of `./tree`. It has no `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, ADR or SPEC; I confirmed this with a glob of every file. The project states its invariants in `scripts/check.py:2-50` ("Check the repository's own invariants before a commit"), `README.md:244-254`, `CHANGELOG.md:3`, `scripts/test_check.py:1-5` and the comment at `scripts/check.py:423` ("the list is never committed"). I found 9. Every one is touched, because the scope is the code that enforces them.

| # | Invariant | Source | Touched by | Enforced by (file:line / test name) | Bites on changed path? |
|---|-----------|--------|------------|-------------------------------------|------------------------|
| I1 | `evals.json` is valid, has exactly 4 keys, integer ids 1..n in file order, non-empty fields and tags from eval 21 on | check.py:6-9, README.md:248 | check.py:163-207 | `check_evals`; tests `EvalsTest.*` (test_check.py:104-163) | **Yes.** Traced in C1. |
| I2 | SKILL.md's version equals **every** skill badge, plugin.json and the newest CHANGELOG entry | check.py:10-12, README.md:249, CHANGELOG.md:3 | check.py:212-241 | `check_version`; `VersionTest.test_second_badge_mismatch` (test_check.py:171-173) | **No, for badges after the first.** `badges[:1]` at check.py:223 (F1). The test that would catch it does not gate commits (T-F5). |
| I3 | No private term appears in any tracked file's content or name, however its parts are joined | check.py:13-26, README.md:250 | check.py:259-323 | `check_private`; `PrivateTest.*` | **Partly.** A separator of 2 or more characters (CRLF, `" - "`, double space) escapes detection (F2). |
| I4 | The private-terms list is never committed | check.py:423, README.md:250, .gitignore:1 | check.py:301, pre-commit:9 | `.gitignore:1` (only advisory: `git add -f` bypasses it); test `test_terms_file_is_gitignored` (test_check.py:365-366) checks only the ignore file | **No.** The check exempts the file by name (check.py:301) and nothing reports it when it is tracked or staged (F5). |
| I5 | Terms are never printed: any output line containing one is masked | check.py:22-23, README.md:250, test_check.py:4-5 | check.py:397-414 | `mask`; `assert_no_leak` (test_check.py:70-73) | **No, for `=` terms.** `mask` builds whole-word patterns (check.py:400), so glued forms are printed (F3). Two-character separators also escape masking (F2). |
| I6 | The private-name check is enforced before every commit (`--strict --staged`) | README.md:260, pre-commit:5 | pre-commit:9 | the hook | **No.** The hook omits `--strict`, so with no terms configured the commit passes with a warning (F4). |
| I7 | Every stated eval fact is executed; a missing toolchain is an error, never a silent skip | check_facts.py:8, README.md:254 | check_facts.py:90-93,113; pre-commit:12-17 | `check_facts.py`; `FactsTest.test_runner_*` | **No.** A missing `rustc` or `node` prints "skip" and exits 0. The hook hides that output on success (F6). |
| I8 | Every fact file belongs to an existing eval and carries the hash of its prompt | check.py:34-38, README.md:254 | check.py:457-501 | `check_facts` (check.py); `FactsTest.test_prompt_changed_after_its_facts`, `test_fact_file_without_hash`, `test_orphan_fact_file` | **Mostly.** A second fact file for the same id (for example `38.py` and `38.rs`) has its hash never checked (F10). |
| I9 | Every `references/<name>.md` named in the skill exists, and every reference file is named in SKILL.md | check.py:39-44, README.md:253 | check.py:506-520 | `check_references`; `ReferencesTest.*` | **Yes.** Traced in C18. |

## DECOMPOSED CLAIMS
1. C1 `check_evals` rejects bad JSON, missing or extra keys, non-int or bool ids, duplicate or non-consecutive ids, empty prompt, output or assertion, and untagged assertions from id 21 on — Mode: Deductive
2. C2 `check_version` compares the frontmatter version with every skill badge in the README — Deductive
3. C3 `check_version` compares the plugin.json `version` (a string) — Deductive
4. C4 `check_version` compares the first numeric `## <version>` heading of the CHANGELOG — Deductive
5. C5 Every failure of `check.py` is reported as an `ERROR` line followed by the summary — Deductive
6. C6 The parts of a private term match when joined by anything that is not a letter or digit (spaces, hyphens, underscores, line breaks) or by nothing — Deductive
7. C7 A term prefixed with `=` matches only as a whole word — Deductive
8. C8 Any output line containing a term is masked, with substring matching ("err on the side of hiding too much") — Deductive
9. C9 The private-terms list is never committed — Deductive
10. C10 JSON strings are also scanned after their escapes are decoded — Deductive
11. C11 Non-UTF-8 files are still scanned (UTF-16 with a BOM, otherwise Latin-1) — Deductive
12. C12 A tracked file that cannot be read is an error, not a silent skip — Deductive
13. C13 `--staged` checks exactly the index content and always removes its temporary directory — Deductive
14. C14 `--strict` fails when no terms are configured — Deductive
15. C15 The pre-commit hook enforces `--strict --staged` — Deductive
16. C16 Every fact file belongs to an eval and carries the sha256 of that eval's prompt — Deductive
17. C17 `NOT_COMPUTABLE` lines are parsed, and an eval with both a fact file and a reason fails — Deductive
18. C18 Reference files: a named file that is missing fails, and a file nobody names fails — Deductive
19. C19 Tables: every row has as many cells as the header (escaped pipes and code spans excluded, fences skipped) — Deductive
20. C20 `check_facts.py`: a missing toolchain is an error, never a silent skip — Deductive
21. C21 `check_facts.py`: a file with no assertion fails, and a file whose last output line is not `ok <id>` fails — Deductive
22. C22 `check_facts.py --root DIR` runs the fact files of any checkout DIR — Deductive
23. C23 `check_facts.py` exits non-zero when it ran nothing — Deductive
24. C24 A fact-file run always ends (it cannot block the hook indefinitely) — Deductive
25. C25 The hook runs the fact files only when the staged change touches the evals, and on exactly the staged content — Deductive
26. C26 The hook finds a working Python on every supported platform — Abductive
27. C27 Neutral-wording findings are warnings and never block — Deductive

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| **Silent fallthrough** (a protection that degrades to "warn and pass" or "skip and pass") | F4 (no `--strict` in the hook), F6 (toolchain "skip" exits 0, and the hook hides it), F5 (the terms file is skipped by name, with nothing reporting it) | pre-commit:9,17; check_facts.py:91-93,113; check.py:301 |
| **Missing completeness** (a rule stated for N cases, enforced for fewer) | F1 (only the first badge), F3 (masking substring for plain terms but not for `=` terms), F10 (one hash per id when several files share it), F2 (one separator character, not "anything") | check.py:223, 400, 466-473, 90 |
| **Assumed environment** | F7 (an absolute `--root` is assumed), F12 (`python3` on PATH is a real interpreter), F2 (LF line endings assumed for "line breaks"), U-F1 (an output encoding able to hold every file name) | check_facts.py:82-100; pre-commit:7-8; check.py:90, 525 |
| **Implicit ordering / stale state** | HB2 (the hook runs the working-tree copy of the checkers against staged content) | pre-commit:9,15 |

## OUT OF SCOPE (listed, not verified)
The same mismatches appear in files outside the four in scope:
- `README.md:260` — the comment "runs --strict --staged before every commit" (contradicted by pre-commit:9; see F4).
- `README.md:249` — "every skill badge in the README" (see F1).
- `README.md:250` — "how the parts of a term are joined (space, hyphen, underscore, line break, or nothing)" and "any output line containing a term is masked" (see F2, F3).
- `README.md:246,254` — "fails … if a needed toolchain (`rustc`, `node` 22.6 or later) is missing" (see F6).
- `CHANGELOG.md:3` — "`scripts/check.py` fails if they differ" (true only for the first badge, F1).

## VERIFICATION RESULTS

### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| C1 | `check_evals` enforces the evals contract | check.py:165-169 catches OSError and ValueError. 170-173 require a non-empty list. 180-184 report extra and missing keys. 186 uses `type(i) is not int`, which rejects bool. 191-193 reject empty prompt and output. 195-202 reject empty or untagged assertions with `TAG_RE` (75), which requires text after the tag. 203-207 report duplicates and non-consecutive ids separately, so both are reported (test_check.py:117-119). |
| C3 | plugin.json version compared as a string | check.py:226-236. A non-dict or non-string value gives "no version (a string)" (233-234). Invalid JSON gives "not valid JSON" (228-229). |
| C4 | First numeric CHANGELOG heading | check.py:237. `^## +([0-9][0-9.]*)\b` with `re.M` skips `## Unreleased` (CHANGELOG.md:5) and takes `## 4.2` (CHANGELOG.md:10), which equals SKILL.md:20 `"4.2"`. |
| C7 | `=` terms match whole words only | check.py:265 `whole_word = t.startswith("=") and not substring`; 275 `(?<![^\W_])…(?![^\W_])`. "Not preceded or followed by a letter or digit" matches docstring line 18-19. |
| C10 | JSON escapes decoded | check.py:313-323. Every key and string value is yielded (279-289) and searched when the raw body did not match (322). |
| C11 | Non-UTF-8 files scanned | check.py:112-122. UTF-16 is used only with a BOM (114). `utf-8-sig` strips a BOM (120). Latin-1 cannot fail (122). The Latin-1 and UTF-16 docstring limits (line 25) are stated honestly. |
| C12 | An unreadable file is an error | check.py:306-310. `OSError` → `rep.error(rel, "unreadable file, not checked")`, then `continue`. |
| C13 | `--staged` checks the index and cleans up | check.py:386-394: `checkout-index -a --prefix=tmp/` writes the index, not the working tree. 427-433 set `root = tmp`. 438-440: `finally: shutil.rmtree(tmp)` runs on every path, including git failure (431). Terms are read from the real repo before the switch (423). |
| C14 | `--strict` fails without terms | check.py:294-298. `(rep.error if strict else rep.warning)`. `CHECK_PRIVATE_TERMS=" , "` becomes `[]` (256), so strict fails (test_check.py:362-363). |
| C17 | NOT_COMPUTABLE parsing | check.py:483-496. `^(\d+):\s*(\S.*)?$` requires a reason (491). Overlap with `with_file` is an error (495-496). |
| C18 | Reference files | check.py:506-520. Names are collected from SKILL.md and every reference file (511-518), but only SKILL.md counts as "named" (515-516). Unnamed files fail (519-520). `reference_files` reads the folder as it is on disk under `root`, which is the index copy under `--staged`, as the docstring at 43-44 says. |
| C19 | Table row counts | check.py:341-381. The header is the line before a delimiter that contains a pipe on either line (369). The delimiter's own count is checked (372-373). Rows run until a blank line or a line without a pipe (375-379). Code spans and `\|` are removed before counting (345). Fences toggle (361-368). Two preventive limits are reported as F15 and F16. |
| C21 | No-assertion and missing-`ok` cases fail | check_facts.py:42-51. Python uses `ast` (Assert or Raise nodes, so comments and strings are excluded). Rust and TS strip comments and strings first (35-39). 95-98 fail on no assertion. 106-109 require the last non-empty stdout line to be exactly `ok <stem>`. 99-104 stop at the first failing step. |
| C23 | Exits non-zero when no file matched | check_facts.py:113 `return 1 if failed or not files else 0`. An id selection that matches nothing gives an empty `files` and exit 1 (test_check.py:615-617). This is not true when every file was skipped: see F6. |
| C25 | The hook runs facts only on an evals change, on staged content | pre-commit:12 filters `git diff --cached --name-only` on `^skills/adversarial-verify/evals/`. 14 copies the index into a fresh `mktemp -d`. 15 points `--root` at it. 16 removes it on success and failure alike (rc is captured first). `out=$(…); rc=$?` gives the command's own status in POSIX `sh`. The limits are listed in HB2 and HB3. |
| C27 | Neutral wording only warns | check.py:328-336. Only `rep.warning` is called, and exit status depends on `rep.errors` alone (442). |

### FALSIFIED HYPOTHESES
| # | Location | Suspected defect | Check (quote) | Status (falsified / conditionally) | Could it have failed? (how shown, or the check that would complete it) | Paths not covered | Mode | Confidence |
|---|----------|------------------|-------|------------------------------------|------------------------------------------------------------------------|-------------------|------|------------|
| FH1 | check.py:321 | Line numbers of a private-term hit are wrong because `normalize` (NFKD, casefold) changes the text before newlines are counted | `body.count(chr(10), 0, m.start()) + 1` on the normalized `body` | falsified | Yes. Both the count and `m.start()` are on the same normalized string, so the offset is consistent. NFKD and casefold never create or remove U+000A. A defect would show if the count ran on the raw `text`, and it does not. | A file whose decoded text uses lone `\r` as its line terminator: its line number would be 1. This is cosmetic. | Deductive | 85 |
| FH2 | check.py:436-437 | `--staged` outside git runs the checks on an empty tree and passes | `if files or not args.staged: run_checks(...)` together with `rep.error("--staged", "not a git repository …")` at 431 | falsified | Yes. The error is added before the guard, so the exit is 1 (442). The guard only skips running checks on nothing. | An index with zero entries (a fresh repo with nothing staged) passes with "0 error(s)". Git refuses an empty commit anyway, so this stays open as HB4. | Deductive | 85 |
| FH3 | pre-commit:15 | `rc=$?` reads the status of the assignment, not of `check_facts.py` | `out="$("$py" -I … )"; rc=$?` | falsified | Yes. In POSIX `sh` the exit status of an assignment that contains a command substitution is that of the substitution. The defect would exist only with `local out=$(…)` or `export`, which are not used. | — | Deductive | 85 |

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| F1 | scripts/check.py:223 | `for b in badges[:1]:` | Demonstrated defect | low | The docstring (check.py:10) and README.md:249 promise "every skill badge". The README gets a second badge `![old](…/badge/skill-v2.0-blue)` (exactly test_check.py:172). `badges == ["4.2","2.0"]` but only `"4.2"` is compared, so no error and exit 0. A stale version badge ships silently, and `VersionTest.test_second_badge_mismatch` is red by trace. No violation today: README.md:1 is the only skill badge (README.md:2 is `skills-1`, which the regex does not match). | Deductive | 92 | `for b in badges:` (report each mismatching badge). |
| F2 | scripts/check.py:90 (used at 274) | `SEP = r"[\W_]?"  # anything that is not a letter or digit, possibly nothing` | Demonstrated defect | high | The `?` allows **at most one** separator character. The two-word term `quillane dorvex` gives the pattern `quillane[\W_]?dorvex`, which does not match (a) `QUILLANE  dorvex` (two spaces; the variant at test_check.py:286, so `test_two_words_joined_any_way` is red by trace); (b) the term split across a line in a **CRLF** file, `quillane\r\ndorvex`, because `read_text`/`decode` (112-130) keeps `\r\n` as two characters; (c) `Quillane - Dorvex` or `Quillane, Dorvex`. Such a file is committed with no error, against the docstring at check.py:16-17 ("anything … line breaks") and README.md:250. The same pattern drives `mask` (400), so these forms are also printed unmasked. | Deductive | 92 | `SEP = r"[\W_]*"`. A cap such as `[\W_]{0,8}` also works if false positives across long punctuation runs are a concern. Add a CRLF case to the test. |
| F3 | scripts/check.py:399-400 | `# substring patterns: when hiding output, err on the side of hiding too much` / `pats = term_patterns(terms)` | Demonstrated defect | medium | `term_patterns` defaults to `substring=False` (259), so a `=` term keeps its whole-word pattern in `mask`. Configure `=zqvorblax` and add an eval key `zqvorblaxlabs`. `check_evals` prints `unexpected keys ['zqvorblaxlabs']` (182), and `mask` does not hide it because `zqvorblax` is not a whole word there. The private name reaches the terminal or a CI log, against check.py:22-23 and README.md:250. `test_whole_word_term_glued_in_output_is_still_masked` (test_check.py:341-344) is red by trace. Medium, not high: the glued form is already a documented "not caught" for detection (check.py:25-26), so the file itself is committed anyway. The output leak is the extra exposure. | Deductive | 92 | `pats = term_patterns(terms, substring=True)`. That is the parameter that exists for this purpose and is never passed anywhere. |
| F4 | scripts/pre-commit:9 | `"$py" -I "$root/scripts/check.py" --staged --root "$root" \|\| exit 1` | Demonstrated defect | high | Line 5 ("--strict fails if no private terms are configured") and README.md:260 ("runs --strict --staged before every commit") both describe `--strict`, but the command does not pass it. On a fresh clone or a new machine with no `.check-private-terms` and no `CHECK_PRIVATE_TERMS`, `check_private` takes the warning branch (check.py:297), exit is 0 and the commit proceeds with private names **not checked**. That defeats invariant I3 at the one point where it is meant to bite. | Deductive | 92 | `"$py" -I "$root/scripts/check.py" --strict --staged --root "$root" \|\| exit 1`. |
| F5 | scripts/check.py:301-302 | `if os.path.basename(rel) == TERMS_FILE: continue` | Preventive measure | high | Invariant I4 ("the list is never committed", check.py:423; README.md:250) rests only on `.gitignore:1`. A `git add -f .check-private-terms` (or a copy named that in any subfolder) puts **every private term in plain text** into the commit. Under `--staged` that file is in `files` (check.py:391-394) and is skipped by name, and no other line reports that it is tracked or staged. Nothing shows this happening today: no such file exists in `./tree`. Likelihood: low (a deliberate `-f`, or a tool that ignores `.gitignore`). Impact: the whole list leaks. | Deductive | 88 | In `check_private`, report `rep.error(rel, "the private-terms list is tracked/staged: it must never be committed")` for any `rel` whose basename is `TERMS_FILE`, instead of skipping it silently. Add a staged test for it. |
| F6 | scripts/check_facts.py:91-93 (and 113; pre-commit:15-17) | `print(f"skip {name}: toolchain not found")` / `continue` | Demonstrated defect | medium | The docstring at check_facts.py:8 says "A missing toolchain is an error, never a silent skip", and README.md:254 says the same. On a machine without `rustc` (or without `node`), `52.rs` (or `53.ts`) prints `skip`, `failed` stays 0 and `files` is non-empty, so the exit is 0 (113). `check_facts.py 52` on such a machine prints `1 fact file(s), 0 failed` and exits 0 having run nothing. The hook only prints `out` when `rc ≠ 0` (pre-commit:17), so at commit time the skip is **completely silent**. A false fact edited into the Rust or TS evals, with its hash updated, is committed unverified. | Deductive | 90 | Count a missing toolchain as a failure: `print(f"FAIL {name}: toolchain not found ({'rustc' if …})"); failed += 1; continue`. Report a `skipped` count separately if an opt-out is ever wanted. |
| F7 | scripts/check_facts.py:82,89,100 | `FACTS = os.path.join(root, FACTS_REL)` … `path = os.path.join(FACTS, name)` … `subprocess.run(step, cwd=FACTS, …)` | Demonstrated defect | low | With a **relative** root (`python3 scripts/check_facts.py --root .`, a form the docstring at line 18 allows), `path` is relative to the parent's cwd. The child is started with `cwd=FACTS`, so Python, rustc and node resolve `./skills/…/facts/38.py` again from inside `facts/`, giving `…/facts/skills/…/facts/38.py`, which is not found. Every file is reported `FAIL`. This is a false red, never a false green. The hook (`mktemp -d`, absolute) and the default `ROOT` (absolute, line 31) are not affected. | Deductive | 85 | `root = os.path.abspath(args.root)` at line 81. |
| F8 | scripts/check_facts.py:43 | `text = open(path, encoding="utf-8").read()` | Demonstrated defect | low | A fact file that is not valid UTF-8 (for example saved as Latin-1 with an accented comment) raises `UnicodeDecodeError` in `has_assertion`. The runner then dies with a traceback, its summary is never printed and the remaining files are never run. The exit is non-zero, so the hook still blocks. The cost is a confusing message, not a false pass. | Deductive | 85 | Read with `errors="replace"` (only the assertion scan needs the text), or catch the error and report `FAIL {name}: not UTF-8`. |
| F9 | scripts/check.py:214,217,227-229,237 (also 331, 355) | `plugin = json.loads(read_text(root, PLUGIN, rep))` / `except ValueError as e:` | Demonstrated defect | low | `read_text` raises `OSError` when README.md, plugin.json, CHANGELOG.md or SKILL.md is missing (for example a staged deletion under `--staged`). `check_version` catches only `ValueError`, and `check_neutral`/`check_tables` catch nothing. The script ends with a traceback, no `ERROR` line and no summary, against test_check.py:4 ("Every failing case must come from the script's own ERROR and summary") and the pattern of `check_evals` (167). It still exits non-zero, so it blocks; the messages are what is lost. | Deductive | 85 | Wrap each file read in `try/except OSError` → `rep.error(rel, "missing or unreadable")`, as `check_evals` does. |
| F10 | scripts/check.py:466-473 | `with_file[int(stem)] = name` | Preventive measure | low | If two fact files share an id (`38.py` and `38.rs`, a plausible step when porting a fact to another language), the dict keeps only the last in sorted order (`38.rs`). The hash of `38.py` is **never checked**, so it can go stale after a prompt edit and invariant I8 does not bite on it. `check_facts.py` would still run both. Nothing shows this today: every fact id in `facts/` is unique. | Deductive | 85 | Collect `with_file.setdefault(id, []).append(name)` and check the hash of every file (or forbid two files per id with an error). |
| F11 | scripts/check_facts.py:100 | `r = subprocess.run(step, cwd=FACTS, capture_output=True, text=True)` | Preventive measure | low | There is no `timeout`. A fact file with an infinite loop (or a `rustc` that hangs) blocks `git commit` indefinitely, with no output because the hook captures it (pre-commit:15). Likelihood: low; these are small scripts reviewed before commit (pre-commit:11). | Deductive | 80 | `subprocess.run(..., timeout=120)` with `except subprocess.TimeoutExpired` → `FAIL {name}: timed out`. |
| F12 | scripts/pre-commit:7-8 | `py=python3` / `command -v "$py" >/dev/null 2>&1 \|\| py=python` | Preventive measure | low | On Windows (a platform the hook supports, line 4), `python3` often resolves to the Microsoft Store alias in `WindowsApps`. `command -v` finds it, but running it prints an install hint and exits non-zero, so every commit is blocked with a misleading message. README.md:263 and check.py:50 tell Windows users to use `py -3`, which the hook never tries. Whether a given machine hits this depends on its PATH (H3). | Abductive | 55 | Try the interpreter, not only its presence: `for c in python3 python py; do "$c" -c 'import sys; sys.exit(sys.version_info < (3, 8))' 2>/dev/null && { py=$c; break; }; done` (with `py -3` when the candidate is `py`). |
| F15 | scripts/check.py:361-366 | `if fence is None: fence = f.group(1)[0] else: fence = None` | Preventive measure | low | Any fence line closes an open fence, even one of the other character or a shorter run. CommonMark requires the same character and at least the same length. A ```` ```` ```` block that shows a `~~~` or ```` ``` ```` example ends the fence early. The rest of the block is then checked as Markdown, or the real closing fence opens a new fence, so tables after it are skipped. Nothing shows this in today's docs (not searched exhaustively). | Deductive | 80 | Close only on `s.startswith(open_char * open_len)` with the same character and a length of at least the opening fence. |
| F17 | scripts/pre-commit:12 | `if git diff --cached --name-only \| grep -q '^skills/adversarial-verify/evals/'; then` | Preventive measure | low | (HB3) A commit that changes only `scripts/check_facts.py` does not trigger the facts run, so a runner broken by that very commit (for example one that no longer fails on a false fact) is committed without being exercised. Nothing shows this happening. Likelihood: low, because the runner rarely changes. | Deductive | 85 | Extend the filter to `'^\(skills/adversarial-verify/evals/\|scripts/check_facts\.py$\)'`. |
| F16 | scripts/check.py:345 | ``s = re.sub(r"`[^`]*`", "x", line)`` | Preventive measure | low | The checker treats a pipe inside a code span as content. My understanding of the GitHub Flavored Markdown table rule (cells split before inline parsing, so a pipe inside a span must be escaped) is that GitHub renders such a row with an extra cell. If so, the check passes a table that renders broken, and `test_escaped_pipe_and_code_span_are_not_separators` (test_check.py:441-443) enshrines that. I did not read the GFM spec (it is outside `./tree`), and I found no such row in today's docs; my search at README.md:229-238 found no span holding a pipe. | Abductive | 50 | If H4 confirms the rule, count unescaped pipes inside code spans as separators (or report them as an error asking for `\|`). |

## STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|
| S1 | Scale Shift | C1 (`check_evals` at 10× evals and at zero) | yes | 85 | 570 evals: `ids.count(i)` (check.py:203) is O(n²), about 325k comparisons, which is negligible. Zero: `not evals` → "no 'evals' list" (171-173). Negative or zero ids fail the consecutive check (206). |
| S2 | Time Travel | C16/C17 (the magic numbers `TAGGED_FROM = 21`, `FACTS_FROM = 29`) | yes | 80 | Both are named constants with a comment (check.py:74,77), restated in the docstring (8, 34) and README.md:248,254, and pinned by the boundary tests (test_check.py:149-159). A maintainer in 6 months finds why they exist. |
| S3 | Requirement Inversion | C13 (`--staged` checks the index, not the working tree) | yes | 85 | The inverse need (check the working tree) is the default mode (check.py:434-435). Both directions are tested (test_check.py:382-387, 502-510). Terms always come from the working repo (423), which is correct in both directions. |
| S4 | Existence Question | C11 (the Latin-1 fallback of `decode`) | yes | 85 | Delete it mentally: any non-UTF-8 tracked file would raise in `read_text` → `check_private` would report "unreadable" and stop scanning that file's content for terms. It must exist. `test_latin1_file` (test_check.py:296-298) pins it. |
| S5 | Scale Shift | C21 (the "last line is `ok <id>`" rule) on a file printing 0 lines | yes | 85 | `out[-1:]` on an empty list is `[]`, which differs from `["ok N"]` → FAIL (check_facts.py:107-109). No IndexError. |

## HYPOTHESES (Abductive — require further investigation)
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| H1 | Three tests contradict the code by trace (F1, F2, F3), and nothing in `./tree` runs `test_check.py` automatically: the hook runs only `check.py` and `check_facts.py` (pre-commit:9,15), and there is no CI configuration in `./tree` | The suite was not run after the last changes to `check.py`, or the three tests were written first (evals-first) and the fixes are pending | The suite runs in a CI outside `./tree` and these failures are known | `python3 -m unittest scripts/test_check.py -v` in a copy (P1) |
| H3 | pre-commit:7-8 picks the first `python3` on PATH | On some Windows machines this is the Store alias and every commit fails (F12) | Git for Windows' PATH puts a real Python first, or users have `python3` installed | On a Windows machine: `sh -c 'command -v python3; python3 -c "print(1)"'` |
| H4 | check.py:345 excludes pipes in code spans | GitHub renders those rows with an extra cell (F16) | GitHub's renderer treats code spans first | Render a test table with `` `a|b` `` in a cell on GitHub (a preview of an untracked gist or a draft PR; an outward-facing action, so it needs your approval) |
| H5 | `scripts/pre-commit` must be executable for the symlink install (pre-commit:3) to work, and the file mode is not visible by reading | The file is tracked as `100755` | It is `100644` and the hook silently does not run (git ignores non-executable hooks with a hint) | `git ls-files -s scripts/pre-commit` (read-only) |

## HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| HB1 | check.py:145-158 | "the files tracked by git (all files outside .git if git is not available)" (check.py:46-47) | It also falls back to **every** file, untracked ones included, when git is available but `root` is not a repo or **has zero tracked files** (150: `if files: return files`) | Documentation drift, see D-F1 | 90 |
| HB2 | pre-commit:9,15 | "run the repository invariant checks on exactly what is staged" (pre-commit:2) | The *content* checked is the staged one, but the *checkers* are the working-tree `scripts/check.py` and `scripts/check_facts.py`. A staged change to the checkers is not what judges the commit, and a staged-only weakening of a checker is never exercised. | Not a problem by itself (it is the usual hook pattern). Noted for review. | 85 |
| HB3 | pre-commit:12 | facts run "only when the staged change touches the evals" | A change to `scripts/check_facts.py` itself (the runner) does not trigger a run, so a broken runner is committed unexercised | Preventive measure, low: FAIL row F17 | 85 |
| HB4 | check.py:436 | — | With `--staged` and an empty index, no check runs and the summary reads `checked (staged content): — 0 error(s)` | No (git refuses an empty commit) | 80 |
| HB5 | check_facts.py:57 | fact files are "run" | They run with `-E -s` but not `-I`, so the facts folder is on `sys.path` (needed for `from _parse_day import …`, 37.py:3), and they execute arbitrary code at commit time (acknowledged at pre-commit:11) | No (advertised at pre-commit:11) | 85 |

## ADVERSARIAL SCAFFOLD FINDINGS
- **Reviewer blind spots:** `[\W_]?` reads as "a separator" and the `?` looks harmless (F2). `term_patterns(terms)` looks equivalent to the substring call that the comment above it describes (F3). A hook line that "obviously" mirrors the README is missing one flag (F4). A `continue` after a `print("skip …")` looks like graceful degradation (F6).
- **Highest-risk claims:** (1) C15/I6, the hook without `--strict` (F4): every commit on an unconfigured clone; (2) C6/I3, multi-character separators and CRLF (F2): silent private-name leak into a public repo; (3) C9/I4, the terms list itself committable (F5): the whole list leaks.
- **Multi-step traces:** a missing rustc → `check_facts.py:91-93` prints skip → `113` returns 0 → `pre-commit:17` prints nothing on rc 0 → the commit passes with Rust facts unverified, and `test_check.py:575-578` is green in that same environment (T-F2). A CRLF checkout on Windows (Git for Windows default `core.autocrlf=true`) → `decode` keeps `\r\n` → `SEP` matches one char → a two-word term split over lines is not detected → the hook (no `--strict` needed here; terms are configured) passes → pushed.
- **Subtlety flags:** check.py:90 (one-character `?`), check.py:223 (`[:1]` slice), check.py:400 (missing keyword argument), check.py:301 (an exemption with no matching error), check_facts.py:93 (`continue` without `failed += 1`).

---

# DOMAIN 2 — TESTS (`scripts/test_check.py`)

## VERIFICATION DOMAIN
Tests

## GROUND TRUTH
- The production code under test: `scripts/check.py`, `scripts/check_facts.py`. `scripts/pre-commit` is the production path into `check.py`.
- The test bootstrap and helpers: `Base.setUp` (test_check.py:30-37), `run_check` (42-52), `assert_fails` / `assert_passes` / `assert_no_leak` (54-73).
- The fixtures the tests mutate: evals.json, facts/38.py:21, 40.py:1,13, 49.py:12-14, 51.py:1, NOT_COMPUTABLE:4, README.md:1, CHANGELOG.md:5,10, plugin.json:2-4.
- The production configuration it should reproduce: the hook runs `check.py -I --staged` from a git repo on the developer's machine (pre-commit:9), with whatever toolchains are installed.

**Test bootstrap review (would results be the same in production?):** `Base.setUp` copies the repo into a fresh `mkdtemp` that is **not** a git repository. So every test outside `StagedTest` and `test_staged_content_is_what_is_checked` exercises the `os.walk` fallback of `list_files` (check.py:153-158), not the `git ls-files` path that production uses (an untracked file is checked in the tests but not in production). `run_check` passes the parent's full environment plus `-I` (test_check.py:43,50), which matches the hook's `-I`. `run_facts` (571-573) runs with the host's toolchains, which is the source of T-F2.

## INVARIANTS
Same invariants as Domain 1 (I1-I9). For the test domain: the mechanism for each is listed there with its test name. I2, I3 and I5 have tests that bite (they are red against the current code, by trace). I4 and I6 have **no test that bites**: `test_terms_file_is_gitignored` checks only `.gitignore` (365-366), and nothing tests the hook. I7's test is green even when the invariant is broken (T-F2).

## DECOMPOSED CLAIMS
1. T1 Every invariant of check.py has at least one negative test that fails when it is broken — Mode: Deductive
2. T2 `test_file_nobody_names` fails when an unnamed reference file is not reported — Deductive
3. T3 `test_runner_passes_on_the_repo` shows that every fact file was executed and is true — Deductive
4. T4 No private test term appears literally in any repo file, including the test file — Deductive
5. T5 `assert_fails` counts a failure only when the script ran to its summary and reported an ERROR naming what failed — Deductive
6. T6 No private test term is ever printed (test_check.py:4-5) — Deductive
7. T7 The tests give the same result on every developer platform the repo supports (Linux, macOS, Windows per pre-commit:4 and README.md:263) — Deductive
8. T8 `test_staged_outside_git_is_a_clear_error` proves that the temp directory is removed — Deductive
9. T9 The comment of each test matches what it exercises — Deductive
10. T10 The suite covers check_facts.py's toolchain rule, the hook, CRLF input, a tracked terms file and a relative `--root` — Deductive (absence probe)
11. T11 The fixtures the tests edit exist (so edits do not silently no-op) — Deductive

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| **Tautological test** | T-F1 (`r.stdout + self.ref("orphan.md")` always contains "orphan.md") | test_check.py:479 |
| **Test-environment artifact** | T-F2 (a missing toolchain → green), T-F3 (symlink privilege → false red on Windows), T-F4 (global git config → false red; a test lacking the git skip), bootstrap note (the os.walk path instead of git ls-files) | test_check.py:350-352, 369-380, 502-505, 575-578 |
| **Missing negative tests** | T-F6 | test_check.py (absent cases) |
| **Test-code drift** | T-F7 (a comment describes whole-word detection with a plain term) | test_check.py:336-339 |

## VERIFICATION RESULTS

### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| T4 | No literal test term in the repo | test_check.py:24-26 build `NONE`, `T1`, `T2` by concatenation, so the file holds `"zq" + "vorblax"`, which never matches the contiguous pattern. `T2`'s source pieces (`"quil" + "lane " + …`) are separated by `" + "` (more than one character), so even the one-char `SEP` (check.py:90) does not join them. Test-environment check: none needed; this is a static property of the file. |
| T5 | `assert_fails` is strict | test_check.py:54-62: non-zero exit, `"checked ("` summary present (so not a crash), `"ERROR"` present, every token present, and no leak. A traceback (F9) would fail it, which is correct. |
| T8 | Temp-dir cleanup is really checked | test_check.py:389-396 take a listing of `check-staged-*` before and after in the same `tempfile.gettempdir()` that check.py uses (428). The test could fail: removing `finally` (check.py:438-440) would leave a dir. Production-equal: same function, same temp root. |
| T11 | The fixtures edited by the tests exist | `edit` asserts `old in s` (test_check.py:80), so a missing fixture fails loudly. Verified by reading: facts/38.py:21 `assert round(10.05 * 0.9, 2) == 9.05`; 49.py:12-14 the three `assert clipped(…)`; 40.py:1 `# prompt-sha256:` and 40.py:13 `print('ok 40')`; README.md:1 `badge/skill-v`; NOT_COMPUTABLE:4 `30:`, where eval 30 states facts (evals.json:381). `evals[36]` is id 37 (ids consecutive, evals.json:462) and contains `day > 31` (evals.json:463). The non-`edit` replacement at 550 has no presence assert, but if the text vanished the test would go red (no hash error), not green. |
| T1 (partial) | Negative tests per invariant | `EvalsTest` (I1), `VersionTest` (I2), `PrivateTest` (I3, I5), `NeutralTest`, `TablesTest`, `ReferencesTest` (I9), `FactsTest` (I8, I7 partly). The exceptions are listed in T-F6. |

### FALSIFIED HYPOTHESES
| # | Location | Suspected defect | Check (quote) | Status (falsified / conditionally) | Could it have failed? (how shown, or the check that would complete it) | Paths not covered | Mode | Confidence |
|---|----------|------------------|-------|------------------------------------|------------------------------------------------------------------------|-------------------|------|------------|
| FH4 | test_check.py:417 | `test_evals_are_excluded` is tautological, because `check_neutral` never reads evals.json | `self.assertNotIn("evals.json", r.stdout.split("checked (")[0])` after asserting `SQLite` is in evals.json (414) | conditionally falsified | It can fail: if `EVALS` were added to `skill_docs` (check.py:140-142), the `SQLite` hit (a STACK_TERM, check.py:84) would print `WARNING skills/…/evals.json:N`. That is shown by trace, not by a mutant run. The check that completes it: red with `EVALS` added to `skill_docs`. | Other files that are not skill docs (only evals.json is probed) | Deductive | 75 |

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| T-F1 | scripts/test_check.py:479 | `self.assertIn("orphan.md", r.stdout + self.ref("orphan.md"))` | Demonstrated defect | low | The haystack contains `self.ref("orphan.md")`, which always contains `"orphan.md"`, so the assertion is always true. It also never checks the exit code. Delete `check.py:519-520` and this test is still green. The case is partly covered by `test_file_named_only_by_another_reference_file_is_still_unnamed` (481-485), which uses the same code path. | Deductive | 95 | `self.assert_fails(r, "orphan.md", "never named in SKILL.md")`. |
| T-F2 | scripts/test_check.py:575-578 | `self.assertEqual(r.returncode, 0, …)` / `assertRegex(r.stdout, r"\d+ fact file\(s\), 0 failed")` | Demonstrated defect (test-environment artifact) | medium | On a host without `rustc` or `node`, `52.rs` and `53.ts` print `skip` (check_facts.py:92) and the exit is 0 (113). The test is green, and its name ("passes on the repo") is read as "every fact holds" when two of 13 files never ran. This is the test half of F6. | Deductive | 88 | Assert `"skip" not in r.stdout` (it becomes a red with F6's fix anyway). Add a test that runs with a `PATH` lacking `rustc` and expects a non-zero exit. |
| T-F3 | scripts/test_check.py:350-352 | `os.symlink(os.path.join(self.tmp, "does-not-exist"), self.path("dangling.md"))` | Preventive measure (false red) | low | On Windows without Developer Mode or admin rights, `os.symlink` raises `OSError` (WinError 1314), so the test errors before reaching the code. The repo explicitly supports Windows (pre-commit:4; README.md:263). The code under test (check.py:306-310) is fine; only the test environment fails. | Deductive | 75 | Create the unreadable file another way (a directory named `dangling.md` makes `open` raise `IsADirectoryError`/`PermissionError` on every platform), or `skipUnless` symlinks can be created. |
| T-F4 | scripts/test_check.py:369-380, 502-505 | `self.git("commit", "-q", "-m", "base")` / `git = lambda *a: subprocess.run(["git", … "-c", "user.email=t@t", *a]` | Preventive measure (false red) | low | Both helpers inherit the developer's global git config. With `commit.gpgsign=true` (no agent in the test shell) or a global `core.hooksPath` hook, `git commit` fails, so `CalledProcessError` and a red with no defect. `ReferencesTest.test_staged_content_is_what_is_checked` (502) also lacks the `@skipUnless(shutil.which("git"))` that `StagedTest` has (369), so without git it errors instead of skipping. | Deductive | 80 | Pass `-c commit.gpgsign=false -c core.hooksPath=/dev/null` (or `GIT_CONFIG_GLOBAL=/dev/null` in `env`) and add the skip decorator to the staged test in `ReferencesTest`. |
| T-F5 | scripts/pre-commit:9-17 (absence) | (no invocation of `test_check.py`) | Preventive measure | medium | The suite is the mechanism that bites for I2, I3 and I5, and by trace three of its tests are red today (F1, F2, F3). Nothing in `./tree` runs it automatically: I looked at pre-commit:1-18 and the full file list of `./tree` (no `.github/`, no CI config), and found no other runner. A red suite can therefore coexist with green commits indefinitely, which is the situation H1 describes. | Deductive | 85 | Run `python3 -I -m unittest scripts/test_check.py` in CI, or in the hook when `scripts/` is staged. |
| T-F6 | scripts/test_check.py (absent cases) | — | Preventive measure | medium | No test for: the hook itself (so F4 cannot be caught); a missing toolchain in check_facts.py (F6); a two-word term split across a **CRLF** line (F2's CRLF form); a tracked or staged `.check-private-terms` (F5); a relative `--root` for check_facts.py (F7); two fact files for one id (F10); an inline `#` comment in the terms file (DA-F1). I searched all 622 lines of test_check.py for each. | Deductive | 85 | Add one test per case. Each is a regression guard for a finding in this report. |
| T-F7 | scripts/test_check.py:336-339 | `# whole-word detection does not flag "<term>labs", but the evals check prints the key name` / `self.run_check(terms=T1)` | Demonstrated defect (test-code drift) | low | The comment describes whole-word detection, but `terms=T1` has no `=`, so detection is substring and **does** flag `zqvorblaxlabs` (check.py:265). The test therefore duplicates `test_leak_through_another_check_is_masked` (331-334) instead of testing "masked even if not detected". The case the comment describes is the one at 341-344. | Deductive | 90 | Fix the comment, or delete the test as redundant with 331-334 and 341-344. |
| T-F9 | scripts/test_check.py:30-37 | `shutil.copytree(src, dst, …)` into `tempfile.mkdtemp()` (not a git repository) | Preventive measure (test-environment artifact) | low | (HB6) Every test outside `StagedTest` and `test_staged_content_is_what_is_checked` runs check.py on a copy that is not a git repository, so `list_files` takes the `os.walk` fallback (check.py:153-158). Production (the hook, and a plain run in a clone) takes the `git ls-files` path (147-150). A defect only on the git path (for example decoding of `-z` names, or tracked-but-deleted files) would not show in these tests. Only the staged tests cover git. | Deductive | 85 | Run `RepoTest` (and one private-terms test) a second time on a `git init`-ed copy with everything added. |
| T-F8 | scripts/test_check.py:4-5, 64-68 | "no private test term may ever be printed" / `assert_passes` (no `assert_no_leak`) | Preventive measure | low | `assert_no_leak` is called only from `assert_fails` (62). Passing runs that use T1 (329, 387, 401-402, 257) and the `run_facts` tests never check for leaks, so a leak through a `WARNING` line on a passing run would go unnoticed, against the file's own rule. | Deductive | 85 | Call `self.assert_no_leak(r)` in `assert_passes` too. |

## STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|
| S6 | Existence Question | T4 (terms built at run time) | yes | 85 | Without it, the test file would itself contain the terms, and `check_private` would fail every test that configures them. The construction is essential. |
| S7 | Time Travel | T11 (fixtures pinned to specific lines of facts files and evals) | yes | 80 | When facts/38.py or 49.py change, `edit` (80) fails loudly with the missing text. `test_prompt_changed_after_its_facts` depends on `evals[36]` and `day > 31` but goes red, not green, if they drift. Fragile but never silently green. |
| S8 | Scale Shift | T8 / the bootstrap (copy of the repo per test, about 75 tests) | yes | 75 | Each test copies README, CHANGELOG, skills, .claude-plugin, scripts and .gitignore (30-37), a few hundred kB. At 10× tests the cost is linear disk I/O; `tearDown` always removes the copy (39-40). No shared state between tests. |

## HYPOTHESES (Abductive — require further investigation)
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| H1 | (same as Domain 1) three tests red by trace | the suite has not been run since check.py changed | run in an external CI with the failures known | P1 |
| H6 | The bootstrap uses a non-git temp dir, so `list_files` takes the `os.walk` path | If `TMPDIR` lies inside some git working tree, `git -C tmp ls-files` succeeds with an empty list and still falls back, so the result is the same | A `TMPDIR` inside a repo where these paths are tracked would change which files are scanned | Run the suite with `TMPDIR` set inside a git repo (P1 variant) |

## HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| HB6 | test_check.py:30-37 | the tests check "the repo" (`test_repo_passes`) | They check a **non-git** copy, so the os.walk path (check.py:153-158) and not the git ls-files path (147-150) that production uses. Untracked files in the developer's working tree are copied only if under the copied items | Test-environment artifact, low: FAIL row T-F9 | 85 |

## ADVERSARIAL SCAFFOLD FINDINGS
- **Reviewer blind spots:** `r.stdout + self.ref(…)` reads like a helpful message argument (T-F1). A green "runner passes on the repo" hides skips (T-F2).
- **Highest-risk claims:** T10 (no hook test, so F4 is invisible), T3 (green without toolchains), T-F5 (red tests that gate nothing).
- **Multi-step traces:** F2 is introduced → `test_two_words_joined_any_way` goes red → nothing runs the suite (T-F5) → the hook stays green → the defect ships.
- **Subtlety flags:** test_check.py:479 (the haystack includes the needle); 337 (stale comment); 502 (a missing skip decorator).

---

# DOMAIN 3 — DOCUMENTATION (docstrings, comments, usage text and error messages in the four files)

## VERIFICATION DOMAIN
Documentation

## GROUND TRUTH
The code those texts describe (traced in Domains 1-2), plus README.md:244-263 and CHANGELOG.md:3 as the project's other statements of the same rules.

## INVARIANTS
No invariant is specific to the text. The texts restate I1-I9. Respected? A restatement is respected when the code does what it says. The ones contradicted are counted once, in their primary domain (Code): check.py:10 vs F1; check.py:16-17 vs F2; check.py:22-23 and 399 vs F3; pre-commit:5 vs F4; check_facts.py:8 vs F6.

## DECOMPOSED CLAIMS
1. D1 check.py:4 "Errors make the exit code non-zero; warnings are printed but do not block" — Deductive
2. D2 check.py:46-47 "Files checked: the files tracked by git (all files outside .git if git is not available)" — Deductive
3. D3 check.py:49-50 usage line and "Requires Python 3.8 or later" — Deductive
4. D4 check.py:24-26 "Not caught: …" limitation list — Deductive
5. D5 check_facts.py:6-9 how each language runs, and "types stripped, not type-checked" — Deductive
6. D6 check_facts.py:11-14 the assertion and `ok <id>` rule — Deductive
7. D7 check_facts.py:16-18 usage examples — Deductive
8. D8 pre-commit:3-4 install instructions (symlink; copy on Windows) — Deductive
9. D9 test_check.py:3 "Run from the repo root: python3 -m unittest scripts/test_check.py" — Deductive
10. D10 Error messages name what failed and how to fix it (for example check.py:482, 501, 520) — Deductive
11. D11 check.py:35-36 "has a file facts/<id>.py|.rs|.ts (run by scripts/check_facts.py)" — Deductive

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| **Stale or partial description** (text promises a broader rule than the code) | D-F1, plus the cross-domain items F1, F2, F3, F4, F6 counted in Code | check.py:10,16-17,22-23,46-47,399; check_facts.py:8; pre-commit:5 |

## VERIFICATION RESULTS

### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| D1 | Exit-code rule | check.py:442 `return 1 if rep.errors else 0`. Warnings never set it. |
| D3 | Usage and Python ≥ 3.8 | argparse at check.py:418-421 accepts exactly `--strict`, `--staged`, `--root`. Features used: `capture_output`/`text` (3.7), f-strings, `str.casefold`, `yield from`. No walrus, no `removeprefix`, no 3.9+ API found in the 4 files. |
| D4 | "Not caught" list is honest | One-word-as-two-words: a single part cannot match across a separator. UTF-16 without BOM: `decode` (114) tests only BOMs. `=` glued forms: by construction (275). It omits F2's multi-character separators, which belong to Code F2. |
| D5 | Per-language run | check_facts.py:57 (`sys.executable`), 63 (`rustc --edition 2021 -O`, then the binary), 67 (`node --experimental-strip-types`). Strip-types is not a type check. |
| D6 | Assertion and `ok` rule | check_facts.py:42-51, 95-109 (traced as C21). |
| D8 | Install | `ln -s ../../scripts/pre-commit .git/hooks/pre-commit`: a relative target from `.git/hooks/` resolves to `<repo>/scripts/pre-commit`. The executable bit cannot be seen by reading (H5). |
| D9 | Running the tests | `python3 -m unittest scripts/test_check.py`: unittest turns the path into `scripts.test_check`, importable from the repo root as a namespace package (no `__init__.py` needed). The test locates the repo from `__file__` (17), not the cwd. Confidence capped because it is run-only to confirm. |
| D10 | Actionable messages | check.py:482 gives the exact hash to set; 501 names both remedies; 520 explains why an unnamed file matters; 202 names the tag format. |
| D11 | "run by scripts/check_facts.py" | Accurate: check.py never runs fact files; the runner does (check_facts.py:99-104). |

### FALSIFIED HYPOTHESES
None: no suspicion in this domain was checked and found clean.

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| D-F1 | scripts/check.py:46-47 | "Files checked: the files tracked by git (all files outside .git if git is not available)." | Demonstrated defect | low | `list_files` (145-158) also falls back to **every** file, untracked ones included, when git is installed but `--root` is not a repository, or when it is a repo with **zero tracked files** (`if files: return files`, 149-150). A user running `check.py --root some/export` (not a repo) gets untracked build output or virtualenvs scanned and reported, which the docstring says will not happen. | Deductive | 90 | Say "the files tracked by git; every file outside .git when git is unavailable, the root is not a repository, or nothing is tracked yet". |
| D-F2 | scripts/check_facts.py:16-18 | `python3 scripts/check_facts.py --root DIR      # the files under another checkout` | Demonstrated defect | low | The example accepts any DIR, but a relative DIR makes every file FAIL (F7). Counted once in Code as F7, and listed here because the text is the user's entry point. | Deductive | 85 | Fix F7 (absolute path); no text change needed then. |

> D-F2 duplicates F7 for the reader's sake. It is **not** counted again in the totals.

## STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|
| S9 | Time Travel | D4 (the "Not caught" list) | yes | 80 | A future maintainer can tell which gaps are deliberate. Every item is reachable from the code (114, 275). The one undocumented gap (F2) is a code defect, not an omission of a deliberate limit. |
| S10 | Requirement Inversion | D10 (actionable messages) | yes | 80 | Inverted, a user who wants *no* hint (for example CI log noise): messages are single lines, and the hint lives in the same line, so no multi-line spam. |
| S11 | Existence Question | D11's parenthetical "(run by scripts/check_facts.py)" | yes | 80 | Delete it and the reader of check.py would assume check.py executes facts. It prevents that misreading. |

## HYPOTHESES (Abductive — require further investigation)
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| H5 | (see Domain 1) the install instruction needs an executable file | tracked as 100755 | tracked as 100644 | `git ls-files -s scripts/pre-commit` |

## HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| HB1 | check.py:46-47 | see D-F1 | see D-F1 | counted as D-F1 | 90 |

## ADVERSARIAL SCAFFOLD FINDINGS
- **Reviewer blind spots:** the docstrings are precise and long, which invites trust. Five of their promises are broader than the code (cross-domain list above).
- **Highest-risk claims:** pre-commit:5 (it describes a flag the hook does not pass), check_facts.py:8 (it promises the opposite of the code), check.py:22-23 (the masking promise).
- **Multi-step traces:** a reader trusts check.py:22-23 → configures `=`-prefixed terms → a glued form in an eval key is printed to a CI log (F3).
- **Subtlety flags:** check.py:399, a comment that describes the intent and contradicts the very next line.

---

# DOMAIN 4 — DATA (formats the scripts parse and enforce)

## VERIFICATION DOMAIN
Data

## GROUND TRUTH
`skills/adversarial-verify/evals/evals.json` (ids at lines 5…711, "(Facts" markers), `facts/NOT_COMPUTABLE:1-12`, the fact-file headers (`facts/37.py:1`, `38.py:1`, `40.py:1`, `49.py:1`, `51.py:1`, `52.rs:1`, `53.ts:1`), `README.md:1-4`, `CHANGELOG.md:5,10`, `.claude-plugin/plugin.json:3`, `SKILL.md:20`, `.gitignore:1`. These are the data already in the field, read against the parsers in check.py.

## INVARIANTS
I1 and I8 (Domain 1) are the data contracts. Against the data in the field, both are respected (DA1, DA3).

## DECOMPOSED CLAIMS
1. DA1 The current evals.json satisfies the contract: ids 1..57 consecutive, and the eval-21 and eval-20 boundary as tested — Deductive
2. DA2 Every eval from 29 on that states facts has exactly one of a fact file or a NOT_COMPUTABLE reason — Deductive
3. DA3 Every fact file in `facts/` belongs to an existing eval and has a `prompt-sha256:` line in its first 2000 characters — Deductive
4. DA4 The version data agree: SKILL.md, the README badge, plugin.json and the newest CHANGELOG entry — Deductive
5. DA5 The private-terms file format is "one per line, # for comments" — Deductive
6. DA6 NOT_COMPUTABLE rejects malformed, duplicate or meaningless entries — Deductive
7. DA7 The stored hashes equal sha256 of the current prompts — Deductive (run-only)

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| **Silent fallthrough** (malformed input accepted with a changed meaning) | DA-F1 (an inline `#` comment becomes part of the term), DA-F2 (duplicate or unknown ids in NOT_COMPUTABLE accepted) | check.py:255-256, 483-496 |

## VERIFICATION RESULTS

### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| DA1 | evals.json ids | The 57 `"id": N` entries at evals.json:5…711 run 1..57 in order. Eval 20 is untagged (evals.json:269) and eval 21 is tagged (evals.json:282). |
| DA2 | Facts coverage | Evals ≥ 29 with "(Facts": 30, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 43, 45, 48, 49, 50, 51, 52, 53, 56, 57 (evals.json:381…712). Fact files: 35, 37, 38, 39, 40, 42, 48, 49, 51, 52, 53, 56, 57. NOT_COMPUTABLE: 30, 32, 33, 34, 36, 41, 43, 45, 50 (NOT_COMPUTABLE:4-12). Every stating eval is covered exactly once, with no overlap. 42 has a file without "(Facts", which is allowed. |
| DA3 | Fact files' membership and header | Every stem is an id from 1..57. Each header is on line 1 (for example 37.py:1, 52.rs:1, 53.ts:1) with 64 lowercase hex characters, matching check.py:477. `_parse_day.py` is excluded by its `_` prefix (check.py:469). |
| DA4 | Version agreement | SKILL.md:20 `"4.2"` = README.md:1 `skill-v4.2` = plugin.json:3 `"4.2"` = CHANGELOG.md:10 `## 4.2` (CHANGELOG.md:5 `## Unreleased` is skipped by the numeric regex). |

### FALSIFIED HYPOTHESES
None.

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| DA-F1 | scripts/check.py:255-256 (with 266) | `terms = [l for l in … if not l.strip().startswith("#")]` | Preventive measure | medium | The terms file allows only whole-line comments, but nothing rejects an inline one. A user writes `acmecorp  # old client`. The term becomes the parts `["acmecorp","old","client"]` (266), which matches only the literal sequence "acmecorp old client". The real name `acmecorp` is **silently no longer protected**, and no warning is given (the term has letters and is long). The docstring (check.py:15) and README.md:250 say "one per line, # for comments", which invites the inline form. | Deductive | 85 | Strip inline comments (`l.split("#", 1)[0]`), or warn when a term contains `#`. |
| DA-F3 | scripts/check.py:500 | `if "(Facts" in str(e.get("prompt", "")) and …` | Preventive measure | low | (HB7) Only the case-sensitive literal `(Facts` marks a prompt as stating facts. A new eval written as `(facts: …)` or `Facts: …` escapes the "fact file or reason" requirement with no error. Nothing shows this today: all 21 stating evals use `(Facts` (evals.json:381…712). | Deductive | 85 | Match case-insensitively (`re.search(r"\(\s*facts\b", prompt, re.I)`), or reject a lowercase marker with an error. |
| DA-F2 | scripts/check.py:494 | `reasons[int(m.group(1))] = m.group(2)` | Preventive measure | low | Duplicate ids in NOT_COMPUTABLE are overwritten silently. Reasons for an id that does not exist, is below 29, or no longer states facts are never reported. The file can accumulate stale reasons that hide nothing today but mislead a reader about which evals are uncomputable. Nothing shows this in the current data (NOT_COMPUTABLE:4-12 are unique and all state facts). | Deductive | 85 | Report a duplicate id, and a reason for an eval that does not exist or does not state facts. |

## STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|
| S12 | Scale Shift | DA3 (the header within the first 2000 chars) | yes | 80 | At 10× file size the header still sits on line 1 by convention, and `[:2000]` bounds the scan. At zero size, no header → a clear error (check.py:479-480). |
| S13 | Requirement Inversion | DA2 (facts must have a file **or** a reason) | yes | 80 | Inverse: an eval with both is forbidden (check.py:495-496), and one with neither fails (500-501). Both directions are enforced and tested (test_check.py:523-526, 562-565). |
| S14 | Time Travel | DA4 (the CHANGELOG "## Unreleased" convention) | yes | 80 | A later "## 4.3" entry placed above "## 4.2" becomes the newest, as intended. A textual "## Unreleased" never satisfies or breaks the check. |

## HYPOTHESES (Abductive — require further investigation)
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| H7 | DA7: the hashes cannot be computed by reasoning | each stored `prompt-sha256` equals the sha256 of the current prompt (the repo's own check enforces it) | a prompt was edited after its file without re-hashing | `python3 scripts/check.py` (check 6), P1 |

## HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| HB7 | check.py:500 | an eval "whose prompt states facts" | only the case-sensitive literal `(Facts` counts. `(facts:` or `Facts:` without the parenthesis escape the requirement | Preventive measure, low: FAIL row DA-F3 | 85 |

## ADVERSARIAL SCAFFOLD FINDINGS
- **Reviewer blind spots:** a comment syntax that is only half implemented (DA-F1).
- **Highest-risk claims:** DA5 (the terms file is the root of the privacy guarantee), DA2, DA7.
- **Multi-step traces:** an inline comment in the terms file → a term that never matches → `check_private` is green → the private name is committed.
- **Subtlety flags:** check.py:255 (a `startswith("#")` that looks complete).

---

# DOMAIN 5 — UX (the terminal output of the three scripts)

## VERIFICATION DOMAIN
UX (command-line interface). I applied `references/ux.md`, adapted to a terminal: render, legibility, real content, states, sensitive data. Contrast, targets, focus and motion do not apply: the output is plain text in the user's terminal theme, with no colour of its own.

## GROUND TRUTH
The output code: check.py:523-527 (report), 397-414 (masking); check_facts.py:92,96,102,108,111-112; pre-commit:17. The project's own guideline: terms are never printed (check.py:22-23).

## INVARIANTS
I5 (no term printed) is the UX "sensitive data" target. It is counted in Code as F3 and F2.

## DECOMPOSED CLAIMS
1. U1 Every run of check.py ends with a one-line summary: scope, checks run, error and warning counts — Deductive
2. U2 Each error is located (path or path:line) where the location is not itself sensitive — Deductive
3. U3 check_facts.py makes skipped files as visible as failed ones — Deductive
4. U4 The hook shows the user only what they need: check.py always, facts output on failure — Deductive
5. U5 The output can always be printed, whatever the characters in file names and keys — Deductive

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| **Assumed environment** (output encoding) | U-F1 | check.py:525 |
| **Silent fallthrough** (state hidden from the user) | U3, counted in Code as F6 | check_facts.py:92; pre-commit:17 |

## VERIFICATION RESULTS

### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| U1 | Summary line | check.py:526-527 `checked (working tree\|staged content): evals, version, … — N error(s), M warning(s)`. Printed on every non-crashing path, including `--staged` outside git (441 is after `finally`). The crash paths are F8 and F9. |
| U2 | Locatable errors | Content hits carry `path:line` (check.py:321). Table errors carry `path:line` and the header line (373, 378). When the path itself contains a term, the location is replaced by an explicit placeholder (410), which is the right trade-off for the stated guideline: the user knows their own terms and can search locally. |
| U4 | Hook verbosity | pre-commit:9 lets check.py print directly. pre-commit:15-17 capture the runner and print it only on failure, which keeps a passing commit quiet. The cost of that choice is F6. |

### FALSIFIED HYPOTHESES
None.

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| U-F1 | scripts/check.py:525 (also 527) | `print(line)` | Preventive measure | low | Under the hook, stdout is a pipe to git. On Windows, Python then encodes with the ANSI code page (for example cp1252) with `errors="strict"`. `-I` (pre-commit:9) also disables `PYTHONIOENCODING`/`PYTHONUTF8` from the environment. An error line that carries a file name or an eval key with a character outside that code page (for example CJK, `→`) raises `UnicodeEncodeError`. The report is cut short, with a traceback and no summary (exit non-zero, so it still blocks). This depends on the Python version and the system code page, so it is not demonstrated. | Deductive | 60 | `sys.stdout.reconfigure(errors="backslashreplace")` at the start of `main()` (Python 3.7+), or pass `-X utf8` in the hook. |

> U3 (skips not visible under the hook) is a UX symptom of F6 and is counted there.

## STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|
| S15 | Scale Shift | U1 (the summary with 0 and with 1,000 errors) | yes | 80 | 0 errors: the same one line. 1,000 errors: errors print before warnings (524), each on one line, and the summary is last, so it is always the line the user sees at the bottom. |
| S16 | Requirement Inversion | U2 (hiding locations that contain a term) | yes | 75 | Inverse: a user who wants the location printed. The location is withheld only when it contains a term, and the message still names the term's index (`#k`), which is enough to find it locally. |
| S17 | Existence Question | U4 (capturing the facts output in the hook) | yes | 75 | Delete the capture and passing commits print 13+ `ok` lines each time, which is noise. The capture should exist; the fix belongs in F6 (make a skip fail), not in removing the capture. |

## HYPOTHESES (Abductive — require further investigation)
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| H8 | U-F1 depends on how the platform encodes a piped stdout | it raises on Windows with a non-UTF-8 ANSI code page | the user's Python runs in UTF-8 mode by default (a newer version), so there is no error | Under the hook on Windows: stage a file named with a CJK character that triggers an error (P9) |

## HIDDEN BEHAVIORS DETECTED
None beyond HB4 (an empty staged index gives a summary with no checks named), which is listed in Domain 1.

## ADVERSARIAL SCAFFOLD FINDINGS
- **Reviewer blind spots:** silence on success hides the one state the user must see (a skip).
- **Highest-risk claims:** U3 (F6), U5 (U-F1).
- **Multi-step traces:** see F6.
- **Subtlety flags:** pre-commit:17, a well-meant `[ $rc -eq 0 ] ||` that hides "skip".

---

# CROSS-DOMAIN SUMMARY

- **Domains:** Code, Tests, Documentation, Data, UX.
- **Claims:** 61 decomposed (Code 27, Tests 11, Documentation 11, Data 7, UX 5). 36 verified (PASS rows: Code 15, Tests 5, Documentation 9, Data 4, UX 3). 29 in FAIL (Code 15, Tests 9, Documentation 1, Data 3, UX 1). Each is counted once in its primary domain: D-F2 only points to F7 and is not counted, and U3 is counted as F6. 4 falsified hypotheses (FH1-FH4; 1 conditionally: FH4). Some claims gave both a PASS and a FAIL row (for example C19 with F15 and F16, C25 with F17), so these are row counts, not unique claims.
- **Survived:** 17/17 stress tests passed (S1-S17). All four techniques were used, at least 3 per domain, never the same one twice on a claim.
- **Failure categories:** 9 systemic patterns: silent fallthrough, missing completeness, assumed environment, implicit ordering / stale state, test-environment artifact, tautological test, missing negative tests, test-code drift, stale or partial description.
- **Invariants:** 9 found (check.py:2-50, README.md:244-254, CHANGELOG.md:3, check.py:423, test_check.py:4-5; no CLAUDE.md, AGENTS.md, CONTRIBUTING.md, SPEC or ADR exists in `./tree`). All 9 are touched. 2 are enforced by a mechanism that fully bites on the path in scope (I1, I9). 5 bite only partly (I2, I3, I5, I7, I8). 2 have nothing that bites (I4, I6).
- **Hypotheses:** 7 requiring further investigation (H1, H3, H4, H5, H6, H7, H8).
- **Hidden behaviors:** 7 detected (HB1-HB7). 4 are problems, each also a FAIL row: HB1 → D-F1, HB3 → F17, HB6 → T-F9, HB7 → DA-F3.
- **Findings by type:** **12 demonstrated defects** (F1, F2, F3, F4, F6, F7, F8, F9, T-F1, T-F2, T-F7, D-F1), **17 preventive measures** (F5, F10, F11, F12, F15, F16, F17, T-F3, T-F4, T-F5, T-F6, T-F8, T-F9, DA-F1, DA-F2, DA-F3, U-F1), and **4 falsified hypotheses (1 of them conditionally)**.
- **Critical issues:** 0 demonstrated defects of critical severity. Preventive measures of critical severity: 0. The highest severity is **high**: F2 and F4 (demonstrated defects) and F5 (preventive measure).
- **Pre-code:** not applicable (no artifact proposes work not yet done).
- **Executed:** 0 tests run (reasoning only). No mutation probe.
- **Proposed:** 10 checks (P1-P10) and 10 writes awaiting an answer.
- **Recommendation:** **Do not rely on the hook as the privacy gate until F4 (one flag), F2 (one character) and F3 (one keyword argument) are fixed.** They are three one-line changes, and the tests for F2 and F3 already exist and would turn green. Then fix F6 so that missing toolchains fail, add F5's error, and run `test_check.py` somewhere that gates commits (T-F5). The rest are low-severity robustness and test-hygiene items. The design is careful (staged-content checking, decoded JSON, masking, hash-bound facts) and most claims hold under trace. The defects cluster in the gaps between what the docs promise and the last few characters of the code.

## PROPOSED EXECUTABLE CHECKS
All ten rows below have the status **proposed**: none has been run. The Status column is folded into this line to keep the table readable.

| # | Claim | Confidence now | Check (command, test or query) | Confirms if | Refutes if | Cost and side effects |
|---|-------|----------------|--------------------------------|-------------|------------|-----------------------|
| P1 | F1, F2, F3 make `test_second_badge_mismatch`, `test_two_words_joined_any_way` (the `A  B` variant) and `test_whole_word_term_glued_in_output_is_still_masked` red. H1, H7 (hashes valid), T-F2 | 92 (code trace), ≤79 for the test outcomes (run-only) | `python3 -I -m unittest -v scripts/test_check.py`, run from a **separate copy** of `./tree` | exactly those 3 tests fail, everything else passes | they pass (my trace is wrong) or others fail | Runs check.py and check_facts.py many times. It writes only under the system temp dir (each test's own copy) and **executes every fact file** (Python, plus rustc and node if present). It reads nothing outside the copy. A few minutes of CPU. A memory-backed temp dir (tmpfs) is optional: it needs your separate consent and a few MB of free memory. |
| P2 | F6: a missing toolchain exits 0 | 90 | In a copy: `env PATH=<dir with python3 only> python3 scripts/check_facts.py 52 53; echo $?` | prints `skip 52.rs`, `skip 53.ts`, `2 fact file(s), 0 failed`, exit 0 | a FAIL or non-zero exit | Runs nothing but the runner. Reads only. |
| P3 | F7: a relative `--root` breaks every file | 85 | From the copy's root: `python3 scripts/check_facts.py --root . 38` | `FAIL 38.py: … can't open file …`, exit 1 | `ok   38.py` | Executes facts/38.py. Reads only. |
| P4 | F4: the hook passes with no terms configured | 92 | In a throwaway clone with the hook installed and no `.check-private-terms`/`CHECK_PRIVATE_TERMS`: stage a harmless change and `git commit` | the commit succeeds with `WARNING private terms: … NOT checked` | the commit is refused | Writes a commit in a **throwaway clone** only, never your working copy. |
| P5 | F5: a force-added terms file is not reported | 88 | In a throwaway clone: create `.check-private-terms` with a dummy term, `git add -f` it, `python3 scripts/check.py --strict --staged` | 0 errors about the file | an error naming the tracked terms file | Writes to a throwaway clone's index only. |
| P6 | F2 (CRLF form) | 92 | In a copy: write a file with `foo\r\nbar` (binary mode) and run `CHECK_PRIVATE_TERMS="foo bar" python3 scripts/check.py` | no `private term #1` error | the error is reported | Writes one file in the copy. Choose `foo bar` so that no real term is used. |
| P7 | DA-F1 (inline comment) | 85 | In a copy: terms file `zqvorblax  # note`, a file containing `zqvorblax`, then `python3 scripts/check.py` | no error for that file | the error is reported | Writes 2 files in the copy. |
| P8 | H5 (the hook is executable) | — | `git ls-files -s scripts/pre-commit` in the real repo | mode `100755` | `100644` | Read-only. It needs the real repo, which I was told not to read outside `./tree` (`./tree` has no `.git`). |
| P9 | U-F1, H8 | 60 | On Windows, in a throwaway clone with the hook: stage a fact file named `漢.py` (an orphan → an error that prints its name) and commit | `UnicodeEncodeError` traceback | a clean `ERROR … 漢.py …` line | Writes a commit in a throwaway clone. |
| P10 | H4 / F16 (GFM pipes in code spans) | 50 | Render a 3-column table with `` `a|b` `` in one cell on GitHub | GitHub shows 4 cells in that row | 3 cells | **Outward-facing:** it publishes content to GitHub (a gist or a draft). Use a throwaway account or repo, or skip it and read the GFM spec instead. |

Proposed writes (none made):
1. `scripts/pre-commit:9`: add `--strict` (F4).
2. `scripts/check.py:90`: `SEP = r"[\W_]*"` (F2).
3. `scripts/check.py:400`: `term_patterns(terms, substring=True)` (F3).
4. `scripts/check.py:223`: `for b in badges:` (F1).
5. `scripts/check.py:301-302`: an error instead of a silent skip when `.check-private-terms` is in the checked files (F5). Add a test.
6. `scripts/check_facts.py:91-93`: a missing toolchain counts as a failure (F6); `scripts/check_facts.py:81`: `root = os.path.abspath(args.root)` (F7); `timeout=` at line 100 (F11).
7. `scripts/check.py:255`: strip or warn on inline `#` comments in the terms file (DA-F1).
8. `scripts/test_check.py:479`: `self.assert_fails(r, "orphan.md", "never named in SKILL.md")` (T-F1); `assert_no_leak` in `assert_passes` (T-F8); fix the comment at 337 (T-F7); the git skip decorator and an isolated git config (T-F4); a portable unreadable file (T-F3); the missing negative tests of T-F6.
9. `scripts/check.py:46-47`: correct the fallback description (D-F1).
10. Out of scope, proposed only: `README.md:260` stays as is once F4 is fixed. Otherwise it needs correcting. Add a CHANGELOG "Unreleased" entry for whichever fixes are made (Step 5: `CHANGELOG.md` exists; no `TODO.md`, `SPEC.md`, `PLAN.md`, `ADR/` or agent instruction files exist in `./tree`).

**Which of P1-P10 may I run (P4, P5, P9 only in a throwaway clone; P10 only if you accept publishing to GitHub), and which of writes 1-10 should I make?**
