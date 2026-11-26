# Coordinator log

All agents: general-purpose, model sonnet, effort medium (as the request asked), run in background.
Briefs are in ./out/briefs/ as sent. Returns are in ./out/returns/.

## Agents launched

| # | Role | Files | Rows returned | Rows discarded |
|---|------|-------|---------------|----------------|
| 1 | Domain agent: Code | the 23 files in scope, Code domain only | 113 (41 decomposed, 29 PASS, 19 FAIL, 6 hypotheses, 12 hidden behaviors, 6 categories) | 0 |
| 2 | Domain agent: Tests | the 23 files, Tests domain only | 64 (23 decomposed, 9 PASS, 12 FAIL, 5 hypotheses, 8 hidden behaviors, 7 categories) | 0 |
| 3 | Domain agent: Data | the 23 files, Data domain only | 69 (27 decomposed, 18 PASS, 6 FAIL, 6 hypotheses, 8 hidden behaviors, 4 categories) | 1 at lookup (PASS C13: quote at _parse_day.py:10, row said :11), restored after resend |
| 4 | Domain agent: Documentation | the 23 files, Documentation domain only | 109 (51 decomposed, 22 PASS, 15 FAIL, 6 hypotheses, 10 hidden behaviors, 5 categories) | 2 at lookup (C31 and F6: quote at check_facts.py:8, rows said :10), restored after resend |
| 5 | Resend: Data | the 1 discarded row | 1 (corrected to :10, verdict holds) | 0 |
| 6 | Resend: Documentation | the 2 discarded rows | 2 (corrected to :8, verdicts hold) | 0 |
| 7 | Independent verifier | 5 claims: NOT_COMPUTABLE:13, pre-commit:9, check.py:400, check.py:90, check_facts.py:92 (claim and location only) | 5 (all FAIL, agreeing with the domain agents) | 0 |
| 8 | Category agent | the 23 files, 9 categories with the known locations | 24 (19 FAIL, 5 hypotheses) | 0 |

Totals: 387 rows returned, 3 discarded at lookup, 3 restored, 0 dropped. Verifier: 5 confirmed, 0 changed.
Token usage per agent, as the harness reported it: Code 121,844; Tests 112,628; Data 105,502; Documentation 125,112; Data resend 20,443; Documentation resend 15,348; verifier 44,700; category 133,394. Total 678,971. The coordinator's largest context and the wall time are not visible to me; they are in the harness record.

## Departures from the protocol

1. **Resend to "its agent".** Finished agents cannot be continued in this harness, so the "send back once to its agent" step went to a fresh agent of the same role and model. Its brief held the discarded rows and the path of the original return, not the original agent's context (briefs/Data-resend.md, briefs/Documentation-resend.md).
2. **Domain detection and file sizes.** I sized the domains by line count (a Grep count), not bytes. No domain looked near 60 kB except possibly Data through evals.json (725 lines). That is a single file, which the protocol does not allow to be cut, so each domain got one agent.
3. **Domains not detected.** UX was not assigned, although check.py prints terminal output: it is a check script's report, not an interface under review. Architecture and Analysis had no artifacts.
4. **Quote lookup method.** I looked quotes up with targeted searches (Grep with line numbers) on a distinctive substring of each quote. For multi-line and range rows, I accepted the quote when it was within the named range. For evals.json, whose lines are long, I matched a substring of the quote at the named line. For the small fact files, one search listed every line, so I compared the quotes against that listing.
5. **Sections not returned.** The brief template asks for six sections only, so INVARIANTS and STRESS TEST RESULTS are marked "not returned" in the report instead of filled. ADVERSARIAL SCAFFOLD FINDINGS was written once, under Code, from the returned rows.
6. **Merging and primary domain.** Many findings were reported by several agents. In the report each is counted once in a primary domain I chose (for example, pre-commit:9 under Code, NOT_COMPUTABLE:13 under Data), and the other reports are named in its Scenario. Severity disagreements (Data rated NOT_COMPUTABLE:13 Medium, the other three High) were resolved to High, as the majority and the verifier's scenario support.
7. **Category agent brief.** For each category it listed the locations already found, so the agent would not report them again. It holds locations only, not reasoning or verdicts. Two of its FAIL rows (check.py:10, README.md:250) still restated known findings and were merged into C6.
8. **Category agent ran on categories from step 1 only.** The verifier changed nothing, so step 2 added no categories.
9. **The report ends with a question.** That follows the skill's Output Format. No check was run and no file in ./tree was written. The question is in the report; I did not stop the run to ask it.
