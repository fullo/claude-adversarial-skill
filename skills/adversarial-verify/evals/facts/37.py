"""Eval 37: parse_day('2026-02-31') returns (2026, 2, 31), no exception."""
from _parse_day import parse_day_v1

assert parse_day_v1('2026-02-31') == (2026, 2, 31)
# Eval 35 states the same code with three valid-date tests passing and none on 31 February.
assert parse_day_v1('2026-01-15') == (2026, 1, 15)
print('ok 37')
