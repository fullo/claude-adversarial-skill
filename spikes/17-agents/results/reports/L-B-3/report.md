# Adversarial verification: ./tree (23 files)

## INTAKE

- **Target:** every domain detected in the 23 files: **Code** (scripts/check.py, scripts/check_facts.py, scripts/pre-commit, evals/facts/*.py|.rs|.ts), **Tests** (scripts/test_check.py, the fact files used as checks), **Documentation** (README.md, CHANGELOG.md, docstrings, comments), **Data** (.claude-plugin/plugin.json, evals/evals.json, evals/facts/NOT_COMPUTABLE). No Architecture, Analysis or UX artifact was found in scope.
- **Depth:** standard. **Scope:** the whole of the 23 files (no diff, no version history). **Execution mode:** reasoning only. Nothing was run. All four choices were set by the request; none are defaults.
- **Cost estimate (large request, cost accepted in the request):** 23 files, 4 domains, about 160 decomposed claims, nothing run. Agents launched: 4 domain agents, 1 correction pass on the Code return, 1 independent verifier, and 1 category agent.
- **Rows:** 467 rows came back: 404 from the domain agents, 10 from the independent verifier, and 53 from the category agent. 6 were discarded because their quote was not at the named line, all in the first Code return. On resend, all 6 were corrected and none was dropped. The independent verifier **confirmed 5 of 5** high-risk FAIL verdicts and **changed 1** row: the Documentation agent's PASS on output masking (README.md:251) became a FAIL.
- Full per-agent returns: out/returns/Code-resend.md, Tests.md, Documentation.md, Data.md, IndependentVerifier.md, CategoryAgent.md. Below, each finding is counted once, in its primary domain. The "Found by" column names every agent that reported it.

Ground truth used by all agents: the code itself, skills/adversarial-verify/SKILL.md, skills/adversarial-verify/references/*.md, and evals.json read against the fact files. **Project invariants found:**
- "Terms are never printed" (scripts/check.py:22-23)
- "A missing toolchain is an error, never a silent skip" (scripts/check_facts.py:8)
- the version agreement rule (CHANGELOG.md:3, scripts/check.py:10-11)
- "file or reason, not both" (scripts/check.py:36)
- the hook runs `--strict --staged` (README.md:261)

All five are touched. Only the version rule and the "not both" rule are enforced by a mechanism that bites. The "not both" rule is currently violated by the tree itself (D-F1).

---

## DOMAIN: CODE

### DECOMPOSED CLAIMS
43 claims are listed in out/returns/Code-resend.md, all Deductive except fact-file hash equality (Abductive, run-only). Main ones:
- check 1 evals format (scripts/check.py:6)
- every badge compared (scripts/check.py:10)
- separator matching (scripts/check.py:16)
- masking (scripts/check.py:22)
- `--strict` (scripts/check.py:23)
- tables (scripts/check.py:30)
- facts "not both" (scripts/check.py:36)
- references (scripts/check.py:40)
- `--staged` (scripts/check.py:47)
- toolchain error (scripts/check_facts.py:8)
- assertion rule (scripts/check_facts.py:11)
- hook strict (scripts/pre-commit:5)
- staged facts (scripts/pre-commit:10)
- each fact file's arithmetic

### VERIFICATION RESULTS

#### PASS ✅
| # | Claim | Location | Quote | Confidence |
|---|-------|----------|-------|------------|
| C-P1 | evals.json format check rejects extra/missing keys, bool ids, gaps, untagged assertions from 21 | scripts/check.py:186 | `if type(i) is not int:  # bool is an int subclass: reject it` | 90 |
| C-P2 | plugin.json version and first numbered CHANGELOG entry are compared; `## Unreleased` skipped | scripts/check.py:237 | `first = re.search(r"^## +([0-9][0-9.]*)\b", read_text(root, CHANGELOG, rep), re.M)` | 92 |
| C-P3 | Plain terms match as substrings, `=` terms as whole words (detection) | scripts/check.py:265 | `whole_word = t.startswith("=") and not substring` | 90 |
| C-P4 | No-letter term is an error, short term a warning | scripts/check.py:269 | `rep.error("private terms", f"term #{k} has no letters or digits and cannot be checked")` | 92 |
| C-P5 | Without terms: warning; with `--strict`: error (in check.py itself) | scripts/check.py:297 | `(rep.error if strict else rep.warning)("private terms", msg)` | 95 |
| C-P6 | Table rows: escaped pipes and code spans ignored | scripts/check.py:345 | ``s = re.sub(r"`[^`]*`", "x", line).replace("\\|", "x").strip()`` | 85 |
| C-P7 | `--staged` checks the index content | scripts/check.py:389 | `subprocess.run(["git", "-C", root, "checkout-index", "-a", "--prefix=" + tmp + os.sep],` | 88 |
| C-P8 | Named reference files exist; unnamed .md files reported | scripts/check.py:519 | `for name in sorted(existing - named_in_skill):` | 90 |
| C-P9 | Fact file needs an Assert/Raise node and a last line `ok <id>` | scripts/check_facts.py:107 | `if out[-1:] != [f"ok {stem}"]:` | 90 |
| C-P10 | Id filter works; empty selection fails | scripts/check_facts.py:113 | `return 1 if failed or not files else 0` | 88 |
| C-P11 | Hook runs fact files on the staged copy | scripts/pre-commit:14 | `git checkout-index -a --prefix="$tmp/" \|\| { rm -rf "$tmp"; exit 1; }` | 85 |
| C-P12 | Plain terms are masked in output (falsified suspicion, independent verifier H-a) | scripts/check.py:409 | `if hit(where):` | 85 |

The arithmetic of the fact files (35, 37, 39, 40, 42, 48, 49, 51, 52, 53, 56, 57) is under Data (D-P rows). The PASS rows for these in the Code return that had no quoted line (Code PASS 27, 33, 34, 35, 39) are capped at 79, following the protocol.

#### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix | Found by |
|---|-----------|-------|------|----------|----------|------|------------|-----|----------|
| C-F1 | scripts/check_facts.py:91-93 | `if steps is None:` / `print(f"skip {name}: toolchain not found")` / `continue` | Demonstrated defect | high | Without rustc or node, 52.rs and 53.ts are skipped and `failed` stays 0, so scripts/check_facts.py:113 returns 0. This contradicts scripts/check_facts.py:8 ("never a silent skip") and README.md:255. In the hook, scripts/pre-commit:17 prints output only on failure, so the skip is invisible. **Independent verifier: FAIL (92), agrees.** | Deductive | 92 | Print `FAIL {name}: toolchain not found` and do `failed += 1` | Code, Tests, Documentation, Data, Category, Verifier |
| C-F2 | scripts/pre-commit:9 | `"$py" -I "$root/scripts/check.py" --staged --root "$root" \|\| exit 1` | Demonstrated defect | high | `--strict` is missing, although scripts/pre-commit:5 and README.md:261 say the hook runs it. With no terms configured, scripts/check.py:297 only warns and the commit goes through with private names unchecked. **Independent verifier: FAIL (92), agrees.** | Deductive | 92 | Add `--strict` to scripts/pre-commit:9 | all 4 domains, Category, Verifier |
| C-F3 | scripts/check.py:400 | `pats = term_patterns(terms)` | Demonstrated defect | high | The comment at scripts/check.py:399 says "substring patterns", but `substring` defaults to False, so `=` terms are masked only as whole words. A glued form is printed in clear, e.g. an eval key `<term>labs` printed by scripts/check.py:182, or a file name in a check-7 error. This contradicts scripts/check.py:22-23 and README.md:251. **Disagreement:** the Documentation agent marked README.md:251 "any output line containing a term is masked" as PASS. The Code agent (92), the category agent (85) and the **independent verifier (88)** say FAIL. The row is kept at the lower confidence. | Deductive | 88 | `term_patterns(terms, substring=True)` | Code, Category, Verifier (Documentation: PASS) |
| C-F4 | scripts/check.py:90 | `SEP = r"[\W_]?"  # anything that is not a letter or digit, possibly nothing` | Demonstrated defect | high | `?` allows at most one separator character. A term is missed when its parts are joined by two spaces, by " - ", or by a CRLF line break (`\r\n`; `\r` is kept by the reader). This contradicts scripts/check.py:16-17 and README.md:251. The subtest using `f"{a.upper()}  {b}"` at scripts/test_check.py:286 is red by trace. **Independent verifier: FAIL (92), agrees.** | Deductive | 90 | `SEP = r"[\W_]*"` (optionally bounded) | Code, Tests, Documentation, Category, Verifier |
| C-F5 | scripts/check.py:223 | `for b in badges[:1]:` | Demonstrated defect | medium | Only the first skill badge is compared, while scripts/check.py:10, README.md:250 and CHANGELOG.md:3 promise every badge. test_second_badge_mismatch (scripts/test_check.py:171) is red by trace. | Deductive | 90 | `for b in badges:` | all 4 domains, Category |
| C-F6 | scripts/pre-commit:12 | `if git diff --cached --name-only \| grep -q '^skills/adversarial-verify/evals/'; then` | Preventive measure | low | A commit that changes only scripts/check_facts.py (for example one that weakens the assertion rule) does not rerun the facts. | Deductive | 82 | Also match `^scripts/check_facts\.py$` | Code, Data, Category |
| C-F7 | scripts/pre-commit:15 | `out="$("$py" -I "$root/scripts/check_facts.py" --root "$tmp")"; rc=$?` | Preventive measure | medium | The working-tree checker runs against the staged tree, and the same holds for check.py at scripts/pre-commit:9. A staged fix to the checker is not what runs, and an unstaged weakened checker is. | Deductive | 80 | Run the checkers from `$tmp/scripts/` | Code, Category |
| C-F8 | scripts/check.py:248 | `if raw is not None:` | Preventive measure | medium | An exported but empty CHECK_PRIVATE_TERMS silently overrides .check-private-terms. Combined with C-F2, the commit passes with a warning only. | Deductive | 80 | Treat an empty variable as unset, or report which source was used | Code, Tests, Category |
| C-F9 | scripts/check.py:301 | `if os.path.basename(rel) == TERMS_FILE:` | Preventive measure | medium | A tracked `.check-private-terms` at any depth is skipped, so the list of private terms could be committed with no error. README.md:251 says it "is never committed". | Deductive | 80 | Exempt only the untracked root file, and error if one is tracked | Code, Category |
| C-F10 | scripts/check.py:227 | `plugin = json.loads(read_text(root, PLUGIN, rep))` | Preventive measure | low | Only ValueError is caught. A missing plugin.json, CHANGELOG or README raises OSError: a traceback with no summary, printed outside the mask. | Deductive | 80 | Catch OSError and report it as an error | Code, Documentation |
| C-F11 | scripts/check.py:363 | `if fence is None:` | Preventive measure | low | The fence character is stored (scripts/check.py:364) but never compared, so a ``` line inside a `~~~` block closes it. | Deductive | 82 | Close only on the same fence character and a length at least as long | Code, Tests, Category |
| C-F12 | scripts/check.py:436 | `if files or not args.staged:` | Preventive measure | low | `--staged` with an empty index runs no check, so `--strict` passes with no terms configured. | Deductive | 80 | Run the terms check regardless | Code, Category |
| C-F13 | scripts/check.py:316-317 | `except ValueError:` / `pass` | Preventive measure | low | In a .json file that does not parse, `\uXXXX`-escaped terms are not decoded and go unreported. | Deductive | 82 | Report invalid JSON, or decode escapes on the raw text | Category |
| C-F14 | scripts/check.py:128 | `if enc != "utf-8" and rep is not None and (rel in (SKILL, README, EVALS) or rel.startswith(REFS_DIR + "/")):` | Preventive measure | low | CHANGELOG.md and plugin.json, which check 2 reads, are not required to be UTF-8. | Deductive | 80 | Add PLUGIN and CHANGELOG to the list | Tests, Category |
| C-F15 | scripts/check.py:511 | `for rel in [SKILL] + refs:` | Preventive measure | low | README.md:113-115 also names the reference files and is never checked, so a rename leaves the README stale. | Deductive | 80 | Include README.md in check 7 | Category |
| C-F16 | scripts/check_facts.py:85 | `files = [f for f in files if os.path.splitext(f)[0] in ids]` | Preventive measure | low | Requested ids without a file are dropped silently: `38 999` runs only 38 and exits 0. | Deductive | 85 | Error on unknown ids | Category |
| C-F17 | scripts/check_facts.py:50 | `return any(isinstance(n, (ast.Assert, ast.Raise)) for n in ast.walk(tree))` | Preventive measure | low | `assert True`, or an assert in a function that is never called, satisfies the rule. | Deductive | 80 | Require a top-level assert, or document the limit | Code, Tests, Category |
| C-F18 | scripts/check_facts.py:37 | `".rs": re.compile(r'//[^\n]*\|/\*.*?\*/\|"(?:\\.\|[^"\\])*"', re.S),` | Preventive measure | low | Raw strings and `'"'` char literals are not handled, so assertion detection can be wrong. | Deductive | 65 | Handle raw strings and char literals | Tests, Category |
| C-F19 | scripts/check_facts.py:64 | `node = shutil.which("node")` | Preventive measure | low | Only presence is checked. A node older than 22.6 fails on `--experimental-strip-types` (scripts/check_facts.py:67) with a generic FAIL, not a version message. | Deductive | 75 | Check `node --version` | Documentation, Verifier |
| C-F20 | scripts/pre-commit:7-8 | `py=python3` / `command -v "$py" >/dev/null 2>&1 \|\| py=python` | Preventive measure | low | On Windows, `python3` may be the Store stub and `python` may not be Python 3. | Abductive | 55 | Try `py -3` and check the version | Data, Category |
| C-F21 | scripts/pre-commit:1 | `#!/bin/sh` | Preventive measure | medium | There is no .gitattributes in ./tree, so on a Windows autocrlf checkout the copied hook gets CRLF and sh fails. | Abductive | 55 | Add `scripts/pre-commit text eol=lf` | Category |

