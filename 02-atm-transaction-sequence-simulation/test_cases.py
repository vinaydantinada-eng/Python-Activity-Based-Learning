"""Automated test cases for Case Study 02 - ATM Transaction Sequence Simulation."""
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


def run(start, txs):
    return sol.process_transactions(start, txs, verbose=False)


# TC-01: a valid deposit is accepted and raises the balance
res = run(10000, [("T1", "D", 5000)])
check("valid deposit accepted, balance 10000 -> 15000",
      res[0] == 15000 and res[3] == 1 and res[4] == 0)

# TC-02: a valid withdrawal is accepted and lowers the balance
res = run(10000, [("T1", "W", 4000)])
check("valid withdrawal accepted, balance 10000 -> 6000",
      res[0] == 6000 and res[3] == 1)

# TC-03: withdrawal leading to balance below minimum is rejected
res = run(5000, [("T1", "W", 4500)])
check("withdrawal below minimum balance rejected, balance unchanged",
      res[0] == 5000 and res[4] == 1)

# TC-04: withdrawal exactly down to the minimum balance is allowed
res = run(5000, [("T1", "W", 4000)])
check("withdrawal down to exact minimum balance accepted", res[0] == 1000)

# TC-05: single withdrawal above Rs 20000 rejected
res = run(50000, [("T1", "W", 25000)])
check("withdrawal above single limit Rs 20000 rejected",
      res[4] == 1 and res[0] == 50000)

# TC-06: deposit above Rs 100000 rejected
res = run(10000, [("T1", "D", 150000)])
check("deposit above limit Rs 100000 rejected",
      res[4] == 1 and res[0] == 10000)

# TC-07: unknown transaction type rejected
res = run(10000, [("T1", "Z", 500)])
check("unknown transaction type rejected", res[4] == 1)

# TC-08: withdrawal below Rs 100 rejected
res = run(10000, [("T1", "W", 50)])
check("withdrawal below Rs 100 rejected", res[4] == 1)

# TC-09: daily withdrawal limit enforced
res = run(60000, [("T1", "W", 20000), ("T2", "W", 10000)])
check("daily limit Rs 25000: second withdrawal rejected",
      res[4] == 1 and res[5] == 20000 and res[0] == 40000)

# TC-10: a deposit does not reset the daily withdrawal counter
res = run(60000, [("T1", "W", 20000), ("T2", "D", 50000), ("T3", "W", 6000)])
check("deposit does not free up the daily withdrawal limit",
      res[4] == 1 and res[5] == 20000)

# TC-11: summary totals are consistent
res = run(12500, sol.TRANSACTIONS)
check("opening + deposits - withdrawals = closing",
      abs(12500 + res[1] - res[2] - res[0]) < 0.01)

# TC-12: accepted + rejected counts cover every transaction
res = run(12500, sol.TRANSACTIONS)
check("accepted + rejected = total transactions",
      res[3] + res[4] == len(sol.TRANSACTIONS))

print("\n%d test cases passed" % passed)
