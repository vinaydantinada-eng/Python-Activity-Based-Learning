"""Automated test cases for Case Study 06 - Text Compression Using Character Runs."""
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


# TC-01: simple mixed runs
check("encode('AAAABBBCCDAA') = 'A4B3C2D1A2'",
      sol.encode("AAAABBBCCDAA") == "A4B3C2D1A2")

# TC-02: no repetitions - every run has length 1
check("encode('ABCDEF') = 'A1B1C1D1E1F1'",
      sol.encode("ABCDEF") == "A1B1C1D1E1F1")

# TC-03: single character
check("encode('A') = 'A1'", sol.encode("A") == "A1")

# TC-04: empty string
check("encode('') = ''", sol.encode("") == "")

# TC-05: multi-digit run count
check("encode('A'*12) = 'A12'", sol.encode("A" * 12) == "A12")

# TC-06: alternating characters never merge
check("encode('abab') = 'a1b1a1b1'", sol.encode("abab") == "a1b1a1b1")

# TC-07: decode a simple string
check("decode('A4B3C2D1A2') = 'AAAABBBCCDAA'",
      sol.decode("A4B3C2D1A2") == "AAAABBBCCDAA")

# TC-08: decode with two-digit counts
check("decode('A12B2') = 'A'*12 + 'BB'",
      sol.decode("A12B2") == "A" * 12 + "BB")

# TC-09: round trip on every sample
ok = True
for text in sol.SAMPLES:
    if sol.decode(sol.encode(text)) != text:
        ok = False
check("round trip decode(encode(x)) = x for all samples", ok)

# TC-10: round trip on a long random-looking string of runs
long_text = "pppppqqqqqrrrrrrssss"
check("round trip on 'pppppqqqqqrrrrrrssss' works",
      sol.decode(sol.encode(long_text)) == long_text)

# TC-11: malformed code returns None
check("decode('A') = None (missing count)", sol.decode("A") is None)

# TC-12: savings percentage correct
check("savings(12, 10) = 16.67%",
      abs(sol.savings(12, 10) - 16.6667) < 0.01)

# TC-13: negative savings when encoding grows
check("savings(6, 12) = -100%", abs(sol.savings(6, 12) + 100.0) < 0.01)

# TC-14: savings of empty string is zero (no divide by zero)
check("savings(0, 0) = 0", sol.savings(0, 0) == 0.0)

# TC-15: non-beneficial case detected
text = "ABCDEF"
check("encoding ABCDEF is longer than the original",
      len(sol.encode(text)) > len(text))

# TC-16: beneficial case detected
text = "AAAAA"
check("encoding AAAAA is shorter than the original",
      len(sol.encode(text)) < len(text))

print("\n%d test cases passed" % passed)
