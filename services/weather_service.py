"""Consulta da previsão semanal através da API Visual Crossing."""

import os
from datetime import datetime
from urllib.parse import quote

import requests
from dotenv import load_dotenv

from app.path import ENV_FILE


load_dotenv(ENV_FILE)


class WeatherService:
    """Obter e adaptar a previsão de Braga para os widgets da barra superior."""

    BASE_URL = (
        "https://weather.visualcrossing.com/"
        "VisualCrossingWebServices/rest/services/timeline"
    )
    LOCATION = "Braga, Portugal"

    WEEKDAYS = {
        0: "Seg",
        1: "Ter",
        2: "Qua",
        3: "Qui",
        4: "Sex",
        5: "Sáb",
        6: "Dom",
    }

    ICON_FILES = {
        "clear-day": "clear.svg",
        "clear-night": "clear.svg",
        "partly-cloudy-day": "partly-cloudy.svg",
        "partly-cloudy-night": "partly-cloudy.svg",
        "cloudy": "cloudy.svg",
        "fog": "fog.svg",
        "wind": "cloudy.svg",
        "rain": "rain.svg",
        "showers-day": "rain.svg",
        "showers-night": "rain.svg",
        "snow": "snow.svg",
        "snow-showers-day": "snow.svg",
        "snow-showers-night": "snow.svg",
        "sleet": "snow.svg",
        "hail": "storm.svg",
        "thunder": "storm.svg",
        "thunder-rain": "storm.svg",
        "thunder-showers-day": "storm.svg",
        "thunder-showers-night": "storm.svg",
    }

    def get_week_forecast(self):
        """Devolver sete dias de previsão já formatados para a interface."""
        api_key = os.getenv("VISUAL_CROSSING_API_KEY", "").strip()

        if not api_key:
            return False, []

        url = f"{self.BASE_URL}/{quote(self.LOCATION)}"
        params = {
            "unitGroup": "metric",
            "include": "days",
            "contentType": "json",
            "lang": "pt",
            "key": api_key,
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            days = response.json().get("days", [])

            if not days:
                return False, []

            forecast = []

            for index, day in enumerate(days[:7]):
                date_text = day.get("datetime", "")
                icon_code = day.get("icon", "cloudy")

                forecast.append(
                    {
                        "day": (
                            "Hoje"
                            if index == 0
                            else self.get_weekday_label(date_text)
                        ),
                        "min": round(float(day.get("tempmin", 0))),
                        "max": round(float(day.get("tempmax", 0))),
                        "icon": self.ICON_FILES.get(icon_code, "cloudy.svg"),
                        "description": (
                            day.get("conditions")
                            or "Estado do tempo indisponível"
                        ),
                    }
                )

            return True, forecast

        except (requests.RequestException, TypeError, ValueError, KeyError):
            return False, []

    @classmethod
    def get_weekday_label(cls, date_text):
        """Converter uma data ISO na abreviatura portuguesa do dia da semana."""
        try:
            parsed_date = datetime.strptime(date_text, "%Y-%m-%d").date()
        except (TypeError, ValueError):
            return ""

        return cls.WEEKDAYS.get(parsed_date.weekday(), "")
