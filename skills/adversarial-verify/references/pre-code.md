# Pre-code validation and spike reports

Part of the adversarial-verify skill. Step numbers and section names with no file name are in `SKILL.md`; paths are relative to the skill's folder. Read this file when the artifact proposes work not yet done (Step 1c) or is the report of a spike, a prototype or an experiment (Step 3, Analysis). The spike checklist that Step 3 (Analysis) and Step 1c name is the second section below.

Contents: Step 1c (classes of claim, what a suggested spike and a suggested mock-up state); the checklist for spike and prototype reports; the PRE-CODE VALIDATION section of the report.

## Step 1c: PRE-CODE VALIDATION (any artifact that proposes work not yet done)

A plan, a spec, an ADR or an analysis that recommends work can be verified before anyone writes code, and that is when a wrong assumption is cheapest. Classify every claim of it by the evidence behind it (at quick depth, only the top 3 highest-risk claims, ranked as in Step 3c):

| Class | Meaning | What to suggest |
|-------|---------|-----------------|
| **Evidenced** | the evidence already exists: code, tests, a recorded response, a measurement, recorded user evidence (research notes, test sessions) or an already approved mock-up, that you can cite. A result someone only reports counts once you have read the result itself (the output, the log, the measurement); a spike's result counts once it passes the spike checklist (Step 3, Analysis) | nothing; cite it |
| **Technical assumption** | it depends on something nobody has observed yet: an external API, a library, performance, a file format, a device | a **spike** before the code |
| **User-expectation assumption** | it depends on what the users want, expect or will understand | a **mock-up** before the code (below) |

The class feeds the confidence: an assumption of either kind is a claim only a run or the users can decide, so it scores at most 79 (Run-only constraint, Step 4) until its spike or mock-up is done. An assumption the plan presents as settled fact goes in FAIL as a preventive measure, with its open question as the scenario; one the plan already marks as open stays only in PRE-CODE VALIDATION.

**A spike** is a small, throwaway experiment that answers one question. Each suggested spike states:
1. **The question**, one per spike (e.g. "does the API honour `updated_since`?").
2. **The measurement that decides it**: what will be run or read, and which result answers yes or no.
3. **The decision rule**, with all three branches: the result that means do, the result that means don't, and the result that means postpone, with the conditions that would reopen it.
4. **The throwaway constraint**: no production code, and no writes to real systems (no real orders, payments, messages or records). A spike that needs a real system uses read-only calls, test credentials, a sandbox or recorded responses. A proposed spike that writes to a real system is a demonstrated defect of the plan, in FAIL.

Typical adversarial questions for a spike on an external system: does it silently ignore a parameter it does not support? Does the documentation match the real responses? What are the limits of quantity, page size, rate and format? What does it return when nothing matches?

Design each suggested spike so that its report will pass the spike checklist (Step 3, Analysis): declared sample, held-out data when anything is tuned, reproducible bench. A spike that could run now (e.g. a read-only call with test credentials) is also a row of PROPOSED EXECUTABLE CHECKS. The verifier runs it only with approved checks, and writes one only with consent to write (Execution and consent).

**A mock-up** (a picture of the proposed interface for users, not a test double) answers what the users expect before anyone builds it. The verifier suggests one; it does not make it. Each suggested mock-up states:
1. **The question** the users must answer (e.g. "do managers need the totals per status, or only the list?").
2. **The form** that fits the software: images, a static page, a clickable prototype, screens of a native app or a game, sample output of a command-line tool.
3. **Today next to Proposed**: the current screen or output beside the new one, so the change is visible, when a current one exists.
4. **Alternatives A and B** when the choice is open, with what each one favours.
5. **Real content and states**: long names, empty lists, many rows, errors, a translation longer than the original.
6. **Who approves it, and the link**: the mock-up is approved by the users or their representative before development, and the link between the request, the mock-up and the change is written down.

## Spike and prototype reports (Step 3, Analysis)

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

## Report section

In the report it comes after DECOMPOSED CLAIMS (Output Format).

```
## PRE-CODE VALIDATION (artifacts that propose work not yet done; omit otherwise)
[With many claims, list evidenced ones by number only]
| # | Claim | Class | Confidence | Evidence; or spike (question, measurement, decision rule); or mock-up (question, form, alternatives, approver) |
|---|-------|-------|------------|--------------------------------------------------------------|
```
