/// Lekhini RTS (Real Time Transliteration Scheme) Rule Definitions for Telugu
use serde::{Deserialize, Serialize};

pub const VIRAMA: &str = "\u{0C4D}"; // ్ (పొల్లు)
pub const ZWNJ: &str = "\u{200C}";   // Zero Width Non-Joiner

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RuleEntry {
    pub key: String,
    pub telugu: String,
    pub category: String,
    pub example: String,
}

pub struct Rules;

impl Rules {
    /// Independent Vowels (అచ్చులు)
    pub const VOWELS: &'static [(&'static str, &'static str)] = &[
        ("aa", "ఆ"),
        ("A", "ఆ"),
        ("a", "అ"),
        ("ii", "ఈ"),
        ("I", "ఈ"),
        ("ee", "ఈ"),
        ("i", "ఇ"),
        ("uu", "ఊ"),
        ("U", "ఊ"),
        ("oo", "ఊ"),
        ("u", "ఉ"),
        ("R^I", "ౠ"),
        ("RU", "ౠ"),
        ("R^i", "ఋ"),
        ("Ru", "ఋ"),
        ("E", "ఏ"),
        ("ea", "ఏ"),
        ("e", "ఎ"),
        ("ai", "ఐ"),
        ("ay", "ఐ"),
        ("O", "ఓ"),
        ("oa", "ఓ"),
        ("o", "ఒ"),
        ("au", "ఔ"),
        ("ou", "ఔ"),
        ("av", "ఔ"),
    ];

    /// Vowel Modifiers / Matras (గుణింతాలు)
    pub const VOWEL_MODS: &'static [(&'static str, &'static str)] = &[
        ("aa", "ా"),
        ("A", "ా"),
        ("a", ""),
        ("ii", "ీ"),
        ("I", "ీ"),
        ("ee", "ీ"),
        ("i", "ి"),
        ("uu", "ూ"),
        ("U", "ూ"),
        ("oo", "ూ"),
        ("u", "ు"),
        ("R^I", "ౄ"),
        ("RU", "ౄ"),
        ("R^i", "ృ"),
        ("Ru", "ృ"),
        ("E", "ే"),
        ("ea", "ే"),
        ("e", "ె"),
        ("ai", "ై"),
        ("ay", "ై"),
        ("O", "ో"),
        ("oa", "ో"),
        ("o", "ొ"),
        ("au", "ౌ"),
        ("ou", "ౌ"),
        ("av", "ౌ"),
    ];

    /// Consonants (హల్లులు) and special conjuncts
    pub const CONSONANTS: &'static [(&'static str, &'static str)] = &[
        // Compound ligatures
        ("ksh", "క్ష"),
        ("kSh", "క్ష"),
        ("kS", "క్ష"),
        ("jnya", "జ్ఞ"),
        ("dnya", "జ్ఞ"),
        // Velars
        ("kh", "ఖ"),
        ("K", "ఖ"),
        ("k", "క"),
        ("gh", "ఘ"),
        ("G", "ఘ"),
        ("g", "గ"),
        ("~g", "ఙ"),
        ("nga", "ఙ"),
        // Palatals
        ("ch", "చ"),
        ("c", "చ"),
        ("Ch", "ఛ"),
        ("C", "ఛ"),
        ("jh", "ఝ"),
        ("J", "ఝ"),
        ("j", "జ"),
        ("~n", "ఞ"),
        ("nya", "ఞ"),
        // Retroflexes
        ("Th", "ఠ"),
        ("T", "ట"),
        ("Dh", "ఢ"),
        ("D", "డ"),
        ("N", "ణ"),
        // Dentals
        ("th", "థ"),
        ("t", "త"),
        ("dh", "ధ"),
        ("d", "ద"),
        ("n", "న"),
        // Labials
        ("ph", "ఫ"),
        ("P", "ఫ"),
        ("f", "ఫ"),
        ("p", "ప"),
        ("bh", "భ"),
        ("B", "భ"),
        ("b", "బ"),
        ("m", "మ"),
        // Semivowels & liquids
        ("y", "య"),
        ("r", "ర"),
        ("l", "ల"),
        ("v", "వ"),
        ("w", "వ"),
        ("L", "ళ"),
        ("R", "ఱ"), // Bandira
        // Sibilants & Aspirate
        ("sh", "శ"),
        ("S", "శ"),
        ("Sh", "ష"),
        ("s", "స"),
        ("h", "హ"),
    ];

    /// Special markers (అనుస్వారము, విసర్గ, పొల్లు)
    pub const SPECIAL: &'static [(&'static str, &'static str)] = &[
        ("M", "ం"),
        ("H", "ః"),
        ("~", "\u{0C4D}"),
        ("_", "\u{200C}"),
    ];

    /// Return full list of rules formatted for the Settings Key Map UI
    pub fn get_all_entries() -> Vec<RuleEntry> {
        let mut entries = Vec::new();

        // Vowels
        for &(k, v) in Self::VOWELS {
            entries.push(RuleEntry {
                key: k.to_string(),
                telugu: v.to_string(),
                category: "Vowels (అచ్చులు)".to_string(),
                example: format!("{} -> {}", k, v),
            });
        }

        // Consonants
        for &(k, v) in Self::CONSONANTS {
            entries.push(RuleEntry {
                key: k.to_string(),
                telugu: v.to_string(),
                category: "Consonants (హల్లులు)".to_string(),
                example: format!("{}a -> {}", k, v),
            });
        }

        // Modifiers
        for &(k, v) in Self::VOWEL_MODS {
            if !v.is_empty() {
                entries.push(RuleEntry {
                    key: k.to_string(),
                    telugu: v.to_string(),
                    category: "Guninthalu (గుణింతాలు)".to_string(),
                    example: format!("k{} -> క{}", k, v),
                });
            }
        }

        // Specials
        for &(k, v) in Self::SPECIAL {
            let desc = match k {
                "M" => "Sunna / Anusvara (సున్నా)",
                "H" => "Visarga (విసర్గ)",
                "~" => "Explicit Virama (పొల్లు)",
                "_" => "ZWNJ (విభాజకం)",
                _ => "Special",
            };
            entries.push(RuleEntry {
                key: k.to_string(),
                telugu: v.to_string(),
                category: "Special (ప్రత్యేక గుర్తులు)".to_string(),
                example: format!("{} -> {} ({})", k, v, desc),
            });
        }

        entries
    }
}
