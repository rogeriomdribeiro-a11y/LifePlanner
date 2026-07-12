from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QDialog,
    QGraphicsDropShadowEffect,
)

from app.session import Session
from database.user_repository import UserRepository
from ui.dialogs.custom_dialog import CustomDialog
from ui.widgets.line_edit import LPPasswordEdit


class ChangePasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)
        self.setFixedSize(560, 430)

        wrapper_layout = QVBoxLayout(self)
        wrapper_layout.setContentsMargins(15, 15, 15, 15)

        container = QFrame()
        container.setObjectName("settingsDialogContainer")

        shadow = QGraphicsDropShadowEffect(container)
        shadow.setBlurRadius(35)
        shadow.setOffset(0, 5)
        shadow.setColor(QColor(0, 0, 0, 150))
        container.setGraphicsEffect(shadow)

        wrapper_layout.addWidget(container)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(28, 26, 28, 26)
        layout.setSpacing(14)

        title = QLabel("Alterar password")
        title.setObjectName("settingsDialogTitle")

        subtitle = QLabel("Confirma a password atual e define uma nova password.")
        subtitle.setObjectName("settingsDialogSubtitle")
        subtitle.setWordWrap(True)

        self.error_label = QLabel("")
        self.error_label.setObjectName("settingsDialogError")
        self.error_label.setFixedHeight(18)

        self.current_password_input = LPPasswordEdit("Password atual")
        self.new_password_input = LPPasswordEdit("Nova password")
        self.confirm_password_input = LPPasswordEdit("Confirmar nova password")

        buttons = QHBoxLayout()
        buttons.setSpacing(10)
        buttons.addStretch()

        cancel_button = QPushButton("Cancelar")
        cancel_button.setObjectName("settingsDialogCancelButton")
        cancel_button.setCursor(Qt.PointingHandCursor)
        cancel_button.setFixedSize(130, 40)
        cancel_button.clicked.connect(self.reject)

        save_button = QPushButton("Alterar password")
        save_button.setObjectName("settingsDialogPrimaryButton")
        save_button.setCursor(Qt.PointingHandCursor)
        save_button.setFixedSize(170, 40)
        save_button.clicked.connect(self.validate_and_accept)

        buttons.addWidget(cancel_button)
        buttons.addWidget(save_button)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(4)
        layout.addWidget(self.current_password_input)
        layout.addWidget(self.new_password_input)
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(self.error_label)
        layout.addStretch()
        layout.addLayout(buttons)

    def validate_and_accept(self):
        current_password = self.current_password_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not current_password or not new_password or not confirm_password:
            self.error_label.setText("Preenche todos os campos.")
            return

        if len(new_password) < 6:
            self.error_label.setText("A nova password deve ter pelo menos 6 caracteres.")
            return

        if new_password != confirm_password:
            self.error_label.setText("As novas passwords não coincidem.")
            return

        self.accept()

    def get_data(self):
        return {
            "current_password": self.current_password_input.text(),
            "new_password": self.new_password_input.text(),
        }


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("settingsPage")

        self.user_repository = UserRepository()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        scroll_area = QScrollArea()
        scroll_area.setObjectName("settingsScrollArea")
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        content = QWidget()
        content.setObjectName("settingsContent")

        self.layout = QVBoxLayout(content)
        self.layout.setContentsMargins(40, 32, 40, 40)
        self.layout.setSpacing(22)

        scroll_area.setWidget(content)
        main_layout.addWidget(scroll_area)

        self.create_header()
        self.create_user_section()
        self.create_security_section()
        self.create_preferences_section()
        self.create_app_section()

    def create_header(self):
        title = QLabel("Definições")
        title.setObjectName("contentPageTitle")

        subtitle = QLabel("Gere os teus dados, segurança e preferências da aplicação.")
        subtitle.setObjectName("contentPageSubtitle")

        self.layout.addWidget(title)
        self.layout.addWidget(subtitle)

    def create_user_section(self):
        section = self.create_section("Utilizador")

        self.name_input = QLineEdit()
        self.name_input.setObjectName("settingsInput")
        self.name_input.setPlaceholderText("Nome completo")
        self.name_input.setFixedHeight(40)

        self.email_input = QLineEdit()
        self.email_input.setObjectName("settingsInputReadOnly")
        self.email_input.setReadOnly(True)
        self.email_input.setFixedHeight(40)

        name_row = self.create_field_row("Nome completo", self.name_input)
        email_row = self.create_field_row("Email", self.email_input)

        save_button = QPushButton("Guardar alterações")
        save_button.setObjectName("settingsPrimaryButton")
        save_button.setCursor(Qt.PointingHandCursor)
        save_button.setFixedSize(170, 40)
        save_button.clicked.connect(self.save_user_name)

        button_row = QHBoxLayout()
        button_row.addStretch()
        button_row.addWidget(save_button)

        section.addLayout(name_row)
        section.addLayout(email_row)
        section.addSpacing(8)
        section.addLayout(button_row)

    def create_security_section(self):
        section = self.create_section("Segurança")

        row = QHBoxLayout()
        row.setSpacing(12)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)

        title = QLabel("Alterar password")
        title.setObjectName("settingsRowTitle")

        subtitle = QLabel("Atualiza a password da tua conta local.")
        subtitle.setObjectName("settingsRowSubtitle")

        text_layout.addWidget(title)
        text_layout.addWidget(subtitle)

        change_button = QPushButton("Alterar password")
        change_button.setObjectName("settingsSecondaryButton")
        change_button.setCursor(Qt.PointingHandCursor)
        change_button.setFixedSize(160, 40)
        change_button.clicked.connect(self.open_change_password_dialog)

        row.addLayout(text_layout)
        row.addStretch()
        row.addWidget(change_button)

        section.addLayout(row)

    def create_preferences_section(self):
        section = self.create_section("Preferências")

        row = QHBoxLayout()
        row.setSpacing(12)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)

        title = QLabel("Tema da aplicação")
        title.setObjectName("settingsRowTitle")

        subtitle = QLabel("Tema atual: Escuro")
        subtitle.setObjectName("settingsRowSubtitle")

        text_layout.addWidget(title)
        text_layout.addWidget(subtitle)

        theme_button = QPushButton("Alterar tema")
        theme_button.setObjectName("settingsSecondaryButton")
        theme_button.setCursor(Qt.PointingHandCursor)
        theme_button.setFixedSize(140, 40)
        theme_button.clicked.connect(self.theme_coming_next)

        row.addLayout(text_layout)
        row.addStretch()
        row.addWidget(theme_button)

        section.addLayout(row)

    def create_app_section(self):
        section = self.create_section("Aplicação")

        section.addLayout(self.create_info_row("Nome", "LifePlanner"))
        section.addLayout(self.create_info_row("Versão", "1.0"))
        section.addLayout(self.create_info_row("Ano", "2026"))

    def create_section(self, title_text):
        card = QFrame()
        card.setObjectName("settingsSectionCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(22, 20, 22, 22)
        layout.setSpacing(16)

        title = QLabel(title_text)
        title.setObjectName("settingsSectionTitle")

        layout.addWidget(title)

        self.layout.addWidget(card)

        return layout

    def create_field_row(self, label_text, widget):
        row = QHBoxLayout()
        row.setSpacing(16)

        label = QLabel(label_text)
        label.setObjectName("settingsFieldLabel")
        label.setFixedWidth(150)

        row.addWidget(label)
        row.addWidget(widget)

        return row

    def create_info_row(self, label_text, value_text):
        row = QHBoxLayout()
        row.setSpacing(16)

        label = QLabel(label_text)
        label.setObjectName("settingsFieldLabel")

        value = QLabel(value_text)
        value.setObjectName("settingsInfoValue")
        value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        row.addWidget(label)
        row.addStretch()
        row.addWidget(value)

        return row

    def refresh(self):
        user = Session.current_user

        if not user:
            return

        self.name_input.setText(user["full_name"] or "")
        self.email_input.setText(user["email"] or "")

    def save_user_name(self):
        user = Session.current_user

        if not user:
            return

        full_name = self.name_input.text().strip()

        success, message = self.user_repository.update_full_name(
            user["id"],
            full_name,
        )

        if not success:
            CustomDialog.warning(
                self,
                message,
                "Não foi possível atualizar",
            )
            return

        updated_user = self.user_repository.get_user_by_id(user["id"])

        if updated_user:
            Session.login(updated_user)

        CustomDialog.success(
            self,
            message,
            "Dados atualizados",
        )

    def open_change_password_dialog(self):
        user = Session.current_user

        if not user:
            return

        dialog = ChangePasswordDialog(self)

        if dialog.exec() != QDialog.Accepted:
            return

        data = dialog.get_data()

        success, message = self.user_repository.change_password(
            user["id"],
            data["current_password"],
            data["new_password"],
        )

        if not success:
            CustomDialog.warning(
                self,
                message,
                "Password não alterada",
            )
            return

        CustomDialog.success(
            self,
            message,
            "Password alterada",
        )

    def theme_coming_next(self):
        CustomDialog.info(
            self,
            "A alteração de tema será implementada no próximo passo.",
            "Tema da aplicação",
        )