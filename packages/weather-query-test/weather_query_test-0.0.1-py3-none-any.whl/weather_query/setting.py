import os

from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


class Settings:
    def __init__(self):
        self.base_url = os.getenv("base_url")
        self.api_key = os.getenv("api_key")
