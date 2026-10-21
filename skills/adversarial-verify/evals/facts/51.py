# prompt-sha256: dfba6277eff6648cd9808834cbe3d55c424d22fb77c174ab6c2d407357b55e76
"""Eval 51: button height = line-height + vertical padding, before and after the commit."""
before = 20 + 2 * 12
after = 16 + 2 * 4
assert (before, after) == (44, 24)
assert before >= 44 > after  # the project's touch-target rule
print('ok 51')
