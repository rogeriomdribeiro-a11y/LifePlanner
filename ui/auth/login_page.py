"""Ecrã de autenticação local e através do Google."""

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
from app.session import Session
from database.user_repository import UserRepository
from services.google_auth_service import GoogleAuthService
from ui.base.base_page import BasePage
from ui.dialogs.custom_dialog import CustomDialog
from ui.widgets.button import LPButton, LPGoogleButton
from ui.widgets.line_edit import LPLineEdit, LPPasswordEdit
from ui.widgets.separator import LPSeparator


class LoginPage(BasePage):
    """Apresentar o formulário de login e iniciar a sessão do utilizador."""

    def __init__(self, app_controller=None):
        super().__init__()
        self.app_controller = app_controller
        self.setObjectName("loginWindow")
        self.setup_ui()

    def setup_ui(self):
        """Construir os painéis visual e funcional do ecrã de login."""
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

        welcome = QLabel("Bem-vindo!")
        welcome.setObjectName("loginWelcome")

        description = QLabel(
            "Inicia sessão para aceder ao\n"
            "teu espaço pessoal e continuar\n"
            "a alcançar os teus objetivos"
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
        layout.setContentsMargins(48, 42, 48, 42)
        layout.setSpacing(14)

        title = QLabel("Iniciar sessão")
        title.setObjectName("loginTitle")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Utiliza a tua conta Google ou os teus dados locais")
        subtitle.setObjectName("loginSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        google_button = LPGoogleButton()
        google_button.clicked.connect(self.handle_google_login)

        self.email_input = LPLineEdit("Email")
        self.password_input = LPPasswordEdit("Password")
        self.email_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)

        login_button = LPButton("Login")
        login_button.clicked.connect(self.handle_login)

        register_link = QPushButton("Ainda não tens conta? Criar conta")
        register_link.setObjectName("textLinkButton")
        register_link.setCursor(Qt.PointingHandCursor)
        register_link.clicked.connect(self.go_to_register)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(8)
        layout.addWidget(google_button, alignment=Qt.AlignHCenter)
        layout.addSpacing(22)
        layout.addWidget(LPSeparator("ou"))
        layout.addSpacing(14)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addSpacing(32)
        layout.addWidget(login_button, alignment=Qt.AlignHCenter)
        layout.addWidget(register_link, alignment=Qt.AlignHCenter)
        layout.addStretch()
        return panel

    def handle_login(self):
        """Validar as credenciais locais e abrir a área autenticada."""
        email = self.email_input.text().strip().lower()
        password = self.password_input.text()

        if not email or not password:
            CustomDialog.warning(
                self,
                "Preenche todos os campos.",
                "Campos obrigatórios",
            )
            return

        repository = UserRepository()
        success, message, user = repository.authenticate_user(email, password)

        if not success:
            CustomDialog.error(self, message, "Erro no login")
            return

        Session.login(user)
        self.reset_form()

        if self.app_controller:
            self.app_controller.show_dashboard()

    def handle_google_login(self):
        """Executar o OAuth, persistir a conta e abrir a área autenticada."""
        success, message, google_user = GoogleAuthService().authenticate()

        if not success:
            CustomDialog.error(self, message, "Erro no login Google")
            return

        repository = UserRepository()
        success, message, user = repository.get_or_create_google_user(google_user)

        if not success:
            CustomDialog.error(self, message, "Erro no login Google")
            return

        Session.login(user)
        self.reset_form()

        if self.app_controller:
            self.app_controller.show_dashboard()

    def reset_form(self):
        """Limpar credenciais que não devem permanecer visíveis no formulário."""
        self.email_input.clear()
        self.password_input.clear()
        self.email_input.setFocus()

    def go_to_register(self):
        if self.app_controller:
            self.app_controller.show_register()
