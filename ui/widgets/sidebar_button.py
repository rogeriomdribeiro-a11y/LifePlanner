from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton


from app.path import ICONS_DIR


SIDEBAR_ICONS_DIR = ICONS_DIR / "sidebar"


class LPSidebarButton(QPushButton):
    """Botão selecionável utilizado no menu lateral."""
    def __init__(self, text, icon_name):
        super().__init__(text)

        self.setObjectName("sidebarButton")
        self.setCursor(Qt.PointingHandCursor)

        self.setIcon(QIcon(str(SIDEBAR_ICONS_DIR / icon_name)))
        self.setIconSize(QSize(20, 20))

        self.setMinimumHeight(46)
        self.setCheckable(True)