### HYPOTHESES
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| C-H1 | scripts/check_facts.py:62 `exe = os.path.join(tmp, os.path.basename(path) + ".bin")` | Windows runs the `.bin` PE | rustc writes `.bin.exe`, or CreateProcess refuses the name | `py -3 scripts/check_facts.py 52` on Windows with rustc |
| C-H2 | scripts/check_facts.py:100 `r = subprocess.run(step, cwd=FACTS, capture_output=True, text=True)` | ASCII output, no issue | cp1252 decoding raises UnicodeDecodeError on non-ASCII toolchain output | Fact file printing non-ASCII to stderr on Windows |
| C-H3 | scripts/check.py:494 `reasons[int(m.group(1))] = m.group(2)` | The reason line for 52 predates 52.rs | 52.rs was meant to be removed | `git log -- skills/adversarial-verify/evals/facts/` (no .git in ./tree) |

### HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type | Confidence |
|---|----------|-----------|--------|------|------------|
| C-HB1 | scripts/check_facts.py:92 `print(f"skip {name}: toolchain not found")` | Missing toolchain is an error (scripts/check_facts.py:8) | Skip, exit 0 | Defect (C-F1) | 92 |
| C-HB2 | scripts/pre-commit:17 `[ $rc -eq 0 ] \|\| { printf "%s\n" "$out"; exit 1; }` | Hook runs the fact files | Output, including "skip" lines, shown only on failure | Defect, compounds C-F1 | 88 |
| C-HB3 | scripts/check.py:400 `pats = term_patterns(terms)` | Comment at scripts/check.py:399: substring patterns | Whole-word patterns for `=` terms | Defect (C-F3) | 88 |
| C-HB4 | scripts/check.py:223 `for b in badges[:1]:` | Every badge | First badge only | Defect (C-F5) | 90 |
| C-HB5 | scripts/check.py:90 `SEP = r"[\W_]?"` | "anything" between parts | One character at most | Defect (C-F4) | 90 |
| C-HB6 | scripts/pre-commit:9 `"$py" -I "$root/scripts/check.py" --staged --root "$root" \|\| exit 1` | `--strict --staged` | No `--strict` | Defect (C-F2) | 92 |
| C-HB7 | scripts/check_facts.py:57 `return [[sys.executable, "-E", "-s", path]]` | The hook runs isolated (`-I`) | Fact files run with -E -s so that `_parse_day` imports work | Not a problem | 85 |

