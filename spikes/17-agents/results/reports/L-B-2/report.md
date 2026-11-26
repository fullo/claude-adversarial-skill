# Adversarial verification report: ./tree (23 files)

**Cost estimate (stated before starting, as Intake rule 2 requires for a large request that settles every choice):** 23 files in scope; 4 domains detected (Code, Tests, Data, Documentation); about 160 decomposed claims; nothing run. The work was done by 4 domain agents, 1 independent verifier and 1 category agent.

## INTAKE
- **Target:** every domain the skill detects in the 23 files: Code, Tests, Data, Documentation. Step 0 found no Architecture, Analysis or UX artifact in scope. *Given in the request.*
- **Depth:** standard. *Given in the request.*
- **Scope:** the whole of the 23 listed files. There is no diff and no version history, because ./tree is not a git repository. *Given in the request.*
- **Execution mode:** reasoning only. Nothing was run, compiled or written in ./tree. *Given in the request.*
- To change any of these, ask for e.g. "deep", "approved checks: the existing test suite", or "only Code".

Paths below are relative to ./tree.

**Return accounting:**
- 459 table rows came back from the 6 agents: Code 104, Tests 81, Data 81, Documentation 146, independent verifier 5, category agent 42.
- 0 rows were discarded. Every FAIL, PASS, HYPOTHESIS and HIDDEN BEHAVIOR quote I looked up was at the line its row names. Some quotes differ only in backticks or are wrapped across a stated line range.
- The independent verifier re-checked the 5 highest-risk claims. It confirmed all 5 verdicts and changed none. On 3 of them it gave a lower severity than a domain agent; both severities are shown in the rows.
- Rows reported by several agents are merged below and counted once, in their primary domain. The category agent returned 33 rows: 25 were new, and 8 duplicated findings already in the domain returns.

---

# Domain 1: Code

## VERIFICATION DOMAIN
Code: scripts/check.py, scripts/check_facts.py, scripts/pre-commit, and the fact programs in skills/adversarial-verify/evals/facts/.

## GROUND TRUTH
The docstrings of the scripts (scripts/check.py:1-47, scripts/check_facts.py:1-14, scripts/pre-commit:1-10) and README.md:245-264 serve as the spec. scripts/test_check.py serves as the executable statement of intent. The eval prompts in evals.json are the source of the fact files.

## INVARIANTS
The repository's own invariants are the six numbered checks of scripts/check.py:6-44 and the "never a silent skip" rule of scripts/check_facts.py:8. No CLAUDE.md, AGENTS.md or CONTRIBUTING.md was found in ./tree; the file count above lists every file. The protocol brief did not ask agents for an INVARIANTS table, so no per-invariant table is given. The touched invariants show up as FAIL rows: C1, C2, C3, C5, C6 and Data D1.

## DECOMPOSED CLAIMS
37 claims (Code return), as Deductive except C31 (Inductive) and C33 (Abductive, run-only). The main ones:
- Version check covers every badge (scripts/check.py:10).
- Term separators accept any non-alphanumeric join (scripts/check.py:16).
- Terms are never printed (scripts/check.py:22).
- `=` terms match whole words (scripts/check.py:18).
- Eval schema is enforced (scripts/check.py:6).
- Fact file or reason, not both (scripts/check.py:34).
- `--staged` checks exactly the index (scripts/check.py:47).
- A missing toolchain is an error (scripts/check_facts.py:8).
- Every fact file asserts and ends with `ok <id>` (scripts/check_facts.py:13).
- The hook checks the staged content and is strict (scripts/pre-commit:2, :5, :10).

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Missing completeness | 10 (C1, C2, C3, C4, C10, C11, C14, C15, C16, C26) | scripts/check.py, scripts/check_facts.py |
| Silent fallthrough | 12 (C5, C7, C8, C9, C13, C17, C18, C19, C20, C21, C22, C27, C28) | scripts/check_facts.py, scripts/pre-commit, scripts/check.py |
| Assumed environment | 4 (C2 CRLF, C23, C24, C25) | scripts/check.py, scripts/check_facts.py |
| Stale state | 1 (C12) | scripts/check.py |

## VERIFICATION RESULTS
### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| P1 | The plugin.json version and the newest numbered CHANGELOG entry are compared with SKILL.md | scripts/check.py:237 `first = re.search(r"^## +([0-9][0-9.]*)\b", read_text(root, CHANGELOG, rep), re.M)` skips `## Unreleased` (CHANGELOG.md:5) and takes `## 4.2 - 2026-11-25` (CHANGELOG.md:10). All four sources say 4.2: skills/adversarial-verify/SKILL.md:20, README.md:1, .claude-plugin/plugin.json:3. Confidence 90 |
| P2 | `=` terms are detected as whole words, others as substrings | scripts/check.py:275 `pats.append(re.compile(rf"(?<![^\W_]){body}(?![^\W_])" if whole_word else body))`. Confidence 88 |
| P3 | Short terms give a warning; with no terms, the result is a warning, or an error under --strict | scripts/check.py:271 `if rep is not None and sum(len(p) for p in parts) < 4:`; scripts/check.py:297 `(rep.error if strict else rep.warning)("private terms", msg)`. Confidence 88 |
| P4 | The evals schema is enforced: keys, integer ids that reject bool, tags from 21 on, order | scripts/check.py:186 `if type(i) is not int:`; scripts/check.py:201 `elif i >= TAGGED_FROM and not TAG_RE.match(a):`. Confidence 88 |
| P5 | `--staged` reads the index copy, and terms still come from the working repository | scripts/check.py:423 `terms = load_terms(args.root)`; scripts/check.py:433 `root = tmp`. Confidence 85 |
| P6 | The fact runner requires an assertion and a final `ok <id>`, and Python asserts are not optimised away | scripts/check_facts.py:107 `if out[-1:] != [f"ok {stem}"]:`; scripts/check_facts.py:57 `return [[sys.executable, "-E", "-s", path]]`. Confidence 85 |
| P7 | A failing fact run blocks the commit | scripts/pre-commit:15 `out="$("$py" -I "$root/scripts/check_facts.py" --root "$tmp")"; rc=$?`. Confidence 82 |
| P8 | Named reference files must exist, and unnamed ones are reported | scripts/check.py:517 `if name not in existing:`. Confidence 88 |
| P9 | Every reported error gives exit 1 (normal path) | scripts/check.py:442 `return 1 if rep.errors else 0`. Confidence 85 |
| P10 | The fact programs compute what their evals state (35, 37, 39, 40, 42, 48, 49, 51, 52, 53, 56, 57), traced by hand by all four domain agents | e.g. skills/adversarial-verify/evals/facts/40.py:9 `assert killed == {'>= to <', '>= to <=', 'return True'}`; facts/49.py:12 `assert clipped(375) == (77.75, {'Bestellungen', 'Einstellungen'})`; facts/56.py:12 `assert (measured_survivors, measured, excluded) == (4, 108, 12)`. Confidence 85. The float equalities (38.py:19-21, 48.py:17-21) are capped at 79 (run-only, see H2) |

