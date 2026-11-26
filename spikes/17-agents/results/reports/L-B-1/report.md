# Adversarial verification report

## INTAKE
- Target: every domain detected in the 23 listed files: **Code, Tests, Data, Documentation** (named by the request: "every domain the skill detects"). Architecture, Analysis and UX were not detected (no plan/spec/ADR, no agent report, no interface under review).
- Depth: standard (stated). Scope: the whole of the 23 files; no diff, no history (stated). Execution mode: reasoning only, nothing run (stated). No defaults used.
- To change: name other domains, a depth (quick / deep), or approve the checks proposed at the end.
- Method: one domain agent per domain (no domain over 60 kB), an independent verifier on the 5 highest-risk claims, one category agent. Every location is `path:line` relative to `./tree`.

**Row count.** 387 rows came back (domain agents 355, independent verifier 5, category agent 24, resends 3). 3 rows were discarded at the quote lookup (Data 1, Documentation 2: wrong line). Both returns were sent back once, all 3 rows came back corrected and were restored, and none was dropped. The independent verifier **confirmed 5 of 5** claims and changed none. Each quote was looked up at its line, so no PASS was lowered for an unchecked quote. Findings that several agents reported are merged below: each counts once, in its primary domain.

---

## VERIFICATION DOMAIN
Code

## GROUND TRUTH
scripts/check.py, scripts/check_facts.py, scripts/pre-commit (traced by reading); README.md, CHANGELOG.md and the docstrings as the stated contract; scripts/test_check.py as the encoded spec.

## INVARIANTS
Not returned: the briefs asked the agents for six sections only (see log). The invariants the findings touch are the check's own docstring rules, scripts/check.py:6-47.

## DECOMPOSED CLAIMS
1. The version check compares SKILL.md with every skill badge, scripts/check.py:10 `2. The version in SKILL.md's frontmatter matches every skill badge in the README,`. Deductive
2. Term parts joined by anything not a letter or digit are caught, scripts/check.py:16-17. Deductive
3. Terms are never printed, scripts/check.py:22-23. Deductive
4. A missing toolchain is an error, never a silent skip, scripts/check_facts.py:8. Deductive
5. The hook runs `--strict --staged`, scripts/pre-commit:5, README.md:261. Deductive
6. Fact file or reason, not both; fact files bound to the prompt by sha256, scripts/check.py:34-38. Deductive / Abductive (hash values)
7. evals.json structure, the table rule, the reference-file rule and `--staged`, scripts/check.py:6-9, :32-33, :40-42, :47. Deductive
8. Fact files 37–57 compute what their evals state (see Data). Deductive

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Missing completeness | scripts/check.py:223, :478, :500, :301, :495, :186-188; scripts/pre-commit:9 | scripts/check.py, scripts/pre-commit |
| Silent fallthrough | scripts/check_facts.py:92, :85; scripts/check.py:473, :436, :494, :316-317, :151-152; scripts/pre-commit:12, :17 | scripts/check_facts.py, scripts/check.py, scripts/pre-commit |
| Spec drift (docstring/README vs code) | scripts/check.py:10/223, :16/90, :22/399-400; scripts/check_facts.py:8/92; scripts/pre-commit:5/9 | scripts/check.py, scripts/check_facts.py, scripts/pre-commit, README.md |
| Assumed environment | scripts/check.py:227, :237; scripts/check_facts.py:83, :67 | scripts/check.py, scripts/check_facts.py |
| Checker vs checked content | scripts/pre-commit:9, :15 | scripts/pre-commit |
| Markdown parsing diverging from rendering | scripts/check.py:345, :366, :360-361, :341 | scripts/check.py |

## VERIFICATION RESULTS
### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| P1 | No-letter term is an error, a short term a warning | scripts/check.py:269 `rep.error("private terms", f"term #{k} has no letters or digits and cannot be checked")`; traced. 90 |
| P2 | Non-UTF-8 files still scanned | scripts/check.py:114 `if data.startswith((b"\xff\xfe", b"\xfe\xff")):` Latin-1 fallback never raises. 88 |
| P3 | Without terms the check says so; `--strict` fails | scripts/check.py:297 `(rep.error if strict else rep.warning)("private terms", msg)`. 92 |
| P4 | evals.json structure (bool ids rejected, ids 1..n, keys, tags) | scripts/check.py:186 `if type(i) is not int:  # bool is an int subclass: reject it`. 88 |
| P5 | "Not both" logic for fact file and reason | scripts/check.py:496 `rep.error(f"{FACTS_DIR}/NOT_COMPUTABLE", f"eval {i} has a fact file and a reason not to have one")`. The logic is right, and the tree violates it (Data F1). 90 |
| P6 | Hash binding logic | scripts/check.py:477 `m = re.search(r"prompt-sha256:\s*([0-9a-f]{64})", head)`. 85 |
| P7 | Reference-file check | scripts/check.py:519 `for name in sorted(existing - named_in_skill):`. 88 |
| P8 | `--staged` reads the index | scripts/check.py:389 `subprocess.run(["git", "-C", root, "checkout-index", "-a", "--prefix=" + tmp + os.sep],`. 85 |
| P9 | Assertion required outside comments | scripts/check_facts.py:50 `return any(isinstance(n, (ast.Assert, ast.Raise)) for n in ast.walk(tree))`. 85 |
| P10 | Last output line must be `ok <id>` | scripts/check_facts.py:107 `if out[-1:] != [f"ok {stem}"]:`. 90 |
| P11 | No files selected → exit 1 | scripts/check_facts.py:113 `return 1 if failed or not files else 0`. 85 |
| P12 | Hook runs facts on the staged copy and propagates rc | scripts/pre-commit:15 `out="$("$py" -I "$root/scripts/check_facts.py" --root "$tmp")"; rc=$?`. 85 |

