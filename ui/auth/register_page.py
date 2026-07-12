from pathlib import Path

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
)

from app.constants import (
    LEFT_PANEL_WIDTH,
    LEFT_PANEL_HEIGHT,
    RIGHT_PANEL_WIDTH,
    RIGHT_PANEL_HEIGHT,
    LOGO_WIDTH,
    LOGO_HEIGHT,
    ILLUSTRATION_WIDTH,
    ILLUSTRATION_HEIGHT,
)
from ui.widgets.button import LPButton
from ui.widgets.line_edit import LPLineEdit, LPPasswordEdit
from database.user_repository import UserRepository
from ui.base.base_page import BasePage
from ui.dialogs.custom_dialog import CustomDialog


BASE_DIR = Path(__file__).resolve().parents[2]
IMAGES_DIR = BASE_DIR / "assets" / "images" / "login"


class RegisterPage(BasePage):
    def __init__(self, app_controller=None):
        super().__init__()

        self.app_controller = app_controller

        self.setObjectName("loginWindow")
        self.setWindowTitle("LifePlanner - Criar Conta")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMinimumSize(1280, 720)

        self.old_pos = None

        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(78, 28, 78, 36)
        main_layout.setSpacing(176)

        main_layout.addWidget(self.create_left_panel())
        main_layout.addWidget(
            self.create_right_panel(),
            alignment=Qt.AlignVCenter,
        )

    def create_left_panel(self):
        panel = QFrame()
        panel.setObjectName("loginPanel")
        panel.setFixedSize(LEFT_PANEL_WIDTH, LEFT_PANEL_HEIGHT)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(36, 20, 36, 38)
        layout.setSpacing(18)

        logo = self.image_label("logo.png", LOGO_WIDTH, LOGO_HEIGHT)
        logo.setAlignment(Qt.AlignLeft)

        welcome = QLabel("Cria a tua conta!")
        welcome.setObjectName("loginWelcome")

        description = QLabel(
            "Começa a organizar o teu dia\n"
            "com tarefas, eventos, notas\n"
            "e objetivos num só lugar"
        )
        description.setObjectName("loginDescription")
        description.setWordWrap(True)

        illustration = self.image_label(
            "login_illustration.png",
            ILLUSTRATION_WIDTH,
            ILLUSTRATION_HEIGHT,
        )

        layout.addWidget(logo)
        layout.addSpacing(22)
        layout.addWidget(welcome)
        layout.addWidget(description)
        layout.addStretch()
        layout.addWidget(illustration, alignment=Qt.AlignCenter)

        return panel

    def create_right_panel(self):
        panel = QFrame()
        panel.setObjectName("loginPanel")
        panel.setFixedSize(RIGHT_PANEL_WIDTH, RIGHT_PANEL_HEIGHT)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(48, 38, 48, 38)
        layout.setSpacing(12)

        title = QLabel("Criar conta")
        title.setObjectName("loginTitle")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Preenche os dados para criar a tua conta")
        subtitle.setObjectName("loginSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        self.name_input = LPLineEdit("Nome completo")
        self.email_input = LPLineEdit("Email")
        self.password_input = LPPasswordEdit("Password")
        self.confirm_password_input = LPPasswordEdit("Confirmar password")

        create_button = LPButton("Criar")
        create_button.clicked.connect(self.handle_register)

        login_link = QPushButton("Já tens conta? Iniciar sessão")
        login_link.setObjectName("textLinkButton")
        login_link.setCursor(Qt.PointingHandCursor)
        login_link.clicked.connect(self.go_to_login)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(18)
        layout.addWidget(self.name_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.confirm_password_input)
        layout.addSpacing(24)
        layout.addWidget(create_button, alignment=Qt.AlignHCenter)
        layout.addSpacing(10)
        layout.addWidget(login_link, alignment=Qt.AlignHCenter)
        layout.addStretch()

        return panel

    def handle_register(self):
        full_name = self.name_input.text().strip()
        email = self.email_input.text().strip().lower()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not full_name or not email or not password or not confirm_password:
            CustomDialog.warning(
                self,
                "Preenche todos os campos para criar a tua conta.",
                "Campos obrigatórios",
            )
            return

        if "@" not in email or "." not in email:
            CustomDialog.warning(
                self,
                "Introduz um email válido.",
                "Email inválido",
            )
            return

        if password != confirm_password:
            CustomDialog.warning(
                self,
                "As passwords não coincidem.",
                "Password inválida",
            )
            return

        repository = UserRepository()

        success, message = repository.create_user(
            full_name,
            email,
            password,
        )

        if not success:
            CustomDialog.error(
                self,
                message,
                "Erro ao criar conta",
            )
            return

        CustomDialog.success(
            self,
            message,
            "Conta criada",
        )

        self.go_to_login()

    def go_to_login(self):
        if self.app_controller:
            self.app_controller.show_login()

    def image_label(self, filename, width, height):
        label = QLabel()
        label.setFixedSize(width, height)
        label.setAlignment(Qt.AlignCenter)

        image_path = IMAGES_DIR / filename

        if image_path.exists():
            pixmap = QPixmap(str(image_path))
            pixmap = pixmap.scaled(
                width,
                height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
            label.setPixmap(pixmap)
        else:
            label.setText(f"Imagem não encontrada:\n{filename}")
            label.setStyleSheet("color: #EF4444;")

        return label