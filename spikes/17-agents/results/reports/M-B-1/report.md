# Adversarial verification report: scripts/ of ./tree

Rows returned: 370 (Code 93, Tests 72, Documentation 102 on first pass, then 104 after the send-back, Independent verifier 19, Category agent 81). Rows discarded: 1, Documentation H8 (no quoted line). It was sent back, came back as H8a to H8c with valid quotes, and none was left discarded after the send-back. Independent verifier: 5 claims re-verified. It confirmed 4 (V1 to V4, all FAIL as the domain agents found) and changed 1 (V5, which the domain agents had as PASS and the verifier as FAIL, see K12). Every quote below was looked up at its line by the coordinator, so no PASS was lowered to 79 for a missing lookup.

## INTAKE

- Target: every domain detected in scripts/check.py, scripts/check_facts.py, scripts/pre-commit and scripts/test_check.py. The detected domains are **Code** (check.py, check_facts.py, pre-commit), **Tests** (test_check.py, plus the pre-commit hook as the automation that runs checks) and **Documentation** (docstrings, comments, usage and help text, error messages in the four files). The target was named in the request, so no question was asked.
- Depth: standard (stated). Scope: the whole of the four files; no diff and no history. Execution mode: reasoning only. **Nothing was run.** Every "test would be red" statement is a trace, not an observed result.
- To change these: name other domains or files, ask for deep depth, or approve the checks under PROPOSED EXECUTABLE CHECKS.

## GROUND TRUTH

