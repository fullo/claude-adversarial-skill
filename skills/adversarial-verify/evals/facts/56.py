# prompt-sha256: 8cda5f7ac01dc23e06a67b582f237c390e5e079e306e5c072f1478f34ad8a84a
"""Eval 56: the totals of the mutation run, and the score once the unmeasured mutant is taken out."""
killed, survived, timed_out, skipped, total = 104, 5, 8, 3, 120
assert killed + survived + timed_out + skipped == total
tests_run = {311: 7, 702: 7, 1188: 4, 1630: 0, 2051: 3}  # log line of each SURVIVED entry -> tests run
assert len(tests_run) == survived
not_measured = [line for line, n in tests_run.items() if n == 0]
assert not_measured == [1630]
measured_survivors = survived - len(not_measured)
measured = killed + measured_survivors
excluded = timed_out + skipped + len(not_measured)
assert (measured_survivors, measured, excluded) == (4, 108, 12)
assert measured + excluded == total
assert round(100 * killed / measured) == 96
print('ok 56')