### FALSIFIED HYPOTHESES
None.

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| C1 | scripts/check.py:223 | `for b in badges[:1]:` | Demonstrated defect | Medium | scripts/check.py:10 and README.md:250 say "every skill badge", but only the first is compared. The second badge that scripts/test_check.py:172 appends (`skill-v2.0`) is not flagged, so test_second_badge_mismatch is red by trace. Found by 4 of 4 domain agents | Deductive | 90 | `for b in badges:` |
| C2 | scripts/check.py:90 | `SEP = r"[\W_]?"  # anything that is not a letter or digit, possibly nothing` | Demonstrated defect | High (Code agent) / Medium (independent verifier) | `?` allows at most one separator. Two spaces, " - ", ", " or CRLF between the parts of a private term are not detected, so the name can be committed. This contradicts scripts/check.py:15-17 and README.md:251. The test_check.py:286 variant `f"{a.upper()}  {b}"` is red by trace. The independent verifier agrees (FAIL, 92) | Deductive | 90 | `SEP = r"[\W_]*"` (or bounded `{0,3}`) |
| C3 | scripts/check.py:400 | `pats = term_patterns(terms)` | Demonstrated defect | High (Code, Tests agents) / Medium (independent verifier) | mask() uses the default `substring=False`, so `=` terms are masked only as whole words. With term `=zqvorblax` and an evals key `zqvorblaxlabs`, scripts/check.py:182 prints the key unmasked, which breaks scripts/check.py:22 "Terms are never printed" and the comment at :399. test_check.py:341-344 is red by trace. The independent verifier agrees (FAIL, 90) | Deductive | 90 | `term_patterns(terms, substring=True)` |
| C4 | scripts/check.py:401 | `hit = lambda s: any(p.search(normalize(s)) for p in pats)` | Preventive measure | Medium | Masking shares C2's single-character SEP, so a term printed with two separators is neither detected nor masked. It needs such a key or path; none exists today | Deductive | 85 | Fixed with C2 |
| C5 | scripts/check_facts.py:91-93 | `print(f"skip {name}: toolchain not found")` | Demonstrated defect | High (Tests, Code, Documentation agents) / Medium (Data agent, independent verifier) | Without rustc or node, 52.rs and 53.ts are skipped, `failed` is not incremented, and the exit code is 0 (scripts/check_facts.py:113). This contradicts scripts/check_facts.py:8 "never a silent skip" and README.md:255. The independent verifier agrees (FAIL, 90) | Deductive | 90 | `failed += 1` with a FAIL line |
| C6 | scripts/pre-commit:9 | `"$py" -I "$root/scripts/check.py" --staged --root "$root" \|\| exit 1` | Demonstrated defect | High | README.md:261 ("runs --strict --staged before every commit") and scripts/pre-commit:5 promise --strict. Without it, missing private terms are only a warning (scripts/check.py:297), so a fresh clone commits with no private-name check. The independent verifier agrees (FAIL, 95). The category agent found the same at pre-commit:5 and README.md:261 | Deductive | 95 | Add `--strict` |
| C7 | scripts/pre-commit:17 | `[ $rc -eq 0 ] \|\| { printf "%s\n" "$out"; exit 1; }` | Preventive measure | Medium | Output is shown only on failure, so the skip of C5 is invisible at commit time | Deductive | 85 | Fix C5, or always print the summary |
| C8 | scripts/check.py:364 | `fence = f.group(1)[0]` | Preventive measure | Low | The stored fence character is never compared, so a `~~~` line inside a ``` block closes it, and later tables escape the table check. No instance today | Deductive | 85 | Close only on the same fence character with at least as many of them |
| C9 | scripts/check.py:228 | `except ValueError as e:` | Preventive measure | Low | A missing plugin.json, README.md or CHANGELOG.md raises OSError. The result is a traceback with no summary, the other errors are lost, and masking is bypassed (Code and Data agents) | Deductive | 85 | Catch OSError and report "missing file" |
| C10 | scripts/check.py:473 | `with_file[int(stem)] = name` | Preventive measure | Low | With two fact files for one id (e.g. 38.py and 38.ts), only one is hash-checked | Deductive | 85 | Error on a second file for the same id |
| C11 | scripts/check.py:494 | `reasons[int(m.group(1))] = m.group(2)` | Preventive measure | Low | Duplicate, unknown, below-29 and no-"(Facts" ids in NOT_COMPUTABLE are accepted silently, so stale reasons pile up (Data D1 is one) | Deductive | 82 | Report them |
| C12 | scripts/check.py:43 | `reader nowhere. The folder is read as it is on disk, tracked or not, since` | Demonstrated defect | Low | With --staged (the hook), root is the index copy (scripts/check.py:433), so untracked reference files are not seen. test_check.py:508 relies on exactly that | Deductive | 88 | Say so in the docstring |
| C13 | scripts/check.py:341 | `:?-{3,}:?` (DELIM) | Preventive measure | Low | GFM accepts 1-dash delimiter cells, so such tables are never recognised or counted. No instance today | Deductive | 82 | `-+` |
| C14 | scripts/check.py:478 | `want = hashlib.sha256(prompts[i].encode("utf-8")).hexdigest()` | Preventive measure | Medium | The fact binding covers the prompt only. expected_output and assertions can contradict the facts, as Data D2 and D3 show | Deductive | 85 | Hash the whole eval, or assert the quoted numbers in the fact file |
| C15 | scripts/check.py:500 | `if "(Facts" in str(e.get("prompt", "")) and e["id"] not in with_file and e["id"] not in reasons:` | Preventive measure (Data agent) / Demonstrated defect (category agent) | Medium | Evals 54 (evals.json:672) and 55 (evals.json:686) state computable facts without the "(Facts" marker and need neither a file nor a reason, while CHANGELOG.md:24 says "every eval from 29 on that states facts". The two agents disagree on the type; the lower confidence is kept | Inductive | 75 | Require a file or reason for every eval from 29 on, or reword the rule |
| C16 | scripts/check_facts.py:50 | `return any(isinstance(n, (ast.Assert, ast.Raise)) for n in ast.walk(tree))` | Preventive measure | Low | An assert in an uncalled function or a dead branch counts, so a fact file that asserts nothing at run time passes (Documentation, Code and category agents) | Deductive | 80 | Count only executed or top-level assertions |
| C17 | scripts/check.py:301 | `if os.path.basename(rel) == TERMS_FILE:` | Preventive measure | High | Any file named `.check-private-terms`, anywhere and tracked or not, is exempt from the scan. A force-added list ships unreported, although README.md:251 says "The list is never committed" | Deductive | 80 | Exempt only the untracked root file, and error if it is tracked |
| C18 | scripts/check.py:248 | `if raw is not None:` | Preventive measure | Low | A set but empty CHECK_PRIVATE_TERMS silently disables the terms file, and under the hook (C6) that is only a warning | Deductive | 85 | Treat an empty variable as unset, or warn |
| C19 | scripts/check.py:436 | `if files or not args.staged:` | Preventive measure | Low | With an empty index, --staged runs no check at all | Deductive | 85 | Run the checks or report "nothing staged" |
| C20 | scripts/check.py:151 | `except (OSError, subprocess.CalledProcessError):` | Preventive measure | Medium | Any git failure (e.g. "dubious ownership") silently falls back to walking untracked files, while scripts/check.py:46 says the fallback applies only when git is unavailable | Deductive | 75 | Fall back only on OSError, otherwise warn |
| C21 | scripts/check.py:316 | `except ValueError:` | Preventive measure | Low | A .json file that does not parse is scanned raw only, with no note that `\u` escapes were not decoded | Deductive | 80 | Warn |
| C22 | scripts/check.py:440 | `shutil.rmtree(tmp, ignore_errors=True)` | Preventive measure | Low | A failed cleanup leaves the staged copy in the system temp folder silently | Deductive | 70 | Warn with the leftover path |
| C23 | scripts/check.py:527 | `print(f"checked ({scope}): {', '.join(rep.checked)} — {len(rep.errors)} error(s), {len(rep.warnings)} warning(s)")` | Preventive measure | Medium | U+2014 printed to a pipe under an ANSI code page without it raises UnicodeEncodeError after the checks have run | Abductive | 60 | ASCII separator or reconfigure stdout |
| C24 | scripts/check_facts.py:100 | `r = subprocess.run(step, cwd=FACTS, capture_output=True, text=True)` | Preventive measure | Low | Locale decoding of tool output can raise UnicodeDecodeError and abort the run (Code H8, category agent) | Abductive | 55 | `encoding="utf-8", errors="replace"` |
| C25 | scripts/check_facts.py:63 | `return [[rustc, "--edition", "2021", "-O", "-o", exe, path], [exe]]` | Preventive measure | Low | rustc on PATH without a linker gives a false "fact failed" | Abductive | 55 | Report a link failure as an incomplete toolchain |
| C26 | scripts/check.py:330 | `patterns = [re.compile(t) for t in STACK_TERMS]` | Preventive measure | Low | The neutral-wording terms are case-sensitive, so lowercase "python" or "docker" are not warned about (Code H7, category agent) | Deductive | 80 | `re.I` for word-like terms |
| C27 | scripts/check_facts.py:85 | `files = [f for f in files if os.path.splitext(f)[0] in ids]` | Demonstrated defect | Low | `check_facts.py 38 99` drops 99 silently and exits 0 | Deductive | 85 | FAIL on a requested id with no file |
| C28 | scripts/check.py:469 | `if ext in FACT_EXTS and not stem.startswith("_"):` | Preventive measure | Low | `42.PY`, `53.mts` or `_38.py` are neither run nor reported as orphans. The rule also exempts the helper from any hash (see Data D4) | Deductive | 75 | Report unknown files in facts/ |
| C29 | scripts/pre-commit:12 | `if git diff --cached --name-only \| grep -q '^skills/adversarial-verify/evals/'; then` | Preventive measure | Low | A commit that changes only scripts/check_facts.py does not run the facts. Both the hook and check.py run from the working tree, not from the staged scripts (Tests HB5, HB6; Code HB11 calls it a design limit) | Deductive | 82 | Also trigger on scripts/check_facts.py |

## STRESS TEST RESULTS
The protocol's brief asked the domain agents only for the six listed sections, so no stress-test table came back. Not done.

## HYPOTHESES
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| H1 | Every fact file starts with a hash, e.g. skills/adversarial-verify/evals/facts/35.py:1 `# prompt-sha256: a502f0639b93c074fd20190e3f58c7c630fa1d91a21742e31cdb07b968e7823b` | Each equals the sha256 of its current prompt | A prompt was edited after its hash was set | `python3 scripts/check.py` and look for "prompt changed" |
| H2 | facts/38.py:19-21 and facts/48.py:17-21 assert exact float or 2-decimal results | They all hold in IEEE-754 (hand traces agree) | A rounding lands on the other side | `python3 scripts/check_facts.py 38 48` |
| H3 | scripts/check_facts.py:67 `return [[node, "--experimental-strip-types", "--no-warnings", path]]` and no node version check | node < 22.6 shows up as a false fact, not as a missing toolchain | Every committer has node ≥ 22.6 | Run with node 20 |
| H4 | scripts/check.py:389 `checkout-index -a` | With core.autocrlf=true the staged copy has CRLF, so C2 applies to every multi-line term | eol=lf is forced | `git config core.autocrlf`; compare bytes with `git show :path` |
| H5 | scripts/pre-commit:7-8 `py=python3` / `command -v "$py" >/dev/null 2>&1 \|\| py=python` | On Windows the python3 Store stub blocks every commit | A real python3 is on Git-sh's PATH | Run the hook on such a machine |

## HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| HB1 | scripts/check.py:223 | Every badge compared | First only | Demonstrated defect (C1) | 90 |
| HB2 | scripts/check.py:400 | Substring masking | Whole-word masking for `=` terms | Demonstrated defect (C3) | 90 |
| HB3 | scripts/check.py:90 | Any join | At most one character | Demonstrated defect (C2) | 90 |
| HB4 | scripts/check_facts.py:92 | Missing toolchain = error | Skip, exit 0 | Demonstrated defect (C5) | 90 |
| HB5 | scripts/pre-commit:9 | --strict --staged | --staged only | Demonstrated defect (C6) | 95 |
| HB6 | scripts/check.py:476 `head = read_text(root, f"{FACTS_DIR}/{name}")[:2000]` | The file carries the hash | Searched in the first 2000 characters only | None today | 85 |
| HB7 | scripts/check.py:301 | The untracked root terms file is exempt | Any file of that name is exempt | Preventive measure (C17) | 85 |

---

# Domain 2: Tests

## VERIFICATION DOMAIN
Tests: scripts/test_check.py; the fact files as executable checks of the evals.

## GROUND TRUTH
The production code under test (scripts/check.py, scripts/check_facts.py) and the hook that runs it in production (scripts/pre-commit). The test bootstrap is scripts/test_check.py:28-90.

