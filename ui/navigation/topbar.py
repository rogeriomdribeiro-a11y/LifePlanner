from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton

from app.session import Session


class Topbar(QFrame):
    def __init__(self):
        super().__init__()

        self.setObjectName("topbar")
        self.setFixedHeight(74)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(28, 16, 28, 16)
        layout.setSpacing(12)

        user = Session.current_user
        name = user["full_name"] if user else "Utilizador"

        title = QLabel(f"Olá, {name}! 👋")
        title.setObjectName("topbarTitle")

        search = QLineEdit()
        search.setObjectName("searchInput")
        search.setPlaceholderText("Pesquisar...")
        search.setFixedWidth(300)

        notification = QPushButton("🔔")
        notification.setObjectName("topbarIconButton")
        notification.setCursor(Qt.PointingHandCursor)

        settings = QPushButton("⚙")
        settings.setObjectName("topbarIconButton")
        settings.setCursor(Qt.PointingHandCursor)

        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(search)
        layout.addWidget(notification)
        layout.addWidget(settings)