import sys
import os
import shutil
import subprocess
import winreg
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QCheckBox, QProgressBar, QMessageBox,
    QFileDialog, QFrame, QStackedWidget
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPixmap, QIcon

APP_NAME = "Rachayitha"
DISPLAY_NAME = "రచయిత (Rachayitha)"
DEFAULT_INSTALL_DIR = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "Programs", APP_NAME)

def get_bundled_payload_path():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dist_path = os.path.join(base, "dist", "Rachayitha.exe")
        if os.path.exists(dist_path):
            return dist_path

    candidate = os.path.join(base, "Rachayitha.exe")
    if os.path.exists(candidate):
        return candidate
    return os.path.join(base, "dist", "Rachayitha.exe")

def get_bundled_logo_path():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logo_path = os.path.join(base, "rachayitha_logo.png")
    if os.path.exists(logo_path):
        return logo_path
    return os.path.join(base, "icon.png")

def create_windows_shortcut(target_exe, shortcut_path, working_dir, description):
    try:
        ps_cmd = (
            f"$ws = New-Object -ComObject WScript.Shell; "
            f"$s = $ws.CreateShortcut('{shortcut_path}'); "
            f"$s.TargetPath = '{target_exe}'; "
            f"$s.WorkingDirectory = '{working_dir}'; "
            f"$s.Description = '{description}'; "
            f"$s.Save();"
        )
        subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, creationflags=0x08000000)
    except Exception as e:
        print(f"Error creating shortcut {shortcut_path}: {e}")

def register_uninstaller(install_dir, exe_path):
    try:
        key_path = rf"Software\Microsoft\Windows\CurrentVersion\Uninstall\{APP_NAME}"
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
        winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, "Rachayitha (రచయిత) - Telugu Typing Tool")
        winreg.SetValueEx(key, "DisplayIcon", 0, winreg.REG_SZ, exe_path)
        winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, "2.0.0")
        winreg.SetValueEx(key, "Publisher", 0, winreg.REG_SZ, "Ramaputhra")
        winreg.SetValueEx(key, "InstallLocation", 0, winreg.REG_SZ, install_dir)

        # Create uninstaller batch command in install directory
        uninst_bat = os.path.join(install_dir, "uninstall.bat")
        with open(uninst_bat, "w") as f:
            f.write('@echo off\n')
            f.write('echo Uninstalling Rachayitha...\n')
            f.write('taskkill /F /IM Rachayitha.exe >nul 2>nul\n')
            f.write('del "%USERPROFILE%\\Desktop\\Rachayitha.lnk" >nul 2>nul\n')
            f.write('del "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Rachayitha.lnk" >nul 2>nul\n')
            f.write('del "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\Rachayitha.lnk" >nul 2>nul\n')
            f.write(f'reg delete "HKCU\\{key_path}" /f >nul 2>nul\n')
            f.write('timeout /t 1 >nul\n')
            f.write(f'start "" cmd /c "timeout /t 1 >nul & rd /s /q \\"{install_dir}\\""\n')

        winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ, f'"{uninst_bat}"')
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Error registering uninstaller: {e}")