## INVARIANTS
See Domain 1. The test that should enforce "the repo passes" (scripts/test_check.py:97-101) is red by trace because of Data D1.

## DECOMPOSED CLAIMS
24 claims (Tests return). Examples:
- The repo passes (scripts/test_check.py:97-98).
- Second-badge mismatch (:171-173).
- Glued `=` term masked (:341-344).
- Two-word joins (:286).
- Orphan reference (:479).
- Runner on the repo (:575-578).
- Environment independence (:43).
- Git guard (:502-505).
- Fact files reproduce their evals.

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Tautological tests | 5 (T1, T12 ×4) | scripts/test_check.py, facts/51.py, 52.rs, 57.py |
| Test-environment artifact | 7 (T2, T3, T4, T7, T8, T9, T10) | scripts/test_check.py |
| Missing completeness (missing negative tests) | 1 (T6) | scripts/test_check.py |
| Stale state / test-code drift | 3 (T5, T11, T13) | scripts/test_check.py, facts/35.py |

## VERIFICATION RESULTS
### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| P1 | The runner's negative tests cannot pass by not editing | scripts/test_check.py:80 `self.assertIn(old, s)`. Confidence 85 |
| P2 | The changelog tests hold although the first heading is `## Unreleased` | scripts/test_check.py:223 `i = s.index("\n## ")` with the regex at scripts/check.py:237. Confidence 85 |
| P3 | The drift test changes eval 37's prompt | scripts/test_check.py:550 `d["evals"][36]["prompt"] = d["evals"][36]["prompt"].replace("day > 31", "day > 28")`; evals.json:463 holds `day > 31`. Confidence 85 |
| P4 | assert_fails cannot pass on a crash | scripts/test_check.py:58 `self.assertIn("checked (", r.stdout, "the script did not run to its summary:\n" + out)`. Confidence 85 |
| P5 | Private-term test values do not occur literally in the source | scripts/test_check.py:25 `T1 = "zq" + "vorblax"`. Confidence 82 |
| P6 | `ids` before `--root` is accepted | scripts/check_facts.py:78 `ap.add_argument("ids", nargs="*", help="eval ids to run (default: all)")`. Confidence 80 |

