# Coordinator log

## Agents launched
All on model sonnet, effort medium, subagent type general-purpose. Briefs are in `out/briefs/`; returns are in `out/returns/`.

| Agent | Role | Files | Rows returned | Rows discarded |
|-------|------|-------|---------------|----------------|
| Code | Domain agent (Code) | scripts/check.py, scripts/check_facts.py, scripts/pre-commit, scripts/test_check.py | 92 (31 claims, 19 PASS, 16 FAIL, 7 hypotheses, 11 hidden behaviors, 8 categories) | 0 |
| Tests | Domain agent (Tests) | same four files | 93 (36 claims, 17 PASS, 18 FAIL, 6 hypotheses, 9 hidden behaviors, 7 categories) | 0 |
| Documentation | Domain agent (Documentation) | same four files | 109 (43 claims, 30 PASS, 9 FAIL, 9 hypotheses, 13 hidden behaviors, 5 categories) | 0 |
| Verifier | Independent verifier, 5 highest-risk claims (masking of `=` terms, toolchain skip, hook --strict, separator, --staged) | same four files (read freely) | 5 (4 confirmed FAIL, 1 changed PASS → FAIL preventive at 65) | 0 |
| Category | Category agent, 9 categories, whole scope | same four files | 27 (22 new, 5 duplicates of known rows merged: Category 4, 8, 12, 18, 19) | 0 |

Total: 326 rows, 0 discarded. No return was sent back, since none had a discarded row.

## Quote lookup
Every quote that names a line in the four files was checked against that line (the coordinator read the four files once to do the lookup). Every quote that names a line in another file of ./tree was checked by search (CHANGELOG.md:5 and :10, .claude-plugin/plugin.json:2-4, .gitignore:1, README.md:1, evals.json:269 and :462, facts/38.py:20-21, facts/40.py:13, facts/49.py:12-14, NOT_COMPUTABLE:4, SKILL.md:207). Some quotes were abbreviated with "..." (Tests categories: scripts/check_facts.py:34, scripts/test_check.py:351, scripts/test_check.py:503); the part that was quoted matched, so they were accepted. Tests PASS C34 cites `tree/.gitignore:1`, so the path was normalized to `.gitignore:1`. No PASS above 80 had an unchecked quote, so none was lowered to 79.

## Departures from the protocol
1. **Domain detection.** The protocol lists the domains but leaves detection to the skill. I detected Code, Tests and Documentation. Documentation was included because the files carry help text, usage lines and error messages (SKILL.md Step 0). Data, UX, Architecture and Analysis were not detected.
2. **Domain agents were not split by file.** All three got all four files, using the protocol's brief template verbatim. Each one filters by domain. The total size (about 1,300 lines) is under 60 kB, so no group split was needed.
3. **Working-directory line.** Each brief sent to an agent had one extra line, "(Working directory: F:\GitHub\Aura\spike17-runs\M-B-3 — all ./ paths are relative to it.)", appended after the protocol text so that the relative paths resolve. The copies saved in `out/briefs/` do not include it.
4. **Verifier and category briefs.** The protocol gives no template for these, so I wrote my own. The verifier got only the claim text and its locations, with no verdict or reasoning. The category brief listed the known instances of each category, so that the agent would report only new ones. That tells it what was already found, but not what to expect.
5. **Ordering.** The protocol does not say whether to look up a return before or after the next one arrives. The returns were looked up as they arrived. The verifier and then the category agent were run in the foreground, one after the other, after all three domain returns were checked.
6. **Report structure.** The returns hold only the six sections the protocol asks for. So the report omits INVARIANTS, STRESS TEST RESULTS and ADVERSARIAL SCAFFOLD FINDINGS, and says so. It does not reproduce the full DECOMPOSED CLAIMS tables (110 rows); it points to the returns instead. The Documentation PASS rows are summarized by location instead of re-tabulated. This avoids copying long returns, per the protocol's warning.
7. **Consolidation.** Findings reported by several agents were merged into one row in their primary domain, with the sources named. Where agents disagreed on the type (T3, T4: demonstrated vs preventive), I kept preventive measure and recorded both. This is a coordinator judgment, not a verification.
8. **Disagreement with the verifier (C6).** Three domain agents gave PASS (82-85). The verifier gave FAIL, preventive measure, at 65. Per protocol step 2, the row is in the report with the lower confidence (65) and both verdicts. The part the verifier falsified ("the working tree is read") is a conditionally falsified hypothesis.
9. **Harness metrics.** Total tokens of the agents, as reported in their notifications: Code 88,200; Tests 95,741; Documentation 102,863; Verifier 48,716; Category 95,831; total ≈ 431,351. The coordinator's largest context and the wall time are not visible to me; take them from the harness session log (`out/session.jsonl`).
