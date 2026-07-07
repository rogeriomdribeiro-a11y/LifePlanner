import sys

from PySide6.QtWidgets import QApplication

from database.connection import get_connection
from database.schema import create_tables
from styles.theme import get_theme
from ui.main_window import MainWindow


class LifePlannerApp:
    def __init__(self):
        self.qt_app = QApplication(sys.argv)
        self.qt_app.setStyleSheet(get_theme())

        self.connection = get_connection()
        create_tables(self.connection)

        self.current_window = None

    def show_login(self):
        self.close_current_window()

        self.current_window = MainWindow(app_controller=self)
        self.current_window.maximize_custom()
        self.current_window.show()

    def close_current_window(self):
        if self.current_window is not None:
            self.current_window.close()
            self.current_window = None

    def run(self):
        self.show_login()
        sys.exit(self.qt_app.exec())