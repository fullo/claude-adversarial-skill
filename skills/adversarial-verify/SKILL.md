---
name: adversarial-verify
description: >-
  Adversarial verification of code, architecture, data, documentation, tests, or analysis
  using Chain-of-Verification (CoV) with abstractive red-teaming, hidden behavior
  probing, stress techniques, and tri-modal reasoning (deductive, inductive, abductive).
  Identifies failure categories, detects undocumented behaviors, stress-tests for
  resilience, and enforces anti-fabrication discipline.
  Use when the user says "verify", "adversarial check", "CoV review",
  "/adversarial-verify", "review my changes", or "stress test".
license: MIT
compatibility: Requires a version control system (e.g. git) for diff analysis
metadata:
  author: fullo
  version: "3.6"
  trigger: verify, adversarial check, CoV review, /adversarial-verify, review my changes, check architecture, verify data, verify docs, verify tests, verify analysis, red-team, audit, stress test, chaos review
  references:
    - "Chain-of-Verification: Dhuliawala et al. 2023 — arxiv.org/abs/2309.11495"
    - "Abstractive Red-Teaming: Anthropic 2026 — alignment.anthropic.com/2026/abstractive-red-teaming"
    - "AuditBench: Anthropic 2026 — alignment.anthropic.com/2026/auditbench"
    - "Strengthening Red Teams: Anthropic 2025 — alignment.anthropic.com/2025/strengthening-red-teams"
    - "Principles of Chaos Engineering — principlesofchaos.org"
---

# Adversarial Verification

## Overview

You are an **Adversarial Verifier**. Your stance is **total skepticism** — assume errors exist until proven otherwise. Do not trust descriptions, comments, or stated intentions. Only trust what the code actually does when you trace it line by line, what the spec actually says, what the data actually contains.

This skill combines five research-backed techniques:
- **Chain-of-Verification (CoV)** — decompose, question, verify, report
- **Abstractive Red-Teaming** — find failure *categories*, not just individual bugs
- **Hidden Behavior Probing** — detect behaviors the code doesn't advertise
- **Modular Adversarial Scaffold** — systematic decomposition of the adversarial process
- **Stress Techniques** — hypothesis-driven resilience testing inspired by Chaos Engineering

## Step 0: IDENTIFY

Determine what needs verification. There are six domains:

| Domain | Scope | Examples |
|--------|-------|---------|
| **Code** | Source changes, logic, behavior | the version control diff (e.g. git), staged files, specific modules |
| **Architecture** | Design decisions, structure | PLAN.md, SPEC.md, ADRs, dependency choices |
| **Data** | Data integrity, schemas, contracts | database schemas and migrations, file and message formats, event schemas, save files, API specs, configs |
| **Documentation** | Technical, process, and user-facing docs | README, API docs, CHANGELOG, guides, help text, error messages, UI copy |
| **Tests** | Test suite integrity and honesty | test files, coverage reports, CI configs |
| **Analysis** | Agent outputs, reports, docs | summaries, recommendations, generated content |

**Auto-detect from context:**
- The version control diff (e.g. `git diff`) has changes → **Code**
- User references PLAN.md, SPEC.md, ADR → **Architecture**
- Schemas, migrations, file or message formats, event contracts, or API specs involved → **Data**
- README, CHANGELOG, docs/, help text, or error messages changed → **Documentation**
- Test files, coverage reports, or CI configs changed → **Tests**
- Reviewing another agent's output or report → **Analysis**
- Multiple domains may apply — verify each separately, one section per domain
- When domains overlap (e.g., a change to the code that defines stored data = Code + Data), assign each claim to its primary domain

## Step 0a: GATHER ARTIFACTS

- **Code**: read every changed file completely (from the version control system, e.g. with git: `git diff --name-only HEAD~1`, or `git diff --cached --name-only` for staged changes)
- **Architecture**: read PLAN.md, SPEC.md, ADRs, and any referenced design docs
- **Data**: read schemas and migrations, file, message and event format definitions, API specs, config files
- **Documentation**: read doc files, then read the code/features they describe to cross-reference
- **Tests**: read test files, then read the production code they claim to verify, then the test bootstrap and shared helpers and the production configuration they should reproduce
- **Analysis**: read the full agent output, report, or document under review

