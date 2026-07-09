from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QPixmap, QPainter, QIcon
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QPushButton,
    QGraphicsDropShadowEffect,
    QSizePolicy,
)

from app.path import ICONS_DIR


class NoteFormDialog(QDialog):
    COLORS = {
        "Roxo": "#8B5CF6",
        "Azul": "#3B82F6",
        "Verde": "#10B981",
        "Laranja": "#F59E0B",
        "Vermelho": "#EF4444",
    }

    CATEGORIES = [
        "Geral",
        "Pessoal",
        "Trabalho",
        "Estudo",
        "Ideias",
    ]

    def __init__(self, parent=None, note=None):
        super().__init__(parent)

        self.note_data = note

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)
        self.setFixedSize(660, 700)

        wrapper_layout = QVBoxLayout(self)
        wrapper_layout.setContentsMargins(15, 15, 15, 15)

        container = QFrame()
        container.setObjectName("noteDialogContainer")

        shadow = QGraphicsDropShadowEffect(container)
        shadow.setBlurRadius(35)
        shadow.setOffset(0, 5)
        shadow.setColor(QColor(0, 0, 0, 150))
        container.setGraphicsEffect(shadow)

        wrapper_layout.addWidget(container)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(28, 26, 28, 26)
        layout.setSpacing(14)

        title_text = "Editar nota" if note else "Nova nota"

        title = QLabel(title_text)
        title.setObjectName("noteDialogTitle")

        subtitle = QLabel("Guarda ideias, lembretes e informação importante.")
        subtitle.setObjectName("noteDialogSubtitle")

        self.error_label = QLabel("")
        self.error_label.setObjectName("noteDialogError")

        self.title_input = QLineEdit()
        self.title_input.setObjectName("noteDialogInput")
        self.title_input.setPlaceholderText("Ex: Ideias para o projeto")

        self.content_input = QTextEdit()
        self.content_input.setObjectName("noteDialogTextEdit")
        self.content_input.setPlaceholderText("Escreve aqui a tua nota...")
        self.content_input.setFixedHeight(190)
        self.content_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        row = QHBoxLayout()
        row.setSpacing(14)

        self.category_input = QComboBox()
        self.category_input.setObjectName("noteDialogCombo")
        self.category_input.addItems(self.CATEGORIES)
        self.category_input.setFixedWidth(240)

        self.color_input = QComboBox()
        self.color_input.setObjectName("noteDialogCombo")
        self.color_input.setFixedWidth(240)
        self.color_input.setIconSize(QSize(14, 14))

        for color_name, color_value in self.COLORS.items():
            self.color_input.addItem(
                self.create_color_icon(color_value),
                color_name
            )

        row.addLayout(self.create_field("Categoria", self.category_input))
        row.addLayout(self.create_field("Cor", self.color_input))
        row.addStretch()

        self.pin_button = QPushButton()
        self.pin_button.setObjectName("notePinToggleButton")
        self.pin_button.setCursor(Qt.PointingHandCursor)
        self.pin_button.setCheckable(True)
        self.pin_button.setFixedHeight(40)
        self.pin_button.clicked.connect(self.update_pin_button)

        buttons = QHBoxLayout()
        buttons.setSpacing(10)
        buttons.addStretch()

        cancel_button = QPushButton("Cancelar")
        cancel_button.setObjectName("noteDialogCancelButton")
        cancel_button.setCursor(Qt.PointingHandCursor)
        cancel_button.setFixedSize(130, 40)
        cancel_button.clicked.connect(self.reject)

        save_text = "Guardar alterações" if note else "Criar nota"

        save_button = QPushButton(save_text)
        save_button.setObjectName("noteDialogPrimaryButton")
        save_button.setCursor(Qt.PointingHandCursor)
        save_button.setFixedSize(170, 40)
        save_button.clicked.connect(self.validate_and_accept)

        buttons.addWidget(cancel_button)
        buttons.addWidget(save_button)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(4)
        layout.addLayout(self.create_field("Título", self.title_input))
        layout.addLayout(self.create_field("Conteúdo", self.content_input))
        layout.addSpacing(12)
        layout.addLayout(row)
        layout.addWidget(self.pin_button, alignment=Qt.AlignLeft)
        layout.addWidget(self.error_label)
        layout.addStretch()
        layout.addLayout(buttons)

        self.load_data()
        self.update_pin_button()

    def create_field(self, label_text, widget):
        field_layout = QVBoxLayout()
        field_layout.setSpacing(6)

        label = QLabel(label_text)
        label.setObjectName("noteDialogFieldLabel")

        field_layout.addWidget(label)
        field_layout.addWidget(widget)

        return field_layout

    def create_color_icon(self, color_value):
        pixmap = QPixmap(14, 14)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(color_value))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(1, 1, 12, 12)
        painter.end()

        return QIcon(pixmap)

    def load_data(self):
        if not self.note_data:
            self.category_input.setCurrentText("Geral")
            self.color_input.setCurrentText("Roxo")
            self.pin_button.setChecked(False)
            return

        self.title_input.setText(self.note_data["title"] or "")
        self.content_input.setPlainText(self.note_data["content"] or "")
        self.category_input.setCurrentText(self.note_data["category"] or "Geral")
        self.pin_button.setChecked(bool(self.note_data["is_pinned"]))

        color_name = self.get_color_name(self.note_data["color"] or "#8B5CF6")
        self.color_input.setCurrentText(color_name)

    def update_pin_button(self):
        if self.pin_button.isChecked():
            self.pin_button.setText(" Desafixar nota")
            self.pin_button.setIcon(
                QIcon(str(ICONS_DIR / "actions" / "unpin.svg"))
            )
        else:
            self.pin_button.setText(" Fixar nota")
            self.pin_button.setIcon(
                QIcon(str(ICONS_DIR / "actions" / "pin.svg"))
            )

        self.pin_button.setIconSize(QSize(18, 18))

    def validate_and_accept(self):
        if not self.title_input.text().strip():
            self.error_label.setText("O título da nota é obrigatório.")
            return

        self.accept()

    def get_color_name(self, color_value):
        for name, value in self.COLORS.items():
            if value.lower() == color_value.lower():
                return name

        return "Roxo"

    def get_data(self):
        color_name = self.color_input.currentText()

        return {
            "title": self.title_input.text().strip(),
            "content": self.content_input.toPlainText().strip(),
            "category": self.category_input.currentText(),
            "color": self.COLORS.get(color_name, "#8B5CF6"),
            "is_pinned": self.pin_button.isChecked(),
        }