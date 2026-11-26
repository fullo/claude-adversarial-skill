# prompt-sha256: 807e9a257bad5fe0f35cf6467206bd90575a08e34e390fe9b75666e23309958a
"""Eval 58: the rows of the draft and what the quote lookup does with each."""
at_line, wrong_line, description, not_in_file, removed_line_found_before = 3, 1, 1, 1, 1
rows = at_line + wrong_line + description + not_in_file + removed_line_found_before
assert rows == 7
moved = not_in_file  # only row 6: row 7 is found in the version before the change
assert rows - moved == 6  # rows left in their table after the lookup
print('ok 58')
