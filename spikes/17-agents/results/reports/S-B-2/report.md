# Adversarial verification: scripts/check.py

## INTAKE

- **Target:** every domain detected in `scripts/check.py`: **Code** (the logic of the 7 checks), **Data** (the file formats and contracts the script reads and enforces: evals.json, version fields, private-terms list, facts/ and NOT_COMPUTABLE, encodings), **Documentation** (module docstring, comments, help texts, messages), **UX** (terminal output of a command-line tool: messages, locations, summary, `--help`). The request asked for "every domain the skill detects".
- **Depth:** standard (stated). **Scope:** the whole of `scripts/check.py`. There is no diff and no history (stated). **Execution mode:** reasoning only. Nothing was run (stated).
- **How it was done:** one domain agent per domain (the file is about 25 kB, under the 60 kB split threshold). An independent verifier then re-checked the 5 highest-risk claims, and a category agent swept the file for the 6 failure categories found. Domain agents returned only DECOMPOSED CLAIMS, PASS, FAIL, HYPOTHESES, HIDDEN BEHAVIORS and FAILURE CATEGORIES (protocol). INVARIANTS, GROUND TRUTH tables and STRESS TEST RESULTS were not requested and are not reported.
- **Rows:** **385 rows came back** (Documentation 96, Code 75, Data 70, UX 50, independent verifier 10, category agent 84). **0 discarded.** Every quote was looked up at the line its row names. **The independent verifier confirmed 5 of 5 claims and changed none.** No PASS was lowered to 79: every quote was looked up.
- To change a setting (domain, depth, run the proposed checks), say so. The checks at the end are only proposed.

Ground truth the agents used, all inside `./tree`: `scripts/check.py` itself, `scripts/test_check.py`, `scripts/check_facts.py`, `scripts/pre-commit`, `README.md`, `CHANGELOG.md`, `.gitignore`, `.claude-plugin/plugin.json`, `skills/adversarial-verify/SKILL.md`, `skills/adversarial-verify/evals/evals.json`, `skills/adversarial-verify/evals/facts/*`.

---

## VERIFICATION DOMAIN: Code

### DECOMPOSED CLAIMS (Code)
1. Exit code is 1 if and only if there is an error (scripts/check.py:4, :442). Deductive
2. Invalid JSON, extra or missing eval keys, non-integer/bool ids, duplicates and gaps are errors (scripts/check.py:6-9, :163-207). Deductive
3. Default term patterns match as substrings; `=` terms match only as whole words (scripts/check.py:18-19, :275). Deductive
4. Term parts may be joined by any non-alphanumeric separator, line breaks included (scripts/check.py:16-17, :90). Deductive
5. No configured term ever reaches the output (scripts/check.py:22-23, :397-414). Deductive
6. Every README skill badge is compared with the SKILL.md version (scripts/check.py:10, :223). Deductive
7. Table rows and delimiters have the header's cell count; fenced blocks are skipped (scripts/check.py:30-33, :341-381). Deductive
8. Each fact file is bound to an existing eval and to the sha256 of its prompt (scripts/check.py:36-38, :457-501). Deductive
9. check_facts tolerates malformed evals and leaves the reporting to check 1 (scripts/check.py:462). Deductive
10. A missing or unreadable required file is reported as an ERROR, with the summary printed (scripts/check.py:214). Deductive
11. Terms come from the working repo also with --staged; the temp copy is always removed (scripts/check.py:423, :438-440). Deductive
12. With --staged, exactly the staged content is checked (scripts/check.py:47, :386-394). Deductive
13. Python 3.8 is enough (scripts/check.py:50). Deductive, run-only

