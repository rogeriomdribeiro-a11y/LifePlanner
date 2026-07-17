from PySide6.QtCore import Qt, QDate, QTime, QSize
from PySide6.QtGui import QColor, QPixmap, QPainter, QIcon, QTextCharFormat
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLineEdit,
    QDateEdit,
    QTimeEdit,
    QComboBox,
    QPushButton,
    QGraphicsDropShadowEffect,
    QCalendarWidget,
    QSpinBox,
    QAbstractSpinBox,
)

from app.path import ICONS_DIR


class EventFormDialog(QDialog):
    """Recolher e validar os dados de criação ou edição de um evento."""
    COLORS = {
        "Azul": "#3B82F6",
        "Verde": "#10B981",
        "Roxo": "#8B5CF6",
        "Laranja": "#F59E0B",
        "Vermelho": "#EF4444",
    }

    FIELD_WIDTH = 210

    def __init__(self, parent=None, selected_date=None, event=None):
        super().__init__(parent)

        self.event_data = event

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)
        self.setFixedSize(600, 620)

        wrapper_layout = QVBoxLayout(self)
        wrapper_layout.setContentsMargins(15, 15, 15, 15)

        container = QFrame()
        container.setObjectName("eventDialogContainer")

        shadow = QGraphicsDropShadowEffect(container)
        shadow.setBlurRadius(35)
        shadow.setOffset(0, 5)
        shadow.setColor(QColor(0, 0, 0, 150))
        container.setGraphicsEffect(shadow)

        wrapper_layout.addWidget(container)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(28, 26, 28, 26)
        layout.setSpacing(14)

        title_text = "Editar evento" if event else "Novo evento"

        title = QLabel(title_text)
        title.setObjectName("eventDialogTitle")

        subtitle = QLabel("Preenche os detalhes do evento.")
        subtitle.setObjectName("eventDialogSubtitle")

        self.error_label = QLabel("")
        self.error_label.setObjectName("eventDialogError")

        self.title_input = QLineEdit()
        self.title_input.setObjectName("eventDialogInput")
        self.title_input.setPlaceholderText("Ex: Reunião de equipa")

        self.description_input = QLineEdit()
        self.description_input.setObjectName("eventDialogInput")
        self.description_input.setPlaceholderText("Ex: Revisão semanal do projeto")

        self.location_input = QLineEdit()
        self.location_input.setObjectName("eventDialogInput")
        self.location_input.setPlaceholderText("Ex: Sala 2B")

        self.date_input = QDateEdit()
        self.date_input.setObjectName("eventDialogDate")
        self.date_input.setCalendarPopup(True)
        self.date_input.setFixedWidth(self.FIELD_WIDTH)
        

        calendar_widget = QCalendarWidget()
        calendar_widget.setObjectName("eventDateCalendar")
        calendar_widget.setGridVisible(False)
        calendar_widget.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        

        self.apply_calendar_colors(calendar_widget)

        year_edit = calendar_widget.findChild(QSpinBox, "qt_calendar_yearedit")

        if year_edit:
            year_edit.setFixedWidth(64)
            year_edit.setAlignment(Qt.AlignCenter)
            year_edit.setButtonSymbols(QAbstractSpinBox.NoButtons)
            year_edit.setReadOnly(False)
            year_edit.setCursor(Qt.IBeamCursor)

            if year_edit.lineEdit():
                year_edit.lineEdit().setCursor(Qt.IBeamCursor)

        self.date_input.setCalendarWidget(calendar_widget)

        calendar_icon_path = (ICONS_DIR / "actions" / "calendar.svg").as_posix()

        self.date_input.setStyleSheet(f"""
            QDateEdit#eventDialogDate::drop-down {{
                border: none;
                background-color: transparent;
                width: 34px;
                border-top-right-radius: 10px;
                border-bottom-right-radius: 10px;
            }}

            QDateEdit#eventDialogDate::down-arrow {{
                image: url({calendar_icon_path});
                width: 18px;
                height: 18px;
            }}
        """)

        self.color_input = QComboBox()
        self.color_input.setObjectName("eventDialogCombo")
        self.color_input.setFixedWidth(self.FIELD_WIDTH)
        self.color_input.setIconSize(QSize(14, 14))

        for color_name, color_value in self.COLORS.items():
            self.color_input.addItem(
                self.create_color_icon(color_value),
                color_name
            )

        self.start_time_input = QTimeEdit()
        self.start_time_input.setObjectName("eventDialogTime")
        self.start_time_input.setDisplayFormat("HH:mm")
        self.start_time_input.setFixedWidth(self.FIELD_WIDTH)

        self.end_time_input = QTimeEdit()
        self.end_time_input.setObjectName("eventDialogTime")
        self.end_time_input.setDisplayFormat("HH:mm")
        self.end_time_input.setFixedWidth(self.FIELD_WIDTH)

        fields_grid = QGridLayout()
        fields_grid.setHorizontalSpacing(14)
        fields_grid.setVerticalSpacing(12)

        fields_grid.addLayout(self.create_field("Data", self.date_input), 0, 0)
        fields_grid.addLayout(self.create_field("Cor", self.color_input), 0, 1)
        fields_grid.addLayout(self.create_field("Hora de início", self.start_time_input), 1, 0)
        fields_grid.addLayout(self.create_field("Hora de fim", self.end_time_input), 1, 1)

        fields_grid.setColumnStretch(0, 0)
        fields_grid.setColumnStretch(1, 0)
        fields_grid.setColumnStretch(2, 1)

        buttons = QHBoxLayout()
        buttons.setSpacing(10)
        buttons.addStretch()

        cancel_button = QPushButton("Cancelar")
        cancel_button.setObjectName("eventDialogCancelButton")
        cancel_button.setCursor(Qt.PointingHandCursor)
        cancel_button.setFixedSize(130, 40)
        cancel_button.clicked.connect(self.reject)

        save_text = "Guardar alterações" if event else "Criar evento"

        save_button = QPushButton(save_text)
        save_button.setObjectName("eventDialogPrimaryButton")
        save_button.setCursor(Qt.PointingHandCursor)
        save_button.setFixedSize(170, 40)
        save_button.clicked.connect(self.validate_and_accept)

        buttons.addWidget(cancel_button)
        buttons.addWidget(save_button)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(4)
        layout.addLayout(self.create_field("Título", self.title_input))
        layout.addLayout(self.create_field("Descrição", self.description_input))
        layout.addLayout(self.create_field("Local", self.location_input))
        layout.addLayout(fields_grid)
        layout.addWidget(self.error_label)
        layout.addStretch()
        layout.addLayout(buttons)

        self.load_data(selected_date)

    def create_field(self, label_text, widget):
        field_layout = QVBoxLayout()
        field_layout.setSpacing(6)

        label = QLabel(label_text)
        label.setObjectName("eventDialogFieldLabel")

        field_layout.addWidget(label)
        field_layout.addWidget(widget)

        return field_layout

    def create_color_icon(self, color_value):
        pixmap = QPixmap(14, 14)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(color_value))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(1, 1, 12, 12)
        painter.end()

        return QIcon(pixmap)

    def apply_calendar_colors(self, calendar_widget):
        text_format = QTextCharFormat()
        text_format.setForeground(QColor("#CBD5E1"))

        for weekday in [
            Qt.DayOfWeek.Monday,
            Qt.DayOfWeek.Tuesday,
            Qt.DayOfWeek.Wednesday,
            Qt.DayOfWeek.Thursday,
            Qt.DayOfWeek.Friday,
            Qt.DayOfWeek.Saturday,
            Qt.DayOfWeek.Sunday,
        ]:
            calendar_widget.setWeekdayTextFormat(weekday, text_format)

        today_format = QTextCharFormat()
        today_format.setBackground(QColor("#2563EB"))
        today_format.setForeground(QColor("#FFFFFF"))
        today_format.setFontWeight(700)

        calendar_widget.setDateTextFormat(QDate.currentDate(), today_format)

    def load_data(self, selected_date):
        if self.event_data:
            self.title_input.setText(self.event_data["title"] or "")
            self.description_input.setText(self.event_data["description"] or "")
            self.location_input.setText(self.event_data["location"] or "")

            event_date = QDate.fromString(self.event_data["event_date"], "yyyy-MM-dd")

            if event_date.isValid():
                self.date_input.setDate(event_date)
            else:
                self.date_input.setDate(QDate.currentDate())

            start_time = QTime.fromString(self.event_data["start_time"] or "", "HH:mm")

            if start_time.isValid():
                self.start_time_input.setTime(start_time)
            else:
                self.start_time_input.setTime(QTime.currentTime())

            end_time = QTime.fromString(self.event_data["end_time"] or "", "HH:mm")

            if end_time.isValid():
                self.end_time_input.setTime(end_time)
            else:
                self.end_time_input.setTime(QTime.currentTime().addSecs(3600))

            color_name = self.get_color_name(self.event_data["color"] or "#3B82F6")
            self.color_input.setCurrentText(color_name)

            return

        if selected_date:
            self.date_input.setDate(
                QDate(selected_date.year, selected_date.month, selected_date.day)
            )
        else:
            self.date_input.setDate(QDate.currentDate())

            self.start_time_input.setTime(QTime.currentTime())
            self.end_time_input.setTime(QTime.currentTime().addSecs(3600))
            self.color_input.setCurrentText("Azul")

    def validate_and_accept(self):
        """Validar os campos antes de aceitar o formulário."""
        if not self.title_input.text().strip():
            self.error_label.setText("O título do evento é obrigatório.")
            return

        if self.date_input.date().toJulianDay() < QDate.currentDate().toJulianDay():
            self.error_label.setText("Não é possível adicionar eventos em dias passados.")
            return

        start_time = self.start_time_input.time()
        end_time = self.end_time_input.time()

        if end_time <= start_time:
            self.error_label.setText("A hora de fim deve ser posterior à hora de início.")
            return

        self.accept()

    def get_color_name(self, color_value):
        for name, value in self.COLORS.items():
            if value.lower() == color_value.lower():
                return name

        return "Azul"

    def get_data(self):
        """Devolver os dados normalizados introduzidos no formulário."""
        color_name = self.color_input.currentText()

        return {
            "title": self.title_input.text().strip(),
            "description": self.description_input.text().strip(),
            "location": self.location_input.text().strip(),
            "event_date": self.date_input.date().toString("yyyy-MM-dd"),
            "start_time": self.start_time_input.time().toString("HH:mm"),
            "end_time": self.end_time_input.time().toString("HH:mm"),
            "color": self.COLORS.get(color_name, "#3B82F6"),
        }