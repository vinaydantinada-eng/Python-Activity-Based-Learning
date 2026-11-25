"""
Case Study 09: Tuple-Based Product Catalogue Audit
---------------------------------------------------
Store product identifiers, prices and stock quantities in tuples;
detect invalid records, calculate inventory values and identify items
requiring replenishment.

Syllabus used: variables, data types, operators, conditional statements,
loops, strings, lists, tuples, tuple operations and unpacking.
No library is imported - only core Python 3 is used.
"""

# ------------------------------------------------------------------
# Audit rules (hypothetical values for this study)
# ------------------------------------------------------------------
REORDER_LEVEL = 20        # stock at or below this needs replenishment
MAX_PRICE = 5000.00       # any price above this is treated as a typo
MAX_UNIT_PRICE = 100000   # sanity check on price

# Catalogue tuples: (product_code, product_name, price, stock, reorder_qty)
CATALOGUE = (
    ("P101", "Notebook A5",       45.50,  120,  50),
    ("P102", "Gel Pen Blue",      10.00,   15, 100),      # below reorder level
    ("P103", "Geometry Box",      95.00,   40,  30),
    ("P104", "Highlighter Set",  180.00,    8,  40),      # low stock
    ("P105", "Stapler Large",    260.00,    0,  25),      # out of stock
    ("P106", "Marker Black",      35.00,  210, 100),
    ("P107", "Drawing Sheet",      8.50,  500, 200),
    ("P108", "Calculator FX",   1250.00,   12,  10),      # low stock, high value
    ("P109", "File Folder",       25.00,   95,  50),
    ("P110", "Ruler 30cm",         0.00,   60,  20),      # INVALID price
    ("P111", "Glue Stick",        -12.00,  30,  20),      # INVALID price
    ("P112", "Sketch Pens 12",   320.00,  -5,  30),       # INVALID stock
    ("P113", "",                 55.00,   45,  20),       # INVALID (no name)
    ("P103", "Geometry Box",      95.00,   40,  30),      # DUPLICATE code
    ("P114", "Desk Organiser",  7800.00,    6,  10),      # price above limit
    ("P115", "Wax Crayons",      110.00,  140,  60),
)


def validate_record(record):
    """Return a list of problems with one catalogue tuple."""
    problems = []

    code, name, price, stock, reorder_qty = record        # tuple unpacking

    if len(code) != 4 or code[0] != "P":
        problems.append("product code '%s' must be 'P' + 3 digits" % code)
    else:
        for i in range(1, 4):
            if code[i] < "0" or code[i] > "9":
                problems.append("product code '%s' has a non-digit character" % code)
                break

    if len(name) < 3:
        problems.append("product name is missing or too short")

    if price <= 0:
        problems.append("price %.2f is not positive" % price)
    elif price > MAX_PRICE:
        problems.append("price %.2f is above the sanity limit %.2f"
                        % (price, MAX_PRICE))

    if stock < 0:
        problems.append("stock quantity %d cannot be negative" % stock)

    if reorder_qty <= 0:
        problems.append("reorder quantity %d must be positive" % reorder_qty)

    return problems


def find_duplicates(catalogue):
    """Return a list of product codes that appear more than once."""
    duplicates = []
    seen = []

    for record in catalogue:
        code = record[0]
        if code in seen:
            if code not in duplicates:
                duplicates.append(code)
        else:
            seen.append(code)

    return duplicates


