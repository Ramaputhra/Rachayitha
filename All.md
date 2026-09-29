# Rachayitha - Master Telugu Letters & Keystroke Blueprint (`All.md`)

> **ఉద్దేశం (Purpose)**: 
> This document curates **every possible Telugu letter, sign, modifier, vowel combination (గుణింతాలు), geminate (ద్విత్వాక్షరాలు), conjunct (సంయుక్తాక్షరాలు), and complex cluster (సంశ్లేషాక్షరాలు)**.
> 
> It contrasts:
> 1. **Current Mappings & Conflicts** in Rachayitha (`src-tauri/src/engine/rules.rs`, `rachayitha code files/engine/transliterator.py`, `Keymap-Explorer.py`).
> 2. **Missing letters and combinations** that are not yet mapped.
> 3. **`Your Preferred Keystroke(s)`** column — **Fill or modify this column with your exact desired combinations** so we can build the new transliteration logic with 100% precision.

---

## సూచిక (Status Legend)
- `[EXISTS]` : Currently supported in the codebase.
- `[CONFLICT]` : Inconsistent between files (e.g. `ee` = ఈ in Rust vs ఏ in Python/Keymap).
- `[MISSING]` : Currently missing or not uniquely mapped.
- `[NEEDS_CHOICE]` : Ambiguous in informal English typing (e.g., `th` for త vs థ).

---

## 1. అచ్చులు (Independent Vowels)

| Telugu | Name / Description | Current Mapping(s) | Status | Suggested Standard | Your Preferred Keystroke(s) |
|---|---|---|---|---|---|
| **అ** | Hrasva A (Short) | `a` | `[EXISTS]` | `a` | |
| **ఆ** | Deergha Aa (Long) | `aa`, `A` | `[EXISTS]` | `aa` or `A` | |
| **ఇ** | Hrasva I (Short) | `i` | `[EXISTS]` | `i` | |
| **ఈ** | Deergha Ii (Long) | `ii`, `I`, `ee` *(conflicts)* | `[CONFLICT]` | `ii` or `I` | |
| **ఉ** | Hrasva U (Short) | `u` | `[EXISTS]` | `u` | |
| **ఊ** | Deergha Uu (Long) | `uu`, `U`, `oo` *(conflicts)* | `[CONFLICT]` | `uu` or `U` | |
| **ఋ** | Vocalic R (Hrasva Ru) | `Ru`, `R^i` | `[EXISTS]` | `Ru` or `ru` | |
| **ౠ** | Vocalic R (Deergha RU) | `RU`, `R^I` | `[EXISTS]` | `RU` or `Ruu` | |
| **ఌ** | Vocalic L (Lu - Archaic) | *None* | `[MISSING]` | `~l` or `Lu` | |
| **ౡ** | Vocalic L (Luu - Archaic) | *None* | `[MISSING]` | `~L` or `LU` | |
| **ఎ** | Hrasva E (Short) | `e` | `[EXISTS]` | `e` | |
| **ఏ** | Deergha Ee (Long) | `ee`, `E`, `ea` | `[CONFLICT]` | `E` or `ee` | |
| **ఐ** | Diphthong Ai | `ai`, `ay` | `[EXISTS]` | `ai` | |
| **ఒ** | Hrasva O (Short) | `o` | `[EXISTS]` | `o` | |
| **ఓ** | Deergha Oo (Long) | `oo`, `O`, `oa` | `[CONFLICT]` | `O` or `oo` | |
| **ఔ** | Diphthong Au | `au`, `ou`, `av` | `[EXISTS]` | `au` or `ou` | |

---

## 2. ఉభయాక్షరాలు, విరామం & నియంత్రణ గుర్తులు (Special Marks & Controls)

| Telugu / Symbol | Name / Description | Current Mapping(s) | Status | Suggested Standard | Your Preferred Keystroke(s) |
|---|---|---|---|---|---|
| **ం** | సున్నా / అనుస్వారము (Anusvara) | `M` | `[EXISTS]` | `M` or `o` | |
| **ః** | విసర్గ (Visarga) | `H` | `[EXISTS]` | `H` or `hh` | |
| **ఁ** | అరసున్నా / అర్ధానుస్వారము (Ardhannusvara) | *None* | `[MISSING]` | `~m` or `@m` | |
| **్** | పొల్లు / విరామము (Virama / Halant) | `~` | `[EXISTS]` | `~` or `/` | |
| `ZWNJ` | Zero Width Non-Joiner (విభాజకం - prevents ligature) | `_` | `[EXISTS]` | `_` | |
| `ZWJ` | Zero Width Joiner (సంశ్లేషక / ligature lock) | *None* | `[MISSING]` | `+` or `^` | |
| **ౚ** | నకారపొల్లు (Chillu Nakaram / Archaic Pollu) | *None* | `[MISSING]` | `N~` or `n_` | |

---

## 3. హల్లులు (Base Consonants)

> **గమనిక (Important)**:
> In Telugu phonetics, does typing `k` alone mean pure halant `క్` or full letter `క`?
> - **Option A (Inherent-a / RTS)**: `k` = క, `ka` = క, `k~` = క్.
> - **Option B (Halant-first)**: `k` = క్, `ka` = క.
> Please specify your preferred keystrokes below.

### 3.1 కంఠ్యములు (Velars: K-Varga)
| Telugu | Phonetic Name | Current Mapping | Status | Suggested Keystroke | Your Preferred Keystroke(s) |
|---|---|---|---|---|---|
| **క** | Ka | `k` | `[EXISTS]` | `k` / `ka` | |
| **ఖ** | Kha (Mahaprana) | `kh`, `K` | `[EXISTS]` | `kh` or `K` | |
| **గ** | Ga | `g` | `[EXISTS]` | `g` / `ga` | |
| **ఘ** | Gha (Mahaprana) | `gh`, `G` | `[EXISTS]` | `gh` or `G` | |
| **ఙ** | Nga (Anunasika) | `~g`, `nga` | `[EXISTS]` | `nga` or `~g` | |

### 3.2 తాలవ్యములు (Palatals: C-Varga)
| Telugu | Phonetic Name | Current Mapping | Status | Suggested Keystroke | Your Preferred Keystroke(s) |
|---|---|---|---|---|---|
| **చ** | Cha (Alpaprana) | `ch`, `c` | `[EXISTS]` | `ch` or `c` | |
| **ఛ** | Chha (Mahaprana) | `Ch`, `C` | `[EXISTS]` | `Ch` or `chh` | |
| **జ** | Ja | `j` | `[EXISTS]` | `j` / `ja` | |
| **ఝ** | Jha (Mahaprana) | `jh`, `J` | `[EXISTS]` | `jh` or `J` | |
| **ఞ** | Nya (Anunasika) | `~n`, `nya` | `[EXISTS]` | `nya` or `~n` | |
| **ౘ** | Tsa (దంత్య చకారము - Archaic/Dialect) | *None* | `[MISSING]` | `ts` or `~c` | |
| **ౙ** | Dza (దంత్య జకారము - Archaic/Dialect) | *None* | `[MISSING]` | `dz` or `~j` | |

