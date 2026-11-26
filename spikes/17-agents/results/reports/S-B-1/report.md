# Verification report: scripts/check.py

Scope: the whole of scripts/check.py (531 lines). Depth: standard. Reasoning only, nothing was run.
Domains detected: Code, Documentation, UX (the file is a command-line tool with a long docstring and messages). Architecture, Data, Tests and Analysis were not detected. scripts/test_check.py was read only as ground truth.
Full per-domain tables are in out/returns/Code.md, Documentation.md and UX.md. Below, the rows are merged by finding, with the quoted line at the line named.

**Row count:** 217 rows came back (186 from the three domain agents, 5 from the independent verifier, 26 from the category agent). 5 were discarded because the quote was not at the line named. The independent verifier confirmed 4 of its 5 claims as failures, changed 1 (partly true, lower confidence), and reversed none.

## INTAKE
Target: every detected domain. Files: scripts/check.py (about 25 kB, so one agent per domain).

## CODE

### FAIL
| # | File:Line | Quote | Type | Severity | Scenario | Confidence |
|---|-----------|-------|------|----------|----------|------------|
| C1 | scripts/check.py:223 | `for b in badges[:1]:` | Demonstrated defect | medium | Only the first README badge is compared. A second stale badge (`badge/skill-v2.0-`) raises no error, although scripts/test_check.py:171-172 (`test_second_badge_mismatch`) appends one and expects "version mismatch". Code, Documentation and the verifier agree. Fix: `for b in badges:`. | 95 |
| C2 | scripts/check.py:460 | `evals = json.loads(read_text(root, EVALS)).get("evals", [])` | Demonstrated defect | medium | check_evals reports `"evals": null` or an eval whose `id` is a list, then check_facts raises TypeError at scripts/check.py:463 (`ids = {e.get("id") for e in evals if isinstance(e, dict)}`). Only OSError, ValueError and AttributeError are caught (scripts/check.py:461), so print_report is never reached and the errors already collected are lost. Verifier agrees. | 95 |
| C3 | scripts/check.py:227 | `plugin = json.loads(read_text(root, PLUGIN, rep))` | Demonstrated defect | medium | A missing README, SKILL.md, plugin.json or CHANGELOG.md raises FileNotFoundError and ends in a traceback with no report. Same at scripts/check.py:214, 217, 237, 332, 356, 512. check_evals handles OSError (scripts/check.py:167) but the others do not. UX rates it 85, Code 80. | 83 |
| C4 | scripts/check.py:274 | `body = SEP.join(re.escape(p) for p in parts)` | Demonstrated defect | medium | SEP is `[\W_]?`: at most one character joins the parts of a term. "alpha beta" is missed in "alpha  beta", "alpha, beta" and across a CRLF line break ("alpha\r\nbeta"), though the docstring promises line breaks. A private term leaks past the check. Raised by Documentation and UX, confirmed by the verifier (93). The Code agent's own row for it was discarded (wrong line), so this row stands on the other two plus the verifier. | 90 |
| C5 | scripts/check.py:122 | `return data.decode("latin-1"), "latin-1"` | Demonstrated defect | medium | A file that is mostly UTF-8 with one invalid byte is read as Latin-1, so "café" becomes mojibake and is not matched. The "not UTF-8" error exists only for SKILL, README, evals.json and references (scripts/check.py:128), so elsewhere the miss is silent. Single source. | 80 |
| C6 | scripts/check.py:363 | `if fence is None:` | Preventive measure | low | A fence closes on any line starting with three backticks or tildes, whatever the opener (the stored character at scripts/check.py:364 is never compared). A nested fence turns table checking on or off wrongly. Code, Documentation and UX all raise it. | 75 |
| C7 | scripts/check.py:470 | `if not stem.isdigit() or int(stem) not in ids:` | Preventive measure | low | A fact file named with a character such as "²" passes isdigit() and int() raises ValueError: traceback instead of a report. | 75 |
| C8 | scripts/check.py:473 | `with_file[int(stem)] = name` | Preventive measure | low | 35.py and 35.ts (or 035.py) map to one id; the later overwrites the earlier, which is then never hash-checked. | 80 |
| C9 | scripts/check.py:436 | `if files or not args.staged:` | Demonstrated defect | medium | With --staged and an empty index, no check runs, the summary prints `checked (staged content):  — 0 error(s), 0 warning(s)` and the exit code is 0: a pass that checked nothing. UX 70, Documentation 85, verifier 90 (fails). | 85 |
| C10 | scripts/check.py:524 | `for line in mask(rep.errors + rep.warnings, terms):` | Preventive measure | medium | "Terms are never printed" holds for every ERROR/WARNING line. It does not hold as an absolute: tracebacks (see C2, C3, C7) and argparse errors go to stderr unmasked, with paths. Here the independent verifier said partly (68) where UX had passed the narrower claim (78); the lower figure is kept, both verdicts recorded. | 68 |

