import re
from datetime import datetime, timedelta

from googletrans import Translator


class NaturalLanguageProcessor:
    def __init__(self):
        self.translator = Translator()

    def parse_location(self, question: str) -> str:
        location_match = re.search(r"\b(\w+)\b 날씨", question)

        if location_match:
            location_korean = location_match.group(1)
            # 번역기를 통해 영어로 변환
            location_english = self.translator.translate(location_korean, src="ko", dest="en").text
            return location_english

        return "Seoul"  # 기본값

    def parse_date(self, question: str) -> str:
        if "내일 모레" in question or "모레" in question:
            return (datetime.today() + timedelta(days=2)).strftime("%Y-%m-%d")

        elif "내일" in question:
            return (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")

        elif "어제" in question:
            return (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")

        elif "그저께" in question:
            return (datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d")

        else:
            return datetime.today().strftime("%Y-%m-%d")  # 기본값