### FALSIFIED HYPOTHESES
None.

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| T1 | scripts/test_check.py:479 | `self.assertIn("orphan.md", r.stdout + self.ref("orphan.md"))` | Demonstrated defect | Medium | `self.ref("orphan.md")` always contains "orphan.md", so test_file_nobody_names can never fail. Found by the Tests, Code and Documentation agents | Deductive | 95 | `self.assert_fails(r, "orphan.md", "never named in SKILL.md")` |
| T2 | scripts/test_check.py:575-578 | `self.assertRegex(r.stdout, r"\d+ fact file\(s\), 0 failed")` | Preventive measure (Data agent) / Demonstrated defect (Tests agent) | Medium | Test-environment artifact: without rustc or node, 52.rs and 53.ts are skipped (C5) and the test is still green. The two agents disagree on the type; the lower confidence is kept | Deductive | 85 | Assert no "skip" line |
| T3 | scripts/test_check.py:43 | `env = dict(os.environ)` | Preventive measure | Medium | A developer's CHECK_PRIVATE_TERMS leaks into tests that pass `terms=None`, turning test_missing_terms_* red and making test_terms_file_* pass without exercising the file | Deductive | 85 | `env.pop("CHECK_PRIVATE_TERMS", None)` |
| T4 | scripts/test_check.py:505 | `git("init", "-q"); git("add", "-A"); git("commit", "-q", "-m", "base")` | Preventive measure | Low | No `skipUnless(git)` guard, unlike scripts/test_check.py:369, so it errors (false red) without git | Deductive | 85 | Add the guard |
| T5 | scripts/test_check.py:337 | `# whole-word detection does not flag "<term>labs", but the evals check prints the key name` | Preventive measure | Low | The comment describes the `=` case, but the test uses a plain term | Deductive | 85 | Fix the comment |
| T6 | scripts/test_check.py:571 | `def run_facts(self, *ids):` | Preventive measure | Medium | Untested paths, as stated in the Tests return: a missing toolchain, .rs/.ts assertion detection, --staged with an empty index, the FACTS_FROM boundary, mixed fences, and the hook itself. C5 is a defect on one of these untested paths | Deductive | 82 | One test per path |
| T7 | scripts/test_check.py:32 | `for item in ("README.md", "CHANGELOG.md", "skills", ".claude-plugin", "scripts", ".gitignore"):` | Demonstrated defect | Medium | Tests run on a partial copy that is not a git repository, so check.py takes the walk path (scripts/check.py:153), not `git ls-files`. LICENSE is not checked, and test_repo_passes does not reproduce the hook's path | Deductive | 80 | Copy the tracked files into a git-initialised temp repo |
| T8 | scripts/test_check.py:374 | `subprocess.run(["git", "-C", self.tmp, *args], check=True, capture_output=True, env=env)` | Preventive measure | Medium | Inherits global git config (gpgsign, hooksPath, autocrlf), so the result depends on the machine | Abductive | 65 | `GIT_CONFIG_GLOBAL=os.devnull`, `GIT_CONFIG_NOSYSTEM=1` |
| T9 | scripts/test_check.py:391 | `before = {d for d in os.listdir(tempfile.gettempdir()) if d.startswith("check-staged-")}` | Preventive measure | Low | Shared temp folder: a concurrent run makes the test fail | Abductive | 60 | Per-test TMPDIR |
| T10 | scripts/test_check.py:414 | `self.assertIn("SQLite", open(self.path(EVALS)).read())` | Preventive measure | Low | Opened with the locale encoding; evals.json is UTF-8 with U+2014 | Deductive | 65 | `encoding="utf-8"` |
| T11 | scripts/test_check.py:23 | `# including this one (the check scans every file). Neither occurs in the repo.` | Demonstrated defect | Low | Three terms follow, not two, and only tracked files are scanned in a repo | Deductive | 75 | Reword |
| T12 | skills/adversarial-verify/evals/facts/52.rs:15 | `assert_ne!(days_in_month(2024, 2), 29);` | Demonstrated defect | Low | Implied by line 14, so it can never be the assertion that fails. The same holds for facts/51.py:6 `assert before >= 44 > after  # the project's touch-target rule` (85) and facts/57.py:7 `assert discarded == 1` (70). facts/51.py:3 `before = 20 + 2 * 12` retypes the prompt's constants (Tests HB9, 80) | Deductive | 70 | Derive the values from the prompt, or drop the redundant asserts |
| T13 | skills/adversarial-verify/evals/facts/35.py:2 | `"""Eval 35: the function as shown accepts 31 February, which the three valid-date tests do not cover."""` | Demonstrated defect (category agent) / not a problem, partial coverage (Tests agent HB11) | Low | The docstring claims a second fact that no line checks, and the body is identical to 37.py. The two agents disagree; the lower confidence is kept | Deductive | 75 | Limit the docstring to what is checked |

## HYPOTHESES
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| H6 | Data D1, C1, C2 and C3 predict red tests by trace | The suite is red now: about 20 assert_passes tests, plus test_second_badge_mismatch, test_whole_word_term_glued_in_output_is_still_masked and one subtest of test_two_words_joined_any_way | A file outside the read set changes the outcome | `python3 -m unittest scripts/test_check.py` |
| H7 | scripts/test_check.py:351 `os.symlink(...)` and :390 `shutil.rmtree(self.path(".git"))`; README.md:264 supports Windows | False reds on Windows without Developer Mode | Developer Mode on | Run the suite on Windows |
| H8 | scripts/test_check.py:85 `f.write("\n" + text + "\n")` in text mode | On Windows the `\n` subtest of :286 also fails (CRLF, C2) | Line endings are normalised | Run the subtest on Windows |

## HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| HB1 | skills/adversarial-verify/evals/facts/38.py:21 `assert round(10.05 * 0.9, 2) == 9.05` | Fact files reproduce the prompt | This line is the fixture of test_runner_fails_on_a_false_fact (scripts/test_check.py:582), not a fact of eval 38 | Not a problem (coupling) | 85 |
| HB2 | skills/adversarial-verify/evals/facts/_parse_day.py:28 `def parse_day_fixed(text):  # eval 39, the commit as described` | 39.py checks eval 39's commit | It checks a reconstruction: the prompt has no code for the fix | Not a problem (stated) | 85 |

