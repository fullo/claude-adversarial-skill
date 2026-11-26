# Adversarial verification — `scripts/check.py`

**Cost estimate (large request: more than one domain, whole-file scope; the request accepted the cost and settled every choice, so the verification started without asking):** 1 file in scope (`scripts/check.py`, 532 lines), 2 domains (Code, Documentation), about 45 claims, nothing run.

## INTAKE

- **Target:** every domain detected in the file: **Code** (the logic of the seven checks, `main`, the helpers) and **Documentation** (the module docstring at `scripts/check.py:1-51`, which is the script's contract and the source of its `--help` description at `scripts/check.py:418`, plus the inline comments that state behavior). Given in the request.
- **Depth:** standard. Given in the request.
- **Scope:** the whole of `scripts/check.py`. There is no diff and no version history, so "changed path" means "the code in scope" throughout. Given in the request.
- **Execution mode:** reasoning only. Nothing was run, and every test result below is a prediction from tracing the code. Given in the request.
- Consent lasts for one verification. A later verification starts at reasoning only again. To change these choices, say "deep", "approved checks: the existing test suite", or name another file.
- Reference files of the skill: none was read. The artifact proposes no future work and is not a spike report (`references/pre-code.md`), UX is not in the target (`references/ux.md`), and no run was approved (`references/execution.md`).

---

# DOMAIN 1 — CODE

## VERIFICATION DOMAIN
Code

## GROUND TRUTH
- `scripts/test_check.py` (the unit tests of the script: each test states an intended behavior), read in full.
- `scripts/pre-commit` (how the script is invoked: `--strict --staged`), `scripts/check_facts.py` (the companion runner), `.gitignore`.
- The data the checks run on: `skills/adversarial-verify/SKILL.md`, `README.md`, `CHANGELOG.md`, `.claude-plugin/plugin.json`, `skills/adversarial-verify/evals/facts/` (headers, `NOT_COMPUTABLE`, `_parse_day.py`), and the fences and references in `skills/adversarial-verify/references/*.md` (searched).
- The script's own docstring and comments, used as the stated spec and cross-checked against the code (they are verified as claims in Domain 2).
- Python language semantics (regex, `unicodedata`, exception hierarchy). The GitHub-Flavored Markdown (GFM) table rules come from memory, not from a file in `./tree`, so findings that rest on them are capped at 79.

## INVARIANTS
Where I looked: the `./tree` file list (it has no `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, `SPEC.md`, `PLAN.md`, `ADR/`, `.claude/` or CI configuration), `scripts/check.py:1-51` (the invariants the script enforces), `README.md:244-263` ("Repository checks"), `CHANGELOG.md:3`, `scripts/test_check.py:1-6`, `scripts/pre-commit:1-18`, `.gitignore:1`.

**Found:** 8 invariants. All are touched, because `check.py` is the mechanism that enforces them.

| # | Invariant | Source | Touched by | Enforced by (file:line / test name) | Bites on changed path? |
|---|-----------|--------|------------|-------------------------------------|------------------------|
| I1 | SKILL.md version = **every** README skill badge = plugin.json = newest CHANGELOG entry | `scripts/check.py:10-12`, `README.md:249`, `CHANGELOG.md:3` | `check_version` `scripts/check.py:212-241` | `test_second_badge_mismatch` `scripts/test_check.py:171-173`; `test_badge_mismatch`, `test_plugin_*`, `test_changelog_*` `scripts/test_check.py:167-225` | **The test bites, but the code breaks the invariant.** `scripts/check.py:223` compares only the first badge, so by trace `test_second_badge_mismatch` would be red (FAIL C-1). Whether the test is currently red is run-only. |
| I2 | No private term in any tracked file's content or name, however its parts are joined | `scripts/check.py:13-19`, `README.md:250` | `term_patterns`, `check_private` `scripts/check.py:259-323` | `test_two_words_joined_any_way` `scripts/test_check.py:284-289`, and other `PrivateTest` tests | **The test bites, but the code breaks the invariant.** The separator allows only one character (`scripts/check.py:90`), so by trace the subtest with two spaces would be red (FAIL C-2). |
| I3 | Private terms are never printed: any output line containing one is masked | `scripts/check.py:22-23`, `scripts/check.py:399`, `scripts/test_check.py:4-5` | `mask` `scripts/check.py:397-414`, `print_report` `:523-527` | `test_whole_word_term_glued_in_output_is_still_masked` `scripts/test_check.py:341-344`; `assert_no_leak` `:70-73` | **The test bites, but the code breaks the invariant.** `mask` builds whole-word patterns for `=` terms (`scripts/check.py:400`), so by trace that test would be red (FAIL C-3). Tracebacks bypass `mask` entirely, and no test covers that (FAIL C-5). |
| I4 | The private-terms list is never committed | `scripts/check.py:423` (comment), `README.md:250`, `.gitignore:1` | `check_private` skips the file by basename (`scripts/check.py:301-302`) | `.gitignore:1` and `test_terms_file_is_gitignored` `scripts/test_check.py:365-366` | **Nothing in `check.py` bites.** `.gitignore` can be bypassed with `git add -f`. A tracked `.check-private-terms` is then skipped silently at `:301` and the commit passes (FAIL C-4). |
| I5 | evals.json: four keys, integer ids 1..n in file order, tags from eval 21 | `scripts/check.py:6-9` | `check_evals` `scripts/check.py:163-207` | `EvalsTest` `scripts/test_check.py:104-163` | Yes, by trace: each rule has a test that would fail if the rule were removed (see PASS 1-4). |
| I6 | Markdown tables keep the header's cell count | `scripts/check.py:30-33` | `check_tables` `scripts/check.py:341-381` | `TablesTest` `scripts/test_check.py:420-450` | It bites on the tested shapes. Fence nesting and setext/rule lines are untested and mis-handled (FAIL C-7, C-8). |
| I7 | Eval facts are bound to their prompt by sha256; every eval from 29 on that states facts has a file or a reason, not both | `scripts/check.py:34-38` | `check_facts` `scripts/check.py:457-501` | `FactsTest` `scripts/test_check.py:515-568` | Yes, by trace (PASS 13-14). |
| I8 | Every named `references/*.md` exists, and every file there is named in SKILL.md | `scripts/check.py:39-44` | `check_references` `scripts/check.py:506-520` | `ReferencesTest` `scripts/test_check.py:456-509` | Yes, by trace (PASS 15). |

No mechanism in `./tree` runs `scripts/test_check.py` automatically. `scripts/pre-commit:9-18` runs only `check.py` and `check_facts.py`, and I found no CI configuration in the `./tree` file list. So tests that bite (I1-I3) do not stop a regression of `check.py` from being committed (HYPOTHESES H-5).

## DECOMPOSED CLAIMS
1. `check_evals` rejects a boolean id. — Deductive
2. `check_evals` reports duplicates and gaps, both at once. — Deductive
3. `check_evals` requires `[substance]`/`[format]` + text from eval `TAGGED_FROM` (21) on. — Deductive
4. `check_evals` reports extra and missing keys. — Deductive
5. The version is read only from the frontmatter, with CRLF tolerated. — Deductive
6. Every README skill badge is compared with the frontmatter version. — Deductive
7. plugin.json must hold a string version equal to SKILL.md's. — Deductive
8. The newest CHANGELOG entry is the first numeric `## <version>`, and "## Unreleased" is skipped. — Deductive
9. A missing or unreadable required file is reported as an ERROR, and the run still reaches its summary. — Deductive
10. The parts of a term match when joined by any run of non-alphanumerics, or by nothing. — Deductive
11. Terms match case-, accent- and Unicode-form-insensitively. — Deductive
12. `=` terms match whole words only during detection. — Deductive
13. Masking hides every output line that contains a term, including `=` terms glued to other text. — Deductive
14. No path prints a term outside `mask` (tracebacks included). — Deductive
15. JSON strings are scanned after their escapes are decoded. — Deductive
16. Decoding never fails (UTF-8, UTF-16 with BOM, Latin-1). — Deductive
17. A term with no letters is an error; a short term is a warning, with the `=` hint only for non-`=` terms. — Deductive
18. File names are scanned. — Deductive
19. The terms file supports a BOM and `#` comments. — Deductive
20. The terms list cannot be committed unnoticed. — Deductive
21. An empty `CHECK_PRIVATE_TERMS` does not hide a configured terms file. — Deductive
22. `--staged` checks exactly the index and always removes its temporary directory. — Deductive
23. `--staged` with no files still applies `--strict`. — Deductive
24. In `--staged` mode, terms are loaded from the working repo. — Deductive
25. `check_neutral` warns without failing and excludes evals.json. — Deductive
26. Tables are found and counted correctly, with or without outer pipes. — Deductive
27. Fenced code blocks are skipped correctly for every fence form. — Deductive
28. A `---` line is treated as a table delimiter only inside a table. — Deductive
29. Pipes in code spans are excluded as GitHub renders them. — Deductive (spec from memory)
30. The line numbers in table errors are correct. — Deductive
31. A fact file is bound to its prompt by sha256. — Deductive
32. A fact file plus a reason is an error; a stated fact needs one of the two. — Deductive
33. `check_facts` cannot crash on malformed evals.json. — Deductive
34. References are checked in both directions. — Deductive
35. A non-UTF-8 skill file is reported once. — Deductive
36. The exit code is non-zero exactly when there is an error. — Deductive
37. The script runs on Python 3.8. — Deductive
38. Tests that encode claims 6, 10 and 13 are currently green. — Abductive (run-only)

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Missing completeness | `mask` does not apply the substring mode its comment promises (`scripts/check.py:399-400`). The badge loop is cut to one element (`:223`). The terms-file skip has no matching "is it tracked?" check (`:301`). The `substring` parameter (`:259`) is passed by no caller. | `scripts/check.py` |
| Silent fallthrough | OSError is caught only around evals.json (`:167`) and per-file in `check_private` (`:308`), not at `:214, :217, :227, :237, :332, :356, :476, :512`. `"evals": null` crashes at `:463`. A stale NOT_COMPUTABLE reason is accepted (`:494`). `--staged` with an empty index skips every check (`:436`). | `scripts/check.py` |
| Assumed environment | One-character separator vs CRLF line breaks on Windows (`:90`). NFKD does not fold stroke letters (`:93-96`). The GFM rendering of pipes in code spans (`:345`). The Windows path in `--prefix` (`:389`). | `scripts/check.py`; the test `scripts/test_check.py:286` (writes `\n`, which text mode turns into `\r\n` on Windows) |
| Implicit ordering | `check_facts` relies on `check_evals` having reported a malformed file ("check 1 already reports it", `:462`), but crashes on `null` before the summary. | `scripts/check.py` |
| Stale state (comment/test drift) | The comment at `:399` vs the code at `:400`. The test comment `scripts/test_check.py:337` says detection is whole-word by default; it is substring (`:265`). | `scripts/check.py`, `scripts/test_check.py` |

## OUT OF SCOPE (listed, not verified)
- `scripts/test_check.py:337`: the comment "whole-word detection does not flag `<term>labs`" is stale. The default is substring (`scripts/check.py:265`), so detection *does* flag it. The test still passes for another reason.
- `scripts/test_check.py:286`: the subtest `f"{a}\n{b}"` is written in text mode (`:85`). On Windows that becomes `\r\n`, which the one-character separator does not match. This is a Windows-only red that comes from the same root cause as C-2.
- `scripts/pre-commit:9-18` does not run `scripts/test_check.py`. This is the same missing-completeness pattern as I4: an enforcement that exists but is not wired into the commit path.

## VERIFICATION RESULTS

### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| 1 | Boolean id rejected | `scripts/check.py:186` `type(i) is not int`: `type(True)` is `bool`, so it is rejected. Covered by `scripts/test_check.py:125-127`. Confidence 92. |
| 2 | Duplicates and gaps both reported | `:203-207`: two independent `if`s, no early return. Covered by `scripts/test_check.py:117-119`. Confidence 90. |
| 3 | Tag rule from eval 21 | `:74-75`, `:201`: `i >= TAGGED_FROM` with `^\[(substance\|format)\]\s+\S`, so `[format]` alone fails (needs whitespace then a non-space). Boundary covered by `scripts/test_check.py:149-163`. Confidence 90. |
| 4 | Extra and missing keys | `:180-184`: set differences both ways. Confidence 90. |
| 5 | Version only from frontmatter, CRLF tolerated | `:215` anchors `\A---\n…\n---\n` after `replace("\r\n","\n")`; `:216` searches only `fm.group(1)`. Current data: `skills/adversarial-verify/SKILL.md:20` `version: "4.2"`. Confidence 88. |
| 7 | plugin.json string version | `:231-236`: a non-string (e.g. `4.1` float) gives "no version (a string)". `.claude-plugin/plugin.json:3` is `"4.2"`. Confidence 88. |
| 8 | Newest CHANGELOG entry = first numeric heading | `:237` `re.search(r"^## +([0-9][0-9.]*)\b", …, re.M)` skips `CHANGELOG.md:5` "## Unreleased" and takes `CHANGELOG.md:10` "## 4.2", which matches. Confidence 88. |
| 12 | `=` terms whole-word in detection | `:265`, `:275` lookarounds `(?<![^\W_])…(?![^\W_])`. Confidence 88. |
| 15 | JSON escapes decoded | `:313-317`, `:322`: keys and values via `json_strings` (`:279-289`), normalized. Confidence 88. |
| 16 | Decoding never raises | `:112-122`: Latin-1 decodes any byte sequence, and a UTF-16 failure falls through to it. Confidence 92. |
| 17 | No-letter term is an error; short-term warning and hint | `:266-273`. Confidence 90. |
| 18 | File names scanned | `:303-305` on `normalize(rel)` (the full path). Confidence 90. |
| 19 | Terms file: BOM and comments | `:255` uses `decode` (utf-8-sig strips the BOM), then filters `#` lines after `strip()`. Confidence 88. |
| 22 | `--staged` reads the index; temp dir always removed | `:386-394` `checkout-index -a --prefix=tmp/`, `:438-440` `finally: shutil.rmtree`, also when `staged_tree` returns None. Confidence 85 (the Windows path form is open: H-2). |
| 24 | Terms from the working repo in `--staged` | `:423` `load_terms(args.root)` runs before `root = tmp` (`:433`). Confidence 90. |
| 25 | Neutral wording: warnings only, evals excluded | `:328-336` uses `rep.warning`. `skill_docs` (`:140-142`) lists SKILL, references, README only. Confidence 90. |
| 30 | Table error line numbers | `:373` "header at line {i}" (0-based `i-1`, so 1-based `i`). `:378` uses `start` = delimiter index, which is also the header's 1-based line. Confidence 85. |
| 31 | Fact file bound by sha256 | `:475-482`: hash of `str(prompt).encode("utf-8")` vs the first 64-hex match in the first 2000 chars. All 13 fact files carry the line at line 1 (`skills/adversarial-verify/evals/facts/35.py:1` … `57.py:1`). Confidence 88. |
| 32 | File + reason is an error; facts need one of the two | `:495-501`. Current `skills/adversarial-verify/evals/facts/NOT_COMPUTABLE:4-12` and fact files are disjoint. Confidence 88. |
| 34 | References checked both ways | `:506-520`: names in SKILL and reference files must exist; every `.md` in the folder must be named in SKILL. Current SKILL names all three (`skills/adversarial-verify/SKILL.md:49-51`). Confidence 90. |
| 36 | Exit code | `:442` `return 1 if rep.errors else 0`; warnings never set it. Confidence 92. |
| 37 | Python 3.8 | No 3.9+ construct found in `:1-532` (no `removeprefix`, no `X \| Y` types, no `list[...]` annotations, no `match`). `capture_output` is 3.7+. Confidence 82. |

### FALSIFIED HYPOTHESES
| # | Location | Suspected defect | Check (quote) | Status | Could it have failed? | Paths not covered | Mode | Confidence |
|---|----------|------------------|-------|--------|------------------------|-------------------|------|------------|
| FH-1 | `scripts/check.py:237` | "## Unreleased" (`CHANGELOG.md:5`) is taken as the newest entry, so the version check always fails. | Trace of `re.search(r"^## +([0-9][0-9.]*)\b", …)` on `CHANGELOG.md:1-10`. | falsified | Yes: had the pattern been `^## +(\S+)`, the trace would have yielded "Unreleased" ≠ "4.2". The actual pattern requires a digit. | A heading like `## 4.2a` (captures "4."); a numeric heading inside the Unreleased section. | Deductive | 85 |
| FH-2 | `scripts/check.py:301` | The working repo's own terms file is reported as a leak in fallback (no-git) mode. | `if os.path.basename(rel) == TERMS_FILE: continue` | falsified | Yes: without the line, `os.walk` (`:154-157`) would list `.check-private-terms` and every term would match its own line. | None for the root file. The same skip creates C-4 for a *tracked* copy. | Deductive | 88 |
| FH-3 | `scripts/check.py:203` | `ids.count` inside a set comprehension is O(n²) and too slow. | Trace with the current 57 evals and at 100× (5,700): about 3×10⁷ comparisons, well under a second in CPython. | conditionally | Only a timed run decides (run-only). It would be complete with "a timed run on 5,700 synthetic evals finishes in < 1 s". | Very large eval files (not plausible here). | Deductive | 70 |

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| C-1 | `scripts/check.py:223` | `for b in badges[:1]:` | Demonstrated defect | medium | README has `badge/skill-v4.2-…` at `README.md:1` and a stale `badge/skill-v2.0-blue` further down. `badges == ["4.2","2.0"]`, only `"4.2"` is compared, no error, and the stale badge ships. This contradicts the docstring `:10` "every skill badge", `README.md:249`, and `test_second_badge_mismatch` (`scripts/test_check.py:171-173`), which by trace would be red. | Deductive | 92 | `for b in badges:` |
| C-2 | `scripts/check.py:90` (used at `:274`) | `SEP = r"[\W_]?"  # anything that is not a letter or digit, possibly nothing` | Demonstrated defect | high | Term `quillane dorvex` is built as `quillane[\W_]?dorvex`. File text `QUILLANE  dorvex` (two spaces), `Quillane\r\nDorvex` (any CRLF file, e.g. written on Windows), `Quillane,\n  Dorvex` (wrapped and indented Markdown/JSON) or `Quillane - Dorvex`: no match, no ERROR, and the private name is committed. It is also not masked in output, since `mask` uses the same patterns. This contradicts the docstring `:16-18` "joined by anything that is not a letter or digit … or by nothing" and the subtest `f"{a.upper()}  {b}"` in `scripts/test_check.py:286`, which by trace would be red. | Deductive | 92 | `SEP = r"[\W_]*"` (the lookarounds and the parts are unchanged; the regex stays linear). Then extend the docstring's "Not caught" list only with what is still true. |
| C-3 | `scripts/check.py:399-400` | `# substring patterns: when hiding output, err on the side of hiding too much` / `pats = term_patterns(terms)` | Demonstrated defect | high | Terms `=zqvorblax` and an evals.json key `zqvorblaxlabs`. `check_evals` emits `unexpected keys ['zqvorblaxlabs']` (`:182`). Detection does not flag it (whole word), and `mask` builds the same whole-word pattern (`substring` defaults to `False`, `:259`, `:265`). The line is printed with the private term, to a terminal or to CI logs. This contradicts the docstring `:22-23` "any output line containing one is masked", the comment `:399`, and `test_whole_word_term_glued_in_output_is_still_masked` (`scripts/test_check.py:341-344`), which by trace would be red. | Deductive | 92 | `pats = term_patterns(terms, substring=True)` |
| C-4 | `scripts/check.py:301-302` | `if os.path.basename(rel) == TERMS_FILE: continue` | Preventive measure | high | Likelihood low: someone runs `git add -f .check-private-terms`, or edits `.gitignore:1`, or a sub-folder copy gets tracked. `staged_tree` lists it, `:301` skips it silently, the hook (`scripts/pre-commit:9`) passes, and the **whole** private list is committed. The invariant at `:423` / `README.md:250` ("never committed") has no mechanism in `check.py` that bites. | Deductive | 85 | When the file list comes from git (`list_files` succeeded, or `--staged`), report `rep.error(rel, "the private-terms list is tracked: remove it from the index")` instead of `continue`. Keep the skip only for the untracked root file in fallback mode. Add a test. |
| C-5 | `scripts/check.py:214, 217, 227, 237, 332, 356, 476, 512` | `skill = read_text(root, SKILL, rep)` … `except ValueError as e:` (`:228`, OSError not caught) | Demonstrated defect | medium | A commit that deletes or renames `README.md`, `CHANGELOG.md`, `.claude-plugin/plugin.json` or SKILL.md (staged tree lacks it) makes `read_text` raise `FileNotFoundError`, which is uncaught. The script stops with a traceback: no ERROR line, no summary, and checks 3-7 never run. The exit is non-zero (fail-closed), but `assert_fails`-style expectations ("checked (" in stdout) are not met and the reason is buried. Same with `"evals": null` in evals.json: `check_evals` reports "no 'evals' list", then `:463` iterates `None` and raises `TypeError`. | Deductive | 88 | Wrap each `read_text` of a required file in `try/except OSError` and add `rep.error(rel, "missing or unreadable")`. In `check_facts` use `evals = … .get("evals"); if not isinstance(evals, list): return`. Optionally wrap `run_checks` in a last-resort `except Exception` that adds a masked ERROR. |
| C-6 | `scripts/check.py:530-531` (with C-5) | `sys.exit(main())` (no handler; tracebacks bypass `mask`, `:524`) | Preventive measure | medium | Likelihood low-to-moderate: the error of C-5 occurs, and the absolute root path contains a configured term (e.g. the user's own name in `C:\Users\<name>\…` or `/home/<name>/…`, a typical private term). The traceback prints the path unmasked on stderr, or in CI logs. This contradicts `:22-23`. | Deductive | 80 | The handler proposed in C-5 must print only `mask([...])`ed text and never the raw traceback (or print the traceback through `mask`). |
| C-7 | `scripts/check.py:361-366` | `if fence is None: fence = f.group(1)[0]` / `else: fence = None` | Preventive measure | low | `fence` stores the fence character, but it is never compared, and length and info string are ignored. A ```` ```` ```` block that shows a ```` ``` ```` example (common in docs about Markdown), or a `~~~` line inside a ```` ``` ```` block, flips the state. From then on, broken tables are silently skipped and code content gives false errors. There is no current instance: all fences in `README.md:87-282`, `skills/adversarial-verify/SKILL.md:367,456`, `references/execution.md:70,81`, `references/pre-code.md:55,60` are simple pairs. | Deductive | 85 | Track `(char, length)`. Close only on a line of the same char, at least as long, with nothing after it. |
| C-8 | `scripts/check.py:341, 369` | `DELIM = re.compile(r"^\s*\|?\s*:?-{3,}:?…")` / `"\|" in lines[i] + lines[i - 1]` | Preventive measure | low | (a) A `---` thematic break (or setext underline) right after a paragraph line containing `\|`, or right after a table without a blank line, is taken as a one-cell delimiter: false ERROR "table delimiter has 1 cells", and the commit is blocked. (b) A GFM delimiter with one or two dashes (`\|-\|-\|`) is not recognized, so that table is never checked. | Deductive | 82 | Require the delimiter to have ≥2 cells, or a pipe on the delimiter line itself. Accept `-{1,}`. |
| C-9 | `scripts/check.py:345` | ``s = re.sub(r"`[^`]*`", "x", line)`` | Preventive measure | low | GFM (from memory of the spec, not checkable in `./tree`) splits table cells at an unescaped `\|` even inside a code span. A row like ``\| x \| `a\|b` \|`` passes the check but renders with an extra cell on GitHub, where `README.md` is shown. Double-backtick spans (``` ``a\|b`` ```) are also mis-stripped by the single-backtick regex. There is no current instance in `./tree`. | Deductive | 65 | Treat a pipe inside a code span as a separator unless escaped (`\|`), matching GFM, and update `:32` and `scripts/test_check.py:441-443`. Or keep the current rule and say in `:32` that it differs from GitHub rendering. |
| C-10 | `scripts/check.py:93-96` | `unicodedata.normalize("NFKD", text)` … `not unicodedata.combining(c)` | Preventive measure | low | NFKD does not decompose stroke and ligature letters (ł, ø, đ, æ, ß→"ss" only via casefold). Term `Lukasz` vs text `Łukasz`, or `Soren` vs `Søren`: no match, and the name leaks. The docstring `:15-16` says matching "ignores … accents". Likelihood depends on the configured names. | Deductive | 75 | Add an explicit fold table (ł→l, ø→o, đ→d, æ→ae, œ→oe, þ→th) after NFKD, or list these letters under "Not caught". |
| C-11 | `scripts/check.py:247-249` | `raw = os.environ.get("CHECK_PRIVATE_TERMS")` / `if raw is not None:` | Preventive measure | low | `CHECK_PRIVATE_TERMS=` is exported empty (a CI template, a shell profile) while `.check-private-terms` exists. The result is `[]`, the file is ignored, and the message says "set CHECK_PRIVATE_TERMS or create .check-private-terms" although the file exists. Without `--strict` (the README's first command, `README.md:257`), private names go unchecked. The hook uses `--strict`, so commits are protected. | Deductive | 85 | Use the env var only if it yields at least one term (`if raw is not None and raw.strip(","+" ")`), or name the source in the message ("CHECK_PRIVATE_TERMS is set but empty; .check-private-terms was ignored"). |
| C-12 | `scripts/check.py:436` | `if files or not args.staged:` | Preventive measure | low | `--staged` in a repository whose index is empty: `files == []`, and no check runs (not even the `--strict` "no private terms" failure). The script prints "0 error(s)" and exits 0. Likelihood very low (a commit of an empty index is not normal). | Deductive | 82 | Run `run_checks` whenever `files is not None`, or report "nothing staged" explicitly. |
| C-13 | `scripts/check.py:128, 214, 512` | `rep.error(rel, f"not UTF-8 (read as {enc})")` | Demonstrated defect | low | A SKILL.md saved as Latin-1 is read with `rep` in `check_version` (`:214`) and in `check_references` (`:512`), so the same ERROR appears twice. Cosmetic, and it skews the error count in the summary (`:527`). | Deductive | 88 | Record each file once (e.g. a `set` of reported files in `Report`). |
| C-14 | `scripts/check.py:470-473, 494` | `if not stem.isdigit() or int(stem) not in ids:` / `reasons[int(m.group(1))] = m.group(2)` | Preventive measure | low | (a) `035.py` and `35.py` both map to eval 35, the later one overwrites, and `035.py` is never hash-checked (while `check_facts.py` would run it expecting "ok 035"). (b) A NOT_COMPUTABLE line for a removed or non-existent eval, or for an eval that states no facts, is accepted silently. This is stale state. | Deductive | 82 | Reject stems with leading zeros or with a duplicate id. Report reasons whose id is not an eval from `FACTS_FROM` on that states facts. |

## STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|
| S-1 | Scale Shift | Claim 2, the id checks (`:174-207`) | yes | 80 | At 0 evals: "no 'evals' list" (`:171-173`). At 1: range(1,2). At 100×: see FH-3, quadratic but small. At negative ids: not consecutive, so an error. |
| S-2 | Requirement Inversion | Claim 21, where the terms come from (`:246-256`) | **no** | 85 | Invert "env wins" into "the file wins when the env gives nothing". The current code cannot express it: an empty env shadows the file. This is C-11. |
| S-3 | Time Travel | Claim 27, fence skipping (`:357-367`) | **no** | 85 | In 6 months a contributor adds a reference file that shows a fenced example inside a 4-backtick fence. The `fence` variable looks like it tracks the fence type but does not, which misleads the next reader. This is C-7. |
| S-4 | Existence Question | The `substring` parameter of `term_patterns` (`:259`) | **no** | 90 | Delete it mentally and nothing changes: neither caller (`:299`, `:400`) passes it. The one caller that should (`mask`, per `:399`) does not. Its existence hides C-3. |
| S-5 | Existence Question | Claim 28's guard `"\|" in lines[i] + lines[i - 1]` (`:369`) | yes | 82 | Without it every `---` horizontal rule or setext underline would start a "table", so it is needed. It is insufficient, though (C-8). |
| S-6 | Time Travel | Claim 35's path list for UTF-8 enforcement (`:128`) | yes | 80 | A new reference file is covered automatically through the `REFS_DIR + "/"` prefix, with no list to update. |
| S-7 | Scale Shift | Claim 31, hash binding of 0 vs many fact files (`:475-482`) | yes | 82 | 0 files: loops are empty and no error is reported, which is correct, since the requirement is enforced at `:497-501`. Many files: one read of at most 2,000 chars each. |

## HYPOTHESES (Abductive — require further investigation)
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| H-1 | Three tests in `scripts/test_check.py` (`:171-173`, `:284-289`, `:341-344`) assert behavior that `scripts/check.py:223`, `:90` and `:400` do not implement. | `check.py` regressed (or was edited) after the tests were written, and the suite is currently red on these three. | The tests were written first (tests-first method) and the fixes are pending. Or a test-environment difference makes them pass (no such fixture found: they use a plain copy and a subprocess). | Run the three tests (PROPOSED CHECK 1). |
| H-2 | `:389` builds `--prefix=` with `os.sep` (backslashes on Windows). | Git for Windows accepts it and writes the staged tree into the temp dir. | Git treats `\` literally in the prefix and writes elsewhere or fails, so `--staged` reports "not a git repository" on Windows. | Run `py -3 scripts/check.py --staged` in a Windows checkout (PROPOSED CHECK 5). |
| H-3 | `staged_tree` returns None on *any* `checkout-index` failure (`:392-393`). | Failures happen only outside a repository, as the message says (`:431`). | Unmerged index entries, or an unwritable temp dir, also produce "not a git repository", which is misleading. | Run `--staged` during a merge conflict (PROPOSED CHECK 6). |
| H-4 | C-9 rests on GFM's table rules recalled from memory. | GitHub splits cells at unescaped pipes inside code spans. | GitHub keeps code-span pipes inside the cell, so `:32` and `:345` are right. | Render a one-row table with ``` `a\|b` ``` on GitHub (that is publishing, so it needs consent), or read the GFM spec section "Tables (extension)". |
| H-5 | No file in `./tree` runs `scripts/test_check.py` automatically (`scripts/pre-commit:9-18` runs `check.py` and `check_facts.py` only; no CI config in the `./tree` file list). | Regressions in `check.py` (such as C-1 to C-3) can be committed unnoticed. | CI exists in the upstream repository outside this snapshot. | Inspect the upstream repository's CI configuration. |

## HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| HB-1 | `scripts/check.py:259, 400` | "substring patterns" in masking (`:399`) | Masking uses whole-word patterns for `=` terms. | Demonstrated defect (C-3) | 92 |
| HB-2 | `scripts/check.py:90` | "anything that is not a letter or digit" | At most one such character | Demonstrated defect (C-2) | 92 |
| HB-3 | `scripts/check.py:301` | The terms file is "never committed" | If committed, it is silently not scanned and not reported. | Preventive measure (C-4) | 85 |
| HB-4 | `scripts/check.py:149-152` | Fallback "if git is not available" (`:46`) | Also when git is present but root is not a repo, or has no tracked files. The tests rely on this (temp copies are not repos). | Documentation drift (D-1) | 88 |
| HB-5 | `scripts/check.py:319-321` | "No private term appears" | Only the first occurrence per term per file is reported (one line number). Later occurrences surface only after the first is fixed. | — (not a problem; worth knowing) | 88 |
| HB-6 | `scripts/check.py:82-88, 330-335` | "technology-bound terms" | Case-sensitive and mostly unanchored: `React` also matches "Reactive", `Spring` matches "Springfield". `python`/`sql` in lower case are not flagged. Warnings only. | — (noise, not blocking) | 85 |
| HB-7 | `scripts/check.py:216` | The version comes from the frontmatter | The first line matching `version:` *anywhere* in the frontmatter, at any nesting. A version with a suffix (`4.2-beta`) gives "no version in the frontmatter". | — (low) | 82 |

## ADVERSARIAL SCAFFOLD FINDINGS
- **Reviewer blind spots:** the comment at `:399` reads as if masking were substring-based, so a reviewer trusts it. The `?` in `:90` is one character. `badges[:1]` looks like a guard against an empty list. `fence` looks like it tracks the fence type.
- **Highest-risk claims (blast radius × probability):** (1) Claim 13 / C-3, a private term printed to logs. (2) Claim 10 / C-2, private names committed through common separators (CRLF, double spaces, wrapped text). (3) Claim 20 / C-4, the whole terms list committed unnoticed (high impact, low probability).
- **Multi-step traces:** evals.json key `<term>labs` → `check_evals` `:182` message → `print_report` `:524` → `mask` `:400` builds whole-word patterns → printed (C-3). Staged deletion of README → `check_version` `:217` → `FileNotFoundError` → traceback with the absolute root path → unmasked (C-5 → C-6). CRLF file → `normalize` keeps `\r\n` → `SEP` matches one char → miss in both detection and masking (C-2).
- **Subtlety flags:** `:90` (`?` vs `*`), `:223` (`[:1]`), `:259` (an unused parameter with a safety meaning), `:301` (a silent `continue` on a privacy-critical file), `:362-366` (a state variable stored but never read).

---

# DOMAIN 2 — DOCUMENTATION

## VERIFICATION DOMAIN
Documentation (the module docstring `scripts/check.py:1-51`, which is also the `--help` description via `:418`, and the behavioral comments at `:74, :77, :90, :399, :423, :462`)

## GROUND TRUTH
The code of `scripts/check.py` (traced in Domain 1), `README.md:244-263`, and `scripts/test_check.py`.

## INVARIANTS
Same search as Domain 1. The doc touches I1-I8 by describing them.

| # | Invariant | Source | Touched by | Enforced by | Respected? |
|---|-----------|--------|------------|-------------|------------|
| I1 | Every badge agrees | `:10` | the docstring states it | — | Stated correctly; the code contradicts it (C-1) |
| I2 | Any join of the parts | `:16-18` | the docstring states it | — | Stated correctly; the code contradicts it (C-2) |
| I3 | Terms never printed | `:22-23` | the docstring states it | — | Stated correctly; the code contradicts it (C-3, C-6) |
| I4 | List never committed | `:423` | the comment states it | — | Stated; nothing enforces it in the code (C-4) |
| I5-I8 | evals, tables, facts, references | `:6-9, :30-44` | the docstring states them | — | Respected (see PASS) |

## DECOMPOSED CLAIMS
D1. "Errors make the exit code non-zero; warnings … do not block" (`:4`) — Deductive
D2. The evals rules (`:6-9`) — Deductive
D3. "matches every skill badge … plugin.json … first '## <version>' entry" (`:10-12`) — Deductive
D4. Term sources, "one per line, # for comments" (`:13-15`) — Deductive
D5. "ignores case, accents and Unicode forms; … joined by anything … or by nothing" (`:15-18`) — Deductive
D6. "matches anywhere …; = matches only as a whole word" (`:18-20`) — Deductive
D7. "< 4 characters → warning; no letters or digits → error" (`:20`) — Deductive
D8. "JSON strings are also scanned after decoding escapes" (`:20-21`) — Deductive
D9. "UTF-16 if it has a BOM, otherwise Latin-1" (`:21-22`) — Deductive
D10. "Terms are never printed: any output line containing one is masked" (`:22-23`) — Deductive
D11. "Without terms the check says so; with --strict it fails" (`:23-24`) — Deductive
D12. The "Not caught" list is complete (`:24-26`) — Deductive
D13. Neutral wording, evals.json excluded (`:27-29`) — Deductive
D14. Tables: outer pipes optional, escaped pipes and code spans, fences skipped (`:30-33`) — Deductive
D15. Facts rules (`:34-38`) — Deductive
D16. References rules, folder read "as it is on disk, tracked or not" (`:39-44`) — Deductive
D17. "Files checked: the files tracked by git (all files outside .git if git is not available). With --staged, exactly the content staged" (`:46-47`) — Deductive
D18. Usage and "Requires Python 3.8 or later" (`:49-50`) — Deductive
D19. `staged_tree` returns None only "if root is not a git repository" (`:387`) — Deductive
D20. "check 1 already reports it" (`:462`) — Deductive
D21. "the list is never committed" (`:423`) — Deductive

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| API drift (doc promises what the code does not do) | D3, D5, D10, D12 | `scripts/check.py` |
| Stale/misleading comment | `:399`, `:462` (null case), `:387` | `scripts/check.py` |
| Missing docs | the precedence of env over file (D4); the GFM divergence (D14) | `scripts/check.py` |

## OUT OF SCOPE (listed, not verified)
`README.md:249-250` repeats D3, D5 and D10 word for word, so the same drift applies there. `CHANGELOG.md:3` repeats D3.

## VERIFICATION RESULTS

### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| D1 | Exit code | `:442`, `:108-109`. Confidence 92. |
| D2 | evals rules | `:163-207` (Domain 1 PASS 1-4). Confidence 90. |
| D6 | Substring by default, `=` whole word (in detection) | `:265, :275`. Confidence 88. |
| D7 | Short-term warning; no-letter error | `:266-273`. Confidence 90. |
| D8 | JSON decoding | `:313-323`, `.json` files only, as written. Confidence 88. |
| D9 | Encodings | `:112-122`. Confidence 90. |
| D11 | Missing terms said; fails with `--strict` | `:294-298`. Exception: `--staged` with an empty index (C-12). Confidence 82. |
| D13 | Neutral wording | `:328-336`, `:140-142`. Confidence 90. |
| D14 | Table rules as described | `:341-381` does what `:30-33` says. Whether that matches GitHub is C-9. Confidence 85. |
| D15 | Facts | `:457-501`. Confidence 88. |
| D16 | References, read from disk | `:133-137` `os.listdir`. In `--staged` mode "disk" is the checkout of the index, consistent with `:47` and `scripts/test_check.py:501-509`. Confidence 85. |
| D18 | Usage, Python 3.8 | `:417-422`; Domain 1 PASS 37. Confidence 82. |

### FALSIFIED HYPOTHESES
| # | Location | Suspected defect | Check (quote) | Status | Could it have failed? | Paths not covered | Mode | Confidence |
|---|----------|------------------|-------|--------|------------------------|-------------------|------|------------|
| DF-1 | `scripts/check.py:11-12` | "first '## <version>' entry" is wrong because the CHANGELOG starts with "## Unreleased" (`CHANGELOG.md:5`). | Trace of `:237` | falsified | Yes (see FH-1): a non-numeric first heading would have been taken by a looser pattern. "## <version>" in the docstring means a numeric heading, and the code skips "Unreleased". | — | Deductive | 85 |

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| D-1 | `scripts/check.py:46-47` | "(all files outside .git if git is not available)" | Demonstrated defect | low | The fallback also runs when git *is* available but `--root` is not a repository, or has no tracked files (`:146-152`). This is the path every non-staged test takes (`scripts/test_check.py:31-37`). A reader may assume that a non-repo root with git installed fails or scans nothing. | Deductive | 88 | "(every file outside .git when git is not available, the root is not a repository, or nothing is tracked)" |
| D-2 | `scripts/check.py:13-15` | "Terms come from CHECK_PRIVATE_TERMS (comma-separated) or the untracked file .check-private-terms" | Preventive measure | low | The precedence is not stated: when the env var is set, even empty, the file is ignored (C-11). A user who has the file and an empty env var reads "or" and expects the file to apply. | Deductive | 85 | State it: "CHECK_PRIVATE_TERMS, when set, replaces the file". Better, fix C-11 and document the new rule. |
| D-3 | `scripts/check.py:387, 431` | "or None if root is not a git repository" / "not a git repository (or git is not available)" | Preventive measure | low | Any `checkout-index` failure returns None (`:392-393`), so a different cause would get a misleading message (H-3). | Deductive | 75 | "or None if the index cannot be checked out (not a repository, git missing, or git failed)", and include git's stderr in the error, masked. |
| D-4 | `scripts/check.py:462` | `return  # check 1 already reports it` | Preventive measure | low | True for unreadable or invalid JSON and for a non-dict top level. For `"evals": null` or `"evals": 5`, check 1 reports it, but check 6 then crashes at `:463` before returning (C-5). The comment gives false assurance. | Deductive | 85 | Fixed by the C-5 guard. Then the comment is true. |

Doc claims that fail because the **code** is wrong are counted once, in Domain 1: D3 → C-1; D5 → C-2 (and C-10 for "accents"); D10 → C-3, C-6; D12 (the "Not caught" list omits multi-character joins and stroke letters) → C-2, C-10; D21 → C-4. Each will be true once its Code fix is applied, except D12, which needs C-10's list if C-10 is not fixed.

## STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|
| DS-1 | Time Travel | D15, the facts description | yes | 82 | A reader in 6 months can rebuild the rule exactly from `:34-38` plus the constants `:76-78`. |
| DS-2 | Requirement Inversion | D16, "read as it is on disk, tracked or not" | yes | 80 | If the user wanted only tracked references, the docstring states the rationale ("copying the skill's folder ships every file in it", `:43-44`), so the choice is deliberate and visible. |
| DS-3 | Scale Shift | D11, "Without terms the check says so" | **no** | 82 | At zero staged files the message is not emitted (C-12). |

## HYPOTHESES (Abductive)
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| DH-1 | The docstring and README describe I1-I3 exactly as the tests do, and the code diverges. | The doc is the intended spec, and the code is what drifted. | The code is intended and doc and tests are aspirational. Unlikely, since the comment `:399` inside the code also states the intended behavior. | Version history (not available) or the author. |

## HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| DHB-1 | `scripts/check.py:418` | `--help` shows the description | Only line 1 of the docstring is shown. The seven rules and "Not caught" are not visible through `--help`, only by reading the file. | — (low; README.md:244-263 compensates) | 88 |

## ADVERSARIAL SCAFFOLD FINDINGS
- Reviewer blind spots: the docstring is careful and detailed, which invites trusting it over the code. Three of its strongest promises are not kept.
- Highest-risk claims: D10, D5, D21.
- Multi-step traces: docstring `:22-23` → README `:250` repeats it → users rely on masked CI logs → C-3 leaks.
- Subtlety flags: "or" in `:13-14` (precedence hidden), "if git is not available" in `:46`.

---

## CROSS-DOMAIN SUMMARY
- Domains: Code, Documentation
- Claims: 34 verified PASS (22 Code, 12 Doc). 18 in FAIL (14 Code, 4 Doc). 4 falsified (FH-1, FH-2, FH-3 conditionally, DF-1).
- Survived: 6/10 stress tests passed (S-1, S-5, S-6, S-7, DS-1, DS-2). Not survived: S-2, S-3, S-4, DS-3.
- Failure categories: 5 systemic patterns in Code (missing completeness, silent fallthrough, assumed environment, implicit ordering, stale comments/tests) and 3 in Documentation (API drift, misleading comments, missing docs).
- Invariants: 8 found, 8 touched. 4 are enforced by a mechanism in `check.py` that bites (I5-I8). I1-I3 have tests that would bite but code that breaks them, and nothing runs those tests at commit. I4 has no mechanism in `check.py`.
- Hypotheses: 6 requiring further investigation (H-1 to H-5, DH-1)
- Hidden behaviors: 8 detected (4 are problems: HB-1, HB-2, HB-3, HB-4)
- Findings by type: 6 demonstrated defects (C-1, C-2, C-3, C-5, C-13, D-1). 12 preventive measures (C-4, C-6, C-7, C-8, C-9, C-10, C-11, C-12, C-14, D-2, D-3, D-4). 4 falsified hypotheses (1 of them conditionally).
- Critical issues: 0 demonstrated defects of critical severity. There are 2 of **high** severity (C-2, C-3), both privacy leaks. Preventive measures of critical severity: 0. Of high severity: 1 (C-4).
- Pre-code: not applicable (no work proposed)
- Executed: 0 tests run (reasoning only)
- Proposed: 7 checks and 7 writes awaiting an answer
- Recommendation: **do not trust the private-terms guarantee of this script as it stands.** Three one-line fixes (C-1 `:223`, C-2 `:90`, C-3 `:400`) restore the behavior that the docstring, README and tests already specify. C-4 and C-5/C-6 close the remaining paths by which a private term or the whole list can escape. The rest are low-severity robustness items. Until H-1 is run, treat the current `scripts/test_check.py` suite as probably red on three tests.

## PROPOSED EXECUTABLE CHECKS
| # | Claim | Confidence now | Check (command, test or query) | Confirms if | Refutes if | Cost and side effects | Status |
|---|-------|----------------|--------------------------------|-------------|------------|-----------------------|--------|
| 1 | H-1: C-1, C-2, C-3 make three existing tests red | 79 (run-only) | From `tree/`: `python -I -m unittest scripts.test_check.VersionTest.test_second_badge_mismatch scripts.test_check.PrivateTest.test_two_words_joined_any_way scripts.test_check.PrivateTest.test_whole_word_term_glued_in_output_is_still_masked -v` | All three fail: the first on the exit code, the second on the two-space subtest, the third on "message hidden" and leak. | Any passes, which means a test-environment artifact or my trace is wrong. | Runs `check.py` in subprocesses on temporary copies of the repo (`tempfile.mkdtemp`). Reads the repo and writes only to the system temp dir. A few seconds. | proposed |
| 2 | The whole suite's state, beyond the three tests | — | `python -I -m unittest scripts/test_check.py -v` from `tree/` | Only the tests of check 1 fail (plus Windows-only `\r\n` subtest, symlink test if not privileged) | Other failures appear | About 80 tests, each copying the repo into the temp dir. `StagedTest`/`test_staged_content_is_what_is_checked` run `git init/commit` in temp copies, and `FactsTest` runners need `rustc` and `node` ≥ 22.6. Optional: point `TMPDIR`/`TEMP` at a memory-backed filesystem (tmpfs, RAM disk) to spare the disk the many copies. Creating one needs separate consent and about 2× the repo size in free memory. | proposed |
| 3 | C-11: an empty env var shadows the terms file | 85 | In a temp copy of `tree/` containing `.check-private-terms` with a term that occurs in SKILL.md: `CHECK_PRIVATE_TERMS= python -I scripts/check.py --root <copy>` | Exit 0 and "no private terms configured" | ERROR on the term | Reads; writes one file in a temp copy. | proposed |
| 4 | C-5/C-6: missing README crashes, and the traceback is unmasked | 88 / 80 | In a temp copy whose path contains a test term T: delete `README.md`, run `python -I scripts/check.py --root <copy>` with `CHECK_PRIVATE_TERMS=T` | Traceback, no "checked (" line, T visible in stderr | ERROR line and summary | Writes to a temp copy only. | proposed |
| 5 | H-2: `--staged` on Windows | 50 | In a temp git copy on Windows: `py -3 scripts/check.py --staged --root <copy>` | Summary "checked (staged content)" | "not a git repository" | Creates a temp repo. | proposed |
| 6 | H-3 / D-3: misleading message during a merge conflict | 50 | Create a conflicted merge in a temp git copy and run `--staged` | "not a git repository" printed | Checks run or a precise error | Temp repo only. | proposed |
| 7 | Mutation probe on the guarantees of check 3 | — | 3-5 hand mutations in a separate copy (not the working copy) on `:265`, `:275`, `:319`, `:322`, `:404-412`, each followed by `python -I -m unittest scripts.test_check.PrivateTest` | Survivors show privacy logic no test protects | All mutants killed | Writes mutated copies of `check.py` in a temp copy, restored and removed at the end. About 5 runs of `PrivateTest` (~30 tests each). The memory-backed filesystem suggestion of check 2 applies. | proposed |

Proposed writes (each needs its own approval; none was made):
1. `scripts/check.py:223`: `for b in badges:` (C-1).
2. `scripts/check.py:90`: `SEP = r"[\W_]*"` (C-2).
3. `scripts/check.py:400`: `pats = term_patterns(terms, substring=True)` (C-3).
4. `scripts/check.py:301-302`: report a tracked `.check-private-terms` as an ERROR when the file list came from git. New test in `scripts/test_check.py`: `git add -f .check-private-terms`, then `--staged` must fail with a masked message (C-4).
5. `scripts/check.py`: catch `OSError` on every required `read_text`, guard `evals` type at `:460-463`, and add a last-resort handler that prints only masked text (C-5, C-6). New tests: a staged deletion of README fails with an ERROR and a summary, and `"evals": null` does not crash.
6. `scripts/check.py:13-15, 46-47, 387, 431`: docstring and message corrections (D-1, D-2, D-3). Add stroke letters to "Not caught" unless C-10 is fixed.
7. Step 5, project discovery: `CHANGELOG.md` "## Unreleased" (`CHANGELOG.md:5`) would gain one line for fixes 1-5, since `README.md:249-250` documents these guarantees. Searched for `TODO.md`, `SPEC.md`, `PLAN.md`, `ADR/`, `.claude/`, `AGENTS.md`: none present in the `./tree` file list.

**Which of the proposed checks (1-7) may I run, and which of the proposed writes (1-7) may I make?**