### 3.3 మూర్ధన్యములు (Retroflexes: T-Varga)
| Telugu | Phonetic Name | Current Mapping | Status | Suggested Keystroke | Your Preferred Keystroke(s) |
|---|---|---|---|---|---|
| **ట** | Ta (Hard T) | `T` | `[EXISTS]` | `T` / `Ta` | |
| **ఠ** | Tha (Hard Th - Mahaprana) | `Th` | `[EXISTS]` | `Th` | |
| **డ** | Da (Hard D) | `D` | `[EXISTS]` | `D` / `Da` | |
| **ఢ** | Dha (Hard Dh - Mahaprana) | `Dh` | `[EXISTS]` | `Dh` | |
| **ణ** | Na (Retroflex N) | `N` | `[EXISTS]` | `N` / `Na` | |

### 3.4 దంత్యములు (Dentals: t-Varga)
| Telugu | Phonetic Name | Current Mapping | Status | Suggested Keystroke | Your Preferred Keystroke(s) |
|---|---|---|---|---|---|
| **త** | ta (Soft t) | `t` | `[NEEDS_CHOICE]` | `t` / `ta` *(often typed as `th`)* | |
| **థ** | tha (Soft th - Mahaprana) | `th` | `[NEEDS_CHOICE]` | `th` or `thh` or `T` | |
| **ద** | da (Soft d) | `d` | `[EXISTS]` | `d` / `da` | |
| **ధ** | dha (Soft dh - Mahaprana) | `dh` | `[EXISTS]` | `dh` | |
| **న** | na (Dental n) | `n` | `[EXISTS]` | `n` / `na` | |

### 3.5 ఓష్ఠ్యములు (Labials: P-Varga)
| Telugu | Phonetic Name | Current Mapping | Status | Suggested Keystroke | Your Preferred Keystroke(s) |
|---|---|---|---|---|---|
| **ప** | Pa | `p` | `[EXISTS]` | `p` / `pa` | |
| **ఫ** | Pha / Fa (Mahaprana) | `ph`, `P`, `f` | `[EXISTS]` | `ph` or `f` or `P` | |
| **బ** | Ba | `b` | `[EXISTS]` | `b` / `ba` | |
| **భ** | Bha (Mahaprana) | `bh`, `B` | `[EXISTS]` | `bh` or `B` | |
| **మ** | Ma | `m` | `[EXISTS]` | `m` / `ma` | |

### 3.6 అంతఃస్థములు (Semivowels / Liquids)
| Telugu | Phonetic Name | Current Mapping | Status | Suggested Keystroke | Your Preferred Keystroke(s) |
|---|---|---|---|---|---|
| **య** | Ya | `y` | `[EXISTS]` | `y` / `ya` | |
| **ర** | Ra (Alpaprana) | `r` | `[EXISTS]` | `r` / `ra` | |
| **ల** | La | `l` | `[EXISTS]` | `l` / `la` | |
| **వ** | Va / Wa | `v`, `w` | `[EXISTS]` | `v` or `w` | |
| **ళ** | La (Retroflex L) | `L` | `[EXISTS]` | `L` / `La` | |
| **ఱ** | Rra (Bandira / బండిర) | `R` | `[EXISTS]` | `R` or `rr` | |
| **ఴ** | Zha (Retroflex llla - Archaic Dravidian) | *None* | `[MISSING]` | `zha` or `~z` | |

### 3.7 ఊష్మములు & ప్రాణ (Sibilants & Aspirate)
| Telugu | Phonetic Name | Current Mapping | Status | Suggested Keystroke | Your Preferred Keystroke(s) |
|---|---|---|---|---|---|
| **శ** | Sha (Talavya Sha) | `sh`, `S` | `[EXISTS]` | `sh` or `S` | |
| **ష** | Sha (Murdhanya Sha) | `Sh` | `[EXISTS]` | `Sh` or `shh` | |
| **స** | Sa (Dantya Sa) | `s` | `[EXISTS]` | `s` / `sa` | |
| **హ** | Ha (Kantha Ha) | `h` | `[EXISTS]` | `h` / `ha` | |

### 3.8 సాంప్రదాయ సంయుక్త లిపులు (Traditional Compound Glyphs)
| Telugu | Phonetic Name | Current Mapping | Status | Suggested Keystroke | Your Preferred Keystroke(s) |
|---|---|---|---|---|---|
| **క్ష** | Ksha | `ksh`, `kSh`, `kS` | `[EXISTS]` | `ksh` or `x` | |
| **జ్ఞ** | Jnya / Gnya | `jnya`, `dnya` | `[EXISTS]` | `jnya` or `gnya` | |

---

## 4. గుణింతపు గుర్తులు (Matras / Vowel Diacritics)

Applied to any base consonant (shown with `క` as base: `క` + Matra):

| Matra | Telugu Name | Example with `క` | Current Mapping | Status | Suggested Keystroke | Your Preferred Keystroke(s) |
|---|---|---|---|---|---|---|
| *(none)* | తలకట్టు (Inherent 'a') | **క** | `a` or *none* | `[EXISTS]` | `a` | |
| **ా** | దీర్ఘము (Aa) | **కా** | `aa`, `A` | `[EXISTS]` | `aa` or `A` | |
| **ి** | గుడి (I) | **కి** | `i` | `[EXISTS]` | `i` | |
| **ీ** | గుడిదీర్ఘము (Ii) | **కీ** | `ii`, `I`, `ee` | `[CONFLICT]` | `ii` or `I` | |
| **ు** | కొమ్ము (U) | **కు** | `u` | `[EXISTS]` | `u` | |
| **ూ** | కొమ్ముదీర్ఘము (Uu) | **కూ** | `uu`, `U`, `oo` | `[CONFLICT]` | `uu` or `U` | |
| **ృ** | వట్రుసుడి / రుత్వము (Ru) | **కృ** | `Ru`, `R^i` | `[EXISTS]` | `Ru` or `ru` | |
| **ౄ** | వట్రుసుడి దీర్ఘము (RU) | **కౄ** | `RU`, `R^I` | `[EXISTS]` | `RU` or `Ruu` | |
| **ె** | ఎత్వము (E) | **కె** | `e` | `[EXISTS]` | `e` | |
| **ే** | ఏత్వము (Ee) | **కే** | `ee`, `E`, `ea` | `[CONFLICT]` | `E` or `ee` | |
| **ై** | ఐత్వము (Ai) | **కై** | `ai`, `ay` | `[EXISTS]` | `ai` | |
| **ొ** | ఒత్వము (O) | **కొ** | `o` | `[EXISTS]` | `o` | |
| **ో** | ఓత్వము (Oo) | **కో** | `oo`, `O`, `oa` | `[CONFLICT]` | `O` or `oo` | |
| **ౌ** | ఔత్వము (Au) | **కౌ** | `au`, `ou`, `av` | `[EXISTS]` | `au` or `ou` | |
| **ం** | సున్నా (Anusvara) | **కం** | `M` | `[EXISTS]` | `M` or `am` | |
| **ః** | విసర్గ (Visarga) | **కః** | `H` | `[EXISTS]` | `H` or `ah` | |
| **ఁ** | అరసున్నా (Ardhannusvara) | **కఁ** | *None* | `[MISSING]` | `~m` | |
| **్** | పొల్లు / విరామము (Halant) | **క్** | `~` | `[EXISTS]` | `~` or `/` | |

