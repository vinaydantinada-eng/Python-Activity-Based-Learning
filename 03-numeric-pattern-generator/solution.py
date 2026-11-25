"""
Case Study 03: Advanced Numeric Pattern Generator
--------------------------------------------------
Produce a hollow diamond or a symmetric numerical pattern based on a
user-specified dimension, with validation for invalid dimensions and
carefully aligned output.

Syllabus used: variables, data types, operators, conditional statements,
loops, strings, pattern generation, lists.
No library is imported - only core Python 3 is used.

Pattern choice:
    1 = hollow diamond (stars)
    2 = symmetric number pyramid (1, 121, 12321, ...)
    3 = hollow number diamond
Anything else is reported as an invalid choice.
"""

# ---------------- validation limits ----------------
MIN_DIMENSION = 1
MAX_DIMENSION = 15         # kept moderate so the output stays aligned on screen


def validate(choice, size):
    """Check the user input and return a list of error messages."""
    errors = []

    if choice not in (1, 2, 3):
        errors.append("pattern choice must be 1, 2 or 3 (got %s)" % choice)

    if size < MIN_DIMENSION:
        errors.append("dimension %d is too small (minimum %d)"
                      % (size, MIN_DIMENSION))
    elif size > MAX_DIMENSION:
        errors.append("dimension %d is too large (maximum %d)"
                      % (size, MAX_DIMENSION))

    return errors


def diamond_row(row, size):
    """One row of a hollow diamond outline: leading spaces then outline."""
    inside = 2 * row - 1
    if inside == 1:
        return " " * (size - row) + "*"
    return " " * (size - row) + "*" + " " * (inside - 2) + "*"


def hollow_diamond(size):
    """Print a hollow diamond of stars with 2*size-1 rows."""
    for row in range(1, size + 1):
        print(diamond_row(row, size).rstrip())
    for row in range(size - 1, 0, -1):
        print(diamond_row(row, size).rstrip())


def number_pyramid(size):
    """Print rows 1, 121, 12321, ... up to size, perfectly centred.

    Each number occupies exactly one character, so centring on the
    widest row keeps every row aligned under a monospace font.
    """
    width = 2 * size - 1
    for row in range(1, size + 1):
        line = ""
        for num in range(1, row + 1):
            line += str(num % 10)          # keep one character per cell
        for num in range(row - 1, 0, -1):
            line += str(num % 10)
        print(line.center(width).rstrip())


def hollow_number_diamond(size):
    """Hollow diamond whose outline rows carry the row number.

    Every outline row has exactly 2*row-1 characters (row number,
    spaces, row number), so centring on 2*size-1 aligns all rows.
    """
    for row in range(1, size + 1):
        label = str(row % 10)
        if row == 1:
            line = label.center(2 * size - 1)
        else:
            line = label + " " * (2 * row - 3) + label
            line = line.center(2 * size - 1)
        print(line.rstrip())

    for row in range(size - 1, 0, -1):
        label = str(row % 10)
        if row == 1:
            line = label.center(2 * size - 1)
        else:
            line = label + " " * (2 * row - 3) + label
            line = line.center(2 * size - 1)
        print(line.rstrip())


def generate(choice, size):
    """Validate and then generate the requested pattern."""
    errors = validate(choice, size)
    if len(errors) > 0:
        print("  INVALID INPUT - pattern not generated:")
        for err in errors:
            print("     - %s" % err)
        return False

    if choice == 1:
        print("  Hollow diamond of size %d:" % size)
        print()
        hollow_diamond(size)
    elif choice == 2:
        print("  Symmetric number pyramid of size %d:" % size)
        print()
        number_pyramid(size)
    else:
        print("  Hollow number diamond of size %d:" % size)
        print()
        hollow_number_diamond(size)

    print()
    return True


def main():
    print("=" * 58)
    print("  ADVANCED NUMERIC PATTERN GENERATOR")
    print("=" * 58)
    print("  1. Hollow diamond (stars)")
    print("  2. Symmetric number pyramid")
    print("  3. Hollow number diamond")
    print("  Valid dimension range: %d to %d" % (MIN_DIMENSION, MAX_DIMENSION))

    # Three sample runs demonstrate the patterns; three more demonstrate
    # the validation messages for invalid dimensions and choices.
    samples = [
        (1, 5, "valid input"),
        (2, 6, "valid input"),
        (3, 5, "valid input"),
        (1, 0, "size too small"),
        (2, 18, "size too large"),
        (5, 4, "unknown pattern choice"),
    ]

    for i in range(len(samples)):
        choice, size, note = samples[i]
        print("\n" + "-" * 58)
        print("  RUN %d  (pattern = %d, dimension = %d, %s)"
              % (i + 1, choice, size, note))
        print("-" * 58)
        generate(choice, size)


if __name__ == "__main__":
    main()
