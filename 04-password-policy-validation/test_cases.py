"""Automated test cases for Case Study 04 - Password Policy Validation Engine."""
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


def fails(password):
    return sol.validate_password(password)


# TC-01: a fully valid password has no failures
check("'Tr@ilBlazer99' is valid", fails("Tr@ilBlazer99") == [])

# TC-02: too short
check("'Sun@2024' fails the length rule",
      any("below minimum" in f for f in fails("Sun@2024")))

# TC-03: too long
long_pw = "Alpha@Beta99GammaDelta77"
check("22 character password fails the length rule",
      any("above maximum" in f for f in fails(long_pw)))

# TC-04: missing uppercase
check("'password@1234' fails uppercase and prohibited word rules",
      any("uppercase" in f for f in fails("password@1234")) and
      any("prohibited" in f for f in fails("password@1234")))

# TC-05: not enough digits
check("'Monsoon#Rain1' fails the two-digit rule",
      any("2 digits" in f for f in fails("Monsoon#Rain1")))

# TC-06: missing special character
check("'MonsoonRain77' fails the special character rule",
      any("special character" in f for f in fails("MonsoonRain77")))

# TC-07: consecutive repetition detected
check("'Super@Aaaa11' fails the 3-in-a-row rule",
      any("in a row" in f for f in fails("Super@Aaaa11")))

# TC-08: overall frequency detected
check("'R@inyDay_5555' fails the max-times rule",
      any("appears 4 times" in f for f in fails("R@inyDay_5555")))

# TC-09: prohibited words detected regardless of case
check("'PASSWORD@2024' detected as prohibited (case-insensitive)",
      any("prohibited" in f for f in fails("PASSWORD@2024")))

# TC-10: every prohibited word in the list is caught
caught = 0
for word in sol.PROHIBITED_WORDS:
    test_pw = "Ab1@" + word + "Xy9"
    if any("prohibited" in f for f in fails(test_pw)):
        caught += 1
check("all %d prohibited words are caught" % len(sol.PROHIBITED_WORDS),
      caught == len(sol.PROHIBITED_WORDS))

# TC-11: run length function correct
check("max_run_length('aabbbbcc') = 4", sol.max_run_length("aabbbbcc") == 4)

# TC-12: run length of an empty string is 0
check("max_run_length('') = 0", sol.max_run_length("") == 0)

# TC-13: most repeated character found
check("most_repeated_character('aabbbbcc') = ('b', 4)",
      sol.most_repeated_character("aabbbbcc") == ("b", 4))

# TC-14: category counting
check("count_categories('Ab1@x') = (1, 2, 1, 1, 0)",
      sol.count_categories("Ab1@x") == (1, 2, 1, 1, 0))

# TC-15: unknown characters are caught by the 'others' count
check("'Ab1@x~' has one character outside the allowed set",
      sol.count_categories("Ab1@x~")[4] == 1 and
      any("outside the allowed set" in f for f in fails("Ab1@x~")))

# TC-16: the sample list yields 6 valid passwords
valid = 0
for pw in sol.PASSWORDS:
    if fails(pw) == []:
        valid += 1
check("exactly 5 of the 10 sample passwords are valid", valid == 5)

print("\n%d test cases passed" % passed)
