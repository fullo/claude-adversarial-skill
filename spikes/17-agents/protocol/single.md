# Mode A: one agent

One agent, one context, the skill as published at the base commit. Nothing else.

## Setup of a run

- A fresh session for every run: no memory of another run, of the answer key or of this folder.
- The agent can read the case tree (`DIR/<case>`) and the skill's folder at the base commit
  (`DIR/base/skills/adversarial-verify`). It cannot read `DIR/keys`, `DIR/base` outside the
  skill's folder, or this repository.
- Model, effort and tools are the same in both modes and are written in `results/runs.csv`.

## Prompt

Replace `{TREE}`, `{FILES}` and `{OUT}`. `{FILES}` is the scope of the case, one path per line.

```
Use the adversarial-verify skill in {SKILL}.

Verify these files of the project in {TREE}:
{FILES}

Target: every domain the skill detects in these files. Depth: standard. Scope: the whole of
these files (there is no diff and no version history). Execution mode: reasoning only, run
nothing. I accept the cost: do not stop to ask.

You may read any other file of {TREE} to establish ground truth.

Write the complete report, in the skill's Output Format, to {OUT}/report.md. Cite every
location as path:line, with the path relative to {TREE}.
```

## What is recorded

`report.md`, and from the harness: total tokens of the run, the largest context the agent
reached, wall time.
