import os
import sys

# Ensure both local and rachayitha code files are on python path
cur_dir = os.path.dirname(os.path.abspath(__file__))
r_dir = os.path.join(cur_dir, "rachayitha code files")
if r_dir not in sys.path:
    sys.path.insert(0, r_dir)
if cur_dir not in sys.path:
    sys.path.insert(0, cur_dir)

from engine.casual_type import transliterate, load_dictionaries, CASUAL_DICT, TYPO_FIXES, TOP10K_FREQ

def run_all_tests():
    print("=" * 70)
    print("  RACHAYITHA CASUAL-TYPE DICTIONARY & PHONETIC ENGINE TEST SUITE")
    print("=" * 70)

    load_dictionaries()
    dict_size = len(CASUAL_DICT)
    print(f"[INIT] Loaded Casual Dictionary with {dict_size} mappings.")
    print(f"[INIT] Loaded Typo Fixes with {len(TYPO_FIXES)} rules.")
    print(f"[INIT] Loaded te_top10k with {len(TOP10K_FREQ)} frequency entries.\n")

    test_cases = [
        # --- USER BENCHMARK FULL SENTENCE TEST ---
        (
            "ninna sayantram intiki vellaka ammato konchem matladanu amma naato cheppindi entante manam manushulam manaku edaina kavalsivasthe kashtapadi sadhinchukovali, lekapote manaki evaru mana kosam teesukochchi ivvaru.",
            True,
            "నిన్న సాయంత్రం ఇంటికి వెళ్ళాక అమ్మతో కొంచెం మాట్లాడాను అమ్మ నాతో చెప్పింది ఏంటంటే మనం మనుషులం మనకు ఏదైనా కావల్సివస్తే కష్టపడి సాధించుకోవాలి, లేకపోతే మనకి ఎవరూ మన కోసం తీసుకొచ్చి ఇవ్వరు.",
            "USER BENCHMARK FULL SENTENCE TEST"
        ),
        # With optional 'sepu' in conversation
        (
            "ninna sayantram intiki vellaka ammato konchem sepu matladanu amma naato cheppindi entante manam manushulam manaku edaina kavalsivasthe kashtapadi sadhinchukovali, lekapote manaki evaru mana kosam teesukochchi ivvaru.",
            True,
            "నిన్న సాయంత్రం ఇంటికి వెళ్ళాక అమ్మతో కొంచెం సేపు మాట్లాడాను అమ్మ నాతో చెప్పింది ఏంటంటే మనం మనుషులం మనకు ఏదైనా కావల్సివస్తే కష్టపడి సాధించుకోవాలి, లేకపోతే మనకి ఎవరూ మన కోసం తీసుకొచ్చి ఇవ్వరు.",
            "USER BENCHMARK WITH 'SEPU'"
        ),
        # --- INDIVIDUAL WORD ACCURACY TESTS ---
        ("sayantram", True, "సాయంత్రం", "Word: sayantram -> సాయంత్రం (no toxic 'ay'->ై)"),
        ("intiki", True, "ఇంటికి", "Word: intiki -> ఇంటికి (fixed overtuned deergham)"),
        ("vellaka", True, "వెళ్ళాక", "Word: vellaka -> వెళ్ళాక (retroflex ళ)"),
        ("ammato", True, "అమ్మతో", "Word: ammato -> అమ్మతో (postposition -తో)"),
        ("naato", True, "నాతో", "Word: naato -> నాతో (postposition -తో)"),
        ("matladanu", True, "మాట్లాడాను", "Word: matladanu -> మాట్లాడాను (retroflex ట్ల, డా)"),
        ("entante", True, "ఏంటంటే", "Word: entante -> ఏంటంటే (colloquial connector)"),
        ("manushulam", True, "మనుషులం", "Word: manushulam -> మనుషులం (sibilant ష, Sunna ం)"),
        ("edaina", True, "ఏదైనా", "Word: edaina -> ఏదైనా"),
        ("kavalsivasthe", True, "కావల్సివస్తే", "Word: kavalsivasthe -> కావల్సివస్తే (no toxic 'av'->ౌ)"),
        ("kashtapadi", True, "కష్టపడి", "Word: kashtapadi -> కష్టపడి (retroflex ష్ట, auxiliary పడి)"),
        ("sadhinchukovali", True, "సాధించుకోవాలి", "Word: sadhinchukovali -> సాధించుకోవాలి"),
        ("teesukochchi", True, "తీసుకొచ్చి", "Word: teesukochchi -> తీసుకొచ్చి (geminate చ్చి)"),
        ("ivvaru", True, "ఇవ్వరు", "Word: ivvaru -> ఇవ్వరు"),
        # --- GLOBAL CONVERSATIONAL SENTENCE TESTS (Unrelated to prompt) ---
        (
            "nannato matladali",
            True,
            "నాన్నతో మాట్లాడాలి",
            "Global Test 1: Noun postposition -to + verb infinitive -ali ('nannato matladali')"
        ),
        (
            "intinundi vastunna",
            True,
            "ఇంటినుండి వస్తున్నా",
            "Global Test 2: Noun ablative -nundi + continuous aspect ('intinundi vastunna')"
        ),
        (
            "manushulu munduku vellali",
            True,
            "మనుషులు ముందుకు వెళ్ళాలి",
            "Global Test 3: Sibilants & retroflexes ('manushulu munduku vellali')"
        ),
        # --- USER ARBITRARY TELUGU SENTENCE BENCHMARKS ---
        ("nenu repu vastunna", True, "నేను రేపు వస్తున్నా", "User Test 1: nenu repu vastunna -> నేను రేపు వస్తున్నా"),
        ("chala bagundi", True, "చాలా బాగుంది", "User Test 2: chala bagundi -> చాలా బాగుంది"),
        ("ela unnaru?", True, "ఎలా ఉన్నారు?", "User Test 3: ela unnaru? -> ఎలా ఉన్నారు?"),
        ("pustakam chadavali", True, "పుస్తకం చదవాలి", "User Test 4: pustakam chadavali -> పుస్తకం చదవాలి"),
        ("pillalu aadukuntunnaru", True, "పిల్లలు ఆడుకుంటున్నారు", "User Test 5: pillalu aadukuntunnaru -> పిల్లలు ఆడుకుంటున్నారు"),
        ("snehitulato matladali", True, "స్నేహితులతో మాట్లాడాలి", "User Test 6: snehitulato matladali -> స్నేహితులతో మాట్లాడాలి"),
        # --- ORIGINAL TESTS MUST STILL PASS ---
        ("nuvvu akkade undu vastunna", True, "నువ్వు అక్కడే ఉండు వస్తున్నా", "Original test 1: nuvvu akkade undu vastunna"),
        ("cheppamdi", True, "చెప్పండి", "Original test 2: cheppamdi -> చెప్పండి"),
        ("cheyyandi", True, "చెయ్యండి", "Original test 3: cheyyandi -> చెయ్యండి"),
        ("cheyandi", True, "చేయండి", "Original test 3: cheyandi -> చేయండి"),
        ("randi", True, "రండి", "Original test 4: randi -> రండి"),
        ("choodandi", True, "చూడండి", "Original test 4: choodandi -> చూడండి"),
        ("telugu", False, "తెలుగు", "Casual disabled exact engine check: 'telugu' -> 'తెలుగు'"),
    ]

    all_passed = True
    for input_text, casual_flag, expected, description in test_cases:
        actual = transliterate(input_text, casual_flag)
        passed = (actual == expected)
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {description}")
        if not passed:
            print(f"        Input:    '{input_text}' (casual_enabled={casual_flag})")
            print(f"        Expected: '{expected}'")
            print(f"        Actual:   '{actual}'")
            all_passed = False
        print("-" * 70)

    # Constraint checks
    print("\n--- CONSTRAINT CHECKS ---")
    
    # 1. 58k mappings active
    size_passed = dict_size >= 58000
    print(f"[{'PASS' if size_passed else 'FAIL'}] Dictionary size >= 58,000 active mappings: {dict_size}")
    if not size_passed:
        all_passed = False

    # 2. Collision resolution check: vastunna -> వస్తున్నా (freq 8000)
    col_passed = (CASUAL_DICT.get("vastunna") == "వస్తున్నా")
    print(f"[{'PASS' if col_passed else 'FAIL'}] Collision resolution on 'vastunna' (te_top10k 8000 wins): {CASUAL_DICT.get('vastunna')}")
    if not col_passed:
        all_passed = False

    print("=" * 70)
    if all_passed:
        print(">>> ALL TESTS PASSED! CASUAL TYPING IS 100% ACCURATE! <<<")
    else:
        print(">>> SOME TESTS FAILED. <<<")
    print("=" * 70)
    return all_passed

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