### FAILURE CATEGORIES IDENTIFIED (Code)
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Missing completeness (matcher narrower than the documented rule) | scripts/check.py:90 `SEP = r"[\W_]?"  # anything that is not a letter or digit, possibly nothing`; scripts/check.py:400 `pats = term_patterns(terms)`; scripts/check.py:223 `for b in badges[:1]:`; scripts/check.py:366 `fence = None`; scripts/check.py:345 (double-backtick spans) | scripts/check.py |
| Silent fallthrough | scripts/check.py:473 `with_file[int(stem)] = name`; scripts/check.py:436 `if files or not args.staged:`; scripts/check.py:341 `DELIM` (`-{3,}`); scripts/check.py:151-152 `except (OSError, subprocess.CalledProcessError):` / `pass` | scripts/check.py |
| Missing checks for absent or malformed values (crash instead of an ERROR line) | scripts/check.py:214, :217, :228, :237, :332, :356, :463, :476, :486, :512, :252-254 | scripts/check.py |
| Implicit ordering | scripts/check.py:462 `return  # check 1 already reports it`; scripts/check.py:445-452 (a crash in a later check loses the earlier checks' errors) | scripts/check.py |
| Assumed environment | scripts/check.py:90 (CRLF = two separators); scripts/check.py:389 `"--prefix=" + tmp + os.sep` (eol filters, Windows prefix) | scripts/check.py |

### VERIFICATION RESULTS (Code)

#### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| 1 | Exit code reflects errors only | scripts/check.py:442 `return 1 if rep.errors else 0`; warnings go to `rep.warnings` (:108-109); :531 `sys.exit(main())`. Confidence 95 |
| 2 | Exact key set and integer, unique, consecutive ids | scripts/check.py:180 `extra, missing = sorted(set(e) - EVAL_KEYS), sorted(EVAL_KEYS - set(e))`; :186 `if type(i) is not int:  # bool is an int subclass: reject it`; :203-207. Confidence 92 |
| 3 | Tags from eval 21 followed by text | scripts/check.py:201 `elif i >= TAGGED_FROM and not TAG_RE.match(a):` with :75 `^\[(substance\|format)\]\s+\S`. Confidence 90 |
| 4 | Version read only from the frontmatter; plugin.json and the newest CHANGELOG entry compared | scripts/check.py:215 `fm = re.match(r"\A---\n(.*?)\n---\n", skill.replace("\r\n", "\n"), re.S)`; :237 skips CHANGELOG.md:5 `## Unreleased` and takes CHANGELOG.md:10 `## 4.2 - 2026-11-25`. Confidence 88 |
| 5 | Substring by default, whole word with `=` (detection side) | scripts/check.py:275 `pats.append(re.compile(rf"(?<![^\W_]){body}(?![^\W_])" if whole_word else body))`. Confidence 90 |
| 6 | Short-term warning; no-letter term error; decoded JSON strings scanned | scripts/check.py:271 `if rep is not None and sum(len(p) for p in parts) < 4:`; :267-270; :313-323. Confidence 90 |
| 7 | No terms: warning, --strict: error (working-tree mode) | scripts/check.py:297 `(rep.error if strict else rep.warning)("private terms", msg)`. Confidence 92 |
| 8 | Neutral wording checked on SKILL, references and README only, as warnings | scripts/check.py:142 `return [SKILL] + reference_files(root) + [README]`; :336 `rep.warning`. Confidence 92 |
| 9 | Reference names exist and every reference file is named in SKILL.md (working-tree mode) | scripts/check.py:519 `for name in sorted(existing - named_in_skill):`; :511-518. Confidence 92 |
| 10 | Terms from the working repo with --staged; temp copy removed | scripts/check.py:423 `terms = load_terms(args.root)  # always from the working repo: the list is never committed` runs before :433 `root = tmp`; :439 `if tmp:` inside `finally`. Confidence 92 |
| 11 | Fact files: orphan, missing or stale hash, "not both", "neither" (apart from FAIL C5) | scripts/check.py:478 `want = hashlib.sha256(prompts[i].encode("utf-8")).hexdigest()`; :470-471, :479-482, :495-501. Confidence 88 |
| 12 | Python 3.8 (no newer API found by reading) | scripts/check.py:53-531: `capture_output` (3.7), f-strings, `yield from`, `casefold`; no `removeprefix`, dict `\|` or `match`. Only a run settles it. Confidence 79 (Code agent said 85, Documentation agent 75 with the run-only cap; the lower one is kept below 80 because the claim is run-only) |

#### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| C1 | scripts/check.py:90 | `SEP = r"[\W_]?"  # anything that is not a letter or digit, possibly nothing` | Demonstrated defect | high | `?` allows at most one separator. The term `John Smith` becomes `john[\W_]?smith`, which misses `John  Smith` (two spaces), `John - Smith`, `John, Smith` and the CRLF break `John\r\nSmith` (read_text, :120, keeps `\r\n`). A private name ships through the check meant to stop it. Contradicts scripts/check.py:16-17. scripts/test_check.py:286 `for variant in (f"{a}-{b}", f"{a}_{b}", f"{a}{b}", f"{a}\n{b}", f"{a.upper()}  {b}"):` expects the two-space form to be caught. Found by Code, Data, Documentation, UX (masking side) and the category agent; **the independent verifier confirmed it (FAIL, 90)** | Deductive | 90 | `SEP = r"[\W_]*"` |
| C2 | scripts/check.py:400 | `pats = term_patterns(terms)` | Demonstrated defect | high | :399 says masking uses substring patterns, but `substring` defaults to False (:259), so `=` terms keep whole-word lookarounds. With the term `=acme` and an eval key `acmelabs`, :182 prints `unexpected keys ['acmelabs']` unmasked, and the private term reaches the console and the hook log. Contradicts scripts/check.py:22-23. scripts/test_check.py:344 `self.assert_fails(self.run_check(terms="=" + T1), "message hidden")` expects the opposite. Found by all 4 domain agents and the category agent; **the independent verifier confirmed it (FAIL, 85)** | Deductive | 90 | `pats = term_patterns(terms, substring=True)` |
| C3 | scripts/check.py:223 | `for b in badges[:1]:` | Demonstrated defect | medium | :217 collects every badge, but only the first is compared. A README with `skill-v4.2` and a stale `skill-v2.0` badge passes. Contradicts scripts/check.py:10. scripts/test_check.py:172 `self.append("README.md", "![old](https://img.shields.io/badge/skill-v2.0-blue)")` (test_second_badge_mismatch, :171) expects "version mismatch". Found by Code, Data, Documentation and the category agent; **the independent verifier confirmed it (FAIL, 95)**. Data rated it high, the others medium | Deductive | 92 | `for b in badges:` |
| C4 | scripts/check.py:228 | `except ValueError as e:` | Demonstrated defect | medium | A missing SKILL.md (:214), README.md (:217), plugin.json (:227, only ValueError caught) or CHANGELOG.md (:237), or an unreadable file read in :332, :356 or :512, raises an uncaught OSError. There is no ERROR line, `print_report` (:441) never runs, and every error already collected is lost. The traceback also bypasses `mask()`. This happens when a staged commit deletes or renames one of them, or when `--root` is wrong. check_evals catches OSError (:167), so the handling is inconsistent. Found by Code, Data, UX and the category agent (3.1-3.7) | Deductive | 85 | Catch OSError for each read and report `rep.error(path, "missing or unreadable")` |
| C5 | scripts/check.py:473 | `with_file[int(stem)] = name` | Demonstrated defect | medium | `35.py` and `35.rs` (or `35.py` and `035.py`) both map to id 35. Only the later one gets its prompt-sha256 checked, but scripts/check_facts.py still runs both, so a stale fact file is run and trusted. No duplicate exists today. Found by Code, Data and the category agent; the Documentation agent typed it as a preventive measure | Deductive | 88 | Collect the files per id; error when an id has more than one, or when `stem != str(int(stem))` |
| C6 | scripts/check.py:463 | `ids = {e.get("id") for e in evals if isinstance(e, dict)}` | Demonstrated defect | low | With `"evals": null`, :460 yields None and iterating it raises TypeError. With `"id": [1]`, the set raises "unhashable type". Either way the run crashes before `print_report`, so check 1's error is never printed. With `"evals": "text"`, every fact file is reported as an orphan (category 5.3). Found by Code, Data, Documentation and the category agent | Deductive | 88 | `if not isinstance(evals, list): return`; keep only ids with `type(id) is int` |
| C7 | scripts/check.py:366 | `fence = None` | Preventive measure | low | Any fence line closes the open fence. The opening character stored at :364 is never compared, and neither is the length. A ```` block that shows ``` or `~~~` closes early, so example rows are checked (false errors) and later real tables are skipped. This becomes a defect when a doc nests fences | Deductive | 85 | Close only on the same character with at least the opening length |
| C8 | scripts/check.py:341 | `DELIM = re.compile(r"^\s*\\|?\s*:?-{3,}:?\s*(\\|\s*:?-{3,}:?\s*)*\\|?\s*$")` (pipes escaped for this table) | Preventive measure | low | GFM accepts delimiter cells of one or two dashes. Such a table is not recognized, and its rows go unchecked without a message. Today's docs use `---` | Deductive | 80 | `-+` instead of `-{3,}` |
| C9 | scripts/check.py:436 | `if files or not args.staged:` | Preventive measure | low | With --staged and an empty index, no check runs, not even the --strict no-terms error (:297). The exit code is 0 and the summary lists no checks. Found by all 4 domain agents and the category agent (2.5, 6.2) | Deductive | 80 | Run the no-terms check anyway, or report "nothing staged to check" |
| C10 | scripts/check.py:301 | `if os.path.basename(rel) == TERMS_FILE:` | Preventive measure | high | Any file named `.check-private-terms`, at any depth and tracked or not, is skipped. A force-added or nested copy commits the whole private list while check 3 passes. Only .gitignore keeps it out. Found by Code, Data, Documentation and the category agent (2.2, 1.7). The category agent typed it as a demonstrated defect; it is kept as preventive because no tracked copy exists | Deductive | 80 | Make a tracked (or staged) file with that basename an ERROR |
| C11 | scripts/check.py:345 | ``s = re.sub(r"`[^`]*`", "x", line).replace("\\|", "x").strip()`` | Demonstrated defect | low | Only single-backtick code spans are recognized. In ``` ``a|b`` ``` the regex takes two empty spans and leaves `a|b`, so the pipe is counted. There is also the opposite case (category 4.9): in GFM an unescaped pipe inside a code span still splits the cell, so the check passes a row that renders broken. Category agent only | Deductive | 85 | Match code spans of any backtick length, and treat unescaped pipes in code spans as GFM does |
| C12 | scripts/check.py:151-152 | `except (OSError, subprocess.CalledProcessError):` / `pass` | Demonstrated defect | medium | When git fails (not installed, `safe.directory` refusal, nothing tracked), the script silently walks every file on disk, including `.venv`, `node_modules` and ignored files (:154-157). The summary still says "working tree". Category agent only (2.12, 4.5, 4.13, 6.5) | Deductive | 75 | Say in the output which file set was used; skip ignored files in the fallback |
| C13 | scripts/check.py:252-254 | `if not os.path.exists(path):` ... `with open(path, "rb") as f:` | Demonstrated defect | medium | If `.check-private-terms` is a folder or unreadable, `open` raises before `Report` exists, and the run crashes with a traceback. Category agent only | Deductive | 90 | Use `os.path.isfile` and catch OSError with a clear message |
| C14 | scripts/check.py:67 | `REF_RE = re.compile(r"references/([A-Za-z0-9_.-]+\.md)\b")` | Preventive measure | low | A reference name with a space, a non-ASCII letter or a subfolder is not recognized, so a broken link to it is never reported. Category agent only | Deductive | 85 | Widen the character class, or report unrecognized `references/` mentions |
| C15 | scripts/check.py:218-241 | `elif m and pv != m.group(1):` | Demonstrated defect | low | Every comparison goes through SKILL.md's version. Without it, mismatches between README, plugin.json and CHANGELOG are not reported until SKILL.md is fixed. Category agent only (5.7) | Deductive | 88 | Compare the other three with each other when the frontmatter has no version |

### HYPOTHESES (Code)
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| 1 | scripts/check.py:389 `subprocess.run(["git", "-C", root, "checkout-index", "-a", "--prefix=" + tmp + os.sep],` | checkout-index applies `core.autocrlf` and smudge filters, so --staged does not check "exactly the content staged" (:47), and together with C1 the CRLF case is missed at commit time. Skip-worktree entries are listed but not written (category 4.6, 6.6) | Git writes the blobs unchanged under this repo's config | In a repo with `core.autocrlf=true`, stage `a\nb`, run `--staged` and inspect the bytes in tmp |
| 2 | scripts/check.py:389 `"--prefix=" + tmp + os.sep` | On Windows, the backslash prefix makes git fail or write elsewhere | Git for Windows accepts it | Run `py -3 scripts/check.py --staged` on Windows and list tmp |
| 3 | scripts/check.py:216 `m = re.search(r'^\s*version:\s*"?([0-9][0-9.]*)"?\s*$', fm.group(1), re.M) if fm else None` | The first `version:` key at any indentation wins | Only one exists today (skills/adversarial-verify/SKILL.md:20 `version: "4.2"`) | Add a nested `version:` above `metadata:` |
| 4 | scripts/check.py:309 `rep.error(rel, "unreadable file, not checked")` | A tracked file deleted from the working tree, or a submodule gitlink, blocks every run without --staged | Expected by the user | Delete a tracked file without `git rm` and run |
| 5 | scripts/check.py:441 `print_report(rep, terms, args.staged)` | Tracebacks from C4/C6/C13 bypass masking and may print a path containing a term (category 1.5) | No traceback path with a term was traced | Plant a directory `<term>.md` in references/ and run |

### HIDDEN BEHAVIORS DETECTED (Code)
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| 1 | scripts/check.py:364 `fence = f.group(1)[0]` | Fenced code blocks are skipped (:33) | The fence character is stored but never used when closing | Preventive measure (C7) | 85 |
| 2 | scripts/check.py:369 `if fence is None and i > 0 and DELIM.match(lines[i]) and "\|" in lines[i] + lines[i - 1]:` | Only Markdown tables are checked | A setext `---` underline under a line with a pipe is read as a table delimiter | Preventive measure, low | 80 |
| 3 | scripts/check.py:186-188 `rep.error(where, "id is not an integer")` / `continue` | Each eval's fields are checked | An eval with a non-integer id gets no other field check | none (an error is already reported) | 85 |
| 4 | scripts/check.py:458-462 `rep.checked.append("eval facts")` ... `return  # check 1 already reports it` | The summary lists the checks done | "eval facts" is listed even when it returned early; the same for "private terms" without terms (:293) | Demonstrated defect, low (category 2.6) | 85 |

---

## VERIFICATION DOMAIN: Data

### DECOMPOSED CLAIMS (Data)
1. Terms come from CHECK_PRIVATE_TERMS or the untracked .check-private-terms (one per line, # for comments) (scripts/check.py:13-15, :246-256). Deductive
2. Matching ignores case, accents and Unicode forms, also in files that are not UTF-8 (scripts/check.py:15, :21-22, :93-122). Deductive
3. JSON strings are scanned after their escapes are decoded (scripts/check.py:20-21, :313-323). Deductive
4. NOT_COMPUTABLE lines have the form "<id>: <reason>"; a fact file and a reason for one eval are an error (scripts/check.py:36, :483-496). Deductive
5. Every eval from FACTS_FROM (29) that states facts has a fact file or a reason (scripts/check.py:34-36, :497-501). Inductive
6. The current tree keeps the four version fields equal (scripts/check.py:212). Deductive
7. The newest "## <version>" CHANGELOG entry is the one compared (scripts/check.py:11-12, :237). Deductive

### FAILURE CATEGORIES IDENTIFIED (Data)
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Missing completeness (a contract only partly enforced) | scripts/check.py:122 `return data.decode("latin-1"), "latin-1"`; scripts/check.py:94-95 (letters with no NFKD decomposition); scripts/check.py:255 (inline comments); scripts/check.py:313-317 (JSONC, `.JSON`); scripts/check.py:500 `"(Facts"` | scripts/check.py |
| Silent fallthrough | scripts/check.py:494 `reasons[int(m.group(1))] = m.group(2)`; scripts/check.py:248 `if raw is not None:`; scripts/check.py:166 (duplicate JSON keys); scripts/check.py:469 (other extensions ignored) | scripts/check.py |
| Assumed environment (encodings, file names) | scripts/check.py:114 `if data.startswith((b"\xff\xfe", b"\xfe\xff")):`; scripts/check.py:470 `if not stem.isdigit() or int(stem) not in ids:`; scripts/check.py:215 (CR-only line ends) | scripts/check.py |
| Implicit ordering | scripts/check.py:474, :478 (duplicate ids hash the wrong prompt); scripts/check.py:463, :470 (`True == 1`) | scripts/check.py |

### VERIFICATION RESULTS (Data)

#### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| 1 | Terms file format: BOM removed, comment lines and blanks dropped (whole-line comments only, see FAIL D3) | scripts/check.py:255 `terms = [l for l in decode(f.read())[0].splitlines() if not l.strip().startswith("#")]`; :256 `return [t.strip() for t in terms if t.strip()]`. Confidence 88 |
| 2 | Decoded JSON strings are scanned for strict-JSON `.json` files | scripts/check.py:315 `strings = [normalize(x) for x in json_strings(json.loads(text))]`; :322. Confidence 88 |
| 3 | NOT_COMPUTABLE format and the "not both" rule | scripts/check.py:490 `m = re.match(r"^(\d+):\s*(\S.*)?$", line)`; :491 rejects `77:`; :495 `for i in sorted(set(reasons) & set(with_file)):`. Confidence 88 |
| 4 | The current tree keeps the versions equal | skills/adversarial-verify/SKILL.md:20 `version: "4.2"`; README.md:1 `badge/skill-v4.2-blue`; .claude-plugin/plugin.json:3 `"version": "4.2",`; CHANGELOG.md:10 `## 4.2 - 2026-11-25`, read through scripts/check.py:212 `def check_version(root, rep):`. Confidence 90 |
| 5 | Coverage of fact-stating evals in the current tree (21 instances, each with exactly one of fact file or reason) | scripts/check.py:500 `if "(Facts" in str(e.get("prompt", "")) and e["id"] not in with_file and e["id"] not in reasons:`. Inductive, Confidence 75 (pattern) |
| 6 | plugin.json version must be a string equal to SKILL.md's | scripts/check.py:233 `if not isinstance(pv, str):`; :235 `elif m and pv != m.group(1):`. Confidence 90 |

#### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| D1 | scripts/check.py:122 | `return data.decode("latin-1"), "latin-1"` | Demonstrated defect | medium | One invalid byte switches the whole file to Latin-1. A UTF-8 `José` (`4A 6F 73 C3 A9`) becomes `JosÃ©`, which normalizes to `josa©`, so the term `jose` is missed. Also, a cp1252 `Š` (0x8A) is decoded as a control character, and a cp1250 `ł` (0xB3) becomes `³` and then `3`. Contradicts scripts/check.py:15 and :21-22, and is absent from the "Not caught" list (:24-26). Found by Data; **the independent verifier confirmed it (FAIL, 85) and added the cp1252 and cp1250 cases**; category agent 4.2 adds cp1251, Shift-JIS and GBK | Deductive | 85 | Decode UTF-8 with `errors="surrogateescape"`, or scan both decodings; list the remaining cases under "Not caught" |
| D2 | scripts/check.py:94-95 | `text = unicodedata.normalize("NFKD", text)` / `if not unicodedata.combining(c)` | Demonstrated defect | medium | Letters whose diacritic is not a combining mark (ł, ø, đ, æ, ħ) have no NFKD decomposition. With the term `Lodz`, the text `Łódź` normalizes to `łodz` and is not matched. Contradicts "ignores ... accents" (:15). Category agent only | Deductive | 85 | Add a fold table for those letters, or list them under "Not caught" |
| D3 | scripts/check.py:255 | `terms = [l for l in decode(f.read())[0].splitlines() if not l.strip().startswith("#")]` | Demonstrated defect | high | Only whole-line comments are removed. The line `acme  # client` becomes a term with parts acme/client, so `acme` alone is no longer checked, and nothing reports it. Category agent only (1.6, 2.4) | Deductive | 90 | Strip ` #...` trailing comments, or reject lines that contain `#` after a term |
| D4 | scripts/check.py:248 | `if raw is not None:` | Preventive measure | medium | A set but empty `CHECK_PRIVATE_TERMS` (an inherited CI export) disables the existing terms file. Without --strict the run passes with no scan, and the message tells the user to create a file that already exists. With a partial env list, the file's other terms are silently skipped. Found by Code, Data, Documentation, UX and the category agent (2.14, 6.1, rated high there). Severities differ; medium is kept because the user must set the variable | Deductive | 85 | `if raw and raw.strip():`, or name the env variable as the cause in the message |
| D5 | scripts/check.py:494 | `reasons[int(m.group(1))] = m.group(2)` | Preventive measure | low | A NOT_COMPUTABLE reason for an id that does not exist, is below FACTS_FROM or has no "(Facts", or a duplicate id, is accepted silently (last one wins). Stale reasons pile up. Found by Code, Data, Documentation and the category agent | Deductive | 82 | Error for unknown and duplicate ids |
| D6 | scripts/check.py:500 | `if "(Facts" in str(e.get("prompt", "")) and e["id"] not in with_file and e["id"] not in reasons:` | Preventive measure | low | The trigger is the literal, case-sensitive "(Facts". A prompt that states facts as "Facts:" or "(facts" escapes the requirement. All 21 current instances use "(Facts". Found by Data and the category agent | Inductive | 70 | `re.search(r"\(\s*facts?\b", prompt, re.I)` |
| D7 | scripts/check.py:114 | `if data.startswith((b"\xff\xfe", b"\xfe\xff")):` | Preventive measure | low | A UTF-32-LE file (`FF FE 00 00`) is decoded as UTF-16 with NULs between the letters, so its terms are missed. The "Not caught" list names only UTF-16 without a BOM. Found by Data and the category agent; a hypothesis for Code | Deductive | 80 | Test the UTF-32 BOMs first |
| D8 | scripts/check.py:470 | `if not stem.isdigit() or int(stem) not in ids:` | Preventive measure | low | `str.isdigit()` accepts `²`, which `int()` rejects, so a file `².py` crashes the run. Found by Data and the category agent (3.9, typed there as a demonstrated defect) | Deductive | 80 | `re.fullmatch(r"[0-9]+", stem)` |
| D9 | scripts/check.py:313-317 | `if rel.endswith(".json"):` ... `except ValueError: pass` | Demonstrated defect | medium | Escapes are decoded only in files that parse as strict JSON and end in lowercase `.json`. JSONC (comments, trailing commas), `.JSON`, `.jsonl` and `.ipynb` are skipped silently, so a `\u`-escaped term in them is missed. Contradicts scripts/check.py:20-21. Category agent only (1.8, 2.3) | Deductive | 88 | Case-insensitive extension list; on a parse failure, decode `\uXXXX` escapes with a regex |
| D10 | scripts/check.py:166 | `data = json.loads(read_text(root, EVALS, rep))` | Demonstrated defect | medium | `json.loads` keeps the last of duplicate keys. An eval with two `"prompt"` keys, or two `"evals"` arrays, is accepted and the earlier value dropped without a report. Category agent only | Deductive | 88 | `object_pairs_hook` that errors on duplicate keys |
| D11 | scripts/check.py:477-480 | `m = re.search(r"prompt-sha256:\s*([0-9a-f]{64})", head)` | Demonstrated defect | low | An upper-case hex hash, or a hash line after the first 2000 characters (:476), is reported as "no 'prompt-sha256:' line". Category agent only | Deductive | 88 | Accept `[0-9a-fA-F]`; say "hash not found in the first 2000 characters" |
| D12 | scripts/check.py:237 | `first = re.search(r"^## +([0-9][0-9.]*)\b", read_text(root, CHANGELOG, rep), re.M)` | Preventive measure | low | `## [4.3] - date` (Keep a Changelog) or `## v4.3` never match. When such a heading is on top, an older plain `## 4.2` is compared instead. Category agent only | Deductive | 80 | Accept an optional `[` and `v` |
| D13 | scripts/check.py:215 | `fm = re.match(r"\A---\n(.*?)\n---\n", skill.replace("\r\n", "\n"), re.S)` | Demonstrated defect | low | With CR-only line ends, or a SKILL.md that ends right after the closing `---` with no newline, the result is "no version in the frontmatter" although the version is there. Category agent only | Deductive | 88 | Normalize `\r`, and accept `\n---(\n\|\Z)` |
| D14 | scripts/check.py:474 | `prompts = {e.get("id"): str(e.get("prompt", "")) for e in evals if isinstance(e, dict)}` | Demonstrated defect | low | With duplicate ids, the last prompt wins and a fact file is hashed against the wrong eval (false "changed" or false pass). Also `True == 1` (:463, :470). The run relies on check 1 reporting duplicates and bools. Category agent only | Deductive | 85 | Skip check 6 for ids check 1 rejected |

### HYPOTHESES (Data)
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| 1 | scripts/check.py:478 `want = hashlib.sha256(prompts[i].encode("utf-8")).hexdigest()`; skills/adversarial-verify/evals/facts/35.py:1 `# prompt-sha256: a502f0639b93c074fd20190e3f58c7c630fa1d91a21742e31cdb07b968e7823b` | Every stored hash equals the sha256 of the current decoded prompt | A prompt was edited after its facts were checked | Run `python3 -I scripts/check.py` on the tree |
| 2 | scripts/check.py:148 `files = [f for f in out.stdout.decode("utf-8", "replace").split("\0") if f]` | A submodule gitlink is a directory, so it becomes "unreadable file, not checked" and blocks every commit | The project has no submodules | `git ls-files -s`, looking for mode 160000 entries |
| 3 | scripts/check.py:321 `body.count(chr(10), 0, m.start()) + 1` | Line numbers match the editor | U+2028, U+0085 or lone CR give other numbers (see UX F11) | A fixture with a lone-CR break before the term |

### HIDDEN BEHAVIORS DETECTED (Data)
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| 1 | scripts/check.py:128 `if enc != "utf-8" and rep is not None and (rel in (SKILL, README, EVALS) or rel.startswith(REFS_DIR + "/")):` | (not stated) | Non-UTF-8 is an error only for SKILL.md, README.md, evals.json and the reference files. plugin.json, CHANGELOG.md, fact files and NOT_COMPUTABLE pass silently | Preventive measure, low | 80 |
| 2 | scripts/check.py:469 `if ext in FACT_EXTS and not stem.startswith("_"):` | Fact files are facts/<id>.py\|.rs\|.ts | `_`-prefixed names and other extensions (`45.js`, `45.PY`) are ignored without a message, consistently with scripts/check_facts.py | none (category agent 2.9: low) | 88 |
| 3 | scripts/check.py:476 `head = read_text(root, f"{FACTS_DIR}/{name}")[:2000]` | The file "carries the sha256" | Only the first 2000 characters are searched | none (see D11 for the message) | 88 |
| 4 | scripts/check.py:75 `TAG_RE = re.compile(r"^\[(substance\|format)\]\s+\S")` | "followed by text" | Whitespace after the tag is required; `[format]text` is rejected | none | 88 |
| 5 | scripts/check.py:300 `for rel in files:` | Terms checked in "the files tracked by git" (:46) | Untracked files under skills/ are not scanned for terms, yet :44 says copying the folder ships every file | Preventive measure, low | 75 |

---

## VERIFICATION DOMAIN: Documentation

### DECOMPOSED CLAIMS (Documentation)
40 claims were decomposed from the module docstring (scripts/check.py:2-50), the comments (:74, :77, :90, :399, :423, :462), the function docstrings (:113, :260-262, :387), the help texts (:419-420) and the messages (:225, :373, :378, :431). They are all listed in out/returns/Documentation.md. The claims shared with Code and Data are counted there; the ones whose primary domain is the text are below.

### FAILURE CATEGORIES IDENTIFIED (Documentation)
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Missing completeness (text drifted from the code) | scripts/check.py:10 vs :223; :16-17 vs :90; :24-26 (incomplete "Not caught" list); :43-44 vs :433; :46 vs :464-465; :399 vs :400 | scripts/check.py; also repeated in README.md:249-250 (out of scope) |
| Mode-dependent statements | scripts/check.py:43-44 (true in working-tree mode, false with --staged); :23-24 (false with --staged and an empty index); :47 (false with eol filters, hypothesis) | scripts/check.py |

### VERIFICATION RESULTS (Documentation)

#### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| 1 | scripts/check.py:4 `Errors make the exit code non-zero; warnings are printed but do not block.` | :442 `return 1 if rep.errors else 0`. Confidence 90 |
| 2 | scripts/check.py:6-9 (evals.json rules) | :166-207. Confidence 88 |
| 3 | scripts/check.py:11-12 (plugin.json and newest CHANGELOG entry) | :232-241; CHANGELOG.md:5 `## Unreleased` skipped. Confidence 88 |
| 4 | scripts/check.py:18-19 `a term starting with = matches only as a` / `whole word` | :275. Confidence 90 |
| 5 | scripts/check.py:19-20 (short-term warning, no-letter error) | :267-273. Confidence 86 |
| 6 | scripts/check.py:27-29 `README.md are warnings (they may appear in a list of varied examples).` / `evals.json is excluded.` | :328-336, :142. Confidence 88 |
| 7 | scripts/check.py:34-36 (fact file or reason, not both) | :495-501. Confidence 86 |
| 8 | scripts/check.py:40-42 (named references exist) | :506-520. Confidence 86 |
| 9 | scripts/check.py:49 `Usage: python3 scripts/check.py [--strict] [--staged] [--root PATH]` | :419-421 define exactly these options. Confidence 92 |
| 10 | scripts/check.py:90 comment (describes one optional character, which is what the regex is; the docstring is what is wrong, C1) | Confidence 85 |
| 11 | scripts/check.py:260-262 (term_patterns docstring) | :275 lookarounds use `[^\W_]`. Confidence 88 |
| 12 | scripts/check.py:423 comment (terms from the working repo) | Loaded before :433; .gitignore lists `.check-private-terms`. Confidence 88 |
| 13 | scripts/check.py:373 / :378 (header line numbers in the table messages) | `start = i` is the header's 1-based line. Confidence 88 |
| 14 | scripts/check.py:74, :77 constant comments | Used only at :201 and :498. Confidence 85 |

#### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| T1 | scripts/check.py:43-44 | `The folder is read as it is on disk, tracked or not, since` / `copying the skill's folder ships every file in it.` | Demonstrated defect | medium | With --staged, :433 sets `root = tmp` (index only), so `reference_files` (:136) never sees an untracked, unnamed `references/orphan.md`. The pre-commit hook (scripts/pre-commit:9 `"$py" -I "$root/scripts/check.py" --strict --staged --root "$root" \|\| exit 1`) passes it. scripts/test_check.py:507 `self.assert_passes(self.run_check("--staged", terms=NONE))  # not staged: not part of the commit` shows that this is intended, so the text is what is wrong. Found by Documentation, Data and the category agent; **the independent verifier confirmed it (PASS in working-tree mode, FAIL with --staged, 85)** | Deductive | 88 | "In the working tree the folder is read as it is on disk, tracked or not; with --staged, only what is staged" |
| T2 | scripts/check.py:24-26 | `Not caught: a one-word term written as two words (space or` / `line break in the middle), UTF-16 files without a BOM; with =, also forms` / `glued to other letters or digits.` | Demonstrated defect | medium | The list leaves out multi-part terms joined by two or more separators (C1), mojibake from the Latin-1 fallback (D1), letters with no NFKD decomposition (D2), UTF-32 (D7) and JSONC (D9). A reader believes those forms are covered. README.md:250 repeats the omission | Deductive | 85 | Complete the list, or fix the code |
| T3 | scripts/check.py:462 | `return  # check 1 already reports it` | Demonstrated defect | low | The comment is false for `"evals": null` and unhashable ids, which crash the run (C6) before check 1's report is printed | Deductive | 85 | Fix C6, or correct the comment |
| T4 | scripts/check.py:46 | `Files checked: the files tracked by git (all files outside .git if git is not` | Demonstrated defect | medium | Only check 3 uses the tracked list. Checks 1, 2 and 4-7 read fixed paths and on-disk listings, so in working-tree mode an untracked fact file or NOT_COMPUTABLE edit (:464-465) passes check 6, and the commit then fails or ships without it. The fallback also applies when nothing is tracked, not only when git is missing (:149-158). Category agent 6.4 and Documentation hidden behavior 5 | Deductive | 85 | "Private terms are checked in the files tracked by git; the other checks read the files on disk" |
| T5 | scripts/check.py:387 | `"""Write the staged content into tmp; return the staged file list, or None if root is not a git repository."""` | Preventive measure | low | Any git failure (write error in tmp, `safe.directory`, unmerged entries, a path too long on Windows) returns None and is reported by :431 as "not a git repository (or git is not available)". Found by Documentation and the category agent (1.16) | Deductive | 75 | Include git's stderr in the message |
| T6 | scripts/check.py:36-38 | `every fact file belongs to` / `an existing eval and carries the sha256 of that eval's prompt` | Preventive measure | low | The text depends on C5 (only one file per id is hash-checked). It also does not say that `_`-prefixed and other-extension files are exempt | Deductive | 82 | Fix C5; mention the exemption |

The documentation side of C1 (:16-17), C2 (:22-23, :399), C3 (:10) and C9 (:23-24 with --staged) is counted once, under Code.

### HYPOTHESES (Documentation)
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| 1 | scripts/test_check.py:286, :171, :341 expect what C1, C3 and C2 contradict | The suite is red now: the code regressed after the tests, and the hook (scripts/pre-commit) does not run the tests | Some other path catches these (none was traced) | `python3 -m unittest scripts/test_check.py` |
| 2 | scripts/check.py:50 `Requires Python 3.8 or later.` | The claim holds | A stdlib behaviour differs on 3.8 | Run the tests under Python 3.8 |

---

## VERIFICATION DOMAIN: UX

### DECOMPOSED CLAIMS (UX)
1. Every problem is one line: level, location, message (scripts/check.py:106). Deductive
2. The run always ends with a summary line (scripts/check.py:527). Deductive
3. Input problems come out as ERROR lines, not as a crash (scripts/check.py:126). Deductive
4. The term number `#k` identifies the configured term (scripts/check.py:321). Deductive
5. Locations' line numbers match the editor (scripts/check.py:373). Deductive
6. Messages say what to do (scripts/check.py:482). Deductive
7. One cause gives one error (scripts/check.py:207). Deductive
8. `--help` explains the options (scripts/check.py:421). Deductive
9. Important warnings are not drowned by routine ones (scripts/check.py:336). Inductive
10. The output can be printed on every supported console (scripts/check.py:50). Abductive

### FAILURE CATEGORIES IDENTIFIED (UX)
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Implicit ordering / index coupling | scripts/check.py:264 `for k, t in enumerate(terms, 1):` vs :303 and :318 `for k, p in enumerate(pats, 1):`; :256 (numbering after comments are removed) | scripts/check.py |
| Assumed environment | scripts/check.py:527 (em dash on a non-UTF-8 console); :321 vs :332/:356/:486/:513 (two ways of counting lines) | scripts/check.py |
| Silent fallthrough (a run that checked nothing looks clean) | scripts/check.py:436; :458-462 | scripts/check.py |

### VERIFICATION RESULTS (UX)

#### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| 1 | Line format level / location / message | scripts/check.py:106 `self.errors.append(f"ERROR {where}: {msg}")`; mask() rebuilds the same shape (:413). Confidence 85 |
| 2 | No-terms message is explicit and names both sources | scripts/check.py:295-297. Confidence 90 |
| 3 | Fact hash message gives the exact value to set | scripts/check.py:482 `... re-check the facts, then set prompt-sha256: {want}")`. Confidence 90 |
| 4 | Malformed NOT_COMPUTABLE line is located and the format shown | scripts/check.py:492 `rep.error(f"{FACTS_DIR}/NOT_COMPUTABLE:{n}", "expected '<id>: <reason>'")`. Confidence 90 |
| 5 | Short-term warning gives a remedy only when it applies | scripts/check.py:272 `hint = "" if whole_word else " (prefix it with = to match whole words only)"`. Confidence 90 |
| 6 | Non-UTF-8 skill files are named with the fallback encoding | scripts/check.py:129 `rep.error(rel, f"not UTF-8 (read as {enc})")`. Confidence 85 |
| 7 | Location and message are masked separately | scripts/check.py:409 `if hit(where):` (for plain terms; see C2 for `=`). Confidence 85 |
| 8 | Table locations: header line numbers right (with `\n` line ends) | scripts/check.py:378. Confidence 85 |

#### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| U1 | scripts/check.py:318 | `for k, p in enumerate(pats, 1):` | Demonstrated defect | medium | `term_patterns` drops a term with no letters (:270), so the hit numbers (from `pats`) shift against the warning numbers (from `terms`, :264). With `CHECK_PRIVATE_TERMS="--,acme,beta"`, a `beta` hit is reported as "private term #2", which the user reads as `acme`. Found by UX and the category agent (5.1) | Deductive | 88 | Return `(k, pattern)` pairs and print that `k` |
| U2 | scripts/check.py:256 | `return [t.strip() for t in terms if t.strip()]` | Preventive measure | low | `#k` counts terms after comment and blank lines are removed, not lines of `.check-private-terms`, and neither the message nor the docstring says so. Empty items in the env var (`a,,b`) shift it too. Found by UX and the category agent (5.2) | Deductive | 80 | Print "term #k (line L of .check-private-terms)" |
| U3 | scripts/check.py:168 | `rep.error(EVALS, f"not valid JSON ({e.__class__.__name__}: {e})")` | Demonstrated defect | low | A missing evals.json is reported as "not valid JSON (FileNotFoundError: ...)", which sends the user to look for a syntax error. Found by UX and the category agent (3.14) | Deductive | 85 | Split `except OSError` from `except ValueError` |
| U4 | scripts/check.py:207 | `rep.error(EVALS, "ids are not consecutive from 1 in file order")` | Demonstrated defect | low | The message does not say which eval breaks the sequence, and it repeats the cause of "id is not an integer" or "duplicate id". The messages name the eval by id (:190), so with duplicates they do not say which of the two is meant (category 5.6) | Deductive | 85 | Name the first position where `ids[n-1] != n`; keep `#n` in messages |
| U5 | scripts/check.py:410 | `where = "[location hidden: its path contains a private term]"` | Preventive measure | low | When the term is in a file name, nothing points to the file to rename. The privacy trade-off is intended (scripts/test_check.py:294 expects "location hidden") | Deductive | 80 | Print the path with the matched span replaced |
| U6 | scripts/check.py:421 | `ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))` | Demonstrated defect | low | `--help` shows `--root ROOT` with no help, and the description is only the first docstring line (:418). A non-existent `--root` is not validated: check 1 reports "not valid JSON" and check 2 then crashes (category 3.17) | Deductive | 85 | Add a help text; `description=__doc__` with `RawDescriptionHelpFormatter`; check that `--root` exists |
| U7 | scripts/check.py:336 | `rep.warning(f"{rel}:{ln}", f"technology-bound term {m.group(0)!r}: keep it only as one of varied examples")` | Preventive measure | low | README.md gives routine warnings that cannot be silenced on every run, so the warning that matters ("private names were NOT checked", :296) has the same rank and is easy to skip. Patterns are also case-sensitive and unanchored (`python` missed, `Springfield` flagged; Code, Data, Documentation and category 1.10) | Inductive | 70 | A per-line opt-out; print the no-terms message as a separate notice |
| U8 | scripts/check.py:191-193 | `if key in e and (not isinstance(e[key], str) or not e[key].strip()):` / `rep.error(where, f"empty {key}")` | Demonstrated defect | low | A prompt or expected_output of the wrong type (number, list) is reported as "empty prompt". Category agent only | Deductive | 90 | "prompt is not a string" for the type case |
| U9 | scripts/check.py:128 | `rep.error(rel, f"not UTF-8 (read as {enc})")` | Demonstrated defect | low | SKILL.md and the reference files are read with `rep` by check 2 and check 7, so a non-UTF-8 SKILL.md gives the same ERROR twice and inflates the summary count. Category agent only (5.8) | Deductive | 90 | Report each file's encoding once |
| U10 | scripts/check.py:458 | `rep.checked.append("eval facts")` | Demonstrated defect | low | The summary lists "eval facts" even when the check returned early at :462. With --staged and an empty index, the list of checks is empty but reads like a clean pass (C9). Category agent (2.6) and UX hidden behavior 5 | Deductive | 85 | Append to `checked` only after the check completes, or mark it "skipped" |
| U11 | scripts/check.py:332 | `for ln, line in enumerate(read_text(root, rel).splitlines(), 1):` | Demonstrated defect | low | `splitlines` also breaks on `\x0b`, `\x0c`, `\x85`, U+2028 and U+2029, while check 3 counts only `\n` (:321). The same file is numbered differently by different checks (also :356, :486, :513), and CR-only files report every term hit at line 1. Category agent (4.10, 5.9-5.12); a hypothesis for UX and Data | Deductive | 85 | Number lines the same way everywhere (`split("\n")` after normalizing CR) |

### HYPOTHESES (UX)
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| 1 | scripts/check.py:527 `print(f"checked ({scope}): {', '.join(rep.checked)} — {len(rep.errors)} error(s), {len(rep.warnings)} warning(s)")` and the hook runs `-I` (ignores `PYTHONIOENCODING`) | On Windows with piped output and a code page without U+2014 (cp932), the summary raises UnicodeEncodeError, and a clean run exits 1 | A console stream, or cp1252 (which has U+2014) | `py -3 -I scripts/check.py > out.txt` under a Japanese locale |
| 2 | scripts/check.py:321 with --staged reads the temp checkout | Line numbers refer to the staged blob, not the file the user opens | Users look at the staged version | Stage a hit, add unstaged lines above it, run `--staged` |

### HIDDEN BEHAVIORS DETECTED (UX)
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| 1 | scripts/check.py:319 `m = p.search(body)` | No private term in any file | Only the first hit of each term per file is reported, so n hits need n runs | Preventive measure, low | 85 |
| 2 | scripts/check.py:525 `print(line)` | (not stated) | Everything goes to stdout, nothing to stderr | Preventive measure, low | 85 |
| 3 | scripts/check.py:524 `for line in mask(rep.errors + rep.warnings, terms):` | (not stated) | All errors before all warnings, with no grouping by check | none | 85 |

---

## CROSS-DOMAIN SUMMARY

- **Domains:** Code, Data, Documentation, UX. Each claim is counted once, in its primary domain.
- **Claims:** 40 PASS (Code 12, Data 6, Documentation 14, UX 8); 46 in FAIL (Code 15, Data 14, Documentation 6, UX 11); 0 falsified.
- **Findings by type:** 30 demonstrated defects (Code 10, Data 8, Documentation 4, UX 8), 16 preventive measures (Code 5, Data 6, Documentation 2, UX 3), 0 falsified hypotheses.
- **Critical issues:** 0 demonstrated defects of critical severity (0 critical preventive measures). High severity: 3 demonstrated defects (C1 separator, C2 masking of `=` terms, D3 inline comments in the terms file) and 1 preventive measure (C10, a tracked terms file is skipped).
- **Hypotheses:** 12. **Hidden behaviors:** 12 (after removing duplicates already counted as FAIL rows).
- **Failure categories:** 6 systemic patterns: missing completeness, silent fallthrough, missing checks for absent or malformed values, assumed environment, implicit ordering / index coupling, mode-dependent behavior.
- **Survived:** stress tests were not part of the returns (protocol). Invariants: not requested.
- **Executed:** none (reasoning only). **Proposed:** 5 checks, 0 writes.
- **Rows:** 385 came back, 0 discarded. The independent verifier confirmed 5 of 5 (C1, C2, C3, T1, D1) and changed none. The category agent added 15 FAIL rows that no domain agent had reported (marked "Category agent only"), and added instances to 3 more (T4, U10, U11).
- **Changes that touch several domains:** the private-term guarantee (:13-26) runs through all four. Detection (C1, D1, D2, D3, D9) is Code/Data, the masking of output (C2) is Code/UX, and the statements are Documentation (T2). The --staged mode (C9, T1, T4, hypothesis Code 1) touches Code and Documentation. The text in README.md:249-250 repeats C3, C1 and T2 but is out of scope: listed, not verified.
- **Recommendation:** do not trust check 3 (private terms) as a privacy gate until C1, C2 and D3 are fixed. Three tests in scripts/test_check.py already state the intended behaviour and, by reading, would be red.

## OUT OF SCOPE (listed, not verified)
- README.md:249-250 repeats "every skill badge" and the incomplete "Not caught" list (Documentation agent).
- scripts/test_check.py:171, :286, :341: tests that, by reading, contradict C3, C1 and C2.

## PROPOSED EXECUTABLE CHECKS
| # | Claim | Confidence now | Check (command, test or query) | Confirms if | Refutes if | Cost and side effects | Status |
|---|-------|----------------|--------------------------------|-------------|------------|-----------------------|--------|
| 1 | C1, C2, C3 (the suite is red on 3 tests) | 90 | `python3 -I -m unittest scripts/test_check.py` in ./tree | test_two_words_joined_any_way, test_whole_word_term_glued_in_output_is_still_masked and test_second_badge_mismatch fail | They pass | Runs the test suite; it builds temporary repos (reads and writes only in temp folders); seconds | proposed |
| 2 | Data hypothesis 1 (the stored prompt hashes are current) and the clean-tree result | 75 | `python3 -I scripts/check.py --root .` in ./tree | Exit 0 with no hash errors | A "prompt changed" error | Read-only on the tree; runs git ls-files | proposed |
| 3 | Code PASS 12 (Python 3.8) | 79 | Run check 1 under Python 3.8 | The suite passes on 3.8 | SyntaxError or AttributeError | Needs a 3.8 interpreter; read-only | proposed |
| 4 | UX hypothesis 1 (summary crashes on a non-UTF-8 pipe) | 60 | `py -3 -I scripts/check.py > out.txt` on Windows with a cp932 locale | Exit 1 with UnicodeEncodeError | The summary is in out.txt, exit 0 | Writes out.txt; needs a locale change | proposed |
| 5 | Code hypothesis 1 (--staged applies autocrlf) | 70 | In a scratch repo with `core.autocrlf=true`, stage an LF file, run `--staged` and dump tmp before cleanup | tmp holds CRLF | tmp holds LF | Creates a scratch repo; needs a temporary patch to keep tmp | proposed |

Should I run checks 1 and 2 (read-only on the tree, seconds), and leave 3-5 proposed?
