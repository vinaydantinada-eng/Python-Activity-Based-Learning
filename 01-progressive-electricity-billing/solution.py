"""
Case Study 01: Progressive Electricity Billing
------------------------------------------------
Calculate household bills using multiple consumption slabs, fixed charges,
surcharges and rebates, then compare bills across several months and
identify unusual increases.

Syllabus used: variables, data types, operators, conditional statements,
loops, strings, lists, tuples, tuple operations and tuple unpacking.
No library is imported - only core Python 3 is used.
"""

# ------------------------------------------------------------------
# Tariff and policy constants (hypothetical values for this study)
# ------------------------------------------------------------------
FIXED_CHARGE = 50.0            # Rs. meter / fixed charge per month
SLAB_LIMITS = (100, 200, 400)  # slabs: 0-100, 101-200, 201-400, above 400
SLAB_RATES = (2.50, 4.20, 6.10, 7.80)   # Rs. per unit in each slab
DUTY_PERCENT = 5.0             # electricity duty applied on slab charge
SURCHARGE_PERCENT = 3.0        # extra surcharge when usage > 500 units
SURCHARGE_LIMIT = 500
REBATE_PERCENT = 2.0           # prompt-payment rebate on the total
UNUSUAL_RISE_PERCENT = 25.0    # month-on-month rise treated as unusual

HOUSEHOLDS = ["H-101", "H-102", "H-103"]

# Consumption in units for six successive months (index 0 = month 1)
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
CONSUMPTION = [
    (112, 118, 145, 160, 158, 170),   # H-101 - gently rising
    (240, 255, 310, 330, 420, 455),   # H-102 - sudden summer jump
    (88, 95, 250, 105, 98, 101),      # H-103 - one abnormal month
]


def slab_charge(units):
    """Progressive slab calculation using a loop over the slab tuples."""
    remaining = units
    charge = 0.0
    lower = 0
    for i in range(len(SLAB_LIMITS)):
        upper = SLAB_LIMITS[i]
        rate = SLAB_RATES[i]
        if remaining <= 0:
            break
        slab_units = upper - lower
        if remaining < slab_units:
            slab_units = remaining
        charge += slab_units * rate
        remaining -= slab_units
        lower = upper

    if remaining > 0:                      # last open-ended slab
        charge += remaining * SLAB_RATES[-1]

    return charge


def compute_bill(units):
    """Return (bill_amount, breakdown_lines) for one month's consumption."""
    lines = []

    energy = slab_charge(units)
    duty = energy * DUTY_PERCENT / 100.0

    surcharge = 0.0
    if units > SURCHARGE_LIMIT:
        surcharge = energy * SURCHARGE_PERCENT / 100.0

    gross = FIXED_CHARGE + energy + duty + surcharge
    rebate = gross * REBATE_PERCENT / 100.0
    total = gross - rebate

    lines.append("Energy charge (slabs) : Rs. %8.2f" % energy)
    lines.append("Fixed charge          : Rs. %8.2f" % FIXED_CHARGE)
    lines.append("Electricity duty %4.1f%% : Rs. %8.2f" % (DUTY_PERCENT, duty))
    if surcharge > 0:
        lines.append("Surcharge %4.1f%%        : Rs. %8.2f" % (SURCHARGE_PERCENT, surcharge))
    lines.append("Rebate %4.1f%%           : Rs. %8.2f" % (REBATE_PERCENT, -rebate))
    lines.append("TOTAL PAYABLE         : Rs. %8.2f" % total)

    return round(total, 2), lines


def compare_months(household, readings):
    """Print the month-wise comparison and flag unusual increases."""
    print("\n" + "=" * 62)
    print("  MONTH-WISE BILL COMPARISON  -  Household %s" % household)
    print("=" * 62)
    print("%-7s %-8s %-12s %-10s %s" % ("Month", "Units", "Bill (Rs.)", "Rise %", "Remark"))
    print("-" * 62)

    bills = []
    rises = []
    for i in range(len(readings)):
        units = readings[i]
        bill, _ = compute_bill(units)
        bills.append(bill)

        if i == 0:
            rise = 0.0
        else:
            prev = bills[i - 1]
            rise = (bill - prev) * 100.0 / prev
        rises.append(rise)

        remark = ""
        if i > 0 and rise > UNUSUAL_RISE_PERCENT:
            remark = "UNUSUAL INCREASE"
        elif i > 0 and rise < 0:
            remark = "lower than previous"

        print("%-7s %-8d %-12.2f %-10.1f %s" % (MONTHS[i], units, bill, rise, remark))

    print("-" * 62)
    avg = sum(bills) / len(bills)
    print("Average bill over %d months : Rs. %.2f" % (len(bills), avg))

    highest_index = 0
    for i in range(1, len(bills)):
        if bills[i] > bills[highest_index]:
            highest_index = i
    print("Highest bill : %s  (Rs. %.2f)" % (MONTHS[highest_index], bills[highest_index]))

    return bills, rises


def main():
    print("=" * 62)
    print("  PROGRESSIVE ELECTRICITY BILLING SYSTEM")
    print("=" * 62)

    # sample month-wise detail for the first household, full breakdown
    print("\nDETAILED BILL BREAKDOWN - H-101, month Mar (145 units):")
    _, lines = compute_bill(145)
    for line in lines:
        print("   " + line)

    all_bills = []
    for i in range(len(HOUSEHOLDS)):
        bills, rises = compare_months(HOUSEHOLDS[i], CONSUMPTION[i])
        all_bills.append(bills)

    # ------- which household had the sharpest single jump? -------
    print("\n" + "=" * 62)
    print("  UNUSUAL INCREASE SUMMARY")
    print("=" * 62)
    worst_household = ""
    worst_rise = 0.0
    worst_month = ""
    for i in range(len(HOUSEHOLDS)):
        for j in range(1, len(MONTHS)):
            rise = (all_bills[i][j] - all_bills[i][j - 1]) * 100.0 / all_bills[i][j - 1]
            if rise > UNUSUAL_RISE_PERCENT:
                print("  %s : %s -> %s : %+.1f%%  (Rs. %.2f -> Rs. %.2f)"
                      % (HOUSEHOLDS[i], MONTHS[j - 1], MONTHS[j], rise,
                         all_bills[i][j - 1], all_bills[i][j]))
                if rise > worst_rise:
                    worst_rise = rise
                    worst_household = HOUSEHOLDS[i]
                    worst_month = MONTHS[j]

    if worst_rise > 0:
        print("\n  Sharpest rise: %s in %s (%+.1f%%)."
              % (worst_household, worst_month, worst_rise))
        print("  Recommendation: verify meter reading and check for faulty appliances.")
    else:
        print("  No month showed an unusual increase.")

    print("\nAll values are hypothetical and used only for this activity.")


if __name__ == "__main__":
    main()
