from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel

from app.session import Session
from ui.widgets.sidebar_button import LPSidebarButton


BASE_DIR = Path(__file__).resolve().parents[2]
LOGO_PATH = BASE_DIR / "assets" / "images" / "login" / "logo.png"


class Sidebar(QFrame):
    def __init__(self, app_controller=None):
        super().__init__()

        self.app_controller = app_controller

        self.setObjectName("sidebar")
        self.setFixedWidth(230)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 28, 24, 24)
        layout.setSpacing(10)

        # Logo
        logo = QLabel()
        logo.setObjectName("sidebarLogo")
        logo.setAlignment(Qt.AlignCenter)

        if LOGO_PATH.exists():
            pixmap = QPixmap(str(LOGO_PATH))
            pixmap = pixmap.scaled(
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

        # Menu principal
        self.dashboard_btn = LPSidebarButton("Dashboard", "dashboard.svg")
        self.calendar_btn = LPSidebarButton("Calendário", "calendar.svg")
        self.tasks_btn = LPSidebarButton("Tarefas", "tasks.svg")
        self.notes_btn = LPSidebarButton("Notas", "notes.svg")
        self.goals_btn = LPSidebarButton("Objetivos", "goals.svg")
        self.reports_btn = LPSidebarButton("Relatórios", "reports.svg")

        # Menu inferior
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

        layout.addWidget(self.dashboard_btn)
        layout.addWidget(self.calendar_btn)
        layout.addWidget(self.tasks_btn)
        layout.addWidget(self.notes_btn)
        layout.addWidget(self.goals_btn)
        layout.addWidget(self.reports_btn)

        layout.addStretch()

        layout.addWidget(self.settings_btn)
        layout.addWidget(self.logout_btn)

        self.dashboard_btn.setChecked(True)

        self.dashboard_btn.clicked.connect(
            lambda: self.set_active_button(self.dashboard_btn)
        )
        self.calendar_btn.clicked.connect(
            lambda: self.set_active_button(self.calendar_btn)
        )
        self.tasks_btn.clicked.connect(
            lambda: self.set_active_button(self.tasks_btn)
        )
        self.notes_btn.clicked.connect(
            lambda: self.set_active_button(self.notes_btn)
        )
        self.goals_btn.clicked.connect(
            lambda: self.set_active_button(self.goals_btn)
        )
        self.reports_btn.clicked.connect(
            lambda: self.set_active_button(self.reports_btn)
        )
        self.settings_btn.clicked.connect(
            lambda: self.set_active_button(self.settings_btn)
        )

        self.logout_btn.clicked.connect(self.logout)

    def set_active_button(self, active_button):
        for button in self.menu_buttons:
            button.setChecked(False)

        active_button.setChecked(True)

    def logout(self):
        Session.logout()

        if self.app_controller:
            self.app_controller.show_login()