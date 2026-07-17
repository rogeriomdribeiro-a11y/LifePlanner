from PySide6.QtCore import Qt, QThread, Signal
from services.weather_service import WeatherService
from PySide6.QtCore import Qt, QThread, Signal, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QWidget,
    QSizePolicy,
)

from app.path import ICONS_DIR

class WeatherWorker(QThread):
    finished = Signal(bool, list)

    def run(self):
        service = WeatherService()
        success, forecast = service.get_week_forecast()
        self.finished.emit(success, forecast)


class WeatherDayWidget(QFrame):
    def __init__(self, day):
        super().__init__()

        self.setObjectName("weatherDayItem")
        self.setToolTip(day["description"])
        self.setFixedSize(116, 32)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        day_label = QLabel(day["day"])
        day_label.setObjectName("weatherDayText")
        day_label.setFixedWidth(30)
        day_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        temp_label = QLabel(
            f'{day["min"]}°/{day["max"]}°'
        )
        temp_label.setObjectName("weatherDayText")
        temp_label.setFixedWidth(52)
        temp_label.setAlignment(Qt.AlignCenter)

        icon_label = QLabel()
        icon_label.setObjectName("weatherIcon")
        icon_label.setFixedSize(22, 22)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setToolTip(day["description"])

        icon_path = ICONS_DIR / "weather" / day["icon"]
        icon_pixmap = QIcon(str(icon_path)).pixmap(QSize(20, 20))
        icon_label.setPixmap(icon_pixmap)

        layout.addWidget(day_label)
        layout.addWidget(temp_label)
        layout.addWidget(icon_label)

class Topbar(QFrame):
    def __init__(self):
        super().__init__()

        self.setObjectName("topbar")
        self.setFixedHeight(74)

        self.weather_worker = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(28, 10, 140, 10)
        layout.setSpacing(0)

        self.weather_card = QFrame()
        self.weather_card.setObjectName("weatherCard")
        self.weather_card.setFixedHeight(46)
        self.weather_card.setMaximumWidth(1200)

        weather_layout = QHBoxLayout(self.weather_card)
        weather_layout.setContentsMargins(18, 8, 18, 8)
        weather_layout.setSpacing(16)

        self.weather_title = QLabel("Braga · 7 dias")
        self.weather_title.setObjectName("weatherTitle")
        self.weather_title.setFixedWidth(100)
        self.weather_title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.weather_title.setToolTip("Previsão meteorológica semanal")

        self.weather_days_container = QWidget()
        self.weather_days_layout = QHBoxLayout(self.weather_days_container)
        self.weather_days_layout.setContentsMargins(0, 0, 0, 0)
        self.weather_days_layout.setSpacing(8)

        self.loading_label = QLabel("A carregar meteorologia...")
        self.loading_label.setObjectName("weatherForecast")

        self.weather_days_layout.addWidget(self.loading_label)

        weather_layout.addWidget(self.weather_title)
        weather_layout.addWidget(self.weather_days_container, stretch=1)

        layout.addStretch()
        layout.addWidget(self.weather_card, stretch=1)
        layout.addStretch()

        self.load_weather()

    def load_weather(self):
        self.clear_weather_days()

        self.loading_label = QLabel("A carregar meteorologia...")
        self.loading_label.setObjectName("weatherForecast")
        self.weather_days_layout.addWidget(self.loading_label)

        self.weather_worker = WeatherWorker()
        self.weather_worker.finished.connect(self.handle_weather_loaded)
        self.weather_worker.start()

    def clear_weather_days(self):
        while self.weather_days_layout.count():
            item = self.weather_days_layout.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()

    def handle_weather_loaded(self, success, forecast):
        self.clear_weather_days()

        if not success or not forecast:
            unavailable_label = QLabel("Meteorologia indisponível")
            unavailable_label.setObjectName("weatherForecast")
            self.weather_days_layout.addWidget(unavailable_label)
            return

        for day in forecast:
            day_widget = WeatherDayWidget(day)
            self.weather_days_layout.addWidget(day_widget)
        

    def refresh_user(self):
        pass