class InstallWorker(QThread):
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str)

    def __init__(self, target_dir, create_desktop, create_startup, launch_now):
        super().__init__()
        self.target_dir = target_dir
        self.create_desktop = create_desktop
        self.create_startup = create_startup
        self.launch_now = launch_now

    def run(self):
        try:
            self.progress.emit(10, "Creating destination folder...")
            os.makedirs(self.target_dir, exist_ok=True)
            self.msleep(200)

            self.progress.emit(30, "Extracting Rachayitha core binary...")
            src_exe = get_bundled_payload_path()
            if not os.path.exists(src_exe):
                raise FileNotFoundError(f"Cannot find core binary: {src_exe}")

            dest_exe = os.path.join(self.target_dir, "Rachayitha.exe")
            shutil.copy2(src_exe, dest_exe)

            # Copy logo if present
            logo_src = get_bundled_logo_path()
            if os.path.exists(logo_src):
                shutil.copy2(logo_src, os.path.join(self.target_dir, "rachayitha_logo.png"))

            self.msleep(300)

            self.progress.emit(50, "Installing Telugu phonetic rules matrix...")
            self.msleep(250)

            self.progress.emit(70, "Creating Desktop & Start Menu shortcuts...")
            appdata = os.environ.get("APPDATA", "")
            desktop = os.path.join(os.environ.get("USERPROFILE", ""), "Desktop")

            if self.create_desktop and os.path.exists(desktop):
                create_windows_shortcut(
                    dest_exe,
                    os.path.join(desktop, "Rachayitha.lnk"),
                    self.target_dir,
                    "Rachayitha - Telugu Phonetic Transliteration"
                )

            start_menu = os.path.join(appdata, r"Microsoft\Windows\Start Menu\Programs")
            if os.path.exists(start_menu):
                create_windows_shortcut(
                    dest_exe,
                    os.path.join(start_menu, "Rachayitha.lnk"),
                    self.target_dir,
                    "Rachayitha - Telugu Phonetic Transliteration"
                )

            self.progress.emit(85, "Configuring startup background hook...")
            if self.create_startup:
                startup_dir = os.path.join(appdata, r"Microsoft\Windows\Start Menu\Programs\Startup")
                if os.path.exists(startup_dir):
                    create_windows_shortcut(
                        dest_exe,
                        os.path.join(startup_dir, "Rachayitha.lnk"),
                        self.target_dir,
                        "Rachayitha Startup Hook"
                    )

            self.progress.emit(92, "Registering Windows uninstaller...")
            register_uninstaller(self.target_dir, dest_exe)
            self.msleep(200)

            if self.launch_now:
                self.progress.emit(98, "Launching Rachayitha into System Tray...")
                subprocess.Popen([dest_exe], cwd=self.target_dir, creationflags=0x08000000)

            self.progress.emit(100, "Installation complete!")
            self.finished.emit(True, dest_exe)
        except Exception as e:
            self.finished.emit(False, str(e))

class ProfessionalInstallerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("రచయిత (Rachayitha) v2.0 - Setup")
        self.setGeometry(250, 180, 840, 520)
        self.setFixedSize(840, 520)

        # Setup feature showcase slides
        self.slides = [
            {
                "icon": "⚡",
                "title": "Real-Time Phonetic Typing",
                "desc": "Type in English (Tenglish) in ANY Windows application — MS Word, Chrome, WhatsApp Desktop, Notepad, Slack — and see native Telugu appear in real-time."
            },
            {
                "icon": "✍️",
                "title": "Natural Halant-First Logic",
                "desc": "Single keystroke creates a half-letter (N -> న్, Na -> న, Ksha -> క్ష, NN -> న్న్). Fluid, effortless writing tailored for Telugu creators!"
            },
            {
                "icon": "🔤",
                "title": "Complete Phonetic RTS Coverage",
                "desc": "Full support for all 16 Achulu, 36 Hallulu, Guninthalu, Ligatures (జ్ఞ, క్ష, ఱ), Sunna (ం), and Visarga (ః)."
            },
            {
                "icon": "🏷️",
                "title": "Dynamic System Tray Icon",
                "desc": "The taskbar tray icon visually flips between 'తె' (Telugu) and 'EN' (English) so you always know your active language at a glance."
            },
            {
                "icon": "⚙️",
                "title": "Custom Hotkeys & Key Map",
                "desc": "Toggle languages seamlessly with your preferred hotkey (Default: Alt+T). Click tray icon for 60+ letter reference guide."
            },
            {
                "icon": "🧠",
                "title": "Trigram Context LM (34.7M Tokens)",
                "desc": "Resolves contextual polarity: 'akkada evaru leru' -> 'అక్కడ ఎవరూ లేరు' vs 'akkada evaru unnaru' -> 'అక్కడ ఎవరు ఉన్నారు' without special shift keys."
            },
            {
                "icon": "🔮",
                "title": "Next-Word Prediction & Tab Accept",
                "desc": "Fluid floating ghost pill overlay right at your cursor. Press [Tab ⇥] to autocomplete predicted words instantly."
            },
            {
                "icon": "⚡",
                "title": "Retroactive Sliding Window Lookahead",
                "desc": "3-word sliding buffer automatically backspaces and rewrites previous words when following context resolves them in 0ms."
            },
            {
                "icon": "📖",
                "title": "Casual Type with 58k+ Lexicon",
                "desc": "Type naturally in colloquial Tenglish (e.g. 'repu vastunna', 'cheppamdi' -> 'చెప్పండి') with 58k+ dictionary & typo fixes!"
            },
            {
                "icon": "🔒",
                "title": "100% Offline & Private",
                "desc": "Your typing never leaves your device. Zero cloud dependencies, zero telemetry, and takes under 20MB of RAM."
            }
        ]
        self.current_slide_idx = 0

        self.apply_theme()
        self.init_ui()

        # Timer to auto-rotate showcase slides every 3.5 seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_slide)
        self.timer.start(3500)

    def apply_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                color: #f8fafc;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 13px;
            }
            QFrame#sidebar {
                background-color: #1e293b;
                border-right: 1px solid #334155;
            }
            QFrame#slideCard {
                background-color: #0b0f19;
                border: 1px solid #334155;
                border-radius: 10px;
                padding: 16px;
            }
            QLineEdit {
                background-color: #0b0f19;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 8px 12px;
                color: #ffffff;
            }
            QPushButton#primaryBtn {
                background-color: #22c55e;
                color: white;
                font-weight: bold;
                font-size: 14px;
                padding: 10px 24px;
                border-radius: 6px;
                border: none;
            }
            QPushButton#primaryBtn:hover {
                background-color: #16a34a;
            }
            QPushButton#secondaryBtn {
                background-color: #334155;
                color: #cbd5e1;
                padding: 8px 16px;
                border-radius: 6px;
                border: none;
            }
            QPushButton#secondaryBtn:hover {
                background-color: #475569;
                color: #ffffff;
            }
            QProgressBar {
                background-color: #0b0f19;
                border: 1px solid #334155;
                border-radius: 6px;
                text-align: center;
                color: white;
                font-weight: bold;
                height: 22px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6366f1, stop:1 #38bdf8);
                border-radius: 5px;
            }
            QCheckBox {
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
        """)

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ---------------- LEFT SIDEBAR (Feature Showcase) ----------------
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(330)
        s_layout = QVBoxLayout(sidebar)
        s_layout.setContentsMargins(24, 28, 24, 28)

        # Logo & App Title
        logo_lbl = QLabel()
        logo_path = get_bundled_logo_path()
        if os.path.exists(logo_path):
            pix = QPixmap(logo_path).scaled(72, 72, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_lbl.setPixmap(pix)
            self.setWindowIcon(QIcon(logo_path))
        else:
            logo_lbl.setText("ర")
            logo_lbl.setStyleSheet("font-size: 36px; font-weight: bold; color: #38bdf8;")
        s_layout.addWidget(logo_lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        title_lbl = QLabel("రచయిత (Rachayitha)")
        title_lbl.setStyleSheet("font-size: 19px; font-weight: 700; color: #ffffff; margin-top: 8px;")
        s_layout.addWidget(title_lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        sub_lbl = QLabel("Telugu Phonetic Transliteration Tool")
        sub_lbl.setStyleSheet("font-size: 12px; color: #94a3b8; margin-bottom: 16px;")
        s_layout.addWidget(sub_lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        # Feature Presentation Card
        self.slide_card = QFrame()
        self.slide_card.setObjectName("slideCard")
        sc_layout = QVBoxLayout(self.slide_card)

        self.slide_icon_title = QLabel()
        self.slide_icon_title.setStyleSheet("font-size: 15px; font-weight: bold; color: #38bdf8;")
        sc_layout.addWidget(self.slide_icon_title)

        self.slide_desc = QLabel()
        self.slide_desc.setWordWrap(True)
        self.slide_desc.setStyleSheet("color: #cbd5e1; font-size: 12px; line-height: 1.5; margin-top: 6px;")
        sc_layout.addWidget(self.slide_desc)

        s_layout.addWidget(self.slide_card)

        # Slide Dots Indicator
        self.dots_layout = QHBoxLayout()
        self.dots = []
        for i in range(len(self.slides)):
            dot = QLabel("●")
            dot.setStyleSheet("color: #6366f1; font-size: 10px;" if i == 0 else "color: #334155; font-size: 10px;")
            self.dots.append(dot)
            self.dots_layout.addWidget(dot)
        s_layout.addLayout(self.dots_layout)

        s_layout.addStretch()

        credits_lbl = QLabel("Version 2.0.0 • Ramaputhra")
        credits_lbl.setStyleSheet("color: #64748b; font-size: 11px;")
        s_layout.addWidget(credits_lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(sidebar)

        # ---------------- RIGHT PANEL (Wizard Pages) ----------------
        self.wizard_stack = QStackedWidget()

        # Page 0: Setup Options
        self.page_setup = self.create_page_setup()
        self.wizard_stack.addWidget(self.page_setup)

        # Page 1: Progress
        self.page_progress = self.create_page_progress()
        self.wizard_stack.addWidget(self.page_progress)

        # Page 2: Success
        self.page_success = self.create_page_success()
        self.wizard_stack.addWidget(self.page_success)

        main_layout.addWidget(self.wizard_stack)

        self.update_slide_display()

    def update_slide_display(self):
        slide = self.slides[self.current_slide_idx]
        self.slide_icon_title.setText(f"{slide['icon']}  {slide['title']}")
        self.slide_desc.setText(slide['desc'])
        for i, dot in enumerate(self.dots):
            if i == self.current_slide_idx:
                dot.setStyleSheet("color: #38bdf8; font-size: 12px;")
            else:
                dot.setStyleSheet("color: #334155; font-size: 10px;")

    def next_slide(self):
        self.current_slide_idx = (self.current_slide_idx + 1) % len(self.slides)
        self.update_slide_display()

    def create_page_setup(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(32, 32, 32, 28)
        layout.setSpacing(16)

        header_title = QLabel("Install Rachayitha on your PC")
        header_title.setStyleSheet("font-size: 22px; font-weight: 700; color: #ffffff;")
        layout.addWidget(header_title)

        header_desc = QLabel("Experience smooth, real-time Telugu typing across all your desktop applications.")
        header_desc.setStyleSheet("color: #94a3b8; font-size: 13px; margin-bottom: 8px;")
        layout.addWidget(header_desc)

        # Folder location
        layout.addWidget(QLabel("Installation Directory:"))
        dir_box = QHBoxLayout()
        self.dir_input = QLineEdit(DEFAULT_INSTALL_DIR)
        dir_box.addWidget(self.dir_input)
        browse_btn = QPushButton("Browse...")
        browse_btn.setObjectName("secondaryBtn")
        browse_btn.clicked.connect(self.browse_folder)
        dir_box.addWidget(browse_btn)
        layout.addLayout(dir_box)

        layout.addSpacing(6)

        # Options
        layout.addWidget(QLabel("Installation Options:"))
        self.desktop_chk = QCheckBox("Create Desktop Shortcut")
        self.desktop_chk.setChecked(True)
        layout.addWidget(self.desktop_chk)

        self.startup_chk = QCheckBox("Automatically start when Windows boots (Lives silently in System Tray)")
        self.startup_chk.setChecked(True)
        layout.addWidget(self.startup_chk)

        self.launch_chk = QCheckBox("Launch Rachayitha immediately after installation")
        self.launch_chk.setChecked(True)
        layout.addWidget(self.launch_chk)

        layout.addStretch()

        # Action Buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondaryBtn")
        cancel_btn.clicked.connect(self.close)
        btn_row.addWidget(cancel_btn)

        install_btn = QPushButton("Install Now")
        install_btn.setObjectName("primaryBtn")
        install_btn.clicked.connect(self.start_installation)
        btn_row.addWidget(install_btn)
        layout.addLayout(btn_row)

        return page

    def browse_folder(self):
        chosen = QFileDialog.getExistingDirectory(self, "Select Install Folder", self.dir_input.text())
        if chosen:
            self.dir_input.setText(os.path.join(chosen, APP_NAME))

    def create_page_progress(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(32, 48, 32, 28)
        layout.setSpacing(16)

        p_title = QLabel("Installing Rachayitha...")
        p_title.setStyleSheet("font-size: 22px; font-weight: 700; color: #ffffff;")
        layout.addWidget(p_title)

        p_desc = QLabel("Please wait while setup copies files and configures your keyboard hooks.")
        p_desc.setStyleSheet("color: #94a3b8; font-size: 13px;")
        layout.addWidget(p_desc)

        layout.addSpacing(24)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.status_msg = QLabel("Preparing installation...")
        self.status_msg.setStyleSheet("color: #38bdf8; font-weight: 600; font-size: 13px;")
        layout.addWidget(self.status_msg)

        layout.addStretch()
        return page

    def create_page_success(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(32, 40, 32, 28)
        layout.setSpacing(14)

        check_lbl = QLabel("✓")
        check_lbl.setStyleSheet("font-size: 48px; color: #22c55e; font-weight: bold;")
        layout.addWidget(check_lbl, alignment=Qt.AlignmentFlag.AlignCenter)

        s_title = QLabel("Rachayitha Successfully Installed!")
        s_title.setStyleSheet("font-size: 22px; font-weight: 700; color: #ffffff;")
        layout.addWidget(s_title, alignment=Qt.AlignmentFlag.AlignCenter)

        s_box = QFrame()
        s_box.setStyleSheet("background-color: #0b0f19; border: 1px solid #334155; border-radius: 8px; padding: 16px;")
        sb_layout = QVBoxLayout(s_box)

        tip1 = QLabel("<b>• Active Language Icon:</b> Sits in your Taskbar Tray ('తె' for Telugu, 'EN' for English).")
        tip2 = QLabel("<b>• Hotkey Toggle:</b> Press <b>Alt+T</b> in Word, Chrome, WhatsApp to type in Telugu.")
        tip3 = QLabel("<b>• Key Map & Settings:</b> Click the tray icon to view all 60+ letter mappings.")
        sb_layout.addWidget(tip1)
        sb_layout.addWidget(tip2)
        sb_layout.addWidget(tip3)
        layout.addWidget(s_box)

        layout.addStretch()

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        finish_btn = QPushButton("Finish & Enjoy Typing")
        finish_btn.setObjectName("primaryBtn")
        finish_btn.clicked.connect(self.close)
        btn_row.addWidget(finish_btn)
        layout.addLayout(btn_row)

        return page

    def start_installation(self):
        target_dir = self.dir_input.text().strip()
        if not target_dir:
            QMessageBox.warning(self, "Invalid Directory", "Please select a valid installation directory.")
            return

        self.wizard_stack.setCurrentIndex(1)

        self.worker = InstallWorker(
            target_dir=target_dir,
            create_desktop=self.desktop_chk.isChecked(),
            create_startup=self.startup_chk.isChecked(),
            launch_now=self.launch_chk.isChecked()
        )
        self.worker.progress.connect(self.on_install_progress)
        self.worker.finished.connect(self.on_install_finished)
        self.worker.start()

    def on_install_progress(self, percent, msg):
        self.progress_bar.setValue(percent)
        self.status_msg.setText(msg)

    def on_install_finished(self, success, result):
        if success:
            self.wizard_stack.setCurrentIndex(2)
        else:
            QMessageBox.critical(self, "Installation Failed", f"Installation encountered an error:\n{result}")
            self.wizard_stack.setCurrentIndex(0)

def main():
    app = QApplication(sys.argv)
    window = ProfessionalInstallerWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
