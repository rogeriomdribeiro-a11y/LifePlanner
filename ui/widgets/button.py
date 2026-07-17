from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QPushButton

from app.resources import get_icon


class LPButton(QPushButton):
    """Botão principal reutilizável da aplicação."""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)

        self.setObjectName("lpButton")
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(90, 40)


class LPGoogleButton(QPushButton):
    """Botão reutilizável para iniciar a autenticação Google."""
    def __init__(self, text="Continuar com Google", parent=None):
        super().__init__(text, parent)

        self.setObjectName("googleButton")
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(250, 40)

        self.setIcon(get_icon("login", "google.png"))
        self.setIconSize(QSize(18, 18))
        self.setStyleSheet("""
        text-align: center;
        padding-left: 25px;
        padding-right: 25px;
         """)