---

## 5. గుణింతాల నమూనా (Guninthalu Matrix for Major Consonants)

> All 16 vowel forms should follow an identical logical suffix after the consonant key.
> E.g. If `క` = `k`, then `కా` = `k` + `aa`, `కి` = `k` + `i`, `కీ` = `k` + `ii`, etc.

| Base | a (తల) | aa (దీర్ఘం) | i (గుడి) | ii (గుడిదీర్ఘం) | u (కొమ్ము) | uu (కొమ్ముదీర్ఘం) | Ru (రుత్వం) | RU (రుత్వం దీర్ఘం) | e (ఎత్వం) | ee (ఏత్వం) | ai (ఐత్వం) | o (ఒత్వం) | oo (ఓత్వం) | au (ఔత్వం) | M (సున్నా) | H (విసర్గ) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **క** | క | కా | కి | కీ | కు | కూ | కృ | కౄ | కె | కే | కై | కొ | కో | కౌ | కం | కః |
| **ఖ** | ఖ | ఖా | ఖి | ఖీ | ఖు | ఖూ | ఖృ | ఖౄ | ఖె | ఖే | ఖై | ఖొ | ఖో | ఖౌ | ఖం | ఖః |
| **గ** | గ | గా | గి | గీ | గు | గూ | గృ | గౄ | గె | గే | గై | గొ | గో | గౌ | గం | గః |
| **ఘ** | ఘ | ఘా | ఘి | ఘీ | ఘు | ఘూ | ఘృ | ఘౄ | ఘె | ఘే | ఘై | ఘొ | ఘో | ఘౌ | ఘం | ఘః |
| **చ** | చ | చా | చి | చీ | చు | చూ | చృ | చౄ | చె | చే | చై | చొ | చో | చౌ | చం | చః |
| **ఛ** | ఛ | ఛా | ఛి | ఛీ | ఛు | ఛూ | ఛృ | ఛౄ | ఛె | ఛే | ఛై | ఛొ | ఛో | ఛౌ | ఛం | ఛః |
| **జ** | జ | జా | జి | జీ | జు | జూ | జృ | జౄ | జె | జే | జై | జొ | జో | జౌ | జం | జః |
| **ఝ** | ఝ | ఝా | ఝి | ఝీ | ఝు | ఝూ | ఝృ | ఝౄ | ఝె | ఝే | ఝై | ఝొ | ఝో | ఝౌ | ఝం | ఝః |
| **ట** | ట | టా | టి | టీ | టు | టూ | టృ | టౄ | టె | టే | టై | టొ | టో | టౌ | టం | టః |
| **ఠ** | ఠ | ఠా | ఠి | ఠీ | ఠు | ఠూ | ఠృ | ఠౄ | ఠె | ఠే | ఠై | ఠొ | ఠో | ఠౌ | ఠం | ఠః |
| **డ** | డ | డా | డి | డీ | డు | డూ | డృ | డౄ | డె | డే | డై | డొ | డో | డౌ | డం | డః |
| **ఢ** | ఢ | ఢా | ఢి | ఢీ | ఢు | ఢూ | ఢృ | ఢౄ | ఢె | ఢే | ఢై | ఢొ | ఢో | ఢౌ | ఢం | ఢః |
| **ణ** | ణ | ణా | ణి | ణీ | ణు | ణూ | ణృ | ణౄ | ణె | ణే | ణై | ణొ | ణో | ణౌ | ణం | ణః |
| **త** | త | తా | తి | తీ | తు | తూ | తృ | తౄ | తె | తే | తై | తొ | తో | తౌ | తం | తః |
| **థ** | థ | థా | థి | థీ | థు | థూ | థృ | థౄ | థె | థే | థై | థొ | థో | థౌ | థం | థః |
| **ద** | ద | దా | ది | దీ | దు | దూ | దృ | దౄ | దె | దే | దై | దొ | దో | దౌ | దం | దః |
| **ధ** | ధ | ధా | ధి | ధీ | ధు | ధూ | ధృ | ధౄ | ధె | ధే | ధై | ధొ | ధో | ధౌ | ధం | ధః |
| **న** | న | నా | ని | నీ | ను | నూ | నృ | నౄ | నె | నే | నై | నొ | నో | నౌ | నం | నః |
| **ప** | ప | పా | పి | పీ | పు | పూ | పృ | పౄ | పె | పే | పై | పొ | పో | పౌ | పం | పః |
| **ఫ** | ఫ | ఫా | ఫి | ఫీ | ఫు | ఫూ | ఫృ | ఫౄ | ఫె | ఫే | ఫై | ఫొ | ఫో | ఫౌ | ఫం | ఫః |
| **బ** | బ | బా | బి | బీ | బు | బూ | బృ | బౄ | బె | బే | బై | బొ | బో | బౌ | బం | బః |
| **భ** | భ | భా | భి | భీ | భు | భూ | భృ | భౄ | భె | భే | భై | భొ | భో | భౌ | భం | భః |
| **మ** | మ | మా | మి | మీ | ము | మూ | మృ | మౄ | మె | మే | మై | మొ | మో | మౌ | మం | మః |
| **య** | య | యా | యి | యీ | యు | యూ | యృ | యౄ | యె | యే | యై | యొ | యో | యౌ | యం | యః |
| **ర** | ర | రా | రి | రీ | రు | రూ | రృ | రౄ | రె | రే | రై | రొ | రో | రౌ | రం | రః |
| **ల** | ల | లా | లి | లీ | లు | లూ | లృ | లౄ | లె | లే | లై | లొ | లో | లౌ | లం | లః |
| **వ** | వ | వా | వి | వీ | వు | వూ | వృ | వౄ | వె | వే | వై | వొ | వో | వౌ | వం | వః |
| **శ** | శ | శా | శి | శీ | శు | శూ | శృ | శౄ | శె | శే | శై | శొ | శో | శౌ | శం | శః |
| **ష** | ష | షా | షి | షీ | షు | షూ | షృ | షౄ | షె | షే | షై | షొ | షో | షౌ | షం | షః |
| **స** | స | సా | సి | సీ | సు | సూ | సృ | సౄ | సె | సే | సై | సొ | సో | సౌ | సం | సః |
| **హ** | హ | హా | హి | హీ | హు | హూ | హృ | హౄ | హె | హే | హై | హొ | హో | హౌ | హం | హః |
| **ళ** | ళ | ళా | ళి | ళీ | ళు | ళూ | ళృ | ళౄ | ళె | ళే | ళై | ళొ | ళో | ళౌ | ళం | ళః |
| **క్ష** | క్ష | క్షా | క్షి | క్షీ | క్షు | క్షూ | క్షృ | క్షౄ | క్షె | క్షే | క్షై | క్షొ | క్షో | క్షౌ | క్షం | క్షః |
| **ఱ** | ఱ | ఱా | ఱి | ఱీ | ఱు | ఱూ | ఱృ | ఱౄ | ఱె | ఱే | ఱై | ఱొ | ఱో | ఱౌ | ఱం | ఱః |

