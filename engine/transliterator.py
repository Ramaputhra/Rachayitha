import os
import sys

# Delegate directly to rachayitha code files/engine/transliterator.py
source_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rachayitha code files")
if source_path not in sys.path:
    sys.path.insert(0, source_path)

from engine.transliterator import transliterate, CONSONANTS_MAP, VOWEL_MODS, INDEPENDENT_VOWELS, SPECIAL_MAP

__all__ = ["transliterate", "CONSONANTS_MAP", "VOWEL_MODS", "INDEPENDENT_VOWELS", "SPECIAL_MAP"]