---

## DOMAIN: TESTS

### DECOMPOSED CLAIMS
29 claims are listed in out/returns/Tests.md. Main ones:
- the repo passes (scripts/test_check.py:98)
- the runner test shows every fact ran (scripts/test_check.py:578)
- the orphan test (scripts/test_check.py:479)
- the `--root` test (scripts/test_check.py:605)
- env isolation (scripts/test_check.py:43)
- the hash-change test (scripts/test_check.py:550)
- the false-fact test (scripts/test_check.py:582)
- the no-assertion tests (scripts/test_check.py:588, :599)
- the staged tests (scripts/test_check.py:382)

All Deductive except float/hash facts (run-only).

### VERIFICATION RESULTS

#### PASS ✅
| # | Claim | Location | Quote | Confidence |
|---|-------|----------|-------|------------|
| T-P1 | Prompt edited after facts fails (eval 37) | scripts/test_check.py:550 | `d["evals"][36]["prompt"] = d["evals"][36]["prompt"].replace("day > 31", "day > 28")` | 75 (test result, run-only) |
| T-P2 | Runner catches a false fact | scripts/test_check.py:582 | `self.edit(os.path.join(FACTS, "38.py"), "assert round(10.05 * 0.9, 2) == 9.05", "assert round(10.05 * 0.9, 2) == 9.04")` | 75 |
| T-P3 | Runner fails a file with no assertion | scripts/test_check.py:588 | `self.edit(os.path.join(FACTS, "49.py"), "assert clipped(375)", "x = clipped(375)")` | 75 |
| T-P4 | `assert` in comments/strings does not count | scripts/test_check.py:599 | `open(path, "w").write(first + "\n# this file should assert the heights\nx = 'assert'\nprint('ok 51')\n")` | 75 |
| T-P5 | Table test edits a real SKILL.md row | scripts/test_check.py:422 | `self.edit(SKILL, "\| **Frequency assumptions** \|", "\| **Frequency assumptions** ")` | 75 |
| T-P6 | Staged leak with a clean working tree is caught | scripts/test_check.py:382 | `def test_staged_leak_with_clean_working_tree(self):` | 75 |

#### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix | Found by |
|---|-----------|-------|------|----------|----------|------|------------|-----|----------|
| T-F1 | scripts/test_check.py:578 | `self.assertRegex(r.stdout, r"\d+ fact file\(s\), 0 failed")` | Demonstrated defect (test-environment artifact) | medium | On a machine without rustc/node, 52.rs and 53.ts are skipped (C-F1) and test_runner_passes_on_the_repo is still green. | Deductive | 85 | `assertNotIn("skip ", r.stdout)`, plus a test with rustc removed from PATH expecting a non-zero exit | Tests, Code, Data, Documentation, Category |
| T-F2 | scripts/test_check.py:479 | `self.assertIn("orphan.md", r.stdout + self.ref("orphan.md"))` | Demonstrated defect (tautological) | medium | The haystack always contains "orphan.md", so the assertion is green whatever check.py does. | Deductive | 95 | `self.assert_fails(r, "orphan.md", "never named in SKILL.md")` | all 4 domains, Category |
| T-F3 | scripts/test_check.py:43 | `env = dict(os.environ)` | Preventive measure (test-environment artifact) | medium | A developer who exports CHECK_PRIVATE_TERMS, as README.md:251 offers, gets false reds in the missing-terms tests and a vacuous pass in test_terms_file_itself_is_not_scanned. | Deductive | 85 | `env.pop("CHECK_PRIVATE_TERMS", None)` | Tests, Category |
| T-F4 | scripts/test_check.py:605 | `r = self.run_facts("49", "--root", self.tmp)` | Demonstrated defect (unfalsifiable) | low | `--root` equals the default root of the copied runner, so the test is green even if `--root` were ignored. | Deductive | 88 | Point `--root` at a second copy with a failing 49.py | Tests |
| T-F5 | scripts/test_check.py:337 | `# whole-word detection does not flag "<term>labs", but the evals check prints the key name` | Demonstrated defect (test-code drift) | low | `terms=T1` uses substring detection, so `<term>labs` is detected. The test duplicates scripts/test_check.py:331-334. | Deductive | 88 | Fix the comment and the name, or delete the test | Tests |
| T-F6 | scripts/test_check.py:516 | `class FactsTest(Base):` | Preventive measure (missing negative tests) | medium | Searched all of scripts/test_check.py: there is no test for a missing toolchain, .rs/.ts assertion detection, "no version badge" or "no version entry", non-UTF-8 SKILL.md, the FACTS_FROM=29 boundary, or mixed fence characters. C-F1 is one regression already present. | Deductive | 82 | One failing case per message | Tests, Documentation |
| T-F7 | scripts/test_check.py:503 | `git = lambda *a: subprocess.run(["git", "-C", self.tmp, "-c", "user.name=t", "-c", "user.email=t@t", *a],` | Preventive measure (false red) | low | Unlike StagedTest (scripts/test_check.py:369), this test has no `skipUnless(shutil.which("git"))`. The symlink at scripts/test_check.py:351 likewise errors on Windows without the symlink privilege. | Deductive | 80 | Add the skip guards | Tests, Code, Category |
| T-F8 | scripts/test_check.py:31 | `self.tmp = tempfile.mkdtemp()` | Preventive measure (test-environment artifact) | low | Most tests run on a non-git copy, where scripts/check.py takes the os.walk path and scans untracked files. Production uses `git ls-files`. | Deductive | 75 | Run the scan tests in a git-initialised copy too | Category |
| T-F9 | scripts/test_check.py:32 | `for item in ("README.md", "CHANGELOG.md", "skills", ".claude-plugin", "scripts", ".gitignore"):` | Preventive measure | low | LICENSE and any new top-level file are not copied, so test_repo_passes does not cover the whole repository. | Deductive | 70 | Copy the whole tree except .git | Category |
| T-F10 | skills/adversarial-verify/evals/facts/35.py:2 | `"""Eval 35: the function as shown accepts 31 February, which the three valid-date tests do not cover."""` | Preventive measure | low | The file asserts only the parse result. "The three valid-date tests do not cover" it is not checked, and eval 36's similar fact is in NOT_COMPUTABLE. | Deductive | 80 | Reword the docstring, or move the claim to NOT_COMPUTABLE | Tests, Category |
| T-F11 | skills/adversarial-verify/evals/facts/52.rs:15 | `assert_ne!(days_in_month(2024, 2), 29);` | Preventive measure | low | Implied by skills/adversarial-verify/evals/facts/52.rs:14, so it can never fail on its own. | Deductive | 90 | Drop it, or keep it as documentation | Category |

### HYPOTHESES
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| T-H1 | Data D-F1 makes scripts/check.py exit 1 on the tree. C-F5 and C-F4 contradict scripts/test_check.py:171 and :286. | The suite is currently red: about 20 `assert_passes` tests, test_second_badge_mismatch, and one subTest | The suite has not been run since those lines took their current form | `python3 -m unittest scripts/test_check.py` |
| T-H2 | scripts/test_check.py:565 `self.assert_fails(self.run_check(terms=NONE), "NOT_COMPUTABLE", f"eval {i} has a fact file and a reason")` | No failure test passes only because of the baseline error | A token such as "NOT_COMPUTABLE" also matches the baseline error for eval 52 | Revert each test's edit and check that the test goes red |
| T-H3 | scripts/test_check.py:414 `self.assertIn("SQLite", open(self.path(EVALS)).read())` has no encoding | It reads fine under cp1252 by chance | An undefined cp1252 byte raises UnicodeDecodeError | Run under a cp1252 code page |
| T-H4 | Tests run `git commit` with the global git config (scripts/test_check.py:503) | Typical configs are harmless | `commit.gpgsign` or GIT_DIR makes them error or act on another repo | Run with `GIT_CONFIG_GLOBAL` setting `commit.gpgsign=true` |

### HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type | Confidence |
|---|----------|-----------|--------|------|------------|
| T-HB1 | scripts/test_check.py:577 `self.assertEqual(r.returncode, 0, r.stdout + r.stderr)` | The runner test proves the facts hold | Green with 52.rs/53.ts skipped | Test-environment artifact (T-F1) | 85 |
| T-HB2 | scripts/test_check.py:479 `self.assertIn("orphan.md", r.stdout + self.ref("orphan.md"))` | Detects an unnamed reference file | Always true | Defect (T-F2) | 95 |

