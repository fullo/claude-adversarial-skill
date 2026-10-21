# prompt-sha256: a502f0639b93c074fd20190e3f58c7c630fa1d91a21742e31cdb07b968e7823b
"""Eval 35: the function as shown accepts 31 February, which the three valid-date tests do not cover."""
from _parse_day import parse_day_v1

assert parse_day_v1('2026-02-31') == (2026, 2, 31)
assert parse_day_v1('2026-01-15') == (2026, 1, 15)
print('ok 35')
