<div align="center">

<img src="product_hunt_assets/01_product_hunt_icon_square_1x1.jpg" alt="Rachayitha Logo" width="128" style="border-radius: 24px;" />

# Rachayitha (రచయిత)
### Real-Time Phonetic Telugu Transliteration for Windows

[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS-0078D6?style=for-the-badge&logo=apple&logoColor=white)](https://github.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Privacy](https://img.shields.io/badge/Privacy-100%25%20Offline%20%7C%20Zero%20Telemetry-10B981?style=for-the-badge&logo=shield)](https://github)
[![License](https://img.shields.io/badge/License-MIT-F59E0B?style=for-the-badge)](LICENSE)

**Type natural Telugu anywhere in Windows without switching keyboards or using heavy cloud IMEs.**  
*Inspired by Lekhini RTS and PramukhIME, engineered with zero-latency halant-first phonetic mapping.*

<br/>

[![Rachayitha Hero Showcase](product_hunt_assets/02_hero_transliteration_16x9.jpg)](https://github)

</div>

---

## 📖 Overview

**Rachayitha (రచయిత)** is a native, ultra-lightweight Windows desktop utility that converts standard Roman phonetic keystrokes into elegant Telugu Unicode in real-time. 

Unlike traditional input methods that require bulky web APIs or cumbersome layout switching, Rachayitha hooks directly into low-level keyboard events to provide instant, seamless transliteration across **any application**—including WhatsApp Desktop, Microsoft Word, Notepad, Google Chrome, Discord, Slack, and IDEs.

---

## ✨ Features at a Glance

### 1. ⚡ Natural Halant-First (Pollu-First) Typing
Engineered to mirror the authentic phonetic structure of Telugu:
- **Single Keystroke = Pure Half-Letter (Pollu):**
  - Press `n` $\rightarrow$ **న్**
  - Press `k` $\rightarrow$ **క్**
  - Press `m` $\rightarrow$ **మ్**
- **Followed by Vowel = Full Consonant / Gunintham:**
  - `n` + `a` $\rightarrow$ **న**
  - `n` + `i` $\rightarrow$ **ని**
  - `n` + `u` $\rightarrow$ **ను**
  - `k` + `a` + `a` $\rightarrow$ **కా**
- **Automatic Conjuncts (ద్విత్వాలు & సంయుక్తాక్షరాలు):**
  - `nna` $\rightarrow$ **న్న**
  - `amma` $\rightarrow$ **అమ్మ**
  - `ksha` $\rightarrow$ **క్ష**
  - `kRuShNa` $\rightarrow$ **కృష్ణ**
  - `namaskAram` $\rightarrow$ **నమస్కారం**

---

### 2. 🎛️ Interactive Key Map & Live Playground
Never guess how to spell a complex letter again.

<div align="center">
  <img src="product_hunt_assets/03_features_keymap_playground_16x9.jpg" alt="Key Map and Playground" width="900" />
</div>

- **Searchable 60+ Letter Matrix:** Fast search for vowels (*achulu*), consonants (*hallulu*), and conjuncts (*vatthulu*).
- **Interactive Typing Playground:** Practice sentences and verify key sequences right inside the UI.
- **Dynamic System Tray Status:** Displays **`తె`** in vibrant indigo when Telugu mode is active, and **`EN`** in slate when in English mode. Always visible beside your Windows clock.

---

### 3. 🌐 Universal Multi-App Compatibility & 100% Offline Privacy

<div align="center">
  <img src="product_hunt_assets/04_universal_apps_offline_16x9.jpg" alt="Universal Multi-App & Offline Privacy" width="900" />
</div>

- **Works Across Any Windows App:** Direct injection into WhatsApp, Word, Excel, Chrome, Firefox, VS Code, and Windows Terminal.
- **Zero Latency (0ms):** Pure in-memory state engine; doesn't slow down your typing speed.
- **100% Offline:** No internet connection required, zero cloud dependencies, and zero keystroke logging or analytics.

---

## ⌨️ Quick Typing Reference

| English Input | Telugu Output | Category |
| :--- | :--- | :--- |
| `n` | **న్** | Half-letter (Pollu) |
| `na` | **న** | Full Consonant |
| `nna` | **న్న** | Geminate (*Dvitva*) |
| `amma` | **అమ్మ** | Common Word |
| `ksha` / `Ksha` | **క్ష** | Conjunct (*Samyukta*) |
| `kRuShNa` | **కృష్ణ** | Special Vowel (*Ru-kaaram*) |
| `telugu` | **తెలుగు** | Common Word |
| `bhArat` | **భారత్** | Long Vowel + Halant End |
| `namaskAram` | **నమస్కారం** | Anusvara (*Sunna*) |
| `jnya` | **జ్ఞ** | Classical Conjunct |

> **Toggle Hotkey:** Press `Scroll Lock` (or customize to `Alt+T`, `Ctrl+Shift+T`, `F8` from Settings) to toggle between Telugu and English anytime.

---

## 🚀 Installation & Building

### 🪟 Windows

#### Option A: 1-Click Installer (Recommended)
Download the latest `Rachayitha_Setup.exe` from the [Releases](https://github.com/Ramaputhra/Rachayitha/releases) tab.
- Includes a 2-panel presentation setup wizard.
- Automatically creates Desktop and Start Menu shortcuts.
- Fully registered in Windows *Installed Apps* for 1-click clean uninstallation.

#### Option B: Build from Source on Windows
```powershell
# 1. Clone the repository
git clone https://github.com/Ramaputhra/Rachayitha.git
cd rachayitha/"rachayitha code files"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch directly
python main.py

# 4. Or compile the single setup installer (.exe)
python make_single_installer.py
```

---

### 🍎 macOS Setup & Build Guide

Rachayitha's core transliteration engine is completely cross-platform. On macOS, global keyboard interception uses standard macOS Accessibility APIs.

#### 1. Prerequisites
Ensure you have Python 3.10+ installed via [Homebrew](https://brew.sh):
```bash
brew install python python-tk
```

#### 2. Install Dependencies
```bash
git clone https://github.com/Ramaputhra/Rachayitha.git
cd rachayitha/"rachayitha code files"

# Install requirements
pip3 install PyQt6 pyinstaller
```

#### 3. ⚠️ Grant macOS Accessibility Permissions
macOS security requires explicit user permission for background apps that listen to global key events:
1. Open **System Settings** (or **System Preferences**).
2. Go to **Privacy & Security** $\rightarrow$ **Accessibility**.
3. Click the **`+`** icon and add your terminal app (**Terminal**, **iTerm2**) or the compiled **`Rachayitha.app`**.
4. Toggle the switch to **ON**.

#### 4. Run Directly on macOS
```bash
# Run with root or accessibility privileges
sudo python3 main.py
```

#### 5. Build Native macOS App Bundle (`.app`) & `.dmg`
To package Rachayitha as a standalone Mac application:

```bash
# Step A: Convert PNG logo to Apple ICNS format
mkdir -p Rachayitha.iconset
sips -z 16 16     rachayitha_logo.png --out Rachayitha.iconset/icon_16x16.png
sips -z 32 32     rachayitha_logo.png --out Rachayitha.iconset/icon_16x16@2x.png
sips -z 128 128   rachayitha_logo.png --out Rachayitha.iconset/icon_128x128.png
sips -z 256 256   rachayitha_logo.png --out Rachayitha.iconset/icon_256x256.png
sips -z 512 512   rachayitha_logo.png --out Rachayitha.iconset/icon_512x512.png
iconutil -c icns Rachayitha.iconset -o icon.icns

# Step B: Compile .app Bundle using PyInstaller
pyinstaller --noconfirm --onedir --windowed \
  --name "Rachayitha" \
  --icon="icon.icns" \
  --add-data "data:data" \
  main.py

# Step C: Package into a distributable Disk Image (.dmg)
hdiutil create -volname "Rachayitha" -srcfolder dist/Rachayitha.app -ov -format UDZO dist/Rachayitha.dmg
```
Output:
- 📦 **Native Mac App:** `dist/Rachayitha.app`
- 💿 **Installer Disk Image:** `dist/Rachayitha.dmg` (Drag to `/Applications`)

---

## 📁 Repository Structure

```
rachayitha/
├── product_hunt_assets/        # High-res marketing & showcase images
│   ├── 01_product_hunt_icon_square_1x1.jpg
│   ├── 02_hero_transliteration_16x9.jpg
│   ├── 03_features_keymap_playground_16x9.jpg
│   └── 04_universal_apps_offline_16x9.jpg
├── rachayitha code files/       # Production source code
│   ├── main.py                 # Core background listener & tray loop
│   ├── data/
│   │   ├── config.json         # Settings & hotkey preferences
│   │   └── telugu_rules.json   # Full Lekhini RTS rule matrices
│   ├── engine/
│   │   ├── buffer.py           # Real-time typing buffer manager
│   │   ├── paths.py            # %APPDATA% and resource resolver
│   │   └── transliterator.py   # Halant-first transliteration engine
│   ├── ui/
│   │   ├── settings.py         # Settings & searchable Key Map window
│   │   └── tray.py             # Dynamic 'తె'/'EN' taskbar tray icon
│   ├── installer_src/          # Setup wizard & uninstaller routines
│   ├── make_single_installer.py# Single installer compiler
│   └── icon.ico                # Multi-resolution application icon
└── README.md                   # Project documentation
```

---

## 🛡️ Privacy & Security

Rachayitha is built with strict privacy principles:
- **No Network Permissions:** The binary makes **zero** network requests.
- **Local Transliteration:** Transliteration logic runs locally in memory via `telugu_rules.json`.
- **Ephemeral Buffering:** Keystrokes are processed in a rolling temporary ring buffer and instantly cleared upon typing completion.

---

## 🤝 Contributing & License

Contributions, bug reports, and rule improvements are warmly welcomed!
- Report issues or suggest new key combinations in [Issues](https://github.com).
- Licensed under the [MIT License](LICENSE).
