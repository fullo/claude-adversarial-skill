# Coordinator log

All agents: subagent_type general-purpose, model sonnet, effort medium, run in the background.
Briefs are in out/briefs/. Returns are in out/returns/.

## Agents launched

| # | Role | Files | Rows returned | Rows discarded | Notes |
|---|------|-------|---------------|----------------|-------|
| 1 | Domain agent: Code | the 23 files of the request (brief: out/briefs/Code.md) | 114 (43 claims, 29 PASS, 15 FAIL, 8 hypotheses, 13 hidden behaviors, 6 categories) | 6 | Discarded because the quote was not at the named line: claim 8 (check.py:24, actually :23), claim 12 (check.py:41, actually :40), FAIL F3 and HB1 (check_facts.py:91, actually :92), HB6 (check.py:365, actually :363), and the "Silent fallthrough" category row (check_facts.py:91). |
| 2 | Domain agent: Tests | same 23 files (out/briefs/Tests.md) | 79 (29 / 12 / 16 / 7 / 10 / 5) | 0 | |
| 3 | Domain agent: Documentation | same 23 files (out/briefs/Documentation.md) | 121 (55 / 27 / 16 / 8 / 10 / 5) | 0 | Its PASS P7 (masking, README.md:251) was overturned by the independent verifier. |
| 4 | Domain agent: Data | same 23 files (out/briefs/Data.md) | 90 (35 / 20 / 12 / 9 / 9 / 5) | 0 | |
| 5 | Correction pass on the Code return | out/returns/Code.md and ./tree (out/briefs/Code-resend.md) | 114 (whole return rewritten as out/returns/Code-resend.md) | 0 | All 6 discarded rows were corrected and look up correctly. None was dropped. |
| 6 | Independent verifier | the 5 highest-risk claims, by location only (out/briefs/IndependentVerifier.md) | 10 (5 FAIL, 1 falsified hypothesis, 4 hypotheses) | 0 | Confirmed FAIL on all 5: NOT_COMPUTABLE:13, pre-commit:9, check_facts.py:91-93, check.py:400, check.py:90. Changed 1 row: the Documentation PASS on masking. |
| 7 | Category agent | the 8 failure categories × the 23 files (out/briefs/CategoryAgent.md) | 53 (45 instances, 8 hypotheses) | 0 | |

Totals: 467 rows came back across the domain agents, the verifier and the category agent, not counting the 114 rows of the corrected Code re-return. 6 were discarded and all 6 were recovered on resend.

## Departures from the protocol

1. **Resend to "its agent".** The Agent tool cannot continue a finished agent, so the discarded Code rows went to a new sonnet agent. It received the list of rows and the original return file, not the original agent's context. It wrote its result to out/returns/Code-resend.md instead of overwriting Code.md, so the original return is kept.
2. **Domain split by size.** File sizes were estimated from line counts (Grep), not measured in bytes. evals.json (725 lines) may be over 60 kB on its own. The Data domain was not split, because evals.json cannot be split and the only other Data file, plugin.json, is 20 lines. One agent per domain was used.
3. **Domain detection.** Four domains were detected: Code, Tests, Documentation, Data. No Architecture, Analysis or UX agent was launched. The CLI output of check.py was judged too thin to count as a UX target; this was not asked of the user because the request said not to stop.
4. **Brief path note.** Each brief sent to an agent ended with one extra line giving the absolute working directory, so that ./skill, ./tree and ./out would resolve. The saved briefs in out/briefs/ omit this line. Apart from that line, the domain briefs are the protocol's template with {DOMAIN} filled in.
5. **Rows without a quoted line.** Some Code PASS rows (27, 33, 34, 35, 39) give evidence without a quoted line. They were not discarded. Under the protocol's rule for an unchecked quote, they are capped at 79 in the report. Their claims also appear as quoted, looked-up PASS rows from the Data agent (D-P6, D-P12, D-P13, D-P14, D-P3).
6. **Quote lookup method.** Quotes were looked up with Grep in the named file and the line number compared. For lines too long for Grep to show, a match at the named line on a distinctive substring was accepted. Rows that cite a line range were accepted if the quote fell inside the range.
7. **Category agent timing.** It was launched before the corrected Code return arrived. This was safe because that pass changed only line numbers, not categories.
8. **Report consolidation.** The report does not copy the returns. Findings reported by several agents were merged into one row in their primary domain, with a "Found by" column. Full decomposed-claim lists are referenced, not repeated. Stress tests were not part of the domain brief (protocol template), so only the verifier's appear.
9. **Not recorded by the coordinator:** total tokens of all agents, the coordinator's largest context, and wall time come from the harness. Per-agent token counts reported by the harness: Code 131,139; Tests 135,838; Documentation 130,509; Data 122,039; Code resend 40,997; Verifier 49,751; Category 141,930. Total 752,203.
