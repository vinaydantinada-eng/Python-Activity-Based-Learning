"""Automated test cases for Case Study 01 - Progressive Electricity Billing."""
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


# TC-01: usage fully inside the first slab
check("50 units charged at Rs 2.50 = 125.00",
      abs(sol.slab_charge(50) - 125.00) < 0.01)

# TC-02: exactly on the first slab boundary
check("100 units = 250.00 (boundary)",
      abs(sol.slab_charge(100) - 250.00) < 0.01)

# TC-03: usage spread over three slabs
# 100*2.50 + 100*4.20 + 50*6.10 = 250 + 420 + 305
check("250 units = 975.00 across three slabs",
      abs(sol.slab_charge(250) - 975.00) < 0.01)

# TC-04: usage that enters the open-ended last slab
# 250 + 420 + 200*6.10 + 100*7.80 = 2670
check("500 units = 2670.00 including last slab",
      abs(sol.slab_charge(500) - 2670.00) < 0.01)

# TC-05: no surcharge when usage is exactly at the 500 unit limit
expected = 50 + 2670 + 2670 * 0.05
expected = expected - expected * 0.02
check("500 units -> no surcharge, bill = %.2f" % expected,
      abs(sol.compute_bill(500)[0] - round(expected, 2)) < 0.01)

# TC-06: one unit above the limit brings in the 3% surcharge
energy = 2670 + 7.80
expected = 50 + energy + energy * 0.05 + energy * 0.03
expected = expected - expected * 0.02
check("501 units -> surcharge applied, bill = %.2f" % expected,
      abs(sol.compute_bill(501)[0] - round(expected, 2)) < 0.01)

# TC-07: zero consumption only pays fixed charge minus rebate
check("0 units -> 50.00 - 2% rebate = 49.00",
      abs(sol.compute_bill(0)[0] - 49.00) < 0.01)

# TC-08: bill must grow with consumption
check("bill strictly increases from 180 to 181 units",
      sol.compute_bill(181)[0] > sol.compute_bill(180)[0])

# TC-09: the abnormal month of H-103 is flagged
bills, rises = sol.compare_months("H-103", sol.CONSUMPTION[2])
check("H-103 March rise flagged as unusual (%.1f%% > 25%%)" % rises[2],
      rises[2] > sol.UNUSUAL_RISE_PERCENT)

# TC-10: the next month falls back and shows a negative rise
check("H-103 April bill below March bill (negative rise)",
      bills[3] < bills[2] and rises[3] < 0)

print("\n%d test cases passed" % passed)
