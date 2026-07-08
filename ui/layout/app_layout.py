from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget

from ui.navigation.sidebar import Sidebar
from ui.navigation.topbar import Topbar

from ui.dashboard.dashboard_page import DashboardPage
from ui.calendar.calendar_page import CalendarPage
from ui.tasks.tasks_page import TasksPage
from ui.notes.notes_page import NotesPage
from ui.goals.goals_page import GoalsPage
from ui.reminders.reminders_page import RemindersPage
from ui.reports.reports_page import ReportsPage
from ui.settings.settings_page import SettingsPage


class AppLayout(QWidget):
    def __init__(self, app_controller=None):
        super().__init__()

        self.app_controller = app_controller
        self.setObjectName("appLayout")

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = Sidebar(app_controller=self.app_controller)

        content_area = QWidget()
        content_area.setObjectName("contentArea")

        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.topbar = Topbar()

        self.pages = QStackedWidget()
        self.pages.setObjectName("contentStack")

        self.dashboard_page = DashboardPage()
        self.calendar_page = CalendarPage()
        self.tasks_page = TasksPage()
        self.notes_page = NotesPage()
        self.goals_page = GoalsPage()
        self.reminders_page = RemindersPage()
        self.reports_page = ReportsPage()
        self.settings_page = SettingsPage()

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.calendar_page)
        self.pages.addWidget(self.tasks_page)
        self.pages.addWidget(self.notes_page)
        self.pages.addWidget(self.goals_page)
        self.pages.addWidget(self.reminders_page)
        self.pages.addWidget(self.reports_page)
        self.pages.addWidget(self.settings_page)

        self.connect_sidebar_buttons()

        content_layout.addWidget(self.topbar)
        content_layout.addWidget(self.pages)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(content_area)

    def connect_sidebar_buttons(self):
        self.sidebar.dashboard_btn.clicked.connect(
            lambda: self.show_page(self.dashboard_page)
        )
        self.sidebar.calendar_btn.clicked.connect(
            lambda: self.show_page(self.calendar_page)
        )
        self.sidebar.tasks_btn.clicked.connect(
            lambda: self.show_page(self.tasks_page)
        )
        self.sidebar.notes_btn.clicked.connect(
            lambda: self.show_page(self.notes_page)
        )
        self.sidebar.goals_btn.clicked.connect(
            lambda: self.show_page(self.goals_page)
        )
        self.sidebar.reminders_btn.clicked.connect(
            lambda: self.show_page(self.reminders_page)
        )
        self.sidebar.reports_btn.clicked.connect(
            lambda: self.show_page(self.reports_page)
        )
        self.sidebar.settings_btn.clicked.connect(
            lambda: self.show_page(self.settings_page)
        )

    def show_page(self, page):
        self.pages.setCurrentWidget(page)