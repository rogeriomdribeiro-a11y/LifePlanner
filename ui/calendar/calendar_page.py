import calendar
from datetime import date
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QScrollArea,
    QDialog,
)

from app.session import Session
from database.event_repository import EventRepository
from ui.dialogs.custom_dialog import CustomDialog
from ui.dialogs.event_form_dialog import EventFormDialog
from ui.dialogs.event_details_dialog import EventDetailsDialog
from ui.dialogs.day_events_dialog import DayEventsDialog
from app.path import ICONS_DIR

class CalendarDayCell(QFrame):
    """Representar um dia e os respetivos eventos no calendário mensal."""
    def __init__(self, day_date, current_month, is_today=False, on_click=None):
        super().__init__()

        self.day_date = day_date
        self.current_month = current_month
        self.on_click = on_click

        self.setCursor(Qt.PointingHandCursor)

        if is_today:
            self.setObjectName("calendarDayCellToday")
        elif not current_month:
            self.setObjectName("calendarDayCellMuted")
        else:
            self.setObjectName("calendarDayCell")

        self.setMinimumHeight(105)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(5)

        day_label = QLabel(str(day_date.day))

        if is_today:
            day_label.setObjectName("calendarDayNumberToday")
        elif not current_month:
            day_label.setObjectName("calendarDayNumberMuted")
        else:
            day_label.setObjectName("calendarDayNumber")

        day_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(day_label, alignment=Qt.AlignTop | Qt.AlignCenter)

        self.events_layout = QVBoxLayout()
        self.events_layout.setSpacing(4)

        layout.addLayout(self.events_layout)
        layout.addStretch()

    def mousePressEvent(self, event):
        if self.on_click and event.button() == Qt.LeftButton:
            self.on_click(self.day_date)

        super().mousePressEvent(event)

    def add_event(self, event, callback):
        color = event["color"] or "#3B82F6"
        title = event["title"]
        start_time = event["start_time"] or ""

        if start_time:
            display_text = f"{start_time}  {title}"
        else:
            display_text = title

        if len(display_text) > 22:
            display_text = display_text[:20] + "..."

        event_button = QPushButton(display_text)
        event_button.setObjectName("calendarEventBadge")
        event_button.setCursor(Qt.PointingHandCursor)
        event_button.setFixedHeight(22)
        event_button.setToolTip(event["title"])

        event_button.setAttribute(Qt.WA_NoMousePropagation, True)

        event_button.setStyleSheet(f"""
            QPushButton#calendarEventBadge {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 10px;
                font-weight: 700;
                padding: 2px 6px;
                text-align: left;
            }}

            QPushButton#calendarEventBadge:hover {{
                background-color: {color};
                border: 1px solid rgba(255, 255, 255, 0.35);
            }}
        """)

        event_button.clicked.connect(
            lambda: callback(event)
        )

        self.events_layout.addWidget(event_button)

    def add_more_button(self, count, events, callback):
        button = QPushButton(f"+{count} eventos")
        button.setObjectName("calendarMoreEventsButton")
        button.setCursor(Qt.PointingHandCursor)
        button.setAttribute(Qt.WA_NoMousePropagation, True)

        button.clicked.connect(
            lambda: callback(events)
        )

        self.events_layout.addWidget(button)