### FALSIFIED HYPOTHESES
None.

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| C1 | scripts/pre-commit:9 | `"$py" -I "$root/scripts/check.py" --staged --root "$root" \|\| exit 1` | Demonstrated defect | High | No `--strict`, though scripts/pre-commit:5 `# --strict fails if no private terms are configured` and README.md:261 `# runs --strict --staged before every commit` say it runs strict. With no terms configured, scripts/check.py:297 only warns and the commit goes through with private names unchecked. Reported by all four domain agents; **the independent verifier confirmed it (FAIL, 95)** | Deductive | 93 | Add `--strict` to line 9 |
| C2 | scripts/check.py:400 | `pats = term_patterns(terms)` | Demonstrated defect | High | :399 says masking uses substring patterns, but `substring` defaults to False, so `=` terms mask only whole words. With the term `=acme`, an output line naming `acmecorp` (an unexpected eval key at :182, or an orphan reference at :520) is printed unmasked. This breaks scripts/check.py:22 `Terms are never printed`. test_check.py:341-344 encodes the right behaviour. **Verifier confirmed (FAIL, 85)** | Deductive | 88 | `pats = term_patterns(terms, substring=True)` |
| C3 | scripts/check.py:90 | `SEP = r"[\W_]?"  # anything that is not a letter or digit, possibly nothing` | Demonstrated defect | High | `?` allows at most one separator character, so `Acme  Corp` (two spaces), `Acme - Corp` and a CRLF break are missed, against scripts/check.py:16-17 and README.md:251 `(space, hyphen, underscore, line break, or nothing)`. The two-space variant at test_check.py:286 cannot pass. **Verifier confirmed (FAIL, 95)** | Deductive | 88 | `SEP = r"[\W_]*"` |
| C4 | scripts/check_facts.py:92 | `print(f"skip {name}: toolchain not found")` | Demonstrated defect | High | Lines 91-93 skip without `failed += 1`, and :113 returns 0, against scripts/check_facts.py:8 `A missing toolchain is an error, never a silent skip.` and README.md:255. On a machine without rustc or node, 52.rs or 53.ts go unchecked and the hook passes. **Verifier confirmed (FAIL, 95)** | Deductive | 90 | Count the skip as a failure |
| C5 | scripts/pre-commit:17 | `[ $rc -eq 0 ] \|\| { printf "%s\n" "$out"; exit 1; }` | Demonstrated defect | Medium | Output is printed only on failure, so the `skip … toolchain not found` line from C4 is discarded and the user never learns that facts were not run (category agent) | Deductive | 85 | Always print `$out`, or fail on any `skip` |
| C6 | scripts/check.py:223 | `for b in badges[:1]:` | Demonstrated defect | Medium | Only the first badge is compared, against scripts/check.py:10 and README.md:250 `every skill badge in the README`. test_check.py:171-173 (`test_second_badge_mismatch`) expects "version mismatch" and cannot get it. No live mismatch today: one badge, README.md:1. Reported by all four agents | Deductive | 90 | `for b in badges:` |
| C7 | scripts/check.py:478 | `want = hashlib.sha256(prompts[i].encode("utf-8")).hexdigest()` | Preventive measure | Medium | The hash binds only the prompt, so expected_output and assertions can drift from the facts. Data F2 (evals.json:705) already happened this way | Deductive | 80 | Hash the assertions too, or assert the quoted numbers |
| C8 | scripts/check.py:301 | `if os.path.basename(rel) == TERMS_FILE:` | Preventive measure | Medium | Any file named `.check-private-terms`, at any depth, skips the private-term scan. A tracked copy would ship the whole term list unscanned | Deductive | 85 | Skip only the untracked root file |
| C9 | scripts/check.py:500 | `if "(Facts" in str(e.get("prompt", "")) and e["id"] not in with_file and e["id"] not in reasons:` | Preventive measure | Low | Coverage depends on the literal, case-sensitive marker. Evals 54 and 55 state numbers without it (evals.json:672 `about 400 MB. The machine has 32 GB`, :686 `about 6 GB. The machine has 8 GB`), while CHANGELOG.md:24 says every eval that `states facts` is covered | Inductive | 70 | Require the marker or a reason for every eval from 29 on; match case-insensitively |
| C10 | scripts/check.py:494 | `reasons[int(m.group(1))] = m.group(2)` | Preventive measure | Low | Reasons for unknown ids, ids below 29 or fact-less ids are accepted silently. :495 compares reasons only with fact files | Deductive | 80 | Error on such reasons |
| C11 | scripts/check.py:473 | `with_file[int(stem)] = name` | Preventive measure | Low | With 52.py and 52.rs both present, only the last name's hash is checked | Deductive | 85 | Error on two fact files for one id |
| C12 | scripts/check.py:227 | `plugin = json.loads(read_text(root, PLUGIN, rep))` | Preventive measure | Low | Only ValueError is caught. A missing plugin.json, README, CHANGELOG (:237) or SKILL.md ends in a traceback with no summary | Deductive | 85 | Catch OSError, report "missing" |
| C13 | scripts/check.py:436 | `if files or not args.staged:` | Preventive measure | Low | With `--staged` and an empty index, no check runs and the exit code is 0 | Deductive | 80 | Warn or fail on an empty staged list |
| C14 | scripts/check.py:186-188 | `if type(i) is not int:  # bool is an int subclass: reject it` | Preventive measure | Low | The `continue` at :188 hides the other errors of that eval until the id is fixed | Deductive | 85 | Validate the fields before the id check |
| C15 | scripts/check.py:316-317 | `except ValueError:` / `pass` | Preventive measure | Low | A tracked .json that does not parse loses the decoded-escape scan without a word, so a `\uXXXX`-escaped term passes | Deductive | 85 | Warn: "not valid JSON, escapes not decoded" |
| C16 | scripts/check.py:151-152 | `except (OSError, subprocess.CalledProcessError):` / `pass` | Preventive measure | Low | When git is unavailable the check walks every file on disk, and the summary still says "working tree" | Deductive | 80 | Warn that the file set changed |
| C17 | scripts/pre-commit:12 | `if git diff --cached --name-only \| grep -q '^skills/adversarial-verify/evals/'; then` | Preventive measure | Low | No pipefail: if `git diff` fails, the facts block is skipped silently. A change to check_facts.py alone does not re-run the facts | Deductive | 80 | Store the list first, then exit on error |
| C18 | scripts/pre-commit:15 | `out="$("$py" -I "$root/scripts/check_facts.py" --root "$tmp")"; rc=$?` | Preventive measure | Low | Staged content is checked by the working-tree checkers (same at :9), so a staged change to a checker is committed without having been the code that checked it | Deductive | 75 | Run `$tmp/scripts/…` from the index copy |
| C19 | scripts/check_facts.py:85 | `files = [f for f in files if os.path.splitext(f)[0] in ids]` | Preventive measure | Low | A mistyped id is ignored without a message (`38 3800` passes), and string matching means `038` matches nothing | Deductive | 85 | Report each requested id that has no file |
| C20 | scripts/check_facts.py:83 | `files = sorted(f for f in os.listdir(FACTS) if f.endswith(EXTS) and not f.startswith("_"))` | Preventive measure | Low | `--root` without a facts directory ends in a traceback | Deductive | 85 | Check `isdir`, report and exit 1 |
| C21 | scripts/check.py:366 | `fence = None` | Preventive measure | Low | Any fence line closes any open fence: a `~~~` line inside a fenced block ends it | Deductive | 80 | Close only on the same character and length |
| C22 | scripts/check.py:345 | ``s = re.sub(r"`[^`]*`", "x", line).replace("\\|", "x").strip()`` | Preventive measure | Low | GFM splits cells on an unescaped pipe even inside a code span. A row with `` `a|b` `` passes the check but renders with an extra cell | Deductive | 70 | Require `\|` inside code spans |
| C23 | scripts/check.py:360-361 | `s = lines[i].strip()` / ``f = re.match(r"^(`{3,}|~{3,})", s)`` | Preventive measure | Low | Stripping first lets a fence indented 4+ spaces toggle the state (CommonMark from memory, not a cited file) | Deductive | 70 | Match `^ {0,3}` on the raw line |
| C24 | scripts/check.py:341 | ``DELIM = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")`` | Preventive measure | Low | GFM accepts `\|-\|-\|`, but the check needs 3+ hyphens, so such a table is never checked (GFM from memory) | Deductive | 70 | `-+` |
| C25 | README.md:255 | ``fails if a stated fact is false, if a file has no assertion outside comments, or if a needed toolchain (`rustc`, `node` 22.6 or later) is missing`` | Preventive measure | Low | scripts/check_facts.py:67 `return [[node, "--experimental-strip-types", "--no-warnings", path]]` checks that node exists, never its version | Abductive | 55 | Check `node --version` |

