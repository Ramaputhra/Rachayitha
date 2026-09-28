# TeluguType - Product Requirements Document
Version 1.0 | Inspiration: PramukhIME + Lekhini

## 1. Vision
One-time install Windows app that lives in system tray. Hotkey toggles Telugu typing. User types in Tenglish and sees real-time Telugu transformation in ANY app.

## 2. Core Goals
- One EXE installer that installs all dependencies (offline after)
- Zero config startup: auto-start on boot, sits in tray
- Seamless language switch via customizable hotkey (default Alt+T)
- Real-time transliteration with buffer + backspace
- Lekhini RTS familiarity

## 3. Features

### 3.1 System Tray
- On install: icon appears immediately (like PramukhIME)
- Left click: English | Telugu - Tenglish, Settings, Exit
- Tooltip shows mode: TeluguType: Telugu ON

### 3.2 Typing Engine
- Global keyboard hook
- Buffer-based: holds "telu", renders "తెలు"
- Commit on space, enter, punctuation
- Backspace pops eng_buffer and re-renders
- Special: ksh->క్ష, M->ం, H->ః

### 3.3 Settings (PyQt6)
- Languages tab, Key Map tab (60+ letters searchable), Hotkeys tab
- Saves to %APPDATA%/TeluguType/config.json

### 3.4 Installer
- PyInstaller bundles Python + deps
- Inno Setup creates TeluguType_Setup.exe
- Startup shortcut

## 4. Tech: Python 3.11, pystray, PyQt6, keyboard, PyInstaller

## 5. Testing: Notepad, Word, Chrome, WhatsApp Desktop, fresh VM
