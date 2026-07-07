from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame
)
from app.constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    LEFT_PANEL_WIDTH,
    LEFT_PANEL_HEIGHT,
    LOGO_WIDTH,
    LOGO_HEIGHT,
    ILLUSTRATION_WIDTH,
    ILLUSTRATION_HEIGHT,
    RIGHT_PANEL_WIDTH,
    RIGHT_PANEL_HEIGHT
)
from PySide6.QtCore import Qt, QPoint


BASE_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = BASE_DIR / "assets" / "images" / "login"


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("loginWindow")
        self.setWindowTitle("LifePlanner")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.old_pos = None
        self.setMinimumSize(1280, 720)

        self.setup_ui()
        
    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(78, 28, 78, 36)
        main_layout.setSpacing(176)

        main_layout.addWidget(self.create_left_panel())
        main_layout.addWidget(self.create_right_panel(), alignment=Qt.AlignVCenter)

        self.create_window_buttons()

    def create_left_panel(self):
        panel = QFrame()
        panel.setObjectName("loginPanel")
        panel.setFixedSize(RIGHT_PANEL_WIDTH, RIGHT_PANEL_HEIGHT)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(36, 20, 36, 38)
        layout.setSpacing(18)

        logo = self.image_label("logo.png",LOGO_WIDTH,LOGO_HEIGHT)
        #logo = self.image_label("logo.png", 380, 120)
        logo.setAlignment(Qt.AlignLeft)
       

        welcome = QLabel("Bem vindo!")
        welcome.setObjectName("loginWelcome")

        description = QLabel(
            "Inicie sessão para aceder ao\n"
            "seu espaço pessoal e continuar\n"
            "a alcançar os seus objetivos"
        )
        description.setObjectName("loginDescription")
        description.setWordWrap(True)
        illustration = self.image_label("login_illustration.png", ILLUSTRATION_WIDTH, ILLUSTRATION_HEIGHT)
        illustration.setAlignment(Qt.AlignCenter)

        layout.addWidget(logo)
        layout.addSpacing(22)
        layout.addWidget(welcome)
        layout.addWidget(description)
        layout.addStretch()
        layout.addWidget(illustration)

        return panel

    def create_right_panel(self):
        panel = QFrame()
        panel.setObjectName("loginPanel")
        panel.setFixedSize(424, 550)


        


        layout = QVBoxLayout(panel)
        layout.setContentsMargins(48, 42, 48, 42)
        layout.setSpacing(14)

        title = QLabel("Iniciar sessão")
        title.setObjectName("loginTitle")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Utilize a sua conta Google para continuar")
        subtitle.setObjectName("loginSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        google_button = QPushButton("  Continuar com Google")
        google_button.setObjectName("googleButton")
        google_button.setCursor(Qt.PointingHandCursor)

        google_icon = IMAGES_DIR / "google.png"
        if google_icon.exists():
            google_button.setIcon(QPixmap(str(google_icon)))

        separator = QLabel("────────────  ou  ────────────")
        separator.setObjectName("separator")
        separator.setAlignment(Qt.AlignCenter)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("email")
        self.email_input.setFixedHeight(36)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(36)

        recover = QLabel("Recuperar password")
        recover.setObjectName("recoverPassword")
        recover.setAlignment(Qt.AlignRight)

        login_button = QPushButton("Login")
        login_button.setObjectName("loginButton")
        login_button.setFixedWidth(90)
        login_button.setCursor(Qt.PointingHandCursor)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(8)
        layout.addWidget(google_button)
        layout.addSpacing(22)
        layout.addWidget(separator)
        layout.addSpacing(14)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(recover)
        layout.addSpacing(32)
        layout.addWidget(login_button, alignment=Qt.AlignCenter)
        layout.addStretch()

        return panel

    def image_label(self, filename, width, height):
        label = QLabel()

        image_path = IMAGES_DIR / filename

        if image_path.exists():
            pixmap = QPixmap(str(image_path))
            pixmap = pixmap.scaled(
                width,
                height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            label.setPixmap(pixmap)
        else:
            label.setText(f"Imagem não encontrada:\n{filename}")
            label.setStyleSheet("color: #64748B;")

        return label
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos is not None:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

    def create_window_buttons(self):
        self.minimize_button = QPushButton(self)
        self.minimize_button.setObjectName("windowButton")
        self.minimize_button.setText("─")
        self.minimize_button.setFixedSize(34, 26)
        self.minimize_button.setCursor(Qt.PointingHandCursor)
        self.minimize_button.clicked.connect(self.showMinimized)

        self.close_button = QPushButton(self)
        self.close_button.setObjectName("closeButton")
        self.close_button.setText("×")
        self.close_button.setFixedSize(34, 26)
        self.close_button.setCursor(Qt.PointingHandCursor)
        self.close_button.clicked.connect(self.close)

        self.position_window_buttons()

    def position_window_buttons(self):
        margin_right = 10
        top = 6
        spacing = 4

        close_x = self.width() - margin_right - self.close_button.width()
        minimize_x = close_x - spacing - self.minimize_button.width()

        self.minimize_button.move(minimize_x, top)
        self.close_button.move(close_x, top)

    def resizeEvent(self, event):
        if hasattr(self, "close_button"):
            self.position_window_buttons()

        super().resizeEvent(event)