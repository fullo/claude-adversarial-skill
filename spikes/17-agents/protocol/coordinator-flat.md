# Mode F: the coordinator taken apart in steps

Used where a launched agent cannot launch agents of its own (found on 25 November 2026 in the
environment where the bench was built). The coordinator of mode B becomes four small agents
and one script; a dispatcher launches them in a fixed order and passes files, nothing else.

The dispatcher may know the answer key, so it takes no decision: it does not read the returns,
does not choose claims, does not write a word of the report. Every prompt below is used as it
is, with the paths filled in by `prepare.py`.

Written, not run: in that environment a launched agent cannot write its return to a file
either, so every return would have to be copied by hand by the dispatcher (results/pilot.md).
Where agents can write files the prompts below work as they are.

It is not mode B: there is no single coordinator whose context could be measured, and the
return is never sent back to its agent. What it shares with B: domain agents with the same
brief, the quotes looked up mechanically, an independent verifier on the 5 highest-risk
claims, a round on the failure categories, one report in the skill's format.

Every agent: Sonnet (latest version), medium effort, the same as mode A.

## Step 1: planner

```
Read {SKILL}/SKILL.md, only "Step 0: IDENTIFY" with its auto-detect list. The project is in
{TREE}; these are the files to verify:
{FILES}

List them with their sizes. Open a file only if its name does not tell its domain. Read
nothing outside {TREE} and {SKILL}.

Write {OUT}/plan.json: a JSON list where each item is
{"domain": one of the skill's seven domains, "files": [paths relative to {TREE}]}.
One item per domain you detect in these files. When the files of one domain are more than
60 kB together, split the domain into items of files that belong together (a module with its
tests), never an arbitrary cut. A file goes under each domain that verifies it.

Reply with one line: the number of items.
```

## Step 2: domain agent

One agent per item of `plan.json`, all launched together. `{N}` is the item's position,
`{DOMAIN}` its domain, `{ITEM_FILES}` its files.

```
Use the adversarial-verify skill in {SKILL}.

Verify these files of the project in {TREE}, for the {DOMAIN} domain only:
{ITEM_FILES}

Depth: standard. Scope: the whole of these files (there is no diff and no version history).
Execution mode: reasoning only, run nothing. Do not stop to ask. You may read any other file
of {TREE} to establish ground truth. Read nothing outside {TREE} and {SKILL}.

Write to {OUT}/returns/{N}-{DOMAIN}.md only these sections of the skill's Output Format, as
tables, with path:line relative to {TREE} and the quoted line in every row: DECOMPOSED
CLAIMS, PASS, FAIL, HYPOTHESES, HIDDEN BEHAVIORS DETECTED, FAILURE CATEGORIES IDENTIFIED.
No summary, no recommendation.

Reply with one line: how many rows the FAIL table has.
```

## Step 3: quote lookup (script)

`python3 lookup.py --tree {TREE} --out {OUT}/checked {OUT}/returns/*.md`

## Step 4: risk agent

```
The files in {OUT}/checked/ are the returns of verification agents about one project: tables
of claims (DECOMPOSED CLAIMS, PASS, FAIL, HYPOTHESES, HIDDEN BEHAVIORS DETECTED). Read them,
and in {SKILL}/SKILL.md only "Step 3c: ADVERSARIAL SCAFFOLD". Do not open the project's files.

Choose the 5 claims with the highest risk (blast radius x probability), passed claims
included.

Write {OUT}/risk.json: a JSON list of 5 items {"claim": the claim as one neutral sentence,
"location": "path:line"}. Leave out the verdict, the evidence and the confidence the agents
gave: whoever reads this file must not learn what they concluded.

Reply with one line: done.
```

## Step 5: independent verifier and category agent

Launched together.

```
Use the adversarial-verify skill in {SKILL}.

{OUT}/risk.json lists 5 claims about the project in {TREE}. Verify each one independently:
is it true? Depth: standard. Execution mode: reasoning only, run nothing. Do not stop to ask.
Read the project's files freely. Read nothing outside {TREE}, {SKILL} and that one file.

Write {OUT}/returns-verifier.md: the PASS, FAIL and HYPOTHESES tables of the skill's Output
Format, one row per claim, numbered as in risk.json, with path:line relative to {TREE} and
the quoted line in every row. No summary.

Reply with one line: how many of the 5 claims are in FAIL.
```

```
Use the adversarial-verify skill in {SKILL}, "Step 2b: ABSTRACT TO FAILURE CATEGORIES".

The files in {OUT}/checked/ are the returns of verification agents about the project in
{TREE}; their FAIL and FAILURE CATEGORIES tables say which failure categories were found and
where. For each category, search these files for other instances of the same pattern:
{FILES}

Execution mode: reasoning only, run nothing. Do not stop to ask. Read nothing outside {TREE},
{SKILL} and {OUT}/checked/.

Write {OUT}/returns-category.md: FAIL and HYPOTHESES tables in the skill's Output Format,
with path:line relative to {TREE} and the quoted line in every row, holding only instances
that are not already in the returns. No summary.

Reply with one line: how many new rows.
```

## Step 6: quote lookup of the two returns (script)

`python3 lookup.py --tree {TREE} --out {OUT}/checked2 {OUT}/returns-verifier.md {OUT}/returns-category.md`

## Step 7: assembler

```
You assemble a verification report. You do not verify and you do not open the project's
files. Read in {SKILL}/SKILL.md only "Finding format" and "Output Format".

Inputs:
- {OUT}/checked/*.md: the returns of the domain agents, after the lookup of their quotes;
- {OUT}/checked2/returns-verifier.md: an independent verification of the claims of
  {OUT}/risk.json;
- {OUT}/checked2/returns-category.md: other instances of the failure categories found;
- {OUT}/checked/lookup.json and {OUT}/checked2/lookup.json: per file, the rows returned and
  the rows the lookup discarded.

Write {OUT}/report.md in the skill's Output Format: one section per domain, then the
cross-domain summary. Rules:
- keep every row as it was returned (location, quote, type, severity, confidence); add no
  finding of your own and drop none;
- where the independent verifier disagrees with a domain agent about a claim, keep one row,
  with the lower confidence and both verdicts in its Scenario;
- the category agent's rows go in the FAIL or HYPOTHESES table of their domain;
- one line in the summary says how many rows came back, how many the lookup discarded, how
  many claims the independent verifier confirmed and how many it changed.

Reply with one line: how many rows the FAIL tables have in all.
```

## What is recorded

`report.md`, `plan.json`, every return, `risk.json`, the two `lookup.json`, and for each
agent what the harness reports (tokens, tool calls, time). Total tokens of the run: the sum
over its agents. The dispatcher's own cost is not counted.
