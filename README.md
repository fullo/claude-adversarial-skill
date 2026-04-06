[![Skill Version](https://img.shields.io/badge/skill-v1.0-blue)](SKILL.md)
[![Skills](https://img.shields.io/badge/skills-1-green)](SKILL.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/format-agentskills.io-purple)](https://agentskills.io/)

# Claude Adversarial Verification Skill

A Claude Code skill that performs rigorous adversarial code review using **Chain-of-Verification (CoV)** methodology.

## What it does

When invoked, this skill launches a skeptical verifier agent that:

1. **Decomposes** code changes into individual verifiable claims
2. **Generates adversarial questions** for each claim ("what would make this fail?")
3. **Independently verifies** each claim by tracing actual code paths
4. **Reports findings** with evidence, line numbers, and concrete fix suggestions

## Install

Copy the skill file:

```bash
cp SKILL.md ~/.claude/skills/adversarial-verify.md
```

Or clone as plugin:

```bash
git clone https://github.com/fullo/claude-adversarial-skill.git ~/.claude/skills/adversarial-verify
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
```

## What it catches

The skill is designed to find **pernicious** bugs that surface-level reviews miss:

- **Silent data corruption** — values that look correct but aren't
- **Logic flaws** — code that passes simple tests but fails edge cases
- **Initialization order bugs** — field A used before field B is set
- **Concurrent modification** — adding to a list while iterating it
- **State leaks** — data persisting across frames/calls when it shouldn't
- **Boundary conditions** — off-by-one, coordinate system errors
- **Resource exhaustion** — unbounded lists, missing cleanup

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
