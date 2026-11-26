# Coordinator log

## Agents launched
Every agent ran on Sonnet at medium effort, as the request asked, with subagent type general-purpose. Rows are table rows of the return file. Discarded means the quote was not found at the line the row names.

| # | Role | Files | Rows returned | Rows discarded | Tokens | Duration |
|---|------|-------|---------------|----------------|--------|----------|
| 1 | Domain agent: Code | the 23 files in scope (brief: ./out/briefs/Code.md) | 104 (37 claims, 5 categories, 18 PASS, 20 FAIL, 10 hypotheses, 14 hidden behaviors) | 0 | 146,733 | 365 s |
| 2 | Domain agent: Tests | the 23 files (./out/briefs/Tests.md) | 81 (24, 6, 16, 15, 8, 12) | 0 | 130,586 | 255 s |
| 3 | Domain agent: Data | the 23 files (./out/briefs/Data.md) | 81 (30, 6, 14, 14, 7, 10) | 0 | 126,919 | 225 s |
| 4 | Domain agent: Documentation | the 23 files (./out/briefs/Documentation.md) | 146 (67, 8, 38, 16, 7, 10) | 0 | 147,248 | 286 s |
| 5 | Independent verifier | 5 claims with locations: scripts/test_check.py:1 + NOT_COMPUTABLE; scripts/check_facts.py:8; scripts/pre-commit:5, :9; scripts/check.py:22-23, :399-401; scripts/check.py:15-17, :90 (./out/briefs/IndependentVerifier.md) | 5 (5 FAIL: all 5 domain verdicts confirmed, none changed; lower severity than a domain agent on claims 2, 4 and 5) | 0 | 64,357 | 50 s |
| 6 | Category agent | the 23 files, 9 categories (./out/briefs/CategoryAgent.md) | 42 (33 FAIL, 9 categories). 8 of the FAIL rows duplicated findings already returned (check.py:500, :90 two-space, check_facts.py:50, _parse_day.py:5, check.py:301, check_facts.py:100, pre-commit:5, README.md:261 and :247 merge with existing rows); they were merged, not discarded | 0 | 154,977 | 332 s |

Totals:
- 459 rows returned, 0 discarded. No return was sent back, since none had a discarded row.
- All agents together used 770,820 tokens.
- Wall time: the four domain agents ran in parallel (longest 365 s), then the verifier (50 s), then the category agent (332 s), so roughly 12-13 minutes of agent time end to end. Harness wall-clock for the whole session is not available to me.
- The largest context the coordinator reached is not exposed to me by the harness, so it is not recorded. I estimate roughly 110-130k tokens, mostly from the protocol, SKILL.md, the six returns and the lookup results.

## Departures from the protocol (and points where I applied judgement)
1. **Sizing the domains.** To decide whether any domain exceeded 60 kB, I ran a line-count search (Grep count of `^`) over ./tree. That goes beyond "opens a file only to look up a returned quote". It returns counts, not content. I did not measure byte sizes. No domain was split: the largest single file, evals.json, is 725 lines, and splitting one file would be an arbitrary cut.
2. **Domains detected:** Code, Tests, Data, Documentation. No Architecture, Analysis or UX artifact was in scope. The facts/*.py, .rs and .ts files were left to the agents to assign; each agent took them in its own domain.
3. **Brief wording.** Each brief, including the domain briefs, carried one line the protocol template lacks: "(All relative paths are relative to F:\GitHub\Aura\spike17-runs\L-B-2.)". The saved briefs were edited afterwards to include that line, so they match what was sent.
4. **Briefs of the verifier and the category agent.** The protocol gives no template for these. I wrote my own, ending as the protocol requires. The category brief listed the known instances of each category, so that the agent searched for *other* instances. This tells it what was already found, which goes slightly beyond "takes the failure categories".
5. **How the 5 highest-risk claims were chosen:** by blast radius × probability, among the FAIL rows (no PASS row ranked in the top 5). The verifier's brief stated each claim as the project's own advertised claim, not as the domain agents' verdict.
6. **Quote lookups** were done with searches (Grep), not by opening files. They covered every FAIL, PASS, HYPOTHESIS and HIDDEN BEHAVIOR row of all six returns. For long JSON lines and for quotes that wrap across a stated line range, a distinctive fragment was matched. DECOMPOSED CLAIMS quotes that no result row reuses were not all looked up; they carry no score, so no PASS was capped at 79 for that reason. Quotes that differ from the file only in backticks or an elided "…" were accepted.
7. **Disagreements.**
   - The verifier and the domain agents agreed on every verdict. Where only severity differed, the report shows both severities and keeps the confidence.
   - Where two domain agents gave different types for the same finding, the report keeps the lower confidence and states both: C15 (check.py:500), T2 (test_check.py:575-578) and T13 (facts/35.py:2).
8. **Merging.** Findings reported by several agents were merged and counted once, in their primary domain (e.g. NOT_COMPUTABLE:13 under Data, the badge, SEP and masking findings under Code). Merging also condensed the PASS tables of the report. The full rows stay in ./out/returns/.
9. **Sections the brief does not return.** The protocol's domain brief returns only six sections. INVARIANTS (as a table), STRESS TEST RESULTS and ADVERSARIAL SCAFFOLD FINDINGS therefore have no agent data, and the report says so instead of filling them in.
10. **Coordinator reading.** I read ./PROTOCOL.md and ./skill/SKILL.md to follow the protocol and the Output Format. To check the severity of Doc8 and Doc7 against the skill text, I searched ./tree/skills/adversarial-verify/SKILL.md for "version", "(code, data, tests, UX)" and "issue". That is a lookup of quotes cited by the returns.
11. **The 60 kB rule and grouping.** Each domain agent received all 23 files, as the protocol template has it, with "for the {DOMAIN} domain only". I did not pre-assign files to domains.