---

## 6. వత్తులు (Subscript Consonant Vatthulu)

> A Vattu in Unicode is formed by `Virama (్) + Consonant`.
> E.g., `్ + క` = `్క` (క-వత్తు).

| Consonant | Vattu Glyph | Unicode Breakdown | Current Status | Suggested Keystroke (Subscript Mode) | Your Preferred Keystroke(s) |
|---|---|---|---|---|---|
| క | **్క** | `U+0C4D + U+0C15` | `[EXISTS]` | `kka` or `k~k` | |
| ఖ | **్ఖ** | `U+0C4D + U+0C16` | `[MISSING]` | `k-kha` or `k~kh` | |
| గ | **్గ** | `U+0C4D + U+0C17` | `[EXISTS]` | `gga` | |
| ఘ | **్ఘ** | `U+0C4D + U+0C18` | `[MISSING]` | `g-gha` | |
| ఙ | **్ఙ** | `U+0C4D + U+0C19` | `[MISSING]` | `nnga` | |
| చ | **్చ** | `U+0C4D + U+0C1A` | `[EXISTS]` | `cca` or `chcha` | |
| ఛ | **్ఛ** | `U+0C4D + U+0C1B` | `[EXISTS]` | `ccha` | |
| జ | **్జ** | `U+0C4D + U+0C1C` | `[EXISTS]` | `jja` | |
| ఝ | **్ఝ** | `U+0C4D + U+0C1D` | `[MISSING]` | `jjha` | |
| ఞ | **్ఞ** | `U+0C4D + U+0C1E` | `[MISSING]` | `nnya` | |
| ట | **్ట** | `U+0C4D + U+0C1F` | `[EXISTS]` | `TTa` | |
| ఠ | **్ఠ** | `U+0C4D + U+0C20` | `[MISSING]` | `TTha` | |
| డ | **్డ** | `U+0C4D + U+0C21` | `[EXISTS]` | `DDa` | |
| ఢ | **్ఢ** | `U+0C4D + U+0C22` | `[MISSING]` | `DDha` | |
| ణ | **్ణ** | `U+0C4D + U+0C23` | `[MISSING]` | `NNa` | |
| త | **్త** | `U+0C4D + U+0C24` | `[EXISTS]` | `tta` | |
| థ | **్థ** | `U+0C4D + U+0C25` | `[MISSING]` | `ttha` | |
| ద | **్ద** | `U+0C4D + U+0C26` | `[EXISTS]` | `dda` | |
| ధ | **్ధ** | `U+0C4D + U+0C27` | `[MISSING]` | `ddha` | |
| న | **్న** | `U+0C4D + U+0C28` | `[EXISTS]` | `nna` | |
| ప | **్ప** | `U+0C4D + U+0C2A` | `[EXISTS]` | `ppa` | |
| ఫ | **్ఫ** | `U+0C4D + U+0C2B` | `[MISSING]` | `ppha` | |
| బ | **్బ** | `U+0C4D + U+0C2C` | `[EXISTS]` | `bba` | |
| భ | **్భ** | `U+0C4D + U+0C2D` | `[MISSING]` | `bbha` | |
| మ | **్మ** | `U+0C4D + U+0C2E` | `[EXISTS]` | `mma` | |
| య | **్య** | `U+0C4D + U+0C2F` | `[EXISTS]` | `yya` / `C+ya` | |
| ర | **్ర** | `U+0C4D + U+0C30` | `[EXISTS]` | `rra` / `C+ra` | |
| ల | **్ల** | `U+0C4D + U+0C32` | `[EXISTS]` | `lla` / `C+la` | |
| వ | **్వ** | `U+0C4D + U+0C35` | `[EXISTS]` | `vva` / `C+va` | |
| శ | **్శ** | `U+0C4D + U+0C36` | `[MISSING]` | `shsha` | |
| ష | **్ష** | `U+0C4D + U+0C37` | `[MISSING]` | `ShSha` | |
| స | **్స** | `U+0C4D + U+0C38` | `[EXISTS]` | `ssa` | |
| హ | **్హ** | `U+0C4D + U+0C39` | `[MISSING]` | `hha` | |
| ళ | **్ళ** | `U+0C4D + U+0C33` | `[EXISTS]` | `LLa` | |
| ఱ | **్ఱ** | `U+0C4D + U+0C31` | `[MISSING]` | `RRa` | |
| క్ష | **్క్ష** | `U+0C4D + U+0C15...`| `[MISSING]` | `ksha` vattu | |

---

## 7. ద్విత్వాక్షరాలు (Geminates / Double Consonants: C1 + C1)

> Formed when the same consonant is doubled (e.g. `క్క = k + k + a`).

| Telugu | Meaning / Example Word | Current Mapping | Status | Suggested Keystroke | Your Preferred Keystroke(s) |
|---|---|---|---|---|---|
| **క్క** | కుక్క (Dog), అక్క (Sister) | `kka` | `[EXISTS]` | `kka` | |
| **ఖ్ఖ** | దాఖ్ఖా | *None* | `[MISSING]` | `khkha` / `KKa` | |
| **గ్గ** | దగ్గు (Cough), బొగ్గు (Coal) | `gga` | `[EXISTS]` | `gga` | |
| **ఘ్ఘ** | సంఘ్ఘటన | *None* | `[MISSING]` | `ghgha` | |
| **ఙ్ఙ** | వాఙ్ఙయము | *None* | `[MISSING]` | `ngnga` | |
| **చ్చ** | పచ్చ (Green), రచ్చ | `cca` | `[EXISTS]` | `chcha` / `cca` | |
| **చ్ఛ** | స్వచ్ఛమైన (Pure), ఇచ్చ | `ccha` | `[EXISTS]` | `ccha` / `ChCha` | |
| **జ్జ** | బుజ్జి (Dear), సజ్జ | `jja` | `[EXISTS]` | `jja` | |
| **ఝ్ఝ** | ఝ్ఝ | *None* | `[MISSING]` | `jhjha` | |
| **ట్ట** | చెట్టు (Tree), బుట్ట (Basket) | `TTa` | `[EXISTS]` | `TTa` | |
| **ఠ్ఠ** | కమఠ్ఠము | *None* | `[MISSING]` | `ThTha` | |
| **డ్డ** | గుడ్డు (Egg), లడ్డు (Laddu) | `DDa` | `[EXISTS]` | `DDa` | |
| **ఢ్ఢ** | గూఢ్ఢము | *None* | `[MISSING]` | `DhDha` | |
| **ణ్ణ** | కన్ను / అణ్ణా (Brother) | *None* | `[MISSING]` | `NNa` | |
| **త్త** | అత్త (Aunt), ఉత్తరం (Letter) | `tta` | `[EXISTS]` | `tta` | |
| **థ్థ** | పథ్థ్యము | *None* | `[MISSING]` | `ththa` | |
| **ద్ద** | ముద్దు (Kiss), నిద్ర/పెద్ద (Big) | `dda` | `[EXISTS]` | `dda` | |
| **ద్ధ** | యుద్ధం (War), బుద్ధుడు (Buddha) | *None* | `[MISSING]` | `ddha` / `d-dha` | |
| **న్న** | అమ్మ / నాన్న (Father), వెన్న | `nna` | `[EXISTS]` | `nna` | |
| **ప్ప** | తప్పు (Wrong), కప్ప (Frog) | `ppa` | `[EXISTS]` | `ppa` | |
| **ఫ్ఫ** | గుఫ్ఫ | *None* | `[MISSING]` | `ff` / `phpha` | |
| **బ్బ** | దెబ్బ (Hit), జబ్బ | `bba` | `[EXISTS]` | `bba` | |
| **భ్భ** | గర్భ్భ | *None* | `[MISSING]` | `bhbha` | |
| **మ్మ** | అమ్మ (Mother), బొమ్మ (Doll) | `mma` | `[EXISTS]` | `mma` | |
| **య్య** | నెయ్యి (Ghee), చెయ్యి (Hand) | `yya` | `[EXISTS]` | `yya` | |
| **ర్ర** | జుర్రు (Slurp), కుర్ర (Young) | *None* | `[MISSING]` | `rra` | |
| **ల్ల** | పిల్లి (Cat), చెల్లి (Sister) | `lla` | `[EXISTS]` | `lla` | |
| **వ్వ** | పువ్వు (Flower), నువ్వు (You) | `vva` | `[EXISTS]` | `vva` / `wwa` | |
| **శ్శ** | నిశ్శబ్దం (Silence) | *None* | `[MISSING]` | `shsha` | |
| **ష్ష** | ధనుష్షష్టి | *None* | `[MISSING]` | `ShSha` | |
| **స్స** | బస్సు (Bus), రస్సి | `ssa` | `[EXISTS]` | `ssa` | |
| **హ్హ** | ఆహ్లాదం / హ్హ | *None* | `[MISSING]` | `hha` | |
| **ళ్ళ** | నీళ్ళు (Water), కాళ్ళు (Legs) | `lla2` *(ad-hoc)* | `[CONFLICT]` | `LLa` | |
| **ఱ్ఱ** | గుఱ్ఱం (Horse), బఱ్ఱె | *None* | `[MISSING]` | `RRa` | |

