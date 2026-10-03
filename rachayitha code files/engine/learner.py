import os
import sys
import json
import time
import shutil
from typing import Dict, List, Optional, Tuple, Any

try:
    from .paths import get_config_dir
except ImportError:
    def get_config_dir():
        appdata = os.environ.get('APPDATA') or os.path.expanduser('~')
        cfg_dir = os.path.join(appdata, 'Rachayitha')
        os.makedirs(cfg_dir, exist_ok=True)
        return cfg_dir

class SelfLearningEngine:
    """
    Rachayitha Adaptive Self-Learning Engine.
    
    100% Offline, Privacy-First Architecture:
    - Stored strictly locally in %APPDATA%/Rachayitha/user_learned.json
    - Sub-millisecond (0ms) in-memory lookups during active typing
    - Safe atomic writes to prevent file corruption
    - Captures backspace-correction patterns, candidate pill selections, and personal bigrams
    """
    def __init__(self):
        self.config_dir = get_config_dir()
        self.file_path = os.path.join(self.config_dir, "user_learned.json")
        self.enabled = True
        
        # In-memory storage for 0ms lookup latency
        self.word_overrides: Dict[str, Dict[str, Any]] = {}
        self.candidate_boosts: Dict[str, Dict[str, int]] = {}
        self.personal_bigrams: Dict[str, int] = {}
        self.history: List[Dict[str, Any]] = []
        
        self._dirty = False
        self._load()

    def _load(self):
        if not os.path.exists(self.file_path):
            return
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.enabled = data.get("enabled", True)
            self.word_overrides = data.get("word_overrides", {})
            self.candidate_boosts = data.get("candidate_boosts", {})
            self.personal_bigrams = data.get("personal_bigrams", {})
            self.history = data.get("history", [])
        except Exception as e:
            print(f"[SelfLearningEngine] Error loading learned profile: {e}")

    def save(self):
        """
        Safely write learned profile atomically to user_learned.json
        """
        try:
            data = {
                "version": 1,
                "enabled": self.enabled,
                "word_overrides": self.word_overrides,
                "candidate_boosts": self.candidate_boosts,
                "personal_bigrams": self.personal_bigrams,
                "history": self.history[-100:],  # Retain last 100 events
                "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
            tmp_path = self.file_path + ".tmp"
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            shutil.move(tmp_path, self.file_path)
            self._dirty = False
        except Exception as e:
            print(f"[SelfLearningEngine] Error saving learned profile: {e}")

    def set_enabled(self, enabled: bool):
        self.enabled = enabled
        self.save()

    def is_enabled(self) -> bool:
        return self.enabled

    # -------------------------------------------------------------
    # 1. Backspace-Retype Correction Learning
    # -------------------------------------------------------------
    def learn_backspace_correction(
        self,
        erased_eng: str,
        erased_telugu: str,
        new_eng: str,
        new_telugu: str
    ) -> bool:
        """
        Triggered when a user erases an unwanted word and replaces it with a new word.
        
        If user typed 'chala' -> 'చల', erased it, and typed 'chaala' -> 'చాలా':
        We associate the casual input 'chala' directly with 'చాలా'!
        """
        if not self.enabled:
            return False

        erased_eng = erased_eng.strip().lower()
        new_eng = new_eng.strip().lower()
        erased_telugu = erased_telugu.strip()
        new_telugu = new_telugu.strip()

        if not erased_eng or not new_telugu or erased_telugu == new_telugu:
            return False

        # 1. Learn override for the erased casual Roman word
        existing = self.word_overrides.get(erased_eng, {})
        new_count = existing.get("count", 0) + 1
        self.word_overrides[erased_eng] = {
            "tel": new_telugu,
            "count": new_count,
            "last_used": time.strftime("%Y-%m-%d %H:%M:%S"),
            "source": "backspace_correction"
        }

        # 2. Boost candidate score
        if erased_eng not in self.candidate_boosts:
            self.candidate_boosts[erased_eng] = {}
        self.candidate_boosts[erased_eng][new_telugu] = self.candidate_boosts[erased_eng].get(new_telugu, 0) + 20000
        if erased_telugu:
            self.candidate_boosts[erased_eng][erased_telugu] = self.candidate_boosts[erased_eng].get(erased_telugu, 0) - 5000

        # 3. If new_eng was also typed and differs, register new_eng as well
        if new_eng and new_eng != erased_eng:
            n_existing = self.word_overrides.get(new_eng, {})
            self.word_overrides[new_eng] = {
                "tel": new_telugu,
                "count": n_existing.get("count", 0) + 1,
                "last_used": time.strftime("%Y-%m-%d %H:%M:%S"),
                "source": "backspace_replacement"
            }

        # 4. Log event in audit history
        self.history.append({
            "type": "backspace_correction",
            "from_eng": erased_eng,
            "from_tel": erased_telugu,
            "to_eng": new_eng,
            "to_tel": new_telugu,
            "time": time.strftime("%Y-%m-%d %H:%M:%S")
        })

        self.save()
        return True

    # -------------------------------------------------------------
    # 2. Candidate Selection Learning (Pill Click / Shortcut)
    # -------------------------------------------------------------
    def learn_candidate_selection(
        self,
        roman: str,
        chosen_telugu: str,
        rejected_telugu: Optional[str] = None,
        prev_word: Optional[str] = None
    ):
        """
        Triggered when a user clicks a candidate pill in the suggestion overlay.
        Boosts the chosen candidate so it moves up in future predictions.
        """
        if not self.enabled:
            return

        roman = (roman or "").strip().lower()
        chosen_telugu = (chosen_telugu or "").strip()
        if not chosen_telugu:
            return

        if roman:
            # Boost candidate weight
            if roman not in self.candidate_boosts:
                self.candidate_boosts[roman] = {}
            self.candidate_boosts[roman][chosen_telugu] = self.candidate_boosts[roman].get(chosen_telugu, 0) + 15000
            if rejected_telugu and rejected_telugu != chosen_telugu:
                self.candidate_boosts[roman][rejected_telugu] = self.candidate_boosts[roman].get(rejected_telugu, 0) - 3000

            # Increment override count if chosen multiple times
            existing = self.word_overrides.get(roman, {})
            count = existing.get("count", 0) + 1
            self.word_overrides[roman] = {
                "tel": chosen_telugu,
                "count": count,
                "last_used": time.strftime("%Y-%m-%d %H:%M:%S"),
                "source": "candidate_selection"
            }

            self.history.append({
                "type": "candidate_selection",
                "from_eng": roman,
                "from_tel": rejected_telugu or "",
                "to_tel": chosen_telugu,
                "time": time.strftime("%Y-%m-%d %H:%M:%S")
            })

        # Learn contextual bigram transition if previous word exists
        if prev_word:
            self.learn_bigram(prev_word, chosen_telugu)

        self.save()

    # -------------------------------------------------------------
    # 3. Bigram & Collocation Learning
    # -------------------------------------------------------------
    def learn_bigram(self, w1: str, w2: str):
        """
        Learns personal user transition between two consecutive words.
        """
        if not self.enabled:
            return
        w1 = (w1 or "").strip()
        w2 = (w2 or "").strip()
        if not w1 or not w2 or w1 == w2:
            return

        pair_key = f"{w1}_{w2}"
        self.personal_bigrams[pair_key] = self.personal_bigrams.get(pair_key, 0) + 1
        self._dirty = True

    # -------------------------------------------------------------
    # 4. Manual Custom Words (User Dictionary)
    # -------------------------------------------------------------
    def add_manual_override(self, roman: str, telugu: str) -> bool:
        """
        Explicitly registers a user-defined mapping (e.g. custom slang, names, dialect).
        """
        roman = (roman or "").strip().lower()
        telugu = (telugu or "").strip()
        if not roman or not telugu:
            return False

        self.word_overrides[roman] = {
            "tel": telugu,
            "count": self.word_overrides.get(roman, {}).get("count", 0) + 10,
            "last_used": time.strftime("%Y-%m-%d %H:%M:%S"),
            "source": "manual"
        }
        if roman not in self.candidate_boosts:
            self.candidate_boosts[roman] = {}
        self.candidate_boosts[roman][telugu] = 50000

        self.history.append({
            "type": "manual_add",
            "from_eng": roman,
            "to_tel": telugu,
            "time": time.strftime("%Y-%m-%d %H:%M:%S")
        })
        self.save()
        return True

    def remove_override(self, roman: str) -> bool:
        roman = (roman or "").strip().lower()
        removed = False
        if roman in self.word_overrides:
            del self.word_overrides[roman]
            removed = True
        if roman in self.candidate_boosts:
            del self.candidate_boosts[roman]
            removed = True
        if removed:
            self.save()
        return removed

    def clear_all(self):
        """
        Resets all learned user data.
        """
        self.word_overrides.clear()
        self.candidate_boosts.clear()
        self.personal_bigrams.clear()
        self.history.clear()
        self.save()

    # -------------------------------------------------------------
    # 5. Queries & Resolution Lookups
    # -------------------------------------------------------------
    def get_override(self, roman: str) -> Optional[str]:
        if not self.enabled:
            return None
        item = self.word_overrides.get(roman.strip().lower())
        if item and isinstance(item, dict):
            return item.get("tel")
        elif isinstance(item, str):
            return item
        return None

    def get_candidate_boost(self, roman: str, cand_telugu: str) -> int:
        if not self.enabled:
            return 0
        r = roman.strip().lower()
        return self.candidate_boosts.get(r, {}).get(cand_telugu.strip(), 0)

    def get_personal_bigram_count(self, w1: str, w2: str) -> int:
        if not self.enabled:
            return 0
        return self.personal_bigrams.get(f"{w1.strip()}_{w2.strip()}", 0)

    def get_personal_transitions(self, prev_word: str) -> List[Tuple[str, int]]:
        """
        Returns list of (next_word, count) from personal bigrams for a given prev_word.
        """
        if not self.enabled or not prev_word:
            return []
        prefix = f"{prev_word.strip()}_"
        results = []
        for pair_key, count in self.personal_bigrams.items():
            if pair_key.startswith(prefix):
                w2 = pair_key[len(prefix):]
                if w2:
                    results.append((w2, count))
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_overrides": len(self.word_overrides),
            "total_boosts": sum(len(v) for v in self.candidate_boosts.values()),
            "total_bigrams": len(self.personal_bigrams),
            "total_events": len(self.history),
            "enabled": self.enabled
        }

    # -------------------------------------------------------------
    # 6. Import / Export
    # -------------------------------------------------------------
    def export_profile(self, target_path: str) -> bool:
        try:
            data = {
                "version": 1,
                "exported_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "word_overrides": self.word_overrides,
                "candidate_boosts": self.candidate_boosts,
                "personal_bigrams": self.personal_bigrams
            }
            with open(target_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"[SelfLearningEngine] Export error: {e}")
            return False

    def import_profile(self, source_path: str, merge: bool = True) -> bool:
        try:
            with open(source_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            new_overrides = data.get("word_overrides", {})
            new_boosts = data.get("candidate_boosts", {})
            new_bigrams = data.get("personal_bigrams", {})
            
            if merge:
                self.word_overrides.update(new_overrides)
                for k, v in new_boosts.items():
                    if k not in self.candidate_boosts:
                        self.candidate_boosts[k] = {}
                    self.candidate_boosts[k].update(v)
                self.personal_bigrams.update(new_bigrams)
            else:
                self.word_overrides = new_overrides
                self.candidate_boosts = new_boosts
                self.personal_bigrams = new_bigrams
                
            self.save()
            return True
        except Exception as e:
            print(f"[SelfLearningEngine] Import error: {e}")
            return False


# Singleton instance
_GLOBAL_LEARNER: Optional[SelfLearningEngine] = None

def get_learner() -> SelfLearningEngine:
    global _GLOBAL_LEARNER
    if _GLOBAL_LEARNER is None:
        _GLOBAL_LEARNER = SelfLearningEngine()
    return _GLOBAL_LEARNER
