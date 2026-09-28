# Rachayitha (రచయిత) - Product Requirements Document (PRD)
**Version 1.0 (Production Release)** | *Inspiration: PramukhIME + Lekhini RTS*

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

### 2.2 Dynamic System Tray Icon (Language Indicator)
- **Telugu Active:** Tray icon displays **`తె`** in a vibrant indigo gradient badge.
- **English Active:** Tray icon displays **`EN`** in a modern slate badge.
- Users can always verify their active language at a glance on the Windows taskbar clock area.

### 2.3 Click-to-Open Settings & Key Map
- Left-click or double-click the tray icon to open the main window.
- **Key Map Table:** 60+ Telugu letters categorized with instant search filtering.
- **Live Custom Hotkeys:** Set custom toggle shortcut (Default: `Alt+T`) with immediate live re-registration.
- **Interactive Playground:** Live sandbox to test phonetic conversions immediately.

### 2.4 Professional Standalone Installer
- Single self-contained installer (`installer_output\Rachayitha_Setup.exe`).
- **Feature Presentation Carousel:** Showcases core capabilities while installing.
- **Automated Configuration:** Installs to `%LOCALAPPDATA%\Programs\Rachayitha`, creates Desktop and Start Menu shortcuts, and enables auto-start on boot (`shell:startup`).
- **Clean Uninstaller:** Fully registered in Windows Settings $\rightarrow$ Installed Apps (Add/Remove Programs).

---

## 3. Clean File Structure

```
రచయిత/
├── PRD.md                       # Master Product Requirements Document
├── README.md                    # Project documentation & usage guide
├── rachayitha_logo.png          # Official application master logo
├── clean_workspace.py           # Automated cleanup script
└── rachayitha code files/
    ├── main.py                  # Main application loop & tray manager
    ├── data/
    │   ├── config.json          # Default user configuration
    │   └── telugu_rules.json    # Complete Lekhini RTS rule matrices
    ├── engine/
    │   ├── buffer.py            # Real-time typing buffer & delta manager
    │   ├── paths.py             # Asset and %APPDATA% path resolver
    │   └── transliterator.py    # Halant-first phonetic parsing engine
    ├── ui/
    │   ├── settings.py          # Settings, Key Map Table & Playground GUI
    │   └── tray.py              # Dynamic 'తె'/'EN' System Tray Icon
    ├── installer_src/
    │   ├── setup_gui.py         # 2-Panel Professional Setup Wizard
    │   └── uninstaller_gui.py   # Windows Uninstaller routine
    ├── icon.ico                 # Multi-resolution Windows icon
    ├── icon.png                 # Standard PNG application icon
    ├── rachayitha_logo.png      # Bundled logo asset
    ├── requirements.txt         # Python dependencies (PyQt6, keyboard, Pillow, pyinstaller)
    ├── make_single_installer.py # Professional installer builder
    ├── build_standalone.bat     # 1-click standalone EXE builder
    ├── build_installer.bat      # 1-click single installer builder
    ├── Install_Rachayitha.bat   # 1-click direct system installer
    ├── dist/
    │   └── Rachayitha.exe       # Compiled standalone application
    └── installer_output/
        └── Rachayitha_Setup.exe # Compiled single installer
```