The four files themselves. Also: README.md (the "Repository checks" section), CHANGELOG.md, .gitignore, .claude-plugin/plugin.json, skills/adversarial-verify/SKILL.md, evals/evals.json, evals/facts/* (37.py, 38.py, 40.py, 49.py, 51.py, 52.rs, 53.ts, NOT_COMPUTABLE). The domain agents read these. The coordinator opened case files only to look up quotes.

## INVARIANTS

These were not requested from the agents: the protocol brief limits each return to DECOMPOSED CLAIMS, PASS, FAIL, HYPOTHESES, HIDDEN BEHAVIORS and FAILURE CATEGORIES. The invariants the files state for themselves are checks 1 to 7 in scripts/check.py:6-44. Each is decomposed and verified as a claim below.

---

# DOMAIN: Code

## DECOMPOSED CLAIMS (Code, 34 returned; main ones)

1. Boolean and non-integer eval ids are rejected (scripts/check.py:186). Mode: Deductive
2. Ids are 1..n in file order (scripts/check.py:206). Mode: Deductive
3. From eval 21 on, assertions start with a [substance] or [format] tag followed by text (scripts/check.py:75). Mode: Deductive
4. The SKILL.md version matches every README skill badge (scripts/check.py:10). Mode: Deductive
5. Only a version inside the frontmatter counts (scripts/check.py:215). Mode: Deductive
6. The first numeric CHANGELOG entry must match (scripts/check.py:237). Mode: Deductive
7. The parts of a term may be joined by any run of non-alphanumeric characters (scripts/check.py:16). Mode: Deductive
8. Private terms are never printed (scripts/check.py:22). Mode: Deductive
9. Skipping the terms file during the scan is safe (scripts/check.py:14). Mode: Abductive
10. JSON strings are scanned after their escapes are decoded (scripts/check.py:20). Mode: Deductive
11. No terms gives a warning; with --strict, an error (scripts/check.py:297). Mode: Deductive
12. `=` terms match whole words only (scripts/check.py:275). Mode: Deductive
13. --staged checks exactly the staged content (scripts/check.py:389), and the temporary directory is always removed (scripts/check.py:440). Mode: Deductive
14. Fact-file rules: prompt sha256, not both a file and a reason, no orphans (scripts/check.py:481, :495, :470). Mode: Deductive
15. Reference files: every named file exists and every file is named (scripts/check.py:519). Mode: Deductive
16. Tables: cell counts; escaped pipes and code spans do not count; fenced blocks are skipped (scripts/check.py:345). Mode: Deductive
17. A missing toolchain is an error (scripts/check_facts.py:8). Mode: Deductive
18. A fact file needs an assertion and must end its output with "ok <id>" (scripts/check_facts.py:13); selecting no file fails the run (scripts/check_facts.py:113). Mode: Deductive
19. The hook runs --strict on what is staged, and runs the facts when the evals change (scripts/pre-commit:2, :5, :10). Mode: Deductive
20. A missing file gives an ERROR, not a crash (scripts/check.py:228). Mode: Deductive

## FAILURE CATEGORIES IDENTIFIED (Code)

| Category | Instances | Files affected |
|----------|-----------|---------------|
| Comment/docstring/code drift (the code is narrower than its stated contract) | 5 (K1-K5) | scripts/pre-commit:5, scripts/check.py:10, :16, :22, :399, scripts/check_facts.py:8 |
| Silent fallthrough | 8 (K3, K13, K16, K21, K22, HB-C1, HB-C5, category agent row 30) | scripts/check_facts.py:93, :85, scripts/pre-commit:17, scripts/check.py:151, :316, :436, :462 |
| Missing completeness | 7 (K5, K6, K11, K17, K24, K25, K26) | scripts/check.py:223, :301, :473, :494, :128, :330, :375 |
| Assumed environment | 5 (K4 CRLF, K18, K19, K20, H-C2) | scripts/check.py:90, :147, :389, scripts/pre-commit:8, :12 |
| Working tree leaking into a staged check | 3 (K12, K18) | scripts/check.py:423, :389, scripts/pre-commit:9, :15 |
| Inconsistent matching (detection vs masking, disk vs tracked) | 4 (K2, K14, K15, K8) | scripts/check.py:400, :182, :136, :364 |
| Boundary / quantifier error | 4 (K4, K5, K9, K23) | scripts/check.py:90, :223, :341, :75 |
| Implicit precedence | 1 (K13) | scripts/check.py:248 |

## VERIFICATION RESULTS (Code)

### PASS ✅

| # | Claim | Evidence |
|---|-------|---------|
| P-C1 | Boolean ids rejected | scripts/check.py:186 `if type(i) is not int:  # bool is an int subclass: reject it`. 95 |
| P-C2 | Ids 1..n in order | scripts/check.py:206 `if ids != list(range(1, len(ids) + 1)):`; duplicates are reported at :203-205. 95 |
| P-C3 | A tag needs text after it | scripts/check.py:75 `TAG_RE = re.compile(r"^\[(substance\|format)\]\s+\S")`, applied from id 21 on (:201). It is stricter than stated: see K23. 95 |
| P-C4 | Version read from the frontmatter only | scripts/check.py:216 `m = re.search(r'^\s*version:\s*"?([0-9][0-9.]*)"?\s*$', fm.group(1), re.M) if fm else None`. 92 |
| P-C5 | First numeric CHANGELOG entry | scripts/check.py:237 `first = re.search(r"^## +([0-9][0-9.]*)\b", read_text(root, CHANGELOG, rep), re.M)`. This skips CHANGELOG.md `## Unreleased`. 92 |
| P-C6 | JSON escapes decoded before the scan | scripts/check.py:315 `strings = [normalize(x) for x in json_strings(json.loads(text))]`. 92. A file that is not valid JSON is not decoded (K22) |
| P-C7 | Non-UTF-8 files scanned | scripts/check.py:122 `return data.decode("latin-1"), "latin-1"`. 95 |
| P-C8 | No terms: warning, or error with --strict | scripts/check.py:297 `(rep.error if strict else rep.warning)("private terms", msg)`. 95 |
| P-C9 | Whole-word `=` detection | scripts/check.py:275 `pats.append(re.compile(rf"(?<![^\W_]){body}(?![^\W_])" if whole_word else body))`. 92 |
| P-C10 | Temporary directory removed | scripts/check.py:438 `finally:`. 95 |
| P-C11 | Prompt hash binds each fact file | scripts/check.py:478 `want = hashlib.sha256(prompts[i].encode("utf-8")).hexdigest()`. 92. Only the first 2000 characters are searched; see K17 for two files per eval |
| P-C12 | Not both a fact file and a reason | scripts/check.py:496 `rep.error(f"{FACTS_DIR}/NOT_COMPUTABLE", f"eval {i} has a fact file and a reason not to have one")`. 95 |
| P-C13 | Orphan fact files rejected | scripts/check.py:471 `rep.error(f"{FACTS_DIR}/{name}", "fact file for an eval that does not exist")`. 92 |
| P-C14 | References exist and are named | scripts/check.py:518 `rep.error(f"{rel}:{ln}", f"names references/{name}, which does not exist")`. 92 |
| P-C15 | Cell counting | scripts/check.py:345 ``s = re.sub(r"`[^`]*`", "x", line).replace("\\|", "x").strip()``. The Code agent gave no confidence for this row; the coordinator assigns none. Weaknesses are in K8 and K9 |
| P-C16 | Assertion and "ok <id>" rules (Python) | scripts/check_facts.py:107 `if out[-1:] != [f"ok {stem}"]:`. 88. The Rust and TypeScript stripping is open (H-C1) |
| P-C17 | Selecting no file fails the run | scripts/check_facts.py:113 `return 1 if failed or not files else 0`. 95. Unknown ids that sit next to a valid one are dropped silently (K21) |
| P-C18 | The hook captures rc correctly | scripts/pre-commit:15 `out="$("$py" -I "$root/scripts/check_facts.py" --root "$tmp")"; rc=$?`. 90 |
| P-C19 | Facts run on the staged files | scripts/pre-commit:14 `git checkout-index -a --prefix="$tmp/" \|\| { rm -rf "$tmp"; exit 1; }`. 85. The trigger has gaps: HB-C4 and H-C3 |

### FAIL ❌

| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| K1 | scripts/pre-commit:9 | `"$py" -I "$root/scripts/check.py" --staged --root "$root" \|\| exit 1` | Demonstrated defect | High | The hook does not pass `--strict`, against its own comment at scripts/pre-commit:5 and README.md:260. With no terms configured, scripts/check.py:297 records only a warning and the run exits 0 (:442), so the commit goes through with private names unchecked. All three domain agents found this; the independent verifier confirmed it (FAIL, 95) | Deductive | 93 | Add `--strict` |
| K2 | scripts/check.py:400 | `pats = term_patterns(terms)` | Demonstrated defect | High | The comment at :399 says "substring patterns", but `substring=False` is the default (:259), so `=` terms are masked as whole words only. With term `=<T>` and an evals key `<T>labs`, :182 prints `unexpected keys ['<t>labs']` unmasked, and the term is printed. test_check.py:341-344 expects "message hidden". All three domain agents found this; the independent verifier confirmed it (FAIL, 85; it adds the path printed by :471 for a fact file `<T>x.py`) | Deductive | 92 | `term_patterns(terms, substring=True)` |
| K3 | scripts/check_facts.py:92 | `print(f"skip {name}: toolchain not found")` | Demonstrated defect | High | It runs `continue` (:93) without `failed += 1`, so a missing rustc or node gives exit 0 (:113), against :8 and README.md:254. The hook discards the output when rc is 0 (scripts/pre-commit:17), so the skip is fully silent. The skip also bypasses `has_assertion` (:95). All three domain agents found this; the independent verifier confirmed it (FAIL, 95) | Deductive | 92 | Print FAIL and `failed += 1` when `steps is None` |
| K4 | scripts/check.py:90 | `SEP = r"[\W_]?"  # anything that is not a letter or digit, possibly nothing` | Demonstrated defect | High | At most one separator character is allowed. Missed: two spaces (exercised by test_check.py:286), ` - `, and a CRLF line break (files are read as bytes, :126). The private term ships. All three domain agents found this; the independent verifier confirmed it (FAIL, 95) | Deductive | 90 | `SEP = r"[\W_]*"` |
| K5 | scripts/check.py:223 | `for b in badges[:1]:` | Demonstrated defect | Medium | Only the first README badge is compared, against :10 and README.md:249. A stale second `badge/skill-v2.0-` passes. test_check.py:171-173 expects "version mismatch" | Deductive | 90 | `for b in badges:` |
| K6 | scripts/check.py:301 | `if os.path.basename(rel) == TERMS_FILE:` | Preventive measure | High | Any file named `.check-private-terms`, at any depth and even tracked or staged (`git add -f`), is skipped: the term list itself can be committed while the check passes. Likelihood is low, because .gitignore:1 ignores the name | Abductive | 85 | ERROR when a TERMS_FILE is among the tracked or staged files |
| K7 | scripts/check.py:228 | `except ValueError as e:` | Demonstrated defect | Low | A missing SKILL.md, README.md, plugin.json or CHANGELOG.md (for example a staged deletion) raises FileNotFoundError and a traceback: no report, no masking (see H-C4). The exit is still 1 | Deductive | 88 | Catch OSError at each read and call `rep.error` |
| K8 | scripts/check.py:366 | `fence = None` | Preventive measure | Low | Any fence line closes the open fence, whatever its character or length (:364 stores the character and never compares it). A ```` ``` ```` line inside a `~~~` block ends the skip early, and every table after it is skipped silently or misread | Deductive | 82 | Close only on the same character with at least the opening length |
| K9 | scripts/check.py:341 | `DELIM = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")` | Preventive measure | Low | GFM accepts 1-2 dash delimiter cells. Such a table is not recognized, and its rows are never checked, with no message | Deductive | 85 | `-+` |
| K10 | scripts/check_facts.py:100 | `r = subprocess.run(step, cwd=FACTS, capture_output=True, text=True)` | Preventive measure | Low | There is no timeout. A fact file that loops forever hangs the runner and the pre-commit hook | Deductive | 80 | `timeout=`, and count TimeoutExpired as FAIL |
| K11 | scripts/check.py:494 | `reasons[int(m.group(1))] = m.group(2)` | Preventive measure | Low | A NOT_COMPUTABLE reason for a non-existent eval, or a duplicate id, is accepted silently, while fact files get the opposite treatment (:470) | Deductive | 85 | Report reasons whose id is unknown, and duplicates |
| K12 | scripts/check.py:423 | `terms = load_terms(args.root)  # always from the working repo: the list is never committed` | Preventive measure | Medium | **Disputed, reported at the lower confidence.** Domain verdicts: Code PASS 88 (C14 "--staged checks the index", scripts/check.py:433 `root = tmp`) and Documentation PASS 85 (P13). Independent verifier: FAIL 85. With --staged the file content comes from the index, but the term list comes from the working tree and the environment, and the hook runs the working-tree check.py and check_facts.py (scripts/pre-commit:9, :15). Unstaged edits to these, or deleting the untracked terms file, change the result of a staged check. The narrower claim (the checked content is the staged content) holds, apart from H-C5. The terms source is documented as intentional; the script source is not. The category agent found the same (rows 40-41, 90) | Deductive | 85 | Run the hook's checkers from the staged copy (`$tmp/scripts/...`), and document that terms come from the working tree |
| K13 | scripts/check.py:248 | `if raw is not None:` | Demonstrated defect | Medium | CHECK_PRIVATE_TERMS, if set at all (even to "" or " , "), silently replaces the `.check-private-terms` file. The docstring (:14) says "or". An exported empty variable disables the file and turns the check into a warning when --strict is not set (the hook does not set it, K1). Found by the category agent, and also Documentation HB2 | Deductive | 90 | Merge both sources, or warn when the variable shadows an existing file |
| K14 | scripts/check.py:182 | `rep.error(where, f"unexpected keys {extra} (put facts in the prompt)")` | Demonstrated defect | Medium | The key list is printed as a `repr()`. A key with a real newline between two term parts is detected in the decoded text but printed as a literal `\n` (two characters), which `[\W_]?` does not span, so mask leaves the term readable. Category agent | Deductive | 80 | Mask on the decoded form, or never print key names |
| K15 | scripts/check.py:136 | `names = sorted(os.listdir(d)) if os.path.isdir(d) else []` | Demonstrated defect | Medium | Checks 4, 5 and 7 read references/ from disk, tracked or not, but check 3 scans only git-tracked files. An untracked reference file that ships with the folder (:43-44) is never scanned for private terms. Category agent; also Code HB12 | Deductive | 88 | Add the files of the skill folder on disk to check 3's list |
| K16 | scripts/check.py:151 | `except (OSError, subprocess.CalledProcessError):` | Demonstrated defect | Medium | Any git failure (no repo, safe.directory, broken index) or an empty `ls-files` (:149) falls back silently to os.walk over every file on disk. The summary still says "working tree" | Deductive | 88 | Say in the summary which file list was used |
| K17 | scripts/check.py:473 | `with_file[int(stem)] = name` | Demonstrated defect | Medium | Two fact files for one eval (38.py and 38.rs) overwrite each other: only the last one is hash-checked, while check_facts.py runs both. Category agent | Deductive | 90 | Keep a list per id; error on more than one |
| K18 | scripts/check.py:389 | `subprocess.run(["git", "-C", root, "checkout-index", "-a", "--prefix=" + tmp + os.sep],` | Preventive measure | Medium | checkout-index applies the local eol, autocrlf and smudge filters, so the scanned copy is the staged content after local filters, not the blobs. With autocrlf this produces the CRLF miss of K4. The same applies to scripts/pre-commit:14. Category agent | Deductive | 75 | Read the blobs (`git cat-file --batch`), or disable the filters for the export |
| K19 | scripts/pre-commit:8 | `command -v "$py" >/dev/null 2>&1 \|\| py=python` | Preventive measure | Medium | On Windows, `python3` may be the Store alias stub, and `python` may be Python 2; either one blocks every commit with an unrelated error. check.py:50 advises `py -3`, which the hook never tries. Category agent, plus Code H2 and Documentation H2 | Deductive | 75 | Try `py -3`; check the version |
| K20 | scripts/pre-commit:12 | `if git diff --cached --name-only \| grep -q '^skills/adversarial-verify/evals/'; then` | Preventive measure | Low | With core.quotePath (the default), a non-ASCII path is printed quoted, so `^skills/` misses it and the facts run is skipped. Category agent and Code H5 | Deductive | 75 | `git -c core.quotePath=false diff --cached --name-only -z` |
| K21 | scripts/check_facts.py:85 | `files = [f for f in files if os.path.splitext(f)[0] in ids]` | Demonstrated defect | Low | `check_facts.py 38 999` runs 38, succeeds and never mentions 999. Documentation HB9 and category agent | Deductive | 90 | Report requested ids with no file |
| K22 | scripts/check.py:316 | `except ValueError:` | Demonstrated defect | Low | A .json file that is not valid JSON is not decoded, without a word, so a `\uXXXX`-escaped term in it passes. Category agent | Deductive | 85 | Warn when a .json file does not parse |
| K23 | scripts/check.py:75 | `TAG_RE = re.compile(r"^\[(substance\|format)\]\s+\S")` | Demonstrated defect | Low | It is stricter than "followed by text" (:9): `[substance]text` is rejected, and the message at :202 does not mention the space. Category agent | Deductive | 85 | State "followed by a space and text" |
| K24 | scripts/check.py:128 | `if enc != "utf-8" and rep is not None and (rel in (SKILL, README, EVALS) or rel.startswith(REFS_DIR + "/")):` | Preventive measure | Low | CHANGELOG.md, plugin.json, fact files and NOT_COMPUTABLE are silently read as Latin-1, with no error. Documentation HB5 and category agent | Deductive | 85 | Extend the list, or document it |
| K25 | scripts/check.py:330 | `patterns = [re.compile(t) for t in STACK_TERMS]` | Preventive measure | Low | There is no IGNORECASE, so "python" and "Sqlite" are not warned. Category agent | Deductive | 85 | `re.I` for the plain words |
| K26 | scripts/check.py:375 | `while i < len(lines) and lines[i].strip() and "\|" in lines[i]:` | Preventive measure | Low | A row that lost all its pipes ends the table silently instead of being counted as a 1-cell row. Category agent | Deductive | 75 | Treat non-blank lines that follow as rows |
| K27 | scripts/check.py:15 | `(one per line, # for comments). Matching ignores case, accents and Unicode` | Demonstrated defect | Medium | Only whole-line comments are recognized (:255). `term  # note` becomes a term whose parts include "note", so plain "term" is no longer detected. Category agent | Deductive | 88 | Strip trailing `#` comments, or document whole-line only |

## HYPOTHESES (Code)

| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| H-C1 | scripts/check_facts.py:37 `".rs": re.compile(r'//[^\n]*\|/\*.*?\*/\|"(?:\\.\|[^"\\])*"', re.S),`: char literals and raw strings are not modelled | A `'"'` literal or an `r#"..."#` string misaligns the stripping: false accept or false reject of `has_assertion`. The same holds for .ts nested templates (scripts/check_facts.py:38) | No current fact file contains these literals | Feed such a file to `has_assertion` |
| H-C2 | scripts/check.py:525 `print(line)`, run with -I, so PYTHONIOENCODING and PYTHONUTF8 are ignored | On Windows with piped stdout, a non-cp1252 path raises UnicodeEncodeError and the report is lost. The same applies to the decoding of fact output (scripts/check_facts.py:100) | The console or Python defaults to UTF-8 | Run it on Windows with stdout piped |
| H-C3 | scripts/pre-commit:12 `if git diff --cached --name-only \| grep -q '^skills/adversarial-verify/evals/'; then`, with rename detection | Moving a fact file out of evals/ prints only the new path, and the facts run is skipped | Check 6 still reports the missing file | Stage a `git mv` out of evals/ |
| H-C4 | scripts/check.py:22 `(UTF-16 if it has a BOM, otherwise Latin-1). Terms are never printed: any`, while tracebacks (K7) bypass `mask` | A traceback can print a path that contains a term | Paths in tracebacks are fixed constants | Remove README.md and use a term equal to a root path component |
| H-C5 | scripts/check.py:389 `subprocess.run(["git", "-C", root, "checkout-index", "-a", "--prefix=" + tmp + os.sep],` without `--ignore-skip-worktree-bits` | In a sparse checkout, out-of-cone entries are not written, so they are reported as "unreadable file" | git writes them anyway | Run `git sparse-checkout set scripts`, then `check.py --staged` |
| H-C6 | scripts/check.py:126 `with open(os.path.join(root, rel), "rb") as f:` | A staged absolute symlink makes the staged check read a file outside the staged content | core.symlinks=false (the Windows default) | Stage a symlink to a file that contains a term |
| H-C7 | scripts/pre-commit:15 `out="$("$py" -I "$root/scripts/check_facts.py" --root "$tmp")"; rc=$?` on Git for Windows | With MSYS_NO_PATHCONV, the /tmp path does not reach native Python, and the facts run fails | The conversion applies, and it works | Run the hook on Git for Windows with and without the variable |
| H-C8 | scripts/check_facts.py:62 `exe = os.path.join(tmp, os.path.basename(path) + ".bin")` | On Windows the `.bin` binary runs normally | rustc or Windows rejects it, and .rs facts FAIL on Windows only | Run `check_facts.py 52` on Windows |

