from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget, QLabel

from ui.navigation.sidebar import Sidebar
from ui.navigation.topbar import Topbar


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

        dashboard_placeholder = QLabel("Dashboard em desenvolvimento")
        dashboard_placeholder.setObjectName("pagePlaceholder")

        self.pages.addWidget(dashboard_placeholder)

        content_layout.addWidget(self.topbar)
        content_layout.addWidget(self.pages)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(content_area)