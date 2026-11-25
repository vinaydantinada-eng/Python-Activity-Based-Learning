"""Automated test cases for Case Study 08 - Student Marks Matrix Analysis."""
import importlib.util
import os

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


matrix = []
for roll, name, marks in sol.STUDENTS:
    matrix.append(marks)

# TC-01: row total for the first student
check("Aarav's marks sum to %d" % sum([88, 76, 72, 84, 95]),
      sol.row_total_and_average([88, 76, 72, 84, 95])[0] == sum([88, 76, 72, 84, 95]))

# TC-02: row average is total / number of subjects
check("row average of [88,76,72,84,95] = 83.00",
      abs(sol.row_total_and_average([88, 76, 72, 84, 95])[1] - 83.0) < 0.01)

# TC-03: single-mark row
check("row of [100] -> total 100, average 100",
      sol.row_total_and_average([100]) == (100, 100.0))

# TC-04: zeros handled correctly
check("row of [0,0,0] -> total 0, average 0",
      sol.row_total_and_average([0, 0, 0]) == (0, 0.0))

# TC-05: column average, Chemistry (column 2)
chem = sol.column_average(matrix, 2)
expected_chem = 0
for row in matrix:
    expected_chem += row[2]
expected_chem = expected_chem / len(matrix)
check("Chemistry column average matches manual sum", abs(chem - expected_chem) < 0.001)

# TC-06: column average, first column
maths = sol.column_average(matrix, 0)
manual = 0.0
for row in matrix:
    manual += row[0]
manual = manual / len(matrix)
check("Maths column average = %.2f" % manual, abs(maths - manual) < 0.01)

# TC-07: every row has one mark per subject
rect = True
for row in matrix:
    if len(row) != len(sol.SUBJECTS):
        rect = False
check("matrix is rectangular (each row has 5 marks)", rect)

# TC-08: there are 10 students and 5 subjects
check("matrix is 10 x 5", len(matrix) == 10 and len(matrix[0]) == 5)

# TC-09: every subject average is between lowest and highest mark of the column
ok = True
for col in range(5):
    avg = sol.column_average(matrix, col)
    values = []
    for row in matrix:
        values.append(row[col])
    if not (min(values) <= avg <= max(values)):
        ok = False
check("each column average lies between its min and max", ok)

# TC-10: row totals sum to the grand total of all marks
row_sum = 0
for row in matrix:
    row_sum += sum(row)
manual_total = 0
for row in matrix:
    for m in row:
        manual_total += m
check("sum of row totals = sum of all marks", row_sum == manual_total)

# TC-11: low average subject is Chemistry (58.10 < 60)
check("Chemistry flagged as low average subject",
      sol.column_average(matrix, 2) < sol.LOW_AVERAGE_LIMIT)

# TC-12: no other subject is below the limit
others_low = 0
for col in [0, 1, 3, 4]:
    if sol.column_average(matrix, col) < sol.LOW_AVERAGE_LIMIT:
        others_low += 1
check("no other subject falls below %.0f" % sol.LOW_AVERAGE_LIMIT, others_low == 0)

# TC-13: topper identification
best_total = -1
best_name = ""
for roll, name, marks in sol.STUDENTS:
    total = sol.row_total_and_average(marks)[0]
    if total > best_total:
        best_total = total
        best_name = name
check("topper is Chirag with %d marks" % best_total,
      best_name == "Chirag" and best_total == 432)

# TC-14: exactly one student has a mark below the pass mark
weak_count = 0
for roll, name, marks in sol.STUDENTS:
    for m in marks:
        if m < sol.PASS_MARK:
            weak_count += 1
check("exactly one mark below the pass mark", weak_count == 1)

print("\n%d test cases passed" % passed)
