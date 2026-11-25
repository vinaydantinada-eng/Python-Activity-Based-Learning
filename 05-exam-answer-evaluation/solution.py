"""
Case Study 05: String-Based Examination Answer Evaluation
----------------------------------------------------------
Compare answer strings against an answer key, calculate correct,
incorrect and unanswered responses, apply negative marking and
produce student-wise results.

Syllabus used: variables, data types, operators, conditional statements,
loops, strings, lists, tuples and tuple unpacking.
No library is imported - only core Python 3 is used.
"""

# ------------------------------------------------------------------
# Marking scheme (hypothetical values for this study)
# ------------------------------------------------------------------
CORRECT_MARKS = 4
WRONG_MARKS = -1
BLANK_MARKS = 0
NUM_QUESTIONS = 20
PASS_PERCENT = 40.0          # pass mark as a percentage of maximum

# '?' marks an unanswered question
ANSWER_KEY = "ABCDACBDABCDADCBBACD"

# (roll, name, response string of length 20)
STUDENTS = [
    ("26000477", "Vinay",  "ABCDACBDABCDADCBBA"),   # short response, padded with blanks
    ("26000478", "Meghana", "ABCDACBDABCDADCBBACD"),  # identical to key
    ("26000479", "Arjun",  "ABBDCCBDABCDA?CBBACD"),  # a few wrong, one blank
    ("26000480", "Sneha",  "ABCDACBDABCDADCBBADC"),  # one swapped at the end
    ("26000481", "Rohit",  "????????????????????"),  # all blank
    ("26000482", "Divya",  "BBBBBBBBBBBBBBBBBBBB"),  # all wrong
]


def normalise(response):
    """Pad short responses with '?' and upper-case every letter."""
    fixed = ""
    for ch in response:
        if "a" <= ch <= "z":
            fixed += chr(ord(ch) - 32)      # convert lower to upper
        else:
            fixed += ch
    while len(fixed) < NUM_QUESTIONS:
        fixed += "?"
    if len(fixed) > NUM_QUESTIONS:
        fixed = fixed[0:NUM_QUESTIONS]
    return fixed


def evaluate(response):
    """Return (correct, wrong, blank, score, detail_string)."""
    ans = normalise(response)

    correct = 0
    wrong = 0
    blank = 0
    detail = ""

    for i in range(NUM_QUESTIONS):
        given = ans[i]
        expected = ANSWER_KEY[i]

        if given == "?":
            blank += 1
            detail += "-"
        elif given == expected:
            correct += 1
            detail += "+"
        else:
            wrong += 1
            detail += "x"

    score = correct * CORRECT_MARKS + wrong * WRONG_MARKS + blank * BLANK_MARKS
    return correct, wrong, blank, score, detail


def grade(percentage):
    """Convert percentage to a letter grade."""
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= PASS_PERCENT:
        return "D (pass)"
    else:
        return "F (fail)"


def main():
    maximum = NUM_QUESTIONS * CORRECT_MARKS

    print("=" * 82)
    print("  EXAMINATION ANSWER EVALUATION  (negative marking)")
    print("=" * 82)
    print("  Questions: %d   Correct: +%d   Wrong: %d   Blank: %d   Maximum: %d"
          % (NUM_QUESTIONS, CORRECT_MARKS, WRONG_MARKS, BLANK_MARKS, maximum))
    print("  Answer key : %s" % ANSWER_KEY)
    print("-" * 82)
    print("%-10s %-9s %4s %5s %5s %6s %8s  %s"
          % ("Roll", "Name", "Corr", "Wrong", "Blank", "Score", "Percent", "Grade"))
    print("-" * 82)

    results = []       # (roll, name, correct, wrong, blank, score, percent, grade)

    for student in STUDENTS:
        # ---- tuple unpacking ----
        roll, name, response = student

        correct, wrong, blank, score, detail = evaluate(response)
        percent = score * 100.0 / maximum
        g = grade(percent)

        results.append((roll, name, correct, wrong, blank, score, percent, g))

        print("%-10s %-9s %4d %5d %5d %6d %7.1f%%  %s"
              % (roll, name, correct, wrong, blank, score, percent, g))

    print("-" * 82)

    # ---- answer-wise pattern for each student ----
    print("\n  ANSWER-WISE PATTERN  ( + correct, x wrong, - blank )")
    print("  Question:  1         2         3")
    print("             12345678901234567890")
    print("  Key       : %s" % ANSWER_KEY)

    for student in STUDENTS:
        roll, name, response = student
        _, _, _, _, detail = evaluate(response)
        print("  %-9s : %s" % (name, detail))

    # ---- topper and statistics ----
    print("\n" + "-" * 82)
    topper_index = 0
    for i in range(1, len(results)):
        if results[i][5] > results[topper_index][5]:
            topper_index = i

    top = results[topper_index]
    print("  Topper        : %s (%s) with %d marks (%.1f%%)"
          % (top[1], top[0], top[5], top[6]))

    total_score = 0
    passed_count = 0
    failed_count = 0
    for r in results:
        total_score += r[5]
        if r[6] >= PASS_PERCENT:
            passed_count += 1
        else:
            failed_count += 1

    avg = total_score * 1.0 / len(results)
    print("  Class average : %.2f marks out of %d" % (avg, maximum))
    print("  Passed        : %d    Failed: %d" % (passed_count, failed_count))

    # ---- question-wise analysis: which questions were missed most? ----
    print("\n" + "-" * 82)
    print("  QUESTION-WISE ANALYSIS (across all students)")
    print("  Q  Key  Correct  Wrong  Blank   Remark")
    hardest_q = 1
    hardest_missed = -1
    for q in range(NUM_QUESTIONS):
        c = 0
        w = 0
        b = 0
        for student in STUDENTS:
            roll, name, response = student
            ans = normalise(response)
            if ans[q] == "?":
                b += 1
            elif ans[q] == ANSWER_KEY[q]:
                c += 1
            else:
                w += 1
        remark = ""
        if c >= len(STUDENTS) - 1:
            remark = "well answered"
        elif w + b >= len(STUDENTS) * 0.6:
            remark = "weakly answered"
        print("  %-3d %-4s %-8d %-6d %-6d %s" % (q + 1, ANSWER_KEY[q], c, w, b, remark))
        if w + b > hardest_missed:
            hardest_missed = w + b
            hardest_q = q + 1

    print("\n  Most often missed question: Q%d (%d of %d students did not score on it)."
          % (hardest_q, hardest_missed, len(STUDENTS)))
    print("\nAll names, roll numbers and responses are hypothetical.")


if __name__ == "__main__":
    main()
