import requests


class WeatherService:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    WEATHER_CODES = {
        0: ("☀️", "Céu limpo"),
        1: ("🌤️", "Pouco nublado"),
        2: ("⛅", "Parcialmente nublado"),
        3: ("☁️", "Nublado"),
        45: ("🌫️", "Nevoeiro"),
        48: ("🌫️", "Nevoeiro"),
        51: ("🌦️", "Chuvisco"),
        53: ("🌦️", "Chuvisco"),
        55: ("🌦️", "Chuvisco"),
        56: ("🌧️", "Chuva gelada"),
        57: ("🌧️", "Chuva gelada"),
        61: ("🌧️", "Chuva fraca"),
        63: ("🌧️", "Chuva"),
        65: ("🌧️", "Chuva forte"),
        66: ("🌧️", "Chuva gelada"),
        67: ("🌧️", "Chuva gelada"),
        71: ("🌨️", "Neve fraca"),
        73: ("🌨️", "Neve"),
        75: ("❄️", "Neve forte"),
        77: ("❄️", "Grãos de neve"),
        80: ("🌦️", "Aguaceiros"),
        81: ("🌦️", "Aguaceiros"),
        82: ("⛈️", "Aguaceiros fortes"),
        85: ("🌨️", "Aguaceiros de neve"),
        86: ("❄️", "Aguaceiros de neve"),
        95: ("⛈️", "Trovoada"),
        96: ("⛈️", "Trovoada com granizo"),
        99: ("⛈️", "Trovoada com granizo"),
    }

    WEEKDAYS = {
        0: "Seg",
        1: "Ter",
        2: "Qua",
        3: "Qui",
        4: "Sex",
        5: "Sáb",
        6: "Dom",
    }

    def get_week_forecast(self):
        """
        Devolve previsão compacta para 7 dias.

        Cidade fixa: Fafe.
        Coordenadas:
        latitude: 41.4508
        longitude: -8.1726
        """
        params = {
            "latitude": 41.4508,
            "longitude": -8.1726,
            "daily": "weather_code,temperature_2m_max,temperature_2m_min",
            "timezone": "Europe/Lisbon",
            "forecast_days": 7,
        }

        try:
            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=8,
            )
            response.raise_for_status()

            data = response.json()
            daily = data.get("daily", {})

            dates = daily.get("time", [])
            max_temperatures = daily.get("temperature_2m_max", [])
            min_temperatures = daily.get("temperature_2m_min", [])
            weather_codes = daily.get("weather_code", [])

            forecast = []

            for index, day in enumerate(dates):
                if index >= 7:
                    break

                icon, description = self.WEATHER_CODES.get(
                    weather_codes[index],
                    ("🌡️", "Meteorologia"),
                )

                label = "Hoje" if index == 0 else self.get_weekday_label(day)

                forecast.append({
                    "day": label,
                    "icon": icon,
                    "description": description,
                    "max": round(max_temperatures[index]),
                    "min": round(min_temperatures[index]),
                })

            return True, forecast

        except requests.RequestException:
            return False, []

        except (KeyError, IndexError, TypeError, ValueError):
            return False, []

    def get_weekday_label(self, date_text):
        from datetime import datetime

        try:
            parsed_date = datetime.strptime(date_text, "%Y-%m-%d").date()
        except ValueError:
            return ""

        return self.WEEKDAYS.get(parsed_date.weekday(), "")