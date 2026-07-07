from pathlib import Path

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton


BASE_DIR = Path(__file__).resolve().parents[2]
ICONS_DIR = BASE_DIR / "assets" / "icons" / "sidebar"


class LPSidebarButton(QPushButton):
    def __init__(self, text, icon_name):
        super().__init__(text)

        self.setObjectName("sidebarButton")
        self.setCursor(Qt.PointingHandCursor)

        self.setIcon(QIcon(str(ICONS_DIR / icon_name)))
        self.setIconSize(QSize(20, 20))

        self.setMinimumHeight(46)
        self.setCheckable(True)