# Rachayitha (రచయిత) - Product Requirements Document (PRD)
**Version 2.0 (Production Release)** | *Created by Ramaputhra*

---

## 1. Vision & Purpose
**Rachayitha** (రచయిత - Telugu for *"Writer"* / *"Author"*) is an ultralight, offline desktop utility designed for native Telugu phonetic transliteration. It sits silently in the Windows System Tray and allows users to type phonetically in Roman script (Tenglish) and automatically see it transform in real-time into native Telugu script across **any desktop application** (MS Word, Notepad, Chrome, WhatsApp Desktop, Slack, VS Code, etc.).

---

## 2. Core Architectural Pillars

### 2.1 Natural Halant-First (Pollu-First) Typing Model
- **Single Keystroke = Pure Half-Letter (with Virama `్`):**
  - `n` $\rightarrow$ **న్**, `N` $\rightarrow$ **ణ్**, `k` $\rightarrow$ **క్**, `m` $\rightarrow$ **మ్**, `t` $\rightarrow$ **త్**, `ksh` $\rightarrow$ **క్ష్**
- **Followed by `'a'` = Full Consonant (removes virama):**
  - `na` $\rightarrow$ **న**, `Na` $\rightarrow$ **ణ**, `ka` $\rightarrow$ **క**, `ksha` / `Ksha` $\rightarrow$ **క్ష**
- **Followed by other vowels = Proper Gunintham:**
  - `ni` $\rightarrow$ **ని**, `nu` $\rightarrow$ **ను**, `kaa` $\rightarrow$ **కా**, `kshi` $\rightarrow$ **క్షి**
- **Doubled Consonants = Vatthulu (ద్విత్వాలు & సంయుక్తాక్షరాలు):**
  - `nna` $\rightarrow$ **న్న**, `kka` $\rightarrow$ **క్క**, `amma` $\rightarrow$ **అమ్మ**
  - Word endings with consonants naturally form half-letters without typing `~` (e.g. `jagan` $\rightarrow$ **జగన్**, `bhArat` $\rightarrow$ **భారత్**).

### 2.2 Casual Typing & Conversational Lexicon Engine
- Fast dictionary lookup across 58,678 high-frequency colloquial Tenglish stems.
- Intelligent phonetic decompounding, prefix/suffix handling, and interrogative/habitual verb resolution.
- Dynamic candidate generator resolving colloquial ambiguities (`matlade` $\to$ **మాట్లాడే**, `nenenduku` $\to$ **నేనెందుకు**, `veltanu` $\to$ **వెళ్తాను**, `sarele` $\to$ **సరేలే**).

### 2.3 IndicCorp 1M Trigram Language Model & Contextual Polarity
- 34.7M Token statistical language model running 100% locally with zero latency.
- Dynamic polarity disambiguation (e.g. `akkada evaru leru` $\to$ **అక్కడ ఎవరూ లేరు** vs `akkada evaru unnaru` $\to$ **అక్కడ ఎవరు ఉన్నారు**).
- Contextual collocation scoring for polysemous words (e.g. `inko sari vellanu` $\to$ **ఇంకో సారి వెళ్లను**).

### 2.4 Desktop Next-Word Prediction & Ghost Pill Overlay
- Real-time n-gram next-word suggestions shown in a floating acrylic ghost pill near the active caret.
- Instant acceptance using the **[Tab ⇥]** key.
- 100% offline, zero network telemetry, ultra-low memory footprint (~25 MB RAM).

### 2.5 Real-Time 3-Word Sliding Window Retroactive Correction
- Continuously maintains preceding unigrams and bigrams.
- If subsequent words disambiguate a prior ambiguous candidate, the engine automatically issues non-destructive backspaces and rewrites the optimal Telugu phrasing seamlessly.

### 2.6 Dynamic System Tray Icon (Language Indicator)
- **Telugu Active:** Tray icon displays **`తె`** in a vibrant indigo gradient badge.
- **English Active:** Tray icon displays **`EN`** in a modern slate badge.
- Users can always verify their active language at a glance on the Windows taskbar clock area.