## STRESS TEST RESULTS
Not returned by the agents (outside the six sections the briefs asked for).

## HYPOTHESES (Abductive — require further investigation)
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| CH1 | scripts/check_facts.py:62 `exe = os.path.join(tmp, os.path.basename(path) + ".bin")` | The PE runs on Windows whatever its extension | rustc adds `.exe` or Windows refuses, so step 2 fails | `py -3 scripts/check_facts.py 52` on Windows with rustc |
| CH2 | scripts/check_facts.py:67 `--experimental-strip-types` | Accepted on every supported node | A node that drops the flag fails 53.ts with "bad option" | Run 53.ts on the supported node range |
| CH3 | scripts/pre-commit:7-8 `py=python3` / `command -v "$py" >/dev/null 2>&1 \|\| py=python` | On Windows the `python3` Store alias stub is found and fails every commit | Git for Windows' sh does not see the alias | Commit on Windows with the alias on |
| CH4 | scripts/check.py:369 `if fence is None and i > 0 and DELIM.match(lines[i]) and "\|" in lines[i] + lines[i - 1]:` | A pipe line followed by `---` (a setext heading) is a false table error | No such line exists in the files | Append `a \| b\n---` to a copy of SKILL.md and run the check |
| CH5 | scripts/check.py:375 `while i < len(lines) and lines[i].strip() and "\|" in lines[i]:` | GFM continues a table on a non-blank line without a pipe, but the check stops there | GitHub ends the table there too | Render and compare |

## HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| CB1 | scripts/check.py:237 `first = re.search(r"^## +([0-9][0-9.]*)\b", read_text(root, CHANGELOG, rep), re.M)` | CHANGELOG.md:3 "the first entry below" | Non-numeric headings (`## Unreleased`, CHANGELOG.md:5) are skipped | None (intended; wording in Documentation D6) | 90 |
| CB2 | scripts/check.py:217 `badges = re.findall(r"badge/skill-v([0-9][0-9.]*)-", read_text(root, README, rep))` | Version agrees everywhere in the README | Only badges are read: README.md:125 `(currently 4.1)` is not caught | Preventive measure | 90 |
| CB3 | scripts/check.py:128 `if enc != "utf-8" and rep is not None and (rel in (SKILL, README, EVALS) or rel.startswith(REFS_DIR + "/")):` | Undocumented | A non-UTF-8 SKILL, README, evals or reference file is an error | None | 85 |
| CB4 | scripts/check.py:309 `rep.error(rel, "unreadable file, not checked")` | Unreadable file reported | A tracked file deleted but not staged is reported as unreadable in working-tree mode | None if intended | 80 |
| CB5 | scripts/check_facts.py:83 (as C20) | Runner reproduces the evals' facts | It ignores NOT_COMPUTABLE and runs 52.rs, which eval 52's reason says cannot run | Part of Data F1 | 85 |
| CB6 | scripts/check_facts.py:50 (as P9) | "assertion outside comments and strings" | Unreachable asserts count, and a SyntaxError counts as having an assertion | Preventive measure | 85 |
| CB7 | scripts/check_facts.py:100 `r = subprocess.run(step, cwd=FACTS, capture_output=True, text=True)` | Not stated | No timeout: a looping fact file hangs the hook | Preventive measure | 80 |

