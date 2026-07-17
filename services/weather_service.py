import os
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

import requests
from dotenv import load_dotenv


def get_env_file():
   
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent / ".env"

    return Path(__file__).resolve().parents[1] / ".env"


load_dotenv(get_env_file())


class WeatherService:
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
        api_key = os.getenv("VISUAL_CROSSING_API_KEY", "").strip()

        if not api_key:
            return False, []

        encoded_location = quote(self.LOCATION)

        url = f"{self.BASE_URL}/{encoded_location}"

        params = {
            "unitGroup": "metric",
            "include": "days",
            "contentType": "json",
            "lang": "pt",
            "key": api_key,
        }

        try:
            response = requests.get(
                url,
                params=params,
                timeout=10,
            )
            response.raise_for_status()

            data = response.json()
            days = data.get("days", [])

            if not days:
                return False, []

            forecast = []

            for index, day in enumerate(days[:7]):
                date_text = day.get("datetime", "")
                icon_code = day.get("icon", "cloudy")

                forecast.append({
                    "day": (
                        "Hoje"
                        if index == 0
                        else self.get_weekday_label(date_text)
                    ),
                    "min": round(float(day.get("tempmin", 0))),
                    "max": round(float(day.get("tempmax", 0))),
                    "icon": self.ICON_FILES.get(
                        icon_code,
                        "cloudy.svg",
                    ),
                    "description": (
                        day.get("conditions")
                        or "Estado do tempo indisponível"
                    ),
                })

            return True, forecast

        except requests.RequestException:
            return False, []

        except (TypeError, ValueError, KeyError):
            return False, []

    def get_weekday_label(self, date_text):
        try:
            parsed_date = datetime.strptime(
                date_text,
                "%Y-%m-%d",
            ).date()
        except ValueError:
            return ""

        return self.WEEKDAYS.get(parsed_date.weekday(), "")