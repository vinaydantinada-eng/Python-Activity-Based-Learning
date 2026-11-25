"""
Case Study 08: Student Marks Matrix Analysis
---------------------------------------------
Analyse a matrix of student marks across subjects, calculate row-wise
and column-wise statistics, identify top performers, and detect
subjects with low average performance.

Syllabus used: variables, data types, operators, conditional statements,
loops (nested), lists, nested lists, tuples, unpacking.
No library is imported - only core Python 3 is used.
"""

SUBJECTS = ["Maths", "Physics", "Chemistry", "English", "CS"]

# (roll, name, [marks in SUBJECTS order]) - each mark is out of 100
STUDENTS = [
    ("26000401", "Aarav",   [88, 76, 72, 84, 95]),
    ("26000402", "Bhavya",  [72, 64, 58, 80, 66]),
    ("26000403", "Chirag",  [95, 92, 70, 78, 97]),
    ("26000404", "Dhanya",  [61, 55, 45, 74, 49]),
    ("26000405", "Eshan",   [83, 88, 58, 81, 86]),
    ("26000406", "Farheen", [45, 52, 38, 66, 42]),
    ("26000407", "Gaurav",  [78, 71, 62, 69, 72]),
    ("26000408", "Harshita",[90, 84, 68, 88, 79]),
    ("26000409", "Irfan",   [67, 60, 63, 58, 70]),
    ("26000410", "Jhanavi", [54, 49, 47, 71, 45]),
]

LOW_AVERAGE_LIMIT = 60.0      # subject averages below this are flagged
PASS_MARK = 40                # per-subject pass mark


def row_total_and_average(marks):
    """Sum and average of one student's marks."""
    total = 0
    for m in marks:
        total += m
    return total, total / len(marks)


def column_average(matrix, col):
    """Average of column col across all rows of the nested list."""
    total = 0
    for row in matrix:
        total += row[col]
    return total / len(matrix)


def main():
    # Build a plain nested list of marks for column work
    matrix = []
    for roll, name, marks in STUDENTS:      # tuple unpacking
        matrix.append(marks)

    print("=" * 88)
    print("  STUDENT MARKS MATRIX ANALYSIS")
    print("=" * 88)
    print("  Subjects: " + ", ".join(SUBJECTS))
    print("  Students: %d" % len(STUDENTS))

    # ---------------- row-wise statistics ----------------
    print("\n" + "-" * 88)
    print("  ROW-WISE STATISTICS (per student)")
    print("-" * 88)
    print("%-10s %-10s" % ("Roll", "Name"), end="")
    for subject in SUBJECTS:
        print("%6s" % subject[0:5], end="")
    print("%8s %8s %8s" % ("Total", "Average", "Grade"))

    totals = []
    for i in range(len(STUDENTS)):
        roll, name, marks = STUDENTS[i]
        total, average = row_total_and_average(marks)
        totals.append(total)

        if average >= 85:
            grade = "A+"
        elif average >= 75:
            grade = "A"
        elif average >= 65:
            grade = "B"
        elif average >= 55:
            grade = "C"
        elif average >= PASS_MARK:
            grade = "D"
        else:
            grade = "F"

        print("%-10s %-10s" % (roll, name), end="")
        for m in marks:
            print("%6d" % m, end="")
        print("%8d %7.2f %8s" % (total, average, grade))

    print("-" * 88)

    # ---------------- column-wise statistics ----------------
    print("\n" + "-" * 88)
    print("  COLUMN-WISE STATISTICS (per subject)")
    print("-" * 88)
    print("%-12s %8s %8s %8s %8s %6s  %s"
          % ("Subject", "Average", "Highest", "Lowest", "Passes", "Fails", "Remark"))

    low_avg_subjects = []
    for col in range(len(SUBJECTS)):
        average = column_average(matrix, col)

        highest = matrix[0][col]
        lowest = matrix[0][col]
        passes = 0
        fails = 0
        for row in matrix:
            m = row[col]
            if m > highest:
                highest = m
            if m < lowest:
                lowest = m
            if m >= PASS_MARK:
                passes += 1
            else:
                fails += 1

        remark = ""
        if average < LOW_AVERAGE_LIMIT:
            remark = "LOW AVERAGE"
            low_avg_subjects.append(SUBJECTS[col])

        print("%-12s %8.2f %8d %8d %8d %6d  %s"
              % (SUBJECTS[col], average, highest, lowest, passes, fails, remark))

    print("-" * 88)

    # ---------------- top performers ----------------
    print("\n  TOP PERFORMERS (by total marks)")
    print("-" * 88)

    # rank without disturbing the original data: simple selection sort on copies
    ranked = []
    for i in range(len(STUDENTS)):
        roll, name, marks = STUDENTS[i]
        total, average = row_total_and_average(marks)
        ranked.append((total, average, roll, name))

    # bubble-sort the ranked list by total (descending)
    n = len(ranked)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if ranked[j][0] < ranked[j + 1][0]:
                ranked[j], ranked[j + 1] = ranked[j + 1], ranked[j]

    for i in range(len(ranked)):
        total, average, roll, name = ranked[i]
        print("  %2d. %-10s %-10s total %4d   average %6.2f"
              % (i + 1, roll, name, total, average))

    # ---------------- class summary ----------------
    print("\n" + "-" * 88)
    print("  CLASS SUMMARY")
    print("-" * 88)

    class_total = 0
    for t in totals:
        class_total += t
    class_average = class_total / (len(STUDENTS) * len(SUBJECTS))

    topper_total, topper_avg, topper_roll, topper_name = ranked[0]
    lowest_total, lowest_avg, low_roll, low_name = ranked[-1]

    print("  Class average (all marks) : %.2f" % class_average)
    print("  Topper   : %s (%s) - total %d" % (topper_name, topper_roll, topper_total))
    print("  Lowest   : %s (%s) - total %d" % (low_name, low_roll, lowest_total))

    students_above_avg = 0
    for i in range(len(STUDENTS)):
        avg = row_total_and_average(STUDENTS[i][2])[1]
        if avg > class_average:
            students_above_avg += 1
    print("  Students above class average : %d of %d"
          % (students_above_avg, len(STUDENTS)))

    if len(low_avg_subjects) > 0:
        print("  Subjects below average %.0f : %s"
              % (LOW_AVERAGE_LIMIT, ", ".join(low_avg_subjects)))
    else:
        print("  No subject fell below the %.0f average limit." % LOW_AVERAGE_LIMIT)

    # ---------------- per-student weak subjects ----------------
    print("\n  Students with one or more subjects below the pass mark (%d):" % PASS_MARK)
    any_weak = False
    for i in range(len(STUDENTS)):
        roll, name, marks = STUDENTS[i]
        weak = []
        for col in range(len(SUBJECTS)):
            if marks[col] < PASS_MARK:
                weak.append("%s (%d)" % (SUBJECTS[col], marks[col]))
        if len(weak) > 0:
            any_weak = True
            print("    %-10s %-10s -> %s" % (roll, name, ", ".join(weak)))
    if not any_weak:
        print("    None - every student passed every subject.")

    print("\nAll marks and names are hypothetical.")


if __name__ == "__main__":
    main()
