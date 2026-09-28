import sys
import os
import subprocess
import winreg
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QProgressBar, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QIcon

APP_NAME = "Rachayitha"

class UninstallWorker(QThread):
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str)

    def __init__(self, install_dir):
        super().__init__()
        self.install_dir = install_dir

    def run(self):
        try:
            self.progress.emit(20, "Stopping running Rachayitha processes...")
            # Terminate running app
            subprocess.run(["taskkill", "/F", "/IM", "Rachayitha.exe"], capture_output=True)

            self.progress.emit(40, "Removing Windows shortcuts...")
            # Remove desktop shortcut
            desktop = os.path.join(os.environ.get("USERPROFILE", ""), "Desktop")
            desk_lnk = os.path.join(desktop, "Rachayitha.lnk")
            if os.path.exists(desk_lnk):
                try: os.remove(desk_lnk)
                except Exception: pass

            # Remove start menu shortcut
            appdata = os.environ.get("APPDATA", "")
            start_menu_lnk = os.path.join(appdata, r"Microsoft\Windows\Start Menu\Programs\Rachayitha.lnk")
            if os.path.exists(start_menu_lnk):
                try: os.remove(start_menu_lnk)
                except Exception: pass

            # Remove startup shortcut
            startup_lnk = os.path.join(appdata, r"Microsoft\Windows\Start Menu\Programs\Startup\Rachayitha.lnk")
            if os.path.exists(startup_lnk):
                try: os.remove(startup_lnk)
                except Exception: pass

            self.progress.emit(70, "Cleaning Windows Registry...")
            # Remove from Run registry
            try:
                run_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
                winreg.DeleteValue(run_key, APP_NAME)
                winreg.CloseKey(run_key)
            except Exception:
                pass

            # Remove from Uninstall registry
            try:
                uninst_key = r"Software\Microsoft\Windows\CurrentVersion\Uninstall"
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, uninst_key, 0, winreg.KEY_ALL_ACCESS)
                winreg.DeleteKey(key, APP_NAME)
                winreg.CloseKey(key)
            except Exception:
                pass

            self.progress.emit(90, "Scheduling file cleanup...")
            # Self-deletion batch script (runs after this uninstaller exits)
            del_bat = os.path.join(os.environ.get("TEMP", os.path.expanduser("~")), "uninstall_rachayitha.bat")
            with open(del_bat, "w") as f:
                f.write(f'@echo off\n')
                f.write(f'timeout /t 2 /nobreak >nul\n')
                f.write(f'rd /s /q "{self.install_dir}"\n')
                f.write(f'del "%~f0"\n')

            subprocess.Popen(["cmd.exe", "/c", del_bat], creationflags=0x08000000)

            self.progress.emit(100, "Uninstallation complete!")
            self.finished.emit(True, "")
        except Exception as e:
            self.finished.emit(False, str(e))

class UninstallerWindow(QWidget):
    def __init__(self, install_dir):
        super().__init__()
        self.install_dir = install_dir
        self.setWindowTitle("రచయిత (Rachayitha) - Uninstaller")
        self.setGeometry(350, 250, 520, 320)
        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                color: #f8fafc;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 13px;
            }
            QFrame#headerBox {
                background-color: #1e293b;
                border-bottom: 2px solid #ef4444;
                padding: 16px;
            }
            QPushButton#uninstallBtn {
                background-color: #ef4444;
                color: white;
                font-weight: bold;
                padding: 9px 20px;
                border-radius: 6px;
                border: none;
            }
            QPushButton#uninstallBtn:hover {
                background-color: #dc2626;
            }
            QPushButton#cancelBtn {
                background-color: #334155;
                color: white;
                padding: 9px 18px;
                border-radius: 6px;
                border: none;
            }
            QPushButton#cancelBtn:hover {
                background-color: #475569;
            }
            QProgressBar {
                background-color: #0b0f19;
                border: 1px solid #334155;
                border-radius: 6px;
                text-align: center;
                color: white;
                font-weight: bold;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #ef4444;
                border-radius: 5px;
            }
        """)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 20)

        # Header
        header = QFrame()
        header.setObjectName("headerBox")
        h_layout = QHBoxLayout(header)

        title_box = QVBoxLayout()
        t1 = QLabel("Uninstall Rachayitha (రచయిత)")
        t1.setStyleSheet("font-size: 17px; font-weight: bold; color: #ffffff;")
        t2 = QLabel("Remove Rachayitha and all its components from this computer")
        t2.setStyleSheet("color: #94a3b8; font-size: 12px;")
        title_box.addWidget(t1)
        title_box.addWidget(t2)
        h_layout.addLayout(title_box)
        layout.addWidget(header)

        # Body
        body = QVBoxLayout()
        body.setContentsMargins(24, 16, 24, 0)
        body.setSpacing(14)

        self.info_lbl = QLabel(
            "Are you sure you want to uninstall Rachayitha?\n\n"
            "This will remove the application, desktop and startup shortcuts, "
            "and unregister the system tray hook."
        )
        self.info_lbl.setStyleSheet("line-height: 1.5; color: #cbd5e1;")
        body.addWidget(self.info_lbl)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        body.addWidget(self.progress_bar)

        self.status_lbl = QLabel("")
        self.status_lbl.setStyleSheet("color: #38bdf8; font-weight: 500;")
        body.addWidget(self.status_lbl)

        body.addStretch()

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        self.uninstall_btn = QPushButton("Uninstall")
        self.uninstall_btn.setObjectName("uninstallBtn")
        self.uninstall_btn.clicked.connect(self.start_uninstall)
        btn_row.addWidget(self.uninstall_btn)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setObjectName("cancelBtn")
        self.cancel_btn.clicked.connect(self.close)
        btn_row.addWidget(self.cancel_btn)

        body.addLayout(btn_row)
        layout.addLayout(body)
        self.setLayout(layout)

    def start_uninstall(self):
        self.uninstall_btn.setEnabled(False)
        self.cancel_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.status_lbl.setText("Uninstalling...")

        self.worker = UninstallWorker(self.install_dir)
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def on_progress(self, percent, msg):
        self.progress_bar.setValue(percent)
        self.status_lbl.setText(msg)

    def on_finished(self, success, err):
        if success:
            QMessageBox.information(
                self, "Uninstallation Complete",
                "Rachayitha (రచయిత) has been successfully removed from your computer."
            )
            self.close()
        else:
            QMessageBox.critical(self, "Uninstall Error", f"Uninstallation encountered an error:\n{err}")
            self.uninstall_btn.setEnabled(True)
            self.cancel_btn.setEnabled(True)

def main():
    app = QApplication(sys.argv)
    # Default to current directory if not passed
    install_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    window = UninstallerWindow(install_dir)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