### Not reproduced as passes
Claims that held (Code PASS rows 1, 2, 3, 5, 6, 10-13, 15-17, 19, 20; UX PASS rows 1-10): exit code logic at scripts/check.py:442, key and id validation at scripts/check.py:180-206, tag rule at scripts/check.py:201, plugin.json and CHANGELOG comparison at scripts/check.py:233-241 (CHANGELOG.md:5 `## Unreleased` skipped, CHANGELOG.md:10 `## 4.2` read, README.md:1 badge v4.2, plugin.json:3 `"version": "4.2"`), whole-word terms at scripts/check.py:275, short and empty term handling at scripts/check.py:269-273, --strict at scripts/check.py:297 (scripts/pre-commit:9 passes it), fact/reason rules at scripts/check.py:495-501, reference rules at scripts/check.py:518-520. Code PASS rows carry no confidence figure in the return; I treat them as at most 79 because the evidence lines in other files (scripts/test_check.py:161 and 555) were not all looked up. UX PASS confidences above 80 kept only where the quote and cited lines were found; UX PASS 10 rests on README.md:257-259, where only README.md:258 and 260 were found, so it is 79.

### HYPOTHESES (not confirmed)
| # | Location | Quote | Hypothesis | Test |
|---|----------|-------|-----------|------|
| H1 | scripts/check.py:247 | `raw = os.environ.get("CHECK_PRIVATE_TERMS")` | A set but empty variable replaces the terms file, so no terms apply (error only under --strict). Code, Documentation (hidden, 85) and UX raise it. | Run with `CHECK_PRIVATE_TERMS=` and a populated file. |
| H2 | scripts/check.py:341 | `DELIM = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")` | Short delimiters (`\|-\|`) go unrecognised; a `---` rule under a pipe line may give a false error (scripts/check.py:369). | Add such tables to README.md. |
| H3 | scripts/check.py:375 | `while i < len(lines) and lines[i].strip() and "|" in lines[i]:` | A row with no pipe ends the table silently. | Remove the pipes from one row. |
| H4 | scripts/check.py:114 | `if data.startswith((b"\xff\xfe", b"\xfe\xff")):` | UTF-32 LE (`ff fe 00 00`) is decoded as UTF-16. | Scan a UTF-32 file. |
| H5 | scripts/check.py:148 | `files = [f for f in out.stdout.decode("utf-8", "replace").split("\0") if f]` | With no tracked files the walk runs and includes untracked files (also scripts/check.py:151-152, where any git failure falls back silently). | New repository. |
| H6 | scripts/check.py:527 | `print(f"checked ({scope}): {', '.join(rep.checked)} — {len(rep.errors)} error(s), {len(rep.warnings)} warning(s)")` | On a legacy console code page the em dash (and any non-ASCII path, scripts/check.py:525) raises UnicodeEncodeError and loses the report (UX 55). | Pipe the output on Windows. |
| H7 | scripts/check.py:389 | `subprocess.run(["git", "-C", root, "checkout-index", "-a", "--prefix=" + tmp + os.sep],` | A backslash prefix on Windows and `--root` below the repository top level may break --staged (UX). | Run it on Windows / from a subfolder. |
| H8 | scripts/check.py:418 | `ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])` | `python -OO` makes `__doc__` None: AttributeError. | `python3 -OO scripts/check.py`. |
| H9 | scripts/check.py:404 | `m = re.match(r"^(ERROR|WARNING) (.*?): (.*)$", line)` | A path or message containing ": " splits a term across the halves and it prints. | File name with ": ". |