---

# Domain 3: Data

## VERIFICATION DOMAIN
Data: .claude-plugin/plugin.json, skills/adversarial-verify/evals/evals.json, skills/adversarial-verify/evals/facts/NOT_COMPUTABLE, and the eval↔fact-file binding.

## GROUND TRUTH
The schema in scripts/check.py:6-9 and :34-38, the fact files, and the evals' own expected_output vs assertions.

## DECOMPOSED CLAIMS
30 claims (Data return). They cover:
- Manifest version, name, licence and repository.
- The evals schema.
- File-or-reason for every eval from 29 on.
- The hash binding.
- Arithmetic of evals 38, 39, 40, 48, 49, 51, 53, 56 and 57.

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Contradictory records | 4 (D1, D2, D3, D5) | NOT_COMPUTABLE, facts/52.rs, evals.json |
| Missing completeness | 1 (D4) | facts/_parse_day.py |

## VERIFICATION RESULTS
### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| P1 | Manifest name, repository and licence agree with the skill and README | .claude-plugin/plugin.json:2 `"name": "adversarial-verify",`, :8, :9 = skills/adversarial-verify/SKILL.md:2, :16; README.md:95. Confidence 90 |
| P2 | Eval ids 1..57 are consecutive in file order, and evals 21-57 have tagged assertions | evals.json:5 `"id": 1,` … evals.json:711 `"id": 57,`. The Data agent did not read evals 2-18 line by line. Confidence 85 |
| P3 | Every eval from 29 on with "(Facts" has a file or a reason | e.g. evals.json:611 `(Facts, measured`. The "not both" half fails (D1). Confidence 90 |
| P4 | Every fact file asserts and prints `ok <id>` last | e.g. facts/52.rs:14 `assert_eq!(days_in_month(2024, 2), 28);`. Confidence 90 |
| P5 | The expected output of eval 56 agrees with facts/56.py | facts/56.py:12 `assert (measured_survivors, measured, excluded) == (4, 108, 12)`. Confidence 95 |

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| D1 | skills/adversarial-verify/evals/facts/NOT_COMPUTABLE:13 | `52: the compiler is not installed on every machine` | Demonstrated defect | High | facts/52.rs exists, so scripts/check.py:495-496 reports "eval 52 has a fact file and a reason not to have one". check.py exits 1 on the committed tree (scripts/check.py:442), the hook blocks every commit (scripts/pre-commit:9), and test_repo_passes (scripts/test_check.py:97-101) plus every assert_passes test are red by trace. Found by 4 of 4 domain agents; the independent verifier agrees (FAIL, 92). The red tests themselves are run-only (79) | Deductive | 90 | Delete NOT_COMPUTABLE:13 |
| D2 | skills/adversarial-verify/evals/evals.json:705 | `"[substance] Gives the score on the measured mutants only (104 of 108, about 96%) and says that 11 are excluded: 8 timed out, 3 skipped, 1 not measured",` | Demonstrated defect | Medium | 8+3+1 = 12. The same eval's expected output (evals.json:699 "with 12 excluded") and facts/56.py:12 say 12, so a correct answer fails this assertion | Deductive | 95 | "12 are excluded" |
| D3 | skills/adversarial-verify/evals/evals.json:612 | `… and that at 320 px (80 px buttons, 64 px usable) more labels are clipped; …` | Demonstrated defect | Low (Tests, Documentation agents) / Medium (Code agent) | At 320 px the same two labels are clipped as at 375 px (facts/49.py:13 `assert clipped(320) == (64.0, {'Bestellungen', 'Einstellungen'})`; evals.json:615) | Deductive | 90 | "the same two labels are clipped, with less room" |
| D4 | skills/adversarial-verify/evals/facts/_parse_day.py:5 | `def parse_day_v1(text):  # evals 29, 35 and 37` | Preventive measure | Low | The shared helper copies the functions of evals 29, 35, 37 and 39 but carries no hash (scripts/check.py:469 exempts `_` files), which contradicts README.md:255 "every eval it covers" | Deductive | 75 | Hash each eval the helper copies, or narrow README.md:255 |
| D5 | skills/adversarial-verify/evals/evals.json:166 | `"Uses at least 3 different techniques (forced variety rule)",` | Preventive measure | Low | The prompt (evals.json:160) names two techniques, and the eval grades three | Abductive | 55 | Reword the prompt or the assertion |

## HYPOTHESES
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| H9 | NOT_COMPUTABLE:13 and the skip at scripts/check_facts.py:92 | Rust facts were made optional on purpose, and the docs were not updated | The line is stale from before #25 (CHANGELOG.md:25) | Version history (not available: ./tree is not a repository) |
| H10 | CHANGELOG.md:5 `## Unreleased` lists evals 56 and 57 while plugin.json says 4.2 | Copies installed as "4.2" from different dates have different content | The tree is a development copy that is not shipped | Compare with the published 4.2 |
| H11 | .claude-plugin/plugin.json:3 `"version": "4.2",` | The plugin manager accepts a two-part version | It expects x.y.z | The manager's own manifest validation |

## HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| HB1 | scripts/check.py:478 | Binding between an eval and its facts (CHANGELOG.md:24) | Only the prompt is bound | Preventive measure (C14), with instances D2 and D3 | 85 |

---

# Domain 4: Documentation

## VERIFICATION DOMAIN
Documentation: README.md, CHANGELOG.md, docstrings and comments of the scripts, NOT_COMPUTABLE's header, eval text read as documentation of the skill's behaviour.

