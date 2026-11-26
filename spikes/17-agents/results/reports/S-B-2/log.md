# Coordinator log

## Agents launched

All on model `sonnet`, effort `medium`, subagent type `general-purpose`. Briefs are in out/briefs/; returns are in out/returns/.

| Agent | Role | Files | Rows returned | Rows discarded | Agent tokens | Duration |
|-------|------|-------|---------------|----------------|--------------|----------|
| Code | Domain agent, Code | scripts/check.py | 75 (claims 27, categories 5, PASS 18, FAIL 9, hypotheses 6, hidden 10) | 0 | 78,345 | 187 s |
| Documentation | Domain agent, Documentation | scripts/check.py | 96 (claims 40, PASS 27, FAIL 9, hypotheses 4, hidden 12, categories 4) | 0 | 71,823 | 180 s |
| Data | Domain agent, Data | scripts/check.py | 70 (claims 20, PASS 13, FAIL 15, hypotheses 5, hidden 13, categories 4) | 0 | 78,328 | 186 s |
| UX | Domain agent, UX | scripts/check.py | 50 (claims 16, categories 5, PASS 10, FAIL 9, hypotheses 3, hidden 7) | 0 | 72,676 | 181 s |
| verifier | Independent verifier, 5 highest-risk claims | scripts/check.py (reads ./tree freely) | 10 (5 verdicts, 5 categories) | 0 | 47,920 | 79 s |
| category | Category agent, 6 categories over the whole scope | scripts/check.py | 84 | 0 | 95,011 | 319 s |

Total: 385 rows returned, 0 discarded, 444,103 agent tokens. No return was sent back, since none had a discarded row.

Independent verifier: 5 claims sent (C1 separator :90, C2 masking :400, C3 badges :223, T1 references "tracked or not" :43-44, D1 Latin-1 fallback :122). All 5 confirmed as FAIL. T1 was confirmed as PASS in working-tree mode and FAIL with --staged, which matches the domain agents. There was no disagreement, so no confidence was lowered.

The largest context the coordinator reached and the wall time are recorded by the harness (out/session.jsonl); I cannot measure them from inside.

## Departures from the protocol and judgment calls

1. **Brief text.** Every brief starts with an extra line that the PROTOCOL template does not have: `Working directory: F:\GitHub\Aura\spike17-runs\S-B-2 (all ./ paths are relative to it).` I added it so that the `./` paths resolve. The saved briefs include the line as sent. At first I saved the 4 domain briefs without it and corrected them right after launch, so the saved files match what was sent.
2. **Domain detection.** The coordinator read scripts/check.py once at intake to detect domains (Code, Data, Documentation, UX). It did not verify anything there. The protocol allows the coordinator to open a file of the case only to look up quotes. Detection is part of the intake the protocol assigns to the coordinator, but it is noted here as a reading beyond quote lookup.
3. **Quote lookup.** Quotes in scripts/check.py were compared against the copy of the file read at intake (that file was not modified during the run). Quotes in other files were looked up by search: scripts/test_check.py:171, :172, :286, :294, :341, :342, :344, :507; scripts/pre-commit:9; skills/adversarial-verify/evals/facts/35.py:1; CHANGELOG.md:5, :10; README.md:1; .claude-plugin/plugin.json:3; skills/adversarial-verify/SKILL.md:20. All were found.
4. **Borderline lookups (kept, not discarded):**
   - Category row 1.17 names `scripts/check.py:24 (docstring), 419`, but its quote "Without terms the check says so; with --strict it fails." starts on line 23 and ends on line 24. The text is there across the two lines, so the row was kept. The same finding is reported in the report as C9, which comes from the domain agents.
   - The verifier's evidence for claim 2 quotes scripts/test_check.py:342 as "whole-words". The file says "whole words". This was a quote in the evidence column, not the row's quote, so the row was kept. The report quotes test_check.py:344 instead.
   - Rows whose quote is shown with Markdown escapes (`\|`, doubled backslashes in the DELIM regex at :341, "pipes escaped for this table") were matched on the unescaped text.
5. **Sections not requested.** Following the protocol's domain brief, the agents did not return INVARIANTS, GROUND TRUTH tables or STRESS TEST RESULTS. The report says so and does not invent them.
6. **Confidence edits by the coordinator.** I lowered one PASS, Python 3.8 (Code PASS 12), from 85 to 79. The two agents disagreed on it (85 and 75), and the claim can be settled only by a run. This is a judgment under the skill's run-only cap, not under the protocol's "quote not looked up" rule. For findings reported by several agents with different confidence or severity, the report keeps one value and names the disagreement in the row (C3 severity, C5 type, C10 type, D4 severity, D8 type).
7. **Assignment to primary domains.** Findings reported by several domain agents (C1, C2, C3, C4, C9, D4 and others) are counted once, in the primary domain I assigned. The other agents that found the same finding are named in the row.
8. **Category agent scope.** The category agent was run after the independent verifier, as the protocol orders. Its categories are the union of the domain agents' and the verifier's categories, merged into 6.
