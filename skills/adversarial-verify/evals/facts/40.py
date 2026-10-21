"""Eval 40: which of the six mutants of `age >= 18` the two tests kill."""
tests = [(30, True), (5, False)]
mutants = {
    '>= to <': lambda a: a < 18, '>= to <=': lambda a: a <= 18, 'return True': lambda a: True,
    '>= to >': lambda a: a > 18, '18 to 19': lambda a: a >= 19, '18 to 17': lambda a: a >= 17,
}
killed = {n for n, f in mutants.items() if any(f(x) != y for x, y in tests)}
assert killed == {'>= to <', '>= to <=', 'return True'}
# The boundary tests proposed in the expected answer kill the three survivors.
boundary = [(18, True), (17, False)]
assert all(any(mutants[n](x) != y for x, y in boundary) for n in set(mutants) - killed)
print('ok 40')