class CalendarPage(QWidget):
    """Apresentar e gerir os eventos numa vista mensal."""
    MONTHS = [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]

    WEEKDAYS = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

    def __init__(self):
        super().__init__()

        self.event_repository = EventRepository()

        today = date.today()
        self.current_year = today.year
        self.current_month = today.month

        self.setObjectName("calendarPage")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("calendarScrollArea")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.content = QWidget()
        self.content.setObjectName("calendarContent")

        self.layout = QVBoxLayout(self.content)
        self.layout.setContentsMargins(40, 32, 40, 40)
        self.layout.setSpacing(18)

        self.scroll_area.setWidget(self.content)
        main_layout.addWidget(self.scroll_area)

        self.create_header()
        self.create_calendar()

    def create_header(self):
        header = QHBoxLayout()
        header.setSpacing(16)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)

        title = QLabel("Calendário")
        title.setObjectName("calendarPageTitle")

        subtitle = QLabel("Organiza os teus eventos numa vista mensal.")
        subtitle.setObjectName("calendarPageSubtitle")

        text_layout.addWidget(title)
        text_layout.addWidget(subtitle)

        new_event_button = QPushButton("+ Novo evento")
        new_event_button.setObjectName("calendarPrimaryButton")
        new_event_button.setCursor(Qt.PointingHandCursor)
        new_event_button.setFixedSize(160, 42)
        new_event_button.clicked.connect(
            lambda: self.open_event_form(selected_date=date.today())
        )

        header.addLayout(text_layout)
        header.addStretch()
        header.addWidget(new_event_button)

        self.layout.addLayout(header)

    def create_calendar(self):
        calendar_card = QFrame()
        calendar_card.setObjectName("calendarMonthCard")

        card_layout = QVBoxLayout(calendar_card)
        card_layout.setContentsMargins(22, 20, 22, 22)
        card_layout.setSpacing(18)

        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        today_button = QPushButton("Hoje")
        today_button.setObjectName("calendarTodayButton")
        today_button.setCursor(Qt.PointingHandCursor)
        today_button.clicked.connect(self.go_today)

        previous_button = QPushButton()
        previous_button.setObjectName("calendarNavIconButton")
        previous_button.setCursor(Qt.PointingHandCursor)
        previous_button.setFixedSize(38, 38)
        previous_button.setIcon(QIcon(str(ICONS_DIR / "actions" / "chevron-left.svg")))
        previous_button.setIconSize(QSize(18, 18))
        previous_button.clicked.connect(self.previous_month)

        next_button = QPushButton()
        next_button.setObjectName("calendarNavIconButton")
        next_button.setCursor(Qt.PointingHandCursor)
        next_button.setFixedSize(38, 38)
        next_button.setIcon(QIcon(str(ICONS_DIR / "actions" / "chevron-right.svg")))
        next_button.setIconSize(QSize(18, 18))
        next_button.clicked.connect(self.next_month)

        self.month_label = QLabel()
        self.month_label.setObjectName("calendarMonthTitle")
        self.month_label.setAlignment(Qt.AlignCenter)

        view_button = QPushButton("Mês")
        view_button.setObjectName("calendarViewButton")

        toolbar.addWidget(today_button)
        toolbar.addWidget(previous_button)
        toolbar.addWidget(next_button)
        toolbar.addStretch()
        toolbar.addWidget(self.month_label)
        toolbar.addStretch()
        toolbar.addWidget(view_button)

        self.calendar_grid = QGridLayout()
        self.calendar_grid.setSpacing(0)

        card_layout.addLayout(toolbar)
        card_layout.addLayout(self.calendar_grid)

        self.layout.addWidget(calendar_card)
        self.layout.addStretch()

    def open_event_form(self, selected_date=None, event=None):
        """Abrir o formulário e guardar um evento novo ou editado."""
        user = Session.current_user

        if not user:
            return

        dialog = EventFormDialog(
            self,
            selected_date=selected_date,
            event=event,
        )

        if dialog.exec() != QDialog.Accepted:
            return

        data = dialog.get_data()

        if event:
            self.event_repository.update_event(
                event_id=event["id"],
                user_id=user["id"],
                title=data["title"],
                description=data["description"],
                event_date=data["event_date"],
                start_time=data["start_time"],
                end_time=data["end_time"],
                location=data["location"],
                color=data["color"],
            )
        else:
            self.event_repository.create_event(
                user_id=user["id"],
                title=data["title"],
                description=data["description"],
                event_date=data["event_date"],
                start_time=data["start_time"],
                end_time=data["end_time"],
                location=data["location"],
                color=data["color"],
            )

        event_qdate = dialog.date_input.date()
        self.current_year = event_qdate.year()
        self.current_month = event_qdate.month()

        self.refresh()

    def handle_day_click(self, day_date):
        """Validar a data selecionada antes de criar um evento."""
        if day_date < date.today():
            CustomDialog.warning(
                self,
                "Não é possível criar eventos em datas passadas.",
                "Data inválida"
            )
            return

        self.open_event_form(selected_date=day_date)

    def handle_event_click(self, event):
        """Processar a ação escolhida nos detalhes de um evento."""
        dialog = EventDetailsDialog(self, event)

        if dialog.exec() != QDialog.Accepted:
            return

        if dialog.action == "edit":
            self.open_event_form(event=event)
            return

        if dialog.action == "delete":
            self.delete_event(event)

    def handle_more_events_click(self, events):
        dialog = DayEventsDialog(self, events)

        if dialog.exec() != QDialog.Accepted:
            return

        if not dialog.selected_event:
            return

        self.handle_event_click(dialog.selected_event)

    def delete_event(self, event):
        """Confirmar e eliminar o evento selecionado."""
        user = Session.current_user

        if not user:
            return

        confirmed = CustomDialog.confirm(
            self,
            f'Tens a certeza que queres eliminar o evento "{event["title"]}"?',
            "Eliminar evento",
            "Eliminar",
            "Cancelar",
            "warning",
            True,
        )

        if not confirmed:
            return

        self.event_repository.delete_event(
            event_id=event["id"],
            user_id=user["id"],
        )

        self.refresh()

    def refresh(self):
        """Atualizar a interface com os dados do utilizador autenticado."""
        self.month_label.setText(
            f"{self.MONTHS[self.current_month - 1]} {self.current_year}"
        )

        self.clear_layout(self.calendar_grid)
        self.populate_calendar()

    def populate_calendar(self):
        """Construir a grelha mensal e distribuir os eventos por data."""
        user = Session.current_user

        events_by_date = {}

        if user:
            events = self.event_repository.get_events_by_user(user["id"])

            for event in events:
                events_by_date.setdefault(event["event_date"], []).append(event)

        month_calendar = calendar.Calendar(firstweekday=0).monthdatescalendar(
            self.current_year,
            self.current_month,
        )

        for column, weekday in enumerate(self.WEEKDAYS):
            label = QLabel(weekday)
            label.setObjectName("calendarWeekday")
            label.setAlignment(Qt.AlignCenter)
            self.calendar_grid.addWidget(label, 0, column)

        today = date.today()

        for row_index, week in enumerate(month_calendar, start=1):
            for column_index, day_date in enumerate(week):
                is_current_month = day_date.month == self.current_month
                is_today = day_date == today

                cell = CalendarDayCell(
                    day_date,
                    is_current_month,
                    is_today,
                    self.handle_day_click,
                )

                day_events = events_by_date.get(day_date.isoformat(), [])

                for event in day_events[:3]:
                    cell.add_event(event, self.handle_event_click)

                if len(day_events) > 3:
                    cell.add_more_button(
                        len(day_events) - 3,
                        day_events,
                        self.handle_more_events_click,
                    )

                self.calendar_grid.addWidget(cell, row_index, column_index)

    def previous_month(self):
        self.current_month -= 1

        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1

        self.refresh()

    def next_month(self):
        self.current_month += 1

        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1

        self.refresh()

    def go_today(self):
        today = date.today()

        self.current_year = today.year
        self.current_month = today.month

        self.refresh()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()