## ADVERSARIAL SCAFFOLD FINDINGS
- Reviewer blind spots: comments that state the intent (scripts/check.py:16, :399; scripts/check_facts.py:8; scripts/pre-commit:5) sit right next to code that does something else. A reader who trusts the comment misses C1–C4.
- Highest-risk claims: C1 (privacy gate off by default), C2 (terms printed), C3 (terms missed). All three were confirmed by the independent verifier.
- Multi-step traces: missing rustc → scripts/check_facts.py:92 skip → :113 exit 0 → scripts/pre-commit:17 discards output → commit with unchecked 52.rs. Data F1 → scripts/check.py:496 error → exit 1 → every `assert_passes` red, every commit blocked.
- Subtlety flags: the default argument at scripts/check.py:400; `?` vs `*` at scripts/check.py:90; `[:1]` at scripts/check.py:223.

### SUMMARY
- Domain: Code
- Claims: 12 verified (PASS), 25 in FAIL (6 demonstrated defects, 19 preventive measures), 0 falsified
- Survived: not returned
- Failure categories: 6 systemic patterns
- Invariants: not returned
- Hypotheses: 5
- Hidden behaviors: 7
- Findings by type: 6 demonstrated defects, 19 preventive measures, 0 falsified
- Critical issues: 0 critical; 4 high (C1–C4)
- Executed: none (reasoning only)
- Proposed: see PROPOSED EXECUTABLE CHECKS

---

## VERIFICATION DOMAIN
Data

## GROUND TRUTH
evals.json prompts and assertions, the fact files, NOT_COMPUTABLE, plugin.json, SKILL.md frontmatter, CHANGELOG.md headings; scripts/check.py as the contract enforcer.

## INVARIANTS
Not returned (see log). The touched invariant is "fact file or reason, not both" (scripts/check.py:36). It is enforced by scripts/check.py:495-496, which bites: the current tree fails it (F1).

## DECOMPOSED CLAIMS
1. Versions agree: .claude-plugin/plugin.json:3 `"version": "4.2",`. Deductive
2. Name and licence agree: .claude-plugin/plugin.json:2 `"name": "adversarial-verify",`. Deductive
3. evals.json ids are 1..n in file order; every assertion from eval 21 on is tagged. Inductive
4. An eval has a fact file or a NOT_COMPUTABLE reason, never both: skills/adversarial-verify/evals/facts/NOT_COMPUTABLE:13. Deductive
5. Each fact file computes its eval's stated facts (35–57). Deductive
6. Eval texts agree with the facts their file proves: skills/adversarial-verify/evals/evals.json:705, :612, :249. Deductive

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Stale state (copies of one value drifting) | skills/adversarial-verify/evals/facts/NOT_COMPUTABLE:13; skills/adversarial-verify/evals/evals.json:249 | NOT_COMPUTABLE, evals.json |
| Internal arithmetic inconsistency in eval texts | skills/adversarial-verify/evals/evals.json:705, :612 | evals.json |
| Assumed environment | skills/adversarial-verify/evals/facts/NOT_COMPUTABLE:13; evals.json:648 (cargo message format) | NOT_COMPUTABLE, evals.json |

## VERIFICATION RESULTS
### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| DP1 | Versions agree | .claude-plugin/plugin.json:3 `"version": "4.2",`; skills/adversarial-verify/SKILL.md:20; README.md:1 `badge/skill-v4.2-blue`; CHANGELOG.md:10 `## 4.2 - 2026-11-25`. 90 |
| DP2 | Name and licence | .claude-plugin/plugin.json:2 `"name": "adversarial-verify",`, :9 `"license": "MIT",`; LICENSE:1. 90 |
| DP3 | ids 1..57 in order | skills/adversarial-verify/evals/evals.json:5 `"id": 1,` … :711 `"id": 57,`. 85 |
| DP4 | Tags on evals 21+ | skills/adversarial-verify/evals/evals.json:282 `"[substance] Does not report 'the new test covers the fix'…`; evals 21–57 all tagged. 85 |
| DP5 | Every "(Facts" eval from 29 on is covered | skills/adversarial-verify/evals/facts/NOT_COMPUTABLE:4 `30: repository size and contents, no code`, plus the fact files. 80 (marker-limited, see C9) |
| DP6 | v1 accepts 31 February | skills/adversarial-verify/evals/facts/_parse_day.py:10 `if day < 1 or day > 31:` (row corrected on resend); skills/adversarial-verify/evals/facts/35.py:5 `assert parse_day_v1('2026-02-31') == (2026, 2, 31)`. 90 |
| DP7 | 39.py: 29 Feb 2024 separates parent and fix | skills/adversarial-verify/evals/facts/39.py:6 `assert raises(parse_day_parent, '2024-02-29') and not raises(parse_day_fixed, '2024-02-29')`; skills/adversarial-verify/evals/facts/_parse_day.py:32 `n = 29 if month == 2 and leap(year) else DAYS[month - 1]`. 85 |
| DP8 | 40.py mutant kills | skills/adversarial-verify/evals/facts/40.py:9 `assert killed == {'>= to <', '>= to <=', 'return True'}`. 90 |
| DP9 | 42.py survivors | skills/adversarial-verify/evals/facts/42.py:12 `assert run_tests(lambda t, c: round(t * 0.9, 2) if c else t)               # any non-empty code`. 85 |
| DP10 | 48.py contrast ratios | skills/adversarial-verify/evals/facts/48.py:20 `assert r('#3a3a3a', '#1e1e1e') == 1.47 < 3`; hand-computed. 85 |
| DP11 | 49.py widths | skills/adversarial-verify/evals/facts/49.py:13 `assert clipped(320) == (64.0, {'Bestellungen', 'Einstellungen'})`. 90 |
| DP12 | 51.py heights | skills/adversarial-verify/evals/facts/51.py:5 `assert (before, after) == (44, 24)`. 90 |
| DP13 | 52.rs returns 28 | skills/adversarial-verify/evals/facts/52.rs:8 `2 => 28,`. 90 |
| DP14 | 53.ts weekdays and survivors | skills/adversarial-verify/evals/facts/53.ts:9 `if (tests[0][0] !== 6 \|\| tests[1][0] !== 3) throw new Error("dates");`. 88 |
| DP15 | 56.py counts | skills/adversarial-verify/evals/facts/56.py:12 `assert (measured_survivors, measured, excluded) == (4, 108, 12)`. 92 |
| DP16 | 57.py counts | skills/adversarial-verify/evals/facts/57.py:8 `assert survived - quote_found == 2  # survivors with no standing row`. 92 |
| DP17 | 38.py k = 1 first failure | skills/adversarial-verify/evals/facts/38.py:19 `assert first == 1 and repr(old(0.01)) == '0.009000000000000001'`. 75 (float repr is run-only) |

