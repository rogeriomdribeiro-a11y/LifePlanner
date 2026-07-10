from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
     QHBoxLayout, QVBoxLayout, QLabel,
     QPushButton, QFrame
)

from app.constants import (
    LEFT_PANEL_WIDTH,
    LEFT_PANEL_HEIGHT,
    RIGHT_PANEL_WIDTH,
    RIGHT_PANEL_HEIGHT,
    LOGO_WIDTH,
    LOGO_HEIGHT,
    ILLUSTRATION_WIDTH,
    ILLUSTRATION_HEIGHT
)
from ui.widgets.button import LPButton, LPGoogleButton
from ui.widgets.line_edit import LPLineEdit, LPPasswordEdit
from ui.widgets.separator import LPSeparator
from ui.base.base_page import BasePage
from database.user_repository import UserRepository
from ui.dialogs.custom_dialog import CustomDialog
from app.session import Session

class LoginPage(BasePage):
    def __init__(self, app_controller=None):
        super().__init__()

        self.app_controller = app_controller

        self.setObjectName("loginWindow")
       
        

        self.old_pos = None

        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(78, 28, 78, 36)
        main_layout.setSpacing(176)

        main_layout.addWidget(self.create_left_panel())
        main_layout.addWidget(
            self.create_right_panel(),
            alignment=Qt.AlignVCenter
        )

    def create_left_panel(self):
        panel = QFrame()
        panel.setObjectName("loginPanel")
        panel.setFixedSize(
            LEFT_PANEL_WIDTH,
            LEFT_PANEL_HEIGHT
        )

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(36, 20, 36, 38)
        layout.setSpacing(18)

        logo = self.image_label(
            "logo.png",
            LOGO_WIDTH,
            LOGO_HEIGHT
        )
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

        illustration = self.image_label(
            "login_illustration.png",
            ILLUSTRATION_WIDTH,
            ILLUSTRATION_HEIGHT
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
        panel.setFixedSize(
            RIGHT_PANEL_WIDTH,
            RIGHT_PANEL_HEIGHT
        )

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(48, 42, 48, 42)
        layout.setSpacing(14)

        title = QLabel("Iniciar sessão")
        title.setObjectName("loginTitle")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Utilize a sua conta Google para continuar")
        subtitle.setObjectName("loginSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        google_button = LPGoogleButton()

        separator = LPSeparator("ou")

        self.email_input = LPLineEdit("Email")
        self.password_input = LPPasswordEdit("Password")

        recover = QLabel("Recuperar password")
        recover.setObjectName("recoverPassword")
        recover.setAlignment(Qt.AlignRight)

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
        layout.addWidget(separator)
        layout.addSpacing(14)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(recover)
        layout.addSpacing(32)
        layout.addWidget(login_button, alignment=Qt.AlignHCenter)
        layout.addWidget(register_link, alignment=Qt.AlignHCenter)
        layout.addStretch()

        return panel

    def handle_login(self):
        email = self.email_input.text().strip().lower()
        password = self.password_input.text()

        if not email or not password:
            CustomDialog.warning(
                self,
                "Preencha todos os campos.",
                "Campos obrigatórios"
            )
            return

        repository = UserRepository()

        success, message, user = repository.authenticate_user(
            email,
            password
        )

        if not success:
            CustomDialog.error(
                self,
                message,
                "Erro no login"
            )
            return


        Session.login(user)

        if self.app_controller:
            self.app_controller.show_dashboard()

    def go_to_register(self):
        if self.app_controller:
            self.app_controller.show_register()