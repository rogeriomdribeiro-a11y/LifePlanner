from datetime import datetime, date

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QProgressBar,
    QCheckBox,
)

from app.path import ICONS_DIR


def hex_to_rgba(hex_color, opacity=0.16):
    hex_color = hex_color.replace("#", "")

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return f"rgba({r}, {g}, {b}, {opacity})"


class LPGoalCard(QFrame):
    def __init__(
        self,
        goal,
        steps=None,
        on_edit=None,
        on_delete=None,
        on_step_toggle=None,
        on_set_main=None,
    ):
        super().__init__()

        self.goal = goal
        self.steps = steps or []
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.on_step_toggle = on_step_toggle
        self.on_set_main = on_set_main
        self.is_main = bool(goal["is_main"])

        self.goal_color = goal["color"] or "#10B981"
        self.progress = int(goal["progress"] or 0)
        self.status = goal["status"] or "Em progresso"

        self.setObjectName("goalCard")
        self.setMinimumHeight(240)

        self.setStyleSheet(f"""
            QFrame#goalCard {{
                background-color: rgba(15, 23, 42, 0.92);
                border: 1px solid {hex_to_rgba(self.goal_color, 0.42)};
                border-radius: 18px;
            }}

            QFrame#goalCard:hover {{
                border: 1px solid {hex_to_rgba(self.goal_color, 0.72)};
                background-color: rgba(15, 23, 42, 1);
            }}

            QProgressBar#goalCardProgressBar {{
                background-color: rgba(148, 163, 184, 0.16);
                border: none;
                border-radius: 6px;
                height: 10px;
                text-align: center;
            }}

            QProgressBar#goalCardProgressBar::chunk {{
                background-color: {self.goal_color};
                border-radius: 6px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        header = QHBoxLayout()
        header.setSpacing(8)

        title = QLabel(goal["title"])
        title.setObjectName("goalCardTitle")
        title.setWordWrap(True)

        status_badge = QLabel(self.status)
        status_badge.setObjectName("goalCardStatus")
        status_badge.setStyleSheet(self.get_status_style())

        header.addWidget(title)
        header.addStretch()
        header.addWidget(status_badge)

        description_text = goal["description"] or "Sem descrição."

        if len(description_text) > 110:
            description_text = description_text[:107] + "..."

        description = QLabel(description_text)
        description.setObjectName("goalCardDescription")
        description.setWordWrap(True)

        meta = QHBoxLayout()
        meta.setSpacing(8)

        category = QLabel(goal["category"] or "Pessoal")
        category.setObjectName("goalCardCategory")
        category.setStyleSheet(f"""
            QLabel#goalCardCategory {{
                background-color: {hex_to_rgba(self.goal_color, 0.16)};
                color: {self.goal_color};
                border-radius: 8px;
                padding: 4px 10px;
                font-size: 11px;
                font-weight: 700;
            }}
        """)

        date_label = QLabel(self.format_target_date(goal["target_date"]))
        date_label.setObjectName("goalCardDate")

        meta.addWidget(category)
        meta.addWidget(date_label)
        meta.addStretch()

        progress_row = QHBoxLayout()
        progress_row.setSpacing(8)

        steps_done = sum(1 for step in self.steps if step["is_completed"])
        total_steps = len(self.steps)

        progress_label = QLabel(f"{steps_done}/{total_steps} etapas concluídas")
        progress_label.setObjectName("goalCardProgressLabel")

        progress_value = QLabel(f"{self.progress}%")
        progress_value.setObjectName("goalCardProgressValue")

        progress_row.addWidget(progress_label)
        progress_row.addStretch()
        progress_row.addWidget(progress_value)

        progress_bar = QProgressBar()
        progress_bar.setObjectName("goalCardProgressBar")
        progress_bar.setRange(0, 100)
        progress_bar.setValue(self.progress)
        progress_bar.setTextVisible(False)
        progress_bar.setFixedHeight(10)

        steps_title = QLabel("Etapas")
        steps_title.setObjectName("goalCardStepsTitle")

        steps_layout = QVBoxLayout()
        steps_layout.setSpacing(6)

        for step in self.steps:
            steps_layout.addWidget(self.create_step_row(step))

        footer = QHBoxLayout()
        footer.setSpacing(8)

        footer.addStretch()

        main_button = QPushButton()
        main_button.setObjectName("goalMainButtonActive" if self.is_main else "goalMainButton")
        main_button.setCursor(Qt.PointingHandCursor)
        main_button.setFixedSize(34, 34)

        main_icon = "main-goal.svg" if self.is_main else "main-goal-inactive.svg"

        main_button.setIcon(QIcon(str(ICONS_DIR / "actions" / main_icon)))
        main_button.setIconSize(QSize(18, 18))

        if self.is_main:
            main_button.setToolTip("Objetivo principal")
        else:
            main_button.setToolTip("Definir como objetivo principal")

        main_button.clicked.connect(self.handle_set_main)

        edit_button = QPushButton()
        edit_button.setObjectName("goalIconButton")
        edit_button.setCursor(Qt.PointingHandCursor)
        edit_button.setFixedSize(34, 34)
        edit_button.setIcon(QIcon(str(ICONS_DIR / "actions" / "edit.svg")))
        edit_button.setIconSize(QSize(18, 18))
        edit_button.clicked.connect(self.handle_edit)

        delete_button = QPushButton()
        delete_button.setObjectName("goalIconDangerButton")
        delete_button.setCursor(Qt.PointingHandCursor)
        delete_button.setFixedSize(34, 34)
        delete_button.setIcon(QIcon(str(ICONS_DIR / "actions" / "trash.svg")))
        delete_button.setIconSize(QSize(18, 18))
        delete_button.clicked.connect(self.handle_delete)

        footer.addWidget(edit_button)
        footer.addWidget(delete_button)

        footer.addWidget(main_button)
        footer.addWidget(edit_button)
        footer.addWidget(delete_button)

        layout.addLayout(header)
        layout.addWidget(description)
        layout.addLayout(meta)
        layout.addSpacing(2)
        layout.addLayout(progress_row)
        layout.addWidget(progress_bar)
        layout.addSpacing(6)
        layout.addWidget(steps_title)
        layout.addLayout(steps_layout)
        layout.addStretch()
        layout.addLayout(footer)

    def create_step_row(self, step):
        row = QFrame()
        row.setObjectName("goalStepRow")

        layout = QHBoxLayout(row)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(8)

        checkbox = QCheckBox()
        checkbox.setObjectName("goalStepCheckbox")
        checkbox.setChecked(bool(step["is_completed"]))
        checkbox.setCursor(Qt.PointingHandCursor)
        checkbox.stateChanged.connect(
            lambda state, current_step=step: self.handle_step_toggle(
                current_step,
                state == Qt.Checked.value
            )
        )

        texts = QVBoxLayout()
        texts.setSpacing(2)

        title = QLabel(step["title"])
        title.setObjectName(
            "goalStepTitleDone" if step["is_completed"] else "goalStepTitle"
        )
        title.setWordWrap(True)

        texts.addWidget(title)

        if step["description"]:
            description = QLabel(step["description"])
            description.setObjectName("goalStepDescription")
            description.setWordWrap(True)
            texts.addWidget(description)

        layout.addWidget(checkbox)
        layout.addLayout(texts)
        layout.addStretch()

        return row

    def get_status_style(self):
        if self.status == "Concluído":
            return """
                QLabel#goalCardStatus {
                    background-color: rgba(16, 185, 129, 0.16);
                    color: #10B981;
                    border-radius: 8px;
                    padding: 4px 10px;
                    font-size: 11px;
                    font-weight: 700;
                }
            """

        if self.status == "Pausado":
            return """
                QLabel#goalCardStatus {
                    background-color: rgba(245, 158, 11, 0.16);
                    color: #F59E0B;
                    border-radius: 8px;
                    padding: 4px 10px;
                    font-size: 11px;
                    font-weight: 700;
                }
            """

        return """
            QLabel#goalCardStatus {
                background-color: rgba(59, 130, 246, 0.16);
                color: #60A5FA;
                border-radius: 8px;
                padding: 4px 10px;
                font-size: 11px;
                font-weight: 700;
            }
        """

    def format_target_date(self, target_date):
        if not target_date:
            return "Sem data"

        try:
            parsed_date = datetime.strptime(target_date, "%Y-%m-%d").date()
        except ValueError:
            return target_date

        today = date.today()
        delta = (parsed_date - today).days

        if delta == 0:
            return "Hoje"

        if delta == 1:
            return "Amanhã"

        if delta < 0:
            return "Em atraso"

        return parsed_date.strftime("%d/%m/%Y")

    def handle_step_toggle(self, step, is_completed):
        if self.on_step_toggle:
            self.on_step_toggle(self.goal, step, is_completed)

    def handle_edit(self):
        if self.on_edit:
            self.on_edit(self.goal)

    def handle_delete(self):
        if self.on_delete:
            self.on_delete(self.goal)

    def handle_set_main(self):
        if self.is_main:
            return

        if self.on_set_main:
            self.on_set_main(self.goal)