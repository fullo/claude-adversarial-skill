# Adversarial verification: scripts/check.py

## INTAKE

- **Target:** every domain detected in `scripts/check.py`: Code, Data, Documentation and UX. The script's logic is Code. The evals.json, fact-file and NOT_COMPUTABLE formats it enforces are Data. Its docstring, help text and error messages are Documentation. Its command-line interface and terminal output are UX.
- **Depth:** standard. **Scope:** the whole of `scripts/check.py` (no diff, no version history). **Execution mode:** reasoning only. Nothing was run. All four choices were given in the request, so none are defaults.
- **Cost estimate (large request, cost accepted in the request):** 1 file in scope (532 lines), 4 domains, about 100 claims (100 were decomposed), nothing run.
- **Method:** 4 domain agents, 1 independent verifier on the 5 highest-risk claims, 1 category agent, and 1 resend of a discarded row. All agents ran on the sonnet model at medium effort.
- **Rows:** 310 rows came back: 279 from the domain agents, 5 from the verifier, 25 from the category agent and 1 from the resend. I looked up every quote at the line its row names. 1 row was discarded (category row 24: its quote is at check.py:129, not :128). The resend restored it with the right line, so 0 rows were dropped. The independent verifier **confirmed 5 of 5** claims as FAIL, in agreement with the domain agents' FAIL rows. It **changed 1** domain row: UX PASS #5 (masking uses substring patterns) contradicts it, so that row now carries the lower confidence and both verdicts (U9). No PASS above 80 needed lowering, since every quote was looked up.
- **Not in the returns:** the briefs (PROTOCOL.md) ask only for DECOMPOSED CLAIMS, PASS, FAIL, HYPOTHESES, HIDDEN BEHAVIORS and FAILURE CATEGORIES. GROUND TRUTH, INVARIANTS, STRESS TEST RESULTS and ADVERSARIAL SCAFFOLD were therefore not produced. The full claim lists are in `out/returns/<domain>.md`.
- **Merging:** findings reported by several agents appear once, in their primary domain. They keep the lowest confidence any agent gave, and the agents that reported them are listed in brackets.

---

## VERIFICATION DOMAIN: Code

DECOMPOSED CLAIMS: 22 (out/returns/Code.md).

