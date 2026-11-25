"""
Case Study 07: Nested Loop Calendar Generator
----------------------------------------------
Generate a formatted monthly calendar using the supplied starting
weekday and number of days, correctly aligning weeks and handling
valid month lengths.

Syllabus used: variables, data types, operators, conditional statements,
loops (including nested loops), strings, lists.
No library is imported - only core Python 3 is used.
"""

DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
MONTH_NAMES = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]

# Standard number of days in each month (non-leap year).
# February is handled separately so a leap year can reuse the same list.
MONTH_LENGTHS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# (month_index, starting_day_index (0=Mon .. 6=Sun), year,
#  supplied_length (-1 = use the standard length), note)
MONTHS_TO_SHOW = [
    (0, 2, 2025, -1, "valid month starting on Wednesday"),
    (1, 5, 2025, -1, "valid February of a non-leap year"),
    (1, 5, 2024, -1, "leap February - 29 days"),
    (11, 6, 2025, -1, "valid month starting on Sunday"),
    (5, 8, 2025, -1, "INVALID start day index 8"),
    (3, 0, 2025, 31, "INVALID month length - 31 days supplied for April"),
    (12, 1, 2025, -1, "INVALID month index 12"),
]


def month_length(month_index, year):
    """Days in a month, with the Gregorian leap-year rule for February."""
    if month_index < 0 or month_index > 11:
        return -1
    if month_index == 1:
        if (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0):
            return 29
        return 28
    return MONTH_LENGTHS[month_index]


def validate(month_index, start_day, year, override_length):
    """Return a list of validation errors (empty means the input is valid)."""
    errors = []

    if month_index < 0 or month_index > 11:
        errors.append("month index %d is outside 0-11" % month_index)
        return errors          # nothing else can be checked meaningfully

    if start_day < 0 or start_day > 6:
        errors.append("starting weekday must be 0 (Mon) to 6 (Sun), got %d"
                      % start_day)

    expected = month_length(month_index, year)
    if override_length != -1 and override_length != expected:
        errors.append("%s %d has %d days, but %d were supplied"
                      % (MONTH_NAMES[month_index], year, expected, override_length))

    return errors


def print_calendar(month_index, start_day, year, override_length=-1):
    """Print the formatted calendar. Returns False if input was invalid."""
    errors = validate(month_index, start_day, year, override_length)
    if len(errors) > 0:
        print("  INVALID INPUT - calendar not generated:")
        for err in errors:
            print("     - %s" % err)
        return False

    days = month_length(month_index, year)

    title = "%s %d" % (MONTH_NAMES[month_index], year)
    print("  " + title.center(27))
    print("  " + ("-" * 27))

    # weekday header
    header = ""
    for name in DAY_NAMES:
        header += " " + name
    print(header)
    print("  " + ("-" * 27))

    # ---- nested loops: week rows x day columns ----
    day_number = 1
    week = 0
    while day_number <= days:
        row = ""
        for weekday in range(7):                       # inner loop: columns
            if week == 0 and weekday < start_day:
                row += "    "                          # leading blanks
            elif day_number <= days:
                row += "%4d" % day_number
                day_number += 1
            else:
                row += "    "                          # trailing blanks
        print(row.rstrip())
        week += 1                                      # outer loop: rows

    print("  " + ("-" * 27))
    print("  %d days, %d week rows, starts on %s"
          % (days, week, DAY_NAMES[start_day]))
    return True


def main():
    print("=" * 60)
    print("  NESTED LOOP CALENDAR GENERATOR")
    print("=" * 60)

    for i in range(len(MONTHS_TO_SHOW)):
        month_index, start_day, year, supplied, note = MONTHS_TO_SHOW[i]
        print("\n" + "-" * 60)
        print("  CALENDAR %d  (%s)" % (i + 1, note))
        print("-" * 60)
        print_calendar(month_index, start_day, year, supplied)

    # ---------------- summary of month lengths ----------------
    print("\n" + "=" * 60)
    print("  MONTH LENGTH REFERENCE FOR 2025 (non-leap year)")
    print("=" * 60)
    for i in range(12):
        print("  %-10s : %2d days" % (MONTH_NAMES[i], month_length(i, 2025)))
    print("  %-10s : %2d days  (leap year)" % (MONTH_NAMES[1],
                                               month_length(1, 2024)))
    print("\n  Note: calendars are generated from a supplied starting weekday;")
    print("  the program does not use any date library.")


if __name__ == "__main__":
    main()
