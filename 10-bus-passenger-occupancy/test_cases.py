"""Automated test cases for Case Study 10 - Bus Passenger Occupancy Simulation."""
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


NAMES = ["A", "B", "C"]        # three fake stops for isolated tests

# TC-01: capacity constant
check("total capacity = 50 seats + 20 standing = 70", sol.TOTAL_CAPACITY == 70)

# TC-02: valid record has no problems
check("valid stop record accepted",
      sol.validate_stop_record((0, 10, 0), 8) == [])

# TC-03: negative boarding rejected
check("negative boarding rejected",
      len(sol.validate_stop_record((0, -3, 0), 8)) == 1)

# TC-04: negative alighting rejected
check("negative alighting rejected",
      len(sol.validate_stop_record((0, 3, -2), 8)) == 1)

# TC-05: stop outside route rejected
check("stop index 9 rejected",
      len(sol.validate_stop_record((9, 3, 0), 8)) == 1)

# TC-06: unrealistic boarding rejected
check("boarding 75 rejected (above 60)",
      len(sol.validate_stop_record((0, 75, 0), 8)) == 1)

# TC-07: zero-boarding middle stop is valid
check("stop with 0 boarding is valid (everyone alights)",
      sol.validate_stop_record((1, 0, 5), 8) == [])

# TC-08: simple trip updates the count correctly
results = sol.simulate_trip(NAMES, [(0, 20, 0), (1, 5, 8), (2, 2, 7)], 70)
check("trip counts: 20 -> 17 -> 12",
      results[0][3] == 20 and results[1][3] == 17 and results[2][3] == 12)

# TC-09: over-capacity status is produced
results = sol.simulate_trip(NAMES, [(0, 60, 0), (1, 20, 0), (2, 0, 5)], 70)
check("over capacity flagged at stop 1",
      results[1][4] == "OVER CAPACITY")

# TC-10: exactly-full status is produced
results = sol.simulate_trip(NAMES, [(0, 50, 0), (1, 20, 0), (2, 0, 5)], 70)
check("exactly 70 passengers marks FULL", results[1][4] == "FULL")

# TC-11: almost-full status is produced
results = sol.simulate_trip(NAMES, [(0, 60, 0), (1, 0, 0), (2, 0, 5)], 70)
check("60 of 70 passengers (>= 85%) marks ALMOST FULL",
      results[0][4] == "ALMOST FULL")

# TC-12: alighting more than onboard is rejected
results = sol.simulate_trip(NAMES, [(0, 10, 0), (1, 2, 15), (2, 0, 0)], 70)
check("alighting 15 with 10 onboard rejected",
      results[1][4] == "INVALID")

# TC-13: negative boarding rejected by the simulation
results = sol.simulate_trip(NAMES, [(0, 10, 0), (1, -2, 0), (2, 0, 0)], 70)
check("negative boarding rejected in simulation",
      results[1][4] == "INVALID")

# TC-14: rejection does not change the passenger count
check("rejected stop leaves onboard count unchanged",
      results[2][3] == 10)

# TC-15: the sample trip peaks at 74 passengers
results = sol.simulate_trip(sol.ROUTE_STOPS, sol.BOARDING_ALIGHTING, sol.TOTAL_CAPACITY)
peak = 0
for r in results:
    if r[4] != "INVALID" and r[3] > peak:
        peak = r[3]
check("sample trip peaks at 74 passengers", peak == 74)

# TC-16: the sample trip has exactly 2 capacity violations
violations = 0
for r in results:
    if r[4] == "OVER CAPACITY":
        violations += 1
check("sample trip has 2 capacity violations", violations == 2)

# TC-17: total boarded and alighted reconcile with final count
boarded = 0
alighted = 0
for r in results:
    if r[4] != "INVALID":
        boarded += r[1]
        alighted += r[2]
check("boarded - alighted = final onboard count",
      boarded - alighted == results[-1][3])

# TC-18: every route stop appears once in the sample trip
check("8 stops produce 8 results", len(results) == len(sol.ROUTE_STOPS))

print("\n%d test cases passed" % passed)