### FALSIFIED HYPOTHESES
None.

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| F1 | skills/adversarial-verify/evals/facts/NOT_COMPUTABLE:13 | `52: the compiler is not installed on every machine` | Demonstrated defect | High | facts/52.rs exists, so scripts/check.py:473 puts 52 in `with_file`, :494 puts it in `reasons`, and :495-496 reports `eval 52 has a fact file and a reason not to have one`. check.py exits 1 on the repository. The hook (scripts/pre-commit:9) blocks every commit, and test_check.py:98 `self.assert_passes(self.run_check(terms=NONE))` and every other `assert_passes` go red. Reported by all four agents (Data rated it Medium, the other three High). **The independent verifier confirmed it (FAIL, 95)** | Deductive | 90 | Delete NOT_COMPUTABLE:13 |
| F2 | skills/adversarial-verify/evals/evals.json:705 | `"[substance] Gives the score on the measured mutants only (104 of 108, about 96%) and says that 11 are excluded: 8 timed out, 3 skipped, 1 not measured",` | Demonstrated defect | Medium | 8 + 3 + 1 = 12, which contradicts evals.json:699 `with 12 excluded` and skills/adversarial-verify/evals/facts/56.py:12. A grader following the assertion marks down a correct answer | Deductive | 95 | "12 are excluded" |
| F3 | skills/adversarial-verify/evals/evals.json:249 | `"Fills the INVARIANTS section of the report and the summary line 'Invariants: N found, M touched, K enforced by a mechanism that bites on the changed path (code, data) or respected (plans, specs, docs, analyses)'"` | Demonstrated defect | Medium | Eval 18 quotes the SUMMARY line word for word, but skills/adversarial-verify/SKILL.md:439 now reads `(code, data, tests, UX) … (plans, specs, docs, analyses, mock-ups)`. A literal grader fails a correct answer (category agent) | Deductive | 90 | Quote the current line, or assert the fields |
| F4 | skills/adversarial-verify/evals/evals.json:612 | `… and that at 320 px (80 px buttons, 64 px usable) more labels are clipped; …` | Demonstrated defect | Low | At 320 px the same two labels are clipped as at 375 px: evals.json:615 and skills/adversarial-verify/evals/facts/49.py:12-13 | Deductive | 92 | "the same labels are clipped with less room" |

## STRESS TEST RESULTS
Not returned.

## HYPOTHESES
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| DH1 | skills/adversarial-verify/evals/facts/35.py:1 `# prompt-sha256: a502f0639b93c074fd20190e3f58c7c630fa1d91a21742e31cdb07b968e7823b` (and line 1 of each fact file) | All 13 hashes match the current prompts | A prompt was edited after its fact file (56 and 57 are likely candidates: CHANGELOG.md:7-8) | `python3 scripts/check.py`: look for "prompt changed since its facts were checked" |
| DH2 | skills/adversarial-verify/evals/facts/38.py:21 `assert round(10.05 * 0.9, 2) == 9.05` | The product lies above 9.045 and rounds to 9.05 | It rounds to 9.04 | `python3 scripts/check_facts.py 38` |
| DH3 | skills/adversarial-verify/evals/facts/48.py:19 `assert r('#6b6b6b', '#1e1e1e') == 3.13 < 4.5 and r('#2563eb', '#1e1e1e') == 3.23 < 4.5` | 3.2259 rounds to 3.23 | Float error gives 3.22 | `python3 scripts/check_facts.py 48` |
| DH4 | skills/adversarial-verify/evals/facts/_parse_day.py:28 `def parse_day_fixed(text):  # eval 39, the commit as described` | The reconstructed fix matches the intended commit | Another leap-year rule behaves differently on 2100-02-29 | Compare with the author's diff |
| DH5 | skills/adversarial-verify/evals/evals.json:648 `left: 28, right: 29` | The message format is that of Rust 1.73 or later | Older toolchains print `assertion failed: (left == right)` | Run under the minimum Rust |
| DH6 | skills/adversarial-verify/evals/facts/NOT_COMPUTABLE:13 | The line predates 52.rs (CHANGELOG.md:25) | It was kept as a fallback for machines without rustc | Version history |

## HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| DB1 | skills/adversarial-verify/evals/facts/35.py:2 `"""Eval 35: the function as shown accepts 31 February, which the three valid-date tests do not cover."""` | Checks eval 35's facts | Checks only the acceptance of 31 February; the `3 passed` claim is not computable and has no reason line | None (undeclared partial coverage) | 85 |

### SUMMARY
- Domain: Data
- Claims: 17 verified, 4 in FAIL (4 demonstrated defects), 0 falsified
- Failure categories: 3
- Hypotheses: 6
- Hidden behaviors: 1
- Critical issues: 0 critical; 1 high (F1)

---

## VERIFICATION DOMAIN
Documentation

## GROUND TRUTH
README.md, CHANGELOG.md, the docstrings and comments, checked against the code, the manifest, the skill's references/ and the file tree.

## INVARIANTS
Not returned.

