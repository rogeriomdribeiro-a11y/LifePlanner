"""Barra superior com a previsão meteorológica semanal."""

from PySide6.QtCore import QCoreApplication, QSize, Qt, QThread, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget

from app.path import ICONS_DIR
from services.weather_service import WeatherService


WEATHER_ICONS_DIR = ICONS_DIR / "weather"


class WeatherWorker(QThread):
    """Executar a chamada de rede sem bloquear a interface gráfica."""

    forecast_ready = Signal(bool, list)

    def run(self):
        success, forecast = WeatherService().get_week_forecast()
        self.forecast_ready.emit(success, forecast)


class WeatherDayWidget(QFrame):
    """Apresentar o dia, temperaturas e ícone de uma previsão diária."""

    def __init__(self, day):
        super().__init__()
        description = day.get("description", "Estado do tempo indisponível")

        self.setObjectName("weatherDayItem")
        self.setToolTip(description)
        self.setFixedSize(116, 32)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        day_label = QLabel(day.get("day", ""))
        day_label.setObjectName("weatherDayText")
        day_label.setFixedWidth(30)
        day_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        temp_label = QLabel(f'{day.get("min", 0)}°/{day.get("max", 0)}°')
        temp_label.setObjectName("weatherDayText")
        temp_label.setFixedWidth(52)
        temp_label.setAlignment(Qt.AlignCenter)

        icon_label = QLabel()
        icon_label.setObjectName("weatherIcon")
        icon_label.setFixedSize(22, 22)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setToolTip(description)

        icon_path = WEATHER_ICONS_DIR / day.get("icon", "cloudy.svg")
        if not icon_path.is_file():
            icon_path = WEATHER_ICONS_DIR / "cloudy.svg"
        icon_label.setPixmap(QIcon(str(icon_path)).pixmap(QSize(20, 20)))

        layout.addWidget(day_label)
        layout.addWidget(temp_label)
        layout.addWidget(icon_label)


class Topbar(QFrame):
    """Carregar e apresentar sete dias de meteorologia de forma assíncrona."""

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
        self.weather_days_layout.setAlignment(Qt.AlignCenter)

        weather_layout.addWidget(self.weather_title)
        weather_layout.addWidget(self.weather_days_container, stretch=1)
        layout.addStretch()
        layout.addWidget(self.weather_card, stretch=1)
        layout.addStretch()

        application = QCoreApplication.instance()
        if application:
            application.aboutToQuit.connect(self.shutdown)

        self.load_weather()

    def load_weather(self):
        """Iniciar uma consulta apenas quando não existe outra em execução."""
        if self.weather_worker and self.weather_worker.isRunning():
            return

        self.clear_weather_days()
        loading_label = QLabel("A carregar meteorologia...")
        loading_label.setObjectName("weatherForecast")
        self.weather_days_layout.addWidget(loading_label)

        worker = WeatherWorker(self)
        self.weather_worker = worker
        worker.forecast_ready.connect(self.handle_weather_loaded)
        worker.finished.connect(self.release_weather_worker)
        worker.start()

    def clear_weather_days(self):
        while self.weather_days_layout.count():
            item = self.weather_days_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def handle_weather_loaded(self, success, forecast):
        """Substituir o estado de carregamento pelos dados ou por um aviso."""
        self.clear_weather_days()

        if not success or not forecast:
            unavailable_label = QLabel("Meteorologia indisponível")
            unavailable_label.setObjectName("weatherForecast")
            self.weather_days_layout.addWidget(unavailable_label)
            return

        for day in forecast:
            self.weather_days_layout.addWidget(WeatherDayWidget(day))

    def release_weather_worker(self):
        """Libertar a thread terminada para permitir uma atualização futura."""
        worker = self.sender()
        if worker is self.weather_worker:
            self.weather_worker = None
        if worker:
            worker.deleteLater()

    def shutdown(self):
        """Aguardar brevemente pela thread antes de destruir a aplicação."""
        if self.weather_worker and self.weather_worker.isRunning():
            self.weather_worker.requestInterruption()
            self.weather_worker.wait(11000)