### PASS ✅
| # | Claim | Evidence (path:line) | Conf. |
|---|-------|----------------------|-------|
| 1 | Exact key set of each eval | scripts/check.py:180 `extra, missing = sorted(set(e) - EVAL_KEYS), sorted(EVAL_KEYS - set(e))` | 90 |
| 2 | Integer ids 1..n, bool rejected | scripts/check.py:186 `if type(i) is not int:  # bool is an int subclass: reject it`; :206 | 90 |
| 3 | Tags required from eval 21 | scripts/check.py:201 `elif i >= TAGGED_FROM and not TAG_RE.match(a):`; :75 | 90 |
| 4 | Whole-word matching only for `=` terms (detection side) | scripts/check.py:275 `pats.append(re.compile(rf"(?<![^\W_]){body}(?![^\W_])" if whole_word else body))` | 90 |
| 5 | Short-term warning; a term with no letters or digits is an error | scripts/check.py:271 `if rep is not None and sum(len(p) for p in parts) < 4:` | 90 |
| 6 | Neutral wording is warning-only; evals.json excluded | scripts/check.py:336; :142 | 90 |
| 7 | The staged temp dir is removed in `finally` | scripts/check.py:440 `shutil.rmtree(tmp, ignore_errors=True)` | 90 |
| 8 | Terms are loaded from the working repo before root switches to tmp | scripts/check.py:423 `terms = load_terms(args.root)  # always from the working repo: the list is never committed` | 95 |
| 9 | Reference files are named and exist | scripts/check.py:519 `for name in sorted(existing - named_in_skill):` | 90 |
| 10 | Exit code is 1 exactly when errors exist | scripts/check.py:442 `return 1 if rep.errors else 0` (Doc, UX; the verifier agrees that the exit code holds) | 90 |

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Conf. | Fix |
|---|-----------|-------|------|----------|----------|------|-------|-----|
| K1 | scripts/check.py:400 | `pats = term_patterns(terms)` | Demonstrated defect | high | The comment at :399 says masking uses substring patterns, but no `substring=True` is passed. `=` terms therefore keep their whole-word lookarounds (:265, :275). Example: an eval key `<term>labs` is reported at :182 and printed unmasked, so the private term leaks, contrary to :22-23. scripts/test_check.py:341 `test_whole_word_term_glued_in_output_is_still_masked` expects masking. **Independent verifier: FAIL (92), confirmed.** [Code F1, Doc F4/F5, Data F3, Verifier 1] | Deductive | 88 | `term_patterns(terms, substring=True)` |
| K2 | scripts/check.py:90 | `SEP = r"[\W_]?"  # anything that is not a letter or digit, possibly nothing` | Demonstrated defect | high | `?` allows at most one separator character, while :16-18 promise "anything". `A  B` (two spaces, built by scripts/test_check.py:286), `A - B` and `A\r\nB` (CRLF is not normalized, :125-130) are not caught, so a private name gets committed. **Independent verifier: FAIL (93), confirmed.** [Code F3/F4, Doc F2/F3, Data F2, Verifier 2] | Deductive | 88 | `SEP = r"[\W_]*"` |
| K3 | scripts/check.py:214 | `skill = read_text(root, SKILL, rep)` | Demonstrated defect | medium | The reads at :214, :217, :227 (only `ValueError` caught, :228), :237, :332, :356 and :512 have no OSError handling, and `main` has `try/finally` with no except (:426-440). A missing SKILL.md, README.md, CHANGELOG.md or plugin.json (a typo in `--root`, a staged deletion) gives a traceback. Errors already collected are never printed and checks 3-7 do not run. The exit code is still non-zero. **Independent verifier: FAIL (90), confirmed.** [Code F6, Data F8, UX F1, Verifier 4] | Deductive | 85 | Catch OSError for each required read and turn it into `rep.error(rel, "missing or unreadable")` |
| K4 | scripts/check.py:460 | `evals = json.loads(read_text(root, EVALS)).get("evals", [])` | Demonstrated defect | low | With `"evals": null` or a number, the set comprehension at :463 `ids = {e.get("id") for e in evals if isinstance(e, dict)}` raises a TypeError that is not caught (:461). Check 1's error is lost with the report. [Data F9, Category 15] | Deductive | 85 | `if not isinstance(evals, list): return` |
| K5 | scripts/check.py:470 | `if not stem.isdigit() or int(stem) not in ids:` | Preventive measure | low | `str.isdigit()` accepts `²`, which `int()` rejects, so a file named `².py` crashes the run. [Code F9, Verifier 5] | Deductive | 85 | `re.fullmatch(r"[0-9]+", stem)` |
| K6 | scripts/check.py:476 | `head = read_text(root, f"{FACTS_DIR}/{name}")[:2000]` | Preventive measure | low | No except around this read, nor around the NOT_COMPUTABLE read at :486. A directory or unreadable `40.py` ends the run with no report. [Category 16] | Deductive | 80 | Catch OSError and report it |
| K7 | scripts/check.py:254 | `with open(path, "rb") as f:` | Preventive measure | low | load_terms runs at :423, before the try. A `.check-private-terms` that is a directory or unreadable ends the run with no report. [Category 17] | Deductive | 80 | Catch OSError and report it |
| K8 | scripts/check.py:122 | `return data.decode("latin-1"), "latin-1"` | Preventive measure | medium | One invalid byte sends a UTF-8 file to Latin-1. `josé` becomes `josÃ©`, so an accented term is missed. This is not in the "Not caught" list (:24-26). [Code F8] | Deductive | 80 | Also scan a UTF-8 `errors="replace"` decoding |
| K9 | scripts/check.py:94 | `text = unicodedata.normalize("NFKD", text)` | Preventive measure | medium | Letters with no decomposition (ł, ø, đ, æ) are not folded, so `Lukasz` does not match `Łukasz`, contrary to "ignores accents" (:15). [Data F7] | Deductive | 75 | Transliteration table before casefold |
| K10 | scripts/check.py:365-366 | `else:` / `fence = None` | Preventive measure | low | The fence character stored at :364 `fence = f.group(1)[0]` is never compared. A `~~~` line inside a ``` block closes it early, and tables after it are skipped or code is checked as tables. No current instance. [Code F7, Doc F10, Data F11] | Deductive | 75 | Close only on the same character and at least the opening length |
| K11 | scripts/check.py:341 | `DELIM = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")` | Preventive measure | low | GFM tables whose delimiter has 1-2 dashes are not recognized and are never checked. None in the tree today. [Code H12, Doc B6, Data F10] | Deductive | 75 | `-+` |
| K12 | scripts/check.py:345 | ``s = re.sub(r"`[^`]*`", "x", line).replace("\\|", "x").strip()`` | Demonstrated defect | low | A double-backtick span ``` ``a|b`` ``` is matched as two empty spans, so its inner pipe is counted and a valid row is miscounted. No current instance. [Category 2, Code H12] | Deductive | 85 | Match code spans by backtick-run length |
| K13 | scripts/check.py:356 | `lines = read_text(root, rel).splitlines()` | Preventive measure | low | `splitlines()` also breaks on \x85,   and other characters, so a row splits into false cell-count errors and line numbers disagree with :321. The same applies at :332, :486 and :513. [Category 14] | Deductive | 80 | `split("\n")` after normalizing CRLF |
| K14 | scripts/check.py:85 | `r"Laravel", r"Django", r"Rails", r"Spring", r"React", r"Angular", r"Vue",` | Preventive measure | low | No `\b`: "Reactive" and "Springboard" warn as technology terms. [Category 23] | Deductive | 80 | Add `\b` |
| K15 | scripts/check.py:137 | `return [f"{REFS_DIR}/{n}" for n in names if n.endswith(".md")]` | Preventive measure | low | `.MD` files and subfolders of references/ are never checked by checks 4, 5 and 7, contrary to "every .md file" (:42). [Category 3] | Deductive | 85 | Case-insensitive extension; report subfolders |
| K16 | scripts/check.py:67 | `REF_RE = re.compile(r"references/([A-Za-z0-9_.-]+\.md)\b")` | Preventive measure | low | Names with non-ASCII letters, spaces, `%20` or subfolders are not recognized. A broken link escapes, and a named file is reported as "never named". [Category 4] | Deductive | 80 | Widen the pattern |
| K17 | scripts/check.py:440 | `shutil.rmtree(tmp, ignore_errors=True)` | Preventive measure | low | A failed cleanup (locked files on Windows) is silent and leaves the staged content in the shared temp folder. [Category 9] | Deductive | 85 | Warn when the directory still exists |
| K18 | scripts/check.py:469 | `if ext in FACT_EXTS and not stem.startswith("_"):` | Preventive measure | low | `41.PY`, `41.js` and `41.py.bak` are ignored silently. The author sees only "no fact file". Helpers starting with `_` carry no hash, so editing one does not invalidate the facts that import it. [Code H11, Category 11] | Deductive | 80 | Report unexpected entries |
| K19 | scripts/check.py:525 | `print(line)` | Preventive measure | medium | Assumes stdout can encode every path and message. A pipe with a legacy code page raises UnicodeEncodeError partway through the report. Under the hook's `-I` (scripts/pre-commit:9) the user cannot override this. [Category 12; see also H2] | Deductive | 70 | `sys.stdout.reconfigure(errors="replace")` |

