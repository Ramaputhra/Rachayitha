import json
import os
import sys

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget,
    QTableWidget, QTableWidgetItem, QLineEdit, QPushButton,
    QCheckBox, QTextEdit, QHeaderView, QMessageBox, QFrame,
    QApplication, QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPixmap, QIcon, QColor, QTextCursor

from engine.paths import get_resource_path, load_config, save_config
from engine.casual_type import transliterate
from engine.buffer import TypingBuffer
from engine.learner import get_learner

class PlaygroundEditor(QTextEdit):
    suggestion_changed = pyqtSignal(object)        # Emits list of ghost suggestion texts or []
    hud_state_changed = pyqtSignal(str, str)      # Emits (title, detail) for HUD
    retro_triggered = pyqtSignal(str, str)        # Emits (old_word, new_word)
    language_toggled = pyqtSignal(bool)           # Emits True (Telugu) / False (English)
    casual_toggled = pyqtSignal(bool)             # Emits True (Casual) / False (Exact)

    def __init__(self, parent=None, casual_enabled=True):
        super().__init__(parent)
        self.is_telugu_on = True
        self.casual_enabled = casual_enabled
        self.buffer = TypingBuffer(casual_enabled=self.casual_enabled)

        font = QFont("Mandali", 15)
        if not font.exactMatch():
            font = QFont("Gautami", 15)
            if not font.exactMatch():
                font = QFont("Segoe UI", 15)
        self.setFont(font)
        self.setAcceptRichText(False)
        self.setPlaceholderText(
            "Start typing here in natural Tenglish (e.g. 'nuvvu ', 'namaskaram', 'akkada evaru leru')...\n\n"
            "• Keystrokes transform directly in-place (Natural Halant-First Pollu-First)\n"
            "• Press [Space] to commit words and trigger Next-Word Prediction\n"
            "• Press [Tab ⇥] to autocomplete predicted words\n"
            "• Click any suggestion pill to insert secondary/tertiary candidates\n"
            "• Press [Alt+T] to toggle between Telugu and English anytime"
        )
        self.setStyleSheet("""
            QTextEdit {
                background-color: #0b0f19;
                border: 2px solid #334155;
                border-radius: 8px;
                padding: 14px;
                color: #38bdf8;
                font-family: 'Mandali', 'Gautami', 'Segoe UI', Tahoma;
                font-size: 16px;
                line-height: 1.6;
                selection-background-color: #4338ca;
            }
            QTextEdit:focus {
                border: 2px solid #6366f1;
            }
        """)

    def set_mode(self, enabled: bool):
        self.is_telugu_on = enabled
        self.buffer.commit_sentence()
        self.suggestion_changed.emit([])
        self.language_toggled.emit(self.is_telugu_on)
        state_str = "తెలుగు (Telugu Mode Active)" if self.is_telugu_on else "English (EN Mode Active)"
        self.hud_state_changed.emit("Language Mode", state_str)

    def toggle_mode(self):
        self.set_mode(not self.is_telugu_on)

    def set_casual_mode(self, enabled: bool):
        self.casual_enabled = enabled
        self.buffer.set_casual_enabled(enabled)
        if not enabled:
            self.suggestion_changed.emit([])
        self.casual_toggled.emit(self.casual_enabled)
        engine_str = "Casual Type (58k Lexicon + LM Active)" if self.casual_enabled else "Exact RTS Engine (Deterministic)"
        self.hud_state_changed.emit("Engine Mode", engine_str)

    def toggle_casual_mode(self):
        self.set_casual_mode(not self.casual_enabled)

    def accept_suggestion(self, suggestion_text=None):
        if not self.casual_enabled:
            return
        target = suggestion_text or self.buffer.get_suggestion()
        if not target:
            return

        bs_count, to_insert = self.buffer.accept_suggestion(target)
        if to_insert:
            cursor = self.textCursor()
            cursor.beginEditBlock()
            for _ in range(bs_count):
                cursor.deletePreviousChar()
            cursor.insertText(to_insert)
            cursor.endEditBlock()
            self.setTextCursor(cursor)

            next_sugs = self.buffer.get_suggestions()
            self.suggestion_changed.emit(next_sugs)
            next_str = ", ".join(next_sugs) if next_sugs else "None"
            self.hud_state_changed.emit("Autocomplete Accepted", f"'{target}' → Next: {next_str}")
            self.setFocus()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.buffer.commit_sentence()
        self.suggestion_changed.emit([])

    def keyPressEvent(self, event):
        # 1. Hotkey Check: Alt+T toggles language live
        if (event.modifiers() & Qt.KeyboardModifier.AltModifier) and event.key() == Qt.Key.Key_T:
            self.toggle_mode()
            return

        # 2. English Mode: Let all keys pass through natively
        if not self.is_telugu_on:
            super().keyPressEvent(event)
            return

        # 3. Telugu Mode Handling:
        key = event.key()
        text = event.text()

        # Tab Key: Accept next-word prediction autocomplete
        if key == Qt.Key.Key_Tab:
            if self.casual_enabled and self.buffer.get_suggestions():
                self.accept_suggestion()
                return
            return

        # Space Key: Commit word and query next-word prediction
        if key == Qt.Key.Key_Space:
            self.buffer.commit_word()
            cursor = self.textCursor()
            cursor.insertText(" ")
            if self.casual_enabled:
                sugs = self.buffer.get_suggestions()
                self.suggestion_changed.emit(sugs)
                self.hud_state_changed.emit("Word Committed", f"Context: '{self.buffer.prev_word_telugu or ''}'")
            else:
                self.suggestion_changed.emit([])
            return

        # Sentence Delimiters: Enter, punctuation
        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.buffer.commit_sentence()
            cursor = self.textCursor()
            cursor.insertText("\n")
            self.suggestion_changed.emit([])
            self.hud_state_changed.emit("Sentence End", "Enter")
            return

        if text in ['.', '?', '!', ':', ';', ',']:
            self.buffer.commit_sentence()
            cursor = self.textCursor()
            cursor.insertText(text)
            self.suggestion_changed.emit([])
            self.hud_state_changed.emit("Punctuation", f"'{text}'")
            return

        # Escape Key: Clear suggestion
        if key == Qt.Key.Key_Escape:
            self.buffer.clear_suggestion()
            self.suggestion_changed.emit([])
            return

        # Backspace Key: In-place undo
        if key == Qt.Key.Key_Backspace:
            if self.buffer.is_active():
                backspaces_needed, new_out, _ = self.buffer.backspace()
                cursor = self.textCursor()
                cursor.beginEditBlock()
                for _ in range(backspaces_needed):
                    cursor.deletePreviousChar()
                if new_out:
                    cursor.insertText(new_out)
                cursor.endEditBlock()
                self.setTextCursor(cursor)
                self.hud_state_changed.emit("Backspace", f"Stem: '{self.buffer.get_eng()}' → '{new_out}'")
                if self.casual_enabled:
                    self.suggestion_changed.emit(self.buffer.get_suggestions())
                else:
                    self.suggestion_changed.emit([])
                return
            else:
                self.buffer.notify_external_backspace()
                self.buffer.clear_suggestion()
                self.suggestion_changed.emit([])
                super().keyPressEvent(event)
                return

        # Letter / Phonetic Character Input
        if len(text) == 1 and (text.isalpha() or text in ['~', '_']):
            char = text
            old_len, new_telugu, retro_patch = self.buffer.add(char)
            cursor = self.textCursor()
            cursor.beginEditBlock()
            if retro_patch:
                retro_bs, retro_text = retro_patch
                for _ in range(retro_bs):
                    cursor.deletePreviousChar()
                cursor.insertText(retro_text)
                self.retro_triggered.emit(self.buffer.prev_word_telugu or "", retro_text)
                self.hud_state_changed.emit("✨ Retroactive Correction", retro_text)
            else:
                for _ in range(old_len):
                    cursor.deletePreviousChar()
                cursor.insertText(new_telugu)
                self.hud_state_changed.emit("Syllable Assembled", f"'{self.buffer.get_eng()}' → '{new_telugu}'")
            cursor.endEditBlock()
            self.setTextCursor(cursor)

            if self.casual_enabled:
                self.suggestion_changed.emit(self.buffer.get_suggestions())
            else:
                self.suggestion_changed.emit([])
            return

        # Allow standard shortcuts: Ctrl+C, Ctrl+V, Ctrl+A, Ctrl+Z
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            super().keyPressEvent(event)
            if key in (Qt.Key.Key_V, Qt.Key.Key_Z):
                self.buffer.commit_sentence()
                self.suggestion_changed.emit([])
            return

        # Pass through any other key (arrows, etc.)
        self.suggestion_changed.emit([])
        super().keyPressEvent(event)

    def simulate_text(self, text: str):
        self.clear()
        self.buffer.commit_sentence()
        self.set_mode(True)
        for ch in text:
            if ch == ' ':
                self.buffer.commit_word()
                cursor = self.textCursor()
                cursor.insertText(" ")
            elif ch in ['.', ',', '?', '!', ':', ';']:
                self.buffer.commit_sentence()
                cursor = self.textCursor()
                cursor.insertText(ch)
            elif ch == '\n':
                self.buffer.commit_sentence()
                cursor = self.textCursor()
                cursor.insertText("\n")
            else:
                old_len, new_telugu, retro_patch = self.buffer.add(ch)
                cursor = self.textCursor()
                cursor.beginEditBlock()
                if retro_patch:
                    retro_bs, retro_text = retro_patch
                    for _ in range(retro_bs):
                        cursor.deletePreviousChar()
                    cursor.insertText(retro_text)
                    self.retro_triggered.emit(self.buffer.prev_word_telugu or "", retro_text)
                else:
                    for _ in range(old_len):
                        cursor.deletePreviousChar()
                    cursor.insertText(new_telugu)
                cursor.endEditBlock()
                self.setTextCursor(cursor)

        if self.casual_enabled and self.buffer.get_suggestions():
            self.suggestion_changed.emit(self.buffer.get_suggestions())
        else:
            self.suggestion_changed.emit([])
        self.hud_state_changed.emit("Simulation Complete", "100% In-Memory Accuracy")
        self.setFocus()

