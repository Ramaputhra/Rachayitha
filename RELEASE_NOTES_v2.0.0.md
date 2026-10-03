# Rachayitha (రచయిత) v2.0.0 Production Release

> **Write Telugu at the speed of thought.**  
> *100% Offline • Zero Telemetry • 58k+ Lexicon • IndicCorp 1M Trigram Model • Tab Autocomplete • Adaptive Self-Learning*

---

## 🌟 What's New in Version 2.0.0

Rachayitha v2.0.0 represents a massive leap forward in desktop Telugu computing. Moving far beyond traditional rule-based transliteration, v2.0 introduces **contextual language modeling**, **desktop next-word prediction**, and an **offline adaptive self-learning engine** that personalizes to your vocabulary as you type.

---

### 1. 🧠 Offline Adaptive Self-Learning Engine (స్వయం అభ్యాసం)
Rachayitha now learns your personal writing style, preferred spellings, slang, names, and vocabulary **100% locally and privately**:
- **Automatic Retype Learning:** When you type a word, backspace it, and retype your desired Telugu spelling, Rachayitha automatically detects the correction and records it as your preferred transliteration for that English key.
- **Candidate Pill Reinforcement:** Selecting candidate pills from the typing HUD automatically boosts their priority in future casual typing sessions.
- **Personal Transition Bigrams:** Learns your common two-word phrases to suggest personalized next-word predictions.
- **Dedicated Self-Learning GUI Tab:**
  - View live profile stats: total learned words, boosts, and transitions.
  - Searchable learned words table with per-word removal.
  - Manual Custom Word creator for instant overrides (`Roman Input` $\to$ `Telugu Output`).
  - Safe Backup & Restore: **Export to JSON** and **Import from JSON**.
  - 100% Private: Stored locally in `%APPDATA%\Rachayitha\user_learned.json` with atomic disk writes. Zero cloud syncing.

---

### 2. 📚 IndicCorp 1M Trigram Language Model & Polarity Disambiguation
Trained on **IndicCorp 1 Million Telugu sentences (34.7 Million tokens)**, Rachayitha v2.0 natively resolves complex contextual nuances:
- **Negative vs Positive Polarity Disambiguation:**
  - `akkada evaru leru` $\to$ **అక్కడ ఎవరూ లేరు** *(Negative context automatically triggers emphatic deergham)*
  - `akkada evaru unnaru` $\to$ **అక్కడ ఎవరు ఉన్నారు** *(Positive interrogative context maintains standard vowel)*
  - `emi ledu` $\to$ **ఏమీ లేదు** vs `emi undi` $\to$ **ఏమి ఉంది**
  - `ekkada leru` $\to$ **ఎక్కడా లేరు** vs `ekkada unnaru` $\to$ **ఎక్కడ ఉన్నారు**
- **Zero-Latency Statistical Scoring:** Sub-millisecond transition probability calculation evaluated locally in RAM.

---

### 3. 🔮 Desktop Next-Word Prediction & `[Tab ⇥]` Ghost Autocomplete
Brings modern smartphone predictive typing to every desktop application across Windows:
- **Floating Ghost Pill Overlay:** Translucent acrylic badge (`Next: వస్తున్నా [Tab ⇥]`) appears seamlessly beside your active Windows caret.
- **One-Key Insertion:** Press **`Tab`** to instantly accept the predicted word and advance your sentence.
- **Focus-Free & Non-Intrusive:** Never steals window focus (`WA_ShowWithoutActivating`) and dismisses automatically on typing or escape.

---

### 4. ⚡ Real-Time 3-Word Sliding Window Retroactive Correction
- Continuously maintains a 3-word context window `(w_prev_prev, w_prev, w_curr)`.
- If a subsequent word clarifies an earlier ambiguous phonetic phrase, Rachayitha automatically issues atomic backspaces and rewrites the optimal Telugu phrase in **0 milliseconds**—completely transparent to the user.

---

### 5. ⌨️ 3-Tier Casual Typing Engine (No Shift Keys Needed!)
- **58,678-Word Colloquial Lexicon:** Natural lowercase Tenglish (`matladanu`, `repu`, `intiki`, `chala`, `bagundi`).
- **Telugu Sandhi Morphological Decomposer:** Automatically splits and conjugates 17 noun postpositions (`-to`, `-lo`, `-nundi`) and 25+ verb conjugations (e.g., `aadukuntunnaru` $\to$ **ఆడుకుంటున్నారు**).
- **Halant-First (Pollu-First) Core:** Deterministic phonetic foundation for complex Sanskrit conjuncts, vattulu, and classical literature.

---

### 6. 🎨 Dynamic Taskbar Tray & Modern Installer
- **Dynamic Taskbar Icon:** Displays a vibrant indigo **`తె`** badge when Telugu typing is active and a clean slate **`EN`** badge when in English mode.
- **Single-Click Setup Wizard (`Rachayitha_Setup_V2.exe`):** Complete with live feature showcase carousel, automatic Desktop/Start Menu shortcuts, auto-start on boot, and clean Windows uninstallation entry.
- **Standalone Portable Option (`Rachayitha_v2.exe`):** Zero installation required; run straight from a USB or folder.

---

## 📦 Release Assets & Downloads

| File | Size | Type | Description |
| :--- | :--- | :--- | :--- |
| **`Rachayitha_Setup_V2.exe`** | **~76.5 MB** | **Windows Installer (Recommended)** | 1-Click Setup Wizard with shortcuts, uninstaller, and all models bundled. |
| **`Rachayitha_v2.exe`** | **~37.5 MB** | **Portable Standalone** | Zero-install single binary. Runs immediately on any Windows 10/11 64-bit PC. |
| **Source code (zip / tar.gz)** | — | **Source Code** | Full Python 3.10+ source with PyQt6 UI and complete linguistic datasets. |

### Direct Download Links:
- **Installer (v2.0):** [Rachayitha_Setup_V2.exe](https://github.com/Ramaputhra/Rachayitha/releases/download/Rachayitha_V2/Rachayitha_Setup_V2.exe)
- **Portable (v2.0):** [Rachayitha_v2.exe](https://github.com/Ramaputhra/Rachayitha/releases/download/v2.0.0/Rachayitha_v2.exe)
- **Official Website:** [https://rachayitha.vercel.app](https://rachayitha.vercel.app/)

---

## 🔒 Verification & Privacy Guarantee

- **Air-Gapped Privacy:** Rachayitha requires **zero network access** and transmits **zero telemetry or analytics**. Your keystrokes and learned vocabulary stay strictly on your local PC.
- **License:** Auditable open-source licensed under the [GNU AGPLv3](https://github.com/Ramaputhra/Rachayitha/blob/main/LICENSE).
- **Compatibility:** Tested and optimized for 64-bit Windows 10 and Windows 11 across WhatsApp Desktop, Microsoft Word, Excel, Chrome, Notepad, Discord, Slack, and Terminal.

---

**Full Changelog:** [v1.0.0...v2.0.0](https://github.com/Ramaputhra/Rachayitha/compare/v1.0.0...v2.0.0)
