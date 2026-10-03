import os
import sys

cur_dir = os.path.dirname(os.path.abspath(__file__))
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
        # --- NEW SENTENCE BENCHMARK (Thammudu & Santoshanga) ---
        (
            "naa thammudu naatho chala santoshanga untadu, vadu nannu entha ga abhimanisthadu ante na matallo cheppalenu.",
            True,
            "నా తమ్ముడు నాతో చాలా సంతోషంగా ఉంటాడు, వాడు నన్ను ఎంత గా అభిమానిస్తాడు అంటె నా మాటల్లో చెప్పలేను.",
            "User Test 7: Full Sentence: naa thammudu naatho chala santoshanga untadu..."
        ),
        (
            "naa thammudu naatho chala santoshanga untadu, vadu nannu enthaga abhimanisthadu ante na matallo cheppalenu.",
            True,
            "నా తమ్ముడు నాతో చాలా సంతోషంగా ఉంటాడు, వాడు నన్ను ఎంతగా అభిమానిస్తాడు అంటె నా మాటల్లో చెప్పలేను.",
            "User Test 7b: Full Sentence with 'enthaga' compound"
        ),
        (
            "naa thamudu naatho chala santoshanga untadu, vadu nannu entha ga abhimanisthadu ante na matallo cheppalenu.",
            True,
            "నా తముడు నాతో చాలా సంతోషంగా ఉంటాడు, వాడు నన్ను ఎంత గా అభిమానిస్తాడు అంటె నా మాటల్లో చెప్పలేను.",
            "User Test 7c: Full Sentence with 'thamudu'"
        ),
        (
            "nuvvennanna cheppu, nuvvu naatho matlade samayamlo naaku vere phone vachindi, lekapothe nenenduku bayataki veltanu, sarele inko sari vellanu, enduku anta kopanga unnavo cheppu, lekapothe nenu matladanu.",
            True,
            "నువ్వెన్నన్నా చెప్పు, నువ్వు నాతో మాట్లాడే సమయంలో నాకు వేరే ఫోన్ వచ్చింది, లేకపోతే నేనెందుకు బయటకి వెళ్తాను, సరేలే ఇంకో సారి వెళ్లను, ఎందుకు అంత కోపంగా ఉన్నావో చెప్పు, లేకపోతే నేనూ మాట్లాడను.",
            "User Test 8: Real-World Conversational Benchmark (Phone, Matlade, Veltanu, Sarele, Velanu, Unnavo)"
        ),
        ("santoshanga", True, "సంతోషంగా", "Word Test: santoshanga -> సంతోషంగా (no ఙ)"),
        ("untadu", True, "ఉంటాడు", "Word Test: untadu -> ఉంటాడు"),
        ("vadu", True, "వాడు", "Word Test: vadu -> వాడు"),
        ("abhimanisthadu", True, "అభిమానిస్తాడు", "Word Test: abhimanisthadu -> అభిమానిస్తాడు (no స్థ)"),
        ("ante", True, "అంటె", "Word Test: ante -> అంటె"),
        ("cheppalenu", True, "చెప్పలేను", "Word Test: cheppalenu -> చెప్పలేను (long le)"),
        # --- ORIGINAL TESTS MUST STILL PASS ---
        ("nuvvu akkade undu vastunna", True, "నువ్వు అక్కడే ఉండు వస్తున్నా", "Original test 1: nuvvu akkade undu vastunna"),
        ("cheppamdi", True, "చెప్పండి", "Original test 2: cheppamdi -> చెప్పండి"),
        ("cheyyandi", True, "చెయ్యండి", "Original test 3: cheyyandi -> చెయ్యండి"),
        ("cheyandi", True, "చేయండి", "Original test 3: cheyandi -> చేయండి"),
        ("randi", True, "రండి", "Original test 4: randi -> రండి"),
        ("choodandi", True, "చూడండి", "Original test 4: choodandi -> చూడండి"),
        ("casual", True, "క్యాజువల్", "Loanword Test 1: casual -> క్యాజువల్"),
        ("typing", True, "టైపింగ్", "Loanword Test 2: typing -> టైపింగ్"),
        ("casual typing sariga pani cheyyadam ledu", True, "క్యాజువల్ టైపింగ్ సరిగా పని చెయ్యడం లేదు", "Full Sentence Loanword Test: casual typing sariga pani cheyyadam ledu"),
        ("matlade", True, "మాట్లాడే", "Word Test: matlade -> మాట్లాడే"),
        ("nenenduku", True, "నేనెందుకు", "Word Test: nenenduku -> నేనెందుకు"),
        ("veltanu", True, "వెళ్తాను", "Word Test: veltanu -> వెళ్తాను"),
        ("sarele", True, "సరేలే", "Word Test: sarele -> సరేలే"),
        ("unnavo", True, "ఉన్నావో", "Word Test: unnavo -> ఉన్నావో"),
        ("phone", True, "ఫోన్", "Word Test: phone -> ఫోన్"),
        ("inko sari vellanu", True, "ఇంకో సారి వెళ్లను", "Context Test: inko sari vellanu -> ఇంకో సారి వెళ్లను"),
        ("lekapothe nenu matladanu", True, "లేకపోతే నేనూ మాట్లాడను", "Context Test: lekapothe nenu matladanu -> లేకపోతే నేనూ మాట్లాడను"),
        ("telugu", False, "తెలుగు", "Casual disabled exact engine check: 'telugu' -> 'తెలుగు'"),

        # --- NEW SEMANTIC CONTEXT TESTS ---
        ("akkada evaru leru", True, "అక్కడ ఎవరూ లేరు", "Semantic Polarity 1: Negative verb 'leru' triggers emphatic deergham 'ఎవరూ'"),
        ("akkada evaru unnaru", True, "అక్కడ ఎవరు ఉన్నారు", "Semantic Polarity 2: Positive verb 'unnaru' keeps standard interrogative 'ఎవరు'"),
        ("ekkada ledu", True, "ఎక్కడా లేదు", "Generic Unseen 1: Negative verb 'ledu' triggers emphatic deergham 'ఎక్కడా'"),
        ("ekkada unnadu", True, "ఎక్కడ ఉన్నాడు", "Generic Unseen 2: Positive verb 'unnadu' keeps standard interrogative 'ఎక్కడ'"),
        ("emaina annaara", True, "ఏమైనా అన్నారా", "Emphatic interrogative: emaina annaara -> ఏమైనా అన్నారా"),
        ("kala chusanu", True, "కల చూశాను", "Polysemy 1: kala chusanu -> కల చూశాను"),
        ("kinda padi", True, "కింద పడి", "Polysemy 2: kinda padi -> కింద పడి"),
        ("naluguru padi mandi", True, "నలుగురు పది మంది", "Polysemy 3: naluguru padi mandi -> నలుగురు పది మంది"),

        # --- GENERIC TYPO TOLERANCE TESTS ---
        ("sayantram", True, "సాయంత్రం", "Typo Test 1a: sayantram -> సాయంత్రం"),
        ("sayamtram", True, "సాయంత్రం", "Typo Test 1b: sayamtram (nasal m) -> సాయంత్రం"),
        ("sayantrm", True, "సాయంత్రం", "Typo Test 1c: sayantrm (missing a) -> సాయంత్రం"),
        ("vellaka", True, "వెళ్ళాక", "Typo Test 2a: vellaka -> వెళ్ళాక"),
        ("velaka", True, "వెళ్ళాక", "Typo Test 2b: velaka (single l) -> వెళ్ళాక"),
        ("vellakka", True, "వెళ్ళాక", "Typo Test 2c: vellakka (geminate kk) -> వెళ్ళాక"),

        # --- ISOLATION TESTS (RTS EXACT UNTOUCHED VS CASUAL) ---
        ("avnu", False, "ఔను", "Exact Isolation Test: avnu -> ఔను (RTS untouched for exact users)"),
        ("avunu", True, "అవును", "Casual Isolation Test: avunu -> అవును (Casual fix)"),
        ("avnu", True, "అవును", "Casual Isolation Test: avnu -> అవును (Casual fix)"),
        ("nadavaalsina", True, "నడవాల్సిన", "Word Test: nadavaalsina -> నడవాల్సిన (no toxic 'av'->ౌ)"),
        ("naDavaalsina", True, "నడవాల్సిన", "Word Test: naDavaalsina -> నడవాల్సిన (retroflex D)"),
        ("nadavalsina", True, "నడవాల్సిన", "Word Test: nadavalsina -> నడవాల్సిన"),
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

    # 3. Interactive TypingBuffer retroactive correction check
    from engine.buffer import TypingBuffer
    buf = TypingBuffer(casual_enabled=True)
    for ch in "akkada":
        buf.add(ch)
    buf.commit_word()
    for ch in "evaru":
        buf.add(ch)
    buf.commit_word()

    retro_triggered = False
    retro_text = ""
    for ch in "leru":
        _, out_t, retro = buf.add(ch)
        if retro:
            retro_triggered = True
            _, retro_text = retro

    buf_passed = retro_triggered and ("ఎవరూ లేరు" in retro_text)
    print(f"[{'PASS' if buf_passed else 'FAIL'}] Real-time TypingBuffer retroactive correction ('evaru' -> 'ఎవరూ' on 'leru'): {buf_passed} ({retro_text})")
    if not buf_passed:
        all_passed = False

    # 4. Next-Word Prediction & Tab-to-accept checks
    print("\n--- NEXT WORD PREDICTION CHECKS ---")
    pred_buf = TypingBuffer(casual_enabled=True)

    # Test 4a: "akkada " -> suggestion should show "ఎవరు" or "ఎవరూ"
    for ch in "akkada":
        pred_buf.add(ch)
    pred_buf.commit_word()
    sug_akkada = pred_buf.get_suggestion()
    sugs_akkada = pred_buf.get_suggestions()
    pred_passed_1 = sug_akkada in ["ఎవరు", "ఎవరూ"]
    print(f"[{'PASS' if pred_passed_1 else 'FAIL'}] Prediction after 'akkada ': '{sug_akkada}' (expected 'ఎవరు' or 'ఎవరూ')")
    if not pred_passed_1:
        all_passed = False

    # Test 4b: Multi-candidate ranking (returns top 3 candidates)
    pred_passed_multi = (1 <= len(sugs_akkada) <= 3) and (sug_akkada in sugs_akkada)
    print(f"[{'PASS' if pred_passed_multi else 'FAIL'}] Multi-candidate ranking after 'akkada': {sugs_akkada}")
    if not pred_passed_multi:
        all_passed = False

    # Test 4c: Tab accept -> window advances with accepted word
    pred_buf.commit_word_with_telugu(sug_akkada)
    tab_accepted = (pred_buf.prev_word_telugu == sug_akkada) and (pred_buf.prev_prev_word == "అక్కడ")
    print(f"[{'PASS' if tab_accepted else 'FAIL'}] Tab accept advances window: prev='{pred_buf.prev_word_telugu}', prev_prev='{pred_buf.prev_prev_word}'")
    if not tab_accepted:
        all_passed = False

    # Test 4d: "emi " -> suggestion should show "లేదు" or "ఉంది"
    pred_buf.commit_sentence()
    for ch in "emi":
        pred_buf.add(ch)
    pred_buf.commit_word()
    sug_emi = pred_buf.get_suggestion()
    pred_passed_2 = sug_emi in ["లేదు", "ఉంది"]
    print(f"[{'PASS' if pred_passed_2 else 'FAIL'}] Prediction after 'emi ': '{sug_emi}' (expected 'లేదు' or 'ఉంది')")
    if not pred_passed_2:
        all_passed = False

    # Test 4e: Casual disabled -> no suggestion
    exact_buf = TypingBuffer(casual_enabled=False)
    for ch in "akkada":
        exact_buf.add(ch)
    exact_buf.commit_word()
    no_sug = exact_buf.get_suggestion() == ""
    print(f"[{'PASS' if no_sug else 'FAIL'}] Exact mode (casual=False) yields NO suggestion: '{exact_buf.get_suggestion()}'")
    if not no_sug:
        all_passed = False

    # Test 4f: Dynamic prefix autocomplete while typing next word
    prefix_buf = TypingBuffer(casual_enabled=True)
    for ch in "repu ":
        if ch == " ":
            prefix_buf.commit_word()
        else:
            prefix_buf.add(ch)
    prefix_buf.add('v')
    expected_bs = prefix_buf.get_current_out_len()
    prefix_sugs = prefix_buf.get_suggestions()
    prefix_passed = any(s.startswith("వ") for s in prefix_sugs)
    print(f"[{'PASS' if prefix_passed else 'FAIL'}] Prefix autocomplete after 'repu ' + 'v' -> 'వ': {prefix_sugs}")
    if not prefix_passed:
        all_passed = False

    # Test 4g: Mid-word Tab autocomplete replaces prefix correctly
    bs_count, to_insert = prefix_buf.accept_suggestion()
    tab_prefix_passed = (bs_count == expected_bs) and to_insert.endswith(" ")
    print(f"[{'PASS' if tab_prefix_passed else 'FAIL'}] Mid-word Tab autocomplete: backspaces={bs_count}, inserted='{to_insert}'")
    if not tab_prefix_passed:
        all_passed = False

    # Test 4h: Standalone grammatical particle filter (no 'కి', 'లో', 'తో', etc.)
    from engine.predictor import INVALID_STANDALONE_WORDS
    particle_clean = not any(w in INVALID_STANDALONE_WORDS for w in sugs_akkada)
    print(f"[{'PASS' if particle_clean else 'FAIL'}] Non-standalone particle exclusion: {particle_clean}")
    if not particle_clean:
        all_passed = False

    # 5. UI Playground in-place editor check
    print("\n--- UI PLAYGROUND IN-PLACE SIMULATION CHECKS ---")
    try:
        from PyQt6.QtWidgets import QApplication
        app = QApplication.instance()
        if not app:
            app = QApplication(["--platform", "offscreen"])
        from ui.settings import PlaygroundEditor
        editor = PlaygroundEditor(casual_enabled=True)

        # Test 5a: simulate typing "nuvvu "
        editor.simulate_text("nuvvu ")
        play_text_1 = editor.toPlainText().strip()
        play_passed_1 = (play_text_1 == "నువ్వు")
        print(f"[{'PASS' if play_passed_1 else 'FAIL'}] Playground in-place typing 'nuvvu ' -> '{play_text_1}'")
        if not play_passed_1:
            all_passed = False

        # Test 5b: Tab accept prediction
        sug = editor.buffer.get_suggestion()
        editor.accept_suggestion()
        play_text_2 = editor.toPlainText().strip()
        play_passed_2 = (play_text_2.startswith("నువ్వు") and len(play_text_2) > len("నువ్వు"))
        print(f"[{'PASS' if play_passed_2 else 'FAIL'}] Playground Tab-autocomplete accepts suggestion: '{play_text_2}'")
        if not play_passed_2:
            all_passed = False

        # Test 5c: Retroactive correction in playground
        editor.simulate_text("akkada evaru leru ")
        play_text_3 = editor.toPlainText().strip()
        play_passed_3 = ("ఎవరూ లేరు" in play_text_3)
        print(f"[{'PASS' if play_passed_3 else 'FAIL'}] Playground retroactive correction 'akkada evaru leru' -> '{play_text_3}'")
        if not play_passed_3:
            all_passed = False
    except Exception as e:
        print(f"[FAIL] Playground test encountered error: {e}")
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