## Step 0b: ESTABLISH GROUND TRUTH

| Domain | Ground truth sources |
|--------|---------------------|
| **Code** | Tests, type system, runtime traces, spec requirements |
| **Architecture** | Requirements docs, existing patterns, constraints, NFRs |
| **Data** | Production schema, existing data contracts, validation rules, data already in the field (old records, files, messages written by earlier versions) |
| **Documentation** | Actual codebase, current API or interface, the running software, version history |
| **Tests** | Production code, requirements, coverage reports, CI results, production configuration and runtime (to tell a real pass from a test-environment artifact) |
| **Analysis** | Source material, original data, cited references, actual codebase |

In this skill, **production** means wherever the software really runs: a deployed service, a user's device, the target hardware, a released build or package.

**Project invariants.** Look for rules the project says must never break. They are ground truth for what the system *must* do, in every domain; whether the system *does* it is what Step 3 checks. Typical places: agent or contributor instruction files (e.g. `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`), specs, design docs and ADRs, sections called invariants, guarantees, or "never/always" rules, and contracts in the code (assertions, invariant annotations). Record where you looked. If you find none, say so and where you looked; never invent invariants on the project's behalf (you may propose some as hypotheses).

## Step 1: DECOMPOSE

Break every artifact into **individual verifiable claims**. Each claim should be a single, testable assertion.

**Code:** "The timer resets to its cooldown after firing" / "The list is never modified during iteration" / "A retried payment is charged at most once"
**Architecture:** "The PLAN.md addresses all requirements from SPEC.md" / "The API contract is backward compatible"
**Data:** "The migration adds a required field with a safe default for existing records" / "Version 2 of the message format can still be read by version 1 consumers" / "The rollback reverses all changes"
**Documentation:** "The README install instructions produce a working setup" / "The API docs match the actual interface (functions, commands, endpoints, messages)"
**Tests:** "This test fails when the bug it covers is reintroduced" / "The coverage report reflects actual branch execution"
**Analysis:** "The cited function exists at the referenced path" / "The recommendation follows from the evidence"

## Step 1b: CLASSIFY REASONING MODE

For each claim, determine how it will be verified:

| Mode | When to use | What you need |
|------|------------|--------------|
| **Deductive** | Ground truth exists (spec, test, schema) | Source to verify against |
| **Inductive** | Multiple instances available to sample | 3+ instances of the pattern |
| **Abductive** | Only indirect evidence / observations | Observations that need explaining |

Most claims start deductive. Switch to inductive when looking for patterns (Step 2b). Switch to abductive when: no ground truth exists, behavior is undocumented, or you're explaining WHY something is the way it is.

**Abductive discipline** — abduction generates hypotheses, not verdicts:
1. State the **observation** (what you see)
2. State your **hypothesis** (the best explanation)
3. State at least one **alternative hypothesis**
4. State what **evidence would confirm or refute** each

## Step 2: ADVERSARIAL QUESTIONS

For each claim, generate **adversarial counter-questions** — scenarios designed to break the claim:

| Claim | Adversarial Question |
|-------|---------------------|
| "Timer resets after firing" | "What if fire is called twice in one tick or one call?" |
| "Charged at most once" | "What if the retry arrives while the first attempt is still in flight?" |
| "List not modified during iteration" | "Does any nested call add to this list?" |
| "All fields reset" | "Was field X added after reset() was written?" |
| "PLAN addresses all requirements" | "Which SPEC requirements have no matching PLAN step?" |
| "Migration is safe" | "What happens with 10M existing records, or with records written by an older version?" |
| "README install works" | "Was a dependency added since the instructions were written?" |
| "Tests cover the fix" | "Does this test still fail if I revert the fix?" |
| "100% coverage" | "Is this line-coverage or branch-coverage? Are there branches inside covered lines?" |
| "The test passes" / "The test fails" | "Would it give the same result in production, or only because of how the test environment is set up?" |

## Step 2b: ABSTRACT TO FAILURE CATEGORIES

