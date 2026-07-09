from datetime import date, datetime, timedelta

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGraphicsDropShadowEffect,
)


class EventDetailsDialog(QDialog):
    def __init__(self, parent=None, event_data=None):
        super().__init__(parent)

        self.event_data = event_data
        self.action = None

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)
        self.setFixedSize(500, 390)

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

        header = QHBoxLayout()
        header.setSpacing(12)

        color_dot = QFrame()
        color_dot.setFixedSize(12, 12)
        color_dot.setStyleSheet(f"""
            background-color: {event_data["color"] or "#3B82F6"};
            border-radius: 6px;
        """)

        title = QLabel(event_data["title"])
        title.setObjectName("eventDialogTitle")
        title.setWordWrap(True)

        header.addWidget(color_dot)
        header.addWidget(title)
        header.addStretch()

        description = QLabel(event_data["description"] or "Sem descrição.")
        description.setObjectName("eventDialogText")
        description.setWordWrap(True)

        location = QLabel(f'Local: {event_data["location"] or "Sem local definido"}')
        location.setObjectName("eventDialogInfo")

        time_text = event_data["start_time"] or ""

        if event_data["start_time"] and event_data["end_time"]:
            time_text = f'{event_data["start_time"]} - {event_data["end_time"]}'

        event_date = QLabel(
            f'Data: {self.format_event_date(event_data["event_date"])}'
        )
        event_date.setObjectName("eventDialogInfo")

        time = QLabel(f'Horário: {time_text or "Sem horário definido"}')
        time.setObjectName("eventDialogInfo")

        buttons = QHBoxLayout()
        buttons.setSpacing(10)
        buttons.addStretch()

        close_button = QPushButton("Fechar")
        close_button.setObjectName("eventDialogCancelButton")
        close_button.setCursor(Qt.PointingHandCursor)
        close_button.setFixedSize(110, 40)
        close_button.clicked.connect(self.reject)

        edit_button = QPushButton("Editar")
        edit_button.setObjectName("eventDialogPrimaryButton")
        edit_button.setCursor(Qt.PointingHandCursor)
        edit_button.setFixedSize(110, 40)
        edit_button.clicked.connect(self.edit_event)

        delete_button = QPushButton("Eliminar")
        delete_button.setObjectName("eventDialogDangerButton")
        delete_button.setCursor(Qt.PointingHandCursor)
        delete_button.setFixedSize(110, 40)
        delete_button.clicked.connect(self.delete_event)

        buttons.addWidget(close_button)
        buttons.addWidget(edit_button)
        buttons.addWidget(delete_button)

        layout.addLayout(header)
        layout.addWidget(description)
        layout.addSpacing(6)
        layout.addWidget(location)
        layout.addWidget(event_date)
        layout.addWidget(time)
        layout.addStretch()
        layout.addLayout(buttons)

    def format_event_date(self, event_date):
        if not event_date:
            return "Sem data"

        try:
            parsed_date = datetime.strptime(event_date, "%Y-%m-%d").date()
        except ValueError:
            return event_date

        today = date.today()
        tomorrow = today + timedelta(days=1)
        yesterday = today - timedelta(days=1)

        if parsed_date == today:
            return "Hoje"

        if parsed_date == tomorrow:
            return "Amanhã"

        if parsed_date == yesterday:
            return "Ontem"

        weekdays = [
            "Segunda-feira",
            "Terça-feira",
            "Quarta-feira",
            "Quinta-feira",
            "Sexta-feira",
            "Sábado",
            "Domingo",
        ]

        months = [
            "janeiro",
            "fevereiro",
            "março",
            "abril",
            "maio",
            "junho",
            "julho",
            "agosto",
            "setembro",
            "outubro",
            "novembro",
            "dezembro",
        ]

        weekday = weekdays[parsed_date.weekday()]
        month = months[parsed_date.month - 1]

        return f"{weekday}, {parsed_date.day} de {month}"

    def edit_event(self):
        self.action = "edit"
        self.accept()

    def delete_event(self):
        self.action = "delete"
        self.accept()