## HIDDEN BEHAVIORS DETECTED (Code)

| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| HB-C1 | scripts/check.py:436 `if files or not args.staged:` | --staged checks what is staged | With an empty index no check runs, the exit is 0, and the summary lists no checks | Preventive measure | 88 |
| HB-C2 | scripts/check.py:465 `files = sorted(os.listdir(fdir)) if os.path.isdir(fdir) else []` | "Files checked: the files tracked by git" (:46) | Checks 1, 2 and 4-7 read the disk, untracked files included; check 3 reads tracked files only | None, see K15 | 85 |
| HB-C3 | scripts/check.py:186 `if type(i) is not int:  # bool is an int subclass: reject it` | Prompt, output and assertions are checked per eval | An eval with a non-int id skips its field and tag checks (`continue`, :188) | Preventive measure | 85 |
| HB-C4 | scripts/pre-commit:12 `if git diff --cached --name-only \| grep -q '^skills/adversarial-verify/evals/'; then` | Facts run when they could change | A change to scripts/check_facts.py alone does not trigger the run | Preventive measure | 90 |
| HB-C5 | scripts/check.py:462 `return  # check 1 already reports it` | The summary lists the checks that ran | "eval facts" is already listed (:458) when the check returns early | None (check 1 reports the error) | 85 |
| HB-C6 | scripts/check.py:469 `if ext in FACT_EXTS and not stem.startswith("_"):` and :476 `head = read_text(root, f"{FACTS_DIR}/{name}")[:2000]` | Every fact file is bound to an eval | `_` helpers are exempt, and the hash must sit in the first 2000 characters | None | 88 |
| HB-C7 | scripts/check_facts.py:50 `return any(isinstance(n, (ast.Assert, ast.Raise)) for n in ast.walk(tree))` | A fact file asserts something | `assert True`, or a `raise` in a function that is never called, satisfies the rule | Preventive measure | 85 |

