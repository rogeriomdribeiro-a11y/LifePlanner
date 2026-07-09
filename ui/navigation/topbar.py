from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLineEdit, QPushButton


class Topbar(QFrame):
    def __init__(self):
        super().__init__()

        self.setObjectName("topbar")
        self.setFixedHeight(74)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(40, 16, 140, 16)
        layout.setSpacing(12)

        self.search = QLineEdit()
        self.search.setObjectName("searchInput")
        self.search.setPlaceholderText("Pesquisar...")
        self.search.setFixedWidth(320)

        self.notification_button = QPushButton("🔔")
        self.notification_button.setObjectName("topbarIconButton")
        self.notification_button.setCursor(Qt.PointingHandCursor)

        self.settings_button = QPushButton("⚙")
        self.settings_button.setObjectName("topbarIconButton")
        self.settings_button.setCursor(Qt.PointingHandCursor)

        layout.addWidget(self.search)
        layout.addStretch()
        layout.addWidget(self.notification_button)
        layout.addWidget(self.settings_button)

    def refresh_user(self):
        pass