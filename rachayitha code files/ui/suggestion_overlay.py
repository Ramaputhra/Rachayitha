import os
import sys
import ctypes
from typing import Optional, List, Union
from ctypes import wintypes
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QApplication, QFrame
from PyQt6.QtGui import QColor, QFont, QCursor
from PyQt6.QtCore import Qt, QTimer, QPoint, pyqtSignal

class GUITHREADINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("hwndActive", wintypes.HWND),
        ("hwndFocus", wintypes.HWND),
        ("hwndCapture", wintypes.HWND),
        ("hwndMenuOwner", wintypes.HWND),
        ("hwndMoveSize", wintypes.HWND),
        ("hwndCaret", wintypes.HWND),
        ("rcCaret", wintypes.RECT)
    ]

class POINT(ctypes.Structure):
    _fields_ = [("x", wintypes.LONG), ("y", wintypes.LONG)]

class SuggestionOverlay(QWidget):
    """
    Sleek, production-ready floating pill dock for next-word contextual suggestions.
    - Displays top 3 candidates with primary Tab ⇥ quick-acceptance.
    - Clickable pills allow instant insertion of secondary/tertiary candidates.
    - Window does not steal focus (WindowDoesNotAcceptFocus & WA_ShowWithoutActivating).
    - Intelligent Win32 caret tracking with screen-boundary protection.
    """
    candidate_accepted = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Non-intrusive floating overlay flags
        self.setWindowFlags(
            Qt.WindowType.ToolTip |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.current_candidates = []
        self._user32 = ctypes.windll.user32 if os.name == 'nt' else None

        # Auto-hide timer (3.5 seconds)
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.setInterval(3500)
        self.timer.timeout.connect(self.hide)

        self._init_ui()

    def _init_ui(self):
        root_layout = QHBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)

        # Translucent glassmorphism pill container
        self.card = QFrame(self)
        self.card.setStyleSheet("""
            QFrame {
                background-color: rgba(15, 23, 42, 235);
                border: 1px solid rgba(99, 102, 241, 0.55);
                border-radius: 12px;
            }
        """)
        card_layout = QHBoxLayout(self.card)
        card_layout.setContentsMargins(10, 5, 10, 5)
        card_layout.setSpacing(6)

        # Icon / Prefix label
        self.icon_label = QLabel("🔮")
        self.icon_label.setStyleSheet("font-size: 13px; background: transparent; border: none;")
        card_layout.addWidget(self.icon_label)

        # Common font for Telugu candidates
        telugu_font = QFont("Nirmala UI", 12, QFont.Weight.Bold)
        telugu_font.setFamilies(["Nirmala UI", "Gautami", "Mandali", "Noto Sans Telugu", "Segoe UI"])

        # Candidate Pills (Up to 3)
        self.pills = []
        for i in range(3):
            btn = QPushButton("")
            btn.setFont(telugu_font)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

            if i == 0:
                # Primary candidate: Highlighted glowing cyan with Tab badge
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(14, 165, 233, 0.22);
                        color: #38bdf8;
                        border: 1px solid #38bdf8;
                        border-radius: 7px;
                        padding: 2px 10px;
                        font-weight: bold;
                        font-size: 13px;
                    }
                    QPushButton:hover {
                        background-color: rgba(14, 165, 233, 0.42);
                        color: #ffffff;
                    }
                """)
            else:
                # Secondary & Tertiary candidates: Sleek slate pills
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: rgba(51, 65, 85, 0.65);
                        color: #e2e8f0;
                        border: 1px solid #475569;
                        border-radius: 7px;
                        padding: 2px 8px;
                        font-weight: 600;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: rgba(100, 116, 139, 0.85);
                        color: #ffffff;
                        border: 1px solid #94a3b8;
                    }
                """)

            btn.clicked.connect(lambda checked, idx=i: self._on_pill_clicked(idx))
            card_layout.addWidget(btn)
            self.pills.append(btn)

        root_layout.addWidget(self.card)

    def _on_pill_clicked(self, index: int):
        if 0 <= index < len(self.current_candidates):
            selected = self.current_candidates[index]
            self.candidate_accepted.emit(selected)

    def get_caret_position(self) -> Optional[QPoint]:
        """
        Retrieves OS caret coordinates via Win32 API.
        Falls back to None if unsupported by active foreground window.
        """
        if not self._user32:
            return None

        try:
            gui_info = GUITHREADINFO()
            gui_info.cbSize = ctypes.sizeof(GUITHREADINFO)
            # 0 = foreground thread
            if self._user32.GetGUIThreadInfo(0, ctypes.byref(gui_info)):
                hwnd = gui_info.hwndCaret or gui_info.hwndFocus
                if hwnd and (gui_info.rcCaret.left != 0 or gui_info.rcCaret.top != 0):
                    pt = POINT(gui_info.rcCaret.left, gui_info.rcCaret.bottom)
                    if self._user32.ClientToScreen(hwnd, ctypes.byref(pt)):
                        if pt.x > 0 and pt.y > 0:
                            return QPoint(pt.x, pt.y)
        except Exception:
            pass

        return None

    def show_suggestion(self, suggestions: Union[str, List[str]]):
        if isinstance(suggestions, str):
            candidates = [suggestions] if suggestions.strip() else []
        elif isinstance(suggestions, (list, tuple)):
            candidates = [s for s in suggestions if s and s.strip()]
        else:
            candidates = []

        if not candidates:
            self.hide()
            return

        self.current_candidates = candidates[:3]

        # Update candidate buttons
        for i in range(3):
            if i < len(self.current_candidates):
                word = self.current_candidates[i]
                if i == 0:
                    self.pills[i].setText(f"1. {word}  [Tab ⇥]")
                else:
                    self.pills[i].setText(f"{i + 1}. {word}")
                self.pills[i].setVisible(True)
            else:
                self.pills[i].setVisible(False)

        self.adjustSize()

        # Compute optimal desktop placement
        pos = self.get_caret_position()
        if pos:
            target_x = pos.x()
            target_y = pos.y() + 6
        else:
            mouse_pt = QCursor.pos()
            target_x = mouse_pt.x() + 15
            target_y = mouse_pt.y() + 20

        # Boundary collision check against available desktop workarea
        screen = QApplication.primaryScreen()
        if screen:
            screen_geo = screen.availableGeometry()
            if target_x + self.width() > screen_geo.right():
                target_x = screen_geo.right() - self.width() - 10
            if target_y + self.height() > screen_geo.bottom():
                target_y = target_y - self.height() - 35
            target_x = max(screen_geo.left() + 10, target_x)
            target_y = max(screen_geo.top() + 10, target_y)

        self.move(target_x, target_y)
        self.show()
        self.timer.start()

    def get_primary_suggestion(self) -> str:
        return self.current_candidates[0] if self.current_candidates else ""

    def hide(self):
        self.timer.stop()
        self.current_candidates = []
        super().hide()

    def is_visible(self) -> bool:
        return self.isVisible()
