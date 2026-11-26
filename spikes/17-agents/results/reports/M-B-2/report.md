# Adversarial verification report: scripts/check.py, scripts/check_facts.py, scripts/pre-commit, scripts/test_check.py

All locations are `path:line`, relative to `./tree`.

## INTAKE
- **Target:** every domain detected in the four files: **Code**, **Tests**, **Data**, **Documentation**. Set by the request.
- **Depth:** standard. Set by the request.
- **Scope:** the whole of the four files. There is no diff and no history. Set by the request.
- **Execution mode:** reasoning only, nothing run. Set by the request. Every result below comes from tracing code. Any claim about a test going red or green is a prediction, capped at 79.
- **How to change these:** name other domains or files, ask for the `deep` depth, or approve the checks under PROPOSED EXECUTABLE CHECKS.
- **Process:** 4 domain agents, 1 resend, 1 independent verifier on the 5 highest-risk claims, 1 category agent. The coordinator looked up every quote returned.
  - **Rows:** 417 came back. 2 were discarded on lookup, both from Tests, and both came back corrected on resend, so 0 were dropped.
  - **Independent verifier:** confirmed 4 of the 5 claims and changed 1 (claim 5, `--staged`: PASS → FAIL, preventive, 70).
  - No PASS needed lowering for a missing lookup: every PASS quote was looked up.

---

## DOMAIN: CODE

### VERIFICATION DOMAIN
Code. The primary domain for the logic of `scripts/check.py`, `scripts/check_facts.py` and `scripts/pre-commit`.

