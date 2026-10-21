"""Eval 42: changes the two tests would not catch (examples in assertion 2)."""


def run_tests(discount):
    return discount(100, 'WELCOME10') == 90 and discount(100, '') == 100


assert run_tests(lambda t, c: round(t * 0.9, 2) if c == 'WELCOME10' else t)
assert run_tests(lambda t, c: t * 0.9 if c == 'WELCOME10' else t)          # round removed
assert run_tests(lambda t, c: round(t * 0.9, 0) if c == 'WELCOME10' else t)  # other digits
assert run_tests(lambda t, c: round(t * 0.9, 2) if c else t)               # any non-empty code
print('ok 42')
