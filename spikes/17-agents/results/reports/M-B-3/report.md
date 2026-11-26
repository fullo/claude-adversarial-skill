# Adversarial verification report: scripts/check.py, scripts/check_facts.py, scripts/pre-commit, scripts/test_check.py

## INTAKE
- **Target:** every domain detected in the four files: **Code** (check.py, check_facts.py, pre-commit), **Tests** (test_check.py and the test-like checks it drives), **Documentation** (docstrings, usage lines, comments, error messages, and the README statements they mirror). Named by the request.
- **Depth:** standard (named). **Scope:** the whole of the four files; there is no diff or history (named). **Execution mode:** reasoning only. Nothing was run (named), so every "red"/"green" below is a trace, not a run.
- **How it was produced:** 3 domain agents, 1 independent verifier (5 highest-risk claims), and 1 category agent. The coordinator looked up every returned quote at the line its row names. Returns: `out/returns/{Code,Tests,Documentation,Verifier,Category}.md`.
- **Rows:** 326 table rows came back (Code 92, Tests 93, Documentation 109, Verifier 5, Category 27); **0 discarded** (every quote was found at its line). The independent verifier **confirmed 4** of the 5 claims sent to it and **changed 1** (the `--staged` claim: PASS from three domain agents → FAIL, preventive measure, 65). The category agent found 27 instances: 22 new, 5 that repeated rows already in the report (merged).
- To change any of this (another depth, an execution mode that runs the tests, a narrower target), say so.

The full DECOMPOSED CLAIMS tables are in the returns: Code 31 claims, Tests 36, Documentation 43. Below, each finding is listed once, in its primary domain. Where a finding was reported by more than one source, all of them are named.

---

## VERIFICATION DOMAIN: Code

### GROUND TRUTH
The code of the four files, `README.md` (lines 246-263), `CHANGELOG.md`, `.claude-plugin/plugin.json`, `.gitignore`, `skills/adversarial-verify/SKILL.md`, `skills/adversarial-verify/evals/evals.json`, `skills/adversarial-verify/evals/facts/*`.

### VERIFICATION RESULTS
#### PASS ✅
| # | Claim | Evidence (path:line) | Confidence |
|---|-------|----------------------|-----------|
| 1 | evals.json: exact keys, integer ids 1..n in order, non-empty fields, tags from id 21 | scripts/check.py:180-207, `if ids != list(range(1, len(ids) + 1)):` at scripts/check.py:206 | 90 |
| 2 | Boolean ids are rejected | scripts/check.py:186 `if type(i) is not int:` | 95 |
| 3 | plugin.json version and the newest numbered CHANGELOG entry are compared | scripts/check.py:232-241; CHANGELOG.md:5 `## Unreleased` skipped, CHANGELOG.md:10 `## 4.2 - 2026-11-25` matched | 90 |
| 4 | Substring match by default, whole-word for `=` terms (detection side) | scripts/check.py:275 | 90 |
| 5 | A term with no letters or digits is an error and a short term is a warning; JSON strings are scanned after decoding | scripts/check.py:268-273, scripts/check.py:313-323 | 90 |
| 6 | Non-UTF-8 files are still scanned (UTF-16 with a BOM, else Latin-1) | scripts/check.py:114-122 | 90 |
| 7 | No terms: a warning, or an error with --strict | scripts/check.py:297 | 90 |
| 8 | Neutral wording only warns; evals.json is excluded | scripts/check.py:330-336, scripts/check.py:142 | 90 |
| 9 | Table cell counting (code spans, `\|`, outer pipes) on the traced cases | scripts/check.py:345 | 85 |
| 10 | Fact-file binding: orphan files, missing or stale hash, file and reason both, missing file or reason | scripts/check.py:478, scripts/check.py:470-501 | 85 |
| 11 | Reference files named in SKILL.md exist, and every reference file is named | scripts/check.py:519 | 90 |
| 12 | The staged temp dir is always removed | scripts/check.py:440 (in `finally`) | 90 |
| 13 | Python fact files run with sys.executable, with asserts active | scripts/check_facts.py:57 | 90 |
| 14 | `ok <id>` must be the last output line | scripts/check_facts.py:107 | 90 |
| 15 | The ids filter and --root are accepted in any order | scripts/check_facts.py:85 (but see HB 8) | 85 |
| 16 | No file selected → exit 1 | scripts/check_facts.py:113 | 95 |
| 17 | The hook captures check_facts' status | scripts/pre-commit:15 | 90 |
| 18 | The exit code is non-zero exactly when errors exist | scripts/check.py:442 | 92 (the summary is not always printed: FAIL C9) |

