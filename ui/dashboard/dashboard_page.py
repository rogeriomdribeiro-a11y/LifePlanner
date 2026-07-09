from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QScrollArea,
)

from app.session import Session
from database.task_repository import TaskRepository
from ui.widgets.info_card import LPInfoCard
from ui.widgets.section import LPSection
from ui.widgets.task_item import LPTaskItem
from ui.widgets.event_item import LPEventItem
from ui.widgets.goal_progress import LPGoalProgress
from database.event_repository import EventRepository
from database.note_repository import NoteRepository

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

        self.task_repository = TaskRepository()
        self.event_repository = EventRepository()
        self.note_repository = NoteRepository()
        self.setObjectName("dashboardPage")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("dashboardScrollArea")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.content = QWidget()
        self.content.setObjectName("dashboardContent")

        self.layout = QVBoxLayout(self.content)
        self.layout.setContentsMargins(40, 32, 40, 40)
        self.layout.setSpacing(18)

        self.scroll_area.setWidget(self.content)
        main_layout.addWidget(self.scroll_area)

        self.create_welcome_card()
        self.create_info_cards()
        self.create_sections()

        self.layout.addStretch()

        self.refresh()

    def create_welcome_card(self):
        self.welcome_card = QFrame()
        self.welcome_card.setObjectName("dashboardWelcomeCard")

        layout = QHBoxLayout(self.welcome_card)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(20)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(6)

        self.welcome_title = QLabel()
        self.welcome_title.setObjectName("dashboardWelcomeTitle")

        self.welcome_subtitle = QLabel("Bem-vindo ao LifePlanner")
        self.welcome_subtitle.setObjectName("dashboardWelcomeSubtitle")

        self.summary_label = QLabel()
        self.summary_label.setObjectName("dashboardWelcomeSummary")

        text_layout.addWidget(self.welcome_title)
        text_layout.addWidget(self.welcome_subtitle)
        text_layout.addWidget(self.summary_label)

        self.date_label = QLabel()
        self.date_label.setObjectName("dashboardDateLabel")
        self.date_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout.addLayout(text_layout)
        layout.addStretch()
        layout.addWidget(self.date_label)

        self.layout.addWidget(self.welcome_card)

    def create_info_cards(self):
        cards_grid = QGridLayout()
        cards_grid.setSpacing(18)

        self.tasks_card = LPInfoCard(
            title="Tarefas",
            value="0",
            subtitle="Para hoje",
            icon_name="tasks.svg",
            accent_color="#3B82F6",
        )

        self.goals_card = LPInfoCard(
            title="Objetivos",
            value="3",
            subtitle="Em progresso",
            icon_name="goals.svg",
            accent_color="#10B981",
        )

        self.notes_card = LPInfoCard(
            title="Notas",
            value="12",
            subtitle="Recentes",
            icon_name="notes.svg",
            accent_color="#8B5CF6",
        )

        self.progress_card = LPInfoCard(
            title="Progresso",
            value="82%",
            subtitle="Esta semana",
            icon_name="reports.svg",
            accent_color="#F59E0B",
        )

        cards = [
            self.tasks_card,
            self.goals_card,
            self.notes_card,
            self.progress_card,
        ]

        for index, card in enumerate(cards):
            card.setMinimumWidth(0)
            cards_grid.addWidget(card, 0, index)
            cards_grid.setColumnStretch(index, 1)

        self.layout.addLayout(cards_grid)

    def create_sections(self):
        sections_grid = QGridLayout()
        sections_grid.setSpacing(18)

        self.events_section = LPSection("Próximos eventos", "Ver calendário")
        self.events_section.setMinimumHeight(230)

        goal_section = LPSection("Objetivo principal", "Ver objetivos")
        goal_section.setMinimumHeight(230)

        goal_section.content_layout.addWidget(
            LPGoalProgress(
                title="Aprender Python",
                subtitle="Estudar 30 minutos por dia",
                progress=80,
                left_info="24 de 30 dias",
                right_info="Termina em 12 dias",
            )
        )

        sections_grid.addWidget(self.events_section, 0, 0)
        sections_grid.addWidget(goal_section, 0, 1)

        sections_grid.setColumnStretch(0, 1)
        sections_grid.setColumnStretch(1, 1)

        self.tasks_section = LPSection("Tarefas de hoje", "Ver +")
        self.tasks_section.setMinimumHeight(260)

        self.layout.addLayout(sections_grid)
        self.layout.addWidget(self.tasks_section)

    def refresh(self):
        self.welcome_title.setText(
            f"{self.get_greeting()}, {self.get_first_name()} "
        )

        self.date_label.setText(self.get_current_date())

        user = Session.current_user

        if not user:
            self.summary_label.setText("Hoje tens 0 tarefas e 0 eventos agendados.")
            return

        user_id = user["id"]

        self.task_repository.ensure_sample_tasks_for_today(user_id)
        self.event_repository.ensure_sample_events_for_today(user_id)

        total_tasks = self.task_repository.count_today_tasks(user_id)
        completed_tasks = self.task_repository.count_completed_today_tasks(user_id)
        total_events = self.event_repository.count_today_events(user_id)
        total_notes = self.note_repository.count_notes_by_user(user_id)

        task_word = "tarefa" if total_tasks == 1 else "tarefas"
        event_word = "evento" if total_events == 1 else "eventos"

        self.summary_label.setText(
            f"Hoje tens {total_tasks} {task_word} e {total_events} {event_word} agendados."
        )

        self.tasks_card.set_value(total_tasks)

        if completed_tasks > 0:
            self.tasks_card.set_subtitle(f"{completed_tasks} concluídas")
        else:
            self.tasks_card.set_subtitle("Para hoje")

        self.load_today_tasks(user_id)
        self.load_today_events(user_id)

        self.notes_card.set_value(total_notes)

        if total_notes == 1:
            self.notes_card.set_subtitle("nota guardada")
        else:
            self.notes_card.set_subtitle("notas guardadas")

    def load_today_events(self, user_id):
        self.clear_layout(self.events_section.content_layout)

        events = self.event_repository.get_today_events(user_id, limit=5)

        if not events:
            self.events_section.add_text_item("Não tens eventos para hoje.")
            return

        for event in events:
            start_time = event["start_time"] or "--:--"
            subtitle = event["location"] or event["description"] or ""

            self.events_section.content_layout.addWidget(
                LPEventItem(
                    start_time,
                    event["title"],
                    subtitle,
                    event["color"] or "#3B82F6",
                )
            )
    def load_today_tasks(self, user_id):
        self.clear_layout(self.tasks_section.content_layout)

        tasks = self.task_repository.get_today_tasks(user_id, limit=5)

        if not tasks:
            self.tasks_section.add_text_item("Ainda não tens tarefas para hoje.")
            return

        for task in tasks:
            category = task["category"] or "Pessoal"

            self.tasks_section.content_layout.addWidget(
                LPTaskItem(
                    task["title"],
                    category,
                    task["due_time"] or "",
                    self.get_category_color(category),
                    task["priority"] or "Normal",
                )
            )
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
        }

        return colors.get(category, "#3B82F6")

    def get_first_name(self):
        user = Session.current_user

        if user and user["full_name"]:
            return user["full_name"].split()[0]

        return "Utilizador"

    def get_greeting(self):
        hour = datetime.now().hour

        if hour < 12:
            return "Bom dia"

        if hour < 20:
            return "Boa tarde"

        return "Boa noite"

    def get_current_date(self):
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

        now = datetime.now()

        weekday = weekdays[now.weekday()]
        month = months[now.month - 1]

        return f"{weekday}, {now.day} de {month}"