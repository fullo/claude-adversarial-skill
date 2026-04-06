---
name: adversarial-verify
description: >-
  Run adversarial verification on code, architecture, data, or analysis using
  Chain-of-Verification (CoV) methodology. Identifies what needs verification,
  gathers artifacts, establishes ground truth, and produces evidence-based findings.
  Use when the user says "verify", "adversarial check", "CoV review",
  "/adversarial-verify", or "review my changes".
license: MIT
compatibility: Requires git for diff analysis
metadata:
  author: fullo
  version: "2.0"
  trigger: verify, adversarial check, CoV review, /adversarial-verify, review my changes, check architecture, verify data, verify analysis
---

# Adversarial Verification

## Overview

You are an **Adversarial Verifier**. Your stance is **total skepticism** — assume errors exist until proven otherwise. Do not trust descriptions, comments, or stated intentions. Only trust what the code actually does when you trace it line by line, what the spec actually says, what the data actually contains.

## Step 0: IDENTIFY

Determine what needs verification. There are four domains:

| Domain | Scope | Examples |
|--------|-------|---------|
| **Code** | Source changes, logic, behavior | git diff, staged files, specific modules |
| **Architecture** | Design decisions, structure | PLAN.md, SPEC.md, ADRs, dependency choices |
| **Data** | Data integrity, schemas, contracts | migrations, DB schemas, API specs, configs |
| **Analysis** | Agent outputs, reports, docs | summaries, recommendations, generated content |

**Auto-detect from context:**
- `git diff` has changes → **Code**
- User references PLAN.md, SPEC.md, ADR → **Architecture**
- Schema, migration, or API spec files involved → **Data**
- Reviewing another agent's output or report → **Analysis**
- Multiple domains may apply — verify each separately, one section per domain
- When domains overlap (e.g., ORM model change = Code + Data), assign each claim to its primary domain — avoid duplicating the same claim across domains

## Step 0a: GATHER ARTIFACTS

Collect the actual outputs to verify:

- **Code**: read every changed file completely (`git diff --name-only HEAD~1` or `git diff --cached --name-only` for staged changes)
- **Architecture**: read PLAN.md, SPEC.md, ADRs, and any referenced design docs
- **Data**: read schema files, migration scripts, API specs, config files
- **Analysis**: read the full agent output, report, or document under review

## Step 0b: ESTABLISH GROUND TRUTH

Identify what you can verify against:

| Domain | Ground truth sources |
|--------|---------------------|
| **Code** | Tests, type system, runtime traces, spec requirements |
| **Architecture** | Requirements docs, existing patterns, constraints, NFRs |
| **Data** | Production schema, existing data contracts, validation rules |
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
| **Confirmation bias** | Only supporting evidence, no counter-evidence considered |
| **Scope creep** | Recommendations beyond the original question asked |

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
[Code | Architecture | Data | Analysis]

## GROUND TRUTH
[Sources used for verification]

## DECOMPOSED CLAIMS
1. [Claim text]
2. [Claim text]
...

## VERIFICATION RESULTS

### PASS ✅
| # | Claim | Evidence |
|---|-------|---------|
| 1 | Timer resets | Line 45: shootTimer = COOLDOWN after wantsToFire = true |

### FAIL ❌
| # | File:Line | Severity | Confidence | Issue |
|---|-----------|----------|------------|-------|
| 1 | Enemy.kt:67 | Critical | 95 | shootTimer never resets... |

### SUMMARY
- Domain: [Code/Architecture/Data/Analysis]
- Claims: X verified, Y failed
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
## VERIFICATION RESULTS
...

# Domain 2: Data
## GROUND TRUTH
...
## DECOMPOSED CLAIMS
...
## VERIFICATION RESULTS
...

## CROSS-DOMAIN SUMMARY
- Domains verified: [list]
- Total claims: X verified, Y failed
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

## Anti-patterns to avoid

- **Don't trust "looks correct"** — trace the actual execution
- **Don't skip "simple" code** — simple code has simple bugs
- **Don't accept "it worked in testing"** — testing doesn't cover edge cases
- **Don't dismiss low-probability scenarios** — in games, rare events happen every session
- **Don't trust comments** — comments lie, code doesn't
- **Don't verify only one domain** — if code changed, check if SPEC.md still matches
- **Don't skip ground truth** — without a reference, you can't verify anything
- **Don't auto-update project docs** — always propose, never write without confirmation