#### FALSIFIED HYPOTHESES
| # | Location | Suspected defect | Check (quote) | Status | Could it have failed? | Paths not covered | Mode | Confidence |
|---|----------|------------------|---------------|--------|-----------------------|-------------------|------|-----------|
| 1 | scripts/check.py:389 | `--staged` reads the working tree instead of the index | `subprocess.run(["git", "-C", root, "checkout-index", "-a", "--prefix=" + tmp + os.sep],` plus scripts/test_check.py:502-510 | conditionally falsified (by trace, not run) | test_staged_content_is_what_is_checked would go red if the working tree were read; not run | eol/smudge conversion and symlinks (FAIL C6) | Deductive | 85 |

#### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|-----------|-----|
| C1 | scripts/check.py:400 | `pats = term_patterns(terms)` | Demonstrated defect | high | `mask` builds whole-word patterns for `=` terms (no `substring=True`, despite the comment at scripts/check.py:399). With term `=acme`, the evals key `acmelabs` is printed unmasked by scripts/check.py:182; an unnamed `references/acmeplan.md` is printed unmasked by scripts/check.py:520. This breaks scripts/check.py:22-23. Found by Code F1, Documentation F1, Tests F3; **verifier confirmed (90)** | Deductive | 90 | `term_patterns(terms, substring=True)` |
| C2 | scripts/check_facts.py:92 | `print(f"skip {name}: toolchain not found")` | Demonstrated defect | high | Without rustc or node, 52.rs and 53.ts are skipped, `failed` stays 0, and the exit is 0 (scripts/check_facts.py:113). This contradicts scripts/check_facts.py:8 and README.md:254. The hook shows output only on failure (scripts/pre-commit:17), so the skip is invisible and false Rust/TS facts are committed. The skip also bypasses has_assertion (scripts/check_facts.py:95). Found by Code F3, Tests F5, Documentation F4; **verifier confirmed (95)** | Deductive | 92 | `failed += 1` with a FAIL line |
| C3 | scripts/pre-commit:9 | `"$py" -I "$root/scripts/check.py" --staged --root "$root" \|\| exit 1` | Demonstrated defect | high | `--strict` is not passed, contrary to scripts/pre-commit:5 and README.md:260 ("runs --strict --staged"). With no terms configured, scripts/check.py:297 only warns and the commit goes through unchecked. Found by Code F2, Tests F4, Documentation F5; **verifier confirmed (95)** | Deductive | 92 | Add `--strict` |
| C4 | scripts/check.py:90 | `SEP = r"[\W_]?"  # anything that is not a letter or digit, possibly nothing` | Demonstrated defect | high | At most one separator character is allowed: two spaces, ` - `, CRLF, or a line break plus indentation between the parts of a term are not matched. This contradicts scripts/check.py:16-17. Found by Code F4, Tests F2, Documentation F2; **verifier confirmed (92)** | Deductive | 90 | `[\W_]*` |
| C5 | scripts/check.py:223 | `for b in badges[:1]:` | Demonstrated defect | medium | Only the first README badge is compared; a stale second badge passes. This contradicts scripts/check.py:10 and README.md:249. Found by Code F5, Tests F1, Documentation F3 | Deductive | 90 | `for b in badges:` |
| C6 | scripts/check.py:389 | `subprocess.run(["git", "-C", root, "checkout-index", "-a", "--prefix=" + tmp + os.sep],` | Preventive measure | medium | **Verdicts disagree.** The domain agents gave PASS: Code 85, Documentation 85, Tests 82 ("index content goes to tmp"). The independent verifier gave FAIL, preventive measure, 65: checkout-index writes the working-tree form of each blob (core.autocrlf, smudge/ident filters, working-tree-encoding), and symlinks are followed (scripts/check.py:126). The bytes checked can therefore differ from the staged bytes. For example, a staged LF `Acme\nCorp` is checked as `Acme\r\nCorp`, which C4 misses. Depends on git behavior that was not run | Deductive | 65 | Read blobs with `git cat-file`/`ls-files -s`, or pass `--no-filters`-equivalent |
| C7 | scripts/check.py:473 | `with_file[int(stem)] = name` | Preventive measure | low | If `38.py` and `38.rs` both exist, only one of them is hash-checked (Code F10) | Deductive | 85 | Error on a second file for the same id |
| C8 | scripts/check.py:341 | `DELIM = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")` | Preventive measure | low | A bare `---` after a piped line is taken for a delimiter; `\|-\|-\|` delimiters are never recognised; any fence line closes any fence (scripts/check.py:366). Found by Code F11, Tests F17, Documentation HB4 | Deductive | 80 | Require a pipe, accept `-{1,}`, close a fence only with the same character |
| C9 | scripts/check.py:227 | `plugin = json.loads(read_text(root, PLUGIN, rep))` | Preventive measure | low | Only ValueError is caught (scripts/check.py:228). A missing plugin.json, README, CHANGELOG or SKILL.md gives a traceback, no summary, and the collected errors are never printed. Found by Code F12, Documentation HB7, Category 8 | Deductive | 85 | Catch OSError and report it |
| C10 | scripts/check_facts.py:100 | `r = subprocess.run(step, cwd=FACTS, capture_output=True, text=True)` | Preventive measure | low | No timeout: a looping fact file hangs the hook (Code F13) | Deductive | 80 | `timeout=` → FAIL |
| C11 | scripts/check_facts.py:100 | `r = subprocess.run(step, cwd=FACTS, capture_output=True, text=True)` | Demonstrated defect | low | With a relative `--root .`, `path` is relative to the caller but the run uses cwd=FACTS, so true facts FAIL (Tests F18) | Deductive | 82 | `FACTS = os.path.abspath(...)` |
| C12 | scripts/check_facts.py:37 | `".rs": re.compile(r'//[^\n]*\|/\*.*?\*/\|"(?:\\.\|[^"\\])*"', re.S),` | Preventive measure | low | A char literal `'"'` or a raw string `r#"..."#` mis-strips the code, hiding or inventing an assertion. Found by Code F14, Documentation H4/H5 | Deductive | 80 | Strip char literals and raw strings first |
| C13 | scripts/pre-commit:12 | `if git diff --cached --name-only \| grep -q '^skills/adversarial-verify/evals/'; then` | Preventive measure | low | A commit that changes only scripts/check_facts.py never runs the facts, and quoted non-ASCII paths don't match `^skills`. Found by Code F15, Tests F14 | Deductive | 85 | Also match `^scripts/check_facts.py`; use `-z` |
| C14 | scripts/check.py:95 | `text = "".join(c for c in text if not unicodedata.combining(c))` | Demonstrated defect | medium | ø, ł, đ, æ, œ have no NFKD decomposition: the term `Bjorn` misses `Bjørn`. This contradicts "ignores accents" (scripts/check.py:15) (Category 1) | Deductive | 85 | Add a transliteration table for the non-decomposing letters |
| C15 | scripts/check.py:255 | `terms = [l for l in decode(f.read())[0].splitlines() if not l.strip().startswith("#")]` | Demonstrated defect | medium | The line `acme  # client` becomes the term `acme…client`, so `acme` is silently not checked (Category 3) | Deductive | 80 | Strip trailing `#` comments, or error on them |
| C16 | scripts/check.py:316 | `except ValueError:` | Demonstrated defect | medium | A `.json` that is not strict JSON (comments, trailing comma) is not decoded and gives no warning, so `\uXXXX`-escaped terms in it are missed. This contradicts scripts/check.py:20-21 (Category 5) | Deductive | 85 | Warn when a .json cannot be decoded |
| C17 | scripts/check.py:500 | `if "(Facts" in str(e.get("prompt", "")) and e["id"] not in with_file and e["id"] not in reasons:` | Demonstrated defect | medium | Case-sensitive substring: `(facts:` or `[Facts]` exempts an eval from the fact-file rule silently (Category 20) | Deductive | 85 | Case-insensitive pattern |
| C18 | scripts/check.py:345 | ``s = re.sub(r"`[^`]*`", "x", line).replace("\\|", "x").strip()`` | Demonstrated defect | medium | GFM splits cells at an unescaped pipe inside a code span; the check counts one cell, and scripts/test_check.py:441-443 locks that in (Category 23) | Deductive | 80 | Count unescaped pipes even inside code spans |
| C19 | scripts/check.py:477 | `m = re.search(r"prompt-sha256:\s*([0-9a-f]{64})", head)` | Preventive measure | low | Only the first hash in the first 2000 characters is read (Category 2) | Deductive | 70 | Bind every hash line |
| C20 | scripts/check.py:114 | `if data.startswith((b"\xff\xfe", b"\xfe\xff")):` | Preventive measure | low | UTF-32-LE decodes as UTF-16 with NULs and every term is missed, with no error (Category 6) | Deductive | 70 | Detect UTF-32 BOMs |
| C21 | scripts/check_facts.py:49 | `return True  # let the run report the syntax error` | Preventive measure | medium | A BOM in a .py fact file may make ast.parse fail, so the file counts as asserting; whether it does depends on the version (run-only) (Category 7) | Deductive | 55 | Read with utf-8-sig |
| C22 | scripts/check.py:524 | `for line in mask(rep.errors + rep.warnings, terms):` | Preventive measure | low | Tracebacks on stderr are never masked and can print a path that contains a term (Category 9) | Deductive | 65 | Catch exceptions in main and mask them |
| C23 | scripts/check.py:391 | `out = subprocess.run(["git", "-C", root, "ls-files", "-z"], capture_output=True, check=True)` | Preventive measure | low | In a sparse checkout, ls-files lists files that checkout-index skipped, so they are reported unreadable or crash the run (Category 10) | Deductive | 55 | List only checked-out entries |
| C24 | scripts/check.py:527 | `print(f"checked ({scope}): {', '.join(rep.checked)} — {len(rep.errors)} error(s), {len(rep.warnings)} warning(s)")` | Preventive measure | low | The em dash may fail to encode on a Windows pipe with a non-UTF-8 code page (run-only) (Category 11) | Deductive | 50 | Use ASCII, or reconfigure stdout |
| C25 | scripts/check.py:237 | `first = re.search(r"^## +([0-9][0-9.]*)\b", read_text(root, CHANGELOG, rep), re.M)` | Preventive measure | low | `## v4.3` or `## [4.3]` is skipped and an older entry is compared (Category 21) | Deductive | 80 | Accept `v` and `[` |
| C26 | scripts/check.py:216 | `m = re.search(r'^\s*version:\s*"?([0-9][0-9.]*)"?\s*$', fm.group(1), re.M) if fm else None` | Preventive measure | low | The first `version:` line at any indentation wins (Category 22) | Deductive | 65 | Anchor to `metadata.version` |
| C27 | scripts/check.py:375 | `while i < len(lines) and lines[i].strip() and "\|" in lines[i]:` | Preventive measure | low | A row with no pipe ends the table early; GFM still renders it as a row (Category 24) | Deductive | 75 | End only at a blank line or another block |
| C28 | scripts/check.py:85 | `r"Laravel", r"Django", r"Rails", r"Spring", r"React", r"Angular", r"Vue",` | Preventive measure | low | No word boundaries and case-sensitive: false warnings (`Reaction`) and misses (`react`) (Category 25) | Deductive | 80 | `\b` and IGNORECASE |
| C29 | scripts/check.py:126 | `with open(os.path.join(root, rel), "rb") as f:` | Preventive measure | medium | A tracked symlink is scanned through its target, never as its committed link text (Category 26) | Deductive | 75 | `os.readlink` for links |
| C30 | scripts/check.py:465 | `files = sorted(os.listdir(fdir)) if os.path.isdir(fdir) else []` | Preventive measure | low | Untracked fact files satisfy check 6 on a working-tree run (Category 27) | Deductive | 80 | Use the tracked file list |
| C31 | scripts/check.py:248 | `if raw is not None:` | Preventive measure | low | A set CHECK_PRIVATE_TERMS, even an empty one, silently overrides .check-private-terms. Found by Documentation HB1, Category 4 | Deductive | 88 | Merge both sources, or say which one is used |