---

## VERIFICATION DOMAIN: Data

DECOMPOSED CLAIMS: 25 (out/returns/Data.md).

### PASS ✅
| # | Claim | Evidence (path:line) | Conf. |
|---|-------|----------------------|-------|
| 1 | Invalid evals.json is rejected | scripts/check.py:167 `except (OSError, ValueError) as e:` | 90 |
| 2 | Non-empty fields and assertions | scripts/check.py:192; :195 `if not isinstance(assertions, list) or not assertions:` | 85 |
| 3 | plugin.json version is a string equal to SKILL.md's | scripts/check.py:233 `if not isinstance(pv, str):`; .claude-plugin/plugin.json:3 | 90 |
| 4 | The newest numbered CHANGELOG entry is compared | scripts/check.py:237; CHANGELOG.md:5 `## Unreleased` is skipped, CHANGELOG.md:10 is used | 85 |
| 5 | The version is taken from the frontmatter only (CRLF and BOM handled) | scripts/check.py:215, :216, :120 | 85 |
| 6 | JSON keys and values are scanned after decoding | scripts/check.py:315 `strings = [normalize(x) for x in json_strings(json.loads(text))]` | 85 |
| 7 | A fact file or a reason, not both | scripts/check.py:495 `for i in sorted(set(reasons) & set(with_file)):`; :500 | 85 |
| 8 | NOT_COMPUTABLE line format | scripts/check.py:491 `if not m or not m.group(2):` | 85 |
| 9 | Tracked files / staged content selection | scripts/check.py:389, :147, :433 | 85 |

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Conf. | Fix |
|---|-----------|-------|------|----------|----------|------|-------|-----|
| D1 | scripts/check.py:223 | `for b in badges[:1]:` | Demonstrated defect | medium | Only the first README badge is compared, contrary to :10 and README.md:249 ("every skill badge in the README"). A stale second badge passes. scripts/test_check.py:171 `test_second_badge_mismatch` expects "version mismatch". **Independent verifier: FAIL (94), confirmed.** [Code F2, Doc F1, Data F1, Verifier 3] | Deductive | 90 | `for b in badges:` |
| D2 | scripts/check.py:473 | `with_file[int(stem)] = name` | Demonstrated defect | medium | `35.py` + `35.ts`, or `035.py` + `35.py`: the later name overwrites the earlier one, so only one file's prompt-sha256 is checked (:475-482). scripts/check_facts.py still runs both. No such pair exists today. **Independent verifier: FAIL (90), confirmed.** [Code F5 (as preventive), Doc F6, Data F4, Verifier 5] | Deductive | 85 | A list per id; error when an id has more than one file |
| D3 | scripts/check.py:494 | `reasons[int(m.group(1))] = m.group(2)` | Preventive measure | low | A reason for a non-existent eval, or a duplicate id line, is accepted silently, while orphan fact files are errors (:471). [Code F10, Data F12] | Deductive | 80 | Report unknown and duplicate ids |
| D4 | scripts/check.py:166 | `data = json.loads(read_text(root, EVALS, rep))` | Preventive measure | low | Duplicate keys collapse (last wins), so `"prompt"` given twice passes the exact-keys check and the sha256 binding uses the last value. [Data F13] | Deductive | 80 | `object_pairs_hook` that rejects duplicates |
| D5 | scripts/check.py:301 | `if os.path.basename(rel) == TERMS_FILE:` | Preventive measure | high | Any file named `.check-private-terms`, at any depth and tracked or not, is skipped without a message. Nothing enforces the "never committed" of :423. A `git add -f` publishes the whole private list and the check passes. .gitignore:1 covers only unforced adds. Likelihood low. [Data F5, Doc F12, Category 8] | Deductive | 75 | Error when a tracked or staged file has that name |
| D6 | scripts/check.py:248 | `if raw is not None:` | Preventive measure | medium | An exported but empty `CHECK_PRIVATE_TERMS` shadows `.check-private-terms`, and the message at :295 then tells the user to create a file that already exists. Without `--strict` this is only a warning. [Data F6, UX F6, Doc B1, Code H2] | Deductive | 75 | Treat an empty variable as unset, or name the source used |
| D7 | scripts/check.py:313 | `if rel.endswith(".json"):` | Preventive measure | medium | Only lowercase `.json` gets the decoded pass. A term written with escapes in `.ipynb`, `.jsonl` or `.JSON` passes. [Category 1] | Deductive | 85 | Try a JSON decode for every JSON-like extension |
| D8 | scripts/check.py:237 | `first = re.search(r"^## +([0-9][0-9.]*)\b", read_text(root, CHANGELOG, rep), re.M)` | Preventive measure | low | A newest heading `## [1.3.0]` or `## v1.3.0` is skipped and an older entry is compared: a false pass, or a mismatch naming the wrong entry. [Category 5] | Deductive | 80 | Accept `[`/`v` prefixes, or error on an unparsed heading above the first match |