---

## 8. సంయుక్తాక్షరాలు (High-Frequency Conjunct Consonants: C1 + C2)

### 8.1 Repha / ర-పొల్లు (R-Initial Conjuncts: `ర్ + హల్లు`)
> Very frequent in Sanskrit loan words and Telugu prose.

| Telugu | Example Word | Current Mapping | Status | Suggested Keystroke | Your Preferred Keystroke(s) |
|---|---|---|---|---|---|
| **ర్క** | మార్కెట్, ఆర్క | *None* | `[MISSING]` | `rka` | |
| **ర్గ** | మార్గం (Path), దుర్గ | *None* | `[MISSING]` | `rga` | |
| **ర్చ** | చర్చ (Discussion), ఖర్చు (Expense) | *None* | `[MISSING]` | `rcha` | |
| **ర్జ** | ఖర్జూరం, అర్జునుడు | *None* | `[MISSING]` | `rja` | |
| **ర్ణ** | వర్ణం (Color), పూర్ణ | *None* | `[MISSING]` | `rNa` | |
| **ర్త** | కర్త (Doer), భర్త (Husband) | *None* | `[MISSING]` | `rta` | |
| **ర్థ** | అర్థం (Meaning), ప్రార్థన (Prayer) | *None* | `[MISSING]` | `rtha` | |
| **ర్ద** | పర్ద, నిర్దోషి | *None* | `[MISSING]` | `rda` | |
| **ర్ధ** | స్పర్థ, అర్థరాత్రి | *None* | `[MISSING]` | `rdha` | |
| **ర్న** | గవర్నర్ (Governor) | *None* | `[MISSING]` | `rna` | |
| **ర్ప** | సర్పం (Snake), అర్పణ | *None* | `[MISSING]` | `rpa` | |
| **ర్భ** | గర్భం (Womb), సందర్భం | *None* | `[MISSING]` | `rbha` | |
| **ర్మ** | కర్మ (Karma), ధర్మం (Dharma) | *None* | `[MISSING]` | `rma` | |
| **ర్య** | సూర్యుడు (Sun), భార్య (Wife), కార్యం | `rya` | `[EXISTS]` | `rya` | |
| **ర్ల** | కుర్లా, జార్ల | *None* | `[MISSING]` | `rla` | |
| **ర్వ** | సర్వం (Everything), పూర్వ (East) | *None* | `[MISSING]` | `rva` | |
| **ర్శ** | దర్శనం (Sight), ఆదర్శం | *None* | `[MISSING]` | `rsha` / `rSa` | |
| **ర్ష** | వర్షం (Rain), హర్షం (Joy) | *None* | `[MISSING]` | `rSha` | |
| **ర్స్** | నర్స్ (Nurse), పార్సిల్ | *None* | `[MISSING]` | `rsa` / `rs` | |
| **ర్హ** | అర్హత (Eligibility) | *None* | `[MISSING]` | `rha` | |

---

### 8.2 ర-వత్తు Clusters (`హల్లు + ్ర` : Consonant + Ra)
| Telugu | Example Word | Current Mapping | Status | Suggested Keystroke | Your Preferred Keystroke(s) |
|---|---|---|---|---|---|
| **క్ర** | చక్రం (Wheel), క్రమం | `kra` | `[EXISTS]` | `kra` | |
| **గ్ర** | గ్రామము (Village), అగ్ర | `gra` | `[EXISTS]` | `gra` | |
| **ఘ్ర** | శీఘ్రం (Fast), వ్యాఘ్రం | *None* | `[MISSING]` | `ghra` | |
| **చ్ర** | చ్ర | *None* | `[MISSING]` | `chra` | |
| **జ్ర** | వజ్రం (Diamond) | *None* | `[MISSING]` | `jra` | |
| **ట్ర** | ట్రైన్ (Train), ట్రాఫిక్ | `Tra` | `[EXISTS]` | `Tra` | |
| **డ్ర** | డ్రైవర్ (Driver), డ్రస్సు | `Dra` | `[EXISTS]` | `Dra` | |
| **త్ర** | మిత్రుడు (Friend), సూత్రం | `tra` | `[EXISTS]` | `tra` | |
| **ద్ర** | చంద్రుడు (Moon), సముద్రం | `dra` | `[EXISTS]` | `dra` | |
| **ధ్ర** | ఆంధ్ర (Andhra) | *None* | `[MISSING]` | `dhra` | |
| **న్ర** | న్ర | `nra` | `[EXISTS]` | `nra` | |
| **ప్ర** | ప్రశ్న (Question), ప్రభావం | `pra` | `[EXISTS]` | `pra` | |
| **ఫ్ర** | ఫ్రాన్స్ (France) | *None* | `[MISSING]` | `phra` / `fra` | |
| **బ్ర** | బ్రతుకు (Life), బ్రహ్మ | `bra` | `[EXISTS]` | `bra` | |
| **భ్ర** | భ్రమ (Illusion), విభ్రమ | *None* | `[MISSING]` | `bhra` | |
| **మ్ర** | తామ్రం (Copper) | `mra` | `[EXISTS]` | `mra` | |
| **శ్ర** | శ్రమ (Labor), ఆశ్రమం | *None* | `[MISSING]` | `shra` / `Sra` | |
| **శ్రీ** | శ్రీ (Sri / Respected), శ్రీకృష్ణ | `sri`, `shri` | `[EXISTS]` | `sri` or `shree` | |
| **స్ర** | సహస్ర (Thousand), స్రవంతి | `sra` | `[EXISTS]` | `sra` | |
| **హ్ర** | హ్రస్వము (Short vowel) | `hra` | `[EXISTS]` | `hra` | |
| **క్ష్ర** | నక్షత్రం (క్ష్ర variations) | *None* | `[MISSING]` | `kshra` | |