### GROUND TRUTH
- The code itself.
- README.md:249-260 and CHANGELOG.md:5-10.
- .claude-plugin/plugin.json:3 and skills/adversarial-verify/evals/evals.json.
- The files in skills/adversarial-verify/evals/facts/*.

### INVARIANTS
Not requested from the domain agents: the protocol limits their returns to six sections. The invariants the code states in its own docstring are covered as claims (scripts/check.py:4-50).

### DECOMPOSED CLAIMS
The full list of 39 claims is in out/returns/Code.md. The main ones:
1. Bool and non-integer eval ids are rejected (scripts/check.py:186). Deductive.
2. Eval ids run 1..n in order, and duplicates are reported (scripts/check.py:206). Deductive.
3. The version matches every README badge (scripts/check.py:10). Deductive.
4. The parts of a term can be joined by anything that is not a letter or digit (scripts/check.py:16). Deductive.
5. Terms are never printed (scripts/check.py:22). Deductive.
6. `--staged` checks exactly the staged content (scripts/check.py:47). Deductive.
7. A missing toolchain is an error (scripts/check_facts.py:8). Deductive.
8. The hook checks what is staged and runs `--strict` (scripts/pre-commit:2, scripts/pre-commit:5). Deductive.
9. A fact run always terminates (scripts/check_facts.py:100). Abductive.

### FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|----------------|
| Silent fallthrough | scripts/check_facts.py:92, scripts/pre-commit:15/17, scripts/check.py:436, scripts/check.py:151, scripts/check.py:316, scripts/check_facts.py:85 | check_facts.py, pre-commit, check.py |
| Missing completeness (contract partly implemented) | scripts/check.py:223, scripts/check.py:90, scripts/check.py:400, scripts/check.py:473, scripts/check.py:361/363 | check.py |
| Uncaught error path (traceback, report lost, output unmasked) | scripts/check.py:214, scripts/check.py:217, scripts/check.py:228, scripts/check.py:332, scripts/check.py:463, scripts/check.py:470, scripts/check.py:476, scripts/check_facts.py:43, scripts/check_facts.py:83 | check.py, check_facts.py |
| Assumed environment | scripts/check.py:90 (CRLF), scripts/check_facts.py:67, scripts/check_facts.py:100, scripts/pre-commit:8, scripts/check.py:525 | all three |
| Stale state (working-tree checker or converted copy instead of staged) | scripts/pre-commit:9, scripts/pre-commit:15, scripts/check.py:389, scripts/pre-commit:14 | pre-commit, check.py |

### VERIFICATION RESULTS
#### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| 1 | Bool ids rejected | scripts/check.py:186 `if type(i) is not int:  # bool is an int subclass: reject it`. Deductive, 92 |
| 2 | Ids are consecutive and duplicates are reported | scripts/check.py:203 `dups = sorted({i for i in ids if ids.count(i) > 1})` and scripts/check.py:206 `if ids != list(range(1, len(ids) + 1)):`. 90 |
| 3 | Tags required from eval 21 | scripts/check.py:75 `TAG_RE = re.compile(r"^\[(substance\|format)\]\s+\S")` and scripts/check.py:201 `elif i >= TAGGED_FROM and not TAG_RE.match(a):`. 90 |
| 4 | Only the newest numbered CHANGELOG entry counts | scripts/check.py:237 `first = re.search(r"^## +([0-9][0-9.]*)\b", ...)`. `## Unreleased` is skipped because it has no digit. 88 |
| 5 | `=` terms match whole words only | scripts/check.py:275 `pats.append(re.compile(rf"(?<![^\W_]){body}(?![^\W_])" if whole_word else body))`. 88 |
| 6 | Files that are not UTF-8 are still scanned | scripts/check.py:114 `if data.startswith((b"\xff\xfe", b"\xfe\xff")):` … scripts/check.py:122 `return data.decode("latin-1"), "latin-1"`. Latin-1 never raises. 90 |
| 7 | JSON strings are scanned after their escapes are decoded | scripts/check.py:315 `strings = [normalize(x) for x in json_strings(json.loads(text))]` and scripts/check.py:322 `elif any(p.search(x) for x in strings):`. 88. Exception: invalid JSON skips the decoded scan (see FAIL 14). |
| 8 | Without terms the check says so, and `--strict` makes it fail | scripts/check.py:297 `(rep.error if strict else rep.warning)("private terms", msg)`. 90 |
| 9 | Escaped pipes and pipes in code spans are not cell separators | scripts/check.py:345 ``s = re.sub(r"`[^`]*`", "x", line).replace("\\|", "x").strip()``. 85 |
| 10 | Each fact file is bound to its prompt hash, and an eval cannot have both a file and a reason | scripts/check.py:478 `want = hashlib.sha256(prompts[i].encode("utf-8")).hexdigest()`, scripts/check.py:481 `elif m.group(1) != want:`, scripts/check.py:495. 88. Holds for one file per eval only (FAIL 10). |
| 11 | Orphan fact files are reported | scripts/check.py:470 `if not stem.isdigit() or int(stem) not in ids:`. 88 |
| 12 | Every named reference exists, and every reference file is named | scripts/check.py:517 `if name not in existing:` and scripts/check.py:519 `for name in sorted(existing - named_in_skill):`. 88 |
| 13 | Errors give a non-zero exit, and the temp dir is removed | scripts/check.py:442 `return 1 if rep.errors else 0` and scripts/check.py:438 `finally:`. 88, except on uncaught exceptions (FAIL 6). |
| 14 | The last output line must be `ok <id>` | scripts/check_facts.py:107 `if out[-1:] != [f"ok {stem}"]:`. 90 |
| 15 | The runner fails when no file is selected | scripts/check_facts.py:113 `return 1 if failed or not files else 0`. 92 |
| 16 | The hook captures the runner's exit status | scripts/pre-commit:15 `out="$("$py" -I "$root/scripts/check_facts.py" --root "$tmp")"; rc=$?`. In POSIX sh an assignment takes the status of its command substitution. 85 |
| 17 | Each language runs with the stated tool | scripts/check_facts.py:63 `return [[rustc, "--edition", "2021", "-O", "-o", exe, path], [exe]]` and scripts/check_facts.py:67. 85 |

#### FALSIFIED HYPOTHESES
None.

#### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| 1 | scripts/check_facts.py:92 | `print(f"skip {name}: toolchain not found")` | Demonstrated defect | high | This contradicts scripts/check_facts.py:8 `A missing toolchain is an error, never a silent skip.` and README.md:254. Without rustc or node, 52.rs and 53.ts are skipped and `failed` stays 0. scripts/check_facts.py:113 then returns 0. scripts/pre-commit:17 prints `$out` only when rc≠0, so the skip line is never shown and a commit with false Rust or TS facts passes. **The independent verifier confirmed this (FAIL, 95).** All four domain agents and the category agent reported it too. | Deductive | 95 | `print(f"FAIL {name}: toolchain not found"); failed += 1; continue` |
| 2 | scripts/check.py:400 | `pats = term_patterns(terms)` | Demonstrated defect | high | The comment at scripts/check.py:399 says "substring patterns", but `substring` defaults to False, so masking keeps `=` terms whole-word. With the term `=zqvorblax` and an eval key `zqvorblaxlabs`, scripts/check.py:182 prints `unexpected keys ['zqvorblaxlabs']` unmasked, and the private term leaks. scripts/test_check.py:341-344 expects "message hidden", so by trace that test is red. **The independent verifier confirmed this (FAIL, 80).** It also found that the mask reuses the detection patterns, so any form detection misses (FAIL 3) is printed unmasked too. | Deductive | 90 (code); 79 (the red test) | `pats = term_patterns(terms, substring=True)` |
| 3 | scripts/check.py:90 | `SEP = r"[\W_]?"  # anything that is not a letter or digit, possibly nothing` | Demonstrated defect | high | At most one separator character is allowed. "Quillane  Dorvex" (two spaces), "Quillane - Dorvex" and a CRLF break ("\r\n") are not detected. This contradicts scripts/check.py:16-17 and README.md:250. The two-space variant at scripts/test_check.py:286 is red by trace. On Windows the `\n` variant is written as CRLF (scripts/test_check.py:84-85), so it is red there too. **The independent verifier confirmed this (FAIL, 95).** | Deductive | 90 (code); 79 (the red test) | `SEP = r"[\W_]*"` |
| 4 | scripts/pre-commit:9 | `"$py" -I "$root/scripts/check.py" --staged --root "$root" \|\| exit 1` | Demonstrated defect | high | `--strict` is not passed, yet scripts/pre-commit:5 and README.md:260 ("runs --strict --staged before every commit") say it is. With no terms configured, scripts/check.py:297 only warns, and the commit passes with no private-name check. **The independent verifier confirmed this (FAIL, 97).** Data and Documentation reported it. Code did not. | Deductive | 95 | Add `--strict` (or correct the comment and README.md:260 if non-strict is intended) |
| 5 | scripts/check.py:223 | `for b in badges[:1]:` | Demonstrated defect | medium | Only the first README badge is compared, against scripts/check.py:10 "every skill badge" and README.md:249. scripts/test_check.py:171-173 appends a v2.0 badge and expects "version mismatch", so by trace that test is red. | Deductive | 90 (code); 79 (the red test) | `for b in badges:` |
| 6 | scripts/check.py:228 | `except ValueError as e:` | Demonstrated defect | medium | A missing or unreadable plugin.json, README.md, SKILL.md or CHANGELOG.md raises OSError at scripts/check.py:214, :217, :227 or :237, and nothing catches it. `main` has only try/finally (scripts/check.py:438), so print_report never runs: every collected error is lost, and the traceback is not masked. The verifier showed that the absolute root path in the traceback can contain a private term. | Deductive | 85 | Catch OSError and call `rep.error(rel, "missing or unreadable")` |
| 7 | scripts/check.py:463 | `ids = {e.get("id") for e in evals if isinstance(e, dict)}` | Demonstrated defect | low | With `"evals": null`, `.get("evals", [])` returns None and this line raises TypeError. That contradicts scripts/check.py:462 `return  # check 1 already reports it`, because check 1's report is lost to the traceback. | Deductive | 88 | `if not isinstance(evals, list): return` |
| 8 | scripts/check.py:389 | `subprocess.run(["git", "-C", root, "checkout-index", "-a", "--prefix=" + tmp + os.sep],` | Preventive measure | medium | **The verifiers disagree.** Code P20, Data P10 and Documentation P19 gave PASS at 85: the index is written to tmp and every check reads `root = tmp` (scripts/check.py:433). The independent verifier gave FAIL at 70: checkout-index applies eol conversion (core.autocrlf) and smudge filters, so the scanned bytes are not exactly the staged blobs. With autocrlf, "a\nb" becomes "a\r\nb" and slips past FAIL 3. Symlinks are followed by `open()` (scripts/check.py:126). The category agent agreed with the verifier (75). Reported at the lower confidence. | Deductive | 70 | Read the blobs with `git cat-file --batch`, or check out with `-c core.autocrlf=false` and no filters |
| 9 | scripts/pre-commit:15 | `out="$("$py" -I "$root/scripts/check_facts.py" --root "$tmp")"; rc=$?` | Preventive measure | low | Both checkers run from the working tree (also scripts/pre-commit:9), not from the staged copy. An unstaged edit to a checker changes the verdict on the staged content, and a staged change to a checker is not what runs. This contradicts scripts/pre-commit:2. | Deductive | 85 | Run `$tmp/scripts/check.py` and `$tmp/scripts/check_facts.py` |
| 10 | scripts/check.py:473 | `with_file[int(stem)] = name` | Preventive measure | low | With 38.py and 38.rs side by side, one overwrites the other, so only one hash is checked while both files run. | Deductive | 85 | Report two fact files for one eval as an error |
| 11 | scripts/check.py:363 | `if fence is None:` | Preventive measure | low | Any fence line closes any open fence: a ``` block is closed by `~~~` (scripts/check.py:364 stores the character and never compares it, and scripts/check.py:366 resets). Table checks then run inside code. Reported by Code, Tests (after resend) and Documentation. | Deductive | 85 | Close only on the same character and at least the same length |
| 12 | scripts/pre-commit:12 | `if git diff --cached --name-only \| grep -q '^skills/adversarial-verify/evals/'; then` | Preventive measure | low | A commit that changes only scripts/check_facts.py does not run the facts, so a weakened runner is never exercised. | Deductive | 85 | Add `scripts/check_facts\.py` to the pattern |
| 13 | scripts/check_facts.py:100 | `r = subprocess.run(step, cwd=FACTS, capture_output=True, text=True)` | Preventive measure | medium | There is no timeout, so a looping fact file blocks the commit forever. Output is decoded with the locale codec, which can raise UnicodeDecodeError on cp1252. | Abductive | 65 | `timeout=`, plus `encoding="utf-8", errors="replace"` |
| 14 | scripts/check.py:316 | `except ValueError:` | Preventive measure | low | A .json file that is not valid JSON skips the escape-decoded scan silently, so a `\u`-escaped term goes unreported (category agent). | Deductive | 75 | Report a warning, or decode the string literals with a regex |
| 15 | scripts/check.py:94 | `text = unicodedata.normalize("NFKD", text)` | Preventive measure | medium | "Ignores accents" does not hold for ø, ł, đ and æ, which have no NFKD decomposition. "zqvørblax" is not matched, and the "Not caught" list (scripts/check.py:24) does not mention it. | Deductive | 80 | Add a fold table, or document the gap |
| 16 | scripts/check.py:369 | `if fence is None and i > 0 and DELIM.match(lines[i]) and "\|" in lines[i] + lines[i - 1]:` | Preventive measure | low | A paragraph line containing a pipe, followed by a `---` setext underline, is taken for a table and raises a false ERROR. | Deductive | 75 | Require a pipe in the delimiter line, or matching cell counts |
| 17 | scripts/check.py:470 | `if not stem.isdigit() or int(stem) not in ids:` | Preventive measure | low | The stem "²" passes isdigit() but `int()` raises ValueError, which gives a traceback (Data and the category agent). | Deductive | 85 | `stem.isascii() and stem.isdigit()` |
| 18 | scripts/check_facts.py:83 | `files = sorted(f for f in os.listdir(FACTS) if f.endswith(EXTS) and not f.startswith("_"))` | Preventive measure | low | A wrong `--root` raises a FileNotFoundError traceback. So does a non-UTF-8 fact file, at scripts/check_facts.py:43 `text = open(path, encoding="utf-8").read()`, which aborts the run before the summary (category agent). | Deductive | 85 | Catch the error and report it as FAIL |

### STRESS TEST RESULTS
Not requested from the domain agents (protocol: six sections only). In its place, the independent verifier re-checked the 5 highest-risk claims, as reported above.

### HYPOTHESES (Abductive — require further investigation)
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| 1 | scripts/check_facts.py:49 `return True  # let the run report the syntax error` | A .py fact file with a UTF-8 BOM fails `ast.parse` and so passes the assertion gate unexamined | `ast.parse` accepts the BOM | Run check_facts.py on a BOM copy of 49.py with its asserts removed |
| 2 | scripts/check_facts.py:37 `".rs": re.compile(r'//[^\n]*\|/\*.*?\*/\|"(?:\\.\|[^"\\])*"', re.S),` | A `'"'` char literal or a nested block comment fools the strip in both directions | No fact file uses these forms, so the risk is latent | Run has_assertion on crafted .rs files |
| 3 | scripts/pre-commit:8 `command -v "$py" >/dev/null 2>&1 \|\| py=python` | The Windows Store `python3` stub passes `command -v` but does not run scripts | A real python3 is first on PATH | Run the hook under Git for Windows with only the stub |
| 4 | scripts/check_facts.py:63 `return [[rustc, "--edition", "2021", "-O", "-o", exe, path], [exe]]` | On Windows the binary `52.rs.bin` runs without an .exe extension | CreateProcess refuses it | `check_facts.py 52` on Windows |
| 5 | scripts/pre-commit:14 `git checkout-index -a --prefix="$tmp/" \|\| { rm -rf "$tmp"; exit 1; }` | During `git commit -a`, GIT_INDEX_FILE points to a temporary index, and the right content is checked | A relative GIT_INDEX_FILE with `git -C` resolves to the wrong place | `git commit -a` with a staged leak |

### HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| 1 | scripts/check.py:436 `if files or not args.staged:` | `--staged` checks the staged content | With an empty index, no check runs (not even `--strict`), and the exit code is 0 | Preventive measure, low | 85 |
| 2 | scripts/check.py:149 `if files:` | Walk all files only when git is not available (scripts/check.py:46) | Also walks, untracked files included, when git fails or tracks nothing (scripts/check.py:151 `except (OSError, subprocess.CalledProcessError):`) | Preventive measure, low | 85 |
| 3 | scripts/check.py:247 `raw = os.environ.get("CHECK_PRIVATE_TERMS")` | Terms come from the env var or the file | A set but empty env var disables the file | — (warned) | 88 |
| 4 | scripts/check_facts.py:85 `files = [f for f in files if os.path.splitext(f)[0] in ids]` | Runs "only these eval ids" | Unknown ids are dropped silently: `38 999` exits 0 | Preventive measure, low | 90 |
| 5 | scripts/check_facts.py:63 | .rs files are compiled with rustc | `-O` turns off overflow checks and `debug_assert!` | Preventive measure, low | 80 |
| 6 | scripts/check_facts.py:50 `return any(isinstance(n, (ast.Assert, ast.Raise)) for n in ast.walk(tree))` | "must contain at least one assertion" | An assert in dead code counts | — | 90 |
| 7 | scripts/check.py:319 `m = p.search(body)` | Private terms are reported | Only the first occurrence of each term per file is reported | — | 92 |
| 8 | scripts/check.py:85 `r"Laravel", r"Django", r"Rails", r"Spring", r"React", r"Angular", r"Vue",` | Technology-bound terms | No `\b`, so "Springfield" matches too (warning only) | — | 85 |

