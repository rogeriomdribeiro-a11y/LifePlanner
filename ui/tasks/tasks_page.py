from datetime import date, datetime, timedelta

from PySide6.QtCore import Qt, QSize, QDate
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QScrollArea,
    QDialog,
    QComboBox,
    QDateEdit,
    QCheckBox,
)
from PySide6.QtGui import QIcon

from app.session import Session
from app.path import ICONS_DIR
from database.task_repository import TaskRepository
from ui.dialogs.custom_dialog import CustomDialog
from ui.dialogs.task_form_dialog import TaskFormDialog
from ui.widgets.category_badge import LPCategoryBadge
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
        self.create_filters()
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

        self.new_task_button = QPushButton("+ Nova tarefa")
        self.new_task_button.setObjectName("taskToggleFormButton")
        self.new_task_button.setCursor(Qt.PointingHandCursor)
        self.new_task_button.setFixedSize(160, 42)
        self.new_task_button.clicked.connect(self.open_task_form)

        header.addLayout(text_layout)
        header.addStretch()
        header.addWidget(self.new_task_button)

        self.layout.addLayout(header)

    def create_filters(self):
        self.filters_card = QFrame()
        self.filters_card.setObjectName("taskFiltersCard")

        layout = QHBoxLayout(self.filters_card)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(14)

        date_label = QLabel("Data")
        date_label.setObjectName("taskFilterLabel")

        self.date_filter_checkbox = QCheckBox("Filtrar por data")
        self.date_filter_checkbox.setObjectName("taskFilterCheckbox")
        self.date_filter_checkbox.setCursor(Qt.PointingHandCursor)
        self.date_filter_checkbox.stateChanged.connect(self.handle_date_filter_changed)

        self.date_filter_input = QDateEdit()
        self.date_filter_input.setObjectName("taskFilterDate")
        self.date_filter_input.setCalendarPopup(True)
        self.date_filter_input.setDisplayFormat("dd/MM/yyyy")
        self.date_filter_input.setDate(QDate.currentDate())
        self.date_filter_input.setEnabled(False)
        self.date_filter_input.setFixedSize(140, 40)
        self.date_filter_input.dateChanged.connect(self.refresh)

        category_label = QLabel("Categoria")
        category_label.setObjectName("taskFilterLabel")

        self.category_filter_input = QComboBox()
        self.category_filter_input.setObjectName("taskFilterCombo")
        self.category_filter_input.setFixedSize(150, 40)
        self.category_filter_input.addItems([
            "Todas",
            "Geral",
            "Pessoal",
            "Trabalho",
            "Saúde",
            "Estudo",
        ])
        self.category_filter_input.currentTextChanged.connect(self.refresh)

        self.clear_filters_button = QPushButton("Limpar filtros")
        self.clear_filters_button.setObjectName("taskClearFilterButton")
        self.clear_filters_button.setCursor(Qt.PointingHandCursor)
        self.clear_filters_button.setFixedSize(130, 40)
        self.clear_filters_button.clicked.connect(self.clear_filters)

        layout.addWidget(date_label)
        layout.addWidget(self.date_filter_checkbox)
        layout.addWidget(self.date_filter_input)
        layout.addSpacing(10)
        layout.addWidget(category_label)
        layout.addWidget(self.category_filter_input)
        layout.addStretch()
        layout.addWidget(self.clear_filters_button)

        self.layout.addWidget(self.filters_card)


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

    def open_task_form(self, task=None):
        if task and task["is_completed"]:
            CustomDialog.warning(
                self,
                "Não é possível editar uma tarefa concluída. Reabre primeiro a tarefa.",
                "Ação não permitida",
            )
            return

        dialog = TaskFormDialog(self, task)

        if dialog.exec() != QDialog.Accepted:
            return

        user = Session.current_user

        if not user:
            return

        data = dialog.get_data()

        if task:
            self.task_repository.update_task(
                task_id=task["id"],
                user_id=user["id"],
                title=data["title"],
                category=data["category"],
                due_date=data["due_date"],
                due_time=data["due_time"],
                priority=data["priority"],
            )
        else:
            self.task_repository.create_task(
                user_id=user["id"],
                title=data["title"],
                category=data["category"],
                due_date=data["due_date"],
                due_time=data["due_time"],
                priority=data["priority"],
            )

        self.refresh()
    def handle_date_filter_changed(self):
        is_enabled = self.date_filter_checkbox.isChecked()
        self.date_filter_input.setEnabled(is_enabled)
        self.refresh()


    def clear_filters(self):
        self.date_filter_checkbox.setChecked(False)
        self.date_filter_input.setDate(QDate.currentDate())
        self.category_filter_input.setCurrentText("Todas")
        self.refresh()


    def get_selected_filter_date(self):
        if not self.date_filter_checkbox.isChecked():
            return None

        return self.date_filter_input.date().toString("yyyy-MM-dd")


    def get_selected_filter_category(self):
        category = self.category_filter_input.currentText()

        if category == "Todas":
            return None

        return category
    
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

        selected_date = self.get_selected_filter_date()
        selected_category = self.get_selected_filter_category()
        today = date.today().isoformat()

        pending_tasks = []
        completed_tasks = []

        for task in tasks:
            task_category = task["category"] or "Pessoal"
            task_due_date = task["due_date"]

            if selected_category and task_category != selected_category:
                continue

            if selected_date and task_due_date != selected_date:
                continue

            if task["is_completed"]:
                if selected_date:
                    completed_tasks.append(task)
                elif task_due_date == today:
                    completed_tasks.append(task)
            else:
                pending_tasks.append(task)

        pending_tasks.sort(
            key=lambda task: (
                not self.is_task_overdue(task),
                task["due_date"] or "9999-12-31",
                task["due_time"] or "23:59",
            )
        )

        completed_tasks.sort(
            key=lambda task: (
                task["due_date"] or "9999-12-31",
                task["due_time"] or "23:59",
            )
        )

        total = len(pending_tasks) + len(completed_tasks)

        self.total_label.setText(
            f"{total} tarefa visível" if total == 1 else f"{total} tarefas visíveis"
        )

        self.pending_counter.setText(str(len(pending_tasks)))
        self.completed_counter.setText(str(len(completed_tasks)))

        if not pending_tasks:
            empty_label = QLabel("Não tens tarefas pendentes para este filtro.")
            empty_label.setObjectName("emptyStateLabel")
            self.pending_tasks_layout.addWidget(empty_label)
        else:
            for task in pending_tasks:
                self.pending_tasks_layout.addWidget(
                    self.create_task_row(task)
                )

        if not completed_tasks:
            if selected_date:
                message = "Não tens tarefas concluídas nesta data."
            else:
                message = "Ainda não concluíste nenhuma tarefa hoje."

            empty_label = QLabel(message)
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
        is_overdue = self.is_task_overdue(task)

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
        when.setObjectName("taskRowDateOverdue" if is_overdue else "taskRowDate")

        layout.addWidget(status_button)
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(category)
        layout.addWidget(priority)

        if is_overdue:
            overdue_badge = QLabel("Atrasada")
            overdue_badge.setObjectName("taskOverdueBadge")
            layout.addWidget(overdue_badge)

        layout.addWidget(when)
        
        if not is_completed:
            edit_button = QPushButton()
            edit_button.setObjectName("taskIconButton")
            edit_button.setCursor(Qt.PointingHandCursor)
            edit_button.setFixedSize(34, 34)
            edit_button.setIcon(QIcon(str(ICONS_DIR / "actions" / "edit.svg")))
            edit_button.setIconSize(QSize(18, 18))
            edit_button.clicked.connect(
                lambda: self.open_task_form(task)
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
                "Ação não permitida",
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
                "jul", "ago", "set", "out", "nov", "dez",
            ]

            month = months[task_date.month - 1]

            if task_date.year == today.year:
                date_text = f"{task_date.day} {month}"
            else:
                date_text = task_date.strftime("%d/%m/%Y")

        if due_time:
            return f"{date_text} às {due_time}"

        return date_text
    
    def is_task_overdue(self, task):
        if task["is_completed"]:
            return False

        due_date = task["due_date"]

        if not due_date:
            return False

        try:
            task_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        except ValueError:
            return False

        return task_date < date.today()