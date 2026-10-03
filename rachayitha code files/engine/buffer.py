from typing import List, Optional
from .casual_type import transliterate_word_candidates
from .lm import TeluguLM
from .predictor import NextWordPredictor

class TypingBuffer:
    def __init__(self, casual_enabled=True):
        self.eng = ""
        self.last_telugu = ""
        self.last_out_len = 0
        self.casual_enabled = casual_enabled
        self.lm = TeluguLM()
        self.predictor = NextWordPredictor(self.lm)
        self.current_suggestion = ""
        self.current_suggestions = []

        # 3-word sliding window state
        self.prev_prev_word = None
        self.prev_word_telugu = None
        self.prev_word_eng = None
        self.prev_word_candidates = None

    def set_casual_enabled(self, enabled: bool):
        self.casual_enabled = enabled
        if not enabled:
            self.clear_suggestion()

    def add(self, char):
        old_len = self.last_out_len
        self.eng += char

        if not self.casual_enabled:
            from .transliterator import transliterate as exact_transliterate
            new_telugu = exact_transliterate(self.eng)
            self.last_telugu = new_telugu
            self.last_out_len = len(new_telugu)
            self.clear_suggestion()
            return old_len, new_telugu, None

        # Casual mode: resolve current candidate with left context
        candidates = transliterate_word_candidates(self.eng)
        new_telugu = self.lm.score_candidates(
            candidates,
            prev_word=self.prev_word_telugu,
            next_word=None
        )
        self.last_telugu = new_telugu
        self.last_out_len = len(new_telugu)

        # Update prefix-aware predictions
        self.current_suggestions = self.predictor.predict_next(
            self.prev_word_telugu,
            self.prev_prev_word,
            prefix=new_telugu,
            top_k=3
        )
        self.current_suggestion = self.current_suggestions[0] if self.current_suggestions else ""

        # Check retroactive correction on prev_word if disambiguated by current word
        retro_patch = self._check_retroactive_patch(current_telugu=new_telugu, current_screen_len=old_len)
        return old_len, new_telugu, retro_patch

    def _check_retroactive_patch(self, current_telugu: str, current_screen_len: int):
        """
        Re-score previous candidates using current_telugu as next_word right context.
        If a different candidate wins with higher confidence, issue retroactive backspaces.
        """
        if not self.prev_word_candidates or len(self.prev_word_candidates) <= 1:
            return None

        better_prev = self.lm.score_candidates(
            self.prev_word_candidates,
            prev_word=self.prev_prev_word,
            next_word=current_telugu
        )

        if better_prev and better_prev != self.prev_word_telugu:
            # Backspaces needed: current word chars actually on screen + 1 space + previous word chars
            backspaces = current_screen_len + 1 + len(self.prev_word_telugu)
            replacement = f"{better_prev} {current_telugu}"
            self.prev_word_telugu = better_prev
            return (backspaces, replacement)

        return None

    def backspace(self):
        if not self.eng:
            return 0, "", None
        old_len = self.last_out_len
        self.eng = self.eng[:-1]

        if not self.eng:
            self.last_telugu = ""
            self.last_out_len = 0
            if self.casual_enabled and self.prev_word_telugu:
                self.current_suggestions = self.predictor.predict_next(
                    self.prev_word_telugu,
                    self.prev_prev_word,
                    prefix="",
                    top_k=3
                )
                self.current_suggestion = self.current_suggestions[0] if self.current_suggestions else ""
            else:
                self.clear_suggestion()
            return old_len, "", None

        if not self.casual_enabled:
            from .transliterator import transliterate as exact_transliterate
            new_telugu = exact_transliterate(self.eng)
            self.last_telugu = new_telugu
            self.last_out_len = len(new_telugu)
            self.clear_suggestion()
            return old_len, new_telugu, None

        candidates = transliterate_word_candidates(self.eng)
        new_telugu = self.lm.score_candidates(
            candidates,
            prev_word=self.prev_word_telugu,
            next_word=None
        )
        self.last_telugu = new_telugu
        self.last_out_len = len(new_telugu)

        self.current_suggestions = self.predictor.predict_next(
            self.prev_word_telugu,
            self.prev_prev_word,
            prefix=new_telugu,
            top_k=3
        )
        self.current_suggestion = self.current_suggestions[0] if self.current_suggestions else ""
        return old_len, new_telugu, None

    def commit_word(self):
        """Called when Space is pressed"""
        if self.eng:
            self.prev_prev_word = self.prev_word_telugu
            self.prev_word_telugu = self.last_telugu
            self.prev_word_eng = self.eng
            self.prev_word_candidates = transliterate_word_candidates(self.eng)

        self.eng = ""
        self.last_telugu = ""
        self.last_out_len = 0

        # Predict next word candidates (casual mode only)
        if self.casual_enabled and self.prev_word_telugu:
            self.current_suggestions = self.predictor.predict_next(
                self.prev_word_telugu,
                self.prev_prev_word,
                prefix="",
                top_k=3
            )
            self.current_suggestion = self.current_suggestions[0] if self.current_suggestions else ""
        else:
            self.clear_suggestion()

    def commit_word_with_telugu(self, telugu_word: str):
        """
        Called when a predicted suggestion is accepted.
        Advances the 3-word sliding window with the accepted Telugu word.
        """
        self.prev_prev_word = self.prev_word_telugu
        self.prev_word_telugu = telugu_word
        self.prev_word_eng = None
        self.prev_word_candidates = [telugu_word]
        self.eng = ""
        self.last_telugu = ""
        self.last_out_len = 0

        if self.casual_enabled and self.prev_word_telugu:
            self.current_suggestions = self.predictor.predict_next(
                self.prev_word_telugu,
                self.prev_prev_word,
                prefix="",
                top_k=3
            )
            self.current_suggestion = self.current_suggestions[0] if self.current_suggestions else ""
        else:
            self.clear_suggestion()

    def accept_suggestion(self, suggestion: Optional[str] = None):
        """
        Accepts a suggestion (either specified or the top primary suggestion).
        Returns tuple of (chars_to_backspace, text_to_insert).
        Advances the 3-word sliding window with the accepted Telugu word.
        """
        target = suggestion or self.current_suggestion
        if not target:
            return 0, ""

        bs_count = self.last_out_len
        to_insert = target + " "
        self.commit_word_with_telugu(target)
        return bs_count, to_insert

    def get_suggestion(self) -> str:
        return self.current_suggestion

    def get_suggestions(self) -> List[str]:
        return list(self.current_suggestions)

    def clear_suggestion(self):
        self.current_suggestion = ""
        self.current_suggestions = []

    def get_current_out_len(self) -> int:
        return self.last_out_len

    def commit_sentence(self):
        """Called on punctuation [. ? ! enter]"""
        self.commit_word()
        self.prev_prev_word = None
        self.prev_word_telugu = None
        self.prev_word_eng = None
        self.prev_word_candidates = None
        self.clear_suggestion()

    def commit(self):
        """Backward compatibility for commit()"""
        self.commit_sentence()

    def is_active(self):
        return bool(self.eng)

    def get_eng(self):
        return self.eng

    def get_telugu(self):
        return self.last_telugu
