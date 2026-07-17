"""Ecrã de criação de contas locais."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from app.constants import (
    ILLUSTRATION_HEIGHT,
    ILLUSTRATION_WIDTH,
    LEFT_PANEL_HEIGHT,
    LEFT_PANEL_WIDTH,
    LOGO_HEIGHT,
    LOGO_WIDTH,
    RIGHT_PANEL_HEIGHT,
    RIGHT_PANEL_WIDTH,
)
from database.user_repository import UserRepository
from ui.base.base_page import BasePage
from ui.dialogs.custom_dialog import CustomDialog
from ui.widgets.button import LPButton
from ui.widgets.line_edit import LPLineEdit, LPPasswordEdit


class RegisterPage(BasePage):
    """Recolher, validar e guardar os dados de uma nova conta local."""

    def __init__(self, app_controller=None):
        super().__init__()
        self.app_controller = app_controller
        self.setObjectName("loginWindow")
        self.setup_ui()

    def setup_ui(self):
        """Construir os painéis do formulário de registo."""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(78, 28, 78, 36)
        main_layout.setSpacing(176)
        main_layout.addWidget(self.create_left_panel())
        main_layout.addWidget(self.create_right_panel(), alignment=Qt.AlignVCenter)

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

        for field in (
            self.name_input,
            self.email_input,
            self.password_input,
            self.confirm_password_input,
        ):
            field.returnPressed.connect(self.handle_register)

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
        """Validar o formulário e criar a conta na base de dados local."""
        full_name = self.name_input.text().strip()
        email = self.email_input.text().strip().lower()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not all((full_name, email, password, confirm_password)):
            CustomDialog.warning(
                self,
                "Preenche todos os campos para criar a tua conta.",
                "Campos obrigatórios",
            )
            return

        if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
            CustomDialog.warning(self, "Introduz um email válido.", "Email inválido")
            return

        if len(password) < 6:
            CustomDialog.warning(
                self,
                "A password deve ter pelo menos 6 caracteres.",
                "Password inválida",
            )
            return

        if password != confirm_password:
            CustomDialog.warning(
                self,
                "As passwords não coincidem.",
                "Password inválida",
            )
            return

        success, message = UserRepository().create_user(full_name, email, password)

        if not success:
            CustomDialog.error(self, message, "Erro ao criar conta")
            return

        CustomDialog.success(self, message, "Conta criada")
        self.reset_form()
        self.go_to_login()

    def reset_form(self):
        """Limpar todos os campos antes de uma nova utilização do ecrã."""
        self.name_input.clear()
        self.email_input.clear()
        self.password_input.clear()
        self.confirm_password_input.clear()
        self.name_input.setFocus()

    def go_to_login(self):
        if self.app_controller:
            self.app_controller.show_login()