## GROUND TRUTH
The scripts as written; skills/adversarial-verify/SKILL.md and references/*.md; the directory listing of ./tree.

## DECOMPOSED CLAIMS
67 claims (Documentation return): install methods, version statements, check descriptions, stress and confidence rules, trust scoring, CHANGELOG entries, and eval quotations of SKILL.md.

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|
| Stale state | 7 (Doc2, Doc4, Doc5, Doc6, Doc9, Doc10, Doc11) | README.md, CHANGELOG.md, facts/_parse_day.py, evals.json |
| Self-contradicting instructions | 2 (Doc1, Doc3) | README.md |
| Orphaned expectations | 2 (Doc7, Doc12) | evals.json |
| Missing completeness (docs promise more than the checks do) | counted in Code (C1, C2, C3, C5, C6) | README.md:250, :251, :255, :261 |

## VERIFICATION RESULTS
### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| P1 | The badges show the current version and the skill count | README.md:1 `badge/skill-v4.2-blue`; README.md:2 `badge/skills-1-green`. Confidence 95 |
| P2 | references/ holds the three files README describes | README.md:109 `three files in references/`; SKILL.md:47-51. Confidence 95 |
| P3 | README's descriptions of the evals check, the short-term warning, neutral wording and references match check.py | README.md:249, :251, :252, :254 vs scripts/check.py:180-207, :271-273, :140-142, :506-520. Confidence 85-90 |
| P4 | README's method summaries match SKILL.md and execution.md | README.md:72 `minimum 3 per run, never twice on the same claim`; :78; :241; :243; :272 `+1 trust`. Confidence 95 |
| P5 | CHANGELOG 4.2 and Unreleased entries match the files | CHANGELOG.md:8 `a row only looked up cannot carry a score above 79`; :14; :15; :24 `for every eval from 29 on that states facts`. Confidence 90 |
| P6 | The documented test command is valid | scripts/test_check.py:3 `python3 -m unittest scripts/test_check.py`. Confidence 70 (general knowledge) |

### FAIL ❌
| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| Doc1 | README.md:89 | `cp skills/adversarial-verify/SKILL.md ~/.claude/skills/adversarial-verify/` | Demonstrated defect | High | The first install method copies SKILL.md only, and SKILL.md:49-51 then sends the verifier to missing reference files. README.md:117 says so itself: "`SKILL.md` alone would send the verifier to files that are not there." | Deductive | 95 | `cp -r skills/adversarial-verify ~/.claude/skills/` |
| Doc2 | README.md:125 | `The plugin declares its version in `.claude-plugin/plugin.json` (currently 4.1), …` | Demonstrated defect | Low (Data, Tests, Code agents) / Medium (Documentation agent) | plugin.json:3, SKILL.md:20 and README.md:1 say 4.2. The version check reads only badges (scripts/check.py:217), so this slipped through. Found by 4 of 4 domain agents | Deductive | 95 | Write 4.2, or drop the number |
| Doc3 | README.md:247 | `It needs `python3` 3.8 or later and nothing else.` | Demonstrated defect | Low | --staged and the hook need git (scripts/check.py:389-393), and README.md:264 says to use `py -3` on Windows (Documentation agent and category agent) | Deductive | 80 | Name git and `py -3` |
| Doc4 | CHANGELOG.md:3 | `… and the first entry below; `scripts/check.py` fails if they differ.` | Demonstrated defect | Low | The first entry is `## Unreleased` (CHANGELOG.md:5). check.py takes the first numbered entry | Deductive | 90 | "the first numbered entry below" |
| Doc5 | skills/adversarial-verify/evals/facts/_parse_day.py:1 | `# Shared by facts/37.py and facts/39.py: the functions as shown in the evals.` | Demonstrated defect | Low | facts/35.py:3 `from _parse_day import parse_day_v1` also uses it | Deductive | 95 | Add 35.py |
| Doc6 | scripts/test_check.py:1 | `"""Tests for scripts/check.py: the repo passes, and each invariant fails on a case built to break it.` | Demonstrated defect | Medium | The repo does not pass (D1), and T1 asserts nothing | Deductive | 90 | Fix D1 and T1 |
| Doc7 | skills/adversarial-verify/evals/evals.json:325 | `… proposes to comment on the existing issue #41 with the new evidence instead of opening a duplicate` | Demonstrated defect | Medium | The Documentation agent searched SKILL.md and references/*.md and did not find a rule on proposing issues or searching a tracker. Evals 25 and 26 (evals.json:337) grade behaviour the skill text does not define | Deductive | 80 | Add the rule to SKILL.md Step 5, or rewrite evals 25-26 |
| Doc8 | skills/adversarial-verify/evals/evals.json:249 | `… (code, data) or respected (plans, specs, docs, analyses)` | Demonstrated defect | Low | skills/adversarial-verify/SKILL.md:439 now reads "(code, data, tests, UX) or respected (plans, specs, docs, analyses, mock-ups)" | Deductive | 90 | Quote the current line |
| Doc9 | README.md:46 | `- **Propose project doc updates** — TODO.md, SPEC.md, PLAN.md (with user confirmation)` | Demonstrated defect | Low | SKILL.md Step 5 also lists CHANGELOG.md, ADR/ and the agent instruction files | Deductive | 80 | Same list as Step 5 |
| Doc10 | skills/adversarial-verify/evals/evals.json:113 | `"Checks for missing completeness in enums, switches, and factory methods",` | Preventive measure | Low | Uses the language-bound vocabulary from before the 3.6 rewrite. evals.json:210 `"Checks for flaky indicators: sleep(), retry, @Ignore/skip"` has the same problem | Deductive | 65 | Reword to the current terms |
| Doc11 | scripts/pre-commit:5 | `# --strict fails if no private terms are configured (see scripts/check.py).` | Demonstrated defect | Medium | The comment describes a flag the command does not pass. Counted with C6 (one defect, two texts: this comment and README.md:261) | Deductive | 90 | See C6 |
| Doc12 | skills/adversarial-verify/evals/evals.json:69 | `"Reads the migration file and the ORM model as artifacts",` | Preventive measure | Low | SKILL.md Step 0a names no ORM model. evals.json:388 (`short list of choices` vs Intake rule 6's multiple-choice tool) and evals.json:707 (output file in MUTATION PROBE vs execution.md's EXECUTED TESTS) also grade placements the skill does not define (category agent) | Deductive | 65 | Align the assertions with the skill text |

## HYPOTHESES
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| H12 | CHANGELOG.md:14 `57.3 kB to 46.4 kB … 62.5 kB` | The sizes are current | They predate later edits | Byte sizes of SKILL.md and references/*.md |
| H13 | README.md:226 `read on 2026-10-21` | The mutation-tool table matched the docs then | Flags changed since | Re-read the linked pages (a documentation read) |

## HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| HB1 | scripts/check.py:217 `badges = re.findall(r"badge/skill-v([0-9][0-9.]*)-", read_text(root, README, rep))` | The versions are kept consistent (README.md:250) | Prose versions are not checked | Demonstrated defect (Doc2) | 90 |
| HB2 | scripts/check.py:237 | "the first entry below" (CHANGELOG.md:3) | The first numbered entry | Demonstrated defect in the text (Doc4) | 90 |

---

## CROSS-DOMAIN SUMMARY
- **Domains:** Code, Tests, Data, Documentation.
- **Claims:** about 158 decomposed (37 + 24 + 30 + 67, with overlap). 27 PASS rows listed after merging. 59 in FAIL: Code 29, Tests 13, Data 5, Documentation 12. 0 falsified.
- **Survived:** stress tests were not done (not requested by the protocol brief).
- **Failure categories:** 9 systemic patterns:
  - missing completeness
  - silent fallthrough
  - assumed environment
  - test-environment artifact
  - stale state
  - contradictory records
  - tautological tests
  - orphaned expectations
  - self-contradicting instructions
- **Invariants:** the 6 checks of scripts/check.py and the toolchain rule of scripts/check_facts.py:8. At least 5 of them are violated or unenforced on the current tree: C1, C2, C3, C5 and D1.
- **Hypotheses:** 13 need further investigation.
- **Hidden behaviors:** 12 listed after merging.
- **Findings by type:** 26 demonstrated defects, 33 preventive measures, 0 falsified hypotheses.
- **Critical issues:** 0 rated critical. The high-severity demonstrated defects:
  - **D1.** check.py fails on the committed tree, so the hook blocks every commit and the suite is red.
  - **C6.** The hook does not run --strict.
  - **C5.** A missing toolchain is skipped silently.
  - **C2 and C3.** Private-term detection and masking have gaps (high per the domain agents, medium per the independent verifier).
  - **Doc1.** The first install method yields a broken skill.
- **Cross-domain changes:** these defects touch several domains at once:
  - **D1:** Data, Tests and Code.
  - **C1, C2, C3, C5, C6:** each is a gap between the code and README.md or the docstrings, counted once, in Code.
  - **C14:** the prompt-only hash lets the eval text drift (D2, D3).
- **Pre-code:** not applicable (no plan or spike in scope).
- **Executed:** 0 runs.
- **Proposed:** 8 checks and 0 writes awaiting an answer.
- **Recommendation:** do not trust the repository's own gate as it stands. D1 makes it fail closed, and C5 and C6 make it pass open. Fix D1, C6, C5, C3 and C2 first, then run the suite.

## PROPOSED EXECUTABLE CHECKS
| # | Claim | Confidence now | Check (command, test or query) | Confirms if | Refutes if | Cost and side effects | Status |
|---|-------|----------------|--------------------------------|-------------|------------|-----------------------|--------|
| 1 | D1: check.py fails on the tree | 90 | `python3 scripts/check.py` from ./tree | ERROR "eval 52 has a fact file and a reason not to have one", exit 1 | exit 0 | Reads the tree; needs git for the tracked-file list, otherwise walks the directory; writes nothing | proposed |
| 2 | H1: every prompt-sha256 matches | 50 | same run as #1 | no "prompt changed" lines | any such line | as #1 | proposed |
| 3 | H6, C1, C2, C3, T1: the predicted red tests | 79 | `python3 -m unittest scripts/test_check.py` | the predicted tests are red | they are green | Copies the tree to the system temp folder, runs git init/commit there; nothing written in ./tree | proposed |
| 4 | H2, H3, C5: fact files and the toolchain skip | 79 | `python3 scripts/check_facts.py`, then again with rustc and node removed from PATH | all pass; the second run prints "skip" with exit 0 | a FAIL, or a non-zero exit on the second run | Compiles 52.rs into a temp dir and runs node; no write in ./tree | proposed |
| 5 | H4: CRLF in the staged copy | 50 | `git config core.autocrlf`; compare a file in the --staged temp copy with `git show :path` | CRLF bytes | identical bytes | Read-only | proposed |
| 6 | H7, H8: Windows false reds | 50 | the suite under Windows without Developer Mode | symlink or rmtree errors | green | as #3 | proposed |
| 7 | H11: manifest version format | 50 | the plugin manager's manifest validation command | "4.2" accepted | rejected | Read-only | proposed |
| 8 | H12: CHANGELOG sizes | 50 | byte sizes of skills/adversarial-verify/SKILL.md and references/*.md | 46.4 kB / 62.5 kB | different | Read-only | proposed |

Proposed writes: none yet. The Fix column holds the changes that would be proposed one by one.

Shall I run any of checks 1-8 (name them), or prepare any of the fixes?
