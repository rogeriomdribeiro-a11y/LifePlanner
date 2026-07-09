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
from ui.widgets.info_card import LPInfoCard
from ui.widgets.section import LPSection
from ui.widgets.task_item import LPTaskItem
from ui.widgets.event_item import LPEventItem
from ui.widgets.goal_progress import LPGoalProgress


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

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

        self.summary_label = QLabel("Hoje tens 5 tarefas e 2 eventos agendados.")
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

        cards = [
            LPInfoCard(
                title="Tarefas",
                value="5",
                subtitle="Para hoje",
                icon_name="tasks.svg",
                accent_color="#3B82F6",
            ),
            LPInfoCard(
                title="Objetivos",
                value="3",
                subtitle="Em progresso",
                icon_name="goals.svg",
                accent_color="#10B981",
            ),
            LPInfoCard(
                title="Notas",
                value="12",
                subtitle="Recentes",
                icon_name="notes.svg",
                accent_color="#8B5CF6",
            ),
            LPInfoCard(
                title="Progresso",
                value="82%",
                subtitle="Esta semana",
                icon_name="reports.svg",
                accent_color="#F59E0B",
            ),
        ]

        for index, card in enumerate(cards):
            card.setMinimumWidth(0)
            cards_grid.addWidget(card, 0, index)
            cards_grid.setColumnStretch(index, 1)

        self.layout.addLayout(cards_grid)

    def create_sections(self):
        sections_grid = QGridLayout()
        sections_grid.setSpacing(18)

        events_section = LPSection("Próximos eventos", "Ver calendário")
        events_section.setMinimumHeight(230)
        events_section.content_layout.addWidget(
        LPEventItem("15:00", "Reunião de equipa", "Sala 2B", "#3B82F6")
        )

        events_section.content_layout.addWidget(
            LPEventItem("18:30", "Ginásio", "Treino de força", "#10B981")
        )

        events_section.content_layout.addWidget(
            LPEventItem("20:00", "Aniversário da Ana", "Jantar", "#8B5CF6")
        )

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

        sections_grid.addWidget(events_section, 0, 0)
        sections_grid.addWidget(goal_section, 0, 1)

        sections_grid.setColumnStretch(0, 1)
        sections_grid.setColumnStretch(1, 1)

        tasks_section = LPSection("Tarefas de hoje", "Ver +")
        tasks_section.setMinimumHeight(260)

        tasks_section.content_layout.addWidget(
            LPTaskItem("Comprar leite", "Pessoal", "09:00", "#3B82F6")
            )

        tasks_section.content_layout.addWidget(
            LPTaskItem("Preparar apresentação", "Trabalho", "11:30", "#10B981")
            )

        tasks_section.content_layout.addWidget(
            LPTaskItem("Marcar consulta", "Saúde", "14:00", "#8B5CF6")
            )

        tasks_section.content_layout.addWidget(
            LPTaskItem("Responder a e-mails", "Trabalho", "16:00", "#10B981")
            )

        tasks_section.content_layout.addWidget(
            LPTaskItem("Rever relatório mensal", "Trabalho", "17:30", "#10B981")
            )

        self.layout.addLayout(sections_grid)
        self.layout.addWidget(tasks_section)

    def refresh(self):
        self.welcome_title.setText(
            f"{self.get_greeting()}, {self.get_first_name()}"
        )

        self.date_label.setText(self.get_current_date())

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