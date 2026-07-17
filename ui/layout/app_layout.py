"""Estrutura da área autenticada: menu lateral, topbar e páginas."""

from PySide6.QtWidgets import QHBoxLayout, QStackedWidget, QVBoxLayout, QWidget

from ui.calendar.calendar_page import CalendarPage
from ui.dashboard.dashboard_page import DashboardPage
from ui.goals.goals_page import GoalsPage
from ui.navigation.sidebar import Sidebar
from ui.navigation.topbar import Topbar
from ui.notes.notes_page import NotesPage
from ui.reports.reports_page import ReportsPage
from ui.settings.settings_page import SettingsPage
from ui.tasks.tasks_page import TasksPage


class AppLayout(QWidget):
    """Gerir a navegação e atualização das páginas da área privada."""

    def __init__(self, app_controller=None):
        super().__init__()
        self.app_controller = app_controller
        self.setObjectName("appLayout")

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = Sidebar(app_controller=self.app_controller)
        self.topbar = Topbar()
        self.pages = QStackedWidget()
        self.pages.setObjectName("contentStack")

        self.dashboard_page = DashboardPage()
        self.calendar_page = CalendarPage()
        self.tasks_page = TasksPage()
        self.notes_page = NotesPage()
        self.goals_page = GoalsPage()
        self.reports_page = ReportsPage()
        self.settings_page = SettingsPage()

        for page in (
            self.dashboard_page,
            self.calendar_page,
            self.tasks_page,
            self.notes_page,
            self.goals_page,
            self.reports_page,
            self.settings_page,
        ):
            self.pages.addWidget(page)

        self.connect_sidebar_buttons()

        content_area = QWidget()
        content_area.setObjectName("contentArea")
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        content_layout.addWidget(self.topbar)
        content_layout.addWidget(self.pages)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(content_area)

    def connect_sidebar_buttons(self):
        """Associar cada botão à página correspondente."""
        page_buttons = (
            (self.sidebar.dashboard_btn, self.dashboard_page),
            (self.sidebar.calendar_btn, self.calendar_page),
            (self.sidebar.tasks_btn, self.tasks_page),
            (self.sidebar.notes_btn, self.notes_page),
            (self.sidebar.goals_btn, self.goals_page),
            (self.sidebar.reports_btn, self.reports_page),
            (self.sidebar.settings_btn, self.settings_page),
        )

        for button, page in page_buttons:
            button.clicked.connect(lambda checked=False, target=page: self.show_page(target))

    def show_page(self, page):
        """Atualizar e apresentar a página selecionada."""
        if hasattr(page, "refresh"):
            page.refresh()
        self.pages.setCurrentWidget(page)

    def show_dashboard(self):
        """Repor o estado inicial da área privada após o login."""
        self.sidebar.set_active_button(self.sidebar.dashboard_btn)
        self.show_page(self.dashboard_page)

    def refresh(self):
        """Atualizar a página atualmente visível."""
        page = self.pages.currentWidget()
        if page and hasattr(page, "refresh"):
            page.refresh()