---

## VERIFICATION DOMAIN: Documentation

DECOMPOSED CLAIMS: 35 (out/returns/Documentation.md).

### PASS ✅
| # | Claim | Evidence (path:line) | Conf. |
|---|-------|----------------------|-------|
| 1 | "Errors make the exit code non-zero; warnings ... do not block" (exit code part) | scripts/check.py:4; :442 | 90 |
| 2 | Check 1 rules as documented | scripts/check.py:6-9; :180-207 | 90 |
| 3 | Normalization (case, accents, Unicode forms), except K9 | scripts/check.py:15-16; :93-96 | 90 |
| 4 | Without terms it says so; `--strict` fails | scripts/check.py:23-24; :294-298 | 92 |
| 5 | Check 4 scope and severity | scripts/check.py:27-29; :328-336 | 90 |
| 6 | Fact file or reason, not both (rule text) | scripts/check.py:34-36; :495-501 | 85 |
| 7 | Usage line matches argparse | scripts/check.py:49; :419-421 | 92 |
| 8 | "Requires Python 3.8 or later" | scripts/check.py:50 (run-only) | 79 |
| 9 | decode never raises | scripts/check.py:113; :122 | 92 |
| 10 | Constant comments match their use | scripts/check.py:74, :77 | 85 |
| 11 | "check 1 already reports it" | scripts/check.py:462; :165-173 | 85 |
| 12 | `--strict` help text | scripts/check.py:419 | 90 |

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Conf. | Fix |
|---|-----------|-------|------|----------|----------|------|-------|-----|
| M1 | scripts/check.py:43-44 | `The folder is read as it is on disk, tracked or not, since copying the skill's folder ships every file in it.` | Demonstrated defect | medium | With `--staged`, `root = tmp` (:433), so references/ is read from the checkout-index copy, which has no untracked files. The pre-commit hook always uses `--staged` (scripts/pre-commit:9), so an untracked, unnamed references/x.md passes the commit check. [Doc F7] | Deductive | 85 | Read args.root's references/ in staged mode too, or reword |
| M2 | scripts/check.py:24-26 | `Not caught: a one-word term written as two words ...` | Preventive measure | medium | The list leaves out multi-character separators and CRLF (K2), untracked files, `.check-private-terms` at any depth (D5), unparseable JSON, Latin-1 fallback for accented terms (K8) and non-decomposing letters (K9). [Doc F8] | Deductive | 75 | Complete the list (or fix the causes) |
| M3 | scripts/check.py:46-47 | `Files checked: the files tracked by git (all files outside .git if git is not available).` | Demonstrated defect | low | The fallback also applies when git works but nothing is tracked or root is not a repository (:149-152). The tracked-file list applies only to check 3: checks 4-7 read fixed paths from disk. [Doc F11, Code H5/HY4] | Deductive | 85 | Reword |
| M4 | scripts/check.py:168 | `rep.error(EVALS, f"not valid JSON ({e.__class__.__name__}: {e})")` | Demonstrated defect | low | A missing evals.json is reported as "not valid JSON (FileNotFoundError ...)". [Doc F9, UX H5] | Deductive | 90 | Separate message for OSError |
| M5 | scripts/check.py:22-23 | `Terms are never printed: any output line containing one is masked.` | Preventive measure | medium | Masking covers only report lines (:524). Any uncaught exception (K3-K7) prints a traceback to stderr with unmasked absolute paths, which may contain a private name. [Category 6, Doc H1, UX hidden 5] | Deductive | 75 | Catch in `main`, report through `rep`; or state the limit |
| M6 | scripts/check.py:387 | `"""Write the staged content into tmp; return the staged file list, or None if root is not a git repository."""` | Demonstrated defect | low | None is returned on any git failure (:392), not only "not a repository". [Category 7] | Deductive | 90 | Reword |
| M7 | scripts/check.py:431 | `rep.error("--staged", "not a git repository (or git is not available)")` | Demonstrated defect | low | Shown for any git failure (index.lock, tmp not writable). git's stderr is discarded (:390-391), so the user gets the wrong cause. [Category 18] | Deductive | 85 | Include git's stderr |
| M8 | scripts/check.py:219 | `rep.error(SKILL, "no version in the frontmatter")` | Demonstrated defect | low | Also shown for a version that :216 rejects (`'1.2.0'`, `1.3.0-beta`): the message denies what is in the file. [Category 19] | Deductive | 85 | "no version the check can read" |
| M9 | scripts/check.py:480 | `rep.error(f"{FACTS_DIR}/{name}", f"no 'prompt-sha256:' line binding it to eval {i}'s prompt")` | Preventive measure | low | Also shown for uppercase hex, or for a line beyond the first 2000 characters (:476-477). [Category 20] | Deductive | 80 | Case-insensitive hex; state the limit |
| M10 | scripts/check.py:471 | `rep.error(f"{FACTS_DIR}/{name}", "fact file for an eval that does not exist")` | Preventive measure | low | Also shown for `helper.py` or `35a.py`, which hides the `_` naming rule. [Category 21] | Deductive | 80 | Separate message for non-numeric stems |
| M11 | scripts/check.py:305 | `rep.error(rel, f"private term #{k} in the file name")` | Preventive measure | low | :304 matches the whole path, so a term in a directory name is reported as "in the file name". [Category 22] | Deductive | 75 | "in the path" |
| M12 | scripts/check.py:269 | `rep.error("private terms", f"term #{k} has no letters or digits and cannot be checked")` | Preventive measure | low | `#k` counts terms after comment and blank lines were dropped (:255-256), so it is not the file's line number. [Category 25, UX hidden 7] | Deductive | 70 | Report the source line |
| M13 | scripts/check.py:129 | `rep.error(rel, f"not UTF-8 (read as {enc})")` | Demonstrated defect | low | SKILL.md is read with `rep` at :214 and :512, so a non-UTF-8 SKILL.md is reported twice and the error count is inflated. [Category 24 (resent: line corrected from :128), Code H10] | Deductive | 85 | Report each file once |

