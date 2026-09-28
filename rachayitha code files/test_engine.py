from engine.transliterator import transliterate

test_cases = [
    ("n", "న్"),
    ("na", "న"),
    ("N", "ణ్"),
    ("Na", "ణ"),
    ("nn", "న్న్"),
    ("nna", "న్న"),
    ("k", "క్"),
    ("ka", "క"),
    ("ksh", "క్ష్"),
    ("ksha", "క్ష"),
    ("Ksha", "క్ష"),
    ("telugu", "తెలుగు"),
    ("amma", "అమ్మ"),
    ("kRuShNa", "కృష్ణ"),
    ("bhArat", "భారత్"),
    ("jagan", "జగన్"),
    ("rachayitha", "రచయిత"),
]

def run_tests():
    print("Testing Halant-First Transliteration Engine:")
    print("-" * 50)
    all_passed = True
    for inp, expected in test_cases:
        actual = transliterate(inp)
        passed = actual == expected
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] '{inp}' -> '{actual}' (expected: '{expected}')")
        if not passed:
            all_passed = False
    print("-" * 50)
    if all_passed:
        print("ALL TESTS PASSED! Halant-first logic is functioning perfectly.")
    else:
        print("Some tests failed.")

if __name__ == "__main__":
    run_tests()
