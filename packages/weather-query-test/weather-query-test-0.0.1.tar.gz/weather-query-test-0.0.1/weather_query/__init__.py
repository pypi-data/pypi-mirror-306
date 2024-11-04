from googletrans import Translator

from .client import WeatherAPIClient
from .preprocess import NaturalLanguageProcessor


def query(question: str) -> str:
    location = NaturalLanguageProcessor().parse_location(question)
    date = NaturalLanguageProcessor().parse_date(question)
    weather_data = WeatherAPIClient().fetch_weather(location, date)
    return format_response(weather_data, date, location)


def format_response(weather_data: str, date: str, location: str) -> str:
    # API 응답에서 날씨 정보 포맷팅 예시
    weather_desc = weather_data.get("weather")[0].get("description")
    year, month, day = date.split("-")
    location = Translator().translate(location, src="en", dest="ko").text
    return f"{year}년 {month}월 {day}일 {location} 날씨는 {weather_desc}입니다."
