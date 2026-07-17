from datetime import date, datetime

from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QScrollArea,
    QProgressBar,
)

from app.session import Session
from database.task_repository import TaskRepository
from database.event_repository import EventRepository
from database.note_repository import NoteRepository
from database.goal_repository import GoalRepository

class DonutCircle(QWidget):
    """Desenhar um indicador circular de percentagem."""
    def __init__(self, color="#3B82F6"):
        super().__init__()

        self.value = 0
        self.color = color

        self.setFixedSize(126, 126)

    def set_value(self, value):
        self.value = max(0, min(100, int(value)))
        self.update()

    def paintEvent(self, event):
        """Desenhar o componente com os valores atualmente definidos."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = QRectF(16, 16, self.width() - 32, self.height() - 32)

        background_pen = QPen(QColor(148, 163, 184, 45), 12)
        background_pen.setCapStyle(Qt.RoundCap)

        painter.setPen(background_pen)
        painter.drawArc(rect, 0, 360 * 16)

        progress_pen = QPen(QColor(self.color), 12)
        progress_pen.setCapStyle(Qt.RoundCap)

        painter.setPen(progress_pen)

        start_angle = 90 * 16
        span_angle = -int((360 * 16) * (self.value / 100))

        painter.drawArc(rect, start_angle, span_angle)

        painter.setPen(QColor("#F8FAFC"))

        font = painter.font()
        font.setPointSize(18)
        font.setBold(True)
        painter.setFont(font)

        painter.drawText(self.rect(), Qt.AlignCenter, f"{self.value}%")


class ReportDonutCard(QFrame):
    """Combinar um indicador circular com o respetivo resumo textual."""
    def __init__(self, title, subtitle, color):
        super().__init__()

        self.setObjectName("reportsChartCard")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(18)

        self.circle = DonutCircle(color)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(6)

        title_label = QLabel(title)
        title_label.setObjectName("reportsChartTitle")

        self.subtitle_label = QLabel(subtitle)
        self.subtitle_label.setObjectName("reportsChartSubtitle")
        self.subtitle_label.setWordWrap(True)

        text_layout.addStretch()
        text_layout.addWidget(title_label)
        text_layout.addWidget(self.subtitle_label)
        text_layout.addStretch()

        layout.addWidget(self.circle)
        layout.addLayout(text_layout)

    def set_value(self, value, subtitle=None):
        self.circle.set_value(value)

        if subtitle:
            self.subtitle_label.setText(subtitle)

class ReportsPage(QWidget):
    """Calcular e apresentar estatísticas sobre os dados da aplicação."""
    def __init__(self):
        super().__init__()

        self.setObjectName("reportsPage")

        self.task_repository = TaskRepository()
        self.event_repository = EventRepository()
        self.note_repository = NoteRepository()
        self.goal_repository = GoalRepository()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        scroll_area = QScrollArea()
        scroll_area.setObjectName("reportsScrollArea")
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        content = QWidget()
        content.setObjectName("reportsContent")

        self.layout = QVBoxLayout(content)
        self.layout.setContentsMargins(40, 32, 40, 40)
        self.layout.setSpacing(22)

        scroll_area.setWidget(content)
        main_layout.addWidget(scroll_area)

        self.create_header()
        self.create_summary_cards()
        self.create_charts()
        self.create_details_sections()

    def create_header(self):
        header = QHBoxLayout()
        header.setSpacing(16)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)

        title = QLabel("Relatórios")
        title.setObjectName("contentPageTitle")

        subtitle = QLabel("Consulta estatísticas sobre tarefas, eventos, notas e objetivos.")
        subtitle.setObjectName("contentPageSubtitle")

        text_layout.addWidget(title)
        text_layout.addWidget(subtitle)

        header.addLayout(text_layout)
        header.addStretch()

        self.layout.addLayout(header)

    def create_summary_cards(self):
        grid = QGridLayout()
        grid.setSpacing(18)

        self.tasks_value, self.tasks_subtitle = self.create_stat_card(
            grid,
            0,
            0,
            "Tarefas",
            "0",
            "registadas",
            "#3B82F6",
        )

        self.completed_tasks_value, self.completed_tasks_subtitle = self.create_stat_card(
            grid,
            0,
            1,
            "Concluídas",
            "0",
            "tarefas",
            "#10B981",
        )

        self.overdue_tasks_value, self.overdue_tasks_subtitle = self.create_stat_card(
            grid,
            0,
            2,
            "Atrasadas",
            "0",
            "tarefas pendentes",
            "#F87171",
        )

        self.completion_rate_value, self.completion_rate_subtitle = self.create_stat_card(
            grid,
            0,
            3,
            "Conclusão",
            "0%",
            "das tarefas",
            "#F59E0B",
        )

        self.events_value, self.events_subtitle = self.create_stat_card(
            grid,
            1,
            0,
            "Eventos",
            "0",
            "próximos",
            "#3B82F6",
        )

        self.notes_value, self.notes_subtitle = self.create_stat_card(
            grid,
            1,
            1,
            "Notas",
            "0",
            "guardadas",
            "#8B5CF6",
        )

        self.goals_value, self.goals_subtitle = self.create_stat_card(
            grid,
            1,
            2,
            "Objetivos",
            "0",
            "ativos",
            "#10B981",
        )

        self.goal_progress_value, self.goal_progress_subtitle = self.create_stat_card(
            grid,
            1,
            3,
            "Progresso",
            "0%",
            "média dos objetivos",
            "#FBBF24",
        )

        for column in range(4):
            grid.setColumnStretch(column, 1)

        self.layout.addLayout(grid)

    def create_stat_card(self, parent_layout, row, column, title_text, value_text, subtitle_text, accent_color):
        card = QFrame()
        card.setObjectName("reportsStatCard")

        card.setStyleSheet(f"""
            QFrame#reportsStatCard {{
                background-color: rgba(15, 23, 42, 0.86);
                border: 1px solid rgba(148, 163, 184, 0.12);
                border-left: 4px solid {accent_color};
                border-radius: 18px;
            }}
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(8)

        title = QLabel(title_text)
        title.setObjectName("reportsStatTitle")

        value = QLabel(value_text)
        value.setObjectName("reportsStatValue")

        subtitle = QLabel(subtitle_text)
        subtitle.setObjectName("reportsStatSubtitle")

        layout.addWidget(title)
        layout.addWidget(value)
        layout.addWidget(subtitle)

        parent_layout.addWidget(card, row, column)

        return value, subtitle

    def create_details_sections(self):
        sections = QHBoxLayout()
        sections.setSpacing(18)

        tasks_card, tasks_section = self.create_section_card("Resumo de tarefas")
        goals_card, goals_section = self.create_section_card("Resumo de objetivos")
        general_card, general_section = self.create_section_card("Resumo geral")

        self.task_rows = {}
        self.goal_rows = {}
        self.general_rows = {}

        self.add_metric_row(tasks_section, self.task_rows, "Total de tarefas")
        self.add_metric_row(tasks_section, self.task_rows, "Pendentes")
        self.add_metric_row(tasks_section, self.task_rows, "Concluídas")
        self.add_metric_row(tasks_section, self.task_rows, "Atrasadas")

        task_progress_label = QLabel("Taxa de conclusão")
        task_progress_label.setObjectName("reportsProgressLabel")

        self.task_completion_bar = QProgressBar()
        self.task_completion_bar.setObjectName("reportsProgressBar")
        self.task_completion_bar.setRange(0, 100)
        self.task_completion_bar.setTextVisible(False)
        self.task_completion_bar.setFixedHeight(10)

        tasks_section.addSpacing(8)
        tasks_section.addWidget(task_progress_label)
        tasks_section.addWidget(self.task_completion_bar)

        self.add_metric_row(goals_section, self.goal_rows, "Objetivos ativos")
        self.add_metric_row(goals_section, self.goal_rows, "Objetivos concluídos")
        self.add_metric_row(goals_section, self.goal_rows, "Progresso médio")
        self.add_metric_row(goals_section, self.goal_rows, "Objetivo principal")

        goal_progress_label = QLabel("Progresso dos objetivos")
        goal_progress_label.setObjectName("reportsProgressLabel")

        self.goal_average_bar = QProgressBar()
        self.goal_average_bar.setObjectName("reportsProgressBar")
        self.goal_average_bar.setRange(0, 100)
        self.goal_average_bar.setTextVisible(False)
        self.goal_average_bar.setFixedHeight(10)

        goals_section.addSpacing(8)
        goals_section.addWidget(goal_progress_label)
        goals_section.addWidget(self.goal_average_bar)

        self.add_metric_row(general_section, self.general_rows, "Eventos de hoje")
        self.add_metric_row(general_section, self.general_rows, "Próximos eventos")
        self.add_metric_row(general_section, self.general_rows, "Notas guardadas")
        self.add_metric_row(general_section, self.general_rows, "Estado geral")

        sections.addWidget(tasks_card)
        sections.addWidget(goals_card)
        sections.addWidget(general_card)

        self.layout.addLayout(sections)

    def create_section_card(self, title_text):
        card = QFrame()
        card.setObjectName("reportsSectionCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(22, 20, 22, 22)
        layout.setSpacing(14)

        title = QLabel(title_text)
        title.setObjectName("reportsSectionTitle")

        layout.addWidget(title)

        return card, layout

    def add_metric_row(self, section_layout, store, label_text):
        row = QHBoxLayout()
        row.setSpacing(10)

        label = QLabel(label_text)
        label.setObjectName("reportsMetricLabel")

        value = QLabel("-")
        value.setObjectName("reportsMetricValue")
        value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        row.addWidget(label)
        row.addStretch()
        row.addWidget(value)

        section_layout.addLayout(row)

        store[label_text] = value

    def refresh(self):
        """Atualizar a interface com os dados do utilizador autenticado."""
        user = Session.current_user

        if not user:
            return

        user_id = user["id"]

        tasks = self.task_repository.get_tasks_by_user(user_id)
        events = self.event_repository.get_events_by_user(user_id)
        notes_count = self.note_repository.count_notes_by_user(user_id)
        goals = self.goal_repository.get_goals_by_user(user_id)

        total_tasks = len(tasks)
        completed_tasks = [
            task for task in tasks
            if bool(task["is_completed"])
        ]
        pending_tasks = [
            task for task in tasks
            if not bool(task["is_completed"])
        ]
        overdue_tasks = [
            task for task in pending_tasks
            if self.is_task_overdue(task)
        ]

        completed_count = len(completed_tasks)
        pending_count = len(pending_tasks)
        overdue_count = len(overdue_tasks)

        if total_tasks > 0:
            completion_rate = round((completed_count / total_tasks) * 100)
        else:
            completion_rate = 0

        today = date.today()
        today_text = today.strftime("%Y-%m-%d")

        today_events = [
            event for event in events
            if event["event_date"] == today_text
        ]

        upcoming_events = [
            event for event in events
            if self.is_today_or_future(event["event_date"])
        ]

        active_goals = self.goal_repository.count_active_goals(user_id)
        completed_goals = self.goal_repository.count_completed_goals(user_id)

        if goals:
            average_goal_progress = round(
                sum(int(goal["progress"] or 0) for goal in goals) / len(goals)
            )
        else:
            average_goal_progress = 0

        if total_tasks > 0:
            pending_rate = round((pending_count / total_tasks) * 100)
        else:
            pending_rate = 0

        self.task_completion_chart.set_value(
            completion_rate,
            f"{completed_count} de {total_tasks} tarefas concluídas",
        )

        self.pending_tasks_chart.set_value(
            pending_rate,
            f"{pending_count} pendentes · {overdue_count} atrasadas",
        )

        self.goal_progress_chart.set_value(
            average_goal_progress,
            f"{active_goals} ativos · {completed_goals} concluídos",
        )

        main_goal = self.goal_repository.get_main_goal(user_id)

        self.tasks_value.setText(str(total_tasks))
        self.tasks_subtitle.setText("registada" if total_tasks == 1 else "registadas")

        self.completed_tasks_value.setText(str(completed_count))
        self.completed_tasks_subtitle.setText(
            "tarefa concluída" if completed_count == 1 else "tarefas concluídas"
        )

        self.overdue_tasks_value.setText(str(overdue_count))
        self.overdue_tasks_subtitle.setText(
            "tarefa atrasada" if overdue_count == 1 else "tarefas atrasadas"
        )

        self.completion_rate_value.setText(f"{completion_rate}%")
        self.completion_rate_subtitle.setText("das tarefas")

        self.events_value.setText(str(len(upcoming_events)))
        self.events_subtitle.setText(
            "evento próximo" if len(upcoming_events) == 1 else "eventos próximos"
        )

        self.notes_value.setText(str(notes_count))
        self.notes_subtitle.setText(
            "nota guardada" if notes_count == 1 else "notas guardadas"
        )

        self.goals_value.setText(str(active_goals))
        self.goals_subtitle.setText(
            "objetivo ativo" if active_goals == 1 else "objetivos ativos"
        )

        self.goal_progress_value.setText(f"{average_goal_progress}%")
        self.goal_progress_subtitle.setText("média dos objetivos")

        self.task_rows["Total de tarefas"].setText(str(total_tasks))
        self.task_rows["Pendentes"].setText(str(pending_count))
        self.task_rows["Concluídas"].setText(str(completed_count))
        self.task_rows["Atrasadas"].setText(str(overdue_count))

        self.task_completion_bar.setValue(completion_rate)

        self.goal_rows["Objetivos ativos"].setText(str(active_goals))
        self.goal_rows["Objetivos concluídos"].setText(str(completed_goals))
        self.goal_rows["Progresso médio"].setText(f"{average_goal_progress}%")

        if main_goal:
            self.goal_rows["Objetivo principal"].setText(
                f'{main_goal["title"]} · {int(main_goal["progress"] or 0)}%'
            )
        else:
            self.goal_rows["Objetivo principal"].setText("Sem objetivo principal")

        self.goal_average_bar.setValue(average_goal_progress)

        self.general_rows["Eventos de hoje"].setText(str(len(today_events)))
        self.general_rows["Próximos eventos"].setText(str(len(upcoming_events)))
        self.general_rows["Notas guardadas"].setText(str(notes_count))
        self.general_rows["Estado geral"].setText(
            self.get_general_status(
                pending_count,
                overdue_count,
                active_goals,
                average_goal_progress,
            )
        )

    def is_task_overdue(self, task):
        if bool(task["is_completed"]):
            return False

        due_date = task["due_date"]

        if not due_date:
            return False

        try:
            task_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        except ValueError:
            return False

        return task_date < date.today()

    def is_today_or_future(self, date_text):
        if not date_text:
            return False

        try:
            parsed_date = datetime.strptime(date_text, "%Y-%m-%d").date()
        except ValueError:
            return False

        return parsed_date >= date.today()

    def get_general_status(self, pending_tasks, overdue_tasks, active_goals, average_goal_progress):
        if overdue_tasks > 0:
            return "Atenção necessária"

        if pending_tasks == 0 and active_goals == 0:
            return "Tudo organizado"

        if average_goal_progress >= 75:
            return "Bom progresso"

        if pending_tasks > 0 or active_goals > 0:
            return "Em andamento"

        return "Estável"
    

    def create_charts(self):
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(18)

        self.task_completion_chart = ReportDonutCard(
            "Conclusão das tarefas",
            "0 de 0 tarefas concluídas",
            "#10B981",
        )

        self.pending_tasks_chart = ReportDonutCard(
            "Tarefas pendentes",
            "0 tarefas pendentes",
            "#F59E0B",
        )

        self.goal_progress_chart = ReportDonutCard(
            "Progresso dos objetivos",
            "Média geral dos objetivos",
            "#FBBF24",
        )

        charts_layout.addWidget(self.task_completion_chart)
        charts_layout.addWidget(self.pending_tasks_chart)
        charts_layout.addWidget(self.goal_progress_chart)

        self.layout.addLayout(charts_layout)
    
    