---

### 8.3 య-వత్తు Clusters (`హల్లు + ్య` : Consonant + Ya)
| Telugu | Example Word | Current Mapping | Status | Suggested Keystroke | Your Preferred Keystroke(s) |
|---|---|---|---|---|---|
| **క్య** | వాక్యం (Sentence), ఐక్యం | `kya` | `[EXISTS]` | `kya` | |
| **ఖ్య** | ముఖ్యమైన (Important), సంఖ్య (Number) | *None* | `[MISSING]` | `khya` | |
| **గ్య** | భాగ్యం (Luck), ఆరోగ్యం (Health) | `gya` | `[EXISTS]` | `gya` | |
| **ఘ్య** | శ్లాఘ్యము | *None* | `[MISSING]` | `ghya` | |
| **చ్య** | ప్రాచ్యము | *None* | `[MISSING]` | `chya` | |
| **జ్య** | రాజ్యం (Kingdom), జ్యోతి (Flame) | `jya` | `[EXISTS]` | `jya` | |
| **ట్య** | నాట్యం (Dance) | *None* | `[MISSING]` | `Tya` | |
| **డ్య** | జాడ్యం | *None* | `[MISSING]` | `Dya` | |
| **ణ్య** | పుణ్యం (Virtue), అరణ్యం (Forest) | *None* | `[MISSING]` | `Nya` | |
| **త్య** | సత్యం (Truth), నిత్యం | `tya` | `[EXISTS]` | `tya` | |
| **థ్య** | పథ్యం, తథ్యము | *None* | `[MISSING]` | `thya` | |
| **ద్య** | విద్య (Education), ఉద్యోగం (Job) | `dya` | `[EXISTS]` | `dya` | |
| **ధ్య** | ధ్యానం (Meditation), మధ్య (Middle) | *None* | `[MISSING]` | `dhya` | |
| **న్య** | న్యాయం (Justice), ధన్యవాదాలు (Thanks)| `nya` | `[EXISTS]` | `nya` | |
| **ప్య** | రూప్యం | `pya` | `[EXISTS]` | `pya` | |
| **భ్య** | అభ్యంతరం, సభ్యుడు (Member) | *None* | `[MISSING]` | `bhya` | |
| **మ్య** | సౌమ్యం, రమ్య | `mya` | `[EXISTS]` | `mya` | |
| **ల్య** | కళ్యాణం, బాహుల్యం | `lya` | `[EXISTS]` | `lya` | |
| **వ్య** | ద్రవ్యం, దివ్యమైన (Divine) | *None* | `[MISSING]` | `vya` | |
| **శ్య** | దృశ్యం (Scene), అవశ్యం | *None* | `[MISSING]` | `shya` | |
| **ష్య** | భవిష్యత్తు (Future), శిష్యుడు (Student)| *None* | `[MISSING]` | `Shya` | |
| **స్య** | రహస్యం (Secret), తపస్య | `sya` | `[EXISTS]` | `sya` | |
| **హ్య** | బాహ్యము (External), సహ్యం | `hya` | `[EXISTS]` | `hya` | |
| **క్ష్య** | లక్ష్యం (Goal), సాక్ష్యం (Evidence) | *None* | `[MISSING]` | `kshya` | |

---

### 8.4 వ-వత్తు Clusters (`హల్లు + ్వ` : Consonant + Va)
| Telugu | Example Word | Current Mapping | Status | Suggested Keystroke | Your Preferred Keystroke(s) |
|---|---|---|---|---|---|
| **క్వ** | పక్వం, క్వారీ | `kva` | `[EXISTS]` | `kva` / `kwa` | |
| **గ్వ** | దిగ్వజయం | *None* | `[MISSING]` | `gva` / `gwa` | |
| **జ్వ** | జ్వాల (Flame), ఉజ్వల | *None* | `[MISSING]` | `jva` / `jwa` | |
| **ట్వ** | ట్విట్టర్ (Twitter), పట్వారం | `Tva` | `[EXISTS]` | `Tva` / `Twa` | |
| **త్వ** | తత్వం (Philosophy), వ్యక్తిత్వం | `tva` | `[EXISTS]` | `tva` / `twa` | |
| **ద్వ** | ద్వారా (Through), ద్వారం (Door) | `dva` | `[EXISTS]` | `dva` / `dwa` | |
| **ధ్వ** | ధ్వని (Sound), విధ్వంసం | *None* | `[MISSING]` | `dhva` / `dhwa` | |
| **న్వ** | అన్వయం | `nva` | `[EXISTS]` | `nva` / `nwa` | |
| **ప్వ** | ప్వ | *None* | `[MISSING]` | `pva` | |
| **ల్వ** | బిల్వం | *None* | `[MISSING]` | `lva` / `lwa` | |
| **శ్వ** | విశ్వం (Universe), ఈశ్వరుడు (Shiva)| *None* | `[MISSING]` | `shva` / `shwa` | |
| **స్వ** | స్వతంత్రం (Freedom), స్వాగతం (Welcome)| `sva` | `[EXISTS]` | `sva` / `swa` | |
| **హ్వ** | ఆహ్వానం (Invitation), జిహ్వ (Tongue) | *None* | `[MISSING]` | `hva` / `hwa` | |

---

### 8.5 ల-వత్తు Clusters (`హల్లు + ్ల` : Consonant + La)
| Telugu | Example Word | Current Mapping | Status | Suggested Keystroke | Your Preferred Keystroke(s) |
|---|---|---|---|---|---|
| **క్ల** | క్లిష్టమైన (Complex), క్లాస్ (Class)| `kla` | `[EXISTS]` | `kla` | |
| **గ్ల** | గ్లాసు (Glass), గ్లూకోజ్ | *None* | `[MISSING]` | `gla` | |
| **త్ల** | అట్లతద్ది, రోత్ల | `tla` | `[EXISTS]` | `tla` | |
| **ప్ల** | ప్లీజ్ (Please), విప్లవం (Revolution)| `pla` | `[EXISTS]` | `pla` | |
| **బ్ల** | బ్లౌజ్, బ్లాక్ (Black) | *None* | `[MISSING]` | `bla` | |
| **మ్ల** | ఆమ్లం (Acid) | *None* | `[MISSING]` | `mla` | |
| **శ్ల** | శ్లోకం (Shloka), అశ్లీలం | *None* | `[MISSING]` | `shla` | |
| **స్ల** | స్లేటు (Slate), ముస్లిం | *None* | `[MISSING]` | `sla` | |
| **హ్ల** | ఆహ్లాదం (Pleasantness) | *None* | `[MISSING]` | `hla` | |

