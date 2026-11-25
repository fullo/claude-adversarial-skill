# prompt-sha256: 2e427759c581bc05c4c7ecbb30c38db67c4ee8a010cec2b61a34a8db80dcf546
"""Eval 57: the totals of the run, and how many survivors the returned rows leave unaccounted for."""
killed, survived, timed_out, total = 239, 9, 12, 260
assert killed + survived + timed_out == total
returned, quote_found = 8, 7
discarded = returned - quote_found
assert discarded == 1
assert survived - quote_found == 2  # survivors with no standing row
print('ok 57')