class SettingsWindow(QWidget):
    def __init__(self, on_toggle_callback=None, on_hotkey_changed_callback=None, on_casual_type_changed_callback=None):
        super().__init__()
        self.on_toggle_callback = on_toggle_callback
        self.on_hotkey_changed_callback = on_hotkey_changed_callback
        self.on_casual_type_changed_callback = on_casual_type_changed_callback
        self.setWindowTitle("రచయిత - Telugu Phonetic Transliteration & Key Map")
        self.setGeometry(220, 150, 840, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                color: #f8fafc;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 13px;
            }
            QTabWidget::pane {
                border: 1px solid #334155;
                background-color: #1e293b;
                border-radius: 8px;
            }
            QTabBar::tab {
                background-color: #0f172a;
                color: #94a3b8;
                padding: 11px 22px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                margin-right: 4px;
                font-weight: 600;
            }
            QTabBar::tab:selected {
                background-color: #1e293b;
                color: #6366f1;
                border-bottom: 3px solid #6366f1;
            }
            QLineEdit, QTextEdit {
                background-color: #0b0f19;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 8px 12px;
                color: #ffffff;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #6366f1;
            }
            QPushButton {
                background-color: #6366f1;
                color: white;
                font-weight: 600;
                padding: 8px 18px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #4f46e5;
            }
            QTableWidget {
                background-color: #0b0f19;
                border: 1px solid #334155;
                gridline-color: #1e293b;
                border-radius: 6px;
                selection-background-color: #312e81;
            }
            QHeaderView::section {
                background-color: #1e293b;
                color: #94a3b8;
                font-weight: 600;
                padding: 8px;
                border: 1px solid #334155;
            }
        """)

        self.config = load_config()
        self.learner = get_learner()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Header Title
        title_layout = QHBoxLayout()

        logo_path = get_resource_path("rachayitha_logo.png")
        if not os.path.exists(logo_path):
            logo_path = get_resource_path("icon.png")

        ico_path = get_resource_path("icon.ico")
        if os.path.exists(ico_path):
            self.setWindowIcon(QIcon(ico_path))
        elif os.path.exists(logo_path):
            self.setWindowIcon(QIcon(logo_path))

        logo_label = QLabel()
        if os.path.exists(logo_path):
            pix = QPixmap(logo_path).scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(pix)
        else:
            logo_label.setText("ర")
            logo_label.setStyleSheet("""
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6366f1, stop:1 #a855f7);
                color: white;
                font-size: 26px;
                font-weight: bold;
                padding: 4px 14px;
                border-radius: 8px;
                font-family: 'Mandali', 'Gautami', 'Segoe UI';
            """)
        title_layout.addWidget(logo_label)

        title_info = QVBoxLayout()
        title_text = QLabel("రచయిత (Rachayitha)")
        title_text.setStyleSheet("font-size: 20px; font-weight: 700; color: #ffffff;")
        sub_text = QLabel("System-wide Telugu Phonetic Typing • Created by Ramaputhra")
        sub_text.setStyleSheet("color: #94a3b8; font-size: 12px;")
        title_info.addWidget(title_text)
        title_info.addWidget(sub_text)
        title_layout.addLayout(title_info)
        title_layout.addStretch()

        main_layout.addLayout(title_layout)

        # Tab Widget
        tabs = QTabWidget()

        # Tab 1: Key Map Table (Prominent first tab as requested)
        tabs.addTab(self.create_keymap_tab(), "Key Map Table (అక్షరమాల)")

        # Tab 2: Settings & Hotkeys
        tabs.addTab(self.create_settings_tab(), "Settings & Hotkey (అభిరుచులు)")

        # Tab 3: Live Playground
        tabs.addTab(self.create_playground_tab(), "Live Playground (అభ్యాసం)")

        # Tab 4: Self-Learning & Vocabulary Profile
        tabs.addTab(self.create_learning_tab(), "Self-Learning (స్వయం అభ్యాసం)")

        # Tab 5: About
        tabs.addTab(self.create_about_tab(), "About (వివరాలు)")

        main_layout.addWidget(tabs)
        self.setLayout(main_layout)

    def create_keymap_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Search & Filter Row
        top_row = QHBoxLayout()
        search_lbl = QLabel("Search:")
        search_lbl.setStyleSheet("font-weight: 600; color: #cbd5e1;")
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Type Telugu letter or English key (e.g. 'k', 'aa', 'క్ష', 'M', 'సున్నా')...")
        self.search_box.textChanged.connect(self.filter_keymap)
        top_row.addWidget(search_lbl)
        top_row.addWidget(self.search_box)
        layout.addLayout(top_row)

        # Category Filter Buttons
        cat_row = QHBoxLayout()
        self.current_filter_category = "All"
        categories = ["All", "Vowels (అచ్చులు)", "Consonants (హల్లులు)", "Guninthalu (గుణింతాలు)", "Special (ప్రత్యేకం)"]
        self.cat_buttons = []
        for cat in categories:
            btn = QPushButton(cat)
            btn.setStyleSheet("background-color: #1e293b; color: #94a3b8; font-size: 11px; padding: 5px 12px;")
            if cat == "All":
                btn.setStyleSheet("background-color: #6366f1; color: white; font-size: 11px; padding: 5px 12px; font-weight: bold;")
            btn.clicked.connect(lambda _, c=cat: self.on_category_click(c))
            cat_row.addWidget(btn)
            self.cat_buttons.append((btn, cat))
        cat_row.addStretch()
        layout.addLayout(cat_row)

        # Table: 3 columns
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Telugu Letter (తెలుగు)", "English Type Key", "Example / Pronunciation"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.load_rules_into_table()
        layout.addWidget(self.table)

        tab.setLayout(layout)
        return tab

    def on_category_click(self, category):
        self.current_filter_category = category
        for btn, cat in self.cat_buttons:
            if cat == category:
                btn.setStyleSheet("background-color: #6366f1; color: white; font-size: 11px; padding: 5px 12px; font-weight: bold;")
            else:
                btn.setStyleSheet("background-color: #1e293b; color: #94a3b8; font-size: 11px; padding: 5px 12px;")
        self.filter_keymap(self.search_box.text())

    def load_rules_into_table(self):
        rules_path = get_resource_path(os.path.join('data', 'telugu_rules.json'))
        try:
            with open(rules_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            data = {}

        self.all_rows = []

        # Vowels
        for k, v in data.get('vowels', {}).items():
            self.all_rows.append((v, k, f"{k} -> {v}", "Vowels (అచ్చులు)"))

        # Consonants
        for k, v in data.get('consonants', {}).items():
            self.all_rows.append((v, k, f"{k}a -> {v}", "Consonants (హల్లులు)"))

        # Modifiers
        for k, v in data.get('modifiers', {}).items():
            if v:
                self.all_rows.append((v, k, f"k{k} -> క{v}", "Guninthalu (గుణింతాలు)"))

        # Special
        for k, v in data.get('special', {}).items():
            desc = "సున్నా (Anusvara)" if k == "M" else ("విసర్గ (Visarga)" if k == "H" else ("పొల్లు (Virama)" if k == "~" else "ZWNJ"))
            self.all_rows.append((v, k, f"{k} -> {v} ({desc})", "Special (ప్రత్యేకం)"))

        self.populate_table(self.all_rows)

    def populate_table(self, rows):
        self.table.setRowCount(len(rows))
        for i, (tel, eng, ex, cat) in enumerate(rows):
            item_tel = QTableWidgetItem(tel)
            item_tel.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            font = item_tel.font()
            font.setPointSize(15)
            font.setBold(True)
            item_tel.setFont(font)

            item_eng = QTableWidgetItem(eng)
            item_eng.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            eng_font = item_eng.font()
            eng_font.setFamily("Consolas")
            eng_font.setPointSize(12)
            item_eng.setFont(eng_font)
            item_eng.setForeground(Qt.GlobalColor.cyan)

            item_ex = QTableWidgetItem(ex)
            self.table.setItem(i, 0, item_tel)
            self.table.setItem(i, 1, item_eng)
            self.table.setItem(i, 2, item_ex)

    def filter_keymap(self, text):
        query = text.lower().strip()

        filtered = []
        for row in self.all_rows:
            tel, eng, ex, cat = row
            # Category match
            if self.current_filter_category != "All" and cat != self.current_filter_category:
                continue

            # Text query match
            if query:
                if (query not in tel.lower() and
                    query not in eng.lower() and
                    query not in ex.lower()):
                    continue

            filtered.append(row)

        self.populate_table(filtered)

    def create_settings_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Hotkey Section
        hk_box = QFrame()
        hk_box.setStyleSheet("background-color: #0b0f19; border: 1px solid #334155; border-radius: 8px; padding: 16px;")
        hk_layout = QVBoxLayout(hk_box)

        hk_title = QLabel("Keyboard Hotkey Configuration")
        hk_title.setStyleSheet("font-size: 15px; font-weight: bold; color: #6366f1;")
        hk_desc = QLabel("Set your custom global hotkey to seamlessly toggle Telugu typing in ANY application:")
        hk_desc.setStyleSheet("color: #94a3b8; font-size: 12px; margin-bottom: 8px;")
        hk_layout.addWidget(hk_title)
        hk_layout.addWidget(hk_desc)

        input_row = QHBoxLayout()
        input_row.addWidget(QLabel("Active Hotkey:"))
        self.hotkey_input = QLineEdit(self.config.get("hotkeys", {}).get("telugu_toggle", "alt+t"))
        self.hotkey_input.setFixedWidth(160)
        self.hotkey_input.setStyleSheet("font-family: Consolas; font-size: 14px; font-weight: bold; text-align: center; color: #38bdf8;")
        input_row.addWidget(self.hotkey_input)
        input_row.addStretch()
        hk_layout.addLayout(input_row)

        # Quick preset buttons
        presets_row = QHBoxLayout()
        presets_row.addWidget(QLabel("Presets:"))
        for preset in ["alt+t", "ctrl+shift+t", "alt+shift+t", "f8", "caps lock"]:
            pbtn = QPushButton(preset)
            pbtn.setStyleSheet("background-color: #1e293b; color: #94a3b8; font-size: 11px; padding: 4px 10px;")
            pbtn.clicked.connect(lambda _, p=preset: self.hotkey_input.setText(p))
            presets_row.addWidget(pbtn)
        presets_row.addStretch()
        hk_layout.addLayout(presets_row)

        layout.addWidget(hk_box)
        layout.addSpacing(12)

        # General Preferences Box
        pref_box = QFrame()
        pref_box.setStyleSheet("background-color: #0b0f19; border: 1px solid #334155; border-radius: 8px; padding: 16px;")
        pref_layout = QVBoxLayout(pref_box)

        pref_title = QLabel("System Preferences")
        pref_title.setStyleSheet("font-size: 15px; font-weight: bold; color: #6366f1;")
        pref_layout.addWidget(pref_title)

        self.autostart_chk = QCheckBox("Automatically launch Rachayitha on Windows startup (sits in System Tray)")
        self.autostart_chk.setChecked(self.config.get("auto_start", True))
        pref_layout.addWidget(self.autostart_chk)

        self.notify_chk = QCheckBox("Show toast notification when toggling language")
        self.notify_chk.setChecked(self.config.get("show_notifications", True))
        pref_layout.addWidget(self.notify_chk)

        self.casual_chk = QCheckBox("Casual Type (Colloquial & phonetic dictionary with 58k+ mappings)")
        self.casual_chk.setChecked(self.config.get("casual_type", True))
        self.casual_chk.setStyleSheet("color: #38bdf8; font-weight: 600;")
        pref_layout.addWidget(self.casual_chk)

        layout.addWidget(pref_box)
        layout.addSpacing(16)

        # Save Button
        save_btn = QPushButton("Save & Apply Settings")
        save_btn.setStyleSheet("background-color: #22c55e; color: white; font-weight: bold; font-size: 14px; padding: 10px 24px;")
        save_btn.clicked.connect(self.save_preferences)
        layout.addWidget(save_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        layout.addStretch()
        tab.setLayout(layout)
        return tab

    def save_preferences(self):
        new_hotkey = self.hotkey_input.text().strip().lower()
        if not new_hotkey:
            QMessageBox.warning(self, "Invalid Hotkey", "Hotkey cannot be empty!")
            return

        self.config["hotkeys"]["telugu_toggle"] = new_hotkey
        self.config["auto_start"] = self.autostart_chk.isChecked()
        self.config["show_notifications"] = self.notify_chk.isChecked()
        casual_enabled = self.casual_chk.isChecked()
        self.config["casual_type"] = casual_enabled

        # Update Windows Registry for auto-start
        self.update_windows_autostart(self.autostart_chk.isChecked())

        if save_config(self.config):
            # Notify live running hook to update hotkey immediately
            if self.on_hotkey_changed_callback:
                self.on_hotkey_changed_callback(new_hotkey)

            # Notify casual type toggle
            if self.on_casual_type_changed_callback:
                self.on_casual_type_changed_callback(casual_enabled)

            # Keep live playground editor synchronized
            if hasattr(self, 'playground_editor'):
                self.playground_editor.set_casual_mode(casual_enabled)

            QMessageBox.information(
                self, "Settings Saved",
                f"Preferences saved successfully!\n\nYour new toggle hotkey [{new_hotkey.upper()}] is active."
            )

    def update_windows_autostart(self, enable: bool):
        if sys.platform != 'win32':
            return
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            app_path = sys.executable if getattr(sys, 'frozen', False) else f'"{sys.executable}" "{os.path.abspath(sys.argv[0])}"'
            if enable:
                winreg.SetValueEx(key, "Rachayitha", 0, winreg.REG_SZ, app_path)
            else:
                try:
                    winreg.DeleteValue(key, "Rachayitha")
                except FileNotFoundError:
                    pass
            winreg.CloseKey(key)
        except Exception as e:
            print(f"Autostart registry update error: {e}")

    def create_playground_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(10)

        # 1. Top Controls Bar: Language Mode Toggle, Casual Mode Toggle, Action Buttons
        top_bar = QHBoxLayout()

        # Language Toggle Button (Alt+T)
        self.play_lang_btn = QPushButton("🟢 తెలుగు (Telugu Mode Active) [Alt+T]")
        self.play_lang_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f46e5, stop:1 #7c3aed);
                color: #ffffff;
                font-weight: 700;
                font-size: 13px;
                padding: 8px 16px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4338ca, stop:1 #6d28d9);
            }
        """)
        self.play_lang_btn.clicked.connect(self.on_playground_lang_click)
        top_bar.addWidget(self.play_lang_btn)

        # Casual Type Toggle Button
        casual_active = self.config.get("casual_type", True)
        self.play_casual_btn = QPushButton("⚡ Casual Mode: ON (58k Lexicon + LM)")
        self.play_casual_btn.setStyleSheet("""
            QPushButton {
                background-color: #0284c7;
                color: #ffffff;
                font-weight: 600;
                font-size: 12px;
                padding: 8px 14px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #0369a1;
            }
        """)
        self.play_casual_btn.clicked.connect(self.on_playground_casual_click)
        top_bar.addWidget(self.play_casual_btn)

        top_bar.addStretch()

        # Copy & Clear Buttons
        copy_btn = QPushButton("📋 Copy Telugu")
        copy_btn.setStyleSheet("background-color: #1e293b; color: #94a3b8; font-size: 12px; padding: 7px 14px; border-radius: 6px;")
        copy_btn.clicked.connect(self.copy_playground_text)
        top_bar.addWidget(copy_btn)

        clear_btn = QPushButton("🧹 Clear")
        clear_btn.setStyleSheet("background-color: #1e293b; color: #94a3b8; font-size: 12px; padding: 7px 14px; border-radius: 6px;")
        clear_btn.clicked.connect(self.clear_playground_text)
        top_bar.addWidget(clear_btn)

        layout.addLayout(top_bar)

        # 2. Main Interactive In-Place Editor (Functions exactly as app works!)
        self.playground_editor = PlaygroundEditor(casual_enabled=casual_active)
        self.playground_editor.suggestion_changed.connect(self.on_playground_suggestion_changed)
        self.playground_editor.hud_state_changed.connect(self.on_playground_hud_changed)
        self.playground_editor.retro_triggered.connect(self.on_playground_retro_triggered)
        self.playground_editor.language_toggled.connect(self.update_playground_lang_ui)
        self.playground_editor.casual_toggled.connect(self.update_playground_casual_ui)
        layout.addWidget(self.playground_editor, 1)

        # 3. Next-Word Prediction Ghost Bar (Mirrors the floating desktop suggestion overlay!)
        self.ghost_bar = QFrame()
        self.ghost_bar.setStyleSheet("""
            QFrame {
                background-color: #111827;
                border: 1px solid #1e293b;
                border-radius: 8px;
                padding: 6px 12px;
            }
        """)
        ghost_layout = QHBoxLayout(self.ghost_bar)
        ghost_layout.setContentsMargins(8, 4, 8, 4)

        self.ghost_icon = QLabel("💡")
        self.ghost_icon.setStyleSheet("font-size: 16px;")
        ghost_layout.addWidget(self.ghost_icon)

        self.ghost_label = QLabel("Type in natural Tenglish... press [Space] to see Next-Word Predictions")
        self.ghost_label.setStyleSheet("color: #94a3b8; font-size: 12px;")
        ghost_layout.addWidget(self.ghost_label)

        # Clickable Autocomplete Pills (Top 3)
        self.ghost_pills = []
        self._current_playground_suggestions = []
        for i in range(3):
            btn = QPushButton("")
            btn.setVisible(False)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            if i == 0:
                btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6366f1, stop:1 #ec4899);
                        color: #ffffff;
                        font-weight: 700;
                        font-size: 13px;
                        padding: 4px 14px;
                        border-radius: 12px;
                        border: none;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f46e5, stop:1 #db2777);
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #334155;
                        color: #f1f5f9;
                        font-weight: 600;
                        font-size: 12px;
                        padding: 4px 12px;
                        border-radius: 10px;
                        border: 1px solid #475569;
                    }
                    QPushButton:hover {
                        background-color: #475569;
                        color: #ffffff;
                    }
                """)
            btn.clicked.connect(lambda checked, idx=i: self._on_playground_pill_clicked(idx))
            ghost_layout.addWidget(btn)
            self.ghost_pills.append(btn)

        ghost_layout.addStretch()

        self.ghost_hint = QLabel("[Tab ⇥] Autocomplete")
        self.ghost_hint.setStyleSheet("color: #64748b; font-size: 11px; font-weight: 600;")
        ghost_layout.addWidget(self.ghost_hint)

        layout.addWidget(self.ghost_bar)

        # 4. Real-time Engine Diagnostic HUD (Shows active syllable, context & retroactive events)
        hud_bar = QHBoxLayout()

        self.hud_syllable = QLabel("Syllable: Idle")
        self.hud_syllable.setStyleSheet("background-color: #0b0f19; border: 1px solid #1e293b; border-radius: 4px; padding: 4px 10px; font-size: 11px; color: #94a3b8;")
        hud_bar.addWidget(self.hud_syllable)

        self.hud_retro = QLabel("Retroactive: Ready")
        self.hud_retro.setStyleSheet("background-color: #0b0f19; border: 1px solid #1e293b; border-radius: 4px; padding: 4px 10px; font-size: 11px; color: #94a3b8;")
        hud_bar.addWidget(self.hud_retro)

        hud_bar.addStretch()

        latency_lbl = QLabel("⚡ 0ms Latency • 100% Local In-Memory Engine")
        latency_lbl.setStyleSheet("color: #10b981; font-size: 11px; font-weight: 600;")
        hud_bar.addWidget(latency_lbl)

        layout.addLayout(hud_bar)

        # 5. Quick Test & Benchmark Simulations
        chips_layout = QHBoxLayout()
        test_lbl = QLabel("Quick Benchmarks:")
        test_lbl.setStyleSheet("color: #cbd5e1; font-weight: 600; font-size: 12px;")
        chips_layout.addWidget(test_lbl)

        benchmarks = [
            ("Conversational", "nuvvu akkade undu vastunna"),
            ("Polarity Disambiguation", "akkada evaru leru"),
            ("Collocations", "sarele inko sari vellanu"),
            ("Full Sentence Benchmark", "nuvvennanna cheppu, nuvvu naatho matlade samayamlo naaku vere phone vachindi, lekapothe nenenduku bayataki veltanu, sarele inko sari vellanu, enduku anta kopanga unnavo cheppu, lekapothe nenu matladanu."),
        ]

        for label, text in benchmarks:
            display_title = f"▶ {label}"
            btn = QPushButton(display_title)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1e293b;
                    color: #94a3b8;
                    padding: 5px 12px;
                    font-size: 11px;
                    border: 1px solid #334155;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #334155;
                    color: #ffffff;
                    border-color: #6366f1;
                }
            """)
            btn.clicked.connect(lambda _, t=text: self.playground_editor.simulate_text(t))
            chips_layout.addWidget(btn)

        chips_layout.addStretch()
        layout.addLayout(chips_layout)

        tab.setLayout(layout)
        return tab

    def on_playground_lang_click(self):
        self.playground_editor.toggle_mode()

    def update_playground_lang_ui(self, is_telugu: bool):
        if is_telugu:
            self.play_lang_btn.setText("🟢 తెలుగు (Telugu Mode Active) [Alt+T]")
            self.play_lang_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f46e5, stop:1 #7c3aed);
                    color: #ffffff;
                    font-weight: 700;
                    font-size: 13px;
                    padding: 8px 16px;
                    border-radius: 6px;
                    border: none;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4338ca, stop:1 #6d28d9);
                }
            """)
        else:
            self.play_lang_btn.setText("⚪ English (EN Mode Active) [Alt+T]")
            self.play_lang_btn.setStyleSheet("""
                QPushButton {
                    background-color: #334155;
                    color: #cbd5e1;
                    font-weight: 600;
                    font-size: 13px;
                    padding: 8px 16px;
                    border-radius: 6px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #475569;
                }
            """)

    def on_playground_casual_click(self):
        self.playground_editor.toggle_casual_mode()

    def update_playground_casual_ui(self, is_casual: bool):
        if is_casual:
            self.play_casual_btn.setText("⚡ Casual Mode: ON (58k Lexicon + LM)")
            self.play_casual_btn.setStyleSheet("""
                QPushButton {
                    background-color: #0284c7;
                    color: #ffffff;
                    font-weight: 600;
                    font-size: 12px;
                    padding: 8px 14px;
                    border-radius: 6px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #0369a1;
                }
            """)
        else:
            self.play_casual_btn.setText("🎯 Exact RTS Mode (Deterministic)")
            self.play_casual_btn.setStyleSheet("""
                QPushButton {
                    background-color: #475569;
                    color: #e2e8f0;
                    font-weight: 600;
                    font-size: 12px;
                    padding: 8px 14px;
                    border-radius: 6px;
                    border: none;
                }
                QPushButton:hover {
                    background-color: #64748b;
                }
            """)

    def _on_playground_pill_clicked(self, idx: int):
        if hasattr(self, '_current_playground_suggestions') and 0 <= idx < len(self._current_playground_suggestions):
            word = self._current_playground_suggestions[idx]
            self.playground_editor.accept_suggestion(word)

    def on_playground_suggestion_changed(self, suggestions):
        if isinstance(suggestions, str):
            cands = [suggestions] if suggestions.strip() else []
        elif isinstance(suggestions, (list, tuple)):
            cands = [s for s in suggestions if s and s.strip()]
        else:
            cands = []

        self._current_playground_suggestions = cands[:3]

        if self._current_playground_suggestions:
            self.ghost_icon.setText("🔮")
            self.ghost_label.setText("Next Word Autocomplete:")
            for i in range(3):
                if i < len(self._current_playground_suggestions):
                    w = self._current_playground_suggestions[i]
                    if i == 0:
                        self.ghost_pills[i].setText(f"1. {w}  [Tab ⇥]")
                    else:
                        self.ghost_pills[i].setText(f"{i + 1}. {w}")
                    self.ghost_pills[i].setVisible(True)
                else:
                    self.ghost_pills[i].setVisible(False)

            self.ghost_bar.setStyleSheet("""
                QFrame {
                    background-color: #1e1b4b;
                    border: 1px solid #6366f1;
                    border-radius: 8px;
                    padding: 6px 12px;
                }
            """)
        else:
            self.ghost_icon.setText("💡")
            self.ghost_label.setText("Type in natural Tenglish... press [Space] to trigger Next-Word Prediction")
            for pill in self.ghost_pills:
                pill.setVisible(False)
            self.ghost_bar.setStyleSheet("""
                QFrame {
                    background-color: #111827;
                    border: 1px solid #1e293b;
                    border-radius: 8px;
                    padding: 6px 12px;
                }
            """)

    def on_playground_hud_changed(self, title: str, detail: str):
        self.hud_syllable.setText(f"{title}: {detail}")

    def on_playground_retro_triggered(self, old_word: str, new_word: str):
        self.hud_retro.setText(f"✨ Retroactive: '{new_word}'")
        self.hud_retro.setStyleSheet("background-color: #064e3b; border: 1px solid #10b981; border-radius: 4px; padding: 4px 10px; font-size: 11px; color: #a7f3d0; font-weight: bold;")
        QTimer.singleShot(3000, lambda: self.hud_retro.setStyleSheet("background-color: #0b0f19; border: 1px solid #1e293b; border-radius: 4px; padding: 4px 10px; font-size: 11px; color: #94a3b8;"))

    def copy_playground_text(self):
        text = self.playground_editor.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            self.on_playground_hud_changed("Clipboard", "✓ Telugu text copied to clipboard!")

    def clear_playground_text(self):
        self.playground_editor.clear()
        self.playground_editor.buffer.commit_sentence()
        self.on_playground_suggestion_changed("")
        self.on_playground_hud_changed("Status", "Cleared")

    def create_learning_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Stats Cards Row
        stats_box = QFrame()
        stats_box.setStyleSheet("background-color: #0b0f19; border: 1px solid #334155; border-radius: 8px; padding: 12px;")
        stats_layout = QHBoxLayout(stats_box)

        self.stat_overrides_lbl = QLabel()
        self.stat_overrides_lbl.setStyleSheet("color: #38bdf8; font-weight: bold; font-size: 13px;")
        self.stat_boosts_lbl = QLabel()
        self.stat_boosts_lbl.setStyleSheet("color: #a78bfa; font-weight: bold; font-size: 13px;")
        self.stat_bigrams_lbl = QLabel()
        self.stat_bigrams_lbl.setStyleSheet("color: #34d399; font-weight: bold; font-size: 13px;")
        self.stat_status_lbl = QLabel("🛡️ 100% Offline Profile")
        self.stat_status_lbl.setStyleSheet("color: #94a3b8; font-size: 12px;")

        stats_layout.addWidget(self.stat_overrides_lbl)
        stats_layout.addWidget(self.stat_boosts_lbl)
        stats_layout.addWidget(self.stat_bigrams_lbl)
        stats_layout.addStretch()
        stats_layout.addWidget(self.stat_status_lbl)
        layout.addWidget(stats_box)

        # Quick Add Custom Word Box
        add_box = QFrame()
        add_box.setStyleSheet("background-color: #0b0f19; border: 1px solid #334155; border-radius: 8px; padding: 12px;")
        add_layout = QHBoxLayout(add_box)
        add_layout.setContentsMargins(10, 8, 10, 8)

        add_title = QLabel("Add Custom Mapping:")
        add_title.setStyleSheet("font-weight: bold; color: #f8fafc;")
        add_layout.addWidget(add_title)

        self.add_eng_input = QLineEdit()
        self.add_eng_input.setPlaceholderText("English/Casual input (e.g. 'bava', 'hyd')...")
        self.add_eng_input.setStyleSheet("background-color: #1e293b; border: 1px solid #475569; border-radius: 4px; padding: 6px; color: #38bdf8;")
        add_layout.addWidget(self.add_eng_input)

        self.add_tel_input = QLineEdit()
        self.add_tel_input.setPlaceholderText("Telugu word (e.g. 'బావా', 'హైదరాబాద్')...")
        self.add_tel_input.setStyleSheet("background-color: #1e293b; border: 1px solid #475569; border-radius: 4px; padding: 6px; color: #34d399; font-family: 'Mandali', 'Gautami', 'Segoe UI'; font-size: 14px;")
        add_layout.addWidget(self.add_tel_input)

        add_btn = QPushButton("Save Word")
        add_btn.setStyleSheet("background-color: #6366f1; color: white; font-weight: bold; padding: 6px 14px; border-radius: 4px;")
        add_btn.clicked.connect(self.on_add_learned_word)
        add_layout.addWidget(add_btn)

        layout.addWidget(add_box)

        # Search Bar
        search_row = QHBoxLayout()
        search_lbl = QLabel("Search Learned:")
        search_lbl.setStyleSheet("font-weight: 600; color: #cbd5e1;")
        self.learned_search_box = QLineEdit()
        self.learned_search_box.setPlaceholderText("Filter learned words or English keys...")
        self.learned_search_box.setStyleSheet("background-color: #0b0f19; border: 1px solid #334155; border-radius: 6px; padding: 6px; color: #38bdf8;")
        self.learned_search_box.textChanged.connect(self.populate_learned_table)
        search_row.addWidget(search_lbl)
        search_row.addWidget(self.learned_search_box)
        layout.addLayout(search_row)

        # Table of Learned Overrides
        self.learned_table = QTableWidget(0, 5)
        self.learned_table.setHorizontalHeaderLabels([
            "English / Casual Input",
            "Learned Telugu Output",
            "Usage Count",
            "Learning Source",
            "Action"
        ])
        self.learned_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.learned_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.learned_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.learned_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.learned_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.learned_table.setColumnWidth(4, 90)
        layout.addWidget(self.learned_table)

        # Bottom Controls
        bottom_row = QHBoxLayout()
        self.learning_enabled_chk = QCheckBox("Enable Adaptive Self-Learning (learns when you backspace and retype)")
        self.learning_enabled_chk.setChecked(self.learner.is_enabled() if self.learner else True)
        self.learning_enabled_chk.setStyleSheet("color: #38bdf8; font-weight: bold;")
        self.learning_enabled_chk.toggled.connect(self.on_toggle_learning)
        bottom_row.addWidget(self.learning_enabled_chk)
        bottom_row.addStretch()

        export_btn = QPushButton("Export JSON...")
        export_btn.setStyleSheet("background-color: #1e293b; color: #cbd5e1; padding: 6px 12px; border-radius: 4px;")
        export_btn.clicked.connect(self.on_export_learning)
        bottom_row.addWidget(export_btn)

        import_btn = QPushButton("Import JSON...")
        import_btn.setStyleSheet("background-color: #1e293b; color: #cbd5e1; padding: 6px 12px; border-radius: 4px;")
        import_btn.clicked.connect(self.on_import_learning)
        bottom_row.addWidget(import_btn)

        clear_btn = QPushButton("Reset Profile")
        clear_btn.setStyleSheet("background-color: #7f1d1d; color: #fca5a5; font-weight: bold; padding: 6px 12px; border-radius: 4px;")
        clear_btn.clicked.connect(self.on_clear_learning)
        bottom_row.addWidget(clear_btn)

        layout.addLayout(bottom_row)
        tab.setLayout(layout)

        self.update_learning_stats()
        self.populate_learned_table()
        return tab

    def update_learning_stats(self):
        if not self.learner:
            return
        stats = self.learner.get_stats()
        self.stat_overrides_lbl.setText(f"📖 {stats['total_overrides']} Custom Words")
        self.stat_boosts_lbl.setText(f"⚖️ {stats['total_boosts']} Candidate Boosts")
        self.stat_bigrams_lbl.setText(f"🔗 {stats['total_bigrams']} Collocations")

    def populate_learned_table(self):
        if not self.learner:
            return
        query = self.learned_search_box.text().strip().lower() if hasattr(self, 'learned_search_box') else ""
        items = []
        for eng, data in self.learner.word_overrides.items():
            tel = data.get("tel", "") if isinstance(data, dict) else str(data)
            count = data.get("count", 1) if isinstance(data, dict) else 1
            source = data.get("source", "user") if isinstance(data, dict) else "user"
            if query and (query not in eng.lower() and query not in tel.lower()):
                continue
            items.append((eng, tel, count, source))

        items.sort(key=lambda x: x[2], reverse=True)
        self.learned_table.setRowCount(len(items))

        for row_idx, (eng, tel, count, source) in enumerate(items):
            item_eng = QTableWidgetItem(eng)
            item_eng.setForeground(QColor("#38bdf8"))
            item_eng.setFont(QFont("Consolas", 11, QFont.Weight.Bold))

            item_tel = QTableWidgetItem(tel)
            item_tel.setForeground(QColor("#34d399"))
            item_tel.setFont(QFont("Mandali", 13, QFont.Weight.Bold))

            item_count = QTableWidgetItem(f"{count}×")
            item_count.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_count.setForeground(QColor("#94a3b8"))

            src_label = "Backspace Retype" if source == "backspace_correction" else ("Pill Select" if source == "candidate_selection" else "Manual")
            item_src = QTableWidgetItem(src_label)
            item_src.setForeground(QColor("#a78bfa"))

            del_btn = QPushButton("Delete")
            del_btn.setStyleSheet("background-color: #334155; color: #f87171; border-radius: 3px; padding: 2px 8px; font-size: 11px;")
            del_btn.clicked.connect(lambda _, k=eng: self.on_delete_learned_word(k))

            self.learned_table.setItem(row_idx, 0, item_eng)
            self.learned_table.setItem(row_idx, 1, item_tel)
            self.learned_table.setItem(row_idx, 2, item_count)
            self.learned_table.setItem(row_idx, 3, item_src)
            self.learned_table.setCellWidget(row_idx, 4, del_btn)

    def on_add_learned_word(self):
        eng = self.add_eng_input.text().strip().lower()
        tel = self.add_tel_input.text().strip()
        if not eng or not tel:
            QMessageBox.warning(self, "Invalid Input", "Please provide both English key and Telugu word.")
            return
        if self.learner:
            self.learner.add_manual_override(eng, tel)
            self.add_eng_input.clear()
            self.add_tel_input.clear()
            self.update_learning_stats()
            self.populate_learned_table()

    def on_delete_learned_word(self, eng_key: str):
        if self.learner:
            self.learner.remove_override(eng_key)
            self.update_learning_stats()
            self.populate_learned_table()

    def on_toggle_learning(self, checked: bool):
        if self.learner:
            self.learner.set_enabled(checked)

    def on_export_learning(self):
        if not self.learner:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Export Learned Vocabulary", "rachayitha_learned.json", "JSON Files (*.json)")
        if path:
            if self.learner.export_profile(path):
                QMessageBox.information(self, "Export Success", f"Learned profile exported to:\n{path}")
            else:
                QMessageBox.critical(self, "Export Failed", "Could not export profile.")

    def on_import_learning(self):
        if not self.learner:
            return
        path, _ = QFileDialog.getOpenFileName(self, "Import Learned Vocabulary", "", "JSON Files (*.json)")
        if path:
            if self.learner.import_profile(path, merge=True):
                self.update_learning_stats()
                self.populate_learned_table()
                QMessageBox.information(self, "Import Success", "Learned profile successfully merged!")
            else:
                QMessageBox.critical(self, "Import Failed", "Could not import profile file.")

    def on_clear_learning(self):
        if not self.learner:
            return
        reply = QMessageBox.question(
            self,
            "Reset Profile?",
            "Are you sure you want to clear all learned words and corrections?\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.learner.clear_all()
            self.update_learning_stats()
            self.populate_learned_table()

    def showEvent(self, event):
        super().showEvent(event)
        if hasattr(self, 'update_learning_stats'):
            self.update_learning_stats()
        if hasattr(self, 'populate_learned_table'):
            self.populate_learned_table()

    def create_about_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        about_title = QLabel("రచయిత (Rachayitha) v2.0.0")
        about_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #6366f1;")
        layout.addWidget(about_title)

        about_text = QLabel(
            "Rachayitha enables seamless, system-wide phonetic typing in Telugu across ANY desktop "
            "application (Notepad, MS Word, Chrome, WhatsApp Desktop, Slack, VS Code, etc.).\n\n"
            "• 100% Offline & Private (Zero network telemetry)\n"
            "• Dynamic System Tray icon ('తె' / 'EN') showing active language\n"
            "• Live Hotkey Customization with Instant Re-registration\n"
            "• Complete Phonetic Telugu RTS rules matrix (60+ letters)\n"
            "• Automatic startup on Windows boot\n\n"
            "Created for the Telugu computing community with ❤️ by Ramaputhra."
        )
        about_text.setStyleSheet("color: #94a3b8; font-size: 13px; line-height: 1.6;")
        layout.addWidget(about_text)

        layout.addStretch()
        tab.setLayout(layout)
        return tab

    def closeEvent(self, event):
        event.ignore()
        self.hide()
