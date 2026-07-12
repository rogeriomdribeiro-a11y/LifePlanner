from datetime import date

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QScrollArea,
    QFrame,
    QGraphicsOpacityEffect,
)

from app.session import Session
from app.path import DASHBOARD_IMAGES_DIR
from database.task_repository import TaskRepository
from database.event_repository import EventRepository
from database.note_repository import NoteRepository
from database.goal_repository import GoalRepository
from ui.widgets.info_card import LPInfoCard
from ui.widgets.section import LPSection
from ui.widgets.goal_progress import LPGoalProgress

class DashboardPage(QWidget):
    def __init__(self, on_navigate=None):
        super().__init__()

        self.setObjectName("dashboardPage")
        self.on_navigate = on_navigate

        self.task_repository = TaskRepository()
        self.event_repository = EventRepository()
        self.note_repository = NoteRepository()
        self.goal_repository = GoalRepository()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        scroll_area = QScrollArea()
        scroll_area.setObjectName("dashboardScrollArea")
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        content = QWidget()
        content.setObjectName("dashboardContent")

        self.layout = QVBoxLayout(content)
        self.layout.setContentsMargins(28, 26, 28, 34)
        self.layout.setSpacing(24)

        self.create_welcome_card()
        self.create_info_cards()
        self.create_sections()

        scroll_area.setWidget(content)
        main_layout.addWidget(scroll_area)

    def create_welcome_card(self):
        self.welcome_card = QFrame()
        self.welcome_card.setObjectName("dashboardWelcomeCard")
        self.welcome_card.setMinimumHeight(150)

        image_path = DASHBOARD_IMAGES_DIR / "header_bg_dark.png"

        if image_path.exists():
            self.welcome_card.setStyleSheet(f"""
                QFrame#dashboardWelcomeCard {{
                    border-image: url("{image_path.as_posix()}") 0 0 0 0 stretch stretch;
                    border-radius: 18px;
                    border: 1px solid rgba(148, 163, 184, 0.18);
                }}
            """)

        layout = QVBoxLayout(self.welcome_card)
        layout.setContentsMargins(26, 24, 26, 24)
        layout.setSpacing(8)

        self.welcome_title = QLabel("Olá!")
        self.welcome_title.setObjectName("dashboardWelcomeTitle")

        self.welcome_subtitle = QLabel("")
        self.welcome_subtitle.setObjectName("dashboardWelcomeSubtitle")
        self.welcome_subtitle.setWordWrap(True)

        layout.addStretch()
        layout.addWidget(self.welcome_title)
        layout.addWidget(self.welcome_subtitle)
        layout.addStretch()

        self.layout.addWidget(self.welcome_card)

    def create_info_cards(self):
        cards_grid = QGridLayout()
        cards_grid.setSpacing(18)

        self.tasks_card = LPInfoCard(
            title="Tarefas",
            value="0/0",
            subtitle="sem tarefas hoje",
            icon_name="tasks.svg",
            accent_color="#3B82F6",
        )

        self.goals_card = LPInfoCard(
            title="Objetivos",
            value="0",
            subtitle="objetivos ativos",
            icon_name="goals.svg",
            accent_color="#10B981",
        )

        self.notes_card = LPInfoCard(
            title="Notas",
            value="0",
            subtitle="notas guardadas",
            icon_name="notes.svg",
            accent_color="#8B5CF6",
        )

        self.progress_card = LPInfoCard(
            title="Progresso",
            value="0%",
            subtitle="Objetivos",
            icon_name="reports.svg",
            accent_color="#F59E0B",
        )

        cards_grid.addWidget(self.tasks_card, 0, 0)
        cards_grid.addWidget(self.goals_card, 0, 1)
        cards_grid.addWidget(self.notes_card, 0, 2)
        cards_grid.addWidget(self.progress_card, 0, 3)

        for column in range(4):
            cards_grid.setColumnStretch(column, 1)

        self.layout.addLayout(cards_grid)

    def create_sections(self):
        sections_grid = QGridLayout()
        sections_grid.setSpacing(18)

        self.events_section = LPSection("Próximos eventos", "Ver calendário")
        self.events_section.setMinimumHeight(230)

        self.goal_section = LPSection("Objetivo principal", "Ver objetivos")
        self.goal_section.setObjectName("dashboardGoalSection")
        self.goal_section.setMinimumHeight(230)
        self.goal_section.add_text_item("A carregar objetivo...")

        self.connect_section_action(self.events_section, self.go_to_calendar)
        self.connect_section_action(self.goal_section, self.go_to_goals)

        sections_grid.addWidget(self.events_section, 0, 0)
        sections_grid.addWidget(self.goal_section, 0, 1)

        sections_grid.setColumnStretch(0, 1)
        sections_grid.setColumnStretch(1, 1)

        self.tasks_section = LPSection("Tarefas de hoje", "Ver +")
        self.tasks_section.setMinimumHeight(260)

        self.layout.addLayout(sections_grid)
        self.layout.addWidget(self.tasks_section)

    def connect_section_action(self, section, callback):
        if hasattr(section, "set_action_callback"):
            section.set_action_callback(callback)
            return

        if hasattr(section, "action_button") and section.action_button:
            section.action_button.clicked.connect(callback)

    def go_to_calendar(self):
        if self.on_navigate:
            self.on_navigate("calendar")

    def go_to_goals(self):
        if self.on_navigate:
            self.on_navigate("goals")

    def refresh(self):
        user = Session.current_user

        if not user:
            return

        user_id = user["id"]

        self.update_welcome(user)

        total_tasks = self.task_repository.count_today_tasks(user_id)
        completed_tasks = self.task_repository.count_completed_today_tasks(user_id)
        pending_tasks = max(total_tasks - completed_tasks, 0)

        total_events = self.event_repository.count_today_events(user_id)
        total_notes = self.note_repository.count_notes_by_user(user_id)
        total_goals = self.goal_repository.count_active_goals(user_id)

        goals = self.goal_repository.get_goals_by_user(user_id)

        if goals:
            average_progress = round(
                sum(int(goal["progress"] or 0) for goal in goals) / len(goals)
            )
        else:
            average_progress = 0

        self.tasks_card.set_value(pending_tasks)

        if total_tasks == 0:
            self.tasks_card.set_subtitle("sem tarefas hoje")
        elif completed_tasks == 1:
            self.tasks_card.set_subtitle("1 tarefa concluída")
        else:
            self.tasks_card.set_subtitle(f"{completed_tasks} tarefas concluídas")

        self.goals_card.set_value(total_goals)

        if total_goals == 1:
            self.goals_card.set_subtitle("objetivo ativo")
        else:
            self.goals_card.set_subtitle("objetivos ativos")

        self.notes_card.set_value(total_notes)

        if total_notes == 1:
            self.notes_card.set_subtitle("nota guardada")
        else:
            self.notes_card.set_subtitle("notas guardadas")

        self.progress_card.set_value(f"{average_progress}%")
        self.progress_card.set_subtitle("Objetivos")

        self.load_today_events(user_id)
        self.load_main_goal(user_id)
        self.load_today_tasks(user_id)

    def update_welcome(self, user):
        full_name = user["full_name"] or "Utilizador"
        first_name = full_name.split()[0]

        today = date.today()

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

        weekdays = [
            "segunda-feira",
            "terça-feira",
            "quarta-feira",
            "quinta-feira",
            "sexta-feira",
            "sábado",
            "domingo",
        ]

        formatted_date = (
            f"{weekdays[today.weekday()]}, "
            f"{today.day} de {months[today.month - 1]} de {today.year}"
        )

        self.welcome_title.setText(f"Olá, {first_name} 👋")
        self.welcome_subtitle.setText(
            f"Hoje é {formatted_date}. Organiza o teu dia com clareza."
        )

    def load_today_events(self, user_id):
        self.clear_layout(self.events_section.content_layout)

        events = self.event_repository.get_today_events(user_id)

        if not events:
            self.events_section.add_text_item("Não tens eventos para hoje.")
            return

        for event in events[:4]:
            self.events_section.content_layout.addWidget(
                self.create_event_row(event)
            )

    def load_main_goal(self, user_id):
        self.clear_layout(self.goal_section.content_layout)

        main_goal = self.goal_repository.get_main_goal(user_id)

        if not main_goal:
            self.goal_section.add_text_item("Ainda não tens objetivos ativos.")
            return

        steps = self.goal_repository.get_goal_steps(main_goal["id"])

        total_steps = len(steps)
        completed_steps = sum(1 for step in steps if step["is_completed"])

        progress = int(main_goal["progress"] or 0)

        if total_steps == 1:
            steps_text = f"{completed_steps} de 1 etapa concluída"
        else:
            steps_text = f"{completed_steps} de {total_steps} etapas concluídas"

        goal_widget = LPGoalProgress(
            title=main_goal["title"],
            subtitle=main_goal["description"] or steps_text,
            progress=progress,
            left_info=steps_text,
            right_info=self.format_goal_target_date(main_goal["target_date"]),
        )

        self.goal_section.content_layout.addWidget(goal_widget)

    def load_today_tasks(self, user_id):
        self.clear_layout(self.tasks_section.content_layout)

        tasks = self.task_repository.get_today_tasks(user_id)
        pending_tasks = [task for task in tasks if not bool(task["is_completed"])]

        if not pending_tasks:
            self.tasks_section.add_text_item("Não tens tarefas pendentes para hoje.")
            return

        for task in pending_tasks[:5]:
            self.tasks_section.content_layout.addWidget(
                self.create_task_row(task)
            )

    def create_task_row(self, task):
        row = QFrame()
        row.setObjectName("dashboardTaskRow")

        row.setStyleSheet("""
            QFrame#dashboardTaskRow {
                background-color: rgba(30, 41, 59, 0.48);
                border: 1px solid rgba(148, 163, 184, 0.10);
                border-radius: 12px;
            }

            QLabel#dashboardTaskTitle {
                color: #F8FAFC;
                font-size: 13px;
                font-weight: 700;
            }

            QLabel#dashboardTaskMeta {
                color: #94A3B8;
                font-size: 12px;
                font-weight: 600;
            }

            QLabel#dashboardTaskCategory {
                border-radius: 8px;
                padding: 4px 9px;
                font-size: 11px;
                font-weight: 700;
            }

            QLabel#dashboardTaskPriority {
                background-color: rgba(245, 158, 11, 0.14);
                color: #F59E0B;
                border-radius: 8px;
                padding: 4px 9px;
                font-size: 11px;
                font-weight: 700;
            }
        """)

        layout = QHBoxLayout(row)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(12)

        texts = QVBoxLayout()
        texts.setSpacing(3)

        title = QLabel(task["title"])
        title.setObjectName("dashboardTaskTitle")
        title.setWordWrap(True)

        due_time = task["due_time"] or "Sem hora"

        meta = QLabel(due_time)
        meta.setObjectName("dashboardTaskMeta")

        texts.addWidget(title)
        texts.addWidget(meta)

        category_text = task["category"] or "Geral"
        category_color = self.get_category_color(category_text)

        category = QLabel(category_text)
        category.setObjectName("dashboardTaskCategory")
        category.setStyleSheet(f"""
            QLabel#dashboardTaskCategory {{
                background-color: {self.hex_to_rgba(category_color, 0.16)};
                color: {category_color};
                border-radius: 8px;
                padding: 4px 9px;
                font-size: 11px;
                font-weight: 700;
            }}
        """)

        priority = QLabel(task["priority"] or "Normal")
        priority.setObjectName("dashboardTaskPriority")

        layout.addLayout(texts)
        layout.addStretch()
        layout.addWidget(category)
        layout.addWidget(priority)

        return row

    def create_event_row(self, event):
        row = QFrame()
        row.setObjectName("dashboardEventRow")

        color = event["color"] or "#3B82F6"

        row.setStyleSheet(f"""
            QFrame#dashboardEventRow {{
                background-color: rgba(30, 41, 59, 0.48);
                border: 1px solid rgba(148, 163, 184, 0.10);
                border-left: 4px solid {color};
                border-radius: 12px;
            }}

            QLabel#dashboardEventTitle {{
                color: #F8FAFC;
                font-size: 13px;
                font-weight: 700;
            }}

            QLabel#dashboardEventMeta {{
                color: #94A3B8;
                font-size: 12px;
                font-weight: 600;
            }}
        """)

        layout = QVBoxLayout(row)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(3)

        title = QLabel(event["title"])
        title.setObjectName("dashboardEventTitle")
        title.setWordWrap(True)

        start_time = event["start_time"] or "--:--"
        end_time = event["end_time"] or "--:--"

        if event["location"]:
            meta_text = f"{start_time} - {end_time} · {event['location']}"
        else:
            meta_text = f"{start_time} - {end_time}"

        meta = QLabel(meta_text)
        meta.setObjectName("dashboardEventMeta")

        layout.addWidget(title)
        layout.addWidget(meta)

        return row

    def format_goal_target_date(self, target_date):
        if not target_date:
            return "Sem data objetivo"

        try:
            year, month, day = target_date.split("-")
            return f"Termina em {day}/{month}/{year}"
        except ValueError:
            return target_date

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

    def get_category_color(self, category):
        colors = {
            "Pessoal": "#3B82F6",
            "Trabalho": "#10B981",
            "Saúde": "#8B5CF6",
            "Estudo": "#F59E0B",
            "Geral": "#94A3B8",
        }

        return colors.get(category, "#94A3B8")

    def hex_to_rgba(self, hex_color, opacity=0.16):
        hex_color = hex_color.replace("#", "")

        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)

        return f"rgba({r}, {g}, {b}, {opacity})"