### ADVERSARIAL SCAFFOLD FINDINGS
- **Reviewer blind spots:**
  - The mask reuses the detection patterns, so every detection gap is also a print leak.
  - The hook hides runner output when the run succeeds.
- **Highest-risk claims:**
  1. "Never a silent skip" (FAIL 1).
  2. "Terms are never printed" (FAIL 2, FAIL 6).
  3. "The hook runs `--strict`" (FAIL 4).
- **Multi-step traces:**
  - Missing rustc → skip → exit 0 → the hook swallows the output → a false fact is committed.
  - `=` term → whole-word mask → key printed through scripts/check.py:182 → leak.
  - core.autocrlf → CRLF in tmp → SEP misses "a\r\nb" → leak committed.
- **Subtlety flags:**
  - The default argument `substring=False` at scripts/check.py:259.
  - `badges[:1]` looks like a deliberate slice.

### SUMMARY
- Domain: Code
- Claims: 17 verified, 18 in FAIL (7 demonstrated defects, 11 preventive measures), 0 falsified
- Survived: n/a (no stress table; 4 of 5 independent re-checks agreed)
- Failure categories: 5 systemic patterns
- Invariants: not collected
- Hypotheses: 5 requiring further investigation
- Hidden behaviors: 8 detected
- Findings by type: 7 demonstrated defects, 11 preventive measures, 0 falsified hypotheses
- Critical issues: 0 (4 high: FAIL 1-4)
- Executed: 0 tests run
- Recommendation: do not rely on the hook as a privacy or facts gate until FAIL 1-4 are fixed.

---

## DOMAIN: TESTS

### VERIFICATION DOMAIN
Tests. Primary for `scripts/test_check.py`, and for how the suite covers the other three files.

