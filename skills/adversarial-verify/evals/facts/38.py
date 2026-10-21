"""Eval 38: the k/100 test passes on the new discount and fails at k = 1 on the old one."""


def new(total, code='WELCOME10'):
    return round(total * 0.9, 2) if code == 'WELCOME10' else total


def old(total, code='WELCOME10'):
    return total * 0.9 if code == 'WELCOME10' else total


def two_decimals(x):
    return abs(x * 100 - round(x * 100)) < 1e-9


assert all(two_decimals(new(k / 100)) for k in range(0, 10001))
first = next(k for k in range(0, 10001) if not two_decimals(old(k / 100)))
assert first == 1 and repr(old(0.01)) == '0.009000000000000001'
# The first draft of eval 38 claimed round(10.05 * 0.9, 2) == 9.05: it is 9.05.
assert round(10.05 * 0.9, 2) == 9.05
print('ok 38')
