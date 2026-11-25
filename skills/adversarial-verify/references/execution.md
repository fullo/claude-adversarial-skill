# Running approved checks: executable falsification and the mutation probe

Part of the adversarial-verify skill. Step numbers and section names with no file name are in `SKILL.md`; paths are relative to the skill's folder. Read this file before running or writing any test (Step 3e) and before running the mutation probe. With reasoning only, nothing here applies: the tests and the probe are only proposed.

Contents: the rules of Step 3e; the rules of the mutation probe; where the runs happen (a memory-backed filesystem); long outputs; the EXECUTED TESTS and MUTATION PROBE sections of the report.

## Step 3e: EXECUTABLE FALSIFICATION (only with approved checks)

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

## Mutation probe (on request, any domain where tests cover the code)

1. **Cost first.** State the cost in observable terms: lines in scope, number of mutants, and which tests run for each. Approval of the probe on a scope approves that size; wait for confirmation only when the request named no scope or the probe would go beyond it. Unattended (Intake rule 7): run only if the instructions approved the probe and its scope; otherwise report the cost and leave it proposed.
2. **Scope: the changed lines**, when the tool allows it.
3. **Tool or hand mutations.** Use the project's mutation tool for its language if it is already installed; installing one needs consent. Otherwise apply 3-5 mutations by hand on the highest-risk changed lines (Step 3c: blast radius × probability), such as a flipped comparison, a changed boundary constant or a removed call, and run only the tests that cover each one.
4. **Mutate a separate copy** of the repository (where to keep it: *Where the runs happen*, below) and restore it after every mutant; mutating the user's working copy needs its own consent. Confirm at the end that the user's working copy is unchanged (Execution and consent: mutating is writing, covered only by the approval of the probe).
5. **Read every survivor.** First check that the tests covering it actually ran (not skipped, excluded or run with another configuration): if they did not, the mutant is **not measured**, not a survivor (test-environment constraint, Step 4). Each measured survivor is a **missing test** (no test checks that behavior) or **superfluous code** (nothing depends on it); call it **equivalent** only when the mutant cannot change any observable behavior, and give the reason for each one.
6. **Survivors are findings.** A missing test goes in FAIL as a demonstrated defect of the tests, superfluous code as a demonstrated defect of the code, in the section of the domain whose code the mutated lines belong to (the Tests domain is not added to the target for it), each with the mutant as its evidence; an equivalent mutant is not a finding. Removing superfluous code is only proposed. The test that would kill a survivor is the fix of its FAIL row, not a Step 3e hypothesis: with consent to write, write it and run it; it must be red on the mutant and green on the code. Record both runs in EXECUTED TESTS.
7. **A perfect score is suspicious** until you have seen why the mutants died: a test runner whose output the tool cannot read, a crash in setup, or a timeout can all count as kills. Look at the log for a sample of kills.
8. **Declare what was not measured.** Mutants skipped, timed out or not measured are excluded from the score: say how many, and that the score covers only the rest.

## Where the runs happen: a memory-backed filesystem

The mutation probe and a large test suite write a lot: a copy of the repository, build output, caches and temporary files, written again for every mutant or every run. Suggest keeping all of that in a memory-backed filesystem (e.g. tmpfs, a RAM disk): the runs are faster when writes are what slows them down, and the disk is spared most of those writes.

1. **When to suggest it.** With the mutation probe; with any other approved run when the suite is large or writes a lot at every run (a build, a test database, many files), or when the same suite will run several times (Step 3e on two versions, a run after every fix). Suggest it once per verification, together with the run it serves.
2. **The user decides.** Creating or mounting a memory-backed filesystem acts on the system, so it needs its own consent (Execution and consent, rule 2). A location the system already keeps in memory needs none beyond the approval of the run: check that it really is in memory before saying so. If creating one needs administrator rights, give the user the command and let them run it; the verifier does not raise its own privileges. Unattended (Intake rule 7): use one only if it already exists or the instructions approved it. After a refusal the run goes ahead on disk, with no other change.
3. **What goes there.** The separate copy of the repository (Step 3e, rule 5; mutation probe, rule 4) with the build output, caches and temporary files of the run. Never the user's working copy, and nothing that must outlive the verification: a test written with consent, a log the report cites and the report itself are on disk before the filesystem is removed.
4. **Size first.** What is stored there is taken from the memory the tests need. State the size of the copy with its build output next to the memory that is free, and do not suggest it when the two do not fit with room to spare. A run that exhausts memory kills tests and mutants for a reason that is not in the code: such a mutant is **not measured**, not killed (mutation probe, rules 5 and 7).
5. **It is a difference from production.** A memory-backed filesystem can behave unlike the storage the software really runs on: data that is never really flushed, other limits on size, names, permissions or locks, no slow or full disk. When a test's subject is the storage itself (durability, flushing, locking, a full disk, the speed of reads and writes), its result there falls under the test-environment constraint (Step 4): say so, and run that test on disk before relying on it. A timing measured there is not evidence of production speed.
6. **Clean up, and report what was done.** At the end remove the copy and unmount what the verification mounted, and confirm it. The report says where each run happened (EXECUTED TESTS, *Ran on*; MUTATION PROBE, the summary line). Do not report a speed-up that was not measured.

## Long outputs

The output of a run (a test log, a mutation log) can be thousands of lines. Read whole, it fills the verifier's context with lines that decide nothing, and leaves less room for the artifact under verification. What the report needs from it is short: the outcome, and the lines that prove it.

1. **Send the output of every run to a file**, next to the copy the run works on, never in the user's working copy. It is part of the approved run, not a separate write. Record for each run the command, the exit status and the path of the file.
2. **Read the short part first**: the exit status, the runner's own summary, the totals. They say whether anything else needs reading.
3. **Then read only what a question needs**, by searching the file: the failed tests, the survivors, the sample of kills (mutation probe, rule 7), the entries a finding will cite. Read each of those entries in full, with the lines around it. Do not read the rest to be sure, and do not copy the output into the report.
4. **Quote with a location.** Every result taken from the output is cited as path:line, with the deciding line quoted as it is (Step 4, hard constraint), so that anyone can find it again.
5. **Reconcile the counts.** What you read must add up to the runner's totals: so many failed and so many read, so many survived and so many read. Say which entries were not read and why: an entry nobody read is not evidence of anything (mutation probe, rule 8).
6. **The output can hold secrets or personal data.** Quote only what the finding needs and mask the rest. The file is removed with the copy (*Where the runs happen*, rule 6), unless the user asks to keep it.

## Report sections

In the report they come after VERIFICATION RESULTS, in this order (Output Format).

```
## EXECUTED TESTS (Step 3e and mutation probe, only with approved checks)
[Output: the file of each run's output; which entries were read and which were not]
| # | Hypothesis or survivor | Test | Ran on (one row per run) | Result | Finding type |
|---|-----------|------|--------|--------|--------------|

## MUTATION PROBE (only when the user asked for it)
[Scope, tool or hand mutations, where the copy was (on disk or in memory), mutants generated, killed, survived, skipped or timed out, score and what it excludes]
| # | File:Line | Mutator | Outcome | Reason | Test that would kill it |
|---|-----------|---------|---------|--------|------------------------|
[Outcome: missing test, superfluous code, equivalent, or not measured. Missing tests and superfluous code also go in FAIL]
```
