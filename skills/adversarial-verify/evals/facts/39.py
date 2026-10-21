"""Eval 39: test_rejects_31_april passes on the parent and on the commit; 29 Feb 2024 separates them."""
from _parse_day import parse_day_parent, parse_day_fixed, raises

assert raises(parse_day_parent, '2026-04-31') and raises(parse_day_fixed, '2026-04-31')
assert raises(parse_day_parent, '2024-02-29') and not raises(parse_day_fixed, '2024-02-29')
assert raises(parse_day_fixed, '2026-02-29') and raises(parse_day_fixed, '2100-02-29')
print('ok 39')
