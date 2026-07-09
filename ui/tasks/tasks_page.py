from datetime import date, datetime, timedelta
from PySide6.QtCore import Qt, QDate, QTime, QSize
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
from PySide6.QtGui import QIcon
from app.session import Session
from database.task_repository import TaskRepository
from ui.dialogs.custom_dialog import CustomDialog
from ui.widgets.priority_badge import LPPriorityBadge
from app.path import ICONS_DIR
from ui.widgets.category_badge import LPCategoryBadge
from ui.widgets.priority_badge import LPPriorityBadge



class TasksPage(QWidget):
    def __init__(self):
        super().__init__()

        self.task_repository = TaskRepository()
        self.editing_task = None
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
        header = QHBoxLayout()
        header.setSpacing(16)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)

        title = QLabel("Tarefas")
        title.setObjectName("contentPageTitle")

        subtitle = QLabel("Cria, organiza e acompanha as tuas tarefas.")
        subtitle.setObjectName("contentPageSubtitle")

        text_layout.addWidget(title)
        text_layout.addWidget(subtitle)

        self.toggle_form_button = QPushButton("+ Nova tarefa")
        self.toggle_form_button.setObjectName("taskToggleFormButton")
        self.toggle_form_button.setCursor(Qt.PointingHandCursor)
        self.toggle_form_button.setFixedHeight(42)
        self.toggle_form_button.clicked.connect(self.toggle_task_form)

        header.addLayout(text_layout)
        header.addStretch()
        header.addWidget(self.toggle_form_button)

        self.layout.addLayout(header)

    def create_form(self):
        self.form_card = QFrame()
        self.form_card.setObjectName("taskFormCard")
        self.form_card.hide()

        form_layout = QVBoxLayout(self.form_card)
        form_layout.setContentsMargins(22, 20, 22, 20)
        form_layout.setSpacing(14)

        self.form_title = QLabel("Nova tarefa")
        self.form_title.setObjectName("taskFormTitle")

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

        self.submit_button = QPushButton("Adicionar tarefa")
        self.submit_button.setObjectName("taskAddButton")
        self.submit_button.setCursor(Qt.PointingHandCursor)
        self.submit_button.clicked.connect(self.save_task)

        self.category_input.setFixedWidth(180)
        self.date_input.setFixedWidth(190)
        self.time_input.setFixedWidth(170)
        self.priority_input.setFixedWidth(190)

        self.submit_button.setFixedWidth(190)
        self.submit_button.setFixedHeight(42)

        row.addWidget(self.category_input)
        row.addWidget(self.date_input)
        row.addWidget(self.time_input)
        row.addWidget(self.priority_input)
        row.addWidget(self.submit_button)

        form_layout.addWidget(self.form_title)
        form_layout.addWidget(self.title_input)
        form_layout.addLayout(row)

        self.layout.addWidget(self.form_card)

    def toggle_task_form(self):
        is_visible = self.form_card.isVisible()

        if is_visible:
            self.form_card.hide()
            self.toggle_form_button.setText("+ Nova tarefa")
            self.reset_form()
        else:
            self.form_card.show()
            self.toggle_form_button.setText("Fechar")

    def reset_form(self):
        self.editing_task = None

        self.form_title.setText("Nova tarefa")
        self.submit_button.setText("Adicionar tarefa")

        self.title_input.clear()
        self.category_input.setCurrentText("Pessoal")
        self.date_input.setDate(QDate.currentDate())
        self.time_input.setTime(QTime.currentTime())
        self.priority_input.setCurrentText("Normal")

    def create_tasks_list(self):
        self.list_card = QFrame()
        self.list_card.setObjectName("taskListCard")

        list_layout = QVBoxLayout(self.list_card)
        list_layout.setContentsMargins(22, 20, 22, 20)
        list_layout.setSpacing(18)

        header = QHBoxLayout()

        title = QLabel("As minhas tarefas")
        title.setObjectName("taskListTitle")

        self.total_label = QLabel()
        self.total_label.setObjectName("taskListCounter")

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.total_label)

        pending_header = QHBoxLayout()

        pending_title = QLabel("Pendentes")
        pending_title.setObjectName("taskGroupTitle")

        self.pending_counter = QLabel()
        self.pending_counter.setObjectName("taskGroupCounter")

        pending_header.addWidget(pending_title)
        pending_header.addStretch()
        pending_header.addWidget(self.pending_counter)

        self.pending_tasks_layout = QVBoxLayout()
        self.pending_tasks_layout.setSpacing(8)

        completed_header = QHBoxLayout()

        completed_title = QLabel("Concluídas")
        completed_title.setObjectName("taskGroupTitle")

        self.completed_counter = QLabel()
        self.completed_counter.setObjectName("taskGroupCounter")

        completed_header.addWidget(completed_title)
        completed_header.addStretch()
        completed_header.addWidget(self.completed_counter)

        self.completed_tasks_layout = QVBoxLayout()
        self.completed_tasks_layout.setSpacing(8)

        list_layout.addLayout(header)
        list_layout.addLayout(pending_header)
        list_layout.addLayout(self.pending_tasks_layout)
        list_layout.addSpacing(10)
        list_layout.addLayout(completed_header)
        list_layout.addLayout(self.completed_tasks_layout)

        self.layout.addWidget(self.list_card)
        self.layout.addStretch()

    def save_task(self):
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

        if self.editing_task:
            self.task_repository.update_task(
                task_id=self.editing_task["id"],
                user_id=user["id"],
                title=title,
                category=self.category_input.currentText(),
                due_date=due_date,
                due_time=due_time,
                priority=self.priority_input.currentText(),
            )
        else:
            self.task_repository.create_task(
                user_id=user["id"],
                title=title,
                category=self.category_input.currentText(),
                due_date=due_date,
                due_time=due_time,
                priority=self.priority_input.currentText(),
            )

        self.reset_form()

        self.form_card.hide()
        self.toggle_form_button.setText("+ Nova tarefa")

        self.refresh()

    def refresh(self):
        user = Session.current_user

        self.clear_layout(self.pending_tasks_layout)
        self.clear_layout(self.completed_tasks_layout)

        if not user:
            self.total_label.setText("0 tarefas")
            self.pending_counter.setText("0")
            self.completed_counter.setText("0")
            return

        tasks = self.task_repository.get_tasks_by_user(user["id"])

        pending_tasks = [
            task for task in tasks
            if not task["is_completed"]
        ]

        completed_tasks = [
            task for task in tasks
            if task["is_completed"]
        ]

        total = len(tasks)

        self.total_label.setText(
            f"{total} tarefa" if total == 1 else f"{total} tarefas"
        )

        self.pending_counter.setText(str(len(pending_tasks)))
        self.completed_counter.setText(str(len(completed_tasks)))

        if not pending_tasks:
            empty_label = QLabel("Não tens tarefas pendentes.")
            empty_label.setObjectName("emptyStateLabel")
            self.pending_tasks_layout.addWidget(empty_label)
        else:
            for task in pending_tasks:
                self.pending_tasks_layout.addWidget(
                    self.create_task_row(task)
                )

        if not completed_tasks:
            empty_label = QLabel("Ainda não concluíste nenhuma tarefa.")
            empty_label.setObjectName("emptyStateLabel")
            self.completed_tasks_layout.addWidget(empty_label)
        else:
            for task in completed_tasks:
                self.completed_tasks_layout.addWidget(
                    self.create_task_row(task)
                )

    def create_task_row(self, task):
        row = QFrame()
        row.setObjectName("taskRow")
        row.setMinimumHeight(58)

        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 8, 0, 8)
        layout.setSpacing(12)

        is_completed = bool(task["is_completed"])

        status = "✓" if is_completed else "○"

        status_button = QPushButton(status)
        status_button.setObjectName(
            "taskStatusButtonCompleted" if is_completed else "taskStatusButton"
        )
        status_button.setCursor(Qt.PointingHandCursor)
        status_button.clicked.connect(
            lambda: self.toggle_task(task)
        )

        title = QLabel(task["title"])
        title.setObjectName(
            "taskRowTitleCompleted" if is_completed else "taskRowTitle"
        )

        category = LPCategoryBadge(task["category"] or "Pessoal")

        priority = LPPriorityBadge(task["priority"] or "Normal")

        due_date = task["due_date"] or ""
        due_time = task["due_time"] or ""

        when = QLabel(self.format_task_datetime(due_date, due_time))
        when.setObjectName("taskRowDate")

        layout.addWidget(status_button)
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(category)
        layout.addWidget(priority)
        layout.addWidget(when)

        if not is_completed:
            edit_button = QPushButton()
            edit_button.setObjectName("taskIconButton")
            edit_button.setCursor(Qt.PointingHandCursor)
            edit_button.setFixedSize(34, 34)
            edit_button.setIcon(QIcon(str(ICONS_DIR / "actions" / "edit.svg")))
            edit_button.setIconSize(QSize(18, 18))
            edit_button.clicked.connect(
                lambda: self.edit_task(task)
            )

            delete_button = QPushButton()
            delete_button.setObjectName("taskIconDangerButton")
            delete_button.setCursor(Qt.PointingHandCursor)
            delete_button.setFixedSize(34, 34)
            delete_button.setIcon(QIcon(str(ICONS_DIR / "actions" / "trash.svg")))
            delete_button.setIconSize(QSize(18, 18))
            delete_button.clicked.connect(
                lambda: self.delete_task(task)
            )

            layout.addWidget(edit_button)
            layout.addWidget(delete_button)

        return row
    
    def edit_task(self, task):
        if task["is_completed"]:
            CustomDialog.warning(
                self,
                "Não é possível editar uma tarefa concluída. Reabre primeiro a tarefa.",
                "Ação não permitida"
            )
            return

        self.editing_task = task

        self.form_title.setText("Editar tarefa")
        self.submit_button.setText("Guardar alterações")
        self.toggle_form_button.setText("Cancelar")

        self.title_input.setText(task["title"])

        category_index = self.category_input.findText(task["category"] or "Pessoal")
        if category_index >= 0:
            self.category_input.setCurrentIndex(category_index)

        priority_index = self.priority_input.findText(task["priority"] or "Normal")
        if priority_index >= 0:
            self.priority_input.setCurrentIndex(priority_index)

        if task["due_date"]:
            task_date = QDate.fromString(task["due_date"], "yyyy-MM-dd")
            if task_date.isValid():
                self.date_input.setDate(task_date)

        if task["due_time"]:
            task_time = QTime.fromString(task["due_time"], "HH:mm")
            if task_time.isValid():
                self.time_input.setTime(task_time)

        self.form_card.show()
        self.title_input.setFocus()

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

        if task["is_completed"]:
            CustomDialog.warning(
                self,
                "Não é possível eliminar uma tarefa concluída.",
                "Ação não permitida"
            )
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
    def format_task_datetime(self, due_date, due_time):
        if not due_date and not due_time:
            return "Sem data"

        if not due_date:
            return due_time or "Sem data"

        try:
            task_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        except ValueError:
            return f"{due_date} {due_time}".strip()

        today = date.today()
        tomorrow = today + timedelta(days=1)
        yesterday = today - timedelta(days=1)

        if task_date == today:
            date_text = "Hoje"
        elif task_date == tomorrow:
            date_text = "Amanhã"
        elif task_date == yesterday:
            date_text = "Ontem"
        else:
            months = [
                "jan", "fev", "mar", "abr", "mai", "jun",
                "jul", "ago", "set", "out", "nov", "dez"
            ]

            month = months[task_date.month - 1]

            if task_date.year == today.year:
                date_text = f"{task_date.day} {month}"
            else:
                date_text = task_date.strftime("%d/%m/%Y")

        if due_time:
            return f"{date_text} às {due_time}"

        return date_text