### GROUND TRUTH
- The code under test.
- skills/adversarial-verify/evals/evals.json and facts/*.py.
- .gitignore:1.
- CHANGELOG.md:5.

### INVARIANTS
Not collected (protocol: six sections only).

### DECOMPOSED CLAIMS
The 19 claims are in out/returns/Tests.md. The main ones:
1. The suite fails when an invariant is broken (scripts/test_check.py:1). Deductive.
2. No private test term is ever printed (scripts/test_check.py:5). Deductive.
3. Every assertion can fail (scripts/test_check.py:479). Deductive.
4. Results do not depend on the developer's environment (scripts/test_check.py:43). Abductive.

### FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|----------------|
| Tautological or weak assertion | scripts/test_check.py:479, scripts/test_check.py:302, scripts/test_check.py:316, scripts/test_check.py:617, scripts/test_check.py:72 | test_check.py |
| Test-environment artifact | scripts/test_check.py:43, scripts/test_check.py:576-578, scripts/test_check.py:351, scripts/test_check.py:85, scripts/test_check.py:31, scripts/test_check.py:380, scripts/test_check.py:503 | test_check.py |
| Missing negative test | scripts/check_facts.py:91, scripts/check_facts.py:51, scripts/check.py:498, scripts/check.py:77, scripts/check.py:363, scripts/check.py:128, scripts/check.py:271, scripts/check.py:321, scripts/check.py:195, scripts/check.py:436 | check.py, check_facts.py |
| Suite red against the current code (missing completeness) | scripts/test_check.py:173, scripts/test_check.py:286, scripts/test_check.py:344 | test_check.py |

### VERIFICATION RESULTS
#### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| 1 | A bool id is pinned | scripts/test_check.py:126 `d = self.evals(); d["evals"][0]["id"] = True; self.save_evals(d)`. 88 |
| 2 | The tag boundary at 21 is pinned from both sides | scripts/test_check.py:151 `e = [x for x in d["evals"] if x["id"] == 21][0]` and scripts/test_check.py:158. 85 |
| 3 | An older CHANGELOG entry does not satisfy the check | scripts/test_check.py:224 inserts `## 9.0 - unreleased` before the newest entry. 85 |
| 4 | The prompt-hash binding bites | scripts/test_check.py:550 `replace("day > 31", "day > 28")`. Index 36 is id 37 (skills/adversarial-verify/evals/evals.json:462). 85 |
| 5 | The staged blob, not the working tree, is checked | scripts/test_check.py:385 `open(self.path("leak.md"), "w").write("clean\n")`. 85 (it pins index vs working tree. eol and filters are not exercised: Code FAIL 8) |
| 6 | The temp dir is removed | scripts/test_check.py:396 `"temporary directory left behind"`. 82 |
| 7 | Comments and strings in .py do not count as assertions | scripts/test_check.py:599. 88 |
| 8 | A file without assertions fails | scripts/test_check.py:588 `"assert clipped(375)", "x = clipped(375)"`. 88 |
| 9 | The ok line is required | scripts/test_check.py:610 `"print('ok 40')", "print('done')"`. 88 |
| 10 | A false fact is caught | scripts/test_check.py:582. `edit` asserts that the old string is present. 82 |
| 11 | An empty selection fails | scripts/test_check.py:616 `r = self.run_facts("12345")`. 85 |
| 12 | Masking works for substring terms | scripts/test_check.py:334 `"message hidden")`. 85 |
| 13 | The terms file is gitignored | scripts/test_check.py:366, .gitignore:1 `.check-private-terms`. 95 |
| 14 | No test term appears literally in the repo | scripts/test_check.py:25 `T1 = "zq" + "vorblax"`. 85 |

#### FALSIFIED HYPOTHESES
None.

#### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| 1 | scripts/test_check.py:479 | `self.assertIn("orphan.md", r.stdout + self.ref("orphan.md"))` | Demonstrated defect | medium | Tautology: the haystack always contains the needle, and the exit code is not asserted. This breaks the rule at scripts/test_check.py:4. Reported by all four domain agents and the category agent. | Deductive | 95 | `self.assert_fails(r, "orphan.md", "never named in SKILL.md")` |
| 2 | scripts/test_check.py:578 | `self.assertRegex(r.stdout, r"\d+ fact file\(s\), 0 failed")` | Demonstrated defect | medium | Because of Code FAIL 1, this test is green without rustc or node (a false green). It is red with Node older than 22.6 (a false red). | Deductive | 85 | Assert that no line starts with "skip", or use skipUnless on the toolchains |
| 3 | scripts/test_check.py:43 | `env = dict(os.environ)` | Preventive measure | medium | An exported CHECK_PRIVATE_TERMS overrides the terms file (scripts/check.py:247-249). That changes the results at scripts/test_check.py:320, :325, :329, :355 and :360. An inherited GIT_DIR or GIT_INDEX_FILE redirects `git -C`. | Deductive | 85 | `env.pop("CHECK_PRIVATE_TERMS", None)`, and the same for the GIT_* variables |
| 4 | scripts/test_check.py:72 | `for t in (T1, T2, T2.replace(" ", "")):` | Demonstrated defect | medium | The leak check looks for only two forms of T2. Hyphen, underscore, newline and double-space forms would pass if printed (category agent). | Deductive | 85 | Search with the same normalized pattern as check.py, with `*` |
| 5 | scripts/test_check.py:64 | `def assert_passes(self, r):` | Preventive measure | low | assert_passes never calls assert_no_leak (only assert_fails does, at scripts/test_check.py:62 `self.assert_no_leak(r)`), so passing runs with terms are never leak-checked. | Deductive | 85 | Call `self.assert_no_leak(r)` in assert_passes |
| 6 | scripts/test_check.py:302 | `self.assert_fails(self.run_check(terms=T1), "notes16.txt")` | Preventive measure | low | Any error that names the file satisfies it, and scripts/test_check.py:316 `"plugin.json")` has the same flaw. | Deductive | 85 | Also assert "private term #1" or "after decoding JSON escapes" |
| 7 | scripts/test_check.py:617 | `self.assertNotEqual(r.returncode, 0, r.stdout)` | Preventive measure | low | A traceback satisfies it. The same line is repeated at :584, :592, :601 and :612. | Deductive | 85 | Also assert the FAIL message |
| 8 | scripts/test_check.py:351 | `os.symlink(os.path.join(self.tmp, "does-not-exist"), self.path("dangling.md"))` | Preventive measure | low | On Windows without symlink privilege this errors instead of being skipped. | Deductive | 80 | `try/except OSError: self.skipTest(...)` |
| 9 | scripts/test_check.py:503 | `git = lambda *a: subprocess.run(["git", "-C", self.tmp, "-c", "user.name=t", "-c", "user.email=t@t", *a],` | Preventive measure | low | There is no skipUnless(git) guard, so the test errors on machines without git (category agent). | Deductive | 85 | Add the guard that StagedTest uses |
| 10 | scripts/test_check.py:31 | `self.tmp = tempfile.mkdtemp()` | Preventive measure | medium | The temp copy is not a git repository, so non-git tests take the os.walk fallback (scripts/check.py:149-152), which production does not use. The copy also leaves out files such as LICENSE (scripts/test_check.py:32). | Deductive | 85 | `git init` plus `add` in the fixture |
| 11 | scripts/pre-commit:12 | `if git diff --cached --name-only \| grep -q '^skills/adversarial-verify/evals/'; then` | Preventive measure | medium | No test runs the hook: the conditional, checkout-index and the rc handling go unverified. This is why Code FAIL 4 (no `--strict`) went unnoticed. | Deductive | 80 | A test that installs the hook in a temp repo |
| 12 | scripts/check_facts.py:91 | `if steps is None:` | Preventive measure | medium | Missing negative test: the missing-toolchain branch is never exercised. | Deductive | 90 | Run with PATH stripped of rustc and node, and expect a failure |
| 13 | scripts/check_facts.py:51 | `return bool(ASSERTS[ext].search(STRIP[ext].sub(" ", text)))` | Preventive measure | medium | The .rs and .ts strip paths have no test. | Deductive | 85 | Add .rs and .ts files whose only assertion is inside a comment or string |
| 14 | scripts/check.py:498 | `if not isinstance(e, dict) or type(e.get("id")) is not int or e["id"] < FACTS_FROM:` | Preventive measure | low | The FACTS_FROM = 29 boundary (scripts/check.py:77) is not pinned: moving it changes no test. | Deductive | 85 | Tests for eval 28 (passes) and eval 29 (fails) |
| 15 | scripts/check.py:363 | `if fence is None:` | Preventive measure | low | No mixed-fence test (scripts/test_check.py:446-450 uses only matching pairs). This row was corrected on resend from :364. | Deductive | 80 | A ``` block containing `~~~` and then a broken table |
| 16 | scripts/check.py:271 | `if rep is not None and sum(len(p) for p in parts) < 4:` | Preventive measure | low | Missing boundary tests: only a 3-character term is tested. scripts/check.py:321 (the reported line number), scripts/check.py:195 (empty assertions), scripts/check.py:128 (non-UTF-8 key files) and scripts/check.py:436 (empty index) have no test either (category agent). | Deductive | 85 | One test per boundary |

### STRESS TEST RESULTS
Not collected.

### HYPOTHESES (Abductive — require further investigation)
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| 1 | scripts/test_check.py:286 `for variant in (...  f"{a.upper()}  {b}"):`, scripts/test_check.py:173 and scripts/test_check.py:344 | The suite is red today in at least three tests: Code FAIL 2, 3 and 5 | It was never run against this tree | `python3 -m unittest scripts/test_check.py` |
| 2 | scripts/test_check.py:414 `self.assertIn("SQLite", open(self.path(EVALS)).read())` | Under cp1252 a UTF-8 byte raises (a false red) | evals.json is cp1252-safe | Run with `PYTHONUTF8=0` on Windows |
| 3 | scripts/test_check.py:380 `self.git("commit", "-q", "-m", "base")` | Global commit.gpgsign or hooks break StagedTest | No such config is set | Run with `commit.gpgsign=true` |

### HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| 1 | scripts/test_check.py:32 `for item in ("README.md", "CHANGELOG.md", "skills", ".claude-plugin", "scripts", ".gitignore"):` | "the repo passes" | Only the listed items are copied, and the copy is checked through a code path production does not take | Preventive measure | 85 |
| 2 | scripts/test_check.py:337 `# whole-word detection does not flag "<term>labs", ...` | A whole-word case | It uses `terms=T1` (substring), so it duplicates PASS 12. The text of the comment is a Documentation finding. | Preventive measure | 90 |

### ADVERSARIAL SCAFFOLD FINDINGS
- **Reviewer blind spots:**
  - The tautology at scripts/test_check.py:479 reads like a real assertion.
  - The leak helper checks only two literal forms.
- **Highest-risk claims:**
  1. The suite proves the facts hold (FAIL 2).
  2. No leak is ever printed (FAIL 4, FAIL 5).
  3. The hook is covered (FAIL 11).
- **Multi-step trace:** a developer exports CHECK_PRIVATE_TERMS → the terms-file tests go falsely green or red.
- **Subtlety flag:** assert_fails and assert_passes are asymmetric.

### SUMMARY
- Domain: Tests
- Claims: 14 verified, 16 in FAIL (3 demonstrated defects, 13 preventive measures), 0 falsified
- Failure categories: 4
- Hypotheses: 3
- Hidden behaviors: 2
- Critical issues: 0
- Executed: 0
- Recommendation: by trace the suite is red today, and its green runs over-promise. Fix FAIL 1-5 and add the hook test.

---

## DOMAIN: DATA

### VERIFICATION DOMAIN
Data. Covers:
- the evals.json contract;
- the NOT_COMPUTABLE format;
- the fact-file hash binding;
- the private-terms file;
- file decoding.

### GROUND TRUTH
- skills/adversarial-verify/evals/evals.json: 57 evals, ids 1..57.
- facts/NOT_COMPUTABLE:4-12.
- The headers of facts/*.
- CHANGELOG.md:10, plugin.json:3, SKILL.md:20, README.md:1.
- .gitignore:1.

### INVARIANTS
Not collected.

### DECOMPOSED CLAIMS
The 26 claims are in out/returns/Data.md. The main ones:
1. Exactly 4 keys per eval (scripts/check.py:6). Deductive.
2. Facts are required from eval 29 (scripts/check.py:34). Deductive.
3. Every fact file is bound to its prompt hash (scripts/check.py:37). Deductive.
4. The terms list is never committed (scripts/check.py:423). Deductive.
5. The current data passes (scripts/test_check.py:98). Inductive.

### FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|----------------|
| Missing completeness | scripts/check.py:494, scripts/check.py:473, scripts/check.py:128 | check.py |
| Silent fallthrough | scripts/check.py:494, scripts/check.py:301 | check.py |
| Assumed environment (encoding) | scripts/check.py:122, scripts/pre-commit:12 (quotePath) | check.py, pre-commit |
| Stale state | scripts/check.py:469 (helpers exempt from the hash) | check.py |

### VERIFICATION RESULTS
#### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| 1 | Exactly the 4 keys | scripts/check.py:180 `extra, missing = sorted(set(e) - EVAL_KEYS), sorted(EVAL_KEYS - set(e))`. The current data has 57×4 keys. Inductive, 75 |
| 2 | Versions agree | scripts/check.py:237 and scripts/check.py:233 `if not isinstance(pv, str):`. CHANGELOG.md:10 `## 4.2`, plugin.json:3 and the README badge all say 4.2. 90 |
| 3 | A BOM before `#` keeps it a comment | scripts/check.py:120 `return data.decode("utf-8-sig"), "utf-8"`, used at scripts/check.py:255. 88 |
| 4 | Facts are required from 29, with a file or a reason but not both | scripts/check.py:500 `if "(Facts" in str(e.get("prompt", "")) and ...`. In the current data, ids 30-50 are in NOT_COMPUTABLE and the rest have files. Inductive, 78 |
| 5 | `<id>: <reason>` format | scripts/check.py:490 `m = re.match(r"^(\d+):\s*(\S.*)?$", line)`. 88 |
| 6 | The terms file is never committed | .gitignore:1 `.check-private-terms` and scripts/check.py:423. 85, but see FAIL 4 |
| 7 | Index 36 is eval 37 | skills/adversarial-verify/evals/evals.json:462 `"id": 37,`. 88 |
| 8 | Version read from the frontmatter only | scripts/check.py:216. Inductive, 70 |

#### FALSIFIED HYPOTHESES
None.

#### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| 1 | scripts/check.py:494 | `reasons[int(m.group(1))] = m.group(2)` | Preventive measure | low | A NOT_COMPUTABLE id is never checked for being an existing eval or for uniqueness. A stale `NN: reason` silently exempts a future eval NN. | Deductive | 85 | Report unknown and duplicate ids |
| 2 | scripts/check.py:122 | `return data.decode("latin-1"), "latin-1"` | Preventive measure | medium | One invalid byte switches the whole file to Latin-1. Then `ó` becomes `Ã³` and normalizes to `a3`, so an accented term is missed. | Deductive | 80 | Decode per sequence (`errors="replace"`) |
| 3 | scripts/check.py:301 | `if os.path.basename(rel) == TERMS_FILE:` | Preventive measure | medium | A file with this name at any depth, force-added, is exempt from both scans. The private list could be committed with no error, against scripts/check.py:423. Reported by Data, Code, Documentation and the category agent. | Deductive | 82 | Raise an error when a tracked or staged file has this name |
| 4 | scripts/check.py:500 | `if "(Facts" in str(e.get("prompt", "")) and e["id"] not in with_file and e["id"] not in reasons:` | Preventive measure | low | The marker is case- and form-sensitive: `(facts` slips through. | Deductive | 75 | `re.search(r"\(\s*facts\b", prompt, re.I)` |
| 5 | scripts/check.py:476 | `head = read_text(root, f"{FACTS_DIR}/{name}")[:2000]` | Preventive measure | low | The hash must be lowercase hex within the first 2000 characters. An uppercase hash gets the misleading message "no 'prompt-sha256:' line". | Deductive | 82 | Accept `re.I`, or document the format |

### STRESS TEST RESULTS
Not collected.

### HYPOTHESES (Abductive — require further investigation)
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| 1 | scripts/check.py:481 `elif m.group(1) != want:` | Every hash matches its prompt today | Evals 56 and 57 were edited after their facts | `python3 scripts/check.py` |
| 2 | scripts/check.py:469 `if ext in FACT_EXTS and not stem.startswith("_"):` | An edit to `_parse_day.py` changes what 35.py, 37.py and 39.py prove, with no hash failing | Re-running the files is enough | Edit the helper, then run both scripts |
| 3 | scripts/pre-commit:12 | With core.quotePath, a non-ASCII path under evals/ is printed quoted and skips the fact run | Fact names are always ASCII | Stage a non-ASCII-named fact file |

### HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| 1 | scripts/check.py:128 `if enc != "utf-8" and rep is not None and (rel in (SKILL, README, EVALS) or ...` | Files that are not UTF-8 are "still scanned" | It is an ERROR for SKILL.md, README, evals.json and references only. Others pass silently as Latin-1, and the error can be reported twice. | Preventive measure, low | 80 |
| 2 | scripts/check.py:469 | "every fact file belongs to an existing eval" | `_`-prefixed helpers are exempt, and no docstring says so | — | 92 |

### SUMMARY
- Domain: Data
- Claims: 8 verified, 5 in FAIL (0 demonstrated defects, 5 preventive measures), 0 falsified
- Failure categories: 4
- Hypotheses: 3
- Hidden behaviors: 2
- Critical issues: 0
- Recommendation: the current data is consistent. The contract checks have gaps around NOT_COMPUTABLE and the terms-file exemption.

---

## DOMAIN: DOCUMENTATION

### VERIFICATION DOMAIN
Documentation: docstrings, comments, usage text and messages in the four files, checked against the code and against README.md.

### GROUND TRUTH
- The code.
- README.md:249-260 and CHANGELOG.md.
- .gitignore and evals.json.
- skills/adversarial-verify/evals/facts/*.

### INVARIANTS
Not collected.

### DECOMPOSED CLAIMS
There are 48 claims, one per documented statement, in out/returns/Documentation.md. 33 of them pass. For example:
- scripts/check.py:4 (exit code);
- scripts/check.py:27 (neutral wording only warns);
- scripts/check.py:50 (Python 3.8);
- scripts/check_facts.py:17 (id filter);
- scripts/pre-commit:3 (symlink target);
- scripts/test_check.py:3 (the run command).

### FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|----------------|
| Stale documentation (describes intended or earlier behavior) | scripts/check_facts.py:8, scripts/check.py:10, scripts/check.py:16, scripts/check.py:22, scripts/check.py:399, scripts/pre-commit:5, scripts/check.py:43, scripts/check.py:46, scripts/test_check.py:337, scripts/check.py:168, scripts/check.py:295 | all four (and README.md:249, :250, :254, :260, which are outside the scope) |
| Missing completeness (incomplete "Not caught" list) | scripts/check.py:24 | check.py |

### VERIFICATION RESULTS
#### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| 1 | Exit code only on errors | scripts/check.py:4 against scripts/check.py:442. 90 |
| 2 | TAGGED_FROM = 21 matches the data | scripts/check.py:74, evals.json (id 20 untagged, id 21 tagged). Inductive, 85 |
| 3 | FACTS_FROM = 29 matches the documented threshold | scripts/check.py:77 `FACTS_FROM = 29  # from here on, ...`, README.md:254. 85 |
| 4 | The table messages give correct line numbers | scripts/check.py:373 `rep.error(f"{rel}:{i + 1}", f"table delimiter has ...")`. 85 |
| 5 | The Rust strip note matches the code | scripts/check_facts.py:36 against :37. 85 |
| 6 | The hook's install line resolves | scripts/pre-commit:3 `# Install once: ln -s ../../scripts/pre-commit .git/hooks/pre-commit`. 85 |
| 7 | The test run command | scripts/test_check.py:3 `Run from the repo root: python3 -m unittest scripts/test_check.py`. 85 |
| 8 | The BOM comment | scripts/test_check.py:324, against scripts/check.py:120. 88 |
| 9 | The other documented statements | 25 more rows in out/returns/Documentation.md (PASS 1-48). All quotes were looked up. 80-90 |

#### FALSIFIED HYPOTHESES
None.

#### FAIL ❌
Where a statement is false because the code is wrong, the defect is counted once, in Code. Those rows are listed here by reference. The rows below are the ones whose primary fault is the text.

| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| 1 | scripts/pre-commit:5 | `# --strict fails if no private terms are configured (see scripts/check.py).` | Demonstrated defect | high | Line 9 does not pass `--strict`, and README.md:260 repeats the claim. The defect is counted in Code FAIL 4. Here it is the false statement. | Deductive | 95 | Add the flag, or fix the comment and README.md:260 |
| 2 | scripts/check.py:24 | `--strict it fails. Not caught: a one-word term written as two words (space or` | Demonstrated defect | medium | The "Not caught" list leaves out multi-character separators, CRLF and non-decomposing letters (Code FAIL 3, Code FAIL 15). | Deductive | 88 | Fix the code, or extend the list |
| 3 | scripts/check.py:43 | `reader nowhere. The folder is read as it is on disk, tracked or not, since` | Demonstrated defect | low | With `--staged` the folder is the staged copy, and scripts/test_check.py:508 relies on that. | Deductive | 85 | Add "(with --staged: as staged)" |
| 4 | scripts/check.py:46 | `Files checked: the files tracked by git (all files outside .git if git is not` | Demonstrated defect | low | The fallback also happens when git fails or tracks nothing (scripts/check.py:149-151). | Deductive | 85 | Reword |
| 5 | scripts/test_check.py:337 | `# whole-word detection does not flag "<term>labs", but the evals check prints the key name` | Demonstrated defect | low | The test uses `terms=T1` (substring), so detection does flag it. The comment describes an earlier default. Reported by Tests and Documentation. | Deductive | 88 | Reword, or make it the `=` case |
| 6 | scripts/test_check.py:1 | `"""Tests for scripts/check.py: the repo passes, and each invariant fails on a case built to break it.` | Demonstrated defect | low | The file also tests check_facts.py (scripts/test_check.py:571-617), and check 4 has no failing case: it only warns. | Deductive | 82 | Mention both |
| 7 | scripts/check.py:168 | `rep.error(EVALS, f"not valid JSON ({e.__class__.__name__}: {e})")` | Demonstrated defect | low | A missing evals.json (OSError) is reported as "not valid JSON" (category agent). | Deductive | 90 | Distinguish OSError |
| 8 | scripts/check.py:295 | `msg = (f"no private terms configured (set CHECK_PRIVATE_TERMS or create {TERMS_FILE}); "` | Demonstrated defect | low | With CHECK_PRIVATE_TERMS set but empty, the existing file is ignored, and the message tells the user to create a file that already exists (category agent). | Deductive | 80 | Name the env var as the cause |
| — | scripts/check_facts.py:8, scripts/check.py:10, scripts/check.py:16, scripts/check.py:22, scripts/check.py:399, scripts/check.py:462 | (see Code) | — | — | These are false statements whose defect is counted in Code FAIL 1, 5, 3, 2, 2 and 7. | — | — | Fixed by the code fix |

### STRESS TEST RESULTS
Not collected.

### HYPOTHESES (Abductive — require further investigation)
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| 1 | scripts/pre-commit:1 `#!/bin/sh` | The file is committed as 100755, so the install line works | It is 100644, and git ignores the hook | `git ls-files -s scripts/pre-commit` |
| 2 | scripts/check_facts.py:67 `return [[node, "--experimental-strip-types", "--no-warnings", path]]` | An old node reports "FAIL 53.ts", not a missing toolchain, and the required version is not stated in the script | Every contributor has Node 22.6 or later | Run with Node 20 |
| 3 | scripts/check.py:389 | Git for Windows accepts a prefix that ends in a backslash | It writes files to unexpected names | StagedTest on Windows |

### HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| 1 | scripts/check_facts.py:112 `print(f"{len(files)} fact file(s), {failed} failed")` | A per-run summary | Skipped files are counted in the total without being shown as skipped | Part of Code FAIL 1 | 92 |
| 2 | scripts/pre-commit:17 `[ $rc -eq 0 ] \|\| { printf "%s\n" "$out"; exit 1; }` | — | Output is shown only on failure, which hides the skip lines | Part of Code FAIL 1 | 92 |

### SUMMARY
- Domain: Documentation
- Claims: 33 verified, 8 in FAIL (8 demonstrated defects, all text), 0 falsified. 6 more statements are false because of Code defects and are counted there.
- Failure categories: 2
- Hypotheses: 3
- Hidden behaviors: 2
- Critical issues: 0
- Recommendation: the docstrings describe the intended contract more faithfully than the code does. Fix the code rather than the text, except for Documentation FAIL 3, 4, 6, 7 and 8.

---

## CROSS-DOMAIN SUMMARY
- **Claims:** 72 verified. 47 in FAIL: 18 demonstrated defects and 29 preventive measures. 0 falsified.
- **Counting:** each finding is counted once, in its primary domain.
- **Failure categories:** 9 systemic patterns:
  1. silent fallthrough;
  2. missing completeness;
  3. stale documentation;
  4. assumed environment;
  5. test-environment artifact;
  6. tautological or weak assertion;
  7. missing negative test;
  8. stale state;
  9. uncaught error path.
- **Critical issues:** 0. 4 are high and demonstrated:
  - Code FAIL 1: a missing toolchain is a silent pass.
  - Code FAIL 2: `=` terms leak through the mask.
  - Code FAIL 3: the single-character separator misses names.
  - Code FAIL 4: the hook has no `--strict`.
- **Changes that touch several domains:**
  - Code FAIL 2, 3 and 5 are each a code defect, a false docstring (Documentation) and, by trace, a red test (Tests H1).
  - Code FAIL 1 is a code defect, a false docstring and a false-green test (Tests FAIL 2).
  - Code FAIL 4 is a hook defect, a false comment and a false README.md:260, and it went unnoticed because no test covers the hook (Tests FAIL 11).
- **Outside the scope:** README.md:249, :250, :254 and :260 make the same claims as the docstrings, and they would need updating if the code is not fixed.
- **Rows and verification:**
  - Rows returned: 417 (Code 92, Tests 68 + 2 on resend, Data 75, Documentation 119, independent verifier 5, category agent 56).
  - Discarded on lookup: 2 (Tests FAIL F15 and its category instance, both quoted at scripts/check.py:364). Both came back corrected to scripts/check.py:363 on resend. Finally dropped: 0.
  - Independent verifier: 5 claims; 4 confirmed (FAIL), 1 changed (`--staged`: domain PASS 85 → FAIL 70, preventive; Code FAIL 8).
- **Executed:** 0. Reasoning only.

## PROPOSED EXECUTABLE CHECKS
| # | Claim | Confidence now | Check (command, test or query) | Confirms if | Refutes if | Cost and side effects | Status |
|---|-------|----------------|--------------------------------|-------------|------------|-----------------------|--------|
| 1 | The suite is red on Code FAIL 2, 3 and 5 | 79 | `python3 -m unittest scripts/test_check.py` (from ./tree) | test_second_badge_mismatch, test_two_words_joined_any_way and test_whole_word_term_glued_in_output_is_still_masked fail | All three pass | Runs Python locally. It writes only to temp dirs and runs git in temp repos | proposed |
| 2 | Code FAIL 1: a missing toolchain exits 0 | 95 | `PATH=<python only> python3 scripts/check_facts.py` | "skip 52.rs", "0 failed", exit 0 | Exit 1, or FAIL lines | Runs the fact files and reads only | proposed |
| 3 | Code FAIL 8: CRLF in the temp copy | 70 | In a temp repo with `core.autocrlf=true`, stage "a\nb" (a two-word term) and run `check.py --staged` | The leak is not reported | It is reported | A temp repo only | proposed |
| 4 | Data H1: every hash is current | — | `python3 scripts/check.py` | No "prompt changed" error | That error appears | Reads only | proposed |
| 5 | Code H1: a BOM .py file bypasses the gate | — | Run check_facts.py on a BOM copy of 49.py with its asserts removed | It passes | "no assertion" | A temp copy | proposed |

**Proposed writes:**
- scripts/check.py:90 → `[\W_]*`.
- scripts/check.py:223 → `for b in badges:`.
- scripts/check.py:400 → `term_patterns(terms, substring=True)`.
- scripts/check_facts.py:92 → count a missing toolchain as a failure.
- scripts/pre-commit:9 → add `--strict`.
- scripts/test_check.py:479 → replace the tautology with `assert_fails`.
- scripts/test_check.py:43 → pop CHECK_PRIVATE_TERMS.
- Add a CHANGELOG.md entry under "Unreleased" for these fixes.

Should I run checks 1-5 and make the proposed writes, or only some of them (say which)?
