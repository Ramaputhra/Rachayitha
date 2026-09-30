import os
import sys

# Ensure rachayitha code files engine is importable
source_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rachayitha code files")
if source_path not in sys.path:
    sys.path.insert(0, source_path)

from engine.casual_type import (
    transliterate,
    transliterate_word,
    load_dictionaries,
    find_data_file,
    decompose_compound,
    casual_phonetic_transliterate,
    CASUAL_DICT,
    TYPO_FIXES,
    TOP10K_FREQ,
    CONVERSATIONAL_LEXICON
)

__all__ = [
    "transliterate",
    "transliterate_word",
    "load_dictionaries",
    "find_data_file",
    "decompose_compound",
    "casual_phonetic_transliterate",
    "CASUAL_DICT",
    "TYPO_FIXES",
    "TOP10K_FREQ",
    "CONVERSATIONAL_LEXICON"
]
