from datetime import date

from PySide6.QtCore import Qt, QDate, QTime
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QDateEdit,
    QTimeEdit,
    QComboBox,
    QPushButton,
    QGraphicsDropShadowEffect,
)


class EventFormDialog(QDialog):
    COLORS = {
        "Azul": "#3B82F6",
        "Verde": "#10B981",
        "Roxo": "#8B5CF6",
        "Laranja": "#F59E0B",
        "Vermelho": "#EF4444",
    }

    def __init__(self, parent=None, selected_date=None, event=None):
        super().__init__(parent)

        self.event_data = event

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)
        self.setFixedSize(580, 520)

        wrapper_layout = QVBoxLayout(self)
        wrapper_layout.setContentsMargins(15, 15, 15, 15)

        container = QFrame()
        container.setObjectName("eventDialogContainer")

        shadow = QGraphicsDropShadowEffect(container)
        shadow.setBlurRadius(35)
        shadow.setOffset(0, 5)
        shadow.setColor(QColor(0, 0, 0, 150))
        container.setGraphicsEffect(shadow)

        wrapper_layout.addWidget(container)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(28, 26, 28, 26)
        layout.setSpacing(14)

        title_text = "Editar evento" if event else "Novo evento"

        title = QLabel(title_text)
        title.setObjectName("eventDialogTitle")

        subtitle = QLabel("Preenche os detalhes do evento.")
        subtitle.setObjectName("eventDialogSubtitle")

        self.error_label = QLabel("")
        self.error_label.setObjectName("eventDialogError")

        self.title_input = QLineEdit()
        self.title_input.setObjectName("eventDialogInput")
        self.title_input.setPlaceholderText("Título do evento")

        self.description_input = QLineEdit()
        self.description_input.setObjectName("eventDialogInput")
        self.description_input.setPlaceholderText("Descrição")

        self.location_input = QLineEdit()
        self.location_input.setObjectName("eventDialogInput")
        self.location_input.setPlaceholderText("Local")

        row = QHBoxLayout()
        row.setSpacing(12)

        self.date_input = QDateEdit()
        self.date_input.setObjectName("eventDialogDate")
        self.date_input.setCalendarPopup(True)
        self.date_input.setFixedWidth(160)

        self.start_time_input = QTimeEdit()
        self.start_time_input.setObjectName("eventDialogTime")
        self.start_time_input.setDisplayFormat("HH:mm")
        self.start_time_input.setFixedWidth(120)

        self.end_time_input = QTimeEdit()
        self.end_time_input.setObjectName("eventDialogTime")
        self.end_time_input.setDisplayFormat("HH:mm")
        self.end_time_input.setFixedWidth(120)

        self.color_input = QComboBox()
        self.color_input.setObjectName("eventDialogCombo")
        self.color_input.addItems(list(self.COLORS.keys()))
        self.color_input.setFixedWidth(130)

        row.addWidget(self.date_input)
        row.addWidget(self.start_time_input)
        row.addWidget(self.end_time_input)
        row.addWidget(self.color_input)

        buttons = QHBoxLayout()
        buttons.setSpacing(10)
        buttons.addStretch()

        cancel_button = QPushButton("Cancelar")
        cancel_button.setObjectName("eventDialogCancelButton")
        cancel_button.setCursor(Qt.PointingHandCursor)
        cancel_button.setFixedSize(130, 40)
        cancel_button.clicked.connect(self.reject)

        save_text = "Guardar alterações" if event else "Criar evento"

        save_button = QPushButton(save_text)
        save_button.setObjectName("eventDialogPrimaryButton")
        save_button.setCursor(Qt.PointingHandCursor)
        save_button.setFixedSize(170, 40)
        save_button.clicked.connect(self.validate_and_accept)

        buttons.addWidget(cancel_button)
        buttons.addWidget(save_button)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(6)
        layout.addWidget(self.title_input)
        layout.addWidget(self.description_input)
        layout.addWidget(self.location_input)
        layout.addLayout(row)
        layout.addWidget(self.error_label)
        layout.addStretch()
        layout.addLayout(buttons)

        self.load_data(selected_date)

    def load_data(self, selected_date):
        if self.event_data:
            self.title_input.setText(self.event_data["title"] or "")
            self.description_input.setText(self.event_data["description"] or "")
            self.location_input.setText(self.event_data["location"] or "")

            event_date = QDate.fromString(self.event_data["event_date"], "yyyy-MM-dd")
            if event_date.isValid():
                self.date_input.setDate(event_date)
            else:
                self.date_input.setDate(QDate.currentDate())

            start_time = QTime.fromString(self.event_data["start_time"] or "", "HH:mm")
            if start_time.isValid():
                self.start_time_input.setTime(start_time)
            else:
                self.start_time_input.setTime(QTime.currentTime())

            end_time = QTime.fromString(self.event_data["end_time"] or "", "HH:mm")
            if end_time.isValid():
                self.end_time_input.setTime(end_time)
            else:
                self.end_time_input.setTime(QTime.currentTime().addSecs(3600))

            color_name = self.get_color_name(self.event_data["color"] or "#3B82F6")
            self.color_input.setCurrentText(color_name)

            return

        if selected_date:
            self.date_input.setDate(
                QDate(selected_date.year, selected_date.month, selected_date.day)
            )
        else:
            self.date_input.setDate(QDate.currentDate())

        self.start_time_input.setTime(QTime.currentTime())
        self.end_time_input.setTime(QTime.currentTime().addSecs(3600))
        self.color_input.setCurrentText("Azul")

    def validate_and_accept(self):
        if not self.title_input.text().strip():
            self.error_label.setText("O título do evento é obrigatório.")
            return

        self.accept()

    def get_color_name(self, color_value):
        for name, value in self.COLORS.items():
            if value.lower() == color_value.lower():
                return name

        return "Azul"

    def get_data(self):
        color_name = self.color_input.currentText()

        return {
            "title": self.title_input.text().strip(),
            "description": self.description_input.text().strip(),
            "location": self.location_input.text().strip(),
            "event_date": self.date_input.date().toString("yyyy-MM-dd"),
            "start_time": self.start_time_input.time().toString("HH:mm"),
            "end_time": self.end_time_input.time().toString("HH:mm"),
            "color": self.COLORS.get(color_name, "#3B82F6"),
        }