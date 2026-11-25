"""Automated test cases for Case Study 05 - String-Based Examination Answer Evaluation."""
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


KEY = sol.ANSWER_KEY

# TC-01: a response identical to the key scores the maximum
c, w, b, score, _ = sol.evaluate(KEY)
check("identical response: 20 correct, score 80",
      c == 20 and w == 0 and b == 0 and score == 80)

# TC-02: all blanks score zero
c, w, b, score, _ = sol.evaluate("?" * 20)
check("all blanks: 0 correct, 20 blank, score 0",
      c == 0 and b == 20 and score == 0)

# TC-03: all wrong incurs negative marking
wrong_all = ""
for ch in KEY:
    wrong_all += "B" if ch != "B" else "C"     # pick a letter different from the key
c, w, b, score, _ = sol.evaluate(wrong_all)
check("all wrong: score is negative (20 wrong -> -20)",
      w == 20 and score == -20)

# TC-04: one wrong answer costs 4 + 1 = 5 marks
c, w, b, score, _ = sol.evaluate("B" + KEY[1:])
check("one wrong answer: score 80 - 5 = 75", score == 75)

# TC-05: one blank costs 4 marks
c, w, b, score, _ = sol.evaluate("?" + KEY[1:])
check("one blank answer: score 80 - 4 = 76", score == 76)

# TC-06: short responses are padded with blanks
c, w, b, score, _ = sol.evaluate(KEY[0:10])
check("10-char response padded to 20 with 10 blanks",
      b == 10 and c == 10)

# TC-07: very long responses are truncated to 20
c, w, b, score, _ = sol.evaluate(KEY + "ABCDE")
check("25-char response truncated to 20, all correct",
      c == 20 and b == 0)

# TC-08: lowercase answers are accepted as correct
c, w, b, score, _ = sol.evaluate(KEY.lower())
check("lowercase response still scores 80", score == 80)

# TC-09: mixed-case answers are normalised
mixed = "abcdACBDabcdADCBBAcd"
c, w, b, score, _ = sol.evaluate(mixed)
check("mixed-case response equals key -> 20 correct", c == 20)

# TC-10: the detail string has one symbol per question
_, _, _, _, detail = sol.evaluate(KEY)
check("detail string length = 20", len(detail) == 20)

# TC-11: detail string marks are correct
_, _, _, _, detail = sol.evaluate(wrong_all[0] + KEY[1:])
check("detail string starts with 'x' then all '+'",
      detail[0] == "x" and detail[1] == "+")

# TC-12: grade boundaries
check("grade: 100% -> A+", sol.grade(100) == "A+")
check("grade: 90% -> A+", sol.grade(90) == "A+")
check("grade: 89.9% -> A", sol.grade(89.9) == "A")
check("grade: 75% -> B", sol.grade(75) == "B")
check("grade: 65% -> C", sol.grade(65) == "C")
check("grade: 45% -> D (pass)", sol.grade(45) == "D (pass)")
check("grade: 39% -> F (fail)", sol.grade(39) == "F (fail)")

# TC-13: topper of the sample data scores 80
scores = []
for roll, name, resp in sol.STUDENTS:
    scores.append(sol.evaluate(resp)[3])
check("topper score in sample data is 80", max(scores) == 80)

# TC-14: the all-blank student scores exactly 0
c, w, b, score, _ = sol.evaluate(sol.STUDENTS[4][2])
check("Rohit (all blank) scores 0", score == 0)

print("\n%d test cases passed" % passed)