---

# DOMAIN: Tests

## DECOMPOSED CLAIMS (Tests, 24 returned; main ones)

1. `assert_fails` counts a failure only if the script ran to its summary, printed an ERROR, named the failure and leaked no term (scripts/test_check.py:58). Mode: Deductive
2. Test terms never appear literally in the repo (scripts/test_check.py:25). Mode: Deductive
3. Every fixture edit targets text that exists (scripts/test_check.py:550, :582). Mode: Deductive
4. Boundaries are tested on both sides: TAGGED_FROM (scripts/test_check.py:151), FACTS_FROM (scripts/check.py:498). Mode: Deductive
5. The tests are isolated from the developer's environment and take production's path (scripts/test_check.py:43, :50). Mode: Deductive
6. The fact-runner tests prove that the facts ran (scripts/test_check.py:578). Mode: Deductive
7. Something runs the unit tests automatically (scripts/pre-commit:9). Mode: Abductive

## FAILURE CATEGORIES IDENTIFIED (Tests)

| Category | Instances | Files affected |
|----------|-----------|---------------|
| Tautological or vacuous test | 3 (T1, T2, T6) | scripts/test_check.py:479, :578, :617 |
| Test-environment artifact | 6 (T3, T4, T5, T7, T12, T13) | scripts/test_check.py:43, :84, :351, :390, :31, :35, :374, :502, :576 |
| Missing negative test | 4 (T8, T9, T10, T14) | scripts/test_check.py, scripts/pre-commit:9, scripts/check.py:498, :248, :301, :473, :271, :366, :129, :90, scripts/check_facts.py:37, :91 |
| Test-code drift | 2 (T11, D6) | scripts/test_check.py:337, :336, :4 |
| Expected-red tests (the code is narrower than the test) | 3 (H-T1 to H-T3, traced to K2, K4, K5) | scripts/test_check.py:173, :289, :344 |

