# Changelog

The newest version comes first. The version is the same in the skill's frontmatter, the README badge, `.claude-plugin/plugin.json` and the first entry below; `scripts/check.py` fails if they differ.

## 4.1 - 2026-10-21

Validation before code, spike reports and UX (phase C, PR #26; release, #14).

- **Pre-code validation (Step 1c).** Every claim of a plan, spec, ADR or analysis that proposes work is *evidenced*, a *technical assumption* or a *user-expectation assumption*. Assumptions stay below 80 until a spike or a mock-up decides them; an assumption presented as fact is a preventive measure in FAIL. A suggested spike has a question, the measurement that decides it, a three-branch decision rule (do, don't, defer with the conditions to reopen) and a throwaway constraint. A suggested mock-up has the question for users, today next to the proposal, A/B alternatives, real content and states, and who approves it. New report section PRE-CODE VALIDATION.
- **Spike reports** are verified with a checklist in the Analysis domain: question and decision rule fixed before the result, reproducible bench, sample limits, held-out data when tuning, numbers that support the conclusion, the throwaway constraint respected.
- **UX is the seventh domain.** A change made only of interface code, with no logic and no text change, is UX. A check round in every target format (render, contrast computed from the actual colours, legibility, targets, keyboard or controller and focus, real content, states, basic accessibility, motion, sensitive data), proposed with consent; every weak point gets one or two alternatives with what improves, what gets worse and the cost.
- **Eval facts are executed** (#24): `scripts/check_facts.py` runs one file per eval with computable facts (Python, Rust, TypeScript); each file carries the hash of its eval's prompt; `check.py` requires a file or a stated reason for every eval that states facts.
- **Evals in Rust and TypeScript** (#25).
- **Release** (#14): `.claude-plugin/plugin.json` declares the version, repository, licence and keywords; `check.py` also checks the manifest and this changelog against the skill's version; the README lists the mutation tools by language, verified on their official documentation.

## 4.0 - 2026-10-21

Intake, execution with consent, executable falsification, mutation probe (phase B, PR #23).

- **Intake** before Step 0: target, depth (quick, standard, deep), scope, execution mode. Large requests stop with a cost estimate in files, domains and claims, never in time, and questions with defaults; all others start at once with the defaults stated in one line. Unattended runs use the defaults.
- **Execution and consent.** Reading is not running. Nothing is run or written without consent; consent covers only what it names and lasts for one verification. The report ends with PROPOSED EXECUTABLE CHECKS (check, what confirms it, what refutes it, cost) and one closing question.
- **Executable falsification (Step 3e)**, with approved execution: hypothesis, test with the expected value from the spec, run. Red is a demonstrated defect once a test-environment artifact is excluded; green without changes is a falsified hypothesis and the test stays as a regression. Before and after the fix: four cells read; green on both means the test does not prove the fix.
- **Mutation probe**, on request: changed lines, the language's tool if installed or 3-5 hand mutations, code restored. Every measured survivor is a missing test, superfluous code or a motivated equivalent; a 100% score is suspicious; skipped and unmeasured mutants are declared.

## 3.6 - 2026-10-21

Test-environment artifacts, invariants, typed findings, agnostic text (phase A, PR #20), plus the repository's own checks (PR #22).

- **Test-environment artifact**, a failure category: "would this result be the same in production?". A claim resting on a test result cannot score above 79 until checked against production.
- **Project invariants** as ground truth: found in Step 0b (the report says where it looked), each touched invariant needs a mechanism that bites on the changed path. New INVARIANTS section.
- **Typed findings**: demonstrated defect, preventive measure, falsified hypothesis (full, or conditional when the check could not have failed). New FALSIFIED HYPOTHESES table; critical issues and trust scoring count only demonstrated defects.
- **Technology-agnostic text**: no language keywords, no OO assumption, examples from varied software.
- **Repository checks** (`scripts/check.py`, pre-commit hook): evals format, version, private terms, neutral wording, table shape.

## 3.5 and earlier

See the git history.
