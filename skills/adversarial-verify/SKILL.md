---
name: adversarial-verify
description: >-
  Adversarial verification of code, architecture, data, documentation, or analysis
  using Chain-of-Verification (CoV) with abstractive red-teaming, hidden behavior
  probing, stress techniques, and tri-modal reasoning (deductive, inductive, abductive).
  Identifies failure categories, detects undocumented behaviors, stress-tests for
  resilience, and enforces anti-fabrication discipline.
  Use when the user says "verify", "adversarial check", "CoV review",
  "/adversarial-verify", "review my changes", or "stress test".
license: MIT
compatibility: Requires git for diff analysis
metadata:
  author: fullo
  version: "3.5"
  trigger: verify, adversarial check, CoV review, /adversarial-verify, review my changes, check architecture, verify data, verify docs, verify analysis, red-team, audit, stress test, chaos review
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

Determine what needs verification. There are five domains:

| Domain | Scope | Examples |
|--------|-------|---------|
| **Code** | Source changes, logic, behavior | git diff, staged files, specific modules |
| **Architecture** | Design decisions, structure | PLAN.md, SPEC.md, ADRs, dependency choices |
| **Data** | Data integrity, schemas, contracts | migrations, DB schemas, API specs, configs |
| **Documentation** | Technical, process, and user-facing docs | README, API docs, CHANGELOG, guides, help text, error messages, UI copy |
| **Analysis** | Agent outputs, reports, docs | summaries, recommendations, generated content |

**Auto-detect from context:**
- `git diff` has changes → **Code**
- User references PLAN.md, SPEC.md, ADR → **Architecture**
- Schema, migration, or API spec files involved → **Data**
- README, CHANGELOG, docs/, help text, or error messages changed → **Documentation**
- Reviewing another agent's output or report → **Analysis**
- Multiple domains may apply — verify each separately, one section per domain
- When domains overlap (e.g., ORM model change = Code + Data), assign each claim to its primary domain

## Step 0a: GATHER ARTIFACTS

- **Code**: read every changed file completely (`git diff --name-only HEAD~1` or `git diff --cached --name-only` for staged changes)
- **Architecture**: read PLAN.md, SPEC.md, ADRs, and any referenced design docs
- **Data**: read schema files, migration scripts, API specs, config files
- **Documentation**: read doc files, then read the code/features they describe to cross-reference
- **Analysis**: read the full agent output, report, or document under review

## Step 0b: ESTABLISH GROUND TRUTH

| Domain | Ground truth sources |
|--------|---------------------|
| **Code** | Tests, type system, runtime traces, spec requirements |
| **Architecture** | Requirements docs, existing patterns, constraints, NFRs |
| **Data** | Production schema, existing data contracts, validation rules |
| **Documentation** | Actual codebase, current API, running application, git history |
| **Analysis** | Source material, original data, cited references, actual codebase |

## Step 1: DECOMPOSE

Break every artifact into **individual verifiable claims**. Each claim should be a single, testable assertion.

**Code:** "The timer resets to COOLDOWN after firing" / "The list is never modified during iteration"
**Architecture:** "The PLAN.md addresses all requirements from SPEC.md" / "The API contract is backward compatible"
**Data:** "The migration adds NOT NULL with a safe default" / "The rollback reverses all changes"
**Documentation:** "The README install instructions produce a working setup" / "The API docs match the actual endpoints"
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
| "Timer resets after firing" | "What if fire is called twice in one frame?" |
| "List not modified during iteration" | "Does any nested call add to this list?" |
| "All fields reset" | "Was field X added after reset() was written?" |
| "PLAN addresses all requirements" | "Which SPEC requirements have no matching PLAN step?" |
| "Migration is safe" | "What happens on a table with 10M rows?" |
| "README install works" | "Was a dependency added since the instructions were written?" |

## Step 2b: ABSTRACT TO FAILURE CATEGORIES

