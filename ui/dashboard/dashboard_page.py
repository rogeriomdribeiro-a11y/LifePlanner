from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from app.session import Session


class DashboardPage(QWidget):
    def __init__(self, app_controller=None):
        super().__init__()

        self.app_controller = app_controller
        self.setObjectName("dashboardPage")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(80, 80, 80, 80)
        layout.setSpacing(20)

        user = Session.current_user
        name = user["full_name"] if user else "Utilizador"

        title = QLabel(f"Olá, {name}! 👋")
        title.setObjectName("dashboardTitle")

        subtitle = QLabel("Bem-vindo ao LifePlanner.")
        subtitle.setObjectName("dashboardSubtitle")

        logout_button = QPushButton("Logout")
        logout_button.setObjectName("lpButton")
        logout_button.clicked.connect(self.logout)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()
        layout.addWidget(logout_button, alignment=Qt.AlignLeft)

    def logout(self):
        Session.logout()

        if self.app_controller:
            self.app_controller.show_login()