---

## DOMAIN: DOCUMENTATION

### DECOMPOSED CLAIMS
55 claims are listed in out/returns/Documentation.md: the README feature descriptions against SKILL.md, the install recipes, the repository-check descriptions (README.md:247-261), the CHANGELOG entries, the script docstrings, and the fact-file headers. All Deductive except the external mutation-tool table, cross-agent compatibility, and the size figures (Abductive).

### VERIFICATION RESULTS

#### PASS ✅
| # | Claim | Location | Quote | Confidence |
|---|-------|----------|-------|------------|
| Doc-P1 | Badge, plugin.json, frontmatter and newest CHANGELOG entry agree on 4.2 | README.md:1 | `[![Skill Version](https://img.shields.io/badge/skill-v4.2-blue)](skills/adversarial-verify/SKILL.md)` | 92 |
| Doc-P2 | Reference-file table matches SKILL.md:49-51 | README.md:113 | `` \| `references/pre-code.md` \| the artifact proposes work not yet done, or is a spike or prototype report \| `` | 90 |
| Doc-P3 | Seven failure categories match SKILL.md:207-213 | README.md:63 | `frequency assumptions, implicit ordering, stale state, missing completeness, silent fallthrough, assumed environment, test-environment artifact` | 92 |
| Doc-P4 | Stress rule and scoring match SKILL.md:290, :335-343 | README.md:72, README.md:78 | `Four techniques with forced variety` / `Confidence scoring is tied to reasoning mode` | 90 |
| Doc-P5 | evals.json check described correctly | README.md:249 | `the same four keys in every case, integer ids 1..n in file order` | 90 |
| Doc-P6 | Tables check described correctly | README.md:253 | `with or without outer pipes, has as many cells as its header` | 88 |
| Doc-P7 | Trust rules match SKILL.md:466 | README.md:270 | `Each demonstrated defect: **-1 trust**` | 90 |
| Doc-P8 | Unreleased items exist in execution.md and evals 56/57 | CHANGELOG.md:7 | `**Long outputs** (\`references/execution.md\`)` | 88 |
| Doc-P9 | Facts rule and manifest fields described correctly | CHANGELOG.md:24 | `` `check.py` requires a file or a stated reason for every eval from 29 on that states facts `` | 90 |
| Doc-P10 | Hook trigger and staged copy described correctly | scripts/pre-commit:10 | `# Eval facts: only when the staged change touches the evals, and on exactly the staged files.` | 85 |
| Doc-P11 | Test terms do not occur in the repo | scripts/test_check.py:23 | `# including this one (the check scans every file). Neither occurs in the repo.` | 85 |

**Overturned:** Documentation PASS P7 ("any output line containing a term is masked", README.md:251) was contradicted by the independent verifier. It is now reported as C-F3, with both verdicts.

#### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix | Found by |
|---|-----------|-------|------|----------|----------|------|------------|-----|----------|
| Doc-F1 | README.md:89 | `cp skills/adversarial-verify/SKILL.md ~/.claude/skills/adversarial-verify/` | Demonstrated defect | high | The first install method copies SKILL.md alone, but SKILL.md:49-51 sends the verifier to references/*.md, which are then missing. README.md:117 says so itself. | Deductive | 92 | `cp -r skills/adversarial-verify ~/.claude/skills/` | Documentation, Category |
| Doc-F2 | README.md:125 | `The plugin declares its version in .claude-plugin/plugin.json (currently 4.1)` | Demonstrated defect | low | .claude-plugin/plugin.json:3 says `"4.2"`. The same sentence claims it equals the badge (v4.2). Check 2 reads only badges (scripts/check.py:217). | Deductive | 95 | Drop the number, or write 4.2 | all 4 domains, Category |
| Doc-F3 | scripts/check_facts.py:8 | `A missing toolchain is an error, never a silent skip.` | Demonstrated defect | medium | Contradicted by scripts/check_facts.py:91-93. README.md:255 repeats the claim. Counted with C-F1 (fix the code, not the doc). | Deductive | 90 | Same as C-F1 | Category, all domains (via C-F1) |
| Doc-F4 | README.md:261 | `ln -s ../../scripts/pre-commit .git/hooks/pre-commit   # runs --strict --staged before every commit` | Demonstrated defect | medium | The hook does not pass `--strict`. Counted with C-F2. | Deductive | 92 | Same as C-F2 | all domains |
| Doc-F5 | README.md:46 | `- **Propose project doc updates** — TODO.md, SPEC.md, PLAN.md (with user confirmation)` | Demonstrated defect | low | SKILL.md:462 also lists CHANGELOG.md, ADR/ and the agent instruction files. | Deductive | 85 | List the full Step 5 set | Documentation |
| Doc-F6 | README.md:247 | `` It needs `python3` 3.8 or later and nothing else. `` | Demonstrated defect | low | `--staged`, which the hook always uses, needs git (scripts/check.py:389). | Deductive | 85 | "…and git for --staged" | Documentation, Category |
| Doc-F7 | README.md:254 | `` and every file in `references/` is named in SKILL.md `` | Demonstrated defect | low | Only .md files are checked (scripts/check.py:137, and the docstring at scripts/check.py:40-41). | Deductive | 85 | "every .md file" | Documentation, Category |
| Doc-F8 | skills/adversarial-verify/evals/facts/_parse_day.py:1 | `# Shared by facts/37.py and facts/39.py: the functions as shown in the evals.` | Demonstrated defect | low | skills/adversarial-verify/evals/facts/35.py:3 also imports it. | Deductive | 95 | "Shared by facts/35.py, 37.py and 39.py" | all 4 domains, Category |
| Doc-F9 | skills/adversarial-verify/evals/evals.json:329 | `Proposes adding the new evidence to #41` | Demonstrated defect | medium | Evals 25-26 (evals.json:323-344) assert issue-tracker behaviour. The agent searched SKILL.md and references/*.md for "issue", "tracker" and "duplicate" and found no rule that specifies it. | Deductive | 80 | Add the rule to SKILL.md, or rewrite the evals | Documentation |
| Doc-F10 | CHANGELOG.md:3 | `` The version is the same in the skill's frontmatter, the README badge, `.claude-plugin/plugin.json` and the first entry below `` | Demonstrated defect | low | The first entry below is `## Unreleased` (CHANGELOG.md:5). The code uses the first *numbered* entry (scripts/check.py:237). | Deductive | 85 | "the first numbered entry below" | Category |

### HYPOTHESES
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| Doc-H1 | CHANGELOG.md:14 "The text read at every verification goes from 57.3 kB to 46.4 kB; a verification that needs all three files reads 62.5 kB." | The figures are right for 4.2 | They are stale after the Unreleased additions to execution.md | Byte-count the files at 4.2 and now |
| Doc-H2 | README.md:226 "Every cell comes from the tool's official documentation, read on 2026-10-21" | Accurate at that date | Flags changed or were misread | Compare with each tool's docs (outside ./tree, not read) |
| Doc-H3 | README.md:287 "works with Claude Code, Cursor, Windsurf, Cline and other compatible agents." | Compatible in format only | Untested on some of these agents | Load the skill in each agent |
| Doc-H4 | CHANGELOG.md:8 "This is a part of #18, written before the spike of #17." | References correct | Wrong issue numbers | Open issues #17 and #18 |

### HIDDEN BEHAVIORS DETECTED
None specific to Documentation. The documentation/code contradictions are listed as C-HB1 to C-HB6.

---

## DOMAIN: DATA

### DECOMPOSED CLAIMS
35 claims are listed in out/returns/Data.md:
- manifest version and fields (.claude-plugin/plugin.json:3)
- evals.json structure (skills/adversarial-verify/evals/evals.json:5)
- facts coverage from eval 29 (scripts/check.py:500)
- "not both" (scripts/check.py:36)
- hash binding (scripts/check.py:478)
- NOT_COMPUTABLE format (skills/adversarial-verify/evals/facts/NOT_COMPUTABLE:2)
- each fact file reproducing its eval's prompt and numbers
- eval assertions and expected outputs agreeing with their fact files

### VERIFICATION RESULTS

#### PASS ✅
| # | Claim | Location | Quote | Confidence |
|---|-------|----------|-------|------------|
| D-P1 | Manifest is valid; version is the string "4.2" | .claude-plugin/plugin.json:3 | `"version": "4.2",` | 90 |
| D-P2 | evals.json ids 1..57 in order, four keys, tags from eval 21 (evals 1-20 sampled) | skills/adversarial-verify/evals/evals.json:5 | `"id": 1,` | 75 (inductive) |
| D-P3 | Every eval ≥29 with "(Facts" has a file or a reason | scripts/check.py:500 | `if "(Facts" in str(e.get("prompt", "")) and e["id"] not in with_file and e["id"] not in reasons:` | 88 |
| D-P4 | Every fact file names an existing eval | scripts/check.py:470 | `if not stem.isdigit() or int(stem) not in ids:` | 92 |
| D-P5 | parse_day_v1 / parse_day_parent match the prompts of evals 29/35/37/39 | skills/adversarial-verify/evals/facts/_parse_day.py:15 | `def parse_day_parent(text):  # eval 39, parent commit` | 88 |
| D-P6 | Eval 40 kill set | skills/adversarial-verify/evals/facts/40.py:9 | `assert killed == {'>= to <', '>= to <=', 'return True'}` | 92 |
| D-P7 | Eval 42 variants survive (float, run-only) | skills/adversarial-verify/evals/facts/42.py:10 | `assert run_tests(lambda t, c: t * 0.9 if c == 'WELCOME10' else t)          # round removed` | 78 |
| D-P8 | Eval 48 WCAG ratios (3.23 lies near a rounding edge, see D-H2) | skills/adversarial-verify/evals/facts/48.py:19 | `assert r('#6b6b6b', '#1e1e1e') == 3.13 < 4.5 and r('#2563eb', '#1e1e1e') == 3.23 < 4.5` | 75 |
| D-P9 | Eval 49 widths and clipped sets | skills/adversarial-verify/evals/facts/49.py:13 | `assert clipped(320) == (64.0, {'Bestellungen', 'Einstellungen'})` | 95 |
| D-P10 | Eval 51 heights | skills/adversarial-verify/evals/facts/51.py:5 | `assert (before, after) == (44, 24)` | 95 |
| D-P11 | Eval 52 function copy and red result | skills/adversarial-verify/evals/facts/52.rs:14 | `assert_eq!(days_in_month(2024, 2), 28); // so assert_eq!(.., 29) fails: left 28, right 29` | 85 |
| D-P12 | Eval 53 weekdays and survivors | skills/adversarial-verify/evals/facts/53.ts:19 | `const expected = ["0 -> 1", "day === 0 -> false"];` | 88 |
| D-P13 | Eval 56 totals: 108 measured, 12 excluded, 96% | skills/adversarial-verify/evals/facts/56.py:12 | `assert (measured_survivors, measured, excluded) == (4, 108, 12)` | 95 |
| D-P14 | Eval 57 totals | skills/adversarial-verify/evals/facts/57.py:8 | `assert survived - quote_found == 2  # survivors with no standing row` | 95 |
| D-P15 | Eval 35/37/39 date facts | skills/adversarial-verify/evals/facts/39.py:6 | `assert raises(parse_day_parent, '2024-02-29') and not raises(parse_day_fixed, '2024-02-29')` | 92 |
| D-P16 | NOT_COMPUTABLE lines are well formed | skills/adversarial-verify/evals/facts/NOT_COMPUTABLE:4 | `30: repository size and contents, no code` | 92 |

#### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix | Found by |
|---|-----------|-------|------|----------|----------|------|------------|-----|----------|
| D-F1 | skills/adversarial-verify/evals/facts/NOT_COMPUTABLE:13 | `52: the compiler is not installed on every machine` | Demonstrated defect | high | skills/adversarial-verify/evals/facts/52.rs exists. scripts/check.py:473 puts 52 in `with_file`, this line puts it in `reasons`, and scripts/check.py:495-496 reports "eval 52 has a fact file and a reason not to have one". So scripts/check.py exits 1 on the tree as it stands, the hook (scripts/pre-commit:9) blocks every commit, and every `assert_passes` test is red by trace. **Independent verifier: FAIL (92), agrees.** The verifier rated severity medium; the domain agents rated it high. | Deductive | 90 | Delete NOT_COMPUTABLE:13 | all 4 domains, Category, Verifier |
| D-F2 | skills/adversarial-verify/evals/evals.json:705 | `says that 11 are excluded: 8 timed out, 3 skipped, 1 not measured` | Demonstrated defect | medium | 8+3+1 = 12. The eval's own expected output (skills/adversarial-verify/evals/evals.json:699, "with 12 excluded") and skills/adversarial-verify/evals/facts/56.py:12 both say 12. A grader penalises the correct answer. | Deductive | 95 | "12 are excluded" | all 4 domains, Category |
| D-F3 | skills/adversarial-verify/evals/evals.json:612 | `and that at 320 px (80 px buttons, 64 px usable) more labels are clipped` | Demonstrated defect | low | At 320 px the clipped set is still the same two labels (skills/adversarial-verify/evals/facts/49.py:13). The eval's own assertion at evals.json:615 says the others fit. | Deductive | 92 | "the same two labels are clipped, with less margin" | all 4 domains, Category |
| D-F4 | skills/adversarial-verify/evals/evals.json:249 | `K enforced by a mechanism that bites on the changed path (code, data) or respected` | Demonstrated defect | low | The assertion quotes an older form of the summary line. SKILL.md:439 now reads "(code, data, tests, UX) … mock-ups". | Deductive | 90 | Update the quoted line | Category |
| D-F5 | scripts/check.py:500 | `if "(Facts" in str(e.get("prompt", "")) and e["id"] not in with_file and e["id"] not in reasons:` | Demonstrated defect | low | Evals 54 and 55 (evals.json:672, :686) state computable facts without the "(Facts" marker, so they have neither a fact file nor a reason and the check never notices. | Deductive | 85 | Add the marker to those prompts, or widen the trigger | Category |
| D-F6 | scripts/check.py:478 | `want = hashlib.sha256(prompts[i].encode("utf-8")).hexdigest()` | Preventive measure | medium | Only the prompt is bound. Numbers restated in expected_output and assertions drift unchecked, which is how D-F2 and D-F3 got through. | Deductive | 85 | Hash the whole eval, or assert the restated numbers in the fact files | Code, Tests, Data, Category |
| D-F7 | scripts/check.py:494 | `reasons[int(m.group(1))] = m.group(2)` | Preventive measure | low | Reasons for evals that do not exist, for ids below 29, for evals without facts, or duplicated ids are accepted silently. | Deductive | 82 | Validate the id | Code, Data, Documentation |
| D-F8 | scripts/check.py:473 | `with_file[int(stem)] = name` | Preventive measure | low | Two fact files with the same id: only the last one is hash-checked, but check_facts.py runs both. | Deductive | 82 | Error on a duplicate stem | Code, Data |
| D-F9 | skills/adversarial-verify/evals/facts/_parse_day.py:5 | `def parse_day_v1(text):  # evals 29, 35 and 37` | Preventive measure | low | The shared helper has no prompt hash (scripts/check.py:469 skips `_` stems), so it can drift from the prompts while 35/37/39 keep valid hashes. | Deductive | 78 | Bind the helper, or inline it | Category |

### HYPOTHESES
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| D-H1 | skills/adversarial-verify/evals/facts/35.py:1 `# prompt-sha256: a502f0639b93c074fd20190e3f58c7c630fa1d91a21742e31cdb07b968e7823b` (and line 1 of every fact file) | All hashes match the current prompts | A prompt (e.g. 56 or 57) was edited after hashing | `python3 scripts/check.py`: look for "prompt changed since its facts were checked" |
| D-H2 | skills/adversarial-verify/evals/facts/48.py:19 expects 3.23. A hand computation gives about 3.2255, close to the 3.225 rounding edge. | The exact value rounds to 3.23 | It rounds to 3.22 | `python3 scripts/check_facts.py 48` |
| D-H3 | skills/adversarial-verify/evals/facts/38.py:21 `assert round(10.05 * 0.9, 2) == 9.05` | The product is above 9.045 | It rounds to 9.04 | `python3 scripts/check_facts.py 38` |
| D-H4 | skills/adversarial-verify/evals/evals.json:29 `Abstracts to failure category: 'Frequency assumptions' or 'Implicit ordering'` | Eval 2 pins categories that SKILL.md does not tie to concurrent modification | Intended (nested-call frequency) | Review against SKILL.md:205-213 with the author |

### HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type | Confidence |
|---|----------|-----------|--------|------|------------|
| D-HB1 | scripts/check.py:478 `want = hashlib.sha256(prompts[i].encode("utf-8")).hexdigest()` | Facts re-checked when an eval is edited (README.md:255) | Only prompt edits trigger it | Preventive (D-F6) | 85 |
| D-HB2 | scripts/check.py:494 `reasons[int(m.group(1))] = m.group(2)` | NOT_COMPUTABLE lists evals from 29 that state facts | Any id accepted | Preventive (D-F7) | 82 |
| D-HB3 | scripts/check.py:473 `with_file[int(stem)] = name` | Every fact file carries its prompt's hash (scripts/check.py:36-37) | Last file wins | Preventive (D-F8) | 82 |

---

## FAILURE CATEGORIES IDENTIFIED (all domains, after the category search)
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Silent fallthrough | C-F1, C-F2, C-F8, C-F9, C-F12, C-F13, C-F16, C-HB2 | scripts/check_facts.py, scripts/pre-commit, scripts/check.py |
| Missing completeness | C-F5, C-F14, C-F15, C-F18, D-F1, D-F5, D-F6, D-F7, D-F8, D-F9, T-F6, T-F9 | scripts/check.py, scripts/check_facts.py, scripts/test_check.py, evals/facts/NOT_COMPUTABLE, evals/evals.json |
| Stale state / doc-code drift | Doc-F1 to Doc-F10, C-F3 (comment vs call), T-F5, T-F10, D-F4 | README.md, CHANGELOG.md, scripts/check.py, scripts/check_facts.py, scripts/test_check.py, evals/facts/_parse_day.py, evals/facts/35.py, evals/evals.json |
| Assumed environment | C-F4 (CRLF), C-F19, C-F20, C-F21, C-H1, C-H2, T-F7, T-H3 | scripts/check.py, scripts/check_facts.py, scripts/pre-commit, scripts/test_check.py |
| Test-environment artifact | T-F1, T-F3, T-F8, T-H4 | scripts/test_check.py |
| Tautological / unfalsifiable test | T-F2, T-F4, T-F11, C-F17 | scripts/test_check.py, evals/facts/52.rs, scripts/check_facts.py |
| Numbers restated outside their fact file | D-F2, D-F3, D-F6 | evals/evals.json, scripts/check.py |
| Version skew between checker and checked | C-F6, C-F7, D-F9 | scripts/pre-commit, evals/facts/_parse_day.py |

## STRESS TEST RESULTS
Only the independent verifier ran stress techniques. It applied them to its falsified sub-hypothesis on masking (scripts/check.py:409):
- Scale Shift (zero terms): survived (85).
- Requirement Inversion (`=` term): did not survive. Reported as C-F3.
- Time Travel (a new check printing a path): survived for plain terms (80).

The domain agents' returns contain no STRESS TEST section: it was not requested by the protocol's brief.

## ADVERSARIAL SCAFFOLD FINDINGS
- **Reviewer blind spots:**
  - the `?` in scripts/check.py:90
  - the default `substring=False` behind a comment that says the opposite (scripts/check.py:399-400)
  - scripts/pre-commit:5 naming `--strict` while line 9 omits it
  - the `[:1]` slice at scripts/check.py:223
- **Highest-risk claims** (sent to the independent verifier): D-F1, C-F2, C-F1, C-F3, C-F4. All five were confirmed as FAIL.
- **Multi-step traces:**
  - No terms → scripts/check.py:297 warning → exit 0 → scripts/pre-commit:9 passes → private names committed.
  - No rustc → scripts/check_facts.py:92 skip → :113 exit 0 → scripts/pre-commit:17 prints nothing → Rust facts unchecked.
  - NOT_COMPUTABLE:13 → scripts/check.py:495 error → hook blocks every commit and the suite is red.

## CROSS-DOMAIN SUMMARY
- Domains: Code, Tests, Documentation, Data.
- Claims: 162 decomposed by the domain agents (43 + 29 + 55 + 35). Report rows: 45 PASS; 51 in FAIL (C 21, T 11, Doc 10, D 9); 1 falsified hypothesis (masking of plain terms, by the verifier).
- Findings by type: 24 demonstrated defects, 27 preventive measures, 1 falsified hypothesis (0 conditional).
- Critical issues: 0 rated critical. Rated high: D-F1, C-F1, C-F2, C-F3, C-F4, Doc-F1.
- Failure categories: 8 systemic patterns.
- Invariants: 5 found, 5 touched, 2 enforced by a mechanism that bites (the version check and the "not both" check). The second bites against the tree itself (D-F1).
- Hypotheses: 15 need investigation (C 3, T 4, Doc 4, D 4). More run-only hypotheses are in the individual returns.
- Hidden behaviors: 12 detected (C 7, T 2, D 3).
- Cross-domain changes: the toolchain skip (C-F1) shows up in Code, Tests (T-F1), Documentation (Doc-F3) and the hook. The missing `--strict` (C-F2) shows up in Code and Documentation (Doc-F4). The NOT_COMPUTABLE conflict (D-F1) shows up in Data, Code and Tests (T-H1).
- Executed: nothing (reasoning only).
- Proposed: 6 checks and 12 writes awaiting an answer.
- Recommendation: do not rely on the pre-commit hook, the fact runner or the private-name check as documented until D-F1 and C-F1 to C-F4 are fixed. Fix D-F1 first: it makes scripts/check.py fail on the tree as it stands.

## PROPOSED EXECUTABLE CHECKS
| # | Claim | Confidence now | Check | Confirms if | Refutes if | Cost and side effects | Status |
|---|-------|----------------|-------|-------------|------------|-----------------------|--------|
| 1 | D-F1: check.py fails on the tree | 90 | `python3 scripts/check.py` in ./tree | prints `eval 52 has a fact file and a reason not to have one`, exit 1 | exit 0 | Runs the project's script, read-only | proposed |
| 2 | C-F1: a missing toolchain is skipped | 92 | `python3 scripts/check_facts.py 52` with rustc removed from PATH | `skip 52.rs`, exit 0 | FAIL line, exit 1 | Runs the script; nothing compiled | proposed |
| 3 | T-H1: suite state | — | `python3 -m unittest scripts/test_check.py` | ~20 failures, plus test_second_badge_mismatch and the two-space subTest | green | Runs the test suite in temp copies | proposed |
| 4 | D-H1: hashes current | — | Part of check 1 above: look for "prompt changed since its facts were checked" | none printed | any printed | none extra | proposed |
| 5 | D-H2, D-H3: float facts | 75 / — | `python3 scripts/check_facts.py 38 48` | `ok 38`, `ok 48` | FAIL | Runs two fact files | proposed |
| 6 | C-H1: Windows binary name | — | `py -3 scripts/check_facts.py 52` on Windows with rustc | `ok 52` | error launching `52.rs.bin` | Compiles one Rust file into a temp dir | proposed |

Proposed writes (nothing written):
1. Delete skills/adversarial-verify/evals/facts/NOT_COMPUTABLE:13.
2. scripts/check_facts.py:92-93: count the missing toolchain as a failure.
3. scripts/pre-commit:9: add `--strict`.
4. scripts/check.py:400: `substring=True`.
5. scripts/check.py:90: `[\W_]*`.
6. scripts/check.py:223: `for b in badges:`.
7. skills/adversarial-verify/evals/evals.json:705: "12 are excluded". evals.json:612: "the same two labels".
8. README.md:125: drop "(currently 4.1)". README.md:89: `cp -r`.
9. scripts/test_check.py:479: real assertion. scripts/test_check.py:578: assert no "skip ". scripts/test_check.py:43: pop CHECK_PRIVATE_TERMS.
10. skills/adversarial-verify/evals/facts/_parse_day.py:1: list 35.py.
11. README.md:46, :247, :254 and CHANGELOG.md:3 wording.
12. skills/adversarial-verify/evals/evals.json:249: update the quoted summary line.

Shall I run checks 1-6, and which of writes 1-12 should I make?