## DECOMPOSED CLAIMS
1. Install recipe: README.md:89 `cp skills/adversarial-verify/SKILL.md ~/.claude/skills/adversarial-verify/`. Deductive
2. Version statement: README.md:125. Deductive
3. The check's documented behaviours: README.md:247-264. Deductive
4. CHANGELOG entries match the skill: CHANGELOG.md:3, :7-8, :14-15, :24. Deductive / Abductive (sizes)
5. Fact-file headers and comments: skills/adversarial-verify/evals/facts/_parse_day.py:1, :5. Deductive

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Stale state | README.md:125, README.md:89, CHANGELOG.md:3, skills/adversarial-verify/evals/facts/_parse_day.py:1 | README.md, CHANGELOG.md, _parse_day.py |
| Spec drift (docs promise what code does not do) | README.md:261, :251, :250, :255; scripts/check.py:43 | README.md, scripts/check.py |

## VERIFICATION RESULTS
### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| DoP1 | references/ holds three files, each with its condition | README.md:109 ``three files in `references/` hold``; skills/adversarial-verify/references/ has execution.md, pre-code.md, ux.md. 92 |
| DoP2 | Mutation-copy rule | README.md:241 `the skill mutates a separate copy of the repository`; skills/adversarial-verify/references/execution.md:27. 92 |
| DoP3 | Storage-test rule | README.md:243 `a test whose subject is the storage itself is run on disk`; execution.md:41. 90 |
| DoP4 | evals.json check as described | README.md:249 `integer ids 1..n in file order`; scripts/check.py:186. 92 |
| DoP5 | Reference-file check as described | README.md:254 ``every `references/<name>.md` named in SKILL.md``; scripts/check.py:519. 90 |
| DoP6 | Trust example shape | README.md:279 `"dev": { "trust": 7, "clean_reviews": 0 },`; skills/adversarial-verify/examples/agent-trust.json:4-5. 85 |
| DoP7 | CHANGELOG 4.2/Unreleased rules exist | CHANGELOG.md:7 `every result is cited as path:line with the line quoted`; :8 `a row only looked up cannot carry a score above 79`; execution.md:51-62. 90 |
| DoP8 | Fact rule from 29 on | CHANGELOG.md:24 ``check.py` requires a file or a stated reason for every eval from 29 on that states facts``; scripts/check.py:500. 92 |
| DoP9 | Licence | .claude-plugin/plugin.json:9 `"license": "MIT",`; LICENSE:1. 95 |
| DoP10 | Test command | scripts/test_check.py:3 `Run from the repo root: python3 -m unittest scripts/test_check.py`; README.md:260. 90 |
| DoP11 | Hook comment on the facts | scripts/pre-commit:10 `# Eval facts: only when the staged change touches the evals, and on exactly the staged files.`; :12-15. 88 |
| DoP12 | Fact docstrings | e.g. skills/adversarial-verify/evals/facts/39.py:2 `"""Eval 39: test_rejects_31_april passes on the parent and on the commit; 29 Feb 2024 separates them."""`. 85 |
| DoP13 | Python 3.8, nothing else | README.md:247 ``needs `python3` 3.8 or later and nothing else``. 70 (inductive, not run) |

