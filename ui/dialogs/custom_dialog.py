from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGraphicsDropShadowEffect,
)


BASE_DIR = Path(__file__).resolve().parents[2]
DIALOG_ICONS_DIR = BASE_DIR / "assets" / "icons" / "dialogs"


class CustomDialog(QDialog):
    def __init__(
        self,
        parent,
        title,
        message,
        dialog_type="info",
        button_text="OK",
        cancel_text=None,
        destructive=False,
    ):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)
        self.setFixedSize(420, 240)

        wrapper_layout = QVBoxLayout(self)
        wrapper_layout.setContentsMargins(15, 15, 15, 15)

        container = QFrame()
        container.setObjectName("dialogContainer")
        container.setFixedSize(390, 210)

        shadow = QGraphicsDropShadowEffect(container)
        shadow.setBlurRadius(35)
        shadow.setOffset(0, 5)
        shadow.setColor(QColor(0, 0, 0, 150))
        container.setGraphicsEffect(shadow)

        wrapper_layout.addWidget(container)

        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(28, 24, 28, 24)
        main_layout.setSpacing(10)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(14)

        icon = QSvgWidget(str(DIALOG_ICONS_DIR / f"{dialog_type}.svg"))
        icon.setFixedSize(34, 34)

        title_label = QLabel(title)
        title_label.setObjectName("dialogTitle")

        header_layout.addWidget(icon)
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        message_label = QLabel(message)
        message_label.setObjectName("dialogMessage")
        message_label.setWordWrap(True)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        buttons_layout.addStretch()

        if cancel_text:
            cancel_button = QPushButton(cancel_text)
            cancel_button.setObjectName("dialogCancelButton")
            cancel_button.setFixedSize(130, 38)
            cancel_button.setCursor(Qt.PointingHandCursor)
            cancel_button.clicked.connect(self.reject)

            buttons_layout.addWidget(cancel_button)

        button = QPushButton(button_text)
        button.setObjectName("dialogDangerButton" if destructive else "dialogButton")
        button.setFixedSize(140 if cancel_text else 150, 38)
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(self.accept)

        buttons_layout.addWidget(button)

        main_layout.addLayout(header_layout)
        main_layout.addWidget(message_label)
        main_layout.addStretch()
        main_layout.addLayout(buttons_layout)

    @staticmethod
    def success(parent, message, title="Sucesso", button_text="Continuar"):
        CustomDialog(
            parent,
            title,
            message,
            "success",
            button_text,
        ).exec()

    @staticmethod
    def error(parent, message, title="Erro", button_text="Fechar"):
        CustomDialog(
            parent,
            title,
            message,
            "error",
            button_text,
        ).exec()

    @staticmethod
    def warning(parent, message, title="Aviso", button_text="OK"):
        CustomDialog(
            parent,
            title,
            message,
            "warning",
            button_text,
        ).exec()

    @staticmethod
    def info(parent, message, title="Informação", button_text="OK"):
        CustomDialog(
            parent,
            title,
            message,
            "info",
            button_text,
        ).exec()

    @staticmethod
    def confirm(
        parent,
        message,
        title="Confirmar",
        button_text="Confirmar",
        cancel_text="Cancelar",
        dialog_type="warning",
        destructive=False,
    ):
        dialog = CustomDialog(
            parent,
            title,
            message,
            dialog_type,
            button_text,
            cancel_text,
            destructive,
        )

        return dialog.exec() == QDialog.Accepted