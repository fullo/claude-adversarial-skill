[![Skill Version](https://img.shields.io/badge/skill-v2.0-blue)](skills/adversarial-verify/SKILL.md)
[![Skills](https://img.shields.io/badge/skills-1-green)](skills/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/format-agentskills.io-purple)](https://agentskills.io/)

# Claude Adversarial Verification Skill

A Claude Code skill that performs rigorous adversarial verification using **Chain-of-Verification (CoV)** methodology across code, architecture, data, and analysis.

## What it does

When invoked, this skill launches a skeptical verifier agent that:

1. **Identifies** what needs verification — code, architecture, data, or analysis
2. **Gathers artifacts** — the actual outputs to verify
3. **Establishes ground truth** — what to verify against
4. **Decomposes** artifacts into individual verifiable claims
5. **Generates adversarial questions** for each claim ("what would make this fail?")
6. **Independently verifies** each claim by tracing actual paths
7. **Reports findings** with evidence, references, and concrete fix suggestions
8. **Proposes project doc updates** — TODO.md, SPEC.md, PLAN.md (with user confirmation)

## Verification Domains

| Domain | What it verifies | Ground truth |
|--------|-----------------|--------------|
| **Code** | Source changes, logic, behavior | Tests, type system, spec |
| **Architecture** | Design decisions, spec coverage | Requirements, constraints, patterns |
| **Data** | Schemas, migrations, contracts | Production schema, validation rules |
| **Analysis** | Agent outputs, reports, docs | Source material, cited references |

## Install

Copy the skill directory:

```bash
cp -r skills/adversarial-verify ~/.claude/skills/
```

Or clone as plugin:

```bash
git clone https://github.com/fullo/claude-adversarial-skill.git
cp -r claude-adversarial-skill/skills/adversarial-verify ~/.claude/skills/
```

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
```

## What it catches

### Code
- **Silent data corruption** — values that look correct but aren't
- **Logic flaws** — code that passes simple tests but fails edge cases
- **Initialization order bugs** — field A used before field B is set
- **Concurrent modification** — adding to a list while iterating it
- **State leaks** — data persisting across frames/calls when it shouldn't
- **Boundary conditions** — off-by-one, coordinate system errors
- **Resource exhaustion** — unbounded lists, missing cleanup

### Architecture
- **Spec drift** — implementation diverges from SPEC.md
- **Missing constraints** — PLAN.md doesn't address known edge cases
- **Over-engineering** — abstraction without justification
- **Dependency risk** — new deps without evaluation
- **Breaking changes** — API contract violations

### Data
- **Schema inconsistency** — migration doesn't match model
- **Data loss risk** — destructive migration without backup
- **Constraint gaps** — missing NOT NULL, FK, uniqueness
- **Backward compat** — old code reading new schema

### Analysis
- **Hallucinated facts** — claims without traceable source
- **Stale references** — citing removed/renamed code
- **Logical leaps** — conclusion doesn't follow from evidence
- **Confirmation bias** — only supporting evidence presented

## Trust Integration

Optionally integrates with a multi-agent trust scoring system:

- Each confirmed bug: **-1 trust** to the agent that wrote it
- Each false positive: **-1 trust** to the verifier
- Every 3 clean reviews: **+1 trust** to the developer

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

## Origin

Extracted from the [Rainbow Climb](https://github.com/fullo/rainbow-climb) game development project, where it was used to catch critical bugs including:

- Timer-based continuous fire (shootTimer never reset)
- Patrol boundary flip-flop (velocity inverted every frame)
- Missing collision bounds (collectibles had 0x0 rectangles)
- Shield absorption blocking subsequent projectile checks

## License

MIT