### FALSIFIED HYPOTHESES
None.

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| D1 | README.md:89 | `cp skills/adversarial-verify/SKILL.md ~/.claude/skills/adversarial-verify/` | Demonstrated defect | High | Copies only SKILL.md, which sends the verifier to references/*.md that are then missing. README.md:117 itself says: `SKILL.md alone would send the verifier to files that are not there.` | Deductive | 92 | `cp -r skills/adversarial-verify ~/.claude/skills/` |
| D2 | README.md:125 | ``The plugin declares its version in `.claude-plugin/plugin.json` (currently 4.1)`` | Demonstrated defect | Medium | .claude-plugin/plugin.json:3 says 4.2, and the check does not catch it (CB2) | Deductive | 95 | "currently 4.2", or drop the number |
| D3 | README.md:261 | `ln -s ../../scripts/pre-commit .git/hooks/pre-commit   # runs --strict --staged before every commit` | Demonstrated defect | High | Doc side of C1 (also scripts/pre-commit:5). Counted once, in Code C1 | Deductive | 93 | With C1 |
| D4 | scripts/check.py:43 | `reader nowhere. The folder is read as it is on disk, tracked or not, since` | Demonstrated defect | Low | Under `--staged` the root is the index export (scripts/check.py:433 `root = tmp`), so an untracked reference file is not seen. test_check.py:502-508 asserts exactly that | Deductive | 88 | "on disk in working-tree mode; the staged content with --staged" |
| D5 | skills/adversarial-verify/evals/facts/_parse_day.py:1 | `# Shared by facts/37.py and facts/39.py: the functions as shown in the evals.` | Demonstrated defect | Low | skills/adversarial-verify/evals/facts/35.py:3 `from _parse_day import parse_day_v1` also uses it | Deductive | 92 | "Shared by facts/35.py, 37.py and 39.py" |
| D6 | CHANGELOG.md:3 | `The version is the same in the skill's frontmatter, the README badge, `.claude-plugin/plugin.json` and the first entry below` | Demonstrated defect | Low | The first entry is `## Unreleased` (CHANGELOG.md:5). The check skips it (CB1) | Deductive | 85 | "the first numbered entry" |
| D7 | README.md:255 | `each fact file carries the sha256 of the prompt of every eval it covers` | Demonstrated defect | Low | A file is bound to the one eval named by its stem, and a single hash is read (scripts/check.py:477) | Deductive | 85 | ``each fact file `<id>.<ext>` carries the sha256 of eval `<id>`'s prompt`` |

(The doc sides of C2, C3, C4 and C6 are README.md:251, README.md:255, README.md:250 and CHANGELOG.md:3. They are counted once, in Code. The row at scripts/check_facts.py:8 was corrected on resend, from line 10.)

## STRESS TEST RESULTS
Not returned.

## HYPOTHESES
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| DoH1 | CHANGELOG.md:14 `The text read at every verification goes from 57.3 kB to 46.4 kB; a verification that needs all three files reads 62.5 kB.` | True at release 4.2 | The Unreleased edits to execution.md changed 62.5 kB | Measure the byte sizes at the tag and now |
| DoH2 | CHANGELOG.md:14 `No rule changed by the split` | Text moved verbatim | Wording changed in the move | Diff 4.1 SKILL.md against 4.2 SKILL.md + references |
| DoH3 | README.md:264 ``On Windows use `py -3 scripts/check.py` `` | The hook works on Windows | With only `py` on PATH, the hook exits 1 at scripts/pre-commit:9 | Commit on Windows with only `py` |

## HIDDEN BEHAVIORS DETECTED
None beyond those counted in Code.

### SUMMARY
- Domain: Documentation
- Claims: 13 verified, 6 in FAIL (6 demonstrated defects; D3 counted in Code), 0 falsified
- Failure categories: 2
- Hypotheses: 3
- Critical issues: 0 critical; 1 high counted here (D1)

---

## VERIFICATION DOMAIN
Tests

## GROUND TRUTH
scripts/test_check.py traced against scripts/check.py and scripts/check_facts.py; .gitignore; skills/adversarial-verify/SKILL.md for the table fixture.

## INVARIANTS
Not returned.

## DECOMPOSED CLAIMS
1. The repo passes its own check: scripts/test_check.py:98 `self.assert_passes(self.run_check(terms=NONE))`. Deductive
2. Every failing case is decided by the script's own ERROR and a token: scripts/test_check.py:4. Deductive
3. Each named test exercises the case it names (orphan, masking, toolchain, `--root`). Deductive
4. The tests run on every supported platform. Deductive

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Tautological / weak assertion | scripts/test_check.py:479, :316, :302, :500, :605, :617 | scripts/test_check.py |
| Test-environment artifact | scripts/test_check.py:43, :351, :503, :575-578 | scripts/test_check.py |
| Test-code drift | scripts/test_check.py:336-337 | scripts/test_check.py |
| Missing completeness | scripts/test_check.py:64 | scripts/test_check.py |

## VERIFICATION RESULTS
### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| TP1 | Tag boundary covered from both sides | scripts/test_check.py:158 `self.assertFalse(e["assertions"][0].startswith("["), "eval 20 is untagged by design")`; :153 `"id 21"`. 85 |
| TP2 | Evals failure tests hit the right check | scripts/test_check.py:110 `d = self.evals(); d["evals"][-1]["id"] = d["evals"][-2]["id"]; self.save_evals(d)`; :127. 85 |
| TP3 | Version tests break what they name | scripts/test_check.py:224 inserts `## 9.0 - unreleased`; :225. 85 |
| TP4 | Facts tests build on existing content | scripts/test_check.py:550 `d["evals"][36]["prompt"] = d["evals"][36]["prompt"].replace("day > 31", "day > 28")`. 88 |
| TP5 | Table tests use a row that exists | skills/adversarial-verify/SKILL.md:207 `\| **Frequency assumptions** \| Function assumed to be called exactly once per cycle \| Event handlers, callbacks, update loops \|`; scripts/test_check.py:422. 85 |
| TP6 | Staged tests check what they claim | scripts/test_check.py:385-386 `self.assert_fails(self.run_check("--staged", terms=T1), "leak.md")`. 85 |
| TP7 | Terms file gitignored | .gitignore:1 `.check-private-terms`; scripts/test_check.py:366. 95 |
| TP8 | The runner's own failure tests could fail | scripts/test_check.py:582 edits 38.py to `9.04`; scripts/check_facts.py:107. 85 |

### FALSIFIED HYPOTHESES
None.

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| T1 | scripts/test_check.py:479 | `self.assertIn("orphan.md", r.stdout + self.ref("orphan.md"))` | Demonstrated defect | Low | `self.ref("orphan.md")` always contains the name, so the assertion is always true and the test passes even with the orphan check deleted | Deductive | 95 | `self.assert_fails(r, "orphan.md", "never named in SKILL.md")` |
| T2 | scripts/test_check.py:575-578 | `def test_runner_passes_on_the_repo(self):` | Demonstrated defect | Medium | Without rustc or node, 52.rs and 53.ts are skipped (C4) and the test is green while proving nothing about them | Deductive | 80 | Assert no `skip` line |
| T3 | scripts/test_check.py:605 | `r = self.run_facts("49", "--root", self.tmp)` | Demonstrated defect | Low | `--root` equals the script's default root, so the test stays green even if `--root` were ignored | Deductive | 90 | Use a different root that holds a broken 49.py |
| T4 | scripts/test_check.py:617 | `self.assertNotEqual(r.returncode, 0, r.stdout)` | Demonstrated defect | Low | Only a non-zero code is asserted, so a traceback also passes, against scripts/test_check.py:4 `Every failing case must come from the script's own ERROR and summary` | Deductive | 85 | Assert `"0 fact file(s)"` and no traceback |
| T5 | scripts/test_check.py:43 | `env = dict(os.environ)` | Preventive measure | Medium | An inherited CHECK_PRIVATE_TERMS overrides the terms file, giving false reds (:357/:360) and false greens (:326/:329) for anyone who follows README.md:251 | Deductive | 85 | `env.pop("CHECK_PRIVATE_TERMS", None)` |
| T6 | scripts/test_check.py:64 | `def assert_passes(self, r):` | Preventive measure | Medium | `assert_no_leak` runs only in `assert_fails` (:62), so passing runs with terms configured are never checked for a leak, against scripts/test_check.py:4 | Deductive | 85 | Call `assert_no_leak` in `assert_passes` |
| T7 | scripts/test_check.py:336 | `def test_glued_term_in_output_is_masked_even_if_not_detected(self):` | Preventive measure | Low | It runs with `terms=T1` (substring), so the case it names is never run, and the comment at :337 `# whole-word detection does not flag "<term>labs"…` is wrong for it. It duplicates :331-334 | Deductive | 88 | Rename and fix the comment, or drop it |
| T8 | scripts/test_check.py:351 | `os.symlink(os.path.join(self.tmp, "does-not-exist"), self.path("dangling.md"))` | Preventive measure | Low | Without symlink privilege on Windows (README.md:264) this raises: a false red | Deductive | 80 | Skip on OSError |
| T9 | scripts/test_check.py:503 | `git = lambda *a: subprocess.run(["git", "-C", self.tmp, "-c", "user.name=t", "-c", "user.email=t@t", *a],` | Preventive measure | Low | No `skipUnless(shutil.which("git"))`, unlike StagedTest (:369) | Deductive | 85 | Add the decorator |
| T10 | scripts/test_check.py:316 | `self.assert_fails(self.run_check(terms=T1), "plugin.json")` | Preventive measure | Low | Any error on plugin.json satisfies it, and the same holds at :302 `"notes16.txt"` and :500 `self.assertIn("ux.md", r.stdout)` | Deductive | 80 | Add the specific message token |

## STRESS TEST RESULTS
Not returned.

## HYPOTHESES
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| TH1 | scripts/test_check.py:98, :171-173, :286, :341-344 expect behaviour that F1, C6, C3 and C2 prevent | The suite is red today (≤79: run-only) | Another code path satisfies them | `python3 -m unittest scripts/test_check.py` |
| TH2 | scripts/test_check.py:391-396 compares the shared temp directory before and after | Reliable when run alone | Flaky when suites run in parallel | Run two StagedTest copies at once |
| TH3 | scripts/test_check.py:414 `self.assertIn("SQLite", open(self.path(EVALS)).read())` | Works in every locale | A non-UTF-8 locale codec rejects the em dashes | Run under an ASCII-only locale with `-X utf8=0` |

## HIDDEN BEHAVIORS DETECTED
None beyond T1 and T7.

### SUMMARY
- Domain: Tests
- Claims: 8 verified, 10 in FAIL (4 demonstrated defects, 6 preventive measures), 0 falsified
- Failure categories: 4
- Hypotheses: 3
- Critical issues: 0 critical; 0 high

---

## CROSS-DOMAIN SUMMARY
- Domains: Code, Data, Documentation, Tests
- Claims: 50 verified, 45 in FAIL (20 demonstrated defects, 25 preventive measures; the duplicate D3 is counted once, in Code), 0 falsified
- High severity: Data F1 (NOT_COMPUTABLE:13, which fails the repository's own check and blocks every commit); Code C1 (the hook without `--strict`), C2 (terms printed unmasked), C3 (separated terms missed), C4 (toolchain skip); Documentation D1 (install copies only SKILL.md). 0 critical.
- Changes that touch several domains: C1 (scripts/pre-commit:9 plus README.md:261 and scripts/pre-commit:5); C6 (scripts/check.py:223, plus README.md:250, scripts/check.py:10 and test_check.py:171); C4 (scripts/check_facts.py:92, plus README.md:255 and test_check.py:575); F1 (NOT_COMPUTABLE:13, which fails check.py, the hook and every `assert_passes`); C7 (the hash binds only the prompt, which let Data F2 through).
- Hypotheses: 17. Hidden behaviors: 8.
- Independent verifier: 5 claims re-verified (Data F1, Code C1–C4). All 5 were confirmed as FAIL and none changed.
- Rows: 387 returned, 3 discarded at lookup, all 3 restored on resend, 0 dropped.
- Executed: nothing (reasoning only).
- Recommendation: do not trust the repository's gates as they stand. The commit gate is blocked by F1, and once F1 is fixed, C1–C4 leave the privacy and facts gates weaker than documented.

## PROPOSED EXECUTABLE CHECKS
| # | Claim | Confidence now | Check (command, test or query) | Confirms if | Refutes if | Cost and side effects | Status |
|---|-------|----------------|--------------------------------|-------------|------------|-----------------------|--------|
| 1 | The repo fails its own check (F1); the hashes match (DH1) | 90 / hypothesis | `python3 scripts/check.py` | "eval 52 has a fact file and a reason" printed; no "prompt changed" lines | No such error, or extra hash errors | Reads the working tree, writes nothing | proposed |
| 2 | The suite is red on F1, C2, C3, C6 (TH1) | 75 | `python3 -m unittest scripts/test_check.py` | test_repo_passes, test_second_badge_mismatch, the two-space subtest and test_whole_word_term_glued… fail | All green | Builds temp copies in the system temp folder, runs git in them | proposed |
| 3 | The float and rounding facts (DH2, DH3, 38.py:19) | 75 | `python3 scripts/check_facts.py 38 48` | `2 fact file(s), 0 failed` | A FAIL line | Runs two local Python files, writes nothing | proposed |
| 4 | Toolchain skip exits 0 (C4) | 90 | `PATH=<python only> python3 scripts/check_facts.py 52` | `skip 52.rs`, exit 0 | Exit 1 | Runs with a reduced PATH, writes nothing | proposed |
| 5 | Message format of eval 52 (DH5) | hypothesis | `cargo test` with the assert at 29, on the minimum Rust | `left: 28, right: 29` | Old format | Compiles in a temp crate | proposed |

Proposed writes (none made):
- skills/adversarial-verify/evals/facts/NOT_COMPUTABLE: delete line 13 (F1)
- scripts/pre-commit:9: add `--strict` (C1)
- scripts/check.py:400 `substring=True` (C2); :90 `[\W_]*` (C3); :223 `badges` (C6)
- scripts/check_facts.py:91-93: count a missing toolchain as failed (C4)
- skills/adversarial-verify/evals/evals.json:705 "12 are excluded" (F2); :249 current SUMMARY wording (F3); :612 wording (F4)
- README.md:89 `cp -r` (D1); :125 "4.2" (D2); :255 binding wording (D7); CHANGELOG.md:3 "first numbered entry" (D6); _parse_day.py:1 add 35.py (D5)
- scripts/test_check.py:479 real assertion (T1); :43 pop CHECK_PRIVATE_TERMS (T5); :64 leak check (T6)

Do you want me to run any of checks 1–5, and apply any of the proposed writes?
