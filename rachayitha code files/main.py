import sys
import os
import ctypes
import keyboard
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, pyqtSignal

from engine.paths import load_config
from engine.buffer import TypingBuffer
from engine.transliterator import transliterate
from ui.tray import RachayithaTray
from ui.settings import SettingsWindow

class AppBridge(QObject):
    mode_changed = pyqtSignal(bool)

class RachayithaApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        self.bridge = AppBridge()
        self.bridge.mode_changed.connect(self.on_mode_changed_gui)

        self.config = load_config()
        self.is_telugu_on = False
        casual_enabled = self.config.get("casual_type", True)
        self.buffer = TypingBuffer(casual_enabled=casual_enabled)

        # Windows CapsLock check helper
        self.user32 = ctypes.windll.user32 if os.name == 'nt' else None

        # Settings Window (Lazy show)
        self.settings_window = None

        # Active hotkey references
        self.current_hotkey = self.config.get("hotkeys", {}).get("telugu_toggle", "alt+t")
        self.english_hotkey = self.config.get("hotkeys", {}).get("english", "alt+e")

        # System Tray (Icon dynamically renders 'తె' when Telugu is ON, 'EN' when English is ON)
        self.tray = RachayithaTray(
            self.app,
            on_toggle_callback=self.set_mode,
            on_settings_callback=self.open_settings,
            on_exit_callback=self.exit_app
        )

        # Setup Keyboard Hooks
        self.setup_hooks()

    def is_caps_active(self):
        if self.user32:
            return bool(self.user32.GetKeyState(0x14) & 1)
        return False

    def setup_hooks(self):
        try:
            keyboard.add_hotkey(self.current_hotkey, self.toggle_mode)
            keyboard.add_hotkey(self.english_hotkey, lambda: self.set_mode(False))
        except Exception as e:
            print(f"Error adding hotkey {self.current_hotkey}: {e}")

        keyboard.hook(self.handle_key_event, suppress=True)

    def on_hotkey_changed(self, new_hotkey: str):
        """
        Dynamically unregister the old hotkey and register the new one live
        """
        try:
            try:
                keyboard.remove_hotkey(self.current_hotkey)
            except Exception:
                pass
            self.current_hotkey = new_hotkey
            keyboard.add_hotkey(self.current_hotkey, self.toggle_mode)
            print(f"Hotkey successfully updated to: {self.current_hotkey}")
        except Exception as e:
            print(f"Error binding new hotkey {new_hotkey}: {e}")

    def toggle_mode(self):
        self.set_mode(not self.is_telugu_on)

    def set_mode(self, enabled: bool):
        self.is_telugu_on = enabled
        self.buffer.commit()
        # Emit signal to update GUI & dynamic tray icon on Qt main thread
        self.bridge.mode_changed.emit(self.is_telugu_on)

    def on_mode_changed_gui(self, is_telugu: bool):
        # Update dynamic tray icon ('తె' or 'EN') and tooltip
        self.tray.update_mode(is_telugu)

        # Show balloon notification if enabled in config
        if self.config.get("show_notifications", True):
            if is_telugu:
                self.tray.show_notification("రచయిత (Rachayitha)", "Telugu Mode Active (తె)")
            else:
                self.tray.show_notification("రచయిత (Rachayitha)", "English Mode Active (EN)")

    def handle_key_event(self, e):
        if not self.is_telugu_on:
            return True

        if e.event_type != 'down':
            return True

        # Ignore shortcut combinations like Ctrl+C, Ctrl+V, Alt+Tab
        if keyboard.is_pressed('ctrl') or keyboard.is_pressed('alt'):
            return True

        # Commit word on boundary
        if e.name in ['space', 'enter']:
            self.buffer.commit()
            return True

        # Handle Backspace
        if e.name == 'backspace':
            if self.buffer.is_active():
                backspaces_needed, new_out = self.buffer.backspace()
                for _ in range(backspaces_needed):
                    keyboard.send('backspace')
                if new_out:
                    keyboard.write(new_out)
                return False
            return True

        # Handle Letter typing
        if len(e.name) == 1:
            is_alpha = e.name.isalpha()
            is_special = e.name in ['~', '_']

            if is_alpha or is_special:
                # Detect Shift or CapsLock for correct case sensitivity (t vs T, d vs D, n vs N, M)
                shift_held = keyboard.is_pressed('shift')
                caps = self.is_caps_active()
                is_upper = shift_held ^ caps

                char = e.name.upper() if is_upper else e.name.lower()

                backspaces_needed, new_out = self.buffer.add(char)
                for _ in range(backspaces_needed):
                    keyboard.send('backspace')
                keyboard.write(new_out)
                return False

        return True

    def on_casual_type_changed(self, enabled: bool):
        self.config["casual_type"] = enabled
        self.buffer.set_casual_enabled(enabled)
        print(f"Casual Type toggled: {'ON' if enabled else 'OFF'}")

    def open_settings(self):
        try:
            if not self.settings_window:
                self.settings_window = SettingsWindow(
                    on_toggle_callback=self.set_mode,
                    on_hotkey_changed_callback=self.on_hotkey_changed,
                    on_casual_type_changed_callback=self.on_casual_type_changed
                )
            if self.settings_window.isMinimized():
                self.settings_window.showNormal()
            self.settings_window.show()
            self.settings_window.raise_()
            self.settings_window.activateWindow()
        except Exception as e:
            import traceback
            traceback.print_exc()
            try:
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.critical(None, "Rachayitha Error", f"Failed to open settings window:\n{e}")
            except Exception:
                pass

    def exit_app(self):
        self.app.quit()
        os._exit(0)

    def run(self):
        print(f"Rachayitha running in system tray. Press [{self.current_hotkey.upper()}] to toggle Telugu.")
        sys.exit(self.app.exec())

def setup_exception_logger():
    def handler(exctype, value, tb):
        import traceback
        err_msg = "".join(traceback.format_exception(exctype, value, tb))
        print(f"Unhandled Exception: {err_msg}", file=sys.stderr)
        try:
            from engine.paths import get_config_dir
            log_path = os.path.join(get_config_dir(), "rachayitha_error.log")
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"\n--- ERROR ---\n{err_msg}\n")
        except Exception:
            pass
    sys.excepthook = handler

if __name__ == "__main__":
    setup_exception_logger()
    app = RachayithaApp()
    app.run()
