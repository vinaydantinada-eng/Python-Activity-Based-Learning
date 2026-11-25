"""
Case Study 02: ATM Transaction Sequence Simulation
---------------------------------------------------
Process a sequence of deposits and withdrawals, maintain a simulated
balance, enforce withdrawal limits, reject invalid transactions and
produce a transaction summary.

Syllabus used: variables, data types, operators, conditional statements,
loops, strings, lists, tuples, tuple operations and tuple unpacking.
No library is imported - only core Python 3 is used.
"""

# ------------------------------------------------------------------
# Account and ATM rules (hypothetical values for this study)
# ------------------------------------------------------------------
STARTING_BALANCE = 12500.00
MINIMUM_BALANCE = 1000.00        # account must never go below this
DAILY_WITHDRAWAL_LIMIT = 25000.00
SINGLE_WITHDRAWAL_LIMIT = 20000.00
SINGLE_WITHDRAWAL_MIN = 100.00   # smallest note-slot withdrawal
DEPOSIT_LIMIT = 100000.00

# Each transaction tuple: (transaction_id, type, amount)
# type "D" = deposit, "W" = withdrawal
TRANSACTIONS = [
    ("TX01", "D", 5000.00),
    ("TX02", "W", 2000.00),
    ("TX03", "W", 15000.00),
    ("TX04", "W", 22000.00),      # above single withdrawal limit
    ("TX05", "D", 120000.00),     # above deposit limit
    ("TX06", "X", 500.00),        # unknown transaction type
    ("TX07", "W", 50.00),         # below minimum withdrawal
    ("TX08", "W", 4000.00),
    ("TX09", "D", 2500.00),
    ("TX10", "W", 13500.00),      # would breach minimum balance
]


def process_transactions(start_balance, transactions, verbose=True):
    """Run every transaction in order and return the summary data."""
    balance = start_balance
    total_deposits = 0.0
    total_withdrawn = 0.0
    withdrawn_today = 0.0         # used for the daily withdrawal limit
    accepted = 0
    rejected = 0

    if verbose:
        print("=" * 74)
        print("  ATM TRANSACTION SEQUENCE SIMULATION")
        print("=" * 74)
        print("  Opening balance : Rs. %.2f" % balance)
        print("  Rules: minimum balance Rs. %.2f, daily withdrawal limit Rs. %.2f,"
              % (MINIMUM_BALANCE, DAILY_WITHDRAWAL_LIMIT))
        print("         single withdrawal between Rs. %.2f and Rs. %.2f,"
              % (SINGLE_WITHDRAWAL_MIN, SINGLE_WITHDRAWAL_LIMIT))
        print("         deposit limit Rs. %.2f" % DEPOSIT_LIMIT)
        print("-" * 74)
        print("%-6s %-4s %-12s %-12s %-12s %s"
              % ("ID", "Type", "Amount", "Balance", "Status", "Reason if rejected"))
        print("-" * 74)

    for transaction in transactions:
        # ---- tuple unpacking ----
        tx_id, tx_type, amount = transaction

        reason = ""
        status = "ACCEPTED"

        if tx_type == "D":
            if amount <= 0:
                reason = "invalid deposit amount"
            elif amount > DEPOSIT_LIMIT:
                reason = "deposit above limit Rs. %.0f" % DEPOSIT_LIMIT
        elif tx_type == "W":
            if amount < SINGLE_WITHDRAWAL_MIN:
                reason = "below minimum withdrawal Rs. %.0f" % SINGLE_WITHDRAWAL_MIN
            elif amount > SINGLE_WITHDRAWAL_LIMIT:
                reason = "above single withdrawal limit Rs. %.0f" % SINGLE_WITHDRAWAL_LIMIT
            elif withdrawn_today + amount > DAILY_WITHDRAWAL_LIMIT:
                reason = "daily withdrawal limit would be crossed"
            elif balance - amount < MINIMUM_BALANCE:
                reason = "would leave balance below minimum Rs. %.0f" % MINIMUM_BALANCE
        else:
            reason = "unknown transaction type '%s'" % tx_type

        if reason != "":
            status = "REJECTED"
            rejected += 1
            if verbose:
                print("%-6s %-4s %-12.2f %-12.2f %-12s %s"
                      % (tx_id, tx_type, amount, balance, status, reason))
            continue

        # ---- apply the accepted transaction ----
        if tx_type == "D":
            balance += amount
            total_deposits += amount
        else:
            balance -= amount
            total_withdrawn += amount
            withdrawn_today += amount

        accepted += 1
        if verbose:
            print("%-6s %-4s %-12.2f %-12.2f %-12s %s"
                  % (tx_id, tx_type, amount, balance, status, "-"))

    if verbose:
        print("-" * 74)
    return (balance, total_deposits, total_withdrawn,
            accepted, rejected, withdrawn_today)


def main():
    summary = process_transactions(STARTING_BALANCE, TRANSACTIONS)

    # ---- tuple unpacking on the returned summary ----
    (closing_balance, total_deposits, total_withdrawn,
     accepted, rejected, withdrawn_today) = summary

    total = accepted + rejected
    print("\n" + "=" * 74)
    print("  TRANSACTION SUMMARY")
    print("=" * 74)
    print("  Transactions processed : %d" % total)
    print("  Accepted               : %d" % accepted)
    print("  Rejected               : %d" % rejected)
    print("  Success rate           : %.1f%%" % (accepted * 100.0 / total))
    print("-" * 74)
    print("  Opening balance        : Rs. %10.2f" % STARTING_BALANCE)
    print("  Total deposits         : Rs. %10.2f" % total_deposits)
    print("  Total withdrawals      : Rs. %10.2f" % total_withdrawn)
    print("  Closing balance        : Rs. %10.2f" % closing_balance)
    print("-" * 74)

    # ---- reuse the same account for a second sequence on another day ----
    print("\nNext day (limit counters reset):")
    next_day = [("TX11", "D", 20000.00), ("TX12", "W", 9000.00),
                ("TX13", "W", 9000.00), ("TX14", "W", 9000.00),
                ("TX15", "W", 9000.00)]
    new_summary = process_transactions(closing_balance, next_day)
    print("  Overnight closing balance : Rs. %.2f" % new_summary[0])

    print("\nNote: all transactions and figures are hypothetical.")

    # ---- quick self check ----
    if closing_balance < MINIMUM_BALANCE:
        print("WARNING: closing balance went below the minimum balance!")
    else:
        print("Check passed: closing balance never fell below Rs. %.2f."
              % MINIMUM_BALANCE)


if __name__ == "__main__":
    main()