---

### 8.6 న-వత్తు & మ-వత్తు Clusters (`-్న` / `-్మ` : Consonant + Na / Ma)
| Telugu | Example Word | Current Mapping | Status | Suggested Keystroke | Your Preferred Keystroke(s) |
|---|---|---|---|---|---|
| **త్న** | రత్నం (Gem), యత్నం (Effort) | *None* | `[MISSING]` | `tna` | |
| **ద్న** | ద్న | *None* | `[MISSING]` | `dna` | |
| **స్న** | స్నానం (Bath), స్నేహం (Friendship) | *None* | `[MISSING]` | `sna` | |
| **హ్న** | చిహ్నం (Symbol), మధ్యాహ్నం (Afternoon)| *None* | `[MISSING]` | `hna` | |
| **క్ష్మ** | లక్ష్మి (Lakshmi), సూక్ష్మం (Micro)| *None* | `[MISSING]` | `kshma` | |
| **త్మ** | ఆత్మ (Soul), మహాత్ముడు (Mahatma) | *None* | `[MISSING]` | `tma` | |
| **ప్య / ప్మ** | పద్మం (Lotus - ద్మ), పద్మ | *None* | `[MISSING]` | `dma` | |
| **భ్మ** | భ్మ | *None* | `[MISSING]` | `bhma` | |
| **స్మ** | స్మరణ, భస్మం (Ash) | *None* | `[MISSING]` | `sma` | |
| **హ్మ** | బ్రహ్మ (Brahma), బ్రాహ్మణుడు | `hma` | `[EXISTS]` | `hma` | |
| **ష్మ** | గ్రీష్మం (Summer), భీష్ముడు | *None* | `[MISSING]` | `Shma` | |

---

### 8.7 ఇతర ముఖ్యమైన సంయుక్తాక్షరాలు (Sibilant, Nasal & Classical Clusters)
| Telugu | Example Word | Current Mapping | Status | Suggested Keystroke | Your Preferred Keystroke(s) |
|---|---|---|---|---|---|
| **ష్ట** | కష్టం (Hardship), ఇష్టం (Liking) | *None* | `[MISSING]` | `Shta` | |
| **ష్ఠ** | శ్రేష్ఠమైన (Best), ప్రతిష్ఠ | *None* | `[MISSING]` | `ShTha` | |
| **ష్ణ** | కృష్ణుడు (Krishna), విష్ణువు | *None* | `[MISSING]` | `ShNa` | |
| **ష్ప** | పుష్పం (Flower), బాష్పం (Tear) | *None* | `[MISSING]` | `Shpa` | |
| **స్త** | పుస్తకం (Book), ప్రస్తుత (Present)| *None* | `[MISSING]` | `sta` | |
| **స్థ** | స్థలం (Place), పరిస్థితి (Condition)| *None* | `[MISSING]` | `stha` | |
| **స్ప** | స్పర్శ (Touch), స్పష్టం (Clear) | *None* | `[MISSING]` | `spa` | |
| **స్ఫ** | స్ఫూర్తి (Inspiration), స్ఫోటకం | *None* | `[MISSING]` | `spha` | |
| **శ్చ** | ఆశ్చర్యం (Surprise), పశ్చాత్తాపం| *None* | `[MISSING]` | `shcha` | |
| **శ్న** | ప్రశ్న (Question) | *None* | `[MISSING]` | `shna` | |
| **ప్త** | ప్రాప్తం, సుప్త | *None* | `[MISSING]` | `pta` | |
| **బ్ద** | శబ్దం (Sound), శతాబ్దం (Century)| *None* | `[MISSING]` | `bda` | |
| **బ్జ** | అబ్జం | *None* | `[MISSING]` | `bja` | |
| **గ్ధ** | ముగ్ధ | *None* | `[MISSING]` | `gdha` | |
| **ద్ధ** | యుద్ధం (War), ప్రసిద్ధ | *None* | `[MISSING]` | `ddha` | |
| **క్త** | భక్తి (Devotion), ముక్తి (Salvation)| *None* | `[MISSING]` | `kta` | |
| **ఙ్క** | అఙ్కము (Sanskrit style) | *None* | `[MISSING]` | `ngka` | |
| **ఞ్చ** | పఞ్చ (Sanskrit style) | *None* | `[MISSING]` | `ncha` | |
| **ణ్ట** | కణ్టకము | *None* | `[MISSING]` | `NTa` | |
| **ణ్డ** | దణ్డము | *None* | `[MISSING]` | `NDa` | |
| **న్త** | అనన్తము (Non-anusvara style) | *None* | `[MISSING]` | `nta` | |
| **న్ద** | చన్ద్రుడు | *None* | `[MISSING]` | `nda` | |
| **మ్ప** | కంపము (Non-anusvara) | *None* | `[MISSING]` | `mpa` | |
| **మ్బ** | అంబ (Non-anusvara) | *None* | `[MISSING]` | `mba` | |

---

## 9. సంశ్లేషాక్షరాలు (3+ Consonant Conjuncts: C1 + C2 + C3)

> When three or more consonants combine before a vowel. E.g. `స్త్ర` = `స + త + ర + అ`.

| Telugu | Breakdown | Example Word | Current Status | Suggested Keystroke | Your Preferred Keystroke(s) |
|---|---|---|---|---|---|
| **స్త్ర** | `స్ + త్ + ర` | వస్త్రం (Cloth), శాస్త్రం (Science), అస్త్రం | `[MISSING]` | `stra` | |
| **ర్త్స్న** | `ర్ + త్ + స్ + న` | కార్త్స్న్యము | `[MISSING]` | `rtsna` | |
| **త్స్న** | `త్ + స్ + న` | జ్యోత్స్న (Moonlight) | `[MISSING]` | `tsna` | |
| **క్ష్మ్య** | `క్ + ష్ + మ్ + య`| లక్ష్మ్యనుగ్రహం | `[MISSING]` | `kshmya` | |
| **ర్ధ్య** | `ర్ + ధ్ + య` | దౌర్ధ్యం | `[MISSING]` | `rdhya` | |
| **ష్ట్య** | `ష్ + ట్ + య` | దాష్ట్యం | `[MISSING]` | `Shtya` | |
| **క్ష్ర** | `క్ + ష్ + ర` | నక్షత్రం (old alternate) | `[MISSING]` | `kshra` | |
| **ర్ష్ణ** | `ర్ + ష్ + ణ` | వార్ష్ణేయ | `[MISSING]` | `rShNa` | |
| **ర్ద్వ్య** | `ర్ + ద్ + వ్ + య`| దౌర్ద్వ్యము | `[MISSING]` | `rdvya` | |
| **స్ట్ర** | `స్ + ట్ + ర` | స్ట్రైట్ (Straight), స్ట్రక్చర్ (Structure)| `[MISSING]` | `sTra` | |
| **స్ప్ర** | `స్ + ప + ర` | స్ప్రింగ్ (Spring) | `[MISSING]` | `spra` | |
| **స్క్ర** | `స్ + క + ర` | స్క్రీన్ (Screen) | `[MISSING]` | `skra` | |

