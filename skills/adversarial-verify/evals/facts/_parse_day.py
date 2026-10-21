# Shared by facts/37.py and facts/39.py: the functions as shown in the evals.
DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def parse_day_v1(text):  # eval 37 (and 29, 35)
    parts = text.split('-')
    year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
    if month < 1 or month > 12:
        raise ValueError('bad month')
    if day < 1 or day > 31:
        raise ValueError('bad day')
    return (year, month, day)


def parse_day_parent(text):  # eval 39, parent commit
    year, month, day = (int(p) for p in text.split('-'))
    if month < 1 or month > 12:
        raise ValueError('bad month')
    if day < 1 or day > DAYS[month - 1]:
        raise ValueError('bad day')
    return (year, month, day)


def leap(y):
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)


def parse_day_fixed(text):  # eval 39, the commit as described
    year, month, day = (int(p) for p in text.split('-'))
    if month < 1 or month > 12:
        raise ValueError('bad month')
    n = 29 if month == 2 and leap(year) else DAYS[month - 1]
    if day < 1 or day > n:
        raise ValueError('bad day')
    return (year, month, day)


def raises(f, arg):
    try:
        f(arg)
    except ValueError:
        return True
    return False