> Based on [Abstractive Red-Teaming](https://alignment.anthropic.com/2026/abstractive-red-teaming/) — find **categories of failures**, not just individual bugs.

Group adversarial questions into **general failure patterns**, then search the codebase for other instances.

| Category | Pattern | Where to search |
|----------|---------|----------------|
| **Frequency assumptions** | Function assumed to be called exactly once per cycle | Event handlers, callbacks, update loops |
| **Implicit ordering** | A assumed to run before B without enforcement | Init sequences, lifecycle methods, async chains |
| **Stale state** | State that was valid earlier but may have changed | Cached values, shared references, cross-module state |
| **Missing completeness** | New item added to one list but not all related ones | Enums, switch/when, serializers, tests, factory methods |
| **Silent fallthrough** | Error or edge case handled by doing nothing | catch blocks, default cases, empty else branches |
| **Assumed environment** | Code assumes specific runtime conditions | Timezone, locale, OS, memory, network, file system |

## Step 3: INDEPENDENT VERIFY

For each claim, **read the actual artifact** and trace execution or logic:
1. Find the relevant code path / spec section / schema definition / source material
2. Follow it step by step
3. Check boundary conditions and edge cases
4. Verify consistency across related artifacts
5. Check what happens on first use vs subsequent uses
6. Verify cleanup / rollback / error paths

### Verification targets by domain

**Code:** Silent data corruption, initialization order, concurrent modification, state leaks, frame-rate dependence, off-by-one/boundaries, resource exhaustion, missing null checks, physics direction, tolerance windows.

**Architecture:** Spec drift, missing constraints, over-engineering, dependency risk (maintenance, license, CVEs), breaking changes, missing NFRs.

**Data:** Schema inconsistency, data loss risk, constraint gaps (NOT NULL, FK, uniqueness), unsafe defaults, backward compat, migration ordering.

**Documentation:** Stale instructions, API drift, missing docs, broken examples, misleading error messages, version mismatch, orphaned references, UI copy drift.

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

### Finding format

1. **Location** — file:line or section reference
2. **Quote** — the problematic code, spec text, schema, or claim
3. **Scenario** — concrete example of how it fails
4. **Reasoning mode** — Deductive / Inductive / Abductive
5. **Confidence** — per the scoring table above
6. **Survived** — yes (confirmed robust) / no (fragile) / n/a (not stress-tested)
7. **Fix** — specific change (for no) or "Confirmed robust" (for yes)

## Output Format

```
## VERIFICATION DOMAIN
[Code | Architecture | Data | Documentation | Analysis]

## GROUND TRUTH
[Sources used for verification]

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

### FAIL ❌
| # | File:Line | Severity | Mode | Confidence | Issue |
|---|-----------|----------|------|------------|-------|

## STRESS TEST RESULTS
| # | Technique | Target | Survived | Confidence | Evidence |
|---|-----------|--------|----------|------------|---------|

## HYPOTHESES (Abductive — require further investigation)
| # | Observation | Hypothesis | Alternative | Test to confirm |
|---|-------------|-----------|-------------|----------------|

## HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised | Actual | Confidence |
|---|----------|-----------|--------|------------|

## ADVERSARIAL SCAFFOLD FINDINGS
- Reviewer blind spots: [what a normal reviewer would miss]
- Highest-risk claims: [top 3, by blast radius × probability]
- Multi-step traces: [A → B → C chains]
- Subtlety flags: [code hiding complexity]

### SUMMARY
- Domain: [Code/Architecture/Data/Documentation/Analysis]
- Claims: X verified, Y failed
- Survived: X/Y stress tests passed
- Failure categories: N systemic patterns
- Hypotheses: N requiring further investigation
- Hidden behaviors: N detected
- Critical issues: N
- Recommendation: [trust adjustment or approval]
```

For multi-domain verification, repeat per domain with a CROSS-DOMAIN SUMMARY at the end.

## Step 5: PROJECT DISCOVERY UPDATE

After reporting, check for: `TODO.md`, `SPEC.md`, `PLAN.md`, `CHANGELOG.md`, `ADR/`, `.claude/` docs. If findings are relevant, **propose** updates — do NOT write directly. Wait for explicit user confirmation.

## Trust Scoring (Optional)

If the project uses `.claude/agent-trust.json`: bug found → author -1, false positive → verifier -1, 3 clean reviews → author +1.

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
- **Don't dismiss low-probability scenarios** — rare events happen every session at scale
- **Don't trust comments** — comments lie, code doesn't
- **Don't verify only one domain** — if code changed, check if SPEC.md still matches
- **Don't skip ground truth** — without a reference, you can't verify anything
- **Don't auto-update project docs** — always propose, never write without confirmation
- **Don't stop at individual bugs** — abstract to failure categories and search for patterns
- **Don't trust the interface** — probe the actual behavior, not what the code advertises
- **Don't collect evidence without hypotheses** — every finding needs a conclusion
- **Don't claim absence without stating where you looked** — "X doesn't exist" requires citing what you checked
- **Don't report only problems** — stress tests that survive are equally valuable findings
- **Don't use the same technique twice** — forced variety prevents analytical tunnel vision
