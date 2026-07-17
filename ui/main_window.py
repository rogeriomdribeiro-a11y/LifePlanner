"""Janela principal e navegação entre autenticação e área privada."""

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QPushButton, QStackedWidget, QVBoxLayout, QWidget

from app.resources import get_icon
from ui.auth.login_page import LoginPage
from ui.auth.register_page import RegisterPage
from ui.layout.app_layout import AppLayout


class MainWindow(QWidget):
    """Alojar todos os ecrãs e controlar a janela sem moldura do sistema."""

    def __init__(self, app_controller=None):
        super().__init__()
        self.app_controller = app_controller

        self.setObjectName("loginWindow")
        self.setWindowTitle("LifePlanner")
        self.setMinimumSize(1280, 720)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.old_pos = None
        self.is_window_maximized = True

        self.stack = QStackedWidget()
        self.login_page = LoginPage(app_controller=self)
        self.register_page = RegisterPage(app_controller=self)
        self.app_layout = AppLayout(app_controller=self)

        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.register_page)
        self.stack.addWidget(self.app_layout)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stack)

        self.create_window_buttons()
        self.show_login()

    def show_login(self):
        """Apresentar um formulário de login limpo."""
        self.login_page.reset_form()
        self.stack.setCurrentWidget(self.login_page)

    def show_register(self):
        """Apresentar o formulário de registo sem dados anteriores."""
        self.register_page.reset_form()
        self.stack.setCurrentWidget(self.register_page)

    def show_dashboard(self):
        """Repor o Dashboard como página inicial após cada autenticação."""
        self.app_layout.show_dashboard()
        self.stack.setCurrentWidget(self.app_layout)

    def create_window_buttons(self):
        """Criar os controlos próprios da janela sem moldura."""
        self.minimize_button = QPushButton(self)
        self.minimize_button.setObjectName("windowButton")
        self.minimize_button.setIcon(get_icon("window", "minimize.svg"))
        self.minimize_button.setIconSize(QSize(14, 14))
        self.minimize_button.setFixedSize(32, 32)
        self.minimize_button.setCursor(Qt.PointingHandCursor)
        self.minimize_button.clicked.connect(self.showMinimized)

        self.resize_button = QPushButton(self)
        self.resize_button.setObjectName("windowButton")
        self.resize_button.setIcon(get_icon("window", "maximize.svg"))
        self.resize_button.setIconSize(QSize(14, 14))
        self.resize_button.setFixedSize(32, 32)
        self.resize_button.setCursor(Qt.PointingHandCursor)
        self.resize_button.clicked.connect(self.toggle_window_size)

        self.close_button = QPushButton(self)
        self.close_button.setObjectName("closeButton")
        self.close_button.setIcon(get_icon("window", "close.svg"))
        self.close_button.setIconSize(QSize(14, 14))
        self.close_button.setFixedSize(32, 32)
        self.close_button.setCursor(Qt.PointingHandCursor)
        self.close_button.clicked.connect(self.close)

        self.position_window_buttons()

    def position_window_buttons(self):
        margin_right = 10
        top = 6
        spacing = 4

        close_x = self.width() - margin_right - self.close_button.width()
        resize_x = close_x - spacing - self.resize_button.width()
        minimize_x = resize_x - spacing - self.minimize_button.width()

        self.minimize_button.move(minimize_x, top)
        self.resize_button.move(resize_x, top)
        self.close_button.move(close_x, top)
        self.minimize_button.raise_()
        self.resize_button.raise_()
        self.close_button.raise_()

    def toggle_window_size(self):
        """Alternar entre a área útil do ecrã e o tamanho mínimo definido."""
        if self.is_window_maximized:
            self.restore_custom()
        else:
            self.maximize_custom()

    def maximize_custom(self):
        self.setGeometry(self.screen().availableGeometry())
        self.is_window_maximized = True

    def restore_custom(self):
        self.resize(1280, 720)

        screen_geometry = self.screen().availableGeometry()
        x = screen_geometry.x() + (screen_geometry.width() - self.width()) // 2
        y = screen_geometry.y() + (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
        self.is_window_maximized = False

    def resizeEvent(self, event):
        if hasattr(self, "close_button"):
            self.position_window_buttons()
        super().resizeEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.is_window_maximized:
            self.old_pos = event.globalPosition().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.old_pos is not None and not self.is_window_maximized:
            new_pos = event.globalPosition().toPoint()
            delta = new_pos - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = new_pos
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.old_pos = None
        super().mouseReleaseEvent(event)