---

## VERIFICATION DOMAIN: UX (command-line interface)

DECOMPOSED CLAIMS: 18 (out/returns/UX.md). Plain text, no colour, no interactive input: contrast, target and pointer checks do not apply.

### PASS ✅
| # | Claim | Evidence (path:line) | Conf. |
|---|-------|----------------------|-------|
| 1 | Exit code non-zero exactly on errors | scripts/check.py:442 `return 1 if rep.errors else 0` | 90 |
| 2 | Summary line, with scope and counts, on every path that does not raise | scripts/check.py:527 (raising paths: K3) | 85 |
| 3 | Severity readable without colour | scripts/check.py:109 `self.warnings.append(f"WARNING {where}: {msg}")`; :106 | 90 |
| 4 | Missing terms are reported with the two ways to fix it | scripts/check.py:296 `"private names were NOT checked")` (wording issue: D6) | 85 |
| 5 | Editor-friendly `path:line` locations | scripts/check.py:336 | 85 |
| 6 | Table messages name the correct header line | scripts/check.py:373 | 90 |
| 7 | `--staged` outside git: clear error, no leftover temp dir | scripts/check.py:440 | 85 |

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Conf. | Fix |
|---|-----------|-------|------|----------|----------|------|-------|-----|
| U1 | scripts/check.py:293 | `rep.checked.append("private terms")` | Demonstrated defect | medium | With no terms and no `--strict`, the summary says `checked ...: ..., private terms, ... — 0 error(s)`, though nothing was scanned. Someone who reads only the summary believes the scan ran. [UX F2] | Deductive | 85 | Append after the early return, or mark it "NOT checked" |
| U2 | scripts/check.py:462 | `return  # check 1 already reports it` | Demonstrated defect | low | "eval facts" is already appended (:458), so the summary lists check 6 as done when it was skipped. Check 1's error keeps the run red. [Category 10, UX hidden 9] | Deductive | 85 | Append after the parse |
| U3 | scripts/check.py:303 | `for k, p in enumerate(pats, 1):` | Demonstrated defect | low | A term with no letters is dropped (:268-270), so the numbers of later terms shift. "private term #1" then points at the wrong configured term, and the number is the only pointer the user gets. Same at :318. [UX F3] | Deductive | 85 | Carry the original index |
| U4 | scripts/check.py:436 | `if files or not args.staged:` | Demonstrated defect | low | With an empty index, no check runs and the output is `checked (staged content):  — 0 error(s)` with exit 0, `--strict` included. An empty state that looks like a clean pass. [UX F4, Doc B5, Code H4] | Deductive | 80 | Print "nothing staged: no check run" |
| U5 | scripts/check.py:418 | `ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])` | Preventive measure | low | `--help` shows no configuration (environment variable, file, `=` prefix), and `--root` has no help text. [UX F5] | Deductive | 80 | An epilog with the configuration |
| U6 | scripts/check.py:319 | `m = p.search(body)` | Preventive measure | low | Only the first occurrence per term per file is reported, so the user needs one run per occurrence. The decoded JSON scan runs only when the raw text had no match. [UX F7, Data HB9] | Deductive | 80 | `finditer`, or report a count |
| U7 | scripts/check.py:410 | `where = "[location hidden: its path contains a private term]"` | Preventive measure | low | The whole location is dropped, so several affected files cannot be told apart. [UX F8] | Deductive | 80 | Mask only the matched span |
| U8 | scripts/check.py:321 | `rep.error(f"{rel}:{body.count(chr(10), 0, m.start()) + 1}", f"private term #{k} of the configured list")` | Preventive measure | low | Only `\n` is counted, so a CR-only file always reports line 1. [UX F9, Data Y3] | Deductive | 80 | Normalize line endings first |
| U9 | scripts/check.py:524 | `for line in mask(rep.errors + rep.warnings, terms):` | **Disputed** (domain PASS vs verifier FAIL) | high | UX PASS #5 said report lines containing a term are masked with substring patterns (85). The independent verifier says FAIL: :400 builds whole-word patterns for `=` terms, so a glued form is printed unmasked (92). The Code, Doc and Data agents agree with the verifier (K1). Kept at the lower confidence, with both verdicts. | Deductive | 85 | See K1 |

