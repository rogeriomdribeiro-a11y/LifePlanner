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
    def __init__(self, parent=None, event=None):
        super().__init__(parent)

        self.event_data = event 
        self.action = None

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)
        self.setFixedSize(500, 380)

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
            background-color: {event["color"] or "#3B82F6"};
            border-radius: 6px;
        """)

        title = QLabel(event["title"])
        title.setObjectName("eventDialogTitle")

        header.addWidget(color_dot)
        header.addWidget(title)
        header.addStretch()

        description = QLabel(event["description"] or "Sem descrição.")
        description.setObjectName("eventDialogText")
        description.setWordWrap(True)

        location = QLabel(f'Local: {event["location"] or "Sem local definido"}')
        location.setObjectName("eventDialogInfo")

        time_text = event["start_time"] or ""

        if event["start_time"] and event["end_time"]:
            time_text = f'{event["start_time"]} - {event["end_time"]}'

        date = QLabel(f'Data: {event["event_date"]}')
        date.setObjectName("eventDialogInfo")

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
        layout.addWidget(date)
        layout.addWidget(time)
        layout.addStretch()
        layout.addLayout(buttons)

    def edit_event(self):
        self.action = "edit"
        self.accept()

    def delete_event(self):
        self.action = "delete"
        self.accept()