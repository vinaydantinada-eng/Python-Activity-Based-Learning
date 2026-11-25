"""Automated test cases for Case Study 09 - Tuple-Based Product Catalogue Audit."""
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


def problems(code, name, price, stock, reorder):
    return sol.validate_record((code, name, price, stock, reorder))


# TC-01: a well-formed record has no problems
check("valid record accepted", problems("P101", "Notebook A5", 45.50, 120, 50) == [])

# TC-02: zero price rejected
check("zero price rejected", len(problems("P101", "Notebook", 0, 50, 10)) == 1)

# TC-03: negative price rejected
check("negative price rejected", len(problems("P101", "Notebook", -5, 50, 10)) == 1)

# TC-04: price above sanity limit rejected
check("price 7800 rejected (above 5000)",
      len(problems("P101", "Notebook", 7800, 50, 10)) == 1)

# TC-05: negative stock rejected
check("negative stock rejected", len(problems("P101", "Notebook", 50, -1, 10)) == 1)

# TC-06: zero stock is valid (it is out of stock, not invalid)
check("zero stock accepted as valid", problems("P101", "Notebook", 50, 0, 10) == [])

# TC-07: empty name rejected
check("empty product name rejected", len(problems("P101", "", 50, 10, 10)) == 1)

# TC-08: short code rejected
check("three-character code rejected", len(problems("P10", "Notebook", 50, 10, 10)) == 1)

# TC-09: code not starting with P rejected
check("code 'X101' rejected", len(problems("X101", "Notebook", 50, 10, 10)) == 1)

# TC-10: non-digit inside code rejected
check("code 'P1A1' rejected", len(problems("P1A1", "Notebook", 50, 10, 10)) == 1)

# TC-11: non-positive reorder quantity rejected
check("reorder quantity 0 rejected",
      len(problems("P101", "Notebook", 50, 10, 0)) == 1)

# TC-12: duplicate detection finds P103 only
dups = sol.find_duplicates(sol.CATALOGUE)
check("P103 detected as the only duplicate", dups == ["P103"])

# TC-13: a unique catalogue has no duplicates
check("catalogue without repeats has no duplicates",
      sol.find_duplicates([("P101", "A", 10, 5, 5), ("P102", "B", 10, 5, 5)]) == [])

# TC-14: three occurrences reported once
check("code appearing 3 times is reported once",
      sol.find_duplicates([("P101", "A", 1, 1, 1), ("P101", "A", 1, 1, 1),
                           ("P101", "A", 1, 1, 1)]) == ["P101"])

# TC-15: every catalogue tuple has exactly five fields
ok = True
for record in sol.CATALOGUE:
    if len(record) != 5:
        ok = False
check("every catalogue record has 5 fields (tuple shape)", ok)

# TC-16: tuple unpacking works on a catalogue record
code, name, price, stock, reorder = sol.CATALOGUE[0]
check("first record unpacks to P101 / Notebook A5 / 45.50 / 120 / 50",
      code == "P101" and name == "Notebook A5" and price == 45.50
      and stock == 120 and reorder == 50)

# TC-17: there are exactly 5 invalid records in the sample catalogue
invalid = 0
for record in sol.CATALOGUE:
    if len(sol.validate_record(record)) > 0:
        invalid += 1
check("exactly 5 invalid records in the sample catalogue", invalid == 5)

# TC-18: records below reorder level identified
low = 0
for record in sol.CATALOGUE:
    if len(sol.validate_record(record)) == 0 and record[3] <= sol.REORDER_LEVEL:
        low += 1
check("4 valid products are at or below the reorder level", low == 4)

print("\n%d test cases passed" % passed)
