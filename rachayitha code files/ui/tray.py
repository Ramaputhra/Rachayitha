import os
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont, QPen
from PyQt6.QtCore import Qt

def create_dynamic_lang_icon(is_telugu: bool) -> QIcon:
    """
    Dynamically render a high-DPI system tray icon:
    - Displays 'తె' in vibrant indigo gradient badge when Telugu is ON
    - Displays 'EN' in sleek slate/blue badge when English is ON
    """
    size = 64
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

    if is_telugu:
        # Telugu Active Mode: Vibrant Indigo / Violet badge with glow border
        painter.setBrush(QColor("#6366f1"))
        painter.setPen(QPen(QColor("#a5b4fc"), 3))
        painter.drawRoundedRect(3, 3, size - 6, size - 6, 16, 16)

        # Telugu letter 'తె'
        painter.setPen(QColor("#ffffff"))
        font = QFont("Mandali", 30, QFont.Weight.Bold)
        font.setFamilies(["Mandali", "Gautami", "Nirmala UI", "Noto Sans Telugu", "Segoe UI"])
        painter.setFont(font)
        painter.drawText(0, -2, size, size, Qt.AlignmentFlag.AlignCenter, "తె")
    else:
        # English Mode: Modern Slate-Blue badge
        painter.setBrush(QColor("#334155"))
        painter.setPen(QPen(QColor("#64748b"), 3))
        painter.drawRoundedRect(3, 3, size - 6, size - 6, 16, 16)

        # English text 'EN'
        painter.setPen(QColor("#f8fafc"))
        font = QFont("Segoe UI", 24, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(0, 0, size, size, Qt.AlignmentFlag.AlignCenter, "EN")

    painter.end()
    return QIcon(pixmap)

class RachayithaTray(QSystemTrayIcon):
    def __init__(self, app, on_toggle_callback, on_settings_callback, on_exit_callback):
        super().__init__(create_dynamic_lang_icon(False), app)
        self.on_toggle_callback = on_toggle_callback
        self.on_settings_callback = on_settings_callback
        self.on_exit_callback = on_exit_callback

        self.menu = QMenu()

        self.telugu_action = self.menu.addAction("Telugu (తెలుగు) - Tenglish")
        self.telugu_action.setCheckable(True)
        self.telugu_action.triggered.connect(lambda: self.on_toggle_callback(True))

        self.english_action = self.menu.addAction("English (ఆంగ్లం)")
        self.english_action.setCheckable(True)
        self.english_action.triggered.connect(lambda: self.on_toggle_callback(False))

        self.menu.addSeparator()
        self.settings_action = self.menu.addAction("Open Settings & Key Map...")
        self.settings_action.triggered.connect(self.on_settings_callback)

        self.menu.addSeparator()
        self.exit_action = self.menu.addAction("Exit Rachayitha")
        self.exit_action.triggered.connect(self.on_exit_callback)

        self.setContextMenu(self.menu)

        # Clicking tray icon immediately opens the main UI window
        self.activated.connect(self.on_tray_activated)

        self.update_mode(False)
        self.show()

    def update_mode(self, is_telugu: bool):
        # Update dynamic tray icon visually
        self.setIcon(create_dynamic_lang_icon(is_telugu))

        # Update context menu checkmarks
        self.telugu_action.setChecked(is_telugu)
        self.english_action.setChecked(not is_telugu)

        # Update tooltip
        if is_telugu:
            self.setToolTip("Rachayitha: Telugu Mode ACTIVE\nClick to open Key Map & Settings")
        else:
            self.setToolTip("Rachayitha: English Mode ACTIVE\nClick to open Key Map & Settings")

    def show_notification(self, title, message):
        self.showMessage(title, message, QSystemTrayIcon.MessageIcon.Information, 1500)

    def on_tray_activated(self, reason):
        # Upon single-click or double-click, open main UI window
        if reason in (QSystemTrayIcon.ActivationReason.Trigger, QSystemTrayIcon.ActivationReason.DoubleClick):
            self.on_settings_callback()
