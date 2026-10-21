"""Eval 48: WCAG contrast ratios of the stylesheet's colour pairs."""


def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    hi, lo = sorted((lum(a), lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


r = lambda a, b: round(ratio(a, b), 2)
assert r('#333333', '#ffffff') == 12.63 and r('#6b6b6b', '#ffffff') == 5.33 and r('#2563eb', '#ffffff') == 5.17
assert r('#d0d0d0', '#1e1e1e') == 10.81
assert r('#6b6b6b', '#1e1e1e') == 3.13 < 4.5 and r('#2563eb', '#1e1e1e') == 3.23 < 4.5
assert r('#3a3a3a', '#1e1e1e') == 1.47 < 3
assert r('#8a8a8a', '#1e1e1e') == 4.83  # a passing replacement for the hint text
print('ok 48')
