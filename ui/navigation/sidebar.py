"""Menu lateral da área autenticada."""

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout

from app.path import IMAGES_DIR
from app.session import Session
from ui.widgets.sidebar_button import LPSidebarButton


LOGO_PATH = IMAGES_DIR / "login" / "logo.png"


class Sidebar(QFrame):
    """Apresentar as opções de navegação e terminar a sessão."""

    def __init__(self, app_controller=None):
        super().__init__()
        self.app_controller = app_controller
        self.setObjectName("sidebar")
        self.setFixedWidth(230)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 28, 24, 24)
        layout.setSpacing(10)

        logo = QLabel()
        logo.setObjectName("sidebarLogo")
        logo.setAlignment(Qt.AlignCenter)

        if LOGO_PATH.exists():
            pixmap = QPixmap(str(LOGO_PATH)).scaled(
                180,
                75,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
            logo.setPixmap(pixmap)
        else:
            logo.setText("LifePlanner")

        layout.addWidget(logo)
        layout.addSpacing(28)

        self.dashboard_btn = LPSidebarButton("Dashboard", "dashboard.svg")
        self.calendar_btn = LPSidebarButton("Calendário", "calendar.svg")
        self.tasks_btn = LPSidebarButton("Tarefas", "tasks.svg")
        self.notes_btn = LPSidebarButton("Notas", "notes.svg")
        self.goals_btn = LPSidebarButton("Objetivos", "goals.svg")
        self.reports_btn = LPSidebarButton("Relatórios", "reports.svg")
        self.settings_btn = LPSidebarButton("Definições", "settings.svg")
        self.logout_btn = LPSidebarButton("Logout", "logout.svg")

        self.menu_buttons = [
            self.dashboard_btn,
            self.calendar_btn,
            self.tasks_btn,
            self.notes_btn,
            self.goals_btn,
            self.reports_btn,
            self.settings_btn,
        ]

        for button in self.menu_buttons[:-1]:
            layout.addWidget(button)

        layout.addStretch()
        layout.addWidget(self.settings_btn)
        layout.addWidget(self.logout_btn)

        for button in self.menu_buttons:
            button.clicked.connect(
                lambda checked=False, active=button: self.set_active_button(active)
            )

        self.logout_btn.clicked.connect(self.logout)
        self.set_active_button(self.dashboard_btn)

    def set_active_button(self, active_button):
        """Manter apenas uma opção visualmente selecionada."""
        for button in self.menu_buttons:
            button.setChecked(button is active_button)

    def logout(self):
        """Limpar a sessão e regressar ao ecrã de login."""
        Session.logout()
        if self.app_controller:
            self.app_controller.show_login()
