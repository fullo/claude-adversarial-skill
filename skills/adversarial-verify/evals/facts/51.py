"""Eval 51: button height = line-height + vertical padding, before and after the commit."""
before = 20 + 2 * 12
after = 16 + 2 * 4
assert (before, after) == (44, 24)
assert before >= 44 > after  # the project's touch-target rule
print('ok 51')