---

## HYPOTHESES (all domains)
| # | Observation (path:line) | Hypothesis | Alternative | Test to confirm |
|---|-------------------------|-----------|-------------|-----------------|
| H1 | scripts/test_check.py:171 `def test_second_badge_mismatch(self):`, :286, :341 | The repo's own suite is red at HEAD on 3 tests (D1, K2, K1). The code regressed after the tests were written, and the hook (scripts/pre-commit:9) runs only check.py | The tests were written ahead of the code | `python3 -m unittest scripts/test_check.py` |
| H2 | scripts/check.py:527 (em dash in the summary); scripts/pre-commit:9 `-I` | A non-UTF-8 stdout (cp437/cp932 pipe, ISO-8859-1 locale) raises UnicodeEncodeError and the summary is lost | Modern consoles are UTF-8 (PEP 528/538/540) | `chcp 437` then `py -3 scripts/check.py \| more` |
| H3 | scripts/check.py:389-391 | With submodules, `--staged` reports "unreadable file" for every gitlink | ls-files or open() behaves differently for gitlinks | Temporary repo with a submodule |
| H4 | scripts/check.py:149-150 | When `--root` is an untracked folder inside another repo, the script walks untracked files | git errors, and the walk is intended | `--root` on such a folder |
| H5 | scripts/check.py:389 | The absolute `--prefix` with `os.sep` fails on Windows, so every `--staged` run reports "not a git repository" | It works | `py -3 scripts/check.py --staged` on Windows |
| H6 | scripts/check.py:389 | Run from a subdirectory root, the checkout-index paths and the ls-files paths do not match (55) | The hook passes `--show-toplevel`, so it is unaffected | `--root` on a subdirectory |
| H7 | scripts/check.py:33 | GFM splits cells on pipes inside code spans, so a row the check passes renders with an extra cell | The renderer treats them as text | Render the test_check.py:442 case on GitHub |
| H8 | scripts/check.py:114 | A UTF-32-LE BOM is decoded as UTF-16, so terms are missed | No UTF-32 files in the repo | UTF-32 file containing a term |
| H9 | scripts/check.py:463 | `"id": true` makes `1.py` count as belonging to an existing eval | Harmless: check 1 already fails | Eval with id `true` |
| H10 | scripts/check.py:216 | `version: "4.2` (unbalanced quote) passes, and YAML consumers break | No other tool parses it | Edit SKILL.md and run |
| H11 | scripts/check.py:524 | Standing WARNING lines (README.md:229, :230, :234, :240) teach users to skip the no-terms warning | The block is short and errors come first | `python3 scripts/check.py \| grep -c WARNING` |
| H12 | scripts/check.py:436 | Through the hook, git refuses an empty commit before the misleading "0 error(s)" appears | It is shown before "nothing to commit" | `git commit -m x` with an empty index |

