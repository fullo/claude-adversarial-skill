# prompt-sha256: 1e640d4da3f17794796b649ee6cceae0733c96b7a695c25967a59f4f2a024d83
"""Eval 49: usable label width per button and which German labels fit."""
labels = {'Startseite': 61, 'Bestellungen': 79, 'Gemerkt': 50, 'Einstellungen': 82}
padding = 2 * 8


def clipped(screen):
    usable = screen / 4 - padding
    return usable, {name for name, w in labels.items() if w > usable}


assert clipped(375) == (77.75, {'Bestellungen', 'Einstellungen'})
assert clipped(320) == (64.0, {'Bestellungen', 'Einstellungen'})
assert clipped(430) == (91.5, set())
print('ok 49')
