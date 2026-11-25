"""Automated test cases for Case Study 07 - Nested Loop Calendar Generator."""
import importlib.util
import os
import io
import contextlib

spec = importlib.util.spec_from_file_location(
    "sol", os.path.join(os.path.dirname(os.path.abspath(__file__)), "solution.py"))
sol = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sol)

passed = 0


def check(label, condition):
    global passed
    assert condition, "FAILED: " + label
    passed += 1
    print("  PASS:", label)


def build(month, start, year, supplied=-1):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        ok = sol.print_calendar(month, start, year, supplied)
    return ok, buf.getvalue().splitlines()


# TC-01: January has 31 days
check("January 2025 has 31 days", sol.month_length(0, 2025) == 31)

# TC-02: April has 30 days
check("April 2025 has 30 days", sol.month_length(3, 2025) == 30)

# TC-03: February 2025 has 28 days
check("February 2025 has 28 days", sol.month_length(1, 2025) == 28)

# TC-04: leap February 2024 has 29 days
check("February 2024 has 29 days", sol.month_length(1, 2024) == 29)

# TC-05: century non-leap year rule
check("February 1900 has 28 days", sol.month_length(1, 1900) == 28)

# TC-06: century leap year rule
check("February 2000 has 29 days", sol.month_length(1, 2000) == 29)

# TC-07: invalid month index returns -1
check("month index 12 returns -1", sol.month_length(12, 2025) == -1)

# TC-08: valid input is accepted
check("valid January accepted", sol.validate(0, 2, 2025, -1) == [])

# TC-09: invalid start weekday rejected
check("start day 8 rejected", len(sol.validate(0, 8, 2025, -1)) == 1)

# TC-10: negative start weekday rejected
check("start day -1 rejected", len(sol.validate(0, -1, 2025, -1)) == 1)

# TC-11: wrong supplied month length rejected
check("31 days supplied for April rejected",
      len(sol.validate(3, 0, 2025, 31)) == 1)

# TC-12: correct supplied month length accepted
check("30 days supplied for April accepted", sol.validate(3, 0, 2025, 30) == [])

# TC-13: invalid month index rejected
check("month 12 rejected", len(sol.validate(12, 1, 2025, -1)) == 1)

# TC-14: calendar is generated (returns True)
ok, lines = build(0, 2, 2025)
check("January 2025 calendar generated", ok is True)

# TC-15: January 2025 starting Wednesday fits in 5 week rows
number_rows = []
for line in lines:
    if line.strip() != "" and "---" not in line and "Mon" not in line and "January" not in line and "days" not in line:
        number_rows.append(line)
check("January 2025 has 5 day rows", len(number_rows) == 5)

# TC-16: first row starts with a blank Monday-Tuesday
check("first week row starts blank (Wed = 2 blanks)",
      number_rows[0].startswith("           1"))

# TC-17: all 31 dates appear exactly once in the day grid
grid = "\n".join(number_rows)
found_all = True
for d in range(1, 32):
    if grid.count("%4d" % d) != 1:
        found_all = False
check("every date 1..31 appears exactly once", found_all)

# TC-18: December starting Sunday needs 6 rows
ok, lines = build(11, 6, 2025)
number_rows = []
for line in lines:
    if line.strip() != "" and "---" not in line and "Mon" not in line and "December" not in line and "days" not in line:
        number_rows.append(line)
check("December 2025 starting Sunday has 6 rows", len(number_rows) == 6)

# TC-19: leap February prints 29 days
ok, lines = build(1, 5, 2024)
text = "\n".join(lines)
check("leap February prints day 29", "%4d" % 29 in text and "%4d" % 30 not in text)

# TC-20: invalid input prints a message and returns False
ok, lines = build(0, 9, 2025)
check("invalid start day prints error and returns False",
      ok is False and "INVALID INPUT" in "\n".join(lines))

print("\n%d test cases passed" % passed)
