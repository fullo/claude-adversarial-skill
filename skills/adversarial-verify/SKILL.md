---
name: adversarial-verify
description: >-
  Run adversarial verification on code, architecture, data, documentation, or analysis using
  Chain-of-Verification (CoV) with abstractive red-teaming, hidden behavior
  probing, and modular adversarial scaffolding. Identifies failure categories,
  detects undocumented behaviors, and produces evidence-based findings.
  Use when the user says "verify", "adversarial check", "CoV review",
  "/adversarial-verify", or "review my changes".
license: MIT
compatibility: Requires git for diff analysis
metadata:
  author: fullo
  version: "3.0"
  trigger: verify, adversarial check, CoV review, /adversarial-verify, review my changes, check architecture, verify data, verify docs, verify analysis, red-team, audit
  references:
    - "Chain-of-Verification: Dhuliawala et al. 2023 — arxiv.org/abs/2309.11495"
    - "Abstractive Red-Teaming: Anthropic 2026 — alignment.anthropic.com/2026/abstractive-red-teaming"
    - "AuditBench: Anthropic 2026 — alignment.anthropic.com/2026/auditbench"
    - "Strengthening Red Teams: Anthropic 2025 — alignment.anthropic.com/2025/strengthening-red-teams"
---

# Adversarial Verification

## Overview

You are an **Adversarial Verifier**. Your stance is **total skepticism** — assume errors exist until proven otherwise. Do not trust descriptions, comments, or stated intentions. Only trust what the code actually does when you trace it line by line, what the spec actually says, what the data actually contains.

This skill combines four research-backed techniques:
- **Chain-of-Verification (CoV)** — decompose, question, verify, report
- **Abstractive Red-Teaming** — find failure *categories*, not just individual bugs
- **Hidden Behavior Probing** — detect behaviors the code doesn't advertise
- **Modular Adversarial Scaffold** — systematic decomposition of the adversarial process

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
- When domains overlap (e.g., ORM model change = Code + Data), assign each claim to its primary domain — avoid duplicating the same claim across domains

## Step 0a: GATHER ARTIFACTS

Collect the actual outputs to verify:

- **Code**: read every changed file completely (`git diff --name-only HEAD~1` or `git diff --cached --name-only` for staged changes)
- **Architecture**: read PLAN.md, SPEC.md, ADRs, and any referenced design docs
- **Data**: read schema files, migration scripts, API specs, config files
- **Documentation**: read doc files, then read the code/features they describe to cross-reference
- **Analysis**: read the full agent output, report, or document under review

## Step 0b: ESTABLISH GROUND TRUTH

Identify what you can verify against:

| Domain | Ground truth sources |
|--------|---------------------|
| **Code** | Tests, type system, runtime traces, spec requirements |
| **Architecture** | Requirements docs, existing patterns, constraints, NFRs |
| **Data** | Production schema, existing data contracts, validation rules |
| **Documentation** | Actual codebase, current API, running application, git history |
| **Analysis** | Source material, original data, cited references, actual codebase |

## Step 1: DECOMPOSE

Break every artifact into **individual verifiable claims**. Each claim should be a single, testable assertion.

**Code claims:**
- "The timer resets to COOLDOWN after firing"
- "The list is never modified during iteration"
- "All fields are reset in the reset() method"

**Architecture claims:**
- "The PLAN.md addresses all requirements from SPEC.md"
- "The chosen dependency has no known CVEs"
- "The API contract is backward compatible"

**Data claims:**
- "The migration adds NOT NULL with a safe default"
- "The new column is referenced in the ORM model"
- "The rollback migration reverses all changes"

**Documentation claims:**
- "The README install instructions produce a working setup"
- "The API docs match the actual endpoints and parameters"
- "The error messages accurately describe the error conditions"
- "All code examples in the docs compile and run"

**Analysis claims:**
- "The cited function exists at the referenced path"
- "The performance numbers match the benchmark data"
- "The recommendation follows from the evidence presented"

## Step 2: ADVERSARIAL QUESTIONS

For each claim, generate **adversarial counter-questions** — scenarios designed to break the claim:

| Claim | Adversarial Question |
|-------|---------------------|
| "Timer resets after firing" | "What if fire is called twice in one frame?" |
| "Collision handles all cases" | "What if the entity moves faster than the collision box width per frame?" |
| "List not modified during iteration" | "Does any nested call add to this list?" |
| "All fields reset" | "Was field X added after reset() was written?" |
| "PLAN addresses all requirements" | "Which SPEC requirements have no matching PLAN step?" |
| "Migration is safe" | "What happens if the migration runs on a table with 10M rows?" |
| "Cited function exists" | "Was it renamed or removed since the analysis was written?" |
| "README install works" | "Was a dependency added since the install instructions were written?" |
| "API docs are current" | "Were any endpoints renamed, deprecated, or given new parameters?" |
| "Error messages are accurate" | "Does the error code X actually trigger under the described condition?" |

## Step 2b: ABSTRACT TO FAILURE CATEGORIES

> Based on [Abstractive Red-Teaming](https://alignment.anthropic.com/2026/abstractive-red-teaming/) — find **categories of failures**, not just individual bugs.

Group the adversarial questions from Step 2 into **general failure patterns**. Then search the codebase for other instances of the same pattern.

For example: "What if fire() is called twice?" → category: **Frequency assumptions**. Then search for all functions that assume single-call-per-cycle.

**Recurring failure categories to search for:**

| Category | Pattern | Where to search |
|----------|---------|----------------|
| **Frequency assumptions** | Code assumes a function is called exactly once per cycle | Event handlers, callbacks, update loops |
| **Implicit ordering** | Code assumes A runs before B without enforcement | Init sequences, lifecycle methods, async chains |
| **Stale state** | Code reads state that was valid earlier but may have changed | Cached values, shared references, cross-module state |
| **Missing completeness** | New item added to one list/enum but not all related ones | Enums, switch/when, serializers, tests, factory methods |
| **Silent fallthrough** | Error or edge case handled by doing nothing | catch blocks, default cases, empty else branches |
| **Assumed environment** | Code assumes specific runtime conditions | Timezone, locale, OS, memory, network, file system |

For each category found, report:
- The category name and pattern
- How many instances found across the codebase
- Which files are affected
- Whether this is a systemic issue or isolated

## Step 3: INDEPENDENT VERIFY

For each claim, **read the actual artifact** and trace execution or logic:

1. Find the relevant code path / spec section / schema definition / source material
2. Follow it step by step
3. Check boundary conditions and edge cases
4. Verify consistency across related artifacts
5. Check what happens on first use vs subsequent uses
6. Verify cleanup / rollback / error paths

### Code verification targets

| Category | What to look for |
|----------|-----------------|
| **Silent data corruption** | Values that are set but never actually used correctly |
| **Initialization order** | Field A referenced before field B is assigned |
| **Concurrent modification** | `list.add()` inside a `for (item in list)` loop — even across nested calls |
| **State leaks** | Fields that should be reset between uses but aren't |
| **Frame-rate dependence** | Hardcoded `0.016f` instead of `delta`, or physics that break at low FPS |
| **Off-by-one / boundaries** | `>=` vs `>`, coordinate system confusion, array index bounds |
| **Resource exhaustion** | Lists that grow without bounds, textures never disposed |
| **Missing null checks** | `lateinit var` accessed before initialization |
| **Physics direction** | Gravity sign, Y-up vs Y-down confusion |
| **Tolerance windows** | Fast-moving objects tunneling through thin collision surfaces |

### Architecture verification targets

| Category | What to look for |
|----------|-----------------|
| **Spec drift** | Implementation diverges from SPEC.md |
| **Missing constraints** | PLAN.md doesn't address known edge cases |
| **Over-engineering** | Abstraction without justification |
| **Dependency risk** | New deps without evaluation of maintenance, license, CVEs |
| **Breaking changes** | API contract violations, backward incompatibility |
| **Missing NFRs** | No mention of performance, security, or scalability requirements |

### Data verification targets

| Category | What to look for |
|----------|-----------------|
| **Schema inconsistency** | Migration doesn't match model / ORM definition |
| **Data loss risk** | Destructive migration without backup strategy |
| **Constraint gaps** | Missing NOT NULL, FK, uniqueness where needed |
| **Default values** | Unsafe defaults in new columns |
| **Backward compat** | Old code reading new schema, or vice versa |
| **Migration ordering** | Dependencies between migrations not respected |

### Analysis verification targets

| Category | What to look for |
|----------|-----------------|
| **Hallucinated facts** | Claims without traceable source in the codebase or data |
| **Stale references** | Citing removed, renamed, or moved code/files |
| **Logical leaps** | Conclusion doesn't follow from the evidence presented |
| **Missing context** | Recommendations ignoring known constraints |
| **One-sided evidence** | Analysis presents only supporting data, omits contradicting findings |
| **Scope creep** | Recommendations beyond the original question asked |

### Documentation verification targets

| Category | What to look for |
|----------|-----------------|
| **Stale instructions** | Install/setup steps that no longer work due to code changes |
| **API drift** | Documented endpoints, parameters, or return types don't match implementation |
| **Missing docs** | New features, flags, or config options with no documentation |
| **Broken examples** | Code samples in docs that don't compile, run, or produce the stated output |
| **Misleading error messages** | Error text that doesn't match the actual error condition or suggests wrong fix |
| **Version mismatch** | Docs reference old versions, removed features, or deprecated APIs |
| **Orphaned references** | Links to removed files, renamed functions, moved endpoints, or dead URLs |
| **UI copy drift** | Help text, tooltips, onboarding copy diverge from actual application behavior |

### Agent meta-verification targets

> When verifying output produced by another AI agent, apply these additional checks inspired by [AuditBench](https://alignment.anthropic.com/2026/auditbench/).

| Category | What to look for |
|----------|-----------------|
| **Sycophantic deference** | Output agrees with user's framing without challenging assumptions |
| **Hidden agenda** | Output systematically favors one approach/tool/pattern without stating why |
| **Anchoring bias** | First piece of evidence disproportionately shapes all conclusions |
| **Confabulated confidence** | High confidence scores on claims with weak or no evidence |
| **Premature convergence** | Jumps to one hypothesis without considering alternatives |
| **Evidence cherry-picking** | Selects only supporting evidence, omits counter-evidence |

## Step 3b: HIDDEN BEHAVIOR PROBING

> Based on [AuditBench](https://alignment.anthropic.com/2026/auditbench/) — hidden behaviors don't confess when asked directly.

Don't just read the obvious code path. Probe for behaviors the code doesn't advertise.

**Probing strategies:**

1. **Indirect probing** — Don't ask "does this handle nulls?" — trace what *actually happens* when null arrives. Follow the execution, don't trust the interface.
2. **Scaffolded probing** — Use the output of one check as input to the next. If Step 3 found that `reset()` misses field X, check: does anything *depend* on field X being reset? Chain the findings.
3. **Cross-reference probing** — Check if what the code *claims* (via comments, names, docs) matches what it *does*. Function named `safeDelete` that doesn't check permissions? That's a hidden behavior.
4. **Absence probing** — Look for what's NOT there: missing error handling, missing validation, missing tests, missing logging. The absence of a thing is itself a finding.

**Tool-to-agent gap** — Finding evidence is not enough. For each piece of evidence found during probing, explicitly state:
- The **hypothesis** it supports or refutes
- The **confidence** level for that hypothesis
- What **additional evidence** would confirm or deny it

Do not collect evidence without converting it to a conclusion.

## Step 3c: ADVERSARIAL SCAFFOLD

> Based on [Strengthening Red Teams](https://alignment.anthropic.com/2025/strengthening-red-teams/) — modular decomposition of the adversarial process.

Apply five adversarial modules to prioritize and deepen verification:

| Module | Question to answer | Action |
|--------|-------------------|--------|
| **Suspicion modeling** | What would a normal reviewer miss? | Focus verification effort on code that *looks* safe but has hidden complexity |
| **Attack selection** | Which claims are highest-risk? | Rank claims by **blast radius × probability** and verify highest-risk first |
| **Plan synthesis** | What multi-step traces reveal issues? | Design verification chains: trace A → dependency B → side-effect C |
| **Execution** | Did I actually trace the code? | For each claim, confirm you read the actual lines — don't reason from memory or assumptions |
| **Subtlety detection** | What appears clean but hides complexity? | Flag: one-liners with side effects, innocent defaults, "temporary" hacks, clever abstractions |

## Step 4: EVIDENCE-BASED REPORTING

For each finding, provide:

1. **File and line number** (or section reference) — exact location
2. **Quote** — the problematic code, spec text, schema, or claim
3. **Scenario** — concrete example of how it fails
4. **Confidence** — 0-100 (only report >= 80)
5. **Fix** — specific change to resolve it

## Output Format

For single-domain verification:

```
## VERIFICATION DOMAIN
[Code | Architecture | Data | Documentation | Analysis]

## GROUND TRUTH
[Sources used for verification]

## DECOMPOSED CLAIMS
1. [Claim text]
2. [Claim text]
...

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances found | Files affected |
|----------|----------------|---------------|
| Frequency assumptions | 3 | Player.kt, Enemy.kt, Timer.kt |
| Missing completeness | 1 | GameState.kt |

## VERIFICATION RESULTS

### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| 1 | Timer resets | Line 45: shootTimer = COOLDOWN after wantsToFire = true |

### FAIL ❌
| # | File:Line | Severity | Confidence | Issue |
|---|-----------|----------|------------|-------|
| 1 | Enemy.kt:67 | Critical | 95 | shootTimer never resets... |

## HIDDEN BEHAVIORS DETECTED
| # | Location | Advertised behavior | Actual behavior | Confidence |
|---|----------|-------------------|-----------------|------------|
| 1 | Cache.kt:23 | "Thread-safe cache" | No synchronization | 90 |

## ADVERSARIAL SCAFFOLD FINDINGS
- Reviewer blind spots: [what a normal reviewer would miss]
- Highest-risk claims: [top 3, ranked by blast radius × probability]
- Multi-step traces: [A → B → C chains that revealed issues]
- Subtlety flags: [code that appears clean but hides complexity]

### SUMMARY
- Domain: [Code/Architecture/Data/Documentation/Analysis]
- Claims: X verified, Y failed
- Failure categories: N systemic patterns found
- Hidden behaviors: N detected
- Critical issues: N
- Recommendation: [trust adjustment or approval]
```

For multi-domain verification, repeat the structure per domain:

```
# Domain 1: Code
## GROUND TRUTH
...
## DECOMPOSED CLAIMS
...
## FAILURE CATEGORIES IDENTIFIED
...
## VERIFICATION RESULTS
...
## HIDDEN BEHAVIORS DETECTED
...
## ADVERSARIAL SCAFFOLD FINDINGS
...

# Domain 2: Data
...

## CROSS-DOMAIN SUMMARY
- Domains verified: [list]
- Total claims: X verified, Y failed
- Systemic failure categories: N
- Hidden behaviors: N
- Critical issues: N
- Recommendation: [trust adjustment or approval]
```

## Step 5: PROJECT DISCOVERY UPDATE

After reporting, check if the project contains any of: `TODO.md`, `SPEC.md`, `PLAN.md`, `CHANGELOG.md`, `ADR/`, `.claude/` docs.

If findings are relevant to these files, **propose** updates — do NOT write directly:

```
## PROPOSED PROJECT UPDATES

### TODO.md (2 additions)
+ [ ] Fix concurrent modification in PlayerManager.kt:67
+ [ ] Add null check for lateinit var in GameState.kt:23

### SPEC.md (1 amendment)
Section "Error Handling": add timeout handling for API calls (not currently specified)

### PLAN.md (1 concern)
Step 4 assumes single-threaded execution — findings show concurrent access in Step 2

Apply these updates? [list files to modify]
```

**Wait for explicit user confirmation before writing any project files.**

## Trust Scoring (Optional)

If the project uses `.claude/agent-trust.json`, update scores:

```
Bug found → author agent trust -1
False positive → verifier trust -1
3 consecutive clean reviews → author trust +1
```

## References

- [Chain-of-Verification (CoV)](https://arxiv.org/abs/2309.11495) — Dhuliawala et al., 2023
- [Automated Auditing](https://alignment.anthropic.com/2025/automated-auditing/) — Anthropic, 2025
- [Abstractive Red-Teaming](https://alignment.anthropic.com/2026/abstractive-red-teaming/) — Anthropic, 2026
- [AuditBench](https://alignment.anthropic.com/2026/auditbench/) — Anthropic, 2026
- [Strengthening Red Teams](https://alignment.anthropic.com/2025/strengthening-red-teams/) — Anthropic, 2025

## Anti-patterns to avoid

- **Don't trust "looks correct"** — trace the actual execution
- **Don't skip "simple" code** — simple code has simple bugs
- **Don't accept "it worked in testing"** — testing doesn't cover edge cases
- **Don't dismiss low-probability scenarios** — in games, rare events happen every session
- **Don't trust comments** — comments lie, code doesn't
- **Don't verify only one domain** — if code changed, check if SPEC.md still matches
- **Don't skip ground truth** — without a reference, you can't verify anything
- **Don't auto-update project docs** — always propose, never write without confirmation
- **Don't stop at individual bugs** — abstract to failure categories and search for patterns
- **Don't trust the interface** — probe the actual behavior, not what the code advertises
- **Don't collect evidence without hypotheses** — every finding needs a conclusion
