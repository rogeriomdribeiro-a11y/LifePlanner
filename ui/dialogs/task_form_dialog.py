from PySide6.QtCore import Qt, QDate, QTime
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLineEdit,
    QComboBox,
    QDateEdit,
    QTimeEdit,
    QPushButton,
    QGraphicsDropShadowEffect,
    QAbstractSpinBox,
)


class TaskFormDialog(QDialog):
    CATEGORIES = [
        "Pessoal",
        "Trabalho",
        "Saúde",
        "Estudo",
    ]

    PRIORITIES = [
        "Baixa",
        "Normal",
        "Alta",
        "Urgente",
    ]

    def __init__(self, parent=None, task=None):
        super().__init__(parent)

        self.task_data = task

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)
        self.setFixedSize(640, 470)

        wrapper_layout = QVBoxLayout(self)
        wrapper_layout.setContentsMargins(15, 15, 15, 15)

        container = QFrame()
        container.setObjectName("taskDialogContainer")

        shadow = QGraphicsDropShadowEffect(container)
        shadow.setBlurRadius(35)
        shadow.setOffset(0, 5)
        shadow.setColor(QColor(0, 0, 0, 150))
        container.setGraphicsEffect(shadow)

        wrapper_layout.addWidget(container)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(28, 26, 28, 26)
        layout.setSpacing(14)

        title_text = "Editar tarefa" if task else "Nova tarefa"

        title = QLabel(title_text)
        title.setObjectName("taskDialogTitle")

        subtitle = QLabel("Define a tarefa, categoria, data, hora e prioridade.")
        subtitle.setObjectName("taskDialogSubtitle")

        self.error_label = QLabel("")
        self.error_label.setObjectName("taskDialogError")
        self.error_label.setFixedHeight(18)

        self.title_input = QLineEdit()
        self.title_input.setObjectName("taskDialogInput")
        self.title_input.setPlaceholderText("Título da tarefa")
        self.title_input.setFixedHeight(40)

        self.category_input = QComboBox()
        self.category_input.setObjectName("taskDialogCombo")
        self.category_input.addItems(self.CATEGORIES)
        self.category_input.setFixedHeight(40)

        self.date_input = QDateEdit()
        self.date_input.setObjectName("taskDialogDateInput")
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("dd/MM/yyyy")
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setFixedHeight(40)

        self.time_input = QTimeEdit()
        self.time_input.setObjectName("taskDialogTimeInput")
        self.time_input.setDisplayFormat("HH:mm")
        self.time_input.setTime(QTime.currentTime())
        self.time_input.setFixedHeight(40)
        self.time_input.setButtonSymbols(QAbstractSpinBox.NoButtons)
        

        self.priority_input = QComboBox()
        self.priority_input.setObjectName("taskDialogCombo")
        self.priority_input.addItems(self.PRIORITIES)
        self.priority_input.setFixedHeight(40)

        self.category_input.setMinimumWidth(240)
        self.date_input.setMinimumWidth(240)
        self.time_input.setMinimumWidth(240)
        self.priority_input.setMinimumWidth(240)


        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(22)

        grid.addLayout(self.create_field("Categoria", self.category_input), 0, 0)
        grid.addLayout(self.create_field("Data", self.date_input), 0, 1)
        grid.addLayout(self.create_field("Hora", self.time_input), 1, 0)
        grid.addLayout(self.create_field("Prioridade", self.priority_input), 1, 1)

        buttons = QHBoxLayout()
        buttons.setSpacing(10)
        buttons.addStretch()

        cancel_button = QPushButton("Cancelar")
        cancel_button.setObjectName("taskDialogCancelButton")
        cancel_button.setCursor(Qt.PointingHandCursor)
        cancel_button.setFixedSize(130, 40)
        cancel_button.clicked.connect(self.reject)

        save_text = "Guardar alterações" if task else "Criar tarefa"

        save_button = QPushButton(save_text)
        save_button.setObjectName("taskDialogPrimaryButton")
        save_button.setCursor(Qt.PointingHandCursor)
        save_button.setFixedSize(170, 40)
        save_button.clicked.connect(self.validate_and_accept)

        buttons.addWidget(cancel_button)
        buttons.addWidget(save_button)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(4)
        layout.addLayout(self.create_field("Título", self.title_input))
        layout.addLayout(grid)
        layout.addWidget(self.error_label)
        layout.addStretch()
        layout.addLayout(buttons)

        self.load_data()

    def create_field(self, label_text, widget):
        field_layout = QVBoxLayout()
        field_layout.setSpacing(6)

        label = QLabel(label_text)
        label.setObjectName("taskDialogFieldLabel")

        field_layout.addWidget(label)
        field_layout.addWidget(widget)

        return field_layout

    def load_data(self):
        if not self.task_data:
            self.category_input.setCurrentText("Pessoal")
            self.priority_input.setCurrentText("Normal")
            return

        self.title_input.setText(self.task_data["title"] or "")
        self.category_input.setCurrentText(self.task_data["category"] or "Pessoal")
        self.priority_input.setCurrentText(self.task_data["priority"] or "Normal")

        if self.task_data["due_date"]:
            task_date = QDate.fromString(self.task_data["due_date"], "yyyy-MM-dd")

            if task_date.isValid():
                self.date_input.setDate(task_date)

        if self.task_data["due_time"]:
            task_time = QTime.fromString(self.task_data["due_time"], "HH:mm")

            if task_time.isValid():
                self.time_input.setTime(task_time)

    def validate_and_accept(self):
        if not self.title_input.text().strip():
            self.error_label.setText("O título da tarefa é obrigatório.")
            return

        self.accept()

    def get_data(self):
        return {
            "title": self.title_input.text().strip(),
            "category": self.category_input.currentText(),
            "due_date": self.date_input.date().toString("yyyy-MM-dd"),
            "due_time": self.time_input.time().toString("HH:mm"),
            "priority": self.priority_input.currentText(),
        }