### HIDDEN BEHAVIORS DETECTED
| # | Location | Quote | Advertised | Actual | Confidence |
|---|----------|-------|-----------|--------|------------|
| B1 | scripts/check.py:301 | `if os.path.basename(rel) == TERMS_FILE:` | terms file untracked, "never committed" | A file of that name in any directory is exempt from the scan; a committed copy of the terms is never flagged. | 85 |
| B2 | scripts/check.py:321 | `rep.error(f"{rel}:{body.count(chr(10), 0, m.start()) + 1}", f"private term #{k} of the configured list")` | a line number | First match per term and file only; CR-only files always report line 1. | 70 |
| B3 | scripts/check.py:457 | `def check_facts(root, rep):` | a reason line has a purpose | A reason for an id that does not exist, or for an eval that no longer says "(Facts", is never reported (also scripts/check.py:494). | 70 |
| B4 | scripts/check.py:469 | `if ext in FACT_EXTS and not stem.startswith("_"):` | every fact file belongs to an eval | Files starting with `_` (e.g. `_parse_day.py`) are exempt; `35.PY` or `35.py.bak` are skipped too. | 90 |
| B5 | scripts/check.py:477 | `head = read_text(root, f"{FACTS_DIR}/{name}")[:2000]` | the file carries the prompt's sha256 | The hash is looked for in the first 2000 characters only. | 85 |
| B6 | scripts/check.py:259 | `def term_patterns(terms, rep=None, substring=False):` | comment at scripts/check.py:399 says mask uses substring patterns | No caller passes `substring=True` (scripts/check.py:400): the parameter is dead and `=term` terms are masked as whole words only. Documentation (80), UX (90), category agent (90). | 90 |

### FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files |
|----------|-----------|-------|
| Uncaught exception, no report | C2, C3, C7; plus from the category agent: scripts/check.py:217 `badges = re.findall(r"badge/skill-v([0-9][0-9.]*)-", read_text(root, README, rep))`, scripts/check.py:255 `with open(path, "rb") as f:`, scripts/check.py:478 `want = hashlib.sha256(prompts[i].encode("utf-8")).hexdigest()`, scripts/check.py:476 `head = read_text(root, f"{FACTS_DIR}/{name}")[:2000]`, scripts/check.py:315 `strings = [normalize(x) for x in json_strings(json.loads(text))]` | scripts/check.py |
| Silent fallthrough | C1, C5, C8, C9, H3, B1; plus scripts/check.py:313 `if rel.endswith(".json"):`, scripts/check.py:500 `and e["id"] not in reasons:` branch (a prompt saying "(facts" is not seen), scripts/check.py:151-152 `except (OSError, subprocess.CalledProcessError):` | scripts/check.py |
| Documentation or comment says more than the code | C1 vs scripts/check.py:10, C4 vs scripts/check.py:15, scripts/check.py:43 vs :136 and :429-433, B6; plus scripts/check.py:345 `s = re.sub(r"`[^`]*`", "x", line)` against docstring 32-33 | scripts/check.py |
| Misleading messages and numbering | scripts/check.py:303 and :321 (term #k counts only usable terms); scripts/check.py:168 `rep.error(EVALS, f"not valid JSON ({e.__class__.__name__}: {e})")` also reports a missing file; scripts/check.py:172 `rep.error(EVALS, "no 'evals' list")` for an empty list; scripts/check.py:431 blames git for any failure; scripts/check.py:323 `rep.error(f"{rel}:decoded", ...` is not a line number; scripts/check.py:176 "eval #n" vs scripts/check.py:190 "id i" | scripts/check.py |
| Reported once / first hit only | scripts/check.py:129 (same not-UTF-8 error printed twice for SKILL.md via scripts/check.py:214 and :512, inflating the count); scripts/check.py:319 first match only; scripts/check.py:336 first match per pattern per line | scripts/check.py |
| Assumed environment | C4 (LF only), H6, H7, scripts/check.py:64 `SKILL = "skills/adversarial-verify/SKILL.md"` (fixed layout), scripts/check.py:332 `splitlines()` vs `chr(10)` at :321 (line numbers differ on U+2028, U+0085) | scripts/check.py |
| Fence and table parsing ignores context | C6, scripts/check.py:361 `f = re.match(r"^(`{3,}|~{3,})", s)` (indentation stripped, list-nested fences), scripts/check.py:369 (frontmatter `---` after a pipe line) | scripts/check.py |

Category agent rows with lower confidence (30-50) are listed in out/returns/Category.md; they are single-source and not independently confirmed.

## DOCUMENTATION (what the text of the file says against what it does)
| # | Location | Quote | Finding | Confidence |
|---|----------|-------|---------|------------|
| D1 | scripts/check.py:10 | `The version in SKILL.md's frontmatter matches every skill badge in the README,` | Overclaims: see C1. | 90 |
| D2 | scripts/check.py:15 | `forms; the parts of a term may be joined by anything that is not a letter or` | Overclaims: one character only, see C4; the comment at scripts/check.py:90 repeats it. | 88 |
| D3 | scripts/check.py:43 | `The folder is read as it is on disk, tracked or not, since` | True only for the default run. With --staged the folder is the checkout of the index (scripts/check.py:136, :429-433); scripts/test_check.py expects an untracked reference to be ignored. scripts/pre-commit:9 always uses --staged. | 85 |
| D4 | scripts/check.py:260 | `"""One pattern per term. By default a term matches anywhere, also inside other` | Terms that cannot be checked are skipped (scripts/check.py:267-270), so the number k in later messages no longer names the k-th configured term (blank and comment lines are dropped first too). | 85 |
| D5 | scripts/check.py:399 | `# substring patterns: when hiding output, err on the side of hiding too much` | Contradicted by scripts/check.py:400; see B6. The "never printed" claim (scripts/check.py:22-23) is partly true (C10). | 80 |
| D6 | scripts/check.py:74 | `TAGGED_FROM = 21  # evals written with the evals-first method carry [substance]/[format] tags` | The history behind 21 cannot be checked from the tree (hypothesis only). | 50 |
| D7 | scripts/check.py:13 | `CHECK_PRIVATE_TERMS (comma-separated) or the untracked file .check-private-terms` | A term containing a comma cannot be given through the variable; precedence of variable over file is not stated (H1). | 60 |

Documentation passes (31 claims decomposed, 21 passed): docstring items 1, 2 (keys), 3, 4, 6, 7, 11 (neutral wording scope), 12 (tables), 13 (facts), 14 (references), 15 (usage line matches scripts/check.py:419-421), 16 (Python 3.8 syntax; README.md:246 and 263 were not looked up, so 79), 18, 19 are as documented. Row 3 of the Documentation hypotheses (the table docstring at scripts/check.py:32-33) was discarded: its quote spans two lines and is not verbatim; the same fence defect stands as C6.

## UX (the command-line interface)
| # | Location | Quote | Finding | Confidence |
|---|----------|-------|---------|------------|
| U1 | scripts/check.py:214 | `skill = read_text(root, SKILL, rep)` | Missing input file gives a traceback, exit code 1 (same as a failure), no `ERROR path: msg` line; see C3. | 85 |
| U2 | scripts/check.py:527 | `print(f"checked ({scope}): {', '.join(rep.checked)} — {len(rep.errors)} error(s), {len(rep.warnings)} warning(s)")` | H6; hook blocks the commit with a traceback on a legacy code page. | 55 |
| U3 | scripts/check.py:436 | `if files or not args.staged:` | C9. | 70 |
| U4 | scripts/check.py:418 | `ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])` | `--help` shows one sentence; `--root` has no help (scripts/check.py:421); the term syntax and the two ways to configure terms are only in the docstring. | 75 |
| U5 | scripts/check.py:129 | `rep.error(rel, f"not UTF-8 (read as {enc})")` | Duplicate error line and inflated count (see category table). | 85 |
| U6 | scripts/check.py:319 | `m = p.search(body)` | One error per term and file, first line only: each fix needs a rerun. | 70 |
| U7 | scripts/check.py:336 | `rep.warning(f"{rel}:{ln}", f"technology-bound term {m.group(0)!r}: keep it only as one of varied examples")` | Hypothesis: many warnings may bury errors; not counted because nothing was run. | 40 |

UX passes held: errors are one line of the form `LEVEL where: msg` (scripts/check.py:106), version mismatch messages name both values (scripts/check.py:225), the stale-hash message carries the exact value to set (scripts/check.py:482), the no-terms message names both ways to configure terms (scripts/check.py:295-297), file:line locations in table errors are the right lines (scripts/check.py:373, :378).

## CROSS-DOMAIN SUMMARY
- Distinct findings: 10 FAIL rows (C1-C10), 9 hypotheses, 6 hidden behaviors, 7 failure categories. Counting each claim once in its primary domain: Code 10, Documentation 7, UX 7 listed above, of which the same defect appears in two or three domains (C1=D1, C4=D2, C3=U1, C9=U3).
- Highest risk: C2 and C3 (uncaught exceptions lose the report; the pre-commit hook then blocks without a message), C4 (a private term can leak), C9 (a run that checks nothing exits 0).
- The repository's own test (scripts/test_check.py:171) expects the behavior that scripts/check.py:223 does not have.
- Documentation outside the target: README.md:244-260 describes the checks; it was read only to establish ground truth and not verified.

## PROPOSED EXECUTABLE CHECKS (not run)
1. Run scripts/test_check.py and see whether `test_second_badge_mismatch` fails (C1).
2. Run check.py on a fixture whose evals.json has `"evals": null` and on one with `"id": [1]` (C2).
3. Run with a CRLF file containing a term broken over two lines (C4).
4. Run `check.py --staged` in an empty repository and read the exit code (C9).
5. Run it with README.md absent (C3).

Which of these should I run?
