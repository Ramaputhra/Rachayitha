import json
import os
import sys

from .paths import get_resource_path

VIRAMA = '్'
ZWNJ = '\u200c'

# Complete Lekhini RTS Consonants mapping (base glyphs)
CONSONANTS_MAP = {
    # Ligatures & Conjuncts
    "ksha": "క్ష", "Ksha": "క్ష", "kSha": "క్ష", "KSHA": "క్ష",
    "ksh": "క్ష", "Ksh": "క్ష", "kSh": "క్ష", "KSH": "క్ష",
    "jnya": "జ్ఞ", "Jnya": "జ్ఞ", "dnya": "జ్ఞ", "Dnya": "జ్ఞ", "gnya": "జ్ఞ",
    "~g": "ఙ", "nga": "ఙ",
    "~n": "ఞ", "nya": "ఞ",

    # Velars
    "kh": "ఖ", "Kh": "ఖ", "KH": "ఖ", "K": "ఖ",
    "k": "క",
    "gh": "ఘ", "Gh": "ఘ", "GH": "ఘ", "G": "ఘ",
    "g": "గ",

    # Palatals
    "ch": "చ", "Ch": "ఛ", "CH": "ఛ", "c": "చ", "C": "ఛ",
    "jh": "ఝ", "Jh": "ఝ", "JH": "ఝ", "J": "ఝ",
    "j": "జ",

    # Retroflexes
    "Th": "ఠ", "TH": "ఠ", "th": "థ",
    "T": "ట",
    "Dh": "ఢ", "DH": "ఢ", "dh": "ధ",
    "D": "డ",
    "N": "ణ",

    # Dentals
    "t": "త",
    "d": "ద",
    "n": "న",

    # Labials
    "ph": "ఫ", "Ph": "ఫ", "PH": "ఫ", "P": "ఫ", "f": "ఫ", "F": "ఫ",
    "p": "ప",
    "bh": "భ", "Bh": "భ", "BH": "భ", "B": "భ",
    "b": "బ",
    "m": "మ",

    # Semivowels & Liquids
    "yy": "య్య",
    "y": "య", "Y": "య",
    "r": "ర",
    "l": "ల",
    "v": "వ", "w": "వ", "V": "వ", "W": "వ",
    "L": "ళ",
    "R": "ఱ",  # Bandira

    # Sibilants & Aspirate
    "sh": "శ", "Sh": "ష", "SH": "ష", "S": "శ",
    "s": "స",
    "h": "హ", "H": "ః"
}

# Vowel Modifiers (Guninthalu Matras)
VOWEL_MODS = {
    "aa": "ా", "A": "ా",
    "a": "",  # Inherent vowel: removes halant/virama
    "ii": "ీ", "I": "ీ", "ee": "ీ",
    "i": "ి",
    "uu": "ూ", "U": "ూ", "oo": "ూ",
    "u": "ు",
    "R^I": "ౄ", "RU": "ౄ",
    "R^i": "ృ", "Ru": "ృ",
    "E": "ే", "ea": "ే",
    "e": "ె",
    "ai": "ై", "ay": "ై",
    "O": "ో", "oa": "ో",
    "o": "ొ",
    "au": "ౌ", "ou": "ౌ", "av": "ౌ"
}

# Independent Vowels (అచ్చులు)
INDEPENDENT_VOWELS = {
    "aa": "ఆ", "A": "ఆ",
    "a": "అ",
    "ii": "ఈ", "I": "ఈ", "ee": "ఈ",
    "i": "ఇ",
    "uu": "ఊ", "U": "ఊ", "oo": "ఊ",
    "u": "ఉ",
    "R^I": "ౠ", "RU": "ౠ",
    "R^i": "ఋ", "Ru": "ఋ",
    "E": "ఏ", "ea": "ఏ",
    "e": "ఎ",
    "ai": "ఐ", "ay": "ఐ",
    "O": "ఓ", "oa": "ఓ",
    "o": "ఒ",
    "au": "ఔ", "ou": "ఔ", "av": "ఔ"
}

# Special Markers
SPECIAL_MAP = {
    "MDI": "ండి",
    "MDi": "ండి",
    "mdi": "ండి",
    "M": "ం",       # Sunna / Anusvara
    "H": "ః",       # Visarga
    "~": VIRAMA,    # Explicit pollu
    "_": ZWNJ       # Zero Width Non-Joiner
}

