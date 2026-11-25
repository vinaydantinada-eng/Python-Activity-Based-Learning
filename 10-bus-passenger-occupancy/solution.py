"""
Case Study 10: Bus Passenger Occupancy Simulation
--------------------------------------------------
Process boarding and alighting counts across multiple stops, calculate
passenger counts at each stop, and flag any capacity violations.

Syllabus used: variables, data types, operators, conditional statements,
loops, strings, lists, tuples, tuple operations and unpacking.
No library is imported - only core Python 3 is used.
"""

# ------------------------------------------------------------------
# Bus and route constants (hypothetical values for this study)
# ------------------------------------------------------------------
SEATING_CAPACITY = 50
STANDING_CAPACITY = 20
TOTAL_CAPACITY = SEATING_CAPACITY + STANDING_CAPACITY   # 70 passengers max
MAX_AT_ONE_STOP = 60          # safety check on the input data

# Route stops and (boarding, alighting) tuples for one trip
ROUTE_STOPS = [
    "Central Bus Stand",
    "Gandhi Nagar",
    "Railway Station",
    "Benz Circle",
    "Auto Nagar",
    "Ramavarappadu",
    "Gannavaram",
    "Airport Road",
]

# (stop index, boarding, alighting)  - stop 0 is the start
BOARDING_ALIGHTING = (
    (0, 25, 0),      # board at the bus stand
    (1, 34, 3),
    (2, 26, 8),      # rush hour - bus goes over capacity here
    (3, 14, 17),
    (4, 9, 21),
    (5, 6, 15),
    (6, 4, 9),
    (7, 2, 12),
)


def validate_stop_record(record, num_stops):
    """Return a list of problems with one (stop, boarding, alighting) tuple."""
    problems = []

    stop, boarding, alighting = record       # tuple unpacking

    if stop < 0 or stop >= num_stops:
        problems.append("stop index %d is outside the route" % stop)
    if boarding < 0:
        problems.append("boarding count %d cannot be negative" % boarding)
    if alighting < 0:
        problems.append("alighting count %d cannot be negative" % alighting)
    if boarding > MAX_AT_ONE_STOP:
        problems.append("boarding %d seems unrealistic (max %d)"
                        % (boarding, MAX_AT_ONE_STOP))
    if alighting > MAX_AT_ONE_STOP:
        problems.append("alighting %d seems unrealistic (max %d)"
                        % (alighting, MAX_AT_ONE_STOP))

    return problems


def simulate_trip(stop_names, records, capacity):
    """Run the trip and return a list of per-stop result tuples."""
    passengers = 0
    results = []

    for record in records:
        stop, boarding, alighting = record         # unpack

        problems = validate_stop_record(record, len(stop_names))
        if len(problems) > 0:
            # record the problem and skip the stop
            results.append((stop, boarding, alighting, passengers, "INVALID", problems))
            continue

        if alighting > passengers:
            # more people get off than are on the bus
            results.append((stop, boarding, alighting, passengers,
                            "INVALID", ["alighting %d exceeds onboard %d"
                                        % (alighting, passengers)]))
            continue

        passengers = passengers - alighting + boarding

        status = "OK"
        if passengers > capacity:
            status = "OVER CAPACITY"
        elif passengers == capacity:
            status = "FULL"
        elif passengers >= capacity * 0.85:
            status = "ALMOST FULL"

        results.append((stop, boarding, alighting, passengers, status, []))

    return results


def main():
    print("=" * 84)
    print("  BUS PASSENGER OCCUPANCY SIMULATION")
    print("=" * 84)
    print("  Route  : %d stops" % len(ROUTE_STOPS))
    print("  Capacity: %d seats + %d standing = %d passengers"
          % (SEATING_CAPACITY, STANDING_CAPACITY, TOTAL_CAPACITY))
    print("-" * 84)

    results = simulate_trip(ROUTE_STOPS, BOARDING_ALIGHTING, TOTAL_CAPACITY)

    print("%-4s %-22s %7s %8s %8s %6s  %s"
          % ("Stop", "Name", "Board", "Alight", "Onboard", "Util", "Status"))
    print("-" * 84)

    total_boarded = 0
    total_alighted = 0
    violations = 0
    peak_passengers = 0
    peak_stop = ""
    invalid_stops = 0

    for result in results:
        stop, boarding, alighting, onboard, status, problems = result     # unpack

        if status == "INVALID":
            invalid_stops += 1
            name = ROUTE_STOPS[stop] if 0 <= stop < len(ROUTE_STOPS) else "?"
            print("%-4d %-22s %7d %8s %8s %6s  %s"
                  % (stop, name, boarding, "-", onboard, "-", "INVALID DATA"))
            for p in problems:
                print("        -> %s" % p)
            continue

        total_boarded += boarding
        total_alighted += alighting

        util = onboard * 100.0 / TOTAL_CAPACITY

        if status == "OVER CAPACITY":
            violations += 1

        if onboard > peak_passengers:
            peak_passengers = onboard
            peak_stop = ROUTE_STOPS[stop]

        print("%-4d %-22s %7d %8d %8d %5.1f%%  %s"
              % (stop, ROUTE_STOPS[stop], boarding, alighting, onboard, util, status))

    print("-" * 84)

    # ---------------- trip summary ----------------
    print("\n" + "-" * 84)
    print("  TRIP SUMMARY")
    print("-" * 84)
    print("  Total boarded at all stops : %d" % total_boarded)
    print("  Total alighted             : %d" % total_alighted)
    print("  Passengers still on board  : %d" % results[-1][3])
    print("  Peak passengers            : %d at %s (%.1f%% of capacity)"
          % (peak_passengers, peak_stop, peak_passengers * 100.0 / TOTAL_CAPACITY))
    print("  Capacity violations        : %d" % violations)
    print("  Invalid stop records       : %d" % invalid_stops)

    # ---------------- reconciliation check ----------------
    print("\n" + "-" * 84)
    print("  RECONCILIATION CHECK")
    print("-" * 84)
    final_onboard = results[-1][3]
    expected = total_boarded - total_alighted
    print("  Boarded - alighted = %d - %d = %d" % (total_boarded, total_alighted, expected))
    print("  Final passengers on board = %d" % final_onboard)
    if expected == final_onboard:
        print("  Check PASSED: passenger count reconciles.")
    else:
        print("  Check FAILED: counts do not reconcile.")

    # ---------------- second trip with problem data ----------------
    print("\n" + "-" * 84)
    print("  SECOND TRIP - WITH PROBLEM RECORDS (validation demo)")
    print("-" * 84)

    problem_trip = (
        (0, 30, 0),
        (1, 25, 10),
        (2, 15, 45),      # more alighting than onboard
        (3, -5, 5),       # negative boarding
        (4, 4, 9),
        (9, 3, 1),        # stop outside the route
        (6, 75, 2),       # unrealistic boarding count
    )

    problem_results = simulate_trip(ROUTE_STOPS, problem_trip, TOTAL_CAPACITY)
    for result in problem_results:
        stop, boarding, alighting, onboard, status, problems = result
        name = ROUTE_STOPS[stop] if 0 <= stop < len(ROUTE_STOPS) else "?"
        if status == "INVALID":
            print("  Stop %d (%s): board %d, alight %d -> REJECTED"
                  % (stop, name, boarding, alighting))
            for p in problems:
                print("        -> %s" % p)
        else:
            print("  Stop %d (%s): board %d, alight %d -> onboard %d (%s)"
                  % (stop, name, boarding, alighting, onboard, status))

    print("\nAll counts are hypothetical and used only for this activity.")


if __name__ == "__main__":
    main()
