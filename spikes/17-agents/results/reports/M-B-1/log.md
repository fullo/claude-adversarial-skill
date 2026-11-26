# Coordinator log

## Agents launched

All on model sonnet, effort medium, subagent type general-purpose, in the background.

| # | Role | Files | Brief | Return | Rows returned | Rows discarded |
|---|------|-------|-------|--------|---------------|----------------|
| 1 | Domain agent: Code | scripts/check.py, scripts/check_facts.py, scripts/pre-commit, scripts/test_check.py | briefs/Code.md | returns/Code.md | 93 (decomposed 34, PASS 22, FAIL 14, hypotheses 6, hidden 12, categories 5) | 0 |
| 2 | Domain agent: Tests | same four | briefs/Tests.md | returns/Tests.md | 72 (decomposed 24, PASS 13, FAIL 15, hypotheses 4, hidden 9, categories 7) | 0 |
| 3 | Domain agent: Documentation | same four | briefs/Documentation.md | returns/Documentation.md | 102 (decomposed 39, PASS 26, FAIL 11, hypotheses 8, hidden 13, categories 5) | 1 (H8: no quoted line) |
| 4 | Send-back of the Documentation discarded row | same four plus returns/Documentation.md | briefs/Documentation-resend.md | returns/Documentation.md (edited in place) | 3 (H8a, H8b, H8c, replacing H8) | 0 |
| 5 | Independent verifier (5 highest-risk claims) | claims located in scripts/pre-commit, scripts/check.py, scripts/check_facts.py; free reading of ./tree | briefs/Verifier.md | returns/Verifier.md | 19 (verdicts 5, hypotheses 2, categories 12) | 0 |
| 6 | Category agent | same four | briefs/Category.md | returns/Category.md | 81 (category instances 72, hypotheses 9) | 0 |

- Totals: 370 rows returned on the first pass (93+72+102+19+81, plus 3 from the send-back). 1 row was discarded on the first pass, and 0 remained discarded after the send-back.
- Independent verifier: V1 to V4 confirmed (FAIL, as all domain agents found). V5 changed: the domain agents had PASS at 88 and 85, the verifier FAIL at 85, so the report carries it as K12 at 85 with both verdicts.
- Agent tokens, as reported in the completion notifications: 89,410 + 93,357 + 98,354 + 25,412 + 46,225 + 110,580 = 463,338. The largest context the coordinator reached, and wall time, are not visible to the coordinator: take them from the harness.

## Departures from the protocol

1. **Send-back went to a new agent, not to "its agent".** The harness cannot continue a finished agent, so a fresh agent (same model and effort) received the discarded row and the path of the return and corrected it in place. Its brief is saved as briefs/Documentation-resend.md.
2. **How quotes were looked up.** The coordinator read the four script files in full once (Read), then matched each returned quote against the line it names. It did not run one search per row. Quotes in files outside scripts/ were looked up with Grep (evals.json:463, facts/38.py:21, facts/40.py:13, facts/49.py:12, facts/NOT_COMPUTABLE:4, SKILL.md:20, .gitignore:1). The coordinator did not use these reads to verify claims, but it did see whole files, which goes further than "a search of the file".
3. **Partial quote accepted.** Tests PASS P3 gives no full quoted line, only the fragment `day > 31` for evals.json:463 (the agent noted the line is too long). The fragment was found at :463, so the row was kept, not discarded.
4. **Domain detection.** Documentation was added as a third domain, alongside the obvious Code and Tests, because the scripts carry docstrings, usage and help text and error messages. The coordinator decided this from a count-only Grep (print/help/.md mentions) before reading any file.
5. **The verifier's claims were phrased by the coordinator.** V5 was phrased more broadly than the domain claims: "nothing from the working tree decides the result". That wording partly explains the disagreement. The report says so in K12. The verifier brief also asked for a FAILURE CATEGORIES table, which the protocol does not ask of the verifier; these categories were fed into the category agent's list.
6. **The category agent's brief lists 12 categories** merged and renamed from the domain and verifier returns, with a column set close to the FAIL table. The protocol fixes no template for this brief beyond its ending.
7. **Report assembly.** The skill's per-domain INVARIANTS, STRESS TEST and PRE-CODE sections could not be filled from the returns, because the protocol brief excludes them; the report says so. Duplicates across domains were merged once, into a primary domain: code-versus-docstring drift goes to Code. New instances from the category agent were added as FAIL, HYPOTHESES or HIDDEN rows in their domain, not as a separate section. Some report rows quote lines the coordinator itself copied from the files while merging: T12 at scripts/test_check.py:503, the HB-C6 quotes, and H-D2. The agents named these locations; the exact quoted text comes from the coordinator's lookup read.
8. **Missing confidences.** Code PASS rows C20 and C26 came back without a confidence. They are reported without one (P-C15), and the second appears as P-D18 / K12 context. They were not given a number.
9. **Extra file.** out/scratch_lookup.md holds the coordinator's lookup notes. The protocol does not list it.
10. **No send-back** of the "run-only red test" confidence caps (the "79" notes inside some agent rows). These were kept as the agents wrote them.
