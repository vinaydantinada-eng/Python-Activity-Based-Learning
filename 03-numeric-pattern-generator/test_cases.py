"""Automated test cases for Case Study 03 - Advanced Numeric Pattern Generator."""
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


def capture(fn, *args):
    """Capture what a pattern function prints."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(*args)
    return buf.getvalue().splitlines()


# TC-01: valid choice with valid size passes validation
check("choice 1, size 5 accepted",
      sol.validate(1, 5) == [])

# TC-02: size below the minimum rejected
check("size 0 rejected as too small",
      len(sol.validate(1, 0)) == 1)

# TC-03: negative size rejected
check("size -3 rejected as too small",
      len(sol.validate(2, -3)) == 1)

# TC-04: size above the maximum rejected
check("size 18 rejected as too large",
      len(sol.validate(2, 18)) == 1)

# TC-05: unknown pattern choice rejected
check("choice 5 rejected as unknown pattern",
      len(sol.validate(5, 4)) == 1)

# TC-06: two errors reported together
check("choice 5 + size 0 reports both errors",
      len(sol.validate(5, 0)) == 2)

# TC-07: hollow diamond has exactly 2*size-1 rows
rows = capture(sol.hollow_diamond, 5)
check("hollow diamond size 5 has 9 rows", len(rows) == 9)

# TC-08: the diamond is symmetric top to bottom
check("hollow diamond rows are vertically symmetric",
      rows == rows[::-1])

# TC-09: the middle row is the widest
check("diamond row 5 is the widest", len(rows[4]) == max(len(r) for r in rows))

# TC-10: number pyramid row 3 is 12321
rows = capture(sol.number_pyramid, 6)
check("number pyramid row 3 reads 12321", rows[2].strip() == "12321")

# TC-11: pyramid has exactly 'size' rows and last row is longest
check("pyramid size 6 has 6 rows, last row longest",
      len(rows) == 6 and len(rows[5]) == max(len(r) for r in rows))

# TC-12: pyramid rows are centred (palindrome digits)
check("pyramid row 6 reads 12345654321 (palindrome)",
      rows[5].strip() == "12345654321")

# TC-13: hollow number diamond also has 2*size-1 rows
rows = capture(sol.hollow_number_diamond, 5)
check("hollow number diamond size 5 has 9 rows", len(rows) == 9)

# TC-14: hollow number diamond is symmetric
check("hollow number diamond rows symmetric", rows == rows[::-1])

# TC-15: generate() returns False for invalid input
check("generate returns False on invalid dimension",
      sol.generate(1, 0) is False)

# TC-16: generate() returns True for valid input
check("generate returns True on valid input",
      sol.generate(1, 5) is True)

print("\n%d test cases passed" % passed)
