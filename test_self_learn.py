import os
import sys
import shutil
import tempfile

cur_dir = os.path.dirname(os.path.abspath(__file__))
r_dir = os.path.join(cur_dir, "rachayitha code files")
if r_dir not in sys.path:
    sys.path.insert(0, r_dir)
if cur_dir not in sys.path:
    sys.path.insert(0, cur_dir)

from engine.learner import SelfLearningEngine, get_learner
from engine.buffer import TypingBuffer
from engine.casual_type import transliterate_word_candidates, transliterate
from engine.predictor import NextWordPredictor

def run_self_learning_tests():
    print("=" * 70)
    print("  RACHAYITHA ADAPTIVE SELF-LEARNING ENGINE TEST SUITE")
    print("=" * 70)

    # Use a temporary directory for clean sandbox testing
    temp_dir = tempfile.mkdtemp()
    test_json = os.path.join(temp_dir, "user_learned.json")

    try:
        # 1. Initialize clean test learner
        learner = get_learner()
        learner.file_path = test_json
        learner.clear_all()
        print("[PASS] Initialized clean sandbox profile.")

        # -------------------------------------------------------------
        # TEST 1: Backspace-Retype Loop Detection
        # Scenario: User types 'velanu', screen displays 'వెళ్లను' (I won't go).
        # User completely erases it with backspaces, then types 'vellanu' -> 'వెళ్ళాను' (I went), and presses Space.
        # -------------------------------------------------------------
        buffer = TypingBuffer(casual_enabled=True)
        # Type 'velanu'
        for ch in "velanu":
            buffer.add(ch)
        initial_out = buffer.last_telugu
        print(f"\n[STEP 1] User typed 'velanu' -> initial Telugu: '{initial_out}'")

        # User presses backspace until empty
        while buffer.is_active():
            buffer.backspace()
        print(f"[STEP 2] User erased word completely. Pending retype state: {buffer.pending_retype is not None}")
        assert buffer.pending_retype is not None, "Pending retype must be registered on word erasure!"
        assert buffer.pending_retype["erased_eng"] == "velanu"
        assert buffer.pending_retype["erased_telugu"] == initial_out

        # User retypes 'vellanu'
        for ch in "vellanu":
            buffer.add(ch)
        replacement_out = buffer.last_telugu
        print(f"[STEP 3] User retyped 'vellanu' -> new Telugu: '{replacement_out}'")
        assert initial_out != replacement_out, "Initial and replacement Telugu must differ to trigger correction!"

        # User commits with Space
        buffer.commit_word()
        print(f"[STEP 4] User pressed Space to commit.")

        # VERIFICATION 1:
        # Check that 'velanu' is now learned and overrides to 'వెళ్ళాను'
        learned_override = learner.get_override("velanu")
        print(f"[VERIFY] learner.get_override('velanu') = '{learned_override}'")
        assert learned_override == "వెళ్ళాను", f"Expected 'వెళ్ళాను', got '{learned_override}'"

        cands = transliterate_word_candidates("velanu")
        cand_words = [c.get("tel") if isinstance(c, dict) else c for c in cands]
        print(f"[VERIFY] Candidates for 'velanu': {cand_words}")
        assert cand_words[0] == "వెళ్ళాను", f"Expected 'వెళ్ళాను' as top candidate, got '{cand_words[0]}'"
        print("[PASS] Test 1 (Backspace-Retype Loop Learning) PASSED!")

        # -------------------------------------------------------------
        # TEST 2: Post-Commit Erasure & Replacement
        # Scenario: User typed 'namaste' -> 'నమస్తే', committed with space.
        # Then hits backspace to erase space & word, types 'namaskaram' -> 'నమస్కారం', commits.
        # -------------------------------------------------------------
        buffer2 = TypingBuffer(casual_enabled=True)
        for ch in "namaste":
            buffer2.add(ch)
        namaste_tel = buffer2.last_telugu
        print(f"\n[STEP 1] User typed 'namaste' -> committed: '{namaste_tel}'")
        buffer2.commit_word() # Committed with space

        # User deletes space
        buffer2.notify_external_backspace()
        assert buffer2.pending_retype is not None, "External backspace must track committed word!"

        # User types 'namaskaram'
        for ch in "namaskaram":
            buffer2.add(ch)
        replacement_tel = buffer2.last_telugu
        print(f"[STEP 2] User replaced with 'namaskaram' -> '{replacement_tel}'")
        assert namaste_tel != replacement_tel, "Initial and replacement words must differ!"
        buffer2.commit_word()

        learned_override = learner.get_override("namaste")
        print(f"[VERIFY] Post-commit learning: 'namaste' -> '{learned_override}'")
        assert learned_override == replacement_tel, f"Expected '{replacement_tel}', got '{learned_override}'"
        print("[PASS] Test 2 (Post-Commit Erasure Learning) PASSED!")

        # -------------------------------------------------------------
        # TEST 3: Candidate Selection Positive Reinforcement (Pill Click)
        # -------------------------------------------------------------
        buffer3 = TypingBuffer(casual_enabled=True)
        for ch in "matladanu":
            buffer3.add(ch)
        # Select secondary candidate
        target_cand = "మాట్లాడను"
        bs_count, to_insert = buffer3.accept_suggestion(target_cand)
        print(f"\n[STEP] Candidate pill accepted: '{target_cand}'")
        assert target_cand in to_insert
        learned_matladanu = learner.get_override("matladanu")
        print(f"[VERIFY] Candidate selection recorded: 'matladanu' -> '{learned_matladanu}'")
        assert learned_matladanu == target_cand
        print("[PASS] Test 3 (Candidate Selection Pill Learning) PASSED!")

        # -------------------------------------------------------------
        # TEST 4: Personal Bigram / Collocation Learning
        # Scenario: User writes 'రచయిత' followed by 'బాగుంది'
        # -------------------------------------------------------------
        buffer4 = TypingBuffer(casual_enabled=True)
        for ch in "rachayitha":
            buffer4.add(ch)
        buffer4.commit_word()
        for ch in "bagundi":
            buffer4.add(ch)
        buffer4.commit_word()

        bi_count = learner.get_personal_bigram_count("రచయిత", "బాగుంది")
        print(f"\n[VERIFY] Personal bigram count ('రచయిత', 'బాగుంది') = {bi_count}")
        assert bi_count >= 1, "Personal bigram must be incremented!"

        # Next word predictor should surface 'బాగుంది'
        predictor = NextWordPredictor()
        next_words = predictor.predict_next("రచయిత", top_k=3)
        print(f"[VERIFY] Predictor predictions after 'రచయిత': {next_words}")
        assert "బాగుంది" in next_words, f"Expected 'బాగుంది' in predictions {next_words}"
        print("[PASS] Test 4 (Personal Collocation & Next-Word Prediction) PASSED!")

        # -------------------------------------------------------------
        # TEST 5: Manual Custom Mapping & Profile Export/Import
        # -------------------------------------------------------------
        learner.add_manual_override("hyd", "హైదరాబాద్")
        cands_hyd = transliterate_word_candidates("hyd")
        assert (cands_hyd[0].get("tel") if isinstance(cands_hyd[0], dict) else cands_hyd[0]) == "హైదరాబాద్"
        print("\n[VERIFY] Manual custom mapping 'hyd' -> 'హైదరాబాద్' works instantly!")

        # Export
        export_file = os.path.join(temp_dir, "export.json")
        assert learner.export_profile(export_file), "Export must succeed!"
        assert os.path.exists(export_file)

        # Clear and verify empty
        learner.clear_all()
        assert learner.get_override("hyd") is None

        # Re-import
        assert learner.import_profile(export_file), "Import must succeed!"
        assert learner.get_override("hyd") == "హైదరాబాద్"
        print("[PASS] Test 5 (Manual Custom Words & Export/Import Profile) PASSED!")

        print("\n" + "=" * 70)
        print("  ALL 5 SELF-LEARNING TESTS PASSED SUCCESSFULLY! (100% RELIABILITY)")
        print("=" * 70)

    finally:
        # Cleanup test environment and restore default
        shutil.rmtree(temp_dir, ignore_errors=True)
        # Reload default learner profile
        learner = get_learner()
        learner.file_path = os.path.join(learner.config_dir, "user_learned.json")
        learner._load()

if __name__ == "__main__":
    run_self_learning_tests()