## VERIFICATION RESULTS (Tests)

### PASS ✅

| # | Claim | Evidence |
|---|-------|---------|
| P-T1 | `assert_fails` is strict | scripts/test_check.py:57 `self.assertNotEqual(r.returncode, 0, out)` plus the summary, ERROR and token checks and `assert_no_leak` (:58-62). A traceback cannot count as a failure. 88 |
| P-T2 | Test terms are not literal | scripts/test_check.py:24 `NONE = "nosuch" + "term7f3a"`; quote, space and plus between the halves exceed what SEP can span. 82 |
| P-T3 | The eval 37 edit targets real text | skills/adversarial-verify/evals/evals.json:463 contains `day > 31` (the row quotes only this fragment; found at :463); index 36 is id 37. 82 |
| P-T4 | TAGGED_FROM tested on both sides | scripts/test_check.py:158 `self.assertFalse(e["assertions"][0].startswith("["), "eval 20 is untagged by design")` and :149-153 for id 21. 85 |
| P-T5 | 38.py edit targets real text | skills/adversarial-verify/evals/facts/38.py:21 `assert round(10.05 * 0.9, 2) == 9.05`. 88 |
| P-T6 | 49.py edits remove every assertion | skills/adversarial-verify/evals/facts/49.py:12 `assert clipped(375) == (77.75, {'Bestellungen', 'Einstellungen'})` (lines 12-14). 88 |
| P-T7 | 40.py edit targets real text | skills/adversarial-verify/evals/facts/40.py:13 `print('ok 40')`. 86 |
| P-T8 | FACTS_FROM rule bites above the boundary | skills/adversarial-verify/evals/facts/NOT_COMPUTABLE:4 `30: repository size and contents, no code`. 85. The boundary itself is untested (T8) |
| P-T9 | Newest CHANGELOG entry test | scripts/test_check.py:223 `i = s.index("\n## ")`. 85 |
| P-T10 | Staged orphan test | scripts/test_check.py:508 `self.assert_passes(self.run_check("--staged", terms=NONE))  # not staged: not part of the commit`. 82 |
| P-T11 | Frontmatter edit targets real text | skills/adversarial-verify/SKILL.md:20 `  version: "4.2"`. 85 |
| P-T12 | The terms file is gitignored | .gitignore:1 `.check-private-terms`. 90 |
| P-T13 | Whole-word opt-in tested in both directions | scripts/test_check.py:261 `self.assert_fails(self.run_check(terms=prefix), "private term #1")`. 82 |

### FAIL ❌

| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| T1 | scripts/test_check.py:479 | `self.assertIn("orphan.md", r.stdout + self.ref("orphan.md"))` | Demonstrated defect | Medium | Tautology: the needle is always in `self.ref(...)`, and no exit code is checked. Deleting scripts/check.py:519-520 keeps it green; only :481-485 would catch it. Tests, Code and Documentation agents and the category agent all found it | Deductive | 95 | `self.assert_fails(r, "orphan.md", "never named in SKILL.md")` |
| T2 | scripts/test_check.py:578 | `self.assertRegex(r.stdout, r"\d+ fact file\(s\), 0 failed")` | Demonstrated defect | Medium | Without rustc or node it is green while 52.rs and 53.ts never ran (K3): skips count as files with 0 failed. After K3 is fixed it becomes a false red on such machines, because :576 has no skip guard | Deductive | 88 | Assert no `skip` line, or one `ok` line per file; skip when a toolchain is missing |
| T3 | scripts/test_check.py:43 | `env = dict(os.environ)` | Preventive measure | Medium | A developer's exported CHECK_PRIVATE_TERMS overrides the terms file (K13): tests :355 and :360 go red, :318 tests the wrong terms, and :328 passes vacuously | Deductive | 85 | `env.pop("CHECK_PRIVATE_TERMS", None)` before setting `terms` |
| T4 | scripts/test_check.py:85 | `f.write("\n" + text + "\n")` | Preventive measure | Low | On Windows (supported, README.md:263) text mode writes `\r\n`, so the variant `f"{a}\n{b}"` (:286) is red on Windows only. On Linux the CRLF case is never exercised | Deductive | 80 | `newline="\n"` in `append`/`edit`; add an explicit CRLF test |
| T5 | scripts/test_check.py:351 | `os.symlink(os.path.join(self.tmp, "does-not-exist"), self.path("dangling.md"))` | Demonstrated defect | Low | On Windows without symlink privilege, the test errors: a false red. The same kind of risk holds for scripts/test_check.py:390 `shutil.rmtree(self.path(".git"))`, which hits read-only git objects on Windows (75) | Deductive | 80 | Skip on OSError; `onerror` handler for rmtree |
| T6 | scripts/test_check.py:617 | `self.assertNotEqual(r.returncode, 0, r.stdout)` | Preventive measure | Low | Any crash also exits non-zero, so the test does not show that the "no files" rule (scripts/check_facts.py:113) is the cause | Deductive | 85 | Also assert `0 fact file(s)` and no Traceback |
| T7 | scripts/test_check.py:50 | `[sys.executable, "-I", os.path.join(self.tmp, "scripts", "check.py"), "--root", self.tmp, *args],` | Preventive measure | Low | The Base copy is not a git repo, so non-git tests take the os.walk fallback (scripts/check.py:153), not production's `git ls-files`. Tests that rely on untracked files being scanned (file name, latin1, utf16, unreadable) pass only because of the fallback (category agent row 57, 88). LICENSE is not copied | Deductive | 80 | Run RepoTest and the scan tests on a `git init`-ed copy too |
| T8 | scripts/check.py:498 | `if not isinstance(e, dict) or type(e.get("id")) is not int or e["id"] < FACTS_FROM:` | Preventive measure | Low | Missing boundary test: eval 28 states facts and is exempt, and eval 29 does not state facts, so a `<=` mutant survives every test | Deductive | 80 | A test that adds `(Facts:` to eval 29 |
| T9 | scripts/pre-commit:12 | `if git diff --cached --name-only \| grep -q '^skills/adversarial-verify/evals/'; then` | Preventive measure | Medium | Nothing runs scripts/test_check.py automatically: no CI file in ./tree, and the hook never calls it. No test exercises the hook either (K1 would have been caught). K2, K4 and K5 are traced reds that nothing runs | Abductive | 75 | Run the unit tests in the hook when scripts/ is staged, or add CI |
| T10 | scripts/test_check.py:64 | `def assert_passes(self, r):` | Preventive measure | Low | `assert_no_leak` runs only inside `assert_fails` (:62). A passing run that printed a term in a WARNING would go unnoticed, against :4-5 | Deductive | 88 | Call `assert_no_leak` in `assert_passes` |
| T11 | scripts/test_check.py:337 | `# whole-word detection does not flag "<term>labs", but the evals check prints the key name` | Demonstrated defect | Low | Test-code drift: `terms=T1` (no `=`) is substring detection, so `<term>labs` is detected. The test duplicates :331-334, and its name ("even if not detected", :336) is stale. Found by all three domain agents and the category agent | Deductive | 90 | Rename or delete; :341 is the real case |
| T12 | scripts/test_check.py:503 | `git = lambda *a: subprocess.run(["git", "-C", self.tmp, "-c", "user.name=t", "-c", "user.email=t@t", *a],` | Preventive measure | Low | There is no `skipUnless(git)` guard (unlike :369), so it errors without git. It and StagedTest (:374) also inherit the global git config: commit.gpgsign or core.hooksPath break `check=True` | Deductive | 80 | Move it under the git skip; pass `-c commit.gpgsign=false -c core.hooksPath=` |
| T13 | scripts/test_check.py:35 | `shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__"))` | Preventive measure | Low | The fixture copies the developer's working tree, untracked files included. An untracked references/draft.md turns test_repo_passes red. Category agent | Deductive | 85 | Copy from `git ls-files` |
| T14 | scripts/check_facts.py:91 | `if steps is None:` | Preventive measure | High | Missing negative tests. Nothing simulates a missing toolchain (it would have caught K3). Also untested: the env/file precedence (scripts/check.py:248), a tracked terms file (:301), two fact files per eval (:473), the 4-character term boundary (:271), mismatched fences (:366), the non-UTF-8 error (:129), a CRLF file written in binary (:90), and assertion stripping for .rs and .ts (scripts/check_facts.py:37). Category agent rows 62-72 | Deductive | 88 | One targeted test per branch |

## HYPOTHESES (Tests)

| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| H-T1 | scripts/test_check.py:173 `self.assert_fails(self.run_check(terms=NONE), "version mismatch")`; trace K5 | The test is red now | The tree differs from what was last tested | `python3 -m unittest scripts/test_check.py` (proposed, not run) |
| H-T2 | scripts/test_check.py:289 `self.assert_fails(self.leak(f"Seen in {variant}."), "private term #2")`; trace K4, two-space variant | The subtest is red now | As above | As above |
| H-T3 | scripts/test_check.py:344 `self.assert_fails(self.run_check(terms="=" + T1), "message hidden")`; trace K2 | The test is red now | As above | As above |
| H-T4 | scripts/test_check.py:320 `r = self.run_check(terms_file=("﻿" + f"{T1}\n# a comment\n").encode("utf-8"))`: the string renders as empty | It holds a literal U+FEFF | It is empty, and the test does not test a BOM | Inspect the bytes for `EF BB BF` |
| H-T5 | scripts/test_check.py:43 `env = dict(os.environ)`, under a git hook | Inherited GIT_DIR or GIT_INDEX_FILE make `git -C tmp` act on the outer repo | Not set in the usual contexts | Run with `GIT_DIR` exported |
| H-T6 | scripts/test_check.py:414 `self.assertIn("SQLite", open(self.path(EVALS)).read())`, with no encoding | It raises UnicodeDecodeError on Windows if evals.json contains certain characters | None present (partial grep by the category agent) | Run on Windows |
| H-T7 | scripts/test_check.py:3 `Run from the repo root: python3 -m unittest scripts/test_check.py` | It works (namespace package) | The import fails on some Python version | Run the command |

## HIDDEN BEHAVIORS DETECTED (Tests)

| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| HB-T1 | scripts/check_facts.py:90 `steps = command(path, tmp)` | Every fact file must contain an assertion | `command()` runs before `has_assertion()`, so a .rs or .ts file with no assertion is not checked at all without its toolchain | Preventive measure | 88 |

---

# DOMAIN: Documentation

## DECOMPOSED CLAIMS (Documentation, 39 returned; main ones)

1. The docstring of check.py (scripts/check.py:4-50) describes checks 1-7, the file list, the usage line and the Python floor. Mode: Deductive
2. The docstring of check_facts.py (scripts/check_facts.py:2-18) describes the toolchains, the assertion rule and the usage examples. Mode: Deductive
3. The pre-commit comments (scripts/pre-commit:2-5, :10-11) describe what the hook runs and how to install it. Mode: Deductive / Abductive
4. The test docstring and comments (scripts/test_check.py:1-5, :22-23, :324, :332, :337, :581) describe the suite. Mode: Deductive
5. The error messages cite the right lines (scripts/check.py:373, :378). Mode: Deductive

## FAILURE CATEGORIES IDENTIFIED (Documentation)