### HYPOTHESES
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| 1 | scripts/pre-commit:7-8 `py=python3` | On Windows, the Store `python3` stub, or a missing python3, blocks every commit | Git for Windows finds a working python | Run the hook on Windows with only `py` installed |
| 2 | scripts/pre-commit:14 POSIX `$tmp` passed to a native Python | MSYS path conversion makes it work | check_facts crashes at `os.listdir` | Run the hook in Git for Windows on a commit that touches evals/ |
| 3 | scripts/check.py:392 every checkout-index error becomes "not a git repository" | A merge conflict or submodule gives a misleading error or blocks commits | checkout-index exits 0 | Run `--staged` with an unmerged path or a submodule |
| 4 | scripts/check_facts.py:62 `.bin` exe name on Windows | CreateProcess runs it anyway | FAIL 52.rs | Run `check_facts.py 52` on Windows |
| 5 | scripts/check_facts.py:100 locale decoding | Non-ASCII fact output crashes on Windows | Facts print ASCII only | A fact file printing a non-cp1252 character |
| 6 | scripts/check.py:389 backslash prefix on Windows | git accepts it | `--staged` breaks on Windows | `py -3 scripts/check.py --staged` on Windows |

### HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type | Confidence |
|---|----------|-----------|--------|------|-----------|
| 1 | scripts/check.py:301 `if os.path.basename(rel) == TERMS_FILE:` | The terms file is untracked | Any file with that name at any depth is skipped, so a force-added list is committed unreported | Preventive measure, medium | 88 |
| 2 | scripts/check.py:149 `if files:` | Walk only when git is unavailable | Also walks when root is not a repo or nothing is tracked | — | 88 |
| 3 | scripts/check.py:436 `if files or not args.staged:` | --staged checks the staged content | Empty index: no check runs, exit 0 | Preventive measure, low | 85 |
| 4 | scripts/check.py:75 `TAG_RE = ...\s+\S` | Tag "followed by text" | `[format]text` (no space) is rejected | — | 90 |
| 5 | scripts/check.py:469 `not stem.startswith("_")` | Every fact file belongs to an eval | `_`-prefixed helpers are exempt (undocumented) | — | 90 |
| 6 | scripts/check.py:494 `reasons[int(m.group(1))] = m.group(2)` | Reasons for evals that state facts | Reasons for nonexistent ids, or ids below 29, are accepted; duplicates overwrite | Preventive measure, low | 85 |
| 7 | scripts/check.py:193 `rep.error(where, f"empty {key}")` | Empty field | A non-string value is called "empty" | — | 90 |
| 8 | scripts/check_facts.py:85 `files = [f for f in files if ...]` | Only these ids | Unknown ids are dropped silently (`38 9999` exits 0) | Preventive measure, low | 90 |
| 9 | scripts/check_facts.py:50 `ast.Assert, ast.Raise` | A file that asserts nothing fails | An assert in dead code counts | Preventive measure, low | 85 |
| 10 | scripts/check_facts.py:63 `"-O"` | Facts are reproduced | Release mode disables overflow panics | Preventive measure, low | 80 |
| 11 | scripts/check_facts.py:112 summary line | Run summary | Skipped files are counted with "0 failed" (part of C2) | Demonstrated defect, low | 90 |
| 12 | scripts/pre-commit:9 and scripts/pre-commit:15 | "exactly what is staged" | The working-tree checker scripts run, not the staged ones | Preventive measure, low | 85 |

### FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Advertised-contract drift | C1, C2, C3, C4, C5, C14, C16 | scripts/check.py, scripts/check_facts.py, scripts/pre-commit |
| Silent fallthrough | C2, C15, C16, C20, C21, C31, HB 3, HB 6, HB 8 | scripts/check.py, scripts/check_facts.py, scripts/pre-commit |
| Missing completeness | C7, C9, C13, C22, C23, HB 1 | scripts/check.py, scripts/pre-commit |
| Assumed environment | C4 (CRLF), C11, C24, H1-H6 | all three code files |
| Lexical heuristics standing in for parsing | C8, C12, C17, C18, C25, C26, C27, C28, HB 9 | scripts/check.py, scripts/check_facts.py |
| Checked artifact differs from the committed one | C6, C29, C30, HB 12 | scripts/check.py, scripts/pre-commit |

---

## VERIFICATION DOMAIN: Tests

### GROUND TRUTH
scripts/test_check.py against scripts/check.py, scripts/check_facts.py and the fixtures it edits: `skills/adversarial-verify/SKILL.md:207`, `.claude-plugin/plugin.json:2`, `.claude-plugin/plugin.json:4`, `skills/adversarial-verify/evals/evals.json:269`, `skills/adversarial-verify/evals/evals.json:462-463`, `skills/adversarial-verify/evals/facts/38.py:21`, `skills/adversarial-verify/evals/facts/40.py:13`, `skills/adversarial-verify/evals/facts/49.py:12-14`, `skills/adversarial-verify/evals/facts/NOT_COMPUTABLE:4`.