## HIDDEN BEHAVIORS DETECTED (not already a FAIL row)
| # | Location | Advertised | Actual | Type | Conf. |
|---|----------|-----------|--------|------|-------|
| B1 | scripts/check.py:237 | "the first `## <version>` entry" | `## Unreleased` is skipped | Not a problem | 85 |
| B2 | scripts/check.py:128 | "A file that is not UTF-8 is still scanned" | Non-UTF-8 SKILL.md, README.md, evals.json and reference files are errors; CHANGELOG.md and plugin.json are not | Undocumented rule | 85 |
| B3 | scripts/check.py:469 | "every fact file belongs to an existing eval" | `_` files are exempt; the stem `035` is accepted as 35 | Undocumented exemption | 85 |
| B4 | scripts/check.py:316-317 | JSON decoded after escapes | A .json file that does not parse gets no decoded pass, with no message | Preventive, low | 85 |
| B5 | scripts/check.py:255 | "# for comments" | Only whole-line comments: `name  # note` makes "note" part of the term | Undocumented rule, low | 82 |
| B6 | scripts/check.py:193 | "empty prompt" | Also printed for a non-string value | Cosmetic | 85 |
| B7 | scripts/check.py:309 | Unreadable file → error | A tracked file deleted but not staged is reported as "unreadable" | Fails closed, low | 80 |

