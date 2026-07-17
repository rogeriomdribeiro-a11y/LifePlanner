from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QFrame,
    QGridLayout,
    QDialog,
)

from app.session import Session
from database.goal_repository import GoalRepository
from ui.dialogs.custom_dialog import CustomDialog
from ui.dialogs.goal_form_dialog import GoalFormDialog
from ui.widgets.goal_card import LPGoalCard


class GoalsPage(QWidget):
    """Apresentar, criar e atualizar os objetivos do utilizador."""
    def __init__(self):
        super().__init__()

        self.setObjectName("goalsPage")

        self.goal_repository = GoalRepository()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        scroll_area = QScrollArea()
        scroll_area.setObjectName("goalsScrollArea")
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)

        content = QWidget()
        content.setObjectName("goalsContent")

        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(40, 30, 40, 40)
        self.content_layout.setSpacing(24)

        self.create_header()
        self.create_summary()
        self.create_goals_list()

        scroll_area.setWidget(content)
        main_layout.addWidget(scroll_area)

    def create_header(self):
        header = QHBoxLayout()
        header.setSpacing(16)

        texts = QVBoxLayout()
        texts.setSpacing(4)

        title = QLabel("Objetivos")
        title.setObjectName("goalsPageTitle")

        subtitle = QLabel("Define metas, acompanha o progresso e mantém o foco.")
        subtitle.setObjectName("goalsPageSubtitle")

        texts.addWidget(title)
        texts.addWidget(subtitle)

        new_goal_button = QPushButton("+ Novo objetivo")
        new_goal_button.setObjectName("goalsPrimaryButton")
        new_goal_button.setCursor(Qt.PointingHandCursor)
        new_goal_button.setFixedSize(160, 42)
        new_goal_button.clicked.connect(self.open_goal_form)

        header.addLayout(texts)
        header.addStretch()
        header.addWidget(new_goal_button)

        self.content_layout.addLayout(header)

    def create_summary(self):
        self.summary_frame = QFrame()
        self.summary_frame.setObjectName("goalsSummaryCard")

        layout = QHBoxLayout(self.summary_frame)
        layout.setContentsMargins(22, 18, 22, 18)
        layout.setSpacing(18)

        self.total_goals_label = self.create_summary_item(
            layout,
            "0",
            "Objetivos"
        )

        self.active_goals_label = self.create_summary_item(
            layout,
            "0",
            "Em progresso"
        )

        self.completed_goals_label = self.create_summary_item(
            layout,
            "0",
            "Concluídos"
        )

        self.average_progress_label = self.create_summary_item(
            layout,
            "0%",
            "Progresso médio"
        )

        self.content_layout.addWidget(self.summary_frame)

    def create_summary_item(self, parent_layout, value, label):
        item = QFrame()
        item.setObjectName("goalsSummaryItem")

        item_layout = QVBoxLayout(item)
        item_layout.setContentsMargins(16, 12, 16, 12)
        item_layout.setSpacing(4)

        value_label = QLabel(value)
        value_label.setObjectName("goalsSummaryValue")
        value_label.setAlignment(Qt.AlignCenter)

        text_label = QLabel(label)
        text_label.setObjectName("goalsSummaryLabel")
        text_label.setAlignment(Qt.AlignCenter)

        item_layout.addWidget(value_label)
        item_layout.addWidget(text_label)

        parent_layout.addWidget(item)

        return value_label

    def create_goals_list(self):
        self.goals_card = QFrame()
        self.goals_card.setObjectName("goalsListCard")

        layout = QVBoxLayout(self.goals_card)
        layout.setContentsMargins(22, 20, 22, 22)
        layout.setSpacing(18)

        header = QHBoxLayout()

        title = QLabel("Os meus objetivos")
        title.setObjectName("goalsListTitle")

        self.goals_count_label = QLabel("0 objetivos")
        self.goals_count_label.setObjectName("goalsListCount")

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.goals_count_label)

        self.goals_grid = QGridLayout()
        self.goals_grid.setSpacing(16)

        self.empty_label = QLabel("Ainda não tens objetivos criados.")
        self.empty_label.setObjectName("goalsEmptyLabel")
        self.empty_label.setAlignment(Qt.AlignCenter)

        layout.addLayout(header)
        layout.addLayout(self.goals_grid)
        layout.addWidget(self.empty_label)

        self.content_layout.addWidget(self.goals_card)

    def open_goal_form(self, goal=None):
        """Abrir o formulário e guardar um objetivo novo ou editado."""
        steps = []

        if goal:
            steps = self.goal_repository.get_goal_steps(goal["id"])

        dialog = GoalFormDialog(self, goal, steps)

        if dialog.exec() != QDialog.Accepted:
            return

        user = Session.current_user

        if not user:
            return

        data = dialog.get_data()

        if goal:
            self.goal_repository.update_goal(
                goal["id"],
                user["id"],
                data["title"],
                data["description"],
                data["category"],
                data["target_date"],
                0,
                data["status"],
                data["color"],
                data["steps"],
                bool(goal["is_main"]),
            )
        else:
            self.goal_repository.create_goal(
                user["id"],
                data["title"],
                data["description"],
                data["category"],
                data["target_date"],
                0,
                data["status"],
                data["color"],
                data["steps"],
            )

        self.refresh()

    def delete_goal(self, goal):
        """Confirmar e eliminar o objetivo selecionado."""
        confirmed = CustomDialog.confirm(
            self,
            "Tens a certeza que queres eliminar este objetivo?",
            "Eliminar objetivo",
        )

        if not confirmed:
            return

        user = Session.current_user

        if not user:
            return

        self.goal_repository.delete_goal(goal["id"], user["id"])
        self.refresh()

    def toggle_goal_step(self, goal, step, is_completed):
        """Atualizar uma etapa e recalcular o progresso do objetivo."""
        user = Session.current_user

        if not user:
            return

        self.goal_repository.toggle_goal_step(
            step["id"],
            goal["id"],
            user["id"],
            is_completed,
        )

        self.refresh()

    def clear_goals_grid(self):
        while self.goals_grid.count():
            item = self.goals_grid.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

    def refresh(self):
        """Atualizar a interface com os dados do utilizador autenticado."""
        user = Session.current_user

        if not user:
            return

        goals = self.goal_repository.get_goals_by_user(user["id"])

        total_goals = self.goal_repository.count_goals_by_user(user["id"])
        active_goals = self.goal_repository.count_active_goals(user["id"])
        completed_goals = self.goal_repository.count_completed_goals(user["id"])

        if total_goals > 0:
            average_progress = round(
                sum(int(goal["progress"] or 0) for goal in goals) / total_goals
            )
        else:
            average_progress = 0

        self.total_goals_label.setText(str(total_goals))
        self.active_goals_label.setText(str(active_goals))
        self.completed_goals_label.setText(str(completed_goals))
        self.average_progress_label.setText(f"{average_progress}%")

        if total_goals == 1:
            self.goals_count_label.setText("1 objetivo")
        else:
            self.goals_count_label.setText(f"{total_goals} objetivos")

        self.clear_goals_grid()

        self.empty_label.setVisible(total_goals == 0)

        for index, goal in enumerate(goals):
            steps = self.goal_repository.get_goal_steps(goal["id"])

            goal_card = LPGoalCard(
                goal,
                steps=steps,
                on_edit=self.open_goal_form,
                on_delete=self.delete_goal,
                on_step_toggle=self.toggle_goal_step,
                on_set_main=self.set_main_goal,
            )

            row = index // 2
            column = index % 2

            self.goals_grid.addWidget(goal_card, row, column)

        self.goals_grid.setColumnStretch(0, 1)
        self.goals_grid.setColumnStretch(1, 1)

    def set_main_goal(self, goal):
        """Definir o objetivo selecionado como principal."""
        user = Session.current_user

        if not user:
            return

        self.goal_repository.set_main_goal(goal["id"], user["id"])
        self.refresh()