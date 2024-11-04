import requests

from .setting import Settings


class WeatherAPIClient:
    def __init__(self):
        self.api_key = Settings().api_key
        self.base_url = Settings().base_url

    def fetch_weather(self, location: str, date: str) -> dict:
        params = {"q": location, "appid": self.api_key, "lang": "kr", "units": "metric"}
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()
