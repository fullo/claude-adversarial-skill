# Adversarial verification — repository checks, evals and docs of `adversarial-verify`

**Cost estimate (large request, cost accepted, every choice settled, so the verification started at once):** 21 files in scope (4 scripts, 3 docs/manifests, `evals.json`, 13 fact files, `NOT_COMPUTABLE`, `_parse_day.py`), 4 domains (Code, Tests, Data, Documentation), about 75 claims, nothing run.

## INTAKE

- **Target:** every domain detected in the listed files (from the request): **Code** (`scripts/check.py`, `scripts/check_facts.py`, `scripts/pre-commit`, the fact files as code), **Tests** (`scripts/test_check.py`, the fact files as oracles, `evals.json` as the skill's test suite), **Data** (`evals.json` format, `.claude-plugin/plugin.json`, `facts/NOT_COMPUTABLE` format), **Documentation** (`README.md`, `CHANGELOG.md`, script docstrings, error messages). **UX:** I looked at the only interface, the terminal output of `check.py`/`check_facts.py`/`pre-commit`. It is just message text, with no layout, screens or menus. Per Step 0, what message text says belongs to Documentation, so UX has no section of its own.
- **Depth:** standard (from the request).
- **Scope:** the whole of the 21 listed files (from the request; no diff, no version history). "Changed path" in the INVARIANTS table therefore means "the code path in these files that the invariant is about".
- **Execution mode:** reasoning only (from the request). Nothing was run. Every check that a run would decide is in PROPOSED EXECUTABLE CHECKS. Consent lasts for this verification only.
- Reading was limited to `./tree` and `./skill`. External links (mutation-tool docs, the Rainbow Climb repo, the marketplace) were not opened.
- No reference file of the skill was needed. Nothing proposes work not yet done, so there is no Step 1c. No UX target, no approved run.

---

# DOMAIN 1 — CODE (`scripts/check.py`, `scripts/check_facts.py`, `scripts/pre-commit`, fact files)

## VERIFICATION DOMAIN
Code

## GROUND TRUTH
- The scripts' own contracts: `scripts/check.py:2-51` (seven numbered invariants), `scripts/check_facts.py:2-19`, `scripts/pre-commit:2-5`.
- The documented behavior: `README.md:245-264`, `CHANGELOG.md:3`, `CHANGELOG.md:14`, `CHANGELOG.md:24`.
- The tests that state the intended behavior: `scripts/test_check.py` (e.g. `:171-173`, `:284-289`, `:341-344`).
- The repository content the checks run on: `skills/adversarial-verify/SKILL.md` (frontmatter `:20`), `evals.json`, `facts/`, `references/` (3 files: `execution.md`, `pre-code.md`, `ux.md`).
- Python semantics (`re`, `argparse`, `unicodedata`) and POSIX `sh`.

## INVARIANTS
I looked for agent or contributor files (`CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, `.claude/`) and found none in `./tree` (full file list: 28 files). I also looked for invariant sections. The project's invariants are stated in `scripts/check.py:2-44` ("the repository's own invariants"), `CHANGELOG.md:3`, `README.md:245-255` and `scripts/test_check.py:4-5`. I found **7** invariants. All 7 are touched by the files in scope, since those files implement or state them. The table below lists them once; the other domains refer back to it.

| # | Invariant | Source | Touched by | Enforced by (file:line / test name) | Bites on the path? |
|---|-----------|--------|------------|-------------------------------------|------------------------|
| I1 | The version is the same in SKILL.md's frontmatter, **every** README skill badge, plugin.json and the newest CHANGELOG entry | `scripts/check.py:10-12`, `CHANGELOG.md:3`, `README.md:250` | `scripts/check.py:212-241`, `README.md:1`, `README.md:125`, `.claude-plugin/plugin.json:3`, `CHANGELOG.md:10` | `check_version` (`scripts/check.py:212`); tests `VersionTest.*` | **Partly.** Only the first badge is compared (`scripts/check.py:223`, FAIL C2). The prose version at `README.md:125` is not covered at all (FAIL D2). |
| I2 | No private term appears in any file content or name, and terms are never printed | `scripts/check.py:13-26`, `README.md:251`, `scripts/test_check.py:4-5` | `scripts/check.py:246-323`, `:397-414`, `scripts/pre-commit:9` | `check_private`, `mask`; tests `PrivateTest.*` | **Partly.** Separators are limited to one character (FAIL C3). The mask is whole-word for `=` terms, so they leak (FAIL C1). The hook runs without `--strict`, so with no terms configured nothing is checked (FAIL C4). |
| I3 | evals.json: 4 keys, ids 1..n, non-empty fields, tags from 21 on | `scripts/check.py:6-9` | `scripts/check.py:163-207`, `evals.json` | `check_evals`; `EvalsTest.*` | Yes (PASS C-P1) |
| I4 | Every eval ≥29 that states facts has a fact file **or** a reason, not both; fact files carry the prompt hash; facts are true | `scripts/check.py:34-38`, `README.md:255`, `scripts/check_facts.py:2-14` | `scripts/check.py:457-501`, `scripts/check_facts.py`, `facts/*`, `facts/NOT_COMPUTABLE` | `check_facts` (`scripts/check.py:495-496`), `check_facts.py` | **The mechanism bites, and the repo violates it:** eval 52 has both (FAIL C5). Fact truth is not enforced when a toolchain is missing (FAIL C6). |
| I5 | Every named reference file exists; every reference file is named in SKILL.md; the folder is read "as on disk, tracked or not" | `scripts/check.py:39-44` | `scripts/check.py:506-520` | `check_references`; `ReferencesTest.*` | Yes for names and existence. Under `--staged` the folder is read from the index, not the disk (FAIL C9, docstring drift). |
| I6 | Markdown tables have as many cells as the header | `scripts/check.py:30-33` | `scripts/check.py:341-381` | `check_tables`; `TablesTest.*` | Yes (PASS C-P5); one preventive gap (FAIL C12) |
| I7 | Technology-bound terms in the skill texts are warnings | `scripts/check.py:27-29` | `scripts/check.py:80-88`, `:328-336` | `check_neutral`; `NeutralTest.*` | Yes (warnings only, by design) |

## DECOMPOSED CLAIMS
1. `check_evals` rejects every format violation it lists (keys, bool ids, gaps, duplicates, order, empty fields, tags from 21 on) — Deductive
2. `check_version` compares SKILL.md with every README badge — Deductive
3. `check_version` compares plugin.json and the newest numeric CHANGELOG entry — Deductive
4. Private-term parts may be joined by any run of non-alphanumerics, or by nothing — Deductive
5. Terms are never printed: `mask` hides every output line that contains a term, also glued forms of `=` terms — Deductive
6. JSON escapes, Latin-1 and UTF-16-with-BOM files are scanned — Deductive
7. The terms file is never scanned and is gitignored — Deductive
8. `check_tables` counts cells correctly, ignoring escaped pipes, code spans and fenced blocks — Deductive
9. `check_facts` (check.py) flags orphans, hash drift, a missing hash, file+reason, and facts without either — Deductive
10. The repository as it stands passes `check.py` — Deductive
11. `check_references` flags missing and unnamed reference files, reading the folder as on disk — Deductive
12. `--staged` checks exactly the staged content and cleans up its temp dir — Deductive
13. `check_facts.py` treats a missing toolchain as an error, never a silent skip — Deductive
14. `check_facts.py` requires an assertion outside comments/strings and a final `ok <id>` line — Deductive
15. `pre-commit` runs check.py in `--strict --staged` mode (as README says) — Deductive
16. `pre-commit` runs the fact files on exactly the staged files when evals change — Deductive
17. Each fact file computes what its eval's prompt states (35, 37, 38, 39, 40, 42, 48, 49, 51, 52, 53, 56, 57) — Deductive (hand computation)
18. Missing input files give an error line, not a traceback — Deductive
19. Each eval maps to at most one fact file — Deductive

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Silent fallthrough | toolchain missing → `skip` with exit 0 (`scripts/check_facts.py:91-93`); staged run with an empty index → no checks, exit 0 (`scripts/check.py:436`); missing plugin/CHANGELOG/SKILL → traceback instead of an ERROR (`scripts/check.py:214`, `:227`, `:237`); hook without `--strict` → private names unchecked with only a warning (`scripts/pre-commit:9`) | `scripts/check_facts.py`, `scripts/check.py`, `scripts/pre-commit` |
| Missing completeness | only the first badge is checked (`scripts/check.py:223`); prose version not covered (`README.md:125`); `mask` not given `substring=True` (`scripts/check.py:400`); facts detection keyed on the literal `(Facts` (`scripts/check.py:500`); two fact files for one eval overwrite each other (`scripts/check.py:473`) | `scripts/check.py`, `README.md` |
| Stale state (docs or data that outlived the code) | `facts/NOT_COMPUTABLE:13` vs `facts/52.rs`; `README.md:125` "4.1"; the docstring of item 7 vs `--staged` | `NOT_COMPUTABLE`, `README.md`, `scripts/check.py` |
| Assumed environment | `[\W_]?` assumes one-character separators (CRLF line breaks are two); `python3` found but possibly a Windows Store stub (`scripts/pre-commit:7-8`); `os.symlink` needs privileges on Windows (`scripts/test_check.py:351`) | `scripts/check.py`, `scripts/pre-commit`, `scripts/test_check.py` |

## OUT OF SCOPE
- `skills/adversarial-verify/SKILL.md:439` and `references/*.md` were read as ground truth only. I found no other file under `./tree` with a stale version number (grep for `4\.1\b`: only `CHANGELOG.md:17`, which is correct, `README.md:125`, which is in scope, and `scripts/test_check.py:204`, which is a test value).

## VERIFICATION RESULTS
### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| C-P1 | 1 — evals format | `scripts/check.py:175-207`: keys via set difference `:180`; `type(i) is not int` rejects bools `:186`; `i >= TAGGED_FROM` with `TAG_RE` requiring `\s+\S` `:75`, `:201`; duplicates `:203`; order and gaps `:206`. `evals.json`: 57 ids, 1..57 in order (`evals.json:5`…`:711`); 228 key lines = 57 × 4. |
| C-P2 | 3 — plugin.json and CHANGELOG | `scripts/check.py:226-241`: a non-string version is an error `:233`. The CHANGELOG regex `^## +([0-9][0-9.]*)\b` with `re.M` skips `## Unreleased` (`CHANGELOG.md:5`) and finds `## 4.2` (`CHANGELOG.md:10`) = `SKILL.md:20` "4.2" = `.claude-plugin/plugin.json:3`. |
| C-P3 | 6 — JSON escapes, encodings | `scripts/check.py:112-122` (UTF-16 only with a BOM, then utf-8-sig, then Latin-1); `:313-323` scans decoded JSON keys and values via `json_strings` `:279-289`. |
| C-P4 | 7 — terms file | `scripts/check.py:301` skips it by basename; `.gitignore:1`; BOM-prefixed comment handled by `utf-8-sig` in `decode` `:120` and `load_terms` `:255`. |
| C-P5 | 8 — table cells | `scripts/check.py:344-350` replaces code spans and `\|` before counting; outer pipes stripped; fences toggled `:361-368`; the delimiter row is checked `:372`. |
| C-P6 | 9 — fact-file checks (logic) | `scripts/check.py:467-501`: orphan `:470-471`; hash in the first 2000 chars `:476-482`; reason format `:490-492`; both `:495-496`; facts without either `:497-501`. |
| C-P7 | 11 — references | `scripts/check.py:506-520`; the 3 files in `references/` are each named in SKILL.md (`SKILL.md:49-51`). |
| C-P8 | 12 — staged content and cleanup | `scripts/check.py:386-394` uses `checkout-index -a` into a temp dir; `finally: shutil.rmtree` `:438-440`; outside git → an ERROR, no traceback `:430-432`. |
| C-P9 | 14 — assertion and `ok` line | `scripts/check_facts.py:42-51`: AST `Assert`/`Raise` for .py; strip-then-regex for .rs/.ts; last-line check `:106-108`; no file selected → exit 1 `:113`. |
| C-P10 | 16 — facts on staged files | `scripts/pre-commit:12-17` checks out the index into `$tmp` and runs `check_facts.py --root "$tmp"`; the exit code is taken from the command substitution `:15`. |
| C-P11 | 17 — fact arithmetic for 39, 40, 42, 49, 51, 56, 57 | Hand-traced: 39 (`_parse_day.py:15-35`: the parent rejects 2024-02-29 with 28 days; the fix accepts it; 2100 is not a leap year); 40 (killed {<, <=, True}, survivors die at 18/17); 42 (`100*0.9` rounds to the double `90.0`, so all four variants pass); 49 (93.75−16 = 77.75; 80−16 = 64; 107.5−16 = 91.5); 51 (20+24 = 44, 16+8 = 24); 56 (104+5+8+3 = 120; 104+4 = 108; 8+3+1 = 12; 104/108 = 96.3 %); 57 (239+9+12 = 260; 9−7 = 2). All match their asserts. |

### FALSIFIED HYPOTHESES
| # | Location | Suspected defect | Check (quote) | Status | Could it have failed? | Paths not covered | Mode | Confidence |
|---|----------|------------------|-------|--------|-----------------------|-------------------|------|------------|
| C-FH1 | `skills/adversarial-verify/evals/facts/48.py:17-21` | A WCAG ratio is misstated | Hand computation of the relative luminance of all 8 pairs: 12.63, 5.33, 5.17, 10.81, 3.13, 3.23, 1.47, 4.83 | conditionally | Yes in principle (any mismatched digit would show), but it is a hand computation, not the run | Completes with `python3 -I scripts/check_facts.py 48`; the rounding at the 2nd decimal of 1.47 (1.4657) and 4.83 (4.8291) is the closest margin | Deductive | 75 |
| C-FH2 | `skills/adversarial-verify/evals/facts/53.ts:6-7`, `:22` | The dates are not Saturday/Wednesday/Sunday | Day count from Thursday 1 Jan 2026: 24 Oct = day 297 → Saturday; 21 Oct → Wednesday; 25 Oct → Sunday. Survivors {"0 -> 1", "day === 0 -> false"} | conditionally | Same as above | Completes with `check_facts.py 53` (needs node ≥ 22.6) | Deductive | 75 |
| C-FH3 | `skills/adversarial-verify/evals/facts/38.py:19-21` | The float claims are wrong (`0.009000000000000001`, `round(10.05*0.9,2) == 9.05`) | The exact product 9.0450000000000008617… rounds to the double 9.045000000000002 (nearer than 9.04499999999999993), so it rounds to 9.05 | conditionally | It depends on IEEE rounding I traced by hand | Completes with `check_facts.py 38` | Deductive | 70 |
| C-FH4 | `scripts/check.py:201` | Off-by-one at the tag boundary (eval 21) | `elif i >= TAGGED_FROM and not TAG_RE.match(a)` with `TAGGED_FROM = 21` `:74`; `evals.json:282` (id 21) is tagged, `evals.json:270` (id 20) is untagged | falsified | Yes: `>` instead of `>=` would let id 21 pass, which `test_untagged_assertion_at_the_boundary` (`scripts/test_check.py:149-153`) asserts against | Ids beyond 57 | Deductive | 85 |

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| C1 | `scripts/check.py:400` | `pats = term_patterns(terms)` under the comment `# substring patterns: when hiding output, err on the side of hiding too much` (`:399`) | Demonstrated defect | high | Term `=acme`. An eval gets the key `acmelabs`. `check_private` does not flag it (whole word only, `:265`, `:275`), but `check_evals` prints `unexpected keys ['acmelabs']` (`:182`). `mask` builds whole-word patterns because `substring` defaults to False (`:259`, `:265`), so `hit(msg)` is False and the private term is printed. This breaks I2 (`:22-23` "Terms are never printed"; `README.md:251`) and is exactly what `test_whole_word_term_glued_in_output_is_still_masked` (`scripts/test_check.py:341-344`) asserts against | Deductive | 90 | `pats = term_patterns(terms, substring=True)` |
| C2 | `scripts/check.py:223` | `for b in badges[:1]:` | Demonstrated defect | medium | README gets a second badge `badge/skill-v2.0-`: `findall` returns `['4.2','2.0']`, only `'4.2'` is compared, no error. This contradicts `:10` "matches every skill badge", `README.md:250` and `test_second_badge_mismatch` (`scripts/test_check.py:171-173`) | Deductive | 92 | `for b in badges:` |
| C3 | `scripts/check.py:90` | `SEP = r"[\W_]?"  # anything that is not a letter or digit, possibly nothing` | Demonstrated defect | medium | The term `jane doe` written `JANE  doe` (two spaces), `jane - doe`, `jane, doe`, or split across a CRLF line break (`\r\n`, two characters): `?` allows at most one separator character, so it does not match and the private name is committed. This contradicts `:15-17` "joined by anything", `README.md:251` ("line break"), and the variant `f"{a.upper()}  {b}"` in `scripts/test_check.py:286` | Deductive | 88 | `SEP = r"[\W_]*"` (optionally bounded, e.g. `{0,3}`) |
| C4 | `scripts/pre-commit:9` | `"$py" -I "$root/scripts/check.py" --staged --root "$root" \|\| exit 1` | Demonstrated defect | high | On a fresh clone with no `.check-private-terms` and no env var, every commit passes with only `WARNING private terms: … private names were NOT checked` (`scripts/check.py:295-297`), although `README.md:261` says the hook "runs --strict --staged before every commit" and the hook's own comment `:5` describes `--strict`. I2 is not enforced at the one point that guards commits | Deductive | 92 | `--strict --staged` |
| C5 | `skills/adversarial-verify/evals/facts/NOT_COMPUTABLE:13` with `facts/52.rs:1` | `52: the compiler is not installed on every machine` | Demonstrated defect | high | `check_facts` puts 52 into `with_file` (`52.rs`, `.rs` ∈ `FACT_EXTS`, id 52 exists at `evals.json:647`) and into `reasons`, so `:495-496` emits `ERROR … eval 52 has a fact file and a reason not to have one`. `check.py` therefore exits 1 on the repository as it stands, every commit through the hook is blocked, and every `assert_passes` test in `scripts/test_check.py` (e.g. `test_repo_passes` `:97-98`) fails on that line | Deductive | 90 | Delete `NOT_COMPUTABLE:13` (the reason also contradicts `README.md:247`, which requires `rustc`) |
| C6 | `scripts/check_facts.py:91-93` | `print(f"skip {name}: toolchain not found")` / `continue` | Demonstrated defect | medium | On a machine without `node`, `53.ts` is skipped, `failed` stays 0, the run prints `13 fact file(s), 0 failed` and exits 0 (`:112-113`). The pre-commit hook then passes a commit whose TS fact was never run. This contradicts `:8` "A missing toolchain is an error, never a silent skip" and `README.md:255` | Deductive | 92 | `print(f"FAIL {name}: toolchain not found"); failed += 1; continue` |
| C7 | `scripts/check.py:214`, `:227`, `:237` | `plugin = json.loads(read_text(root, PLUGIN, rep))` / `except ValueError` | Preventive measure | low | If plugin.json, CHANGELOG.md or SKILL.md is missing or deleted in a staged commit, `open` raises `FileNotFoundError` (an `OSError`, not caught), so the script dies with a traceback and no summary. `check_evals` catches `OSError` (`:167`), so the handling is inconsistent. Likelihood: low (only when a file is removed) | Deductive | 85 | Catch `OSError` in `check_version` and report an ERROR |
| C8 | `scripts/check.py:436` | `if files or not args.staged:` | Preventive measure | low | `--staged` in a git repo whose index is empty (e.g. right after `git init`, or `git rm -r --cached .`): `staged_tree` returns `[]`, no check runs, no error, and the summary shows `checked (staged content):  — 0 error(s)` with exit 0. Likelihood: low | Deductive | 82 | Report an ERROR (or a line saying nothing was staged) when `files == []` |
| C9 | `scripts/check.py:42-44` | `The folder is read as it is on disk, tracked or not, since copying the skill's folder ships every file in it.` | Demonstrated defect (docstring drift) | low | With `--staged`, the path the hook uses, `root` is the temp checkout of the index (`:433`), so an untracked `references/x.md` is not seen. `test_staged_content_is_what_is_checked` (`scripts/test_check.py:502-510`) asserts exactly that behavior. The docstring promises the opposite | Deductive | 85 | Reword item 7: "in the working tree, the folder as it is on disk; with --staged, as staged" |
| C10 | `scripts/check.py:473` | `with_file[int(stem)] = name` | Preventive measure | low | If both `35.py` and `35.ts` exist, the later name overwrites the earlier one, so only one file's `prompt-sha256` is checked, while `check_facts.py` runs both. An edited prompt can then go unnoticed for one of them. Likelihood: low (no such pair today) | Deductive | 80 | Error on a second fact file for the same id |
| C11 | `scripts/check.py:500` | `if "(Facts" in str(e.get("prompt", ""))` | Preventive measure | low | The rule keys on a literal marker. Evals 54, 55 (`evals.json:672`, `:686`: 400 MB vs 24 GB, 6 GB vs 5 GB) and 42 state checkable facts without `(Facts`, so a future eval written that way escapes I4. Likelihood: medium as evals are added (see stress S2) | Deductive | 80 | Document the marker as mandatory in `README.md:255`, or match `Facts` case-insensitively and also list evals ≥29 with numbers in NOT_COMPUTABLE |
| C12 | `scripts/check.py:363-366` | `if fence is None: fence = f.group(1)[0] else: fence = None` | Preventive measure | low | A ```` ``` ```` block that contains a `~~~` line (or a shorter fence) is closed early. The table lines after it are then checked, which gives false errors; a broken table before a real closing fence can also be skipped. CommonMark closes only on the same character with at least the same length. Likelihood: low | Deductive | 80 | Close only when the character matches and the length is ≥ the opening length |
| C13 | `scripts/pre-commit:12` | `grep -q '^skills/adversarial-verify/evals/'` | Preventive measure | low | A commit that changes only `scripts/check_facts.py` (e.g. weakens `has_assertion`) does not re-run the fact files. Likelihood: low | Deductive | 80 | Also match `^scripts/check_facts.py` |

## STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|
| S1 | Scale Shift | C-P1 `check_evals` at 0 and at 10× evals | yes | 85 | 0 evals → `"no 'evals' list"` (`scripts/check.py:171-173`); 570 evals → `ids.count` is O(n²), about 3×10⁵ ops, which is negligible |
| S2 | Time Travel | C-P6 fact-file rule in 6 months | **no** | 80 | New evals that state facts without the literal `(Facts` (already 42, 54, 55) escape the rule; the magic numbers `TAGGED_FROM=21`/`FACTS_FROM=29` (`scripts/check.py:74`, `:77`) have comments, so they survive. Reported as C11 |
| S3 | Existence Question | `facts/_parse_day.py` | yes | 85 | Deleting it would duplicate `parse_day_v1` in 35.py and 37.py and two versions in 39.py; it is excluded from both checkers by the leading `_` (`scripts/check.py:469`, `scripts/check_facts.py:83`), consistently |
| S4 | Requirement Inversion | C-P3 encoding fallback (a user wants strict UTF-8) | yes | 80 | Strictness is already enforced where it matters: non-UTF-8 SKILL/README/evals/references are ERRORs (`scripts/check.py:128-129`); the permissive decode only widens the private-term scan |

## HYPOTHESES
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| C-H1 | Every fact file carries a `prompt-sha256` (`facts/35.py:1` … `facts/57.py:1`) | All 13 hashes match the current prompts | One or more prompts were edited after their facts (e.g. 56 or 57, added in "Unreleased") | Proposed check P3 |
| C-H2 | C1, C2, C3 and C5 each contradict a test in `scripts/test_check.py` | The suite is currently red (≥4 tests failing, plus every `assert_passes` test because of C5) | The tests were run on another tree; or the repo is mid-edit | Proposed check P1 |

## HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| HB1 | `scripts/check_facts.py:91-93` | Missing toolchain = error (`:8`) | Skip, exit 0 | Demonstrated defect → C6 | 92 |
| HB2 | `scripts/check.py:397-400` | Masking errs on hiding too much | Whole-word for `=` terms | Demonstrated defect → C1 | 90 |
| HB3 | `scripts/check.py:223` | Every badge | First badge only | Demonstrated defect → C2 | 92 |
| HB4 | `scripts/check.py:433` with `:42-44` | References read as on disk | Read from the index under `--staged` | Demonstrated defect (doc) → C9 | 85 |
| HB5 | `scripts/check.py:436` | — | Empty staged index runs nothing and passes | Preventive measure → C8 | 82 |

## ADVERSARIAL SCAFFOLD FINDINGS
- **Reviewer blind spots:** the `?` in `[\W_]?` (one character, reads like "optional separator"); the missing keyword argument in `term_patterns(terms)`, sitting right under a comment that says the opposite; `[:1]` on a list the docstring calls "every".
- **Highest-risk claims:** (1) claim 5, terms never printed (C1, a privacy leak); (2) claim 15, the hook enforces `--strict` (C4: private names silently unchecked at commit time); (3) claim 10, the repo passes (C5: every commit blocked, every passing-test assertion red).
- **Multi-step traces:** term `=x` → `check_private` whole-word misses `xlabs` → `check_evals` prints the key → `mask` whole-word misses it → printed to the console and CI log (C1). No node → `command()` returns None → `skip` → `failed=0` → exit 0 → `pre-commit:17` passes → a false TS fact is committed (C6). `NOT_COMPUTABLE:13` + `52.rs` → `:495` ERROR → `pre-commit:9` exits 1 → every commit blocked (C5).
- **Subtlety flags:** `scripts/check.py:90` (one-character quantifier), `:223` (slice), `:400` (default argument), `:473` (silent dict overwrite), `scripts/check_facts.py:92` (`continue` without `failed += 1`).

### SUMMARY (Code)
- Domain: Code
- Claims: 11 verified, 13 in FAIL (7 defects: C1–C6, C9; 6 preventive measures: C7, C8, C10–C13), 4 falsified
- Survived: 3/4 stress tests passed
- Failure categories: 4 systemic patterns
- Invariants: 7 found, 7 touched, 4 enforced by a mechanism that bites (I3, I5, I6, I7); I1, I2 partly; I4 bites but the repo violates it
- Hypotheses: 2
- Hidden behaviors: 5 detected
- Findings by type: 7 demonstrated defects, 6 preventive measures, 4 falsified hypotheses (3 of them conditionally)
- Critical issues: 0 demonstrated defects of critical severity (preventive of critical severity: 0); high: C1, C4, C5
- Pre-code: n/a
- Executed: nothing run (reasoning only)
- Recommendation: do not trust `check.py` green or the hook as privacy guards until C1, C3 and C4 are fixed; fix C5 first, because it blocks every commit.

---

# DOMAIN 2 — TESTS (`scripts/test_check.py`, fact files as oracles, `evals.json` as the skill's suite)

## VERIFICATION DOMAIN
Tests

## GROUND TRUTH
The production code `scripts/check.py`, `scripts/check_facts.py`; the skill text `skills/adversarial-verify/SKILL.md` (the evals' expected behavior, e.g. `:439`); the fact files; the eval prompts. Test bootstrap: `Base.setUp` (`scripts/test_check.py:30-37`), which copies the repo into a temp dir and runs `check.py` with `-I` (`:50`).

## INVARIANTS
See the INVARIANTS table in Domain 1 (I1–I7). For the tests: I2 is tested by `PrivateTest`, which correctly bites on C1 and C3 (they would be red); I4 truth-of-facts is tested by `test_runner_passes_on_the_repo`, which does **not** bite when a toolchain is missing (T2).

## DECOMPOSED CLAIMS
1. `test_check.py` builds a negative case for every invariant and asserts the script's own ERROR text — Deductive
2. `test_file_nobody_names` fails when an orphan reference file is not reported — Deductive
3. `test_runner_passes_on_the_repo` shows that the Rust and TS facts hold — Deductive
4. The test bootstrap reproduces production (the hook / CLI) — Deductive
5. Tests never print a private term — Deductive
6. Test edits target strings that exist in the repo (`edit` asserts `old in s`) — Deductive
7. The eval expected outputs and assertions agree with their prompts and fact files (49, 56) — Deductive
8. The eval assertions match the current skill text (18) — Deductive
9. The tests are portable (Windows, no git) — Deductive

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Tautological test | `scripts/test_check.py:479` | `scripts/test_check.py` |
| Test-environment artifact | `scripts/test_check.py:575-578` passes when rustc/node are absent | `scripts/test_check.py` |
| Test-code drift (oracle drift) | `evals.json:249` vs `SKILL.md:439`; `evals.json:612` vs `:615`; `evals.json:705` vs `:699`/`facts/56.py:11-12` | `evals.json` |
| Assumed environment | `os.symlink` `scripts/test_check.py:351`; git without a skip guard `:502-505` | `scripts/test_check.py` |

## VERIFICATION RESULTS
### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| T-P1 | 1 — negative cases per invariant | Classes `EvalsTest`, `VersionTest`, `PrivateTest`, `StagedTest`, `NeutralTest`, `TablesTest`, `ReferencesTest`, `FactsTest` (`scripts/test_check.py:104-617`); `assert_fails` requires a non-zero exit, the summary line, `ERROR` and the named token (`:54-62`), so a crash does not count as a pass |
| T-P2 | 4 — the bootstrap matches production | `run_check` runs the real script with `-I` and `--root` (`:49-52`), the same entry point as `scripts/pre-commit:9`; `StagedTest` uses a real git repo (`:376-380`). Test-environment check: the only difference is the temp dir vs the user's repo; no fake or store is involved |
| T-P3 | 5 — no term printed | Terms are built at run time (`:24-26`); `assert_no_leak` runs in every `assert_fails` (`:62`), so C1's leak would make `:344` red |
| T-P4 | 6 — edit targets exist | `"| **Frequency assumptions** |"` = `SKILL.md:207`; `"day > 31"` is in the eval 37 prompt (`evals.json:463`, index 36 = id 37); `"assert round(10.05 * 0.9, 2) == 9.05"` = `facts/38.py:21`; `"assert clipped(375)"`, `"(320)"`, `"(430)"` = `facts/49.py:12-14`; `"print('ok 40')"` = `facts/40.py:13` |
| T-P5 | 7 (partly) — facts vs prompts | All prompts with fact files agree with their files (C-P11, C-FH1–3); eval 48 expected "about 3.1/3.2/1.5" (`evals.json:599`) = 3.13/3.23/1.47; eval 51 44/24 = `facts/51.py:5` |

### FALSIFIED HYPOTHESES
| # | Location | Suspected defect | Check (quote) | Status | Could it have failed? | Paths not covered | Mode | Confidence |
|---|----------|------------------|-------|--------|-----------------------|-------------------|------|------------|
| T-FH1 | `scripts/test_check.py:595-602` | The "assert in a comment" test is vacuous because `has_assertion` would count it anyway | `x = 'assert'` and `# … assert …` with no `ast.Assert`/`ast.Raise` → `has_assertion` False (`scripts/check_facts.py:50`) → `FAIL … no assertion` | falsified | Yes: a regex-based Python check would count the string, and the test would go red | `.rs`/`.ts` comment stripping is not tested (`STRIP`, `scripts/check_facts.py:35-39`) | Deductive | 85 |

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| T1 | `scripts/test_check.py:479` | `self.assertIn("orphan.md", r.stdout + self.ref("orphan.md"))` | Demonstrated defect (tautological) | low | `self.ref("orphan.md")` always contains `orphan.md`, so the assertion is true even if `check_references` (`scripts/check.py:519-520`) were deleted. `:481-485` covers the case only partly | Deductive | 95 | `self.assert_fails(r, "orphan.md", "never named in SKILL.md")` |
| T2 | `scripts/test_check.py:575-578` | `self.assertEqual(r.returncode, 0, …)`; `self.assertRegex(r.stdout, r"\d+ fact file\(s\), 0 failed")` | Demonstrated defect (test-environment artifact, missing negative test) | medium | On a CI image without `node`/`rustc`, 52.rs and 53.ts are skipped (C6) and the test is green, so a false Rust/TS fact passes. No test covers "toolchain missing → failure" | Deductive | 85 | Assert no `skip ` line in stdout; add a test that runs with `PATH` lacking node and expects a non-zero exit |
| T3 | `skills/adversarial-verify/evals/evals.json:705` | `"… (104 of 108, about 96%) and says that 11 are excluded: 8 timed out, 3 skipped, 1 not measured"` | Demonstrated defect | medium | 8+3+1 = 12; the expected output says "with 12 excluded" (`:699`); `facts/56.py:11-12` asserts `excluded == 12`. A grader following the assertion rewards a wrong count or penalizes the right one. The fact file checks the prompt, not the assertion | Deductive | 95 | "says that 12 are excluded" |
| T4 | `skills/adversarial-verify/evals/evals.json:612` | `"… and that at 320 px (80 px buttons, 64 px usable) more labels are clipped"` | Demonstrated defect | low | At 320 px the same two labels are clipped as at 375 px ('Startseite' 61 ≤ 64, 'Gemerkt' 50 ≤ 64), as the assertion (`:615`) and `facts/49.py:13` state. The expected output contradicts its own assertion | Deductive | 92 | "…the same two labels are clipped with less room to spare" |
| T5 | `skills/adversarial-verify/evals/evals.json:249` | `"… 'Invariants: N found, M touched, K enforced by a mechanism that bites on the changed path (code, data) or respected (plans, specs, docs, analyses)'"` | Demonstrated defect (oracle drift) | low | The current summary line is `(code, data, tests, UX)` / `(plans, specs, docs, analyses, mock-ups)` (`SKILL.md:439`). A strict grader marks a skill-conformant output as failing this assertion | Deductive | 90 | Quote the current line, or assert only the "N found, M touched, K enforced" part |
| T6 | `scripts/test_check.py:351`, `:502-505` | `os.symlink(...)`; `ReferencesTest.test_staged_content_is_what_is_checked` without `skipUnless(git)` | Preventive measure | low | On Windows without developer mode, `os.symlink` raises `OSError` (an error, not a failure, but red); without git, `:503` raises. `README.md:264` documents Windows use. Likelihood: medium on Windows | Deductive | 80 | `skipUnless` guards (symlink capability, `shutil.which("git")`) |

## STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|
| S5 | Requirement Inversion | T-P1, `assert_fails` (what if the script crashes instead of failing?) | yes | 85 | A crash has no `checked (` summary, so `:58` rejects it as a pass of the negative test |
| S6 | Time Travel | T-P4, string-based edits in 6 months | yes | 80 | `edit` asserts `old in s` (`:80`), so a reworded SKILL/fact file makes the test fail loudly, not pass silently |
| S7 | Scale Shift | T-P3, many subtests reuse `tearDown(); setUp()` (`:248`, `:288`) | yes | 75 | Each subtest gets a fresh copy, so there is no cross-subtest state; the cost grows linearly (one repo copy per variant) |

## HYPOTHESES
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| T-H1 | `evals.json:29` maps "adds items to a list while iterating" to "Frequency assumptions or Implicit ordering" | The category list is a stale or arbitrary oracle (the SKILL's Step 2 example, `SKILL.md:188`, treats it as nested modification, closer to stale state) | The authors accept either as abstraction targets on purpose | Ask the maintainer, or check the eval's grading history |

## HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| HB6 | `scripts/test_check.py:575` | "runner passes on the repo" proves the facts | Proves only the facts whose toolchain is installed | Demonstrated defect → T2 | 85 |

## ADVERSARIAL SCAFFOLD FINDINGS
- **Reviewer blind spots:** the concatenation inside `assertIn` (T1); the arithmetic inside an assertion string (T3) is not covered by the fact file, which checks the prompt only.
- **Highest-risk claims:** claim 3 (T2), claim 7 (T3), claim 2 (T1).
- **Multi-step traces:** `evals.json:705` "11" → grader → a correct skill output scored as failing → skill tuned toward the wrong count.
- **Subtlety flags:** `scripts/test_check.py:479`.

### SUMMARY (Tests)
- Domain: Tests
- Claims: 5 verified, 6 in FAIL (5 defects, 1 preventive), 1 falsified
- Survived: 3/3 stress tests passed
- Failure categories: 4
- Invariants: see Domain 1; I2 tests bite, the I4 truth test does not bite without toolchains
- Hypotheses: 1
- Hidden behaviors: 1
- Findings by type: 5 demonstrated defects, 1 preventive measure, 1 falsified hypothesis (0 conditionally)
- Critical issues: 0 (preventive critical: 0)
- Recommendation: the suite is good at catching C1–C3 (it would be red, see C-H2); fix T1–T3 before using the evals to grade skill versions.

---

# DOMAIN 3 — DATA (`evals.json` format, `.claude-plugin/plugin.json`, `facts/NOT_COMPUTABLE`)

## VERIFICATION DOMAIN
Data

## GROUND TRUTH
The format contracts in `scripts/check.py:6-9`, `:34-38`, `:490`, `facts/NOT_COMPUTABLE:1-3`; the plugin manifest keys used by `check_version` (`scripts/check.py:232`); `CHANGELOG.md:26` (the manifest declares version, repository, licence, keywords).

## INVARIANTS
I3 and I4 from Domain 1.

## DECOMPOSED CLAIMS
1. `evals.json` satisfies its schema (4 keys, ids 1..57 in order, tags from 21) — Deductive
2. `NOT_COMPUTABLE` lines follow `<id>: <reason>` and list only evals without a fact file — Deductive
3. Every eval ≥29 with `(Facts` has exactly one of a file or a reason — Deductive
4. `plugin.json` is valid and declares version 4.2, repository, licence, keywords — Deductive

## VERIFICATION RESULTS
### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| DA-P1 | 1 | 57 ids in order (`evals.json:5`…`:711`); 228 key lines at object depth = 57×4; ids ≥21 tagged (`evals.json:282`…`:721` all begin `[substance]`/`[format]`) |
| DA-P2 | 3 (except 52) | Evals ≥29 with `(Facts`: 30, 32, 33, 34, 36, 41, 43, 45, 50 → reason (`NOT_COMPUTABLE:4-12`); 35, 37, 38, 39, 40, 48, 49, 51, 53, 56, 57 → file; 42 has a file without the marker (allowed) |
| DA-P3 | 4 | `.claude-plugin/plugin.json:1-20`: valid JSON, `"version": "4.2"` = `SKILL.md:20`, `repository`, `license`, `keywords` present (matches `CHANGELOG.md:26`) |

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| DA1 | `skills/adversarial-verify/evals/facts/NOT_COMPUTABLE:13` | `52: the compiler is not installed on every machine` | Demonstrated defect (same root as C5, counted once there; listed here because the contract of claim 2 is in this file) | high | See C5 | Deductive | 90 | Delete the line |

### FALSIFIED HYPOTHESES
None.

## STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|
| S8 | Existence Question | DA-P3, the `version` in plugin.json (a 4th copy of the version) | yes | 80 | It is needed: the marketplace reads it (`README.md:125`), and `check_version` binds it (`scripts/check.py:231-236`) |

### SUMMARY (Data)
- Claims: 3 verified, 1 in FAIL (counted under C5), 0 falsified; Survived 1/1; Invariants I3 respected, I4 violated (C5); Hypotheses 0; Hidden behaviors 0.

---

# DOMAIN 4 — DOCUMENTATION (`README.md`, `CHANGELOG.md`, docstrings and messages)

## VERIFICATION DOMAIN
Documentation

## GROUND TRUTH
The actual code (`scripts/*`), the skill folder layout (`skills/adversarial-verify/` with `SKILL.md`, `references/`, `evals/`, `examples/`), `SKILL.md` (frontmatter `:20`, the Output Format, trust scoring `:466`, stress depth `:290`), `.gitignore`. There is no version history, so the "No rule changed by the split" claim and the size figures cannot be checked against git.

## INVARIANTS
I1 (the version in the docs) and I2 (the privacy promises in `README.md:251`) from Domain 1. Docs must state them correctly: `README.md:125` contradicts I1 (D2); `README.md:251`'s "any output line containing a term is masked" and "line break" are false as the code stands (C1, C3; the doc is correct to the intent, the code is wrong, so these are counted in Code); `README.md:261` is contradicted by the hook (C4, counted in Code).

## DECOMPOSED CLAIMS
1. The README install instructions produce a working skill — Deductive
2. README states the current version — Deductive
3. README's check descriptions (`:247-255`) match `check.py`/`check_facts.py` — Deductive
4. README's usage commands (`:258-264`) are correct — Deductive
5. README's method summary (`:12-81`, `:266-283`) matches SKILL.md — Deductive
6. CHANGELOG ordering and the "first entry" wording match `check.py` — Deductive
7. The CHANGELOG 4.2 sizes (57.3→46.4 kB; 62.5 kB) are true — Abductive (needs a byte count)
8. `_parse_day.py`'s header names its users — Deductive
9. The fact-file docstrings state what their asserts check — Deductive
10. README's mutation-tool table matches the tools' docs (`:226-241`) — Abductive (external, not read)

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Stale instructions / version mismatch | `README.md:89`, `README.md:125`, `CHANGELOG.md:3` | `README.md`, `CHANGELOG.md` |
| API drift (doc says, code doesn't) | `README.md:255` toolchain; `README.md:261` `--strict`; `README.md:250` every badge; `README.md:251` masking/separators; `scripts/check.py:42-44`; `scripts/check_facts.py:8` | `README.md`, `scripts/*` |

## VERIFICATION RESULTS
### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| D-P1 | 4 — usage | `README.md:258-260` flags exist (`scripts/check.py:419-421`); `:261` the relative symlink `../../scripts/pre-commit` from `.git/hooks/` resolves to `scripts/pre-commit`; `:264` matches `scripts/check.py:50` and `scripts/pre-commit:4` |
| D-P2 | 5 — method summary | `README.md:72` = `SKILL.md:290`; `README.md:78` confidence bands = `SKILL.md:333-343`; `README.md:270-272` = `SKILL.md:466`; `README.md:109-117` table = `SKILL.md:49-51` (3 files) |
| D-P3 | 3 (the rest) | `README.md:249` = `scripts/check.py:163-207`; `:252-254` = `:328-381`, `:506-520`; `:255` "from 29 on" = `FACTS_FROM` `:77`; `:247` "node 22.6 or later" matches the flag `--experimental-strip-types` (`scripts/check_facts.py:67`), added in Node 22.6 |
| D-P4 | 9 — fact docstrings | Each docstring states what its asserts check (`facts/35.py:2` … `facts/57.py:2`); `facts/38.py:20` documents the corrected 9.05 |

### FALSIFIED HYPOTHESES
| # | Location | Suspected defect | Check (quote) | Status | Could it have failed? | Paths not covered | Mode | Confidence |
|---|----------|------------------|-------|--------|-----------------------|-------------------|------|------------|
| D-FH1 | `CHANGELOG.md:7-8`, `:15` | Changelog entries cite evals that do not exist | "Eval 56", "Eval 57", "Evals 54 and 55" → `evals.json:697`, `:711`, `:671`, `:685`, with matching topics (long outputs, delegated reading, memory-backed FS) | falsified | Yes: a missing or renumbered id would show | Issue/PR numbers (#14, #17, #18, #20–#26) not verifiable here | Deductive | 88 |

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| D1 | `README.md:88-89` | `mkdir -p ~/.claude/skills/adversarial-verify` / `cp skills/adversarial-verify/SKILL.md ~/.claude/skills/adversarial-verify/` | Demonstrated defect | medium | A user following the first install method gets SKILL.md without `references/`. SKILL.md then sends the verifier to `references/pre-code.md`, `ux.md` and `execution.md` (`SKILL.md:49-51`), which are missing, and per `SKILL.md:53` it must work without them. The README itself says this is wrong (`README.md:117`: "SKILL.md alone would send the verifier to files that are not there") | Deductive | 92 | `cp -r skills/adversarial-verify ~/.claude/skills/` |
| D2 | `README.md:125` | `` `.claude-plugin/plugin.json` (currently 4.1), the same number as the skill's frontmatter and the badge above `` | Demonstrated defect | low | plugin.json says 4.2 (`.claude-plugin/plugin.json:3`), as do the frontmatter (`SKILL.md:20`) and the badge (`README.md:1`). The sentence contradicts itself and I1. `check_version` cannot catch it (it reads only `badge/skill-v…`, `scripts/check.py:217`) | Deductive | 95 | Drop the number ("…declares its version in plugin.json, the same number as…") so it cannot go stale again |
| D3 | `scripts/check_facts.py:8`, `README.md:255` | `A missing toolchain is an error, never a silent skip.` / `fails … if a needed toolchain (rustc, node 22.6 or later) is missing` | Demonstrated defect (doc side of C6, counted once in C6) | — | See C6 | Deductive | 92 | Fix the code (C6), not the doc |
| D4 | `CHANGELOG.md:3` | `the same in the skill's frontmatter, the README badge, … and the first entry below` | Demonstrated defect | low | The first entry below is `## Unreleased` (`CHANGELOG.md:5`); `check.py` compares the first **numbered** entry (`scripts/check.py:237`). A contributor following the sentence would number "Unreleased" | Deductive | 85 | "…and the first numbered entry below (Unreleased is skipped)" |
| D5 | `skills/adversarial-verify/evals/facts/_parse_day.py:1` | `# Shared by facts/37.py and facts/39.py` | Demonstrated defect | low | `facts/35.py:3` also imports it; a maintainer changing `parse_day_v1` for eval 37 does not know eval 35 depends on it | Deductive | 95 | `# Shared by facts/35.py, 37.py and 39.py` |
| D6 | `README.md:255` | `each fact file carries the sha256 of the prompt of every eval it covers` | Demonstrated defect | low | `check.py` reads one hash per file, bound to the eval named by the file's stem (`scripts/check.py:477-478`); `_parse_day.py`, which serves 4 evals, carries none and is exempt (`:469`). The sentence suggests a multi-eval binding that does not exist | Deductive | 82 | "…each `<id>.<ext>` file carries the sha256 of eval `<id>`'s prompt; shared helpers (`_*.py`) are not bound" |

## STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|
| S9 | Time Travel | D-P2, the README method summary duplicated from SKILL.md | yes (today) | 70 | It matches now, but nothing enforces it; D2 shows that prose copies of a value drift. No finding: risk only |
| S10 | Requirement Inversion | D-P1, usage on Windows | yes | 75 | `README.md:264` covers `py -3` and copying the hook; `pre-commit:7-8` falls back to `python` |
| S11 | Scale Shift | D-FH1, changelog references at 10× entries | yes | 70 | Entries cite eval ids, which `check.py` keeps consecutive and stable (`scripts/check.py:206`); renumbering is blocked |

## HYPOTHESES
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| D-H1 | `CHANGELOG.md:14`: "57.3 kB to 46.4 kB … 62.5 kB" | The current SKILL.md is ≈46.4 kB and SKILL.md + 3 references ≈62.5 kB | Sizes changed with the "Unreleased" edits to `execution.md` (`CHANGELOG.md:7-8`), so 62.5 kB is now stale; or kB means KiB | Proposed check P5 |
| D-H2 | `README.md:226-241` claims each cell comes from the tool's official docs read on 2026-10-21 | The cells are accurate | Tool docs changed since, or a cell was paraphrased wrongly | Read the linked docs (documentation pages; not opened, because the request limited reading to `./tree` and `./skill`) |
| D-H3 | `CHANGELOG.md:14` "No rule changed by the split" | True | Wording was edited in the move | `git diff` of the 4.2 split commit (no history available) |

## HIDDEN BEHAVIORS DETECTED
None beyond the code ones already reported (HB1–HB4 are the code side of D3, C4 and C9).

## ADVERSARIAL SCAFFOLD FINDINGS
- **Reviewer blind spots:** the README contradicts itself 28 lines apart (`:89` vs `:117`); "currently 4.1" sits next to a badge saying 4.2.
- **Highest-risk claims:** claim 1 (D1), claim 3 (C4/C6 doc side), claim 2 (D2).
- **Multi-step traces:** README `:89` → install without `references/` → `SKILL.md:53` degraded mode → every plan or UX verification runs without its rules.
- **Subtlety flags:** prose copies of checked values (`README.md:125`) escape the checks built for them.

### SUMMARY (Documentation)
- Claims: 4 verified, 6 in FAIL (5 counted here: D1, D2, D4, D5, D6; D3 counted in C6), 1 falsified
- Survived: 3/3
- Invariants: I1 contradicted at `README.md:125`
- Hypotheses: 3; Hidden behaviors: 0
- Findings by type: 5 demonstrated defects, 0 preventive measures, 1 falsified hypothesis

---

## CROSS-DOMAIN SUMMARY
- Domains: Code, Tests, Data, Documentation (UX considered, no separate claims)
- Claims: 23 verified (11 + 5 + 3 + 4), 24 in FAIL (17 demonstrated defects, 7 preventive measures; DA1 and D3 are counted once, under C5 and C6), 6 falsified (3 of them conditionally)
- Survived: 10/11 stress tests passed (S2 failed → C11)
- Failure categories: 6 distinct systemic patterns (silent fallthrough, missing completeness, stale state, assumed environment, tautological test / test-environment artifact, API and oracle drift)
- Invariants: 7 found, 7 touched; fully biting and respected: I3, I5, I6, I7; partly: I1 (C2, D2), I2 (C1, C3, C4); I4's mechanism bites but the repository violates it (C5)
- Hypotheses: 6
- Hidden behaviors: 6
- Findings by type: 17 demonstrated defects, 7 preventive measures, 6 falsified hypotheses (3 conditionally)
- Critical issues: 0 demonstrated defects of critical severity (preventive critical: 0). High: C1 (private term printed), C4 (hook without `--strict`), C5 (repo fails its own check)
- Changes touching several domains: the eval-52 conflict (Data → Code → Tests), the toolchain skip (Code → Tests → Docs), the masking leak (Code → Docs `README.md:251` → Tests `:341-344`)
- Pre-code: n/a
- Executed: 0 runs (reasoning only)
- Proposed: 6 checks and 17 writes awaiting an answer
- **Recommendation:** lower trust in "check.py is green" as a privacy and consistency gate until C1, C3, C4 and C5 are fixed. Several tests in `scripts/test_check.py` already encode the intended behavior and, as I traced it, would be red now (C-H2), which suggests these defects were introduced after the tests. Fix C5 first (it blocks every commit), then C1/C4 (privacy), then C2/C3/C6, then the eval oracles T3–T5 before grading the skill with them.

## PROPOSED EXECUTABLE CHECKS
| # | Claim | Confidence now | Check (command, test or query) | Confirms if | Refutes if | Cost and side effects | Status |
|---|-------|----------------|--------------------------------|-------------|------------|-----------------------|--------|
| P1 | C-H2: the unit suite is red on C1, C2, C3, C5 | 75 | `python3 -m unittest scripts/test_check.py -v` (from `tree/`) | Failures in `test_repo_passes`, `test_second_badge_mismatch`, `test_two_words_joined_any_way` (double-space subtest), `test_whole_word_term_glued_in_output_is_still_masked` | All green | Runs check.py about 80 times on temp copies; writes only to the system temp dir; with git, creates temp repos; runs the fact files (`FactsTest`) | proposed |
| P2 | C5: check.py fails on the repo | 90 (trace) | `CHECK_PRIVATE_TERMS=nosuchterm7f3a python3 -I scripts/check.py --root .` | `ERROR …/NOT_COMPUTABLE: eval 52 has a fact file and a reason` and exit 1 | Exit 0 | Read-only on the tree; one run | proposed |
| P3 | C-H1: all 13 `prompt-sha256` values are current | 50 | Covered by P2: check.py prints `prompt changed since its facts were checked` for any drift | No such line | Such a line for an id | Same as P2 | proposed |
| P4 | C6, C-FH1–3: facts true; toolchain skip exits 0 | 75 | (a) `python3 scripts/check_facts.py` with rustc and node ≥ 22.6; (b) the same with `PATH` lacking `node` | (a) `13 fact file(s), 0 failed`; (b) `skip 53.ts` and exit 0 (confirms C6) | (a) any FAIL; (b) a non-zero exit | Compiles 52.rs to a temp dir; runs 13 small programs; no repo writes | proposed |
| P5 | D-H1: CHANGELOG sizes | 45 | `wc -c skills/adversarial-verify/SKILL.md skills/adversarial-verify/references/*.md` | ≈46.4 kB and ≈62.5 kB total | Other figures | Read-only | proposed |
| P6 | Do the tests protect the risky lines? (mutation probe) | — | Hand mutations (3–5) on `scripts/check.py:90`, `:223`, `:400`, `:473`, `scripts/check_facts.py:92`, each followed by P1 | Every mutant killed by a named test | Survivors (expected at `:473`, `scripts/check_facts.py:92`: no test covers them) | Writes: each mutant is applied to a **separate copy** of `tree/`, then removed; the working copy is untouched; about 5 mutants × 1 suite run. A memory-backed filesystem (tmpfs/RAM disk) for the copy is optional and needs its own consent; the tree is a few hundred kB, so it fits in any free memory | proposed |

Proposed writes:
1. `scripts/check.py:400` → `term_patterns(terms, substring=True)` (C1)
2. `scripts/check.py:223` → `for b in badges:` (C2)
3. `scripts/check.py:90` → `SEP = r"[\W_]*"` (C3)
4. `scripts/pre-commit:9` → add `--strict` (C4)
5. `skills/adversarial-verify/evals/facts/NOT_COMPUTABLE:13` → delete the line (C5)
6. `scripts/check_facts.py:91-93` → count a missing toolchain as a failure (C6)
7. `scripts/check.py:214-237` → catch `OSError` and report an ERROR (C7); `:436` → report an empty staged index (C8); `:42-44` → reword item 7 (C9); `:473` → error on a second fact file per id (C10); `:363-366` → CommonMark fence closing (C12)
8. `scripts/pre-commit:12` → also trigger on `^scripts/check_facts.py` (C13)
9. `scripts/test_check.py:479` → real assertion (T1); `:575-578` → assert no `skip` line, plus a new missing-toolchain test (T2); skip guards at `:351`, `:502` (T6)
10. `skills/adversarial-verify/evals/evals.json:705` "11" → "12" (T3); `:612` reword (T4); `:249` current summary line (T5)
11. `README.md:88-89` → `cp -r` the folder (D1); `README.md:125` → drop "currently 4.1" (D2); `README.md:255` → hash-binding wording (D6)
12. `CHANGELOG.md:3` → "first numbered entry" (D4); `_parse_day.py:1` → add 35.py (D5)
13. Step 5 (project discovery): no `TODO.md`, `SPEC.md`, `PLAN.md`, `ADR/` or agent instruction files exist in `./tree`. Proposed: a `CHANGELOG.md` "Unreleased" bullet listing fixes 1–12 once they are applied.

**Which of these should I do: run checks P1–P6 (all, some, or none), and apply writes 1–13 (all, some, or none)?** Nothing will run or be written until you answer.
