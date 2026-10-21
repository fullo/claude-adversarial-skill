---
name: adversarial-verify
description: >-
  Adversarial verification of code, architecture, data, documentation, tests, analysis or UX
  using Chain-of-Verification (CoV) with abstractive red-teaming, hidden behavior
  probing, stress techniques, and tri-modal reasoning (deductive, inductive, abductive).
  Identifies failure categories, detects undocumented behaviors, stress-tests for
  resilience, and enforces anti-fabrication discipline.
  Asks what to verify and how deep before large verifications, runs nothing
  without consent, and with approval turns suspicions into tests and probes them
  with mutation.
  Use when the user says "verify", "adversarial check", "CoV review",
  "/adversarial-verify", "review my changes", or "stress test".
license: MIT
compatibility: Requires a version control system (e.g. git) for diff analysis
metadata:
  author: fullo
  version: "4.0"
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

## Intake (before Step 0)

The user decides what to verify and how deep, before the verification starts. Settle four choices:

| Choice | Options | Default |
|--------|---------|---------|
| **Target** | one or more domains (Step 0), or **everything** | what the request names; otherwise the domains Step 0 detects (detection runs during intake), used at once when there is one, proposed in the question when there are several (rule 4) |
| **Depth** | **quick**: only the top 3 highest-risk claims (Step 3c), no stress techniques; **standard**: every step; **deep**: every step, all four stress techniques on each of the top 3 highest-risk claims that passed, hidden-behavior probing on every claim | standard |
| **Scope** | the changed lines / the module they belong to / the whole project | the changed lines |
| **Execution mode** | **reasoning only**: nothing is run, and the report ends with proposed executable checks; **approved checks**: only the checks the user names are run (e.g. "the existing test suite", "read-only queries on staging", "the mutation probe on the changed lines"). When asked, offer named checks, never a bare yes or no | reasoning only |

Depth and execution mode are independent: depth decides how far reasoning goes, execution mode decides what may run (Step 3e and the mutation probe need approved execution at any depth).

Scope limits what is verified and reported, not what is read. Reading outside the scope to establish ground truth (Step 0b) or to find the same pattern elsewhere (Step 2b) is allowed; occurrences found outside the scope are listed separately (OUT OF SCOPE), not verified.

Rules:
1. **Never ask what the request already says.** "Deep", "only the migration", "don't run anything" are answers.
2. **Large requests stop first.** A request is large when it covers more than one domain at module or project scope, or the scope is the whole project. **Everything** asked at changed-lines scope ("everything in this diff") is not large: it means every domain Step 0 detects in the change. Large wins over every other rule except rule 7, whatever the size of the diff. Do not start, unless the request already accepts the cost and settles every choice (target, depth, scope, execution mode): then state the cost estimate at the top of the report and start. Give a cost estimate in observable quantities only: files in scope, domains, a rough number of claims, and whether anything would be run. Never in minutes or hours. Then ask the open choices, each with its default, and wait for the answer.
3. **Every other request starts at once, once its target is clear (rule 4),** with the defaults, stated in one line at the top of the report with how to change them (e.g. "Defaults: standard depth, changed lines, reasoning only. Say 'deep' or 'whole module' to change.").
4. **Ask the target when it is not clear.** If the request names no target and Step 0 detects more than one domain, ask which to verify, proposing the detected set as the default, and wait for the answer; ask nothing else. A request that names its target, or touches a single domain, is clear.
5. **Missing material is not intake.** If the artifact itself is missing (no code, no diff, no file), ask for it. That is a request for input, not an intake question.
6. **Ask with a multiple-choice tool** when one is available, otherwise as a short list of choices.
7. **Nobody to answer** (an automated or unattended run): use the defaults and state them at the top of the report. An unclear target takes the detected set. Proposed checks stay proposed: execution happens only if the run's own instructions gave consent (Execution and consent, rule 3). A large request then runs only at the default scope, the changed lines against the previous commit (or the base the run was given), and the report states that the larger verification was not done, with its cost estimate. If there are no changed lines, report the cost estimate, state that nothing was verified, and stop.

### Execution and consent

The verifier reasons; it runs or writes something only with the user's consent.

