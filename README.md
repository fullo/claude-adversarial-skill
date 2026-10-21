[![Skill Version](https://img.shields.io/badge/skill-v3.6-blue)](skills/adversarial-verify/SKILL.md)
[![Skills](https://img.shields.io/badge/skills-1-green)](skills/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/format-agentskills.io-purple)](https://agentskills.io/)

# Claude Adversarial Verification Skill

A Claude Code skill that performs rigorous adversarial verification across code, architecture, data, documentation, tests, and analysis using **Chain-of-Verification (CoV)** enhanced with **abstractive red-teaming**, **hidden behavior probing**, **stress techniques**, and **tri-modal reasoning**.

## What it does

When invoked, this skill launches a skeptical verifier agent that follows a structured protocol:

**Intake:**
- **Ask before starting** — target, depth (quick, standard, deep), scope and execution mode; requests start at once with declared defaults, the target is asked only when unclear, large ones first get a cost estimate in files, domains and claims
- **Execution with consent** — by default nothing is run: the report ends with proposed executable checks (what would confirm, what would refute, cost) and asks; only approved checks run, for that verification only, and writing a test or a fix needs its own approval

**Pre-verification (Steps 0–0b):**
- **Identify** what needs verification — code, architecture, data, documentation, tests, or analysis
- **Gather artifacts** — the actual outputs to verify
- **Establish ground truth** — what to verify against
- **Find the project's invariants** — rules that must never break, or say where you looked if there are none

**Chain-of-Verification (Steps 1–2b):**
- **Decompose** artifacts into individual verifiable claims
- **Classify reasoning mode** — deductive, inductive, or abductive per claim
- **Generate adversarial questions** for each claim ("what would make this fail?")
- **Abstract to failure categories** — find patterns, not just individual bugs

**Deep Verification (Steps 3–3d):**
- **Independently verify** each claim by tracing actual paths
- **Check invariants touched** — whatever enforces each one (test, type, constraint, assertion, interlock) must run on the changed path and fail if the invariant is broken there
- **Probe for hidden behaviors** — detect what the code doesn't advertise
- **Apply adversarial scaffold** — suspicion modeling, attack selection, subtlety detection
- **Stress test** — Existence Question, Scale Shift, Time Travel, Requirement Inversion

**Reporting (Steps 4–5):**
- **Report findings** with reasoning-aware confidence scoring and anti-fabrication discipline
- **Survived verdicts** — stress tests that hold are as valuable as those that break
- **Hypotheses** — abductive findings reported separately, with alternatives and tests
- **Propose project doc updates** — TODO.md, SPEC.md, PLAN.md (with user confirmation)

## Verification Domains

| Domain | What it verifies | Ground truth |
|--------|-----------------|--------------|
| **Code** | Source changes, logic, behavior | Tests, type system, spec |
| **Architecture** | Design decisions, spec coverage | Requirements, constraints, patterns |
| **Data** | Schemas, migrations, file and message formats, contracts | Production schema, validation rules, data already in the field |
| **Documentation** | Technical, process, and user-facing docs | Actual codebase, current API or interface, version history |
| **Tests** | Test suite integrity and honesty | Production code, requirements, coverage reports, production configuration |
| **Analysis** | Agent outputs, reports, docs | Source material, cited references |

## Techniques

### Abstractive Red-Teaming
Instead of finding individual bugs, identifies **failure categories** — general patterns that produce bugs repeatedly. Searches the entire codebase for instances of the same pattern (frequency assumptions, implicit ordering, stale state, missing completeness, silent fallthrough, assumed environment, test-environment artifact).

### Hidden Behavior Probing
Detects behaviors the code doesn't advertise using four probing strategies: indirect probing (trace actual execution), scaffolded probing (chain findings), cross-reference probing (claims vs reality), and absence probing (what's NOT there).

### Modular Adversarial Scaffold
Decomposes the adversarial process into five modules: suspicion modeling (what would a reviewer miss?), attack selection (highest-risk claims first), plan synthesis (multi-step trace chains), execution (actually read the code), and subtlety detection (code that hides complexity).

### Stress Techniques
Inspired by Principles of Chaos Engineering, adapted for review. Four techniques with forced variety (at standard depth minimum 3 per run, never twice on the same claim; none at quick depth, all four on the top 3 risks at deep depth): **Existence Question** (should this exist at all?), **Scale Shift** (what at 10x? at zero?), **Time Travel** (what in 6 months?), **Requirement Inversion** (what if the opposite?). Produces **Survived: yes/no** verdicts — knowing what's robust is as valuable as knowing what's fragile.

### Tri-Modal Reasoning
Each claim is classified by reasoning mode — **deductive** (verify against ground truth), **inductive** (generalize from 3+ instances), or **abductive** (generate best explanation from observations). Abductive findings are reported as hypotheses with alternative explanations and proposed tests, never as verified facts.

### Anti-Fabrication Discipline
Before claiming something doesn't exist, you must state where you looked. Every finding is typed as a demonstrated defect, a preventive measure, or a falsified hypothesis (said plainly, only if the check could have failed — otherwise conditionally falsified — kept as a regression check, limited to the paths it covered). Confidence scoring is tied to reasoning mode: deductive (80-100, source cited), inductive (60-79, 3+ instances), abductive (40-59, hypothesis with alternatives). No invariants found is reported as such, with where you looked, never filled with invented ones. Hard constraint: no score above 79 without citing specific file/line/doc. Test-environment constraint: no score above 79 for a claim resting on a test result until that result is checked against production.

### Agent Meta-Verification
When reviewing output from another AI agent, checks for: sycophantic deference, hidden agenda, anchoring bias, confabulated confidence, premature convergence, and evidence cherry-picking.

## Install

Copy the skill directory:

```bash
cp -r skills/adversarial-verify ~/.claude/skills/
```

Or clone and copy:

```bash
git clone https://github.com/fullo/claude-adversarial-skill.git
cp -r claude-adversarial-skill/skills/adversarial-verify ~/.claude/skills/
```

Or install from the marketplace (recommended):

```bash
# Add the marketplace (once)
claude plugin marketplace add fullo/claude-plugins-marketplace

# Install the plugin
claude plugin install adversarial-verify@fullo-plugins
```

## Update

```bash
claude plugin update adversarial-verify@fullo-plugins
```

The plugin system uses git commit hashes as versions. There is no automatic update notification: run the command above periodically to stay current.

## Usage

In Claude Code, type:

```
/adversarial-verify
```

Or ask naturally:

```
"run an adversarial review on my recent changes"
"CoV check the last commit"
"verify this code with total skepticism"
"verify the PLAN.md against the SPEC.md"
"adversarial check on this migration"
"verify this agent's analysis report"
"look for systemic failure patterns in the codebase"
"probe this function for hidden behaviors"
"verify the README matches the actual install process"
"verify the tests actually test what they claim"
"stress test the auth module"
"what happens at 10x scale?"
"check if the planning agent's output is biased"
```

## What it catches

### Code
- **Silent data corruption** — values that look correct but aren't
- **Logic flaws** — code that passes simple tests but fails edge cases
- **Initialization order bugs** — field A used before field B is set
- **Concurrent modification** — adding to a list while iterating it
- **State leaks** — data persisting across calls, requests or frames when it shouldn't
- **Timing dependence** — behavior tied to frame rate, call rate, clock or latency
- **Boundary conditions** — off-by-one, tolerance windows
- **Unit and sign errors** — wrong direction, currency, unit or coordinate system
- **Resource exhaustion** — unbounded lists, missing cleanup

### Architecture
- **Spec drift** — implementation diverges from SPEC.md
- **Missing constraints** — PLAN.md doesn't address known edge cases
- **Over-engineering** — abstraction without justification
- **Dependency risk** — new deps without evaluation
- **Breaking changes** — API contract violations

### Data
- **Schema inconsistency** — a migration or format change doesn't match the code that reads and writes the data
- **Data loss risk** — a destructive migration or in-place upgrade without a backup or a way back
- **Constraint gaps** — missing required fields, references or uniqueness, whatever the storage or format enforces
- **Backward and forward compatibility** — old readers of new data, new readers of old records or files

### Documentation
- **Stale instructions** — install/setup steps that no longer work
- **API drift** — the documented interface (functions, commands, endpoints, messages) doesn't match the implementation
- **Missing docs** — new features with no documentation
- **Broken examples** — code samples that don't compile or run
- **Misleading error messages** — error text doesn't match error condition
- **Version mismatch** — docs reference old versions or deprecated features
- **Orphaned references** — links to removed files or dead URLs
- **UI copy drift** — help text diverges from actual behavior

### Tests
- **Tautological tests** — assertions that are always true regardless of code
- **Mock leakage** — tests verify the mock, not the actual behavior
- **Coverage lies** — line-covered but branch-untested code
- **Missing negative tests** — only happy path tested
- **Fragile assertions** — pass by coincidence (order, timing, locale)
- **Test-code drift** — tests written for a previous code version
- **Flaky indicators** — fixed sleeps, automatic retries, tests disabled or skipped
- **Test-environment artifacts** — the test passes (or fails) only because the test environment differs from production: defaults changed by fixtures, a different storage or concurrency model, permissive fakes, a different path into the code (emulator, direct call), different resources or dependencies, or a false red caused only by the test environment

### Analysis
- **Hallucinated facts** — claims without traceable source
- **Stale references** — citing removed/renamed code
- **Logical leaps** — conclusion doesn't follow from evidence
- **One-sided evidence** — only supporting data, contradicting findings omitted

### Agent Meta-Verification
- **Sycophantic deference** — agrees without challenging assumptions
- **Hidden agenda** — favors one approach without justification
- **Anchoring bias** — first evidence disproportionately shapes conclusions
- **Confabulated confidence** — high confidence on weak evidence
- **Premature convergence** — jumps to one hypothesis
- **Evidence cherry-picking** — selects only supporting evidence

## Repository checks

`scripts/check.py` enforces the repository's own invariants before a commit. It needs `python3` 3.8 or later and nothing else:

- **evals.json**: valid, the same four keys in every case, integer ids 1..n in file order, no empty prompt or assertion, and `[substance]`/`[format]` tags followed by text on every assertion from eval 21 on.
- **Version**: SKILL.md's frontmatter and every skill badge in the README agree.
- **Private names**: none of the configured terms appears in any tracked file's content or name. Matching ignores case, accents and how the parts of a term are joined (space, hyphen, underscore, line break, or nothing), and also covers JSON escapes and files that are not UTF-8. A term matches anywhere, also inside other words (`name` finds `NameLabs`, `name2026`, `names`). Prefix a term with `=` to match it only as a whole word, for common words that would otherwise cause false positives. Terms shorter than 4 characters give a warning. Put the list in the untracked file `.check-private-terms` (one term per line, `#` for comments) or in `CHECK_PRIVATE_TERMS` (comma-separated). The list is never committed, and any output line containing a term is masked. Not caught: a one-word term written as two words (a space or line break in the middle), UTF-16 files without a byte-order mark, and, for `=` terms, forms glued to other letters or digits.
- **Neutral wording**: technology-bound terms in SKILL.md and README.md are reported as warnings.
- **Tables**: every Markdown table row, with or without outer pipes, has as many cells as its header.

```bash
python3 scripts/check.py                    # working tree; says so if no private terms are set
python3 scripts/check.py --strict --staged  # what the next commit will contain; fails without private terms
python3 -m unittest scripts/test_check.py
ln -s ../../scripts/pre-commit .git/hooks/pre-commit   # runs --strict --staged before every commit
```

On Windows use `py -3 scripts/check.py`, and copy `scripts/pre-commit` into `.git/hooks/` instead of linking it (Git for Windows runs it with its own `sh`).

## Trust Integration

Optionally integrates with a multi-agent trust scoring system:

- Each demonstrated defect: **-1 trust** to the agent that wrote it (preventive measures and falsified hypotheses don't count)
- Each false positive: **-1 trust** to the verifier
- Every 3 clean reviews (no demonstrated defect): **+1 trust** to the developer

Track trust in `.claude/agent-trust.json`:

```json
{
  "agents": {
    "dev": { "trust": 7, "clean_commits": 0 },
    "test": { "trust": 7, "clean_commits": 0 }
  }
}
```

## Compatibility

Follows the [Agent Skills format](https://agentskills.io/) and works with Claude Code, Cursor, Windsurf, Cline and other compatible agents.

## References

- [Chain-of-Verification (CoV)](https://arxiv.org/abs/2309.11495) — Dhuliawala et al., 2023
- [Automated Auditing](https://alignment.anthropic.com/2025/automated-auditing/) — Anthropic, 2025
- [Abstractive Red-Teaming](https://alignment.anthropic.com/2026/abstractive-red-teaming/) — Anthropic, 2026
- [AuditBench](https://alignment.anthropic.com/2026/auditbench/) — Anthropic, 2026
- [Strengthening Red Teams](https://alignment.anthropic.com/2025/strengthening-red-teams/) — Anthropic, 2025
- [Principles of Chaos Engineering](https://principlesofchaos.org/)

## Origin

Extracted from the [Rainbow Climb](https://github.com/fullo/rainbow-climb) game development project, where it was used to catch critical bugs including:

- Timer-based continuous fire (shootTimer never reset)
- Patrol boundary flip-flop (velocity inverted every frame)
- Missing collision bounds (collectibles had 0x0 rectangles)
- Shield absorption blocking subsequent projectile checks

## License

MIT