| Category | Instances | Files affected |
|----------|-----------|---------------|
| Doc-code drift: the text promises what the code does not do | 5, counted in Code (K1-K5) | scripts/pre-commit:5, scripts/check.py:10, :16, :22, :399, scripts/check_facts.py:8. The same promises are repeated in README.md:249, :254, :260 (see OUT OF SCOPE) |
| Stale or incomplete text | 6 (D1-D6) | scripts/check.py:43, :46, scripts/test_check.py:1, :4, :23, scripts/check_facts.py:7 |
| Implicit precedence (undocumented) | 1 (K13, counted in Code) | scripts/check.py:14 |

## VERIFICATION RESULTS (Documentation)

### PASS ✅

| # | Claim | Evidence |
|---|-------|---------|
| P-D1 | Exit status depends on errors only | scripts/check.py:4 `Errors make the exit code non-zero; warnings are printed but do not block.`; :442. 90 |
| P-D2 | Check 1 as described | scripts/check.py:6 `1. evals.json: valid JSON; exactly the keys id/prompt/expected_output/assertions;`; :180-207. 88 |
| P-D3 | plugin.json and the CHANGELOG version | scripts/check.py:11 `the "version" string in .claude-plugin/plugin.json and the first "## <version>"`. 90 |
| P-D4 | Case, accents and Unicode forms ignored | scripts/check.py:15; :93-96. 90 |
| P-D5 | `=` whole word; short or empty terms | scripts/check.py:18, :20; :265-273. 90 |
| P-D6 | JSON escapes; non-UTF-8 still scanned | scripts/check.py:21 `scanned after decoding escapes. A file that is not UTF-8 is still scanned`. 88 |
| P-D7 | No terms: warning, or failure with --strict | scripts/check.py:23 `output line containing one is masked. Without terms the check says so; with`. 92 |
| P-D8 | Neutral wording: warnings only, evals.json excluded | scripts/check.py:27 `4. Neutral wording: technology-bound terms in SKILL.md, its reference files and`. 90 |
| P-D9 | Tables as described | scripts/check.py:31 `without outer pipes: every`. 82 (see K8, K9) |
| P-D10 | Facts rule as described | scripts/check.py:35 `has a file facts/<id>.py\|.rs\|.ts (run by scripts/check_facts.py) or a line`. 88 |
| P-D11 | Named references exist | scripts/check.py:40 `references/ that hold the rest. Every "references/<name>.md" named in SKILL.md`. 88 |
| P-D12 | --staged: the content staged | scripts/check.py:47 `available). With --staged, exactly the content staged for the next commit.`. 85. **Disputed by the independent verifier (V5, FAIL 85)**: the term list and the scripts come from the working tree. See K12, filed under Code at 85 |
| P-D13 | Usage line matches the CLI | scripts/check.py:49 `Usage: python3 scripts/check.py [--strict] [--staged] [--root PATH]`. 92 |
| P-D14 | Error messages cite the correct header line | scripts/check.py:373 `rep.error(f"{rel}:{i + 1}", f"table delimiter has {count_cells(lines[i])} cells, header at line {i} has {header}")`. 90 |
| P-D15 | Toolchain per extension | scripts/check_facts.py:6. 90 |
| P-D16 | Assertion and ok-line rule | scripts/check_facts.py:11. 85 |
| P-D17 | Usage examples | scripts/check_facts.py:17 `python3 scripts/check_facts.py 38 49           # only these eval ids`. 88 |
| P-D18 | The hook checks staged content | scripts/pre-commit:2. 88 (see K12) |
| P-D19 | Install path | scripts/pre-commit:3 `# Install once: ln -s ../../scripts/pre-commit .git/hooks/pre-commit`. 85 for the path; the exec bit is H-D1 |
| P-D20 | Facts trigger and staged files | scripts/pre-commit:10. 85 |
| P-D21 | Test terms not literal | scripts/test_check.py:22. 85 |
| P-D22 | Eval 20 is untagged | scripts/test_check.py:158; evals.json:269. 92 |
| P-D23 | BOM stripped before the comment test | scripts/test_check.py:324; scripts/check.py:120. 90 |
| P-D24 | The evals check prints key names | scripts/test_check.py:332; scripts/check.py:182. 92 |
| P-D25 | Fact 38 holds the edited assertion | scripts/test_check.py:582; facts/38.py:21. 85 (history: H-D3) |

### FAIL ❌

| # | File:Line | Quote | Type | Severity | Scenario | Mode | Confidence | Fix |
|---|-----------|-------|------|----------|----------|------|------------|-----|
| D1 | scripts/check.py:46 | `Files checked: the files tracked by git (all files outside .git if git is not` | Demonstrated defect | Low | The fallback also happens when root is not a repo, git errors, or nothing is tracked (:149-152) | Deductive | 85 | "...if git is not available, root is not a repository, or nothing is tracked" |
| D2 | scripts/test_check.py:1 | `"""Tests for scripts/check.py: the repo passes, and each invariant fails on a case built to break it.` | Preventive measure | Low | The module also tests check_facts.py (:571-617), which the docstring does not name | Deductive | 82 | Name check_facts.py |
| D3 | scripts/check.py:43 | `reader nowhere. The folder is read as it is on disk, tracked or not, since` | Demonstrated defect | Low | With --staged, the folder read is the staged copy (:433); test_check.py:508 relies on this | Deductive | 85 | Add "(with --staged: as staged)" |
| D4 | scripts/test_check.py:23 | `# including this one (the check scans every file). Neither occurs in the repo.` | Demonstrated defect | Low | Three constants are defined (:24-26); "Neither" covers two | Deductive | 85 | "None of them" |
| D5 | scripts/check_facts.py:7 | `are compiled with rustc; .ts files run with node --experimental-strip-types.` | Preventive measure | Low | The flag needs node 22.6 or later (README.md:246); the docstring states no version | Abductive | 65 | State the node version |
| D6 | scripts/test_check.py:4 | `Every failing case must come from the script's own ERROR and summary, and no` | Demonstrated defect | Low | The check_facts runner tests (:580-617) assert on FAIL lines or return codes only, never ERROR, the summary or `assert_no_leak`. Category agent | Deductive | 88 | Scope the sentence to check.py |

## HYPOTHESES (Documentation)

| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|
| H-D1 | scripts/pre-commit:3 `# Install once: ln -s ../../scripts/pre-commit .git/hooks/pre-commit`; a symlinked hook needs the exec bit | The file is tracked 100755 | It is tracked 100644, and git ignores the hook silently | `git ls-files -s scripts/pre-commit` |
| H-D2 | scripts/check.py:50 `Requires Python 3.8 or later. On Windows use \`py -3 scripts/check.py\`.` | The floor is a policy; no 3.8-only construct was found | A 3.8 feature was missed | Run under 3.7 |
| H-D3 | scripts/test_check.py:581 `# The first draft of eval 38 stated round(10.05 * 0.9, 2) == 9.04: the runner must catch it.` | The history claim is true | The comment is illustrative | `git log -p` (no history in ./tree) |
| H-D4 | scripts/pre-commit:4 `# (on Windows, Git for Windows runs this file with its own sh; copy it instead of linking)` | Correct | Symlinks work with core.symlinks and Developer Mode | Commit on Windows with both setups |

## HIDDEN BEHAVIORS DETECTED (Documentation)

| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|
| HB-D1 | scripts/check.py:247 `raw = os.environ.get("CHECK_PRIVATE_TERMS")` | Terms from the variable "or" the file | The variable (even empty) overrides the file entirely; counted as K13 | Demonstrated defect | 90 |
| HB-D2 | scripts/check.py:301 `if os.path.basename(rel) == TERMS_FILE:` | Every file is scanned | Files with that name are skipped at any depth; counted as K6 | Preventive measure | 88 |

---

## OUT OF SCOPE (listed, not verified)

- README.md:249 ("every skill badge"), README.md:254 ("fails ... if a needed toolchain ... is missing"), README.md:260 ("runs --strict --staged"). These repeat the promises that K5, K3 and K1 break, so fixing the code or the docstrings leaves them to update.
- No CI configuration exists in ./tree (T9).

## STRESS TEST RESULTS

Not run as a separate pass. The protocol brief limits each return to the six listed sections. The independent verifier is the stress pass on the 5 highest-risk claims: 4 confirmed and 1 changed (K12).

## ADVERSARIAL SCAFFOLD FINDINGS

- Reviewer blind spots: the hook's missing `--strict` (K1), and a skip that the hook prints nowhere (K3 with scripts/pre-commit:17). In both cases the comment says the right thing, so a reader stops there.
- Highest-risk claims: K1 (the private-name check is silently off for any contributor without terms), K2 (the leak path in the one function whose job is to hide terms), K4 (two spaces or a CRLF wrap defeats detection).
- Multi-step traces: no terms configured → hook without --strict (scripts/pre-commit:9) → warning (scripts/check.py:297) → exit 0 → commit. rustc missing → `skip` (scripts/check_facts.py:92) → exit 0 → output discarded (scripts/pre-commit:17) → test green (scripts/test_check.py:578). Exported empty CHECK_PRIVATE_TERMS → the file is ignored (scripts/check.py:248) → "no terms" → warning → commit.
- Subtlety flags: scripts/check.py:400 (a default argument), scripts/check.py:90 (`?` against `*`), scripts/check.py:223 (`[:1]`).

## CROSS-DOMAIN SUMMARY

- Domains: Code, Tests, Documentation. Each claim is counted once, in its primary domain: code-versus-docstring drift counts in Code.
- Claims: 57 PASS shown (Code 19, Tests 13, Documentation 25, with P-D12 disputed). FAIL: 47 (Code 27, Tests 14, Documentation 6). Falsified: 0.
- Survived: 4 of 5 re-verified claims kept their verdict; the changed one is K12.
- Failure categories: 12 systemic patterns. The main ones are doc-code drift, silent fallthrough, missing completeness, assumed environment, working tree leaking into the staged check, tautological tests, test-environment artifacts and missing negative tests.
- Invariants: 7 stated in scripts/check.py:6-44, all touched. These are enforced by their checks, apart from the gaps above. Check 3 has 7 open findings (K2, K4, K6, K13-K15, K27).
- Hypotheses: 19 requiring investigation (Code 8, Tests 7, Documentation 4).
- Hidden behaviors: 10 (Code 7, Tests 1, Documentation 2).
- Findings by type: 23 demonstrated defects, 24 preventive measures, 0 falsified hypotheses.
- Critical issues: 0 of critical severity. High: K1, K2, K3, K4 (demonstrated) and K6, T14 (preventive).
- Pre-code: not applicable.
- Executed: nothing (reasoning only).
- Proposed: 6 checks and 0 writes awaiting an answer.
- Recommendation: do not trust the pre-commit hook as a private-name gate until K1, K2 and K4 are fixed. Do not trust a green check_facts.py until K3 and T2 are fixed. The suite probably has 3 red tests now (H-T1 to H-T3).

## PROPOSED EXECUTABLE CHECKS

| # | Claim | Confidence now | Check (command, test or query) | Confirms if | Refutes if | Cost and side effects | Status |
|---|-------|----------------|--------------------------------|-------------|------------|-----------------------|--------|
| 1 | H-T1 to H-T3: the suite is red now (K2, K4, K5) | traced | `python3 -m unittest scripts/test_check.py` from the ./tree root | test_second_badge_mismatch, test_two_words_joined_any_way and test_whole_word_term_glued_in_output_is_still_masked fail | All green | Runs check.py in temporary copies; writes only to the temp dir; StagedTest runs `git init` in the temp dir | proposed |
| 2 | K3 and T2: a missing toolchain exits 0 | 92 | `PATH=<python only> python3 scripts/check_facts.py; echo $?` | `skip 52.rs` and exit 0 | Exit non-zero | Reads the fact files, runs the .py facts; no writes outside temp | proposed |
| 3 | T3 and K13: environment precedence | 85 | `CHECK_PRIVATE_TERMS=x python3 -m unittest scripts/test_check.py -k missing_terms` | Red | Green | As check 1 | proposed |
| 4 | H-D1: hook exec bit | n/a | `git ls-files -s scripts/pre-commit` | Mode 100755 | Mode 100644 | Read-only; needs the git repo (./tree has none) | proposed |
| 5 | H-T4: BOM in test_check.py:320 | n/a | Hex dump of line 320 | `EF BB BF` between the quotes | Empty string | Read-only | proposed |
| 6 | H-C1: Rust stripping | n/a | Call `has_assertion` on a .rs file with `'"'` and an assert only inside a string | True (false accept) | False | Writes one temp file | proposed |

Proposed writes: none. The fixes are listed per row and are not applied.

Shall I run checks 1-6 (or a subset)? Nothing runs without your answer.
