import json
import os
import sys

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget,
    QTableWidget, QTableWidgetItem, QLineEdit, QPushButton,
    QCheckBox, QTextEdit, QHeaderView, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QIcon, QColor

from engine.paths import get_resource_path, load_config, save_config
from engine.transliterator import transliterate

class SettingsWindow(QWidget):
    def __init__(self, on_toggle_callback=None, on_hotkey_changed_callback=None):
        super().__init__()
        self.on_toggle_callback = on_toggle_callback
        self.on_hotkey_changed_callback = on_hotkey_changed_callback
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
        sub_text = QLabel("System-wide Telugu Phonetic Typing • Lekhini RTS Compatible")
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

        # Tab 4: About
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

        # Update Windows Registry for auto-start
        self.update_windows_autostart(self.autostart_chk.isChecked())

        if save_config(self.config):
            # Notify live running hook to update hotkey immediately
            if self.on_hotkey_changed_callback:
                self.on_hotkey_changed_callback(new_hotkey)

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

        desc = QLabel("Type in phonetic English (Tenglish) below to test real-time Telugu transformation:")
        desc.setStyleSheet("color: #94a3b8; margin-bottom: 6px;")
        layout.addWidget(desc)

        grid_layout = QHBoxLayout()

        # Input Box
        in_col = QVBoxLayout()
        in_col.addWidget(QLabel("English Input (Tenglish):"))
        self.playground_input = QTextEdit()
        self.playground_input.setPlaceholderText("Type here... (e.g. namaskAram, meeru ela unnaru?)")
        self.playground_input.textChanged.connect(self.on_playground_text_changed)
        in_col.addWidget(self.playground_input)
        grid_layout.addLayout(in_col)

        # Output Box
        out_col = QVBoxLayout()
        out_col.addWidget(QLabel("తెలుగు (Telugu Output):"))
        self.playground_output = QTextEdit()
        self.playground_output.setReadOnly(True)
        self.playground_output.setStyleSheet("font-size: 18px; color: #38bdf8; font-family: 'Mandali', 'Gautami', 'Segoe UI';")
        out_col.addWidget(self.playground_output)
        grid_layout.addLayout(out_col)

        layout.addLayout(grid_layout)

        # Quick Try Buttons
        chips_layout = QHBoxLayout()
        chips_layout.addWidget(QLabel("Quick Try:"))
        for word in ["telugu", "amma", "namaskAram", "rachayitha", "kRuShNa", "bhAratadEsham"]:
            btn = QPushButton(word)
            btn.setStyleSheet("background-color: #1e293b; color: #94a3b8; padding: 4px 10px; font-size: 11px;")
            btn.clicked.connect(lambda _, w=word: self.playground_input.setPlainText(w))
            chips_layout.addWidget(btn)
        chips_layout.addStretch()
        layout.addLayout(chips_layout)

        tab.setLayout(layout)
        return tab

    def on_playground_text_changed(self):
        text = self.playground_input.toPlainText()
        self.playground_output.setPlainText(transliterate(text))

    def create_about_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        about_title = QLabel("రచయిత (Rachayitha) v1.0.0")
        about_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #6366f1;")
        layout.addWidget(about_title)

        about_text = QLabel(
            "Inspired by PramukhIME and Lekhini RTS.\n\n"
            "Rachayitha enables seamless, system-wide phonetic typing in Telugu across ANY desktop "
            "application (Notepad, MS Word, Chrome, WhatsApp Desktop, Slack, VS Code, etc.).\n\n"
            "• 100% Offline & Private (Zero network telemetry)\n"
            "• Dynamic System Tray icon ('తె' / 'EN') showing active language\n"
            "• Live Hotkey Customization with Instant Re-registration\n"
            "• Complete Lekhini RTS rules matrix (60+ letters)\n"
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
