from datetime import date, datetime, timedelta

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QScrollArea,
    QWidget,
    QGraphicsDropShadowEffect,
)


class DayEventsDialog(QDialog):
    """Listar todos os eventos existentes numa determinada data."""
    def __init__(self, parent=None, events=None):
        super().__init__(parent)

        self.events = events or []
        self.selected_event = None

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)
        self.setFixedSize(520, 440)

        wrapper_layout = QVBoxLayout(self)
        wrapper_layout.setContentsMargins(15, 15, 15, 15)

        container = QFrame()
        container.setObjectName("dayEventsDialogContainer")

        shadow = QGraphicsDropShadowEffect(container)
        shadow.setBlurRadius(35)
        shadow.setOffset(0, 5)
        shadow.setColor(QColor(0, 0, 0, 150))
        container.setGraphicsEffect(shadow)

        wrapper_layout.addWidget(container)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(28, 26, 28, 26)
        layout.setSpacing(14)

        title = QLabel("Eventos do dia")
        title.setObjectName("dayEventsDialogTitle")

        subtitle = QLabel(self.get_subtitle())
        subtitle.setObjectName("dayEventsDialogSubtitle")

        scroll_area = QScrollArea()
        scroll_area.setObjectName("dayEventsScrollArea")
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)

        scroll_content = QWidget()
        scroll_content.setObjectName("dayEventsScrollContent")

        self.events_layout = QVBoxLayout(scroll_content)
        self.events_layout.setContentsMargins(0, 0, 0, 0)
        self.events_layout.setSpacing(10)

        scroll_area.setWidget(scroll_content)

        for event_data in self.events:
            self.events_layout.addWidget(
                self.create_event_button(event_data)
            )

        close_button = QPushButton("Fechar")
        close_button.setObjectName("eventDialogCancelButton")
        close_button.setCursor(Qt.PointingHandCursor)
        close_button.setFixedSize(120, 40)
        close_button.clicked.connect(self.reject)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(4)
        layout.addWidget(scroll_area)
        layout.addWidget(close_button, alignment=Qt.AlignRight)

    def create_event_button(self, event_data):
        color = event_data["color"] or "#3B82F6"

        start_time = event_data["start_time"] or ""
        end_time = event_data["end_time"] or ""

        time_text = start_time

        if start_time and end_time:
            time_text = f"{start_time} - {end_time}"

        location = event_data["location"] or "Sem local definido"

        button = QPushButton(f'{time_text}  ·  {event_data["title"]}\n{location}')
        button.setObjectName("dayEventButton")
        button.setCursor(Qt.PointingHandCursor)
        button.setMinimumHeight(58)

        button.setStyleSheet(f"""
            QPushButton#dayEventButton {{
                background-color: #0F172A;
                border: 1px solid #334155;
                border-left: 5px solid {color};
                border-radius: 10px;
                color: #F8FAFC;
                text-align: left;
                padding: 8px 12px;
                font-size: 13px;
                font-weight: 600;
            }}

            QPushButton#dayEventButton:hover {{
                background-color: #111C30;
                border: 1px solid #475569;
                border-left: 5px solid {color};
            }}
        """)

        button.clicked.connect(
            lambda: self.select_event(event_data)
        )

        return button

    def select_event(self, event_data):
        self.selected_event = event_data
        self.accept()

    def get_subtitle(self):
        if not self.events:
            return "Sem eventos."

        event_date = self.events[0]["event_date"]

        return self.format_event_date(event_date)

    def format_event_date(self, event_date):
        if not event_date:
            return "Sem data"

        try:
            parsed_date = datetime.strptime(event_date, "%Y-%m-%d").date()
        except ValueError:
            return event_date

        today = date.today()
        tomorrow = today + timedelta(days=1)

        if parsed_date == today:
            return "Hoje"

        if parsed_date == tomorrow:
            return "Amanhã"

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

        month = months[parsed_date.month - 1]

        return f"{parsed_date.day} de {month}"