## FAILURE CATEGORIES IDENTIFIED (after the category search)
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Missing completeness ("every/any" covering part of the set) | D1, D2, D3, D4, D7, K1, K12, K15, K16, D8, M5 | scripts/check.py |
| Stale state (comment, docstring or help drifted from the code; the tests still encode the documented behaviour) | K1 (:399-400), K2 (:90), D1 (:10 vs :223), M1, M3, M6, D5 (:423) | scripts/check.py, scripts/test_check.py |
| Silent fallthrough (an edge case handled by doing nothing, or a skipped state shown as done) | D5, D6, B4, U1, U2, U4, K10, K11, K17, K18 | scripts/check.py |
| Assumed environment (line endings, encodings, console, git layout) | K2 (CRLF), K8, K9, K13, K19, U8, H2, H5, H6, H8 | scripts/check.py, scripts/pre-commit |
| Uneven error handling (an uncaught exception loses the report) | K3, K4, K5, K6, K7 | scripts/check.py |
| Misleading or partial messages | M4, M7, M8, M9, M10, M11, M12, M13, U3, U5, U6, U7, B6 | scripts/check.py |

## CROSS-DOMAIN SUMMARY
- Domains: Code, Data, Documentation, UX (one file, scripts/check.py)
- Claims: 100 decomposed (22 Code, 25 Data, 35 Documentation, 18 UX); 38 PASS rows above (each counted once); 48 in FAIL (18 demonstrated defects, 30 preventive measures); 0 falsified hypotheses; 1 disputed row (U9, the same subject as K1)
- Independent verifier: 5 claims checked, 5 FAIL confirmed, 1 domain PASS contradicted (U9)
- Stress tests: not produced (not requested by the protocol's brief)
- Invariants: not produced by the domain agents. The verifier used scripts/test_check.py and the docstring as project invariants. The docstring's "Terms are never printed" (scripts/check.py:22-23) is broken (K1, M5)
- Failure categories: 6 systemic patterns
- Hypotheses: 12 · Hidden behaviors not already in FAIL: 7
- Critical issues: 0 demonstrated defects of critical severity. High: K1 and K2 (private-term leak through masking or matching, both demonstrated) and D5 (preventive)
- Pre-code: not applicable · Executed: nothing (reasoning only)
- Recommendation: do not rely on check 3's privacy guarantee until K1 and K2 are fixed. Both, and D1, are already caught by the repo's own unit tests, which are not run by the pre-commit hook (H1).

## PROPOSED EXECUTABLE CHECKS
| # | Claim | Confidence now | Check | Confirms if | Refutes if | Cost and side effects | Status |
|---|-------|----------------|-------|-------------|------------|-----------------------|--------|
| 1 | K1, K2, D1 and H1 | 88 / 88 / 90 | `python3 -m unittest scripts/test_check.py` | Red on test_whole_word_term_glued_in_output_is_still_masked, test_two_words_joined_any_way (two-space variant) and test_second_badge_mismatch | All green | Runs the existing suite; the tests write only to their own temp dirs (to be confirmed by reading their setUp) | proposed |
| 2 | K3, M5 | 85 / 75 | `python3 scripts/check.py --root <copy without CHANGELOG.md>` with `CHECK_PRIVATE_TERMS=<dir name>` | A traceback with no summary and the term in stderr | A report line "missing" | Reads a temp copy | proposed |
| 3 | U4, H12 | 80 | `scripts/check.py --strict --staged` in a scratch repo with an empty index | Exit 0 with no checks listed | An error or a "nothing staged" message | Scratch repo only | proposed |
| 4 | H2, K19 | 70 | `chcp 437` then `py -3 scripts/check.py \| more` | UnicodeEncodeError | Summary printed | Read-only | proposed |
| 5 | H5 | — | `py -3 scripts/check.py --staged` on Windows | "not a git repository" in a real repo | Normal report | Read-only; writes a temp dir | proposed |

Proposed writes: fixes K1 (`term_patterns(terms, substring=True)`, scripts/check.py:400), K2 (`SEP = r"[\W_]*"`, scripts/check.py:90), D1 (`for b in badges:`, scripts/check.py:223), and OSError handling for K3. Also proposed: adding `python3 -m unittest scripts/test_check.py` to scripts/pre-commit and a CHANGELOG.md "Unreleased" entry for the fixes.

**Should I run checks 1-5 above, and write any of the proposed fixes? Nothing runs and nothing is written without your answer.**
