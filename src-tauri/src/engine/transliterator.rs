use super::rules::{Rules, VIRAMA, ZWNJ};

pub struct Transliterator;

impl Transliterator {
    /// Transliterate Romanized English text (Tenglish) into Telugu Unicode
    pub fn transliterate(text: &str) -> String {
        if text.is_empty() {
            return String::new();
        }

        let mut out = String::new();
        let bytes = text.as_bytes();
        let n = text.len();
        let mut i = 0;

        while i < n {
            let slice = &text[i..];

            // 1. Check for SPECIAL tokens first (e.g. M, H, ~, _)
            let mut matched_special = None;
            for &(k, v) in Rules::SPECIAL {
                if slice.starts_with(k) {
                    matched_special = Some((k, v));
                    break;
                }
            }
            if let Some((k, v)) = matched_special {
                out.push_str(v);
                i += k.len();
                continue;
            }

            // 2. Check for CONSONANTS (sorted longest first in rules)
            let mut matched_consonant = None;
            for &(k, base) in Rules::CONSONANTS {
                if slice.starts_with(k) {
                    matched_consonant = Some((k, base));
                    break;
                }
            }

            if let Some((ck, base)) = matched_consonant {
                i += ck.len();
                let remaining = &text[i..];

                // Check if a vowel modifier follows
                let mut matched_mod = None;
                for &(vk, vmod) in Rules::VOWEL_MODS {
                    if remaining.starts_with(vk) {
                        matched_mod = Some((vk, vmod));
                        break;
                    }
                }

                if let Some((vk, vmod)) = matched_mod {
                    out.push_str(base);
                    out.push_str(vmod);
                    i += vk.len();
                } else {
                    // No vowel modifier: check if followed by another consonant or ZWNJ
                    let next_is_cons = Rules::CONSONANTS.iter().any(|&(next_ck, _)| remaining.starts_with(next_ck));
                    
                    if next_is_cons {
                        // Form consonant cluster / conjunct with Virama (్)
                        out.push_str(base);
                        out.push_str(VIRAMA);
                    } else if remaining.starts_with('_') {
                        // Explicit ZWNJ
                        out.push_str(base);
                        out.push_str(VIRAMA);
                        out.push_str(ZWNJ);
                        i += 1;
                    } else {
                        // Independent consonant with default inherent 'a' sound (క)
                        out.push_str(base);
                    }
                }
                continue;
            }

            // 3. Check for standalone VOWELS (అచ్చులు)
            let mut matched_vowel = None;
            for &(k, v) in Rules::VOWELS {
                if slice.starts_with(k) {
                    matched_vowel = Some((k, v));
                    break;
                }
            }

            if let Some((vk, v)) = matched_vowel {
                out.push_str(v);
                i += vk.len();
                continue;
            }

            // 4. Non-alphabetic character: copy verbatim (spaces, punctuation, numbers)
            let ch = text[i..].chars().next().unwrap();
            out.push(ch);
            i += ch.len_utf8();
        }

        out
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic_vowels() {
        assert_eq!(Transliterator::transliterate("a"), "అ");
        assert_eq!(Transliterator::transliterate("aa"), "ఆ");
        assert_eq!(Transliterator::transliterate("i"), "ఇ");
        assert_eq!(Transliterator::transliterate("ii"), "ఈ");
        assert_eq!(Transliterator::transliterate("u"), "ఉ");
        assert_eq!(Transliterator::transliterate("uu"), "ఊ");
        assert_eq!(Transliterator::transliterate("e"), "ఎ");
        assert_eq!(Transliterator::transliterate("E"), "ఏ");
        assert_eq!(Transliterator::transliterate("ai"), "ఐ");
        assert_eq!(Transliterator::transliterate("o"), "ఒ");
        assert_eq!(Transliterator::transliterate("O"), "ఓ");
        assert_eq!(Transliterator::transliterate("au"), "ఔ");
    }

    #[test]
    fn test_words_and_conjuncts() {
        assert_eq!(Transliterator::transliterate("telugu"), "తెలుగు");
        assert_eq!(Transliterator::transliterate("amma"), "అమ్మ");
        assert_eq!(Transliterator::transliterate("namaskAram"), "నమస్కారం");
        assert_eq!(Transliterator::transliterate("rachayitha"), "రచయిత");
        assert_eq!(Transliterator::transliterate("kRuShNa"), "కృష్ణ");
        assert_eq!(Transliterator::transliterate("bhArath"), "భారత్");
    }

    #[test]
    fn test_ligatures_and_special() {
        assert_eq!(Transliterator::transliterate("ksh"), "క్ష");
        assert_eq!(Transliterator::transliterate("kshaminchu"), "క్షమించు");
        assert_eq!(Transliterator::transliterate("jnyaanam"), "జ్ఞానం");
        assert_eq!(Transliterator::transliterate("kaM"), "కం");
        assert_eq!(Transliterator::transliterate("duHkham"), "దుఃఖం");
    }
}
