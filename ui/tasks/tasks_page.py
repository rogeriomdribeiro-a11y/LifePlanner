from datetime import date

from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QComboBox,
    QDateEdit,
    QTimeEdit,
    QPushButton,
    QScrollArea,
)

from app.session import Session
from database.task_repository import TaskRepository
from ui.dialogs.custom_dialog import CustomDialog
from ui.widgets.priority_badge import LPPriorityBadge


class TasksPage(QWidget):
    def __init__(self):
        super().__init__()

        self.task_repository = TaskRepository()

        self.setObjectName("tasksPage")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("tasksScrollArea")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.content = QWidget()
        self.content.setObjectName("tasksContent")

        self.layout = QVBoxLayout(self.content)
        self.layout.setContentsMargins(40, 32, 40, 40)
        self.layout.setSpacing(18)

        self.scroll_area.setWidget(self.content)
        main_layout.addWidget(self.scroll_area)

        self.create_header()
        self.create_form()
        self.create_tasks_list()

    def create_header(self):
        title = QLabel("Tarefas")
        title.setObjectName("contentPageTitle")

        subtitle = QLabel("Cria, organiza e acompanha as tuas tarefas.")
        subtitle.setObjectName("contentPageSubtitle")

        self.layout.addWidget(title)
        self.layout.addWidget(subtitle)

    def create_form(self):
        form_card = QFrame()
        form_card.setObjectName("taskFormCard")

        form_layout = QVBoxLayout(form_card)
        form_layout.setContentsMargins(22, 20, 22, 20)
        form_layout.setSpacing(14)

        form_title = QLabel("Nova tarefa")
        form_title.setObjectName("taskFormTitle")

        self.title_input = QLineEdit()
        self.title_input.setObjectName("taskInput")
        self.title_input.setPlaceholderText("Título da tarefa")

        row = QHBoxLayout()
        row.setSpacing(12)

        self.category_input = QComboBox()
        self.category_input.setObjectName("taskCombo")
        self.category_input.addItems(["Pessoal", "Trabalho", "Saúde", "Estudo"])

        self.date_input = QDateEdit()
        self.date_input.setObjectName("taskDate")
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())

        self.time_input = QTimeEdit()
        self.time_input.setObjectName("taskTimeEdit")
        self.time_input.setDisplayFormat("HH:mm")

        self.priority_input = QComboBox()
        self.priority_input.setObjectName("taskCombo")
        self.priority_input.addItems(["Baixa", "Normal", "Alta", "Urgente"])

        add_button = QPushButton("Adicionar tarefa")
        add_button.setObjectName("taskAddButton")
        add_button.setCursor(Qt.PointingHandCursor)
        add_button.clicked.connect(self.create_task)

        row.addWidget(self.category_input)
        row.addWidget(self.date_input)
        row.addWidget(self.time_input)
        row.addWidget(self.priority_input)
        row.addWidget(add_button)

        form_layout.addWidget(form_title)
        form_layout.addWidget(self.title_input)
        form_layout.addLayout(row)

        self.layout.addWidget(form_card)

    def create_tasks_list(self):
        self.list_card = QFrame()
        self.list_card.setObjectName("taskListCard")

        list_layout = QVBoxLayout(self.list_card)
        list_layout.setContentsMargins(22, 20, 22, 20)
        list_layout.setSpacing(14)

        header = QHBoxLayout()

        title = QLabel("As minhas tarefas")
        title.setObjectName("taskListTitle")

        self.total_label = QLabel()
        self.total_label.setObjectName("taskListCounter")

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.total_label)

        self.tasks_layout = QVBoxLayout()
        self.tasks_layout.setSpacing(8)

        list_layout.addLayout(header)
        list_layout.addLayout(self.tasks_layout)

        self.layout.addWidget(self.list_card)
        self.layout.addStretch()

    def create_task(self):
        user = Session.current_user

        if not user:
            return

        title = self.title_input.text().strip()

        if not title:
            CustomDialog.warning(
                self,
                "Escreve o título da tarefa.",
                "Campo obrigatório"
            )
            return

        due_date = self.date_input.date().toString("yyyy-MM-dd")
        due_time = self.time_input.time().toString("HH:mm")

        self.task_repository.create_task(
            user_id=user["id"],
            title=title,
            category=self.category_input.currentText(),
            due_date=due_date,
            due_time=due_time,
            priority=self.priority_input.currentText(),
        )

        self.title_input.clear()

        self.refresh()

    def refresh(self):
        user = Session.current_user

        self.clear_layout(self.tasks_layout)

        if not user:
            self.total_label.setText("0 tarefas")
            return

        tasks = self.task_repository.get_tasks_by_user(user["id"])

        total = len(tasks)
        self.total_label.setText(f"{total} tarefa" if total == 1 else f"{total} tarefas")

        if not tasks:
            empty_label = QLabel("Ainda não tens tarefas criadas.")
            empty_label.setObjectName("emptyStateLabel")
            self.tasks_layout.addWidget(empty_label)
            return

        for task in tasks:
            self.tasks_layout.addWidget(
                self.create_task_row(task)
            )

    def create_task_row(self, task):
        row = QFrame()
        row.setObjectName("taskRow")
        row.setMinimumHeight(54)

        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 8, 0, 8)
        layout.setSpacing(12)

        status = "✓" if task["is_completed"] else "○"

        status_button = QPushButton(status)
        status_button.setObjectName("taskStatusButton")
        status_button.setCursor(Qt.PointingHandCursor)
        status_button.clicked.connect(
            lambda: self.toggle_task(task)
        )

        title = QLabel(task["title"])
        title.setObjectName(
            "taskRowTitleCompleted" if task["is_completed"] else "taskRowTitle"
        )

        category = QLabel(task["category"] or "Pessoal")
        category.setObjectName("taskRowCategory")
        priority = LPPriorityBadge(task["priority"] or "Normal")

        due_date = task["due_date"] or ""
        due_time = task["due_time"] or ""

        when = QLabel(f"{due_date} {due_time}".strip())
        when.setObjectName("taskRowDate")

        delete_button = QPushButton("Eliminar")
        delete_button.setObjectName("taskDeleteButton")
        delete_button.setCursor(Qt.PointingHandCursor)
        delete_button.clicked.connect(
            lambda: self.delete_task(task)
        )

        layout.addWidget(status_button)
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(category)
        layout.addWidget(priority)
        layout.addWidget(when)
        layout.addWidget(delete_button)

        return row

    def toggle_task(self, task):
        user = Session.current_user

        if not user:
            return

        new_status = not bool(task["is_completed"])

        self.task_repository.update_task_status(
            task_id=task["id"],
            user_id=user["id"],
            is_completed=new_status,
        )

        self.refresh()

    def delete_task(self, task):
        user = Session.current_user

        if not user:
            return

        confirmed = CustomDialog.confirm(
            self,
            f'Tens a certeza que queres eliminar a tarefa "{task["title"]}"?',
            "Eliminar tarefa",
            "Eliminar",
            "Cancelar",
            "warning",
            True,
        )

        if not confirmed:
            return

        self.task_repository.delete_task(
            task_id=task["id"],
            user_id=user["id"],
        )

        self.refresh()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()