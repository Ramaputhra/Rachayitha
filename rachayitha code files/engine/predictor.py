import math
from collections import defaultdict
from typing import List, Optional

try:
    from .lm import TeluguLM
except ImportError:
    from engine.lm import TeluguLM

# Non-standalone particles and suffixes that must not be predicted as next standalone words
INVALID_STANDALONE_WORDS = {
    "కి", "లో", "తో", "ను", "కు", "వ", "ల", "పై", "లు", "ని", "గా", "ఓ",
    "రూ", "మ", "ప", "త", "ప్ర", "చే", "క", "చేసి", "అని", "యొక్క"
}

# Permissible conversational reduplications
ALLOWED_REDUPLICATIONS = {"మళ్ళీ", "రోజూ", "చాలా", "మంచి", "కొంచెం"}

class NextWordPredictor:
    """
    Production-ready Context-Aware Next-Word & Prefix Autocomplete Predictor.
    
    Architectural Pillars:
    1. Multi-tier statistical scoring: Trigram context + Bigram transition + Unigram baseline priors.
    2. Zero-keystroke next-word prediction triggered at word boundaries (Space).
    3. Prefix-aware real-time autocomplete as characters of the next word are typed.
    4. Reduplication & grammatical particle filtering (eliminates suffix fragments).
    5. In-memory indexing and LRU caching for sub-millisecond (0ms) zero-latency UI response.
    """
    def __init__(self, lm: Optional[TeluguLM] = None):
        self.lm = lm or TeluguLM()
        self._transitions_by_prev = defaultdict(list)
        self._prefix_index = defaultdict(list)
        self._cache = {}
        self._indexed = False
        self._ensure_indexed()

    def _ensure_indexed(self):
        if self._indexed:
            return
        self.lm.load()
        self._transitions_by_prev.clear()
        self._prefix_index.clear()
        self._cache.clear()

        # 1. Build reverse bigram transition index: prev_word -> [(next_word, count), ...]
        for pair_key, count in self.lm.bigrams.items():
            parts = pair_key.split('_', 1)
            if len(parts) == 2:
                w1, w2 = parts[0], parts[1]
                if len(w2) > 1 and w2 not in INVALID_STANDALONE_WORDS and count >= 3:
                    self._transitions_by_prev[w1].append((w2, count))

        # Sort transitions by frequency descending for instant retrieval
        for w1 in self._transitions_by_prev:
            self._transitions_by_prev[w1].sort(key=lambda x: x[1], reverse=True)

        # 2. Build fast prefix index for unigrams (high-frequency fallback words)
        for word, count in self.lm.unigrams.items():
            if len(word) > 1 and word not in INVALID_STANDALONE_WORDS and count >= 300:
                p1 = word[:1]
                p2 = word[:2]
                self._prefix_index[p1].append((word, count))
                if len(p2) >= 2:
                    self._prefix_index[p2].append((word, count))

        for p in self._prefix_index:
            self._prefix_index[p].sort(key=lambda x: x[1], reverse=True)
            self._prefix_index[p] = self._prefix_index[p][:30]

        self._indexed = True

    @staticmethod
    def _matches_prefix(word: str, prefix: str) -> bool:
        if not prefix:
            return True
        if word.startswith(prefix):
            return True
        # If prefix ends with virama/pollu, match words starting with the base consonant (e.g. 'వ్' matches 'వస్తాను')
        if prefix.endswith('\u0c4d'):
            base = prefix.rstrip('\u0c4d')
            if base and word.startswith(base):
                return True
        return False

    def predict_next(
        self,
        prev_word: Optional[str],
        prev_prev_word: Optional[str] = None,
        prefix: str = "",
        top_k: int = 3
    ) -> List[str]:
        """
        Returns top_k contextually ranked Telugu word predictions.
        Supports both next-word prediction (prefix="") and prefix autocomplete (prefix="...").
        """
        self._ensure_indexed()

        cache_key = (prev_word or "", prev_prev_word or "", prefix or "", top_k)
        if cache_key in self._cache:
            return self._cache[cache_key]

        candidates = []
        seen = set()

        # 1. Gather transitions from prev_word
        if prev_word:
            for w, _ in self._transitions_by_prev.get(prev_word, []):
                if prefix and not self._matches_prefix(w, prefix):
                    continue
                if w == prev_word and w not in ALLOWED_REDUPLICATIONS:
                    continue
                if w not in seen:
                    candidates.append(w)
                    seen.add(w)
                if len(candidates) >= 25:
                    break

        # 2. If prefix is provided and candidates < 10, fill from prefix index
        if prefix and len(candidates) < 10:
            base = prefix.rstrip('\u0c4d')
            prefix_pool = (
                self._prefix_index.get(prefix[:2], []) or
                self._prefix_index.get(prefix[:1], []) or
                self._prefix_index.get(base[:2], []) or
                self._prefix_index.get(base[:1], [])
            )
            for w, _ in prefix_pool:
                if self._matches_prefix(w, prefix) and w not in seen:
                    if w != prev_word or w in ALLOWED_REDUPLICATIONS:
                        candidates.append(w)
                        seen.add(w)
                if len(candidates) >= 25:
                    break

        # 3. Fallback for sentence start or unknown transitions
        if not candidates and not prefix:
            defaults = ["మీరు", "నేను", "నువ్వు", "ఈరోజు", "ఎలా", "ఎక్కడ", "చాలా", "బాగుంది"]
            for d in defaults:
                if d != prev_word:
                    candidates.append(d)
                if len(candidates) >= top_k:
                    break

        if not candidates:
            return []

        # 4. Multi-tier Contextual Scoring
        scored = []
        total_tokens = self.lm.total_tokens
        eps = self.lm.epsilon

        for w in candidates:
            # 4a. Unigram baseline probability
            uni_count = self.lm.unigrams.get(w, 50)
            p_uni = (uni_count + eps) / total_tokens
            score = 0.8 * math.log(max(p_uni, 1e-12))

            # 4b. Bigram transition probability: P(w | prev_word)
            if prev_word:
                p_prev = self.lm.get_bigram_prob(prev_word, w)
                score += 2.2 * math.log(max(p_prev, 1e-12))

            # 4c. Trigram context probability: P(w | prev_prev_word)
            if prev_prev_word:
                p_prev_prev = self.lm.get_bigram_prob(prev_prev_word, w)
                score += 1.6 * math.log(max(p_prev_prev, 1e-12))

            # 4d. Prefix alignment bonus
            if prefix:
                if w.startswith(prefix):
                    score += 2.0
                elif self._matches_prefix(w, prefix):
                    score += 1.5

            scored.append((w, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        results = [w for w, _ in scored[:top_k]]

        if len(self._cache) > 500:
            self._cache.clear()
        self._cache[cache_key] = results
        return results

    def get_ghost_text(
        self,
        prev_word: Optional[str],
        prev_prev_word: Optional[str] = None,
        prefix: str = ""
    ) -> str:
        """
        Returns the top single next-word suggestion for ghost text overlay.
        """
        preds = self.predict_next(prev_word, prev_prev_word, prefix=prefix, top_k=1)
        return preds[0] if preds else ""