# Common Tenglish word overrides
WORD_OVERRIDES = {
    "namaskaaram": "నమస్కారం",
    "namaskaram": "నమస్కారం",
    "namaskaaraM": "నమస్కారం",
    "namaskaraM": "నమస్కారం",
    "namaskAram": "నమస్కారం",
    "namaskAraM": "నమస్కారం",
    "namaskaaramu": "నమస్కారము",
    "namaskaramu": "నమస్కారము",
    "rachayitha": "రచయిత",
    "rachayita": "రచయిత",
    "tho": "తో",
    "tO": "తో",
    "telugulo": "తెలుగులో",
    "telugulO": "తెలుగులో",
    "type": "టైప్",
    "taip": "టైప్",
    "Taip": "టైప్",
    "cheyandi": "చేయండి",
    "chEyandi": "చేయండి",
    "cheyyandi": "చేయ్యండి",
    "chEyyaMDI": "చేయ్యండి",
    "chEyyandi": "చేయ్యండి"
}
SORTED_WORD_OVERRIDES = sorted(WORD_OVERRIDES.keys(), key=len, reverse=True)

# Sort keys by length descending to prioritize greedy prefix matches (e.g. ksha before ksh before k)
SORTED_SPECIAL = sorted(SPECIAL_MAP.keys(), key=len, reverse=True)
SORTED_CONSONANTS = sorted(CONSONANTS_MAP.keys(), key=len, reverse=True)
SORTED_VOWEL_MODS = sorted(VOWEL_MODS.keys(), key=len, reverse=True)
SORTED_INDEP_VOWELS = sorted(INDEPENDENT_VOWELS.keys(), key=len, reverse=True)

def transliterate(text: str) -> str:
    """
    Halant-First (Pollu-First) Telugu Transliteration Engine:
    - Single consonant key produces pure half-letter (e.g. n -> న్, N -> ణ్, k -> క్, ksh -> కృష్/క్ష్)
    - Followed by 'a' produces full letter without halant (e.g. na -> న, Na -> ణ, ka -> క, ksha -> క్ష, Ksha -> క్ష)
    - Followed by other vowels produces corresponding Gunintham (e.g. ni -> ని, kshuu -> క్షూ)
    - Doubled consonants produce proper Vatthulu/Conjuncts (e.g. nna -> న్న, kka -> క్క, amma -> అమ్మ)
    """
    if not text:
        return ""

    out = []
    i = 0
    n = len(text)

    while i < n:
        slice_text = text[i:]

        # 0. Word-level overrides at word boundary
        is_word_start = (i == 0 or text[i - 1] in " \t\n.,!?;:()[]{}\"'-\\/")
        if is_word_start:
            matched_override = None
            slice_lower = slice_text.lower()
            for word in SORTED_WORD_OVERRIDES:
                if slice_lower.startswith(word.lower()):
                    next_char = slice_text[len(word)] if len(slice_text) > len(word) else None
                    if not next_char or next_char in " \t\n.,!?;:()[]{}\"'-\\/":
                        matched_override = word
                        break
            if matched_override:
                out.append(WORD_OVERRIDES[matched_override])
                i += len(matched_override)
                continue

        # 1. Check for Special Markers (e.g. M -> ం, H -> ః, ~, _)
        matched_special = None
        for sm in SORTED_SPECIAL:
            if slice_text.startswith(sm):
                matched_special = sm
                break
        if matched_special:
            out.append(SPECIAL_MAP[matched_special])
            i += len(matched_special)
            continue

        # 2. Check for Consonants
        matched_cons = None
        for ck in SORTED_CONSONANTS:
            if slice_text.startswith(ck):
                matched_cons = ck
                break

        if matched_cons:
            base = CONSONANTS_MAP[matched_cons]
            i += len(matched_cons)
            remaining = text[i:]

            # If the matched consonant key already ended in 'a' (like 'ksha', 'Ksha', 'nga', 'nya')
            if matched_cons.endswith('a'):
                # Base is already full letter without halant
                out.append(base)
                continue

            # Check if a vowel modifier follows immediately
            matched_vmod = None
            for vk in SORTED_VOWEL_MODS:
                if remaining.startswith(vk):
                    matched_vmod = vk
                    break

            if matched_vmod:
                # Vowel follows
                if matched_vmod == 'a':
                    # Inherent vowel 'a' removes virama, forming full letter (e.g. n + a -> న, k + a -> క)
                    out.append(base)
                else:
                    # Other vowel adds matra (e.g. k + i -> కి, k + u -> కు)
                    out.append(base + VOWEL_MODS[matched_vmod])
                i += len(matched_vmod)
            else:
                # NO vowel follows: Halant-First!
                # Produces half letter with Virama (e.g. n -> న్, k -> క్, ksh -> కష్/క్ష్)
                out.append(base + VIRAMA)
            continue

        # 3. Check for Independent Vowels (at beginning of word or after another vowel)
        matched_indep = None
        for ivk in SORTED_INDEP_VOWELS:
            if slice_text.startswith(ivk):
                matched_indep = ivk
                break

        if matched_indep:
            out.append(INDEPENDENT_VOWELS[matched_indep])
            i += len(matched_indep)
            continue

        # 4. Verbatim passthrough for punctuation, digits, spaces
        out.append(text[i])
        i += 1

    return "".join(out)
