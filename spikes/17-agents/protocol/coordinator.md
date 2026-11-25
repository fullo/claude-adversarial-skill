# Mode B: a coordinator with agents

Throwaway protocol for the spike. It is not part of the skill and is not meant to be: if the
spike says "do", the protocol is written again for the skill (issue #18).

The same skill, model, effort, tools, case trees and final report format as mode A. What
changes is who reads what.

## Who runs what

Every agent of this mode, the coordinator included, is a launched agent on Sonnet (latest
version) at medium effort: the same as the single agent of mode A. The session that launches
the runs knows the answer key, so it never acts as the coordinator: it starts the coordinator
with the prompt below and scores what comes back. The coordinator needs to launch agents of
its own; whether the environment allows that is checked once, on the tuning case.

## Prompt of the coordinator

The coordinator gets this prompt and, as `{RUN}/PROTOCOL.md`, this file from "Roles" on.

```
You are the coordinator described in {RUN}/PROTOCOL.md. Read it and follow it exactly.

Skill: {SKILL}. Project: {TREE}. Files to verify:
{FILES}

Target: every domain the skill detects in these files. Depth: standard. Scope: the whole of
these files (there is no diff and no version history). Execution mode: reasoning only, run
nothing. I accept the cost: do not stop to ask. Read nothing outside {TREE}, {SKILL} and {RUN}.

Launch your agents on the sonnet model at medium effort. If you cannot launch agents here,
do not do the verification yourself: write what happened to {OUT}/CANNOT_LAUNCH.txt and stop.

Save every brief to {OUT}/briefs/ as you sent it. Every agent writes its own return to
{OUT}/returns/<agent>.md and answers you with that path only: read the return from the file,
never copy it out yourself. Write the final report to {OUT}/report.md, citing every location as path:line
with the path relative to {TREE}. Then write {OUT}/log.md: each agent you launched (role,
files, rows returned, rows discarded) and every point where you departed from the protocol.
```

## Roles

- **Coordinator.** Does the intake, lists the files in scope, splits the work, writes the
  briefs, checks what comes back, assembles the report. It does not verify: it opens a file
  of the case only to look up a returned quote at the line the row names.
- **Domain agents.** One per domain the coordinator detects in the scope (Code, Tests,
  Documentation, Data...). When a domain's files exceed 60 kB, one agent per group of files
  that belong together (a module with its tests), never an arbitrary cut.
- **Independent verifier.** One agent that verifies again the 5 highest-risk claims
  (blast radius x probability), passed claims included. It gets the claim and its location,
  not the domain agent's reasoning or verdict, and reads the files freely.
- **Category agent.** After the first synthesis, one agent that takes the failure categories
  found so far and searches the whole scope for other instances of each.

## Brief of a domain agent

```
Use the adversarial-verify skill in {SKILL}.

Verify these files of the project in {TREE}, for the {DOMAIN} domain only:
{FILES}

Depth: standard. Scope: the whole of these files. Execution mode: reasoning only, run nothing.
Do not stop to ask. You may read any other file of {TREE} to establish ground truth. Read
nothing outside {TREE} and {SKILL}.

Return only these sections of the skill's Output Format, as tables, with path:line relative
to {TREE} and the quoted line in every row: DECOMPOSED CLAIMS, PASS, FAIL, HYPOTHESES,
HIDDEN BEHAVIORS DETECTED, FAILURE CATEGORIES IDENTIFIED. No summary, no recommendation.
Write them to {OUT}/returns/{DOMAIN}.md and answer with that path only.
```

The brief does not repeat the skill's rules and does not say what the coordinator expects
to find. The briefs of the independent verifier and of the category agent end in the same
way: the agent writes its return to {OUT}/returns/ and answers with the path. (On the tuning
case, a coordinator that copied a long return into a file by itself was stopped by the
model's safeguards, `reasoning_extraction`, and wrote no report.)

## What the coordinator does with a return

1. **Looks up every quote** at the line its row names (a search of the file). A row whose
   quote is not there is discarded and counted. A return with a discarded row is sent back
   once to its agent with the list of the discarded rows; what is still wrong is dropped.
2. **Sends the 5 highest-risk claims to the independent verifier.** Where the two disagree,
   the row goes in the report with the lower confidence and both verdicts in the Scenario.
3. **Runs the category agent** on the categories of step 1 and 2, and looks up its quotes
   in the same way.
4. **Assembles one report** in the skill's Output Format: one section per domain, the
   cross-domain summary, and a line that says how many rows came back, how many were
   discarded, how many the independent verifier confirmed or changed. A PASS above 80 whose
   quote was not looked up goes down to 79.

## What is recorded

`report.md`, every brief and every return, and from the harness: total tokens of all the
agents together, the largest context the **coordinator** reached, wall time.