### VERIFICATION RESULTS
#### PASS ✅
| # | Claim | Evidence (path:line) | Confidence |
|---|-------|----------------------|-----------|
| 1 | assert_fails is not tautological (return code, summary, ERROR, tokens, leak check) | scripts/test_check.py:57-62 | 90 |
| 2 | The TAGGED_FROM boundary is pinned on both sides | scripts/test_check.py:149-159; evals.json:269 (eval 20 untagged) | 85 |
| 3 | A prompt edited after its facts fails the hash check | scripts/test_check.py:550-552; evals.json:462 is id 37 | 85 |
| 4 | A false fact makes the runner fail | scripts/test_check.py:582-585; facts/38.py:21 | 85 |
| 5 | A fact file with no assertion fails (Python) | scripts/test_check.py:588-593; facts/49.py:12-14 | 85 |
| 6 | Python comments and strings don't count as assertions | scripts/check_facts.py:50 | 85 |
| 7 | A missing ok line fails | scripts/test_check.py:610-613; facts/40.py:13 | 85 |
| 8 | Facts with no file and no reason fail | scripts/test_check.py:525-526; NOT_COMPUTABLE:4 | 85 |
| 9 | The newest CHANGELOG entry is the one compared | scripts/test_check.py:224; scripts/check.py:237 | 85 |
| 10 | Untracked files are not checked (git path) | scripts/test_check.py:398-402; scripts/check.py:147 | 82 |
| 11 | Test terms are absent from the repo | scripts/test_check.py:24-26 (grep for the fragments found nothing) | 70 |
| 12 | Whole-word opt-in avoids false positives | scripts/test_check.py:262; scripts/check.py:275 | 82 |
| 13 | Table edits hit a real row (`edit` asserts the anchor) | scripts/test_check.py:80; SKILL.md:207 | 85 |
| 14 | JSON-escaped terms are caught in keys and values | scripts/test_check.py:304-316; scripts/check.py:322-323 | 85 |
| 15 | The terms file is gitignored | scripts/test_check.py:366; .gitignore:1 | 95 |
| 16 | evals.json is excluded from neutral wording | scripts/test_check.py:413-417; scripts/check.py:142 | 82 |

#### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|-----------|-----|
| T1 | scripts/test_check.py:171 | `def test_second_badge_mismatch(self):` | Demonstrated defect | medium | By trace, three tests are red on the current code: scripts/test_check.py:171-173 (C5), the two-space variant at scripts/test_check.py:286 (C4), and scripts/test_check.py:341-344 (C1). The suite contradicts scripts/test_check.py:1. Found by Code F6; Tests H2; Documentation H1-H3 | Deductive | 75 (run-only) | Fix C1, C4, C5; keep the tests |
| T2 | scripts/test_check.py:479 | `self.assertIn("orphan.md", r.stdout + self.ref("orphan.md"))` | Demonstrated defect | medium | Tautology: the haystack always contains "orphan.md", so the test stays green if check 7 is deleted. Found by Code F7, Tests F6, Documentation F8 | Deductive | 92 | `self.assert_fails(r, "orphan.md", "never named in SKILL.md")` |
| T3 | scripts/test_check.py:43 | `env = dict(os.environ)` | Preventive measure (Tests: demonstrated; Code: preventive. Kept preventive: it depends on the developer's env) | medium | An exported CHECK_PRIVATE_TERMS is inherited: tests 354-363 go false red, and tests 318-329 test the env var instead of the file. Found by Code F8, Tests F7 | Deductive | 85 | `env.pop("CHECK_PRIVATE_TERMS", None)` |
| T4 | scripts/test_check.py:578 | `self.assertRegex(r.stdout, r"\d+ fact file\(s\), 0 failed")` | Preventive measure (Tests: demonstrated) | medium | Green without rustc or node while 52.rs and 53.ts never ran (C2). Found by Code F9, Tests F8, Documentation H8 | Deductive | 85 | Assert no `skip` line; add a test with PATH stripped |
| T5 | scripts/test_check.py:337 | `# whole-word detection does not flag "<term>labs", but the evals check prints the key name` | Demonstrated defect | low | The test uses `terms=T1` (substring), so it duplicates scripts/test_check.py:331 and does not exercise its stated case. Found by Tests F9, Documentation F9 | Deductive | 85 | Use `"=" + T1`, or delete it |
| T6 | scripts/test_check.py:503 | `git = lambda *a: subprocess.run(["git", "-C", self.tmp, "-c", "user.name=t", "-c", "user.email=t@t", *a],` | Demonstrated defect | low | No skipUnless(git) guard, unlike scripts/test_check.py:369; without git the test errors instead of skipping (Tests F10) | Deductive | 85 | Add the guard |
| T7 | scripts/test_check.py:84 | `with open(self.path(rel), "a", encoding="utf-8") as f:` | Demonstrated defect | medium | Text mode writes `\r\n` on Windows: the `\n` variant at scripts/test_check.py:286 is red on Windows and green on POSIX, so POSIX never covers CRLF files. Found by Category 12, Code F6, Tests F2 | Deductive | 85 | Write with `newline=""`, plus an explicit CRLF variant |
| T8 | scripts/test_check.py:320 | `r = self.run_check(terms_file=("﻿" + f"{T1}\n# a comment\n").encode("utf-8"))` | Demonstrated defect | low | Passes with or without BOM handling: U+FEFF is dropped by scripts/check.py:266 anyway (Category 15) | Deductive | 85 | Put the BOM before a term that only fails when the BOM is kept |
| T9 | scripts/test_check.py:605 | `r = self.run_facts("49", "--root", self.tmp)` | Demonstrated defect | low | The script's default ROOT is already self.tmp, so a `--root` that is ignored still passes (Category 17) | Deductive | 85 | Run with a different root |
| T10 | scripts/test_check.py:595 | `def test_runner_ignores_assertions_in_comments(self):` | Preventive measure | medium | Only the Python (AST) path is tested; the Rust/TS stripping (scripts/check_facts.py:34-39) is never exercised. Found by Tests F13, Category 19 | Deductive | 80 | Add .rs/.ts cases |
| T11 | scripts/pre-commit:9 | `"$py" -I "$root/scripts/check.py" --staged --root "$root" \|\| exit 1` | Preventive measure | medium | No test runs the hook, which is why C3 goes uncaught (Tests F14) | Deductive | 80 | A temp-repo test that commits with no terms |
| T12 | scripts/test_check.py:617 | `self.assertNotEqual(r.returncode, 0, r.stdout)` | Preventive measure | low | A crash would also pass (Tests F15) | Deductive | 80 | Assert `0 fact file(s)` |
| T13 | scripts/check.py:77 | `FACTS_FROM = 29  # from here on, an eval that states facts needs a fact file or a reason` | Preventive measure | low | No test pins the 28/29 boundary (Tests F16) | Deductive | 75 | Boundary tests |
| T14 | scripts/test_check.py:302 | `self.assert_fails(self.run_check(terms=T1), "notes16.txt")` | Preventive measure | low | Any error naming the file passes; the same at scripts/test_check.py:316 (Code F16) | Deductive | 85 | Also assert `private term #1` |
| T15 | scripts/test_check.py:64 | `def assert_passes(self, r):` | Preventive measure | low | assert_no_leak runs only in assert_fails, so passing runs are never checked for leaks, contrary to scripts/test_check.py:4-5. Found by Documentation F8, Category 18 | Deductive | 75 | Call assert_no_leak in assert_passes |
| T16 | scripts/test_check.py:351 | `os.symlink(os.path.join(self.tmp, "does-not-exist"), self.path("dangling.md"))` | Preventive measure | low | On Windows without symlink rights the test errors (false red). Found by Tests F11, Code H5 | Abductive | 65 | Skip on OSError |
| T17 | scripts/test_check.py:390 | `shutil.rmtree(self.path(".git"))` | Preventive measure | low | Read-only git objects on Windows give PermissionError (Tests F12) | Abductive | 60 | An onerror handler |
| T18 | scripts/test_check.py:106 | `open(self.path(EVALS), "a").write("{")` | Preventive measure | low | Unclosed writes rely on CPython refcounting to flush; the same at :293, :297, :301, :383, :385, :400, :544, :559, :564, :599 (Category 13) | Deductive | 65 | Use `with` |
| T19 | scripts/test_check.py:32 | `for item in ("README.md", "CHANGELOG.md", "skills", ".claude-plugin", "scripts", ".gitignore"):` | Preventive measure | low | The fixture copies untracked files into a non-repo dir: Base tests use only the os.walk path, and results vary by machine (Category 14) | Deductive | 75 | Copy only `git ls-files` |
| T20 | scripts/test_check.py:297 | `open(self.path("notes.txt"), "wb").write(f"caf\xe9 {T1}\n".encode("latin-1"))` | Preventive measure | low | An ASCII term is found by any lossy decode, so the Latin-1 fallback is not shown (Category 16) | Deductive | 65 | Use a non-ASCII term |

### HYPOTHESES
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| 1 | scripts/test_check.py:98 baseline | The repo passes today | Some check errors | `python3 -m unittest scripts.test_check.RepoTest` |
| 2 | scripts/test_check.py:380 global git config inherited | gpgsign or global hooks make setUp fail | No such config | Run with `GIT_CONFIG_GLOBAL` set to a gpgsign config |
| 3 | scripts/test_check.py:390-393 temp dir inside a repo | The test is false red | Temp is outside any repo | TMPDIR inside a git repo |
| 4 | scripts/test_check.py:395 shared temp scan | Flaky under parallel runs | Serial runs | Two concurrent suites |

### HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type | Confidence |
|---|----------|-----------|--------|------|-----------|
| 1 | scripts/test_check.py:572 | "Tests for scripts/check.py" (scripts/test_check.py:1) | Also tests check_facts.py (FactsTest) | — | 90 |

### FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Test-environment artifact | T3, T4, T7, T16, T17, T18, T19, H2, H3, H4 | scripts/test_check.py |
| Tautological or weak assertion | T2, T8, T9, T12, T14, T20 | scripts/test_check.py |
| Test-code drift | T1, T5, T15 | scripts/test_check.py |
| Missing completeness (untested paths) | T6, T10, T11, T13 | scripts/test_check.py, scripts/pre-commit, scripts/check.py |

---

## VERIFICATION DOMAIN: Documentation

### GROUND TRUTH
The docstrings of scripts/check.py:2-51 and scripts/check_facts.py:2-19, comments in scripts/pre-commit:2-11 and scripts/test_check.py, the error messages in scripts/check.py, and README.md:246-263.

### VERIFICATION RESULTS
#### PASS ✅
The 29 PASS rows are in `out/returns/Documentation.md`, minus its row 13, which moved to C6. They hold at 70-95 and cover: exit codes (scripts/check.py:4), check 1 (scripts/check.py:6), plugin/CHANGELOG (scripts/check.py:11), term sources (scripts/check.py:14), normalization (scripts/check.py:15, but see C14), the `=` semantics (scripts/check.py:18), term warnings (scripts/check.py:20), encodings (scripts/check.py:21), strict mode (scripts/check.py:23), neutral wording (scripts/check.py:27), tables (scripts/check.py:30), facts (scripts/check.py:34), the usage lines (scripts/check.py:49, scripts/check_facts.py:17), Python 3.8 (scripts/check.py:50, 70), the bool comment (scripts/check.py:186), scripts/check.py:462, the runner docstrings (scripts/check_facts.py:2, :6, :11), the hook install line (scripts/pre-commit:3, 80), the facts trigger (scripts/pre-commit:10), the test docstrings and comments (scripts/test_check.py:1, :3, :23, :158, :221, :332, :581).

#### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|-----------|-----|
| D1 | scripts/check.py:43 | `reader nowhere. The folder is read as it is on disk, tracked or not, since` | Demonstrated defect | low | With --staged (the hook's mode), references/ is read from the index copy, so an untracked orphan is not reported. scripts/test_check.py:508 asserts that it passes (Documentation F6) | Deductive | 85 | State the --staged exception |
| D2 | scripts/check.py:168 | `rep.error(EVALS, f"not valid JSON ({e.__class__.__name__}: {e})")` | Demonstrated defect | low | A missing or unreadable evals.json is reported as "not valid JSON" (Documentation F7) | Deductive | 85 | Separate `except OSError` |

The documentation sides of C1 (scripts/check.py:22, scripts/check.py:399), C2 (scripts/check_facts.py:8, README.md:254), C3 (scripts/pre-commit:5, README.md:260), C4 (scripts/check.py:16), C5 (scripts/check.py:10, README.md:249) and T5 (scripts/test_check.py:337) are counted once, in their primary domain. Each fix either repairs the code or rewords the text; the code fix is the one recommended.

### FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Doc-code drift | D1, D2, and the documentation sides of C1-C5, T5 | all four files |

---

## CROSS-DOMAIN SUMMARY
- Domains: Code, Tests, Documentation.
- Claims: 110 decomposed (Code 31, Tests 36, Documentation 43). PASS: Code 18, Tests 16, Documentation 29 (each after C6 was moved out). FAIL: 53 (Code 31, Tests 20, Documentation 2). Falsified: 1 (conditionally).
- Findings by type: **20 demonstrated defects** (Code 11, Tests 7, Documentation 2), **33 preventive measures**, 1 falsified hypothesis (conditionally).
- Critical issues: 0 rated critical. **4 high:** C1 (private term printed unmasked), C2 (missing toolchain silently skipped), C3 (hook without --strict), C4 (separator of at most one character). The independent verifier confirmed all four.
- Changes that touch several domains: C1, C2, C3, C4 and C5 are each a docstring or README promise (Documentation) that the code breaks (Code), and that a test encodes and would show red, or doesn't test (Tests: T1, T4, T11).
- Hypotheses: 10 requiring further investigation. Hidden behaviors: 13.
- Failure categories: 9 systemic patterns (advertised-contract drift, silent fallthrough, missing completeness, assumed environment, lexical heuristics, checked artifact ≠ committed one, test-environment artifact, weak assertions, test-code drift).
- Invariants, stress tests, adversarial scaffold: not requested of the agents (the protocol's return format). Not reported.
- Executed: none (reasoning only). Pre-code: not applicable.
- Rows: 326 came back, 0 discarded. The verifier confirmed 4 and changed 1 (C6). The category agent added 22 new rows and repeated 5 known ones (merged).
- Recommendation: do not trust the pre-commit hook as a privacy gate until C1, C3 and C4 are fixed, or the fact runner until C2 is fixed. The test suite already encodes C1, C4 and C5 and would show them red.

## PROPOSED EXECUTABLE CHECKS
| # | Claim | Confidence now | Check | Confirms if | Refutes if | Cost and side effects | Status |
|---|-------|----------------|-------|-------------|------------|-----------------------|--------|
| 1 | T1: three tests are red (C1, C4, C5) | 75 | `python3 -m unittest scripts/test_check.py` from ./tree | test_second_badge_mismatch, test_two_words_joined_any_way and test_whole_word_term_glued_in_output_is_still_masked fail | they pass | Runs check.py in temp copies, with git init in temp dirs; writes only under the system temp dir | proposed |
| 2 | C2: a missing toolchain is silently skipped | 92 | `PATH=<python only> python3 scripts/check_facts.py; echo $?` | prints `skip 52.rs`/`skip 53.ts` and exits 0 | exit 1 | Runs the .py fact files; reads only | proposed |
| 3 | C6: --staged checks converted bytes | 65 | In a temp repo with `core.autocrlf=true`, stage an LF file containing `term\nparts` and run `check.py --staged` with that two-word term | not reported | reported | Temp repo only | proposed |
| 4 | C21: a BOM .py fact counts as asserting | 55 | `ast.parse("﻿x = 1")` on the target Python | SyntaxError | parses | Reads nothing | proposed |
| 5 | C24: the em dash on a Windows pipe | 50 | On Windows, `py -3 scripts/check.py \| more` with a cp932 console | UnicodeEncodeError | summary printed | Read-only run | proposed |

Proposed writes: the fixes in the Fix column of C1-C5, T2, T3 and T5, in scripts/check.py, scripts/check_facts.py, scripts/pre-commit and scripts/test_check.py. If the code is not changed, then README.md:249, README.md:254 and README.md:260 need rewording to match it.

**Shall I run any of checks 1-5 above, or write any of the proposed fixes?**
