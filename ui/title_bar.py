from pathlib import Path

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame, QPushButton


BASE_DIR = Path(__file__).resolve().parent.parent
WINDOW_ICONS_DIR = BASE_DIR / "assets" / "icons" / "window"


class TitleBar(QFrame):
    def __init__(self, window):
        super().__init__()

        self.window = window
        self.setObjectName("titleBar")
        self.setFixedHeight(38)

        self.minimize_button = QPushButton(self)
        self.minimize_button.setObjectName("windowButton")
        self.minimize_button.setGeometry(0, 4, 34, 26)
        self.minimize_button.setIcon(QIcon(str(WINDOW_ICONS_DIR / "minimize.svg")))
        self.minimize_button.setIconSize(QSize(14, 14))
        self.minimize_button.setCursor(Qt.PointingHandCursor)
        self.minimize_button.clicked.connect(self.window.showMinimized)

        self.close_button = QPushButton(self)
        self.close_button.setObjectName("closeButton")
        self.close_button.setGeometry(38, 4, 34, 26)
        self.close_button.setIcon(QIcon(str(WINDOW_ICONS_DIR / "close.svg")))
        self.close_button.setIconSize(QSize(14, 14))
        self.close_button.setCursor(Qt.PointingHandCursor)
        self.close_button.clicked.connect(self.window.close)

    def resizeEvent(self, event):
        margin_right = 10
        button_width = 34
        button_height = 26
        spacing = 4
        top = 6

        close_x = self.width() - margin_right - button_width
        minimize_x = close_x - spacing - button_width

        self.minimize_button.setGeometry(
            minimize_x,
            top,
            button_width,
            button_height
        )

        self.close_button.setGeometry(
            close_x,
            top,
            button_width,
            button_height
        )

        super().resizeEvent(event)