---

## 10. తెలుగు అంకెలు & సంఖ్యా చిహ్నాలు (Telugu Numerals)

| Digit | Telugu Numeral | Name | Current Status | Suggested Keystroke | Your Preferred Keystroke(s) |
|---|---|---|---|---|---|
| 0 | **౦** | సున్నా (Sunna) | `[MISSING]` | `0~` or `#0` | |
| 1 | **౧** | ఒకటి (Okati) | `[MISSING]` | `1~` or `#1` | |
| 2 | **౨** | రెండు (Rendu) | `[MISSING]` | `2~` or `#2` | |
| 3 | **౩** | మూడు (Moodu) | `[MISSING]` | `3~` or `#3` | |
| 4 | **౪** | నాలుగు (Naalugu) | `[MISSING]` | `4~` or `#4` | |
| 5 | **౫** | ఐదు (Aidu) | `[MISSING]` | `5~` or `#5` | |
| 6 | **౬** | ఆరు (Aaru) | `[MISSING]` | `6~` or `#6` | |
| 7 | **౭** | ఏడు (Eedu) | `[MISSING]` | `7~` or `#7` | |
| 8 | **౮** | ఎనిమిది (Enimidi) | `[MISSING]` | `8~` or `#8` | |
| 9 | **౯** | తొమ్మిది (Tommidi) | `[MISSING]` | `9~` or `#9` | |

---

## 11. సాంప్రదాయ విరామ చిహ్నాలు (Telugu Traditional Punctuation & Signs)

| Symbol | Name | Description | Current Status | Suggested Keystroke | Your Preferred Keystroke(s) |
|---|---|---|---|---|---|
| **।** | దండ (Danda) | Poetic / Sanskrit verse pause (U+0964) | `[MISSING]` | `|` or `..` | |
| **॥** | ద్వంద్వ దండ (Double Danda) | Stanza end (U+0965) | `[MISSING]` | `||` | |
| **ౘ** | దంత్య చ (Tsa) | Spoken Telugu affricate (U+0C58) | `[MISSING]` | `~ch` or `ts` | |
| **ౙ** | దంత్య జ (Dza) | Spoken Telugu affricate (U+0C59) | `[MISSING]` | `~j` or `dz` | |
| **ఴ** | ద్రవిడ ళ/ర (Zha) | Archaic retroflex liquid (U+0C34) | `[MISSING]` | `zha` or `~L` | |
| **ౚ** | నకారపొల్లు (Chillu N) | Native Telugu pure n (U+0C5A) | `[MISSING]` | `n_` or `N~` | |

---

## 12. నిత్య జీవితంలో తరచూ తప్పులు జరిగే క్లిష్టమైన పదాలు (Test Words & Edge Cases)

> These are the exact words users find "off-beat" when typing in Tenglish.
> Please review how you would intuitively type these words in English:

| Telugu Word | Meaning | What Often Breaks | Suggested Keystroke | Your Preferred Keystroke(s) |
|---|---|---|---|---|
| **రచయిత** | Writer (App Name) | User types `rachayitha` (expects `త`, but engine puts `థ`) | `rachayitha` or `rachayita` | |
| **నమస్కారం** | Greetings | `am` vs `aM` (users type `namaskaram` with lowercase `m`) | `namaskAram` / `namaskaram` | |
| **భారతదేశం** | India | `bh` / `th` / `dEsham` | `bhAratadEshaM` | |
| **శ్రీకృష్ణదేవరాయ**| Sri Krishnadevaraya | `sri` / `shri`, `kRuShNa` vs `krishna` | `shrIkRuShNadEvarAya` | |
| **విద్యార్థి** | Student | `dya` + `rthi` (Repha combined with `థి`) | `vidyArthi` | |
| **అధ్యక్షుడు** | President / Chairman | `dhya` + `kshu` | `adhyakshuDu` | |
| **జ్యోత్స్న** | Moonlight | Double cluster: `jyo` + `tsna` | `jyOtsna` | |
| **లక్ష్మి** | Goddess Lakshmi | `ksha` + `ma` vattu (`క్ష్మ` + `ి`) | `lakshmi` or `lakShmi` | |
| **బ్రహ్మ** | Creator Brahma | `bra` + `hma` | `brahma` | |
| **ధన్యవాదాలు** | Thank you | `nya` | `dhanyavAdAlu` | |
| **పెళ్ళి** | Marriage | `LLi` (ళ-గుణింతం with ళ-వత్తు: `ళ్ళి`) | `peLLi` | |
| **ప్రభుత్వం** | Government | `pra` + `bhu` + `tvam` | `prabhutvaM` | |
| **ఆశ్చర్యం** | Surprise | `shcha` + `rya` + `M` | `AshcharyaM` | |
| **నిష్కర్ష** | Verdict / Stern | `Shka` + `rSha` | `niShkarSha` | |
| **దుఃఖం** | Sorrow / Grief | Visarga in middle: `duHkham` | `duHkhaM` | |
| **మధ్యాహ్నం** | Afternoon | `dhya` + `hna` (`హ్న` + `ం`) | `madhyAhnaM` | |
| **చేయండి** | Please do (Polite) | `MDi` vs `ndi` | `chEyaMDi` / `cheyandi` | |
| **తెలుగులో** | In Telugu | Long `O` vs short `o` | `telugulO` / `telugulo` | |

---

## 13. కీస్ట్రోక్ నియమాల రూపకల్పన ప్రశ్నలు (Keystroke Logic Design Decisions)

Please specify your rules for the engine architecture:

1. **Halant vs Full Letter by default**:
   - When the user presses `k`:
     - [ ] **Option 1**: Show `క` immediately (Inherent `a`). If followed by another consonant `k`, convert to `క్క`. To get standalone `క్`, press `k~` or `k/`.
     - [ ] **Option 2**: Show `క్` immediately (Halant-first). Pressing `a` makes it `క`. Pressing `i` makes it `కి`. Pressing another consonant `k` makes it `క్క`.
   
2. **Short vs Long Vowels (`e`/`E`, `o`/`O`)**:
   - In informal chatting, many type `ee` for `ఈ` and `oo` for `ఊ`.
   - But in RTS Telugu: `e` = `ఎ`, `E` / `ee` = `ఏ`.
   - How should `ee` behave?
     - `ee` = [ ] **ఈ**  or  [ ] **ఏ**
   - How should `oo` behave?
     - `oo` = [ ] **ఊ**  or  [ ] **ఓ**

3. **Soft `త` vs Hard `ట`**:
   - `t` = [ ] **త**  or  [ ] **ట**
   - `T` = [ ] **ట**
   - `th` = [ ] **థ** (Mahaprana)  or  [ ] **త** (Alpaprana like `rachayitha`)

4. **Sunna / Anusvara (`ం`)**:
   - Should typing lowercase `m` at the end of a word or before consonant automatically offer/convert to `ం` (e.g. `namaskaram` -> `నమస్కారం`)?
     - [ ] Yes, auto-convert word-ending `am`/`em`/`im` to `ం`.
     - [ ] No, require capital `M` (e.g. `namaskAraM`).
