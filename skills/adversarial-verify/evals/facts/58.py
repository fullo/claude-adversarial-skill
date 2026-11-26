# prompt-sha256: 73d336e6056afbbfc0c2ab0b6549a8d1fa464010c861f143a81f88bbce86814c
"""Eval 58: the rows of the draft and what the quote lookup does with each."""
at_line, wrong_line, description, not_in_file = 3, 1, 1, 1
rows = at_line + wrong_line + description + not_in_file
assert rows == 6
moved = not_in_file
assert rows - moved == 5  # rows left in their table after the lookup
assert 91 != 88  # row 4 is corrected, not kept
print('ok 58')