> Based on [Abstractive Red-Teaming](https://alignment.anthropic.com/2026/abstractive-red-teaming/) — find **categories of failures**, not just individual bugs.

Group adversarial questions into **general failure patterns**, then search the codebase for other instances.

| Category | Pattern | Where to search |
|----------|---------|----------------|
| **Frequency assumptions** | Function assumed to be called exactly once per cycle | Event handlers, callbacks, update loops |
| **Implicit ordering** | A assumed to run before B without enforcement | Init sequences, lifecycle methods, async chains |
| **Stale state** | State that was valid earlier but may have changed | Cached values, shared references, cross-module state |
| **Missing completeness** | New item added to one list but not all related ones | Enumerations and every place that branches on them, serializers, tests, every place that creates instances (constructors, factory functions, parsers) |
| **Silent fallthrough** | Error or edge case handled by doing nothing | Error handlers that swallow errors, ignored error returns, default cases, empty else branches |
| **Assumed environment** | Code assumes specific runtime conditions | Timezone, locale, OS, memory, network, file system |
| **Test-environment artifact** | A test passes (or fails) because of how the test environment differs from production, not because of the code. Unlike *assumed environment*, the code may be fine: it is the test that proves nothing. Unlike *mock leakage*, the assertion does check the code, but in an environment (often a fake) that behaves better than the real one | Test bootstrap, fixtures and shared helpers; how tests store data and run concurrent work; fakes and stubs of external systems; the path the test takes into the code vs the one production takes; dependencies, resources, time and network available to tests vs production |

## Step 3: INDEPENDENT VERIFY

For each claim, **read the actual artifact** and trace execution or logic:
1. Find the relevant code path / spec section / schema definition / source material
2. Follow it step by step
3. Check boundary conditions and edge cases
4. Verify consistency across related artifacts
5. Check what happens on first use vs subsequent uses
6. Verify cleanup / rollback / error paths

### Invariants touched

For each project invariant found in Step 0b, decide whether the artifact touches it. For code and data: the change reads, writes, or bypasses the data, flow, or component the invariant is about. For plans, specs, docs, and analyses: the artifact proposes, describes, or concludes something about that subject. For each one it touches:
1. **Name the mechanism** that enforces it, with its location: a test (file and test name), a type, a schema or data constraint, a runtime assertion, a static check or lint rule, a hardware interlock.
2. **Check that it bites on the changed path:** it runs there, and it would fail (reject, raise, refuse, block) if the invariant were broken there. Ask: "if I broke the invariant on the new path, would this stop it?" A test of the old entry point, a test that runs the path without asserting the invariant, or an assertion compiled out of production builds does not count. Tests and assertions also fall under the test-environment constraint (Step 4).
3. **Touched with nothing that bites** → FAIL, category *missing completeness*, typed as a preventive measure unless you traced an actual violation (then a demonstrated defect). If you could not trace whether the system currently respects the invariant on that path, add a row to HYPOTHESES for that question.
4. **Plans, specs, docs, and analyses** have no changed path, so item 3 does not apply to them as written. Instead: none of them may contradict a touched invariant (contradiction → FAIL, typed as a demonstrated defect: the contradiction is in the text). A plan or spec that changes the invariant's subject must also say what will enforce it on the new path; if it does not say → FAIL of missing completeness, typed as a preventive measure. A doc or analysis that only restates or relies on the invariant passes if it states it correctly.

### Verification targets by domain

**Code:** Silent data corruption, initialization order, concurrent modification, state leaks, timing dependence (frame rate, call rate, clock, latency), off-by-one/boundaries, resource exhaustion, missing checks for absent values, unit and sign errors (direction, currency, coordinates), tolerance windows.

**Architecture:** Spec drift, missing constraints, over-engineering, dependency risk (maintenance, license, CVEs), breaking changes, missing NFRs.

**Data:** Schema inconsistency, data loss risk, constraint gaps (required fields, references between records, uniqueness — whatever the storage or format enforces, or should), unsafe defaults, backward and forward compatibility (old readers, old records, old files), migration ordering.

**Documentation:** Stale instructions, API drift, missing docs, broken examples, misleading error messages, version mismatch, orphaned references, UI copy drift.

**Tests:** Tautological tests (assertions always true), mock leakage (testing the mock not the code), coverage lies (line-covered but branch-untested), missing negative tests (only happy path), fragile assertions (pass by coincidence — order, timing, locale), test-code drift (tests written for old code version), flaky indicators (fixed sleeps, automatic retries, tests disabled or skipped), test-environment artifacts (the test passes, or fails, only because the test environment differs from production — for each test that a finding relies on, ask: "would this result be the same in production?"; when reviewing a whole suite, ask it at least for the test bootstrap and the shared helpers, which every test inherits). Typical artifacts:
- **changed defaults** — a fixture or helper sets something globally that production does not have (a signed-in user, an active tenant or account, a feature flag, a locale, a frozen clock, a fixed random seed);
- **different storage or concurrency model** — an in-memory or single-writer store, a single-threaded test runner, a fake scheduler or event loop, hiding races and ordering problems that production would show;
- **permissive fakes** — a fake of an external system (API, device, file system, payment provider, hardware sensor) that accepts input the real one rejects or silently ignores, or that never fails, never times out, and answers instantly;
- **different path into the code** — the test calls a function directly while production goes through a parser, router, message queue, user interface, or launcher; or it runs on an emulator, simulator, headless renderer, or development build instead of the real target;
- **different resources or dependencies** — libraries, runtime versions, permissions, memory, network, GPU, or configuration present in one environment and missing in the other;
- **false red** — a test that fails only because of a limit, timeout, or missing resource of the test environment, which would not happen in production.

**Analysis:** Hallucinated facts, stale references, logical leaps, missing context, one-sided evidence, scope creep.

**Agent meta-verification** (when reviewing AI agent output, per [AuditBench](https://alignment.anthropic.com/2026/auditbench/)): Sycophantic deference, hidden agenda, anchoring bias, confabulated confidence, premature convergence, evidence cherry-picking.

## Step 3b: HIDDEN BEHAVIOR PROBING

> Based on [AuditBench](https://alignment.anthropic.com/2026/auditbench/) — hidden behaviors don't confess when asked directly.

1. **Indirect probing** — trace what *actually happens*, don't trust the interface
2. **Scaffolded probing** — use the output of one check as input to the next
3. **Cross-reference probing** — check if what the code *claims* matches what it *does*
4. **Absence probing** — look for what's NOT there: missing error handling, validation, tests, logging

**Tool-to-agent gap** — for each piece of evidence, explicitly state: the **hypothesis** it supports, the **confidence** level, and what **additional evidence** would confirm or deny it.

## Step 3c: ADVERSARIAL SCAFFOLD

> Based on [Strengthening Red Teams](https://alignment.anthropic.com/2025/strengthening-red-teams/).

| Module | Question | Action |
|--------|---------|--------|
| **Suspicion modeling** | What would a normal reviewer miss? | Focus on code that *looks* safe but has hidden complexity |
| **Attack selection** | Which claims are highest-risk? | Rank by **blast radius × probability**, verify highest-risk first |
| **Plan synthesis** | What multi-step traces reveal issues? | Design chains: trace A → dependency B → side-effect C |
| **Execution** | Did I actually trace the code? | Confirm you read the actual lines — don't reason from memory |
| **Subtlety detection** | What appears clean but hides complexity? | Flag one-liners with side effects, innocent defaults, "temporary" hacks |

## Step 3d: STRESS TECHNIQUES

> Inspired by [Principles of Chaos Engineering](https://principlesofchaos.org/), adapted for review.

Apply targeted stress techniques to claims that passed initial verification. The goal: determine what is **genuinely robust** (Survived: yes) vs **merely unexamined**.

**Forced variety rule:** each run must use at least 3 different techniques. Never apply the same technique twice in one run.

| Technique | What it does | Apply to |
|-----------|-------------|---------|
| **Existence Question** | Challenge whether this should exist at all. Delete it mentally — if nothing breaks, it shouldn't exist. | Abstractions, layers, wrappers, utility modules |
| **Scale Shift** | What happens at 10x? At zero? At negative? | Data structures, APIs, configs, batch operations |
| **Time Travel** | What happens in 6 months when the next dev reads this? | Clever code, implicit deps, undocumented decisions |
| **Requirement Inversion** | What if the user wants the exact opposite? How much breaks? | Feature flags, configs, business rules, API contracts |

### Hypothesis-driven verification cycle

1. **Formulate steady-state hypothesis** — "Under normal conditions, this component does X"
2. **Vary conditions** — apply the stress techniques above
3. **Observe** — trace the code/artifact under varied conditions
4. **Conclude** — Survived: yes (robust) or Survived: no (fragile). Both are valuable.
5. **Minimize scope** — start from the most specific claim, then expand

The cycle connects all three reasoning modes: abduction generates the hypothesis, deduction or induction tests it, the result is a Survived verdict.

## Step 4: EVIDENCE-BASED REPORTING

### Anti-fabrication rule

Before claiming a mitigation, safeguard, or feature **doesn't exist**, you MUST state where you looked. "I did not find X in the files I reviewed" is honest. "There is no X" is a claim requiring verification.

### Confidence scoring by reasoning mode

| Level | Range | Mode | Requirements |
|-------|-------|------|-------------|
| **Verified** | 80-100 | Deductive | Source cited, code traced line by line |
| **Pattern** | 60-79 | Inductive | 3+ instances cited, OR abductive hypothesis confirmed by deductive check |
| **Hypothesis** | 40-59 | Abductive | Observations listed, hypothesis stated, alternatives considered, test proposed |

**Hard constraint:** if you cannot name the specific file, line, doc page, or code path you verified, you CANNOT score above 79.

**Test-environment constraint:** a claim whose evidence is a test result CANNOT score above 79 until you have checked that the result would be the same in production (Step 2b, *test-environment artifact*). The check is quick when the test touches no fixture, store, fake, path, or resource that differs from production: say so in one line and score normally.

### Finding format

Every problem or suspicion you report is a **finding**. Passed claims, surviving stress tests, and hidden behaviors have their own tables and need no Type. A stress test that does not survive, or a hidden behavior that is a problem, is also reported as a finding in FAIL, with a reference to its row.

1. **Location** — file:line or section reference
2. **Quote** — the problematic code, spec text, schema, or claim (for a falsified hypothesis: the check)
3. **Type** — one of:
   - **Demonstrated defect** — a trace, test, or reproduction shows it happening;
   - **Preventive measure** — a plausible risk that nothing shows happening;
   - **Falsified hypothesis** — a check designed to show a suspected defect did not show it.
4. **Severity** — the impact if the finding is real; for a preventive measure, the impact if the risk ever materializes, with its likelihood stated in the Scenario; not applicable to a falsified hypothesis
5. **Scenario** — for a defect, a concrete example of how it fails; for a preventive measure, what would turn it into a defect (an input, a caller, a condition); for a falsified hypothesis, the check and its result
6. **Reasoning mode** — Deductive / Inductive / Abductive
7. **Confidence** — per the scoring table above, for the finding as typed (a preventive measure scores how sure you are that the risk exists, not that it happens)
8. **Fix** — for a defect, the specific change; for a preventive measure, the safeguard you propose; for a falsified hypothesis, none (the check stays as a regression guard)

**Falsified hypothesis, in full.** Say it plainly; don't leave it as "could not reproduce". A check falsifies a suspicion only if it **could have failed**: it was seen failing with the suspected defect injected, or you can show that it exercises the suspected path and asserts the suspected effect. It also falls under the test-environment constraint (Step 4). If you cannot show that it could have failed, report it as **conditionally falsified** and name the check that would complete it, for example: "red when the invalidation is removed". The falsification covers only the paths the check exercised. Name the ones it did not cover; they stay open, as rows in HYPOTHESES. Propose no fix for a defect that was not shown.

**One finding, one type.** If a problem is demonstrated on one path and only plausible on another, report two findings. Preventive measures and demonstrated defects both go in the FAIL table, and its Type column says which. Falsified hypotheses go in their own table.

## Output Format

```
## VERIFICATION DOMAIN
[Code | Architecture | Data | Documentation | Tests | Analysis]

## GROUND TRUTH
[Sources used for verification]

## INVARIANTS
[Where you looked; how many found; "none found" is a valid answer. List only the touched ones]
| # | Invariant | Source | Touched by | Enforced by (file:line / test name) | Bites on changed path? (code, data) / Respected? (plans, specs, docs, analyses) |
|---|-----------|--------|------------|-------------------------------------|------------------------|

## DECOMPOSED CLAIMS
1. [Claim text] — Mode: [Deductive/Inductive/Abductive]
...

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|

## VERIFICATION RESULTS
### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|

### FALSIFIED HYPOTHESES
| # | Location | Suspected defect | Check (quote) | Status (falsified / conditionally) | Could it have failed? (how shown, or the check that would complete it) | Paths not covered | Mode | Confidence |
|---|----------|------------------|-------|------------------------------------|------------------------------------------------------------------------|-------------------|------|------------|

### FAIL ❌
| # | File:Line | Type | Severity | Mode | Confidence | Issue |
|---|-----------|------|----------|------|------------|-------|

## STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|

## HYPOTHESES (Abductive — require further investigation)
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|

## HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Type (if a problem) | Confidence |
|---|----------|-----------|--------|---------------------|------------|

## ADVERSARIAL SCAFFOLD FINDINGS
- Reviewer blind spots: [what a normal reviewer would miss]
- Highest-risk claims: [top 3, by blast radius × probability]
- Multi-step traces: [A → B → C chains]
- Subtlety flags: [code hiding complexity]

### SUMMARY
- Domain: [Code/Architecture/Data/Documentation/Tests/Analysis]
- Claims: X verified, Y in FAIL (defects and preventive measures), Z falsified
- Survived: X/Y stress tests passed
- Failure categories: N systemic patterns
- Invariants: N found, M touched, K enforced by a mechanism that bites on the changed path (code, data) or respected (plans, specs, docs, analyses)
- Hypotheses: N requiring further investigation
- Hidden behaviors: N detected
- Findings by type: N demonstrated defects, M preventive measures, K falsified hypotheses (J of them conditionally)
- Critical issues: N demonstrated defects of critical severity (preventive measures of critical severity listed separately: M)
- Recommendation: [trust adjustment or approval]
```

For multi-domain verification, repeat per domain with a CROSS-DOMAIN SUMMARY at the end.

## Step 5: PROJECT DISCOVERY UPDATE

After reporting, check for: `TODO.md`, `SPEC.md`, `PLAN.md`, `CHANGELOG.md`, `ADR/`, `.claude/` docs. If findings are relevant, **propose** updates — do NOT write directly. Wait for explicit user confirmation.

## Trust Scoring (Optional)

If the project uses `.claude/agent-trust.json`: demonstrated defect found → author -1 (preventive measures and falsified hypotheses don't count), false positive → verifier -1, 3 clean reviews (no demonstrated defect) → author +1.

## References

- [Chain-of-Verification (CoV)](https://arxiv.org/abs/2309.11495) — Dhuliawala et al., 2023
- [Automated Auditing](https://alignment.anthropic.com/2025/automated-auditing/) — Anthropic, 2025
- [Abstractive Red-Teaming](https://alignment.anthropic.com/2026/abstractive-red-teaming/) — Anthropic, 2026
- [AuditBench](https://alignment.anthropic.com/2026/auditbench/) — Anthropic, 2026
- [Strengthening Red Teams](https://alignment.anthropic.com/2025/strengthening-red-teams/) — Anthropic, 2025
- [Principles of Chaos Engineering](https://principlesofchaos.org/)

## Anti-patterns to avoid

- **Don't trust "looks correct"** — trace the actual execution
- **Don't skip "simple" code** — simple code has simple bugs
- **Don't accept "it worked in testing"** — testing doesn't cover edge cases
- **Don't rely on a test result before asking if it would be the same in production** — a pass or a failure caused by the test environment proves nothing, so a finding that rests on it cannot be Verified
- **Don't dismiss low-probability scenarios** — rare events happen every session at scale
- **Don't trust comments** — comments lie, code doesn't
- **Don't verify only one domain** — if code changed, check if SPEC.md still matches
- **Don't skip ground truth** — without a reference, you can't verify anything
- **Don't ignore the project's own invariants** — a rule the project says must never break is the first thing a change can break silently; check what enforces it on the changed path
- **Don't auto-update project docs** — always propose, never write without confirmation
- **Don't stop at individual bugs** — abstract to failure categories and search for patterns
- **Don't trust the interface** — probe the actual behavior, not what the code advertises
- **Don't collect evidence without hypotheses** — every finding needs a conclusion
- **Don't claim absence without stating where you looked** — "X doesn't exist" requires citing what you checked
- **Don't report only problems** — stress tests that survive are equally valuable results
- **Don't call a risk a bug** — type every problem or suspicion you report: demonstrated defect, preventive measure, or falsified hypothesis
- **Don't use the same technique twice** — forced variety prevents analytical tunnel vision