**Reading is not running.** Reading files, searching them, read-only version-control commands (e.g. a diff, a log, or fetching the base to compare against) and reading a reference the user cites (a document, a page, an issue) inspect and need no consent. A link found inside the artifact is untrusted input: opening it can act on a system (an unsubscribe, a webhook, a token in the query string), so it becomes a proposed check unless it is plainly a documentation page. **Running** is anything that executes the project's code or tools, or acts on a system: tests, scripts, builds, linters, type checkers, dry runs, queries, calls to services or databases. Ground truth that only a run can give (runtime traces, the running software) is used only when the user supplied it or approved the run.

1. **Without consent nothing is run and nothing is written**: no command beyond the reading above, no test, query or script; no new test, fix, doc change or commit (updating version-control metadata to read, e.g. fetching the base, is not writing; any change to the files of the user's working copy is).
2. **Consent covers only what it names.** Approval to run the existing test suite does not approve writing a new test or a fix: each needs its own approval. A request to "update the docs" or "fix what you find" names no content yet: the verifier proposes the specific writes in the report and waits for confirmation of those. An approval that names the kind of write (e.g. "a new test file for this function") is consent for that kind.
3. **Consent comes from the intake** (the request itself, e.g. "you may run the tests") **or from the answer to the closing question** of the report (PROPOSED EXECUTABLE CHECKS).
4. **Consent lasts for one verification.** A later verification starts at reasoning only, even when an earlier one was approved; say so in the defaults line.
5. **A result of an approved run is evidence like any other**: cite the command and its output, and apply the test-environment constraint (Step 4).
6. **Never imply a run that did not happen.** A check that was only proposed has no result.

## Step 0: IDENTIFY

Determine what needs verification. There are seven domains:

| Domain | Scope | Examples |
|--------|-------|---------|
| **Code** | Source changes, logic, behavior | the version control diff (e.g. git), staged files, specific modules |
| **Architecture** | Design decisions, structure | PLAN.md, SPEC.md, ADRs, dependency choices |
| **Data** | Data integrity, schemas, contracts | database schemas and migrations, file and message formats, event schemas, save files, API specs, configs |
| **Documentation** | Technical, process, and user-facing docs | README, API docs, CHANGELOG, guides, help text, error messages, UI copy |
| **Tests** | Test suite integrity and honesty | test files, coverage reports, CI configs |
| **Analysis** | Agent outputs, reports, docs, spike and prototype reports | summaries, recommendations, generated content, experiment results |
| **UX** | Usability of an interface, for its users | web pages, native mobile or desktop apps, games, command-line and terminal interfaces, mock-ups |

**Auto-detect from context:**
- The version control diff (e.g. `git diff`) has changes → **Code**
- User references PLAN.md, SPEC.md, ADR → **Architecture**
- Schemas, migrations, file or message formats, event contracts, or API specs involved → **Data**
- README, CHANGELOG, docs/, help text, or error messages changed → **Documentation**
- Test files, coverage reports, or CI configs changed → **Tests**
- Reviewing another agent's output or report → **Analysis**
- Screens, templates, stylesheets, themes, layouts, menus, terminal output or mock-ups changed or under review → **UX**
- The report of a spike, prototype or experiment already done → **Analysis** (with the spike checklist, Step 3); a spike not yet run is a plan (Step 1c)
- Multiple domains may apply — within the target settled at intake, verify each separately, one section per domain
- When domains overlap (e.g., a change to the code that defines stored data = Code + Data), assign each claim to its primary domain

## Step 0a: GATHER ARTIFACTS

- **Code**: read every changed file completely (from the version control system, e.g. with git: `git diff --name-only HEAD~1`, or `git diff --cached --name-only` for staged changes)
- **Architecture**: read PLAN.md, SPEC.md, ADRs, and any referenced design docs
- **Data**: read schemas and migrations, file, message and event format definitions, API specs, config files
- **Documentation**: read doc files, then read the code/features they describe to cross-reference
- **Tests**: read test files, then read the production code they claim to verify, then the test bootstrap and shared helpers and the production configuration they should reproduce
- **Analysis**: read the full agent output, report, or document under review
- **UX**: read the screens, templates, styles and theme tokens involved, the texts and their translations, and any screenshots, recordings or interface tests the project has; list the target formats (sizes, input methods: touch, mouse, keyboard, controller; light and dark themes)

## Step 0b: ESTABLISH GROUND TRUTH

| Domain | Ground truth sources |
|--------|---------------------|
| **Code** | Tests, type system, runtime traces, spec requirements |
| **Architecture** | Requirements docs, existing patterns, constraints, NFRs |
| **Data** | Production schema, existing data contracts, validation rules, data already in the field (old records, files, messages written by earlier versions) |
| **Documentation** | Actual codebase, current API or interface, the running software, version history |
| **Tests** | Production code, requirements, coverage reports, CI results, production configuration and runtime (to tell a real pass from a test-environment artifact) |
| **Analysis** | Source material, original data, cited references, actual codebase |
| **UX** | The approved mock-up, the design system and the project's own guidelines, the platform's guidelines, and WCAG 2.2 where it applies |

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
**UX:** "The hint text is readable in dark mode" / "Every menu entry can be reached with the controller" / "The German labels fit at the narrowest supported width"

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

## Step 1c: PRE-CODE VALIDATION (any artifact that proposes work not yet done)

A plan, a spec, an ADR or an analysis that recommends work can be verified before anyone writes code, and that is when a wrong assumption is cheapest. Classify every claim of it by the evidence behind it (at quick depth, only the top 3 highest-risk claims, ranked as in Step 3c):

| Class | Meaning | What to suggest |
|-------|---------|-----------------|
| **Evidenced** | the evidence already exists: code, tests, a recorded response, or a measurement that you can cite (a result someone only reports counts once you have read the result itself: the output, the log, the measurement) | nothing; cite it |
| **Technical assumption** | it depends on something nobody has observed yet: an external API, a library, performance, a file format, a device | a **spike** before the code |
| **User-expectation assumption** | it depends on what the users want, expect or will understand | a **mock-up** before the code (below) |

The class feeds the confidence: an assumption of either kind is a claim only a run or the users can decide, so it scores at most 79 (Run-only constraint, Step 4) until its spike or mock-up is done. An assumption the plan presents as settled fact goes in FAIL as a preventive measure, with its open question as the scenario; one the plan already marks as open stays only in PRE-CODE VALIDATION.

**A spike** is a small, throwaway experiment that answers one question. Each suggested spike states:
1. **The question**, one per spike (e.g. "does the API honour `updated_since`?").
2. **The measurement that decides it**: what will be run or read, and which result answers yes or no.
3. **The decision rule**, with all three branches: the result that means do, the result that means don't, and the result that means postpone, with the conditions that would reopen it.
4. **The throwaway constraint**: no production code, and no writes to real systems (no real orders, payments, messages or records). A spike that needs a real system uses read-only calls, test credentials, a sandbox or recorded responses. A proposed spike that writes to a real system is a demonstrated defect of the plan, in FAIL.

Typical adversarial questions for a spike on an external system: does it silently ignore a parameter it does not support? Does the documentation match the real responses? What are the limits of quantity, page size, rate and format? What does it return when nothing matches?

Design each suggested spike so that its report will pass the spike checklist (Step 3, Analysis): declared sample, held-out data when anything is tuned, reproducible bench. A spike that could run now (a read-only call, a recorded response) is also a row of PROPOSED EXECUTABLE CHECKS. The verifier runs it only with approved execution, and writes one only with consent to write (Execution and consent).

**A mock-up** (a picture of the proposed interface for users, not a test double) answers what the users expect before anyone builds it. The verifier suggests one; it does not make it. Each suggested mock-up states:
1. **The question** the users must answer (e.g. "do managers need the totals per status, or only the list?").
2. **The form** that fits the software: images, a static page, a clickable prototype, screens of a native app or a game, sample output of a command-line tool.
3. **Today next to Proposed**: the current screen or output beside the new one, so the change is visible, when a current one exists.
4. **Alternatives A and B** when the choice is open, with what each one favours.
5. **Real content and states**: long names, empty lists, many rows, errors, a translation longer than the original.
6. **Who approves it, and the link**: the mock-up is approved by the users or their representative before development, and the link between the request, the mock-up and the change is written down.

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

For each project invariant found in Step 0b, decide whether the artifact touches it. For code, data and interface changes (UX: screens, styles, menus): the change reads, writes, or bypasses the data, flow, or component the invariant is about. For plans, specs, docs, and analyses: the artifact proposes, describes, or concludes something about that subject. For each one it touches:
1. **Name the mechanism** that enforces it, with its location: a test (file and test name), a type, a schema or data constraint, a runtime assertion, a static check or lint rule, a hardware interlock.
2. **Check that it bites on the changed path:** it runs there, and it would fail (reject, raise, refuse, block) if the invariant were broken there. Ask: "if I broke the invariant on the new path, would this stop it?" A test of the old entry point, a test that runs the path without asserting the invariant, or an assertion compiled out of production builds does not count. Tests and assertions also fall under the test-environment constraint (Step 4).
3. **Touched with nothing that bites** → FAIL, category *missing completeness*, typed as a preventive measure unless you traced an actual violation (then a demonstrated defect). If you could not trace whether the system currently respects the invariant on that path, add a row to HYPOTHESES for that question.
4. **Plans, specs, docs, analyses and mock-ups** have no changed path, so item 3 does not apply to them as written. Instead: none of them may contradict a touched invariant (contradiction → FAIL, typed as a demonstrated defect: the contradiction is in the text). A plan or spec that changes the invariant's subject must also say what will enforce it on the new path; if it does not say → FAIL of missing completeness, typed as a preventive measure. A doc or analysis that only restates or relies on the invariant passes if it states it correctly.

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

**Spike and prototype reports** (Analysis): a spike is an analysis, so verify it before a decision rests on it. Check each point that applies (a held-out set and sample limits only when something was sampled or tuned), and report the ones that fail, typed as in the Finding format (tuning on the evaluation data is a demonstrated defect of the report; a missing seed is a preventive measure):
- **The question** is explicit, one per spike, and the result answers that question, not a neighbouring one.
- **The deciding measurement and the decision rule were fixed before the result** (Step 1c): which number answers yes or no, and what means do, don't or postpone. A threshold chosen after seeing the result is not a test.
- **The bench is reproducible**: data, seed, versions of tools and libraries, machine, and the exact command or steps.
- **The sample's limits are declared**: how much data, from where and when, confounding variables, synthetic or hand-picked data.
- **A held-out set**: data kept aside for the evaluation and never used to tune thresholds, rules or prompts. A result measured on the data it was tuned on is not evidence of how it generalises.
- **The numbers support the conclusion**: good and bad cases shown, not just an average; the errors that look plausible but are wrong are counted, since they are the costly ones.
- **The decision is written** and follows the rule fixed before the spike, if there was one: do, don't, or postpone. A postponement names the conditions that would reopen it.
- **The throwaway constraint held**: no spike code went into production, and the spike did not write to a real system. Code that should survive is rewritten for production, not promoted. If it used personal data, say where that data is now and whether it should be deleted.

A spike report that recommends work ("build it") is also checked by Step 1c: the checklist verifies the evidence, Step 1c classifies what the recommendation still assumes.

**UX:** adapt each point to the kind of interface (web, native app, game, command-line or terminal); WCAG 2.2 is the reference where it applies. Check, in every target format (sizes, input methods, themes):
- **Render**: the layout holds in each format; nothing is cut off or off screen; navigation stays reachable.
- **Contrast**: text at least 4.5:1 (3:1 for large text), graphics and the boundaries of controls at least 3:1, in every theme including dark mode. Compute the ratio from the actual colours; do not estimate it.
- **Legibility**: text size for the viewing distance, line length, heading hierarchy; zoom to 200% and reflow at 320 px wide without loss of content, where the platform has them.
- **Targets**: the size of what is touched or clicked, against the project's threshold or WCAG 2.5.8.
- **Keyboard, controller and focus**: everything reachable with each supported input, the focus visible from the viewing distance, the order logical.
- **Real content**: long names, translations longer than the original, empty values, many items.
- **States**: empty, loading, error, success; error messages understandable and placed next to what caused them.
- **Basic accessibility**: labels on fields, text alternatives for images, an accessible name for icon-only buttons.
- **Motion and perceived speed**: reduced-motion preferences respected; time to the first useful content on a slow network or device.
- **Sensitive data**: no secrets or personal data visible on screen, in screenshots or recordings.

**UX check round.** Suggest a check of the main screens in the project's target formats, using its interface tests if it has any. It is a run, so it is proposed under Execution and consent, with the screens, formats and inputs it covers. A measured fact (a width, a colour pair) can be computed by reasoning; how the screen really renders cannot.

**Alternative interfaces.** For each weak point found, suggest one or two alternatives with a short comparison: what each improves, what it makes worse, and its cost. The verifier describes the alternatives; a mock-up of them follows Step 1c.

**Agent meta-verification** (when reviewing AI agent output, per [AuditBench](https://alignment.anthropic.com/2026/auditbench/)): Sycophantic deference, hidden agenda, anchoring bias, confabulated confidence, premature convergence, evidence cherry-picking.

## Step 3b: HIDDEN BEHAVIOR PROBING

> Based on [AuditBench](https://alignment.anthropic.com/2026/auditbench/) — hidden behaviors don't confess when asked directly.

1. **Indirect probing** — trace what *actually happens*, don't trust the interface
2. **Scaffolded probing** — use the output of one check as input to the next
3. **Cross-reference probing** — check if what the code *claims* matches what it *does*
4. **Absence probing** — look for what's NOT there: missing error handling, validation, tests, logging

At quick depth probe only the top 3 highest-risk claims; at standard depth, the claims Step 3c ranks as high risk; at deep depth, every claim.

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

**Forced variety rule:** at standard depth each run must use at least 3 different techniques, and never the same technique twice on the same claim. Quick depth skips this step; deep depth applies all four techniques to each of the highest-risk claims that passed (see Intake).

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

## Step 3e: EXECUTABLE FALSIFICATION (only with approved execution)

When the user has approved running (and, where needed, writing) tests, turn each suspicion that a test can decide into a test, at any depth, for the claims that depth verifies. Without that approval, the same tests are only proposed (PROPOSED EXECUTABLE CHECKS).

1. **Hypothesis first.** State the suspected defect and the observable effect before writing the test.
2. **Test that reproduces it.** The test exercises the suspected path and asserts the suspected effect, with an expected value taken from the spec or the ground truth, not from the code under test. Writing it needs consent to write (Execution and consent, rule 2).
3. **Run it on the current version.**
   - **Red**: check first that the red is not a test-environment artifact or a wrong expectation in the test (Step 2b, *false red*; Step 4). If the expectation was wrong, fix the test, run it again and report the discarded run too. Otherwise the defect is **demonstrated**. Propose the fix, or apply it if changing the code was approved, then run the test again: it must turn green.
   - **Green with no change**: the hypothesis is **falsified**. Say so, keep the test as a regression guard, and propose no fix. It is fully falsified only if the test could have failed (Finding format, *Falsified hypothesis, in full*); otherwise it is conditionally falsified.
4. **Fix only what a test showed broken.** A suspicion no test confirmed gets no fix; call any safeguard a preventive measure.
5. **Both outcomes when a test is run on the previous version** (the parent commit, or the fix reverted). Running on the parent is covered by consent to run there, in a separate copy of the repository (a separate worktree or export of that version); checking it out, or reverting the fix, in the user's working copy is writing and needs its own consent. Read the four cells:
   - red before, green after: the test covers the defect and proves the fix;
   - green before and after: the test does not prove the fix, and the defect could come back with no test failing. A claim that the fix works, resting on this test, cannot score above 79. Propose a test that is red before the fix;
   - red after, whatever before: the fix does not work, or broke something; go back to rule 3.

Record every test in EXECUTED TESTS: the hypothesis, the test, where it ran, the result, and the finding type. The verdict goes in its own table (FAIL or FALSIFIED HYPOTHESES), and an approved proposed check points to its EXECUTED TESTS row in its Status.

### Mutation probe (on request, any domain where tests cover the code)

Measures whether the tests protect the changed code, not only whether they execute it. It runs only when the user asked for mutation (in the request or as an approved check), at any depth. Otherwise propose it in PROPOSED EXECUTABLE CHECKS, stating its scope (the changed lines), its cost, and that the code is mutated and then restored, since it writes and is slow.

1. **Cost first.** State the cost in observable terms: lines in scope, number of mutants, and which tests run for each. Approval of the probe on a scope approves that size; wait for confirmation only when the request named no scope or the probe would go beyond it. Unattended (Intake rule 7): run only if the instructions approved the probe and its scope; otherwise report the cost and leave it proposed.
2. **Scope: the changed lines**, when the tool allows it.
3. **Tool or hand mutations.** Use the project's mutation tool for its language if it is already installed; installing one needs consent. Otherwise apply 3-5 mutations by hand on the highest-risk changed lines (Step 3c: blast radius × probability), such as a flipped comparison, a changed boundary constant or a removed call, and run only the tests that cover each one.
4. **Mutate a separate copy** of the repository and restore it after every mutant; mutating the user's working copy needs its own consent. Confirm at the end that the user's working copy is unchanged (Execution and consent: mutating is writing, covered only by the approval of the probe).
5. **Read every survivor.** First check that the tests covering it actually ran (not skipped, excluded or run with another configuration): if they did not, the mutant is **not measured**, not a survivor (test-environment constraint, Step 4). Each measured survivor is a **missing test** (no test checks that behavior) or **superfluous code** (nothing depends on it); call it **equivalent** only when the mutant cannot change any observable behavior, and give the reason for each one.
6. **Survivors are findings.** A missing test goes in FAIL as a demonstrated defect of the tests, superfluous code as a demonstrated defect of the code, each with the mutant as its evidence; an equivalent mutant is not a finding. Removing superfluous code is only proposed. The test that would kill a survivor is the fix of its FAIL row, not a Step 3e hypothesis: with consent to write, write it and run it; it must be red on the mutant and green on the code. Record both runs in EXECUTED TESTS.
7. **A perfect score is suspicious** until you have seen why the mutants died: a test runner whose output the tool cannot read, a crash in setup, or a timeout can all count as kills. Look at the log for a sample of kills.
8. **Declare what was not measured.** Mutants skipped, timed out or not measured are excluded from the score: say how many, and that the score covers only the rest.

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

**Run-only constraint:** a claim that only a run can decide (a query plan, a measured performance, the behavior of an external system, a test result) CANNOT score above 79 until that run is done or its result is supplied, however well the code is traced. The same holds for a claim only the users can decide (a user-expectation assumption, Step 1c): at most 79 until the users or their representative approve a mock-up; a report that users want it does not lift the cap.

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
## INTAKE
[Target, depth, scope, execution mode used; which were defaults; how to change them]

## VERIFICATION DOMAIN
[Code | Architecture | Data | Documentation | Tests | Analysis | UX]

## GROUND TRUTH
[Sources used for verification]

## INVARIANTS
[Where you looked; how many found; "none found" is a valid answer. List only the touched ones]
| # | Invariant | Source | Touched by | Enforced by (file:line / test name) | Bites on changed path? (code, data, UX) / Respected? (plans, specs, docs, analyses, mock-ups) |
|---|-----------|--------|------------|-------------------------------------|------------------------|

## DECOMPOSED CLAIMS
1. [Claim text] — Mode: [Deductive/Inductive/Abductive]
...

## PRE-CODE VALIDATION (artifacts that propose work not yet done; omit otherwise)
[With many claims, list evidenced ones by number only]
| # | Claim | Class | Evidence; or spike (question, measurement, decision rule); or mock-up (question, form, alternatives, approver) |
|---|-------|-------|--------------------------------------------------------------|

## FAILURE CATEGORIES IDENTIFIED
| Category | Instances | Files affected |
|----------|-----------|---------------|

## OUT OF SCOPE (listed, not verified; omit if none)
[Occurrences of the same pattern found outside the scope, with file:line]

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

## EXECUTED TESTS (Step 3e and mutation probe, only with approved execution)
| # | Hypothesis or survivor | Test | Ran on (one row per run) | Result | Finding type |
|---|-----------|------|--------|--------|--------------|

## MUTATION PROBE (only when the user asked for it)
[Scope, tool or hand mutations, mutants generated, killed, survived, skipped or timed out, score and what it excludes]
| # | File:Line | Mutator | Outcome | Reason | Test that would kill it |
|---|-----------|---------|---------|--------|------------------------|
[Outcome: missing test, superfluous code, equivalent, or not measured. Missing tests and superfluous code also go in FAIL]

## STRESS TEST RESULTS
[At quick depth write "Skipped (quick depth)" instead of the table]
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
- Domain: [Code/Architecture/Data/Documentation/Tests/Analysis/UX]
- Claims: X verified, Y in FAIL (defects and preventive measures), Z falsified
- Survived: X/Y stress tests passed
- Failure categories: N systemic patterns
- Invariants: N found, M touched, K enforced by a mechanism that bites on the changed path (code, data, UX) or respected (plans, specs, docs, analyses, mock-ups)
- Hypotheses: N requiring further investigation
- Hidden behaviors: N detected
- Findings by type: N demonstrated defects, M preventive measures, K falsified hypotheses (J of them conditionally)
- Critical issues: N demonstrated defects of critical severity (preventive measures of critical severity listed separately: M)
- Executed: N tests run (red, green, on which versions); mutation score and survivors, if the probe ran, with what it excludes
- Proposed: N checks and M writes awaiting an answer
- Recommendation: [trust adjustment or approval]

## PROPOSED EXECUTABLE CHECKS
[One row for every claim scored below 80 that running something would decide, and for every other run the verifier wants to do (an untrusted link, a Step 3e test, the mutation probe): the Claim column says what the run would decide. Omit the table if there is none]
| # | Claim | Confidence now | Check (command, test or query) | Confirms if | Refutes if | Cost and side effects | Status |
|---|-------|----------------|--------------------------------|-------------|------------|-----------------------|--------|
[Cost in observable terms: what runs, where, whether it reads or writes, what it touches. Status: proposed, or approved and run with its result. After approved runs, issue the report again: each claim a run decided moves to PASS or FAIL with the command and its output]
Proposed writes: [each test, fix or doc update (Step 5) the verifier wants to write, with the file and the change. Omit if none]
[End the report with one question covering the proposed checks and writes: nothing runs or is written without an answer. Drop the question when nothing is left proposed]
```

For multi-domain verification, repeat per domain with a CROSS-DOMAIN SUMMARY at the end, then one PROPOSED EXECUTABLE CHECKS section for all domains, so the report ends with a single question. INTAKE appears once, at the top.

## Step 5: PROJECT DISCOVERY UPDATE

Before closing the report, check for: `TODO.md`, `SPEC.md`, `PLAN.md`, `CHANGELOG.md`, `ADR/`, `.claude/` docs. If findings are relevant, **propose** the updates under Proposed writes in the closing section — do NOT write directly. Wait for explicit confirmation of those writes (Execution and consent, rules 1 and 2), even when the request asked to update the docs.

## Trust Scoring (Optional)

If the project uses `.claude/agent-trust.json` (writing it needs consent, Execution and consent, rule 1): demonstrated defect found → author -1 (preventive measures and falsified hypotheses don't count), false positive → verifier -1, 3 clean reviews (no demonstrated defect) → author +1.

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
- **Don't ask what the request already says** — and don't start a large verification without stating its cost first
- **Don't skip ground truth** — without a reference, you can't verify anything
- **Don't ignore the project's own invariants** — a rule the project says must never break is the first thing a change can break silently; check what enforces it on the changed path
- **Don't run or write without consent** — propose checks, tests, fixes and doc updates; run or write only what the user approved, for this verification only
- **Don't stop at individual bugs** — abstract to failure categories and search for patterns
- **Don't trust the interface** — probe the actual behavior, not what the code advertises
- **Don't collect evidence without hypotheses** — every finding needs a conclusion
- **Don't claim absence without stating where you looked** — "X doesn't exist" requires citing what you checked
- **Don't report only problems** — stress tests that survive are equally valuable results
- **Don't call a risk a bug** — type every problem or suspicion you report: demonstrated defect, preventive measure, or falsified hypothesis
- **Don't use the same technique twice on the same claim** — forced variety prevents analytical tunnel vision