### 2.7 Authentic In-Place Live Playground
- Single unified interactive document sandbox operating directly on the native `TypingBuffer` core engine.
- Real-time in-place Halant-First transformation directly where the user types without misleading dual-box translation.
- Live Next-Word Prediction ghost pill bar with [Tab ⇥] autocomplete acceptance.
- Real-time 3-word sliding window retroactive correction HUD and benchmark simulation runner.
- Live Alt+T toggle testing between Telugu and English mode.

### 2.8 Professional Standalone Installer
- Single self-contained installer (`Rachayitha_Setup.exe`).
- **Feature Presentation Carousel:** Showcases core capabilities while installing.
- **Automated Configuration:** Installs to `%LOCALAPPDATA%\Programs\Rachayitha`, creates Desktop and Start Menu shortcuts, and enables auto-start on boot (`shell:startup`).
- **Clean Uninstaller:** Fully registered in Windows Settings $\rightarrow$ Installed Apps (Add/Remove Programs).

---

## 3. Clean Canonical File Structure

```
రచయిత/
├── PRD.md                       # Master Product Requirements Document v2.0
├── README.md                    # Project documentation & feature showcase
├── LICENSE                      # GPLv3 Open Source License
├── All.md                       # Master Telugu Keystroke & Unicode Blueprint
├── Golden-1000.json             # RTS Engine Gold Verification Dataset
├── build_installer.bat          # 1-Click Builder: Clean -> Test -> Compile
├── clean_workspace.py           # Canonical workspace cleaner & debt reducer
├── test_casual_type.py          # Standalone test runner (100% pass guarantee)
├── Rachayitha.exe               # Portable zero-install executable
├── Rachayitha_v2.exe            # Portable v2.0 zero-install executable
├── Rachayitha_Setup.exe         # Single setup installer with wizard
├── rachayitha code files/       # Core Python Desktop Application
│   ├── main.py                  # Main application loop, tray & keyboard hook
│   ├── make_single_installer.py # PyInstaller standalone & installer builder
│   ├── prepare_icons.py         # Multi-res icon generation utility
│   ├── test_casual_type.py      # Core unit & integration test suite
│   ├── requirements.txt         # Dependencies (PyQt6, keyboard, Pillow, pyinstaller)
│   ├── icon.ico                 # Multi-resolution Windows app icon
│   ├── icon.png                 # App icon PNG
│   ├── rachayitha_logo.png      # Master branding logo
│   ├── data/
│   │   ├── casual_candidates.json
│   │   ├── casual_type_dict.json
│   │   ├── config.json
│   │   ├── te_lm.json
│   │   ├── te_top10k.json
│   │   ├── telugu_rules.json
│   │   └── typo_fixes.json
│   ├── engine/
│   │   ├── __init__.py
│   │   ├── buffer.py            # Sliding window buffer & retroactive correction
│   │   ├── casual_type.py       # Conversational lexicon & candidate generation
│   │   ├── lm.py                # IndicCorp Trigram LM & collocations
│   │   ├── paths.py             # Bundle & config path resolver
│   │   ├── predictor.py         # Next-word prediction engine
│   │   └── transliterator.py    # Halant-First RTS phonetic engine
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── settings.py          # Settings GUI, Key Map Table & Live Hotkeys
│   │   ├── suggestion_overlay.py# Floating suggestion pill overlay
│   │   └── tray.py              # Dynamic 'తె'/'EN' System Tray Icon
│   └── installer_src/
│       └── setup_gui.py         # 2-Panel Carousel Setup Wizard & Uninstaller
├── WebSite/                     # Official Live Typing Playground & Web App
│   ├── index.html               # Web portal with SEO and interactive engine
│   ├── script.js                # In-browser transliteration engine
│   ├── style.css                # Modern responsive design system
│   ├── Rachayitha.exe           # Hosted portable download
│   ├── Rachayitha_v2.exe        # Hosted portable v2 download
│   └── Rachayitha_Setup.exe     # Hosted installer download
├── product_hunt_assets/         # High-resolution feature showcase graphics
└── scripts/                     # Data generation & language model utilities
```