def main():
    print("=" * 86)
    print("  TUPLE-BASED PRODUCT CATALOGUE AUDIT")
    print("=" * 86)
    print("  Records supplied : %d" % len(CATALOGUE))
    print("  Reorder level    : stock <= %d units" % REORDER_LEVEL)
    print("  Price sanity limit: Rs. %.2f" % MAX_PRICE)

    # ---------------- validation pass ----------------
    print("\n" + "-" * 86)
    print("  VALIDATION")
    print("-" * 86)

    invalid_codes = []
    for i in range(len(CATALOGUE)):
        record = CATALOGUE[i]
        problems = validate_record(record)
        if len(problems) > 0:
            code, name, price, stock, reorder_qty = record
            print("  Record %2d  (%s):" % (i + 1, code))
            for p in problems:
                print("      - %s" % p)
            if code not in invalid_codes:
                invalid_codes.append(code)

    duplicates = find_duplicates(CATALOGUE)
    if len(duplicates) > 0:
        print("\n  DUPLICATE product codes:")
        for code in duplicates:
            occurrences = 0
            for record in CATALOGUE:
                if record[0] == code:
                    occurrences += 1
            print("      - %s appears %d times" % (code, occurrences))

    if len(invalid_codes) == 0 and len(duplicates) == 0:
        print("  No invalid or duplicate records found.")
    else:
        print("\n  %d invalid record(s), %d duplicate code(s)."
              % (len(invalid_codes), len(duplicates)))

    # ---------------- valid records table ----------------
    print("\n" + "-" * 86)
    print("  INVENTORY VALUE (valid records only)")
    print("-" * 86)
    print("%-6s %-18s %10s %7s %10s %14s  %s"
          % ("Code", "Product", "Price", "Stock", "Reorder", "Value", "Status"))
    print("-" * 86)

    counted_codes = []
    total_value = 0.0
    total_units = 0
    replenish_list = []
    highest_value = 0.0
    highest_name = ""

    for record in CATALOGUE:
        code, name, price, stock, reorder_qty = record       # unpack

        problems = validate_record(record)
        if len(problems) > 0:
            continue                                          # skip bad rows

        if code in counted_codes:
            continue                                          # skip duplicates
        counted_codes.append(code)

        value = price * stock
        total_value += value
        total_units += stock

        if value > highest_value:
            highest_value = value
            highest_name = name

        status = "OK"
        if stock == 0:
            status = "OUT OF STOCK"
            replenish_list.append((code, name, stock, reorder_qty))
        elif stock <= REORDER_LEVEL:
            status = "LOW - REORDER"
            replenish_list.append((code, name, stock, reorder_qty))

        print("%-6s %-18s %10.2f %7d %10d %14.2f  %s"
              % (code, name, price, stock, reorder_qty, value, status))

    print("-" * 86)
    print("  Valid products   : %d" % len(counted_codes))
    print("  Total units      : %d" % total_units)
    print("  Total stock value: Rs. %.2f" % total_value)
    print("  Highest value    : %s (Rs. %.2f)" % (highest_name, highest_value))

    # ---------------- replenishment plan ----------------
    print("\n" + "-" * 86)
    print("  REPLENISHMENT PLAN (stock <= %d)" % REORDER_LEVEL)
    print("-" * 86)

    if len(replenish_list) == 0:
        print("  No product needs replenishment.")
    else:
        print("%-6s %-18s %7s %10s %12s"
              % ("Code", "Product", "Stock", "Reorder Qty", "Cost (Rs.)"))
        print("-" * 86)

        replenish_cost = 0.0
        for item in replenish_list:
            code, name, stock, reorder_qty = item              # unpack again
            # find the price of this product from the catalogue
            price = 0.0
            for record in CATALOGUE:
                if record[0] == code:
                    price = record[2]
                    break
            cost = price * reorder_qty
            replenish_cost += cost
            print("%-6s %-18s %7d %10d %12.2f"
                  % (code, name, stock, reorder_qty, cost))

        print("-" * 86)
        print("  Estimated replenishment cost: Rs. %.2f" % replenish_cost)

    # ---------------- category split by price band ----------------
    print("\n" + "-" * 86)
    print("  PRICE BAND SPLIT (valid records)")
    print("-" * 86)

    bands = [("Below Rs 50", 0, 50), ("Rs 50 - 200", 50, 200),
             ("Rs 200 - 500", 200, 500), ("Above Rs 500", 500, 100000)]
    for band_name, low, high in bands:          # unpacking the band tuples
        count = 0
        band_value = 0.0
        for record in CATALOGUE:
            code, name, price, stock, reorder_qty = record
            if len(validate_record(record)) > 0 or code not in counted_codes:
                continue
            if price >= low and price < high:
                count += 1
                band_value += price * stock
        print("  %-14s : %2d product(s), stock value Rs. %10.2f"
              % (band_name, count, band_value))

    print("\nAll product data is hypothetical and used only for this activity.")


if __name__ == "__main__":
    main()
