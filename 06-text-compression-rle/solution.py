"""
Case Study 06: Text Compression Using Character Runs
-----------------------------------------------------
Encode a string by grouping consecutive repeated characters and compare
original and encoded lengths, including cases where encoding is not
beneficial.

Syllabus used: variables, data types, operators, conditional statements,
loops, strings, lists.
No library is imported - only core Python 3 is used.

Encoding format (run-length encoding):
    each run of a character becomes  character + count
    e.g.  "AAAABBBCC"  ->  "A4B3C2"
Runs of a single character are written with count 1 so decoding stays
unambiguous.
"""

# Sample strings covering strongly repetitive, mixed and non-repetitive text
SAMPLES = [
    "AAAABBBCCDAA",
    "WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWB",
    "ABCDEF",
    "A",
    "",
    "aaabbbaaabbbaaabbb",
    "mississippi",
    "AAAAA",
]


def encode(text):
    """Run-length encode text. Returns '' for an empty string."""
    if len(text) == 0:
        return ""

    encoded = ""
    run_char = text[0]
    run_count = 1

    for i in range(1, len(text)):
        if text[i] == run_char:
            run_count += 1
        else:
            encoded += run_char + str(run_count)
            run_char = text[i]
            run_count = 1

    encoded += run_char + str(run_count)
    return encoded


def decode(encoded):
    """Decode a run-length encoded string back to the original text."""
    decoded = ""
    i = 0
    while i < len(encoded):
        ch = encoded[i]
        i += 1

        # collect the full number that follows the character
        number = ""
        while i < len(encoded) and "0" <= encoded[i] <= "9":
            number += encoded[i]
            i += 1

        if number == "":
            # malformed record: character without a count
            return None

        count = int(number)
        decoded += ch * count

    return decoded


def savings(original_length, encoded_length):
    """Percentage saving of the encoded length over the original."""
    if original_length == 0:
        return 0.0
    return (original_length - encoded_length) * 100.0 / original_length


def main():
    print("=" * 78)
    print("  TEXT COMPRESSION USING CHARACTER RUNS (RUN-LENGTH ENCODING)")
    print("=" * 78)
    print("%-22s %-28s %6s %6s %8s  %s"
          % ("Original", "Encoded", "Orig", "Enc", "Saved", "Verdict"))
    print("-" * 78)

    total_original = 0
    total_encoded = 0
    beneficial = 0
    harmful = 0
    neutral = 0

    for i in range(len(SAMPLES)):
        text = SAMPLES[i]
        encoded = encode(text)

        orig_len = len(text)
        enc_len = len(encoded)
        total_original += orig_len
        total_encoded += enc_len

        saved = savings(orig_len, enc_len)

        if enc_len < orig_len:
            verdict = "compressed"
            beneficial += 1
        elif enc_len > orig_len:
            verdict = "NOT beneficial"
            harmful += 1
        else:
            verdict = "no change"
            neutral += 1

        # shorten long strings so the table stays readable
        shown_original = text
        if len(shown_original) > 20:
            shown_original = shown_original[0:17] + "..."
        shown_encoded = encoded
        if len(shown_encoded) > 26:
            shown_encoded = shown_encoded[0:23] + "..."

        print("%-22s %-28s %6d %6d %7.1f%%  %s"
              % (shown_original, shown_encoded, orig_len, enc_len, saved, verdict))

    print("-" * 78)
    print("  Total original length : %d characters" % total_original)
    print("  Total encoded length  : %d characters" % total_encoded)
    print("  Overall saving        : %.1f%%"
          % savings(total_original, total_encoded))
    print("  Strings compressed    : %d   not beneficial: %d   unchanged: %d"
          % (beneficial, harmful, neutral))

    # ---------------- round-trip check ----------------
    print("\n" + "-" * 78)
    print("  ROUND-TRIP VERIFICATION (decode(encode(x)) = x)")
    print("-" * 78)
    all_ok = True
    for i in range(len(SAMPLES)):
        text = SAMPLES[i]
        encoded = encode(text)
        decoded = decode(encoded)
        if decoded == text:
            print("  Sample %d: OK" % (i + 1))
        else:
            all_ok = False
            print("  Sample %d: MISMATCH" % (i + 1))

    if all_ok:
        print("\n  All samples decoded back to the original text exactly.")

    # ---------------- why some strings do not compress ----------------
    print("\n" + "-" * 78)
    print("  OBSERVATION")
    print("-" * 78)
    print("  A run of length 1 becomes two characters (letter + '1'), so text")
    print("  without repeated letters (like ABCDEF) grows by 100%. Compression")
    print("  only pays off when the average run length is greater than 2.")
    print("\n  Example long run: %s" % encode("A" * 12))
    print("  Example no runs : %s (longer than the original)" % encode("ABCDEF"))
    print("\nAll sample strings are hypothetical and used only for this activity.")


if __name__ == "__main__":
    main()
