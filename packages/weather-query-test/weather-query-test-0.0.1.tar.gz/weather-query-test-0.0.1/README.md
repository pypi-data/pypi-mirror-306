# weather-query
크라우드웍스 사전과제

## 환경 설정

### 1. install [rye](https://github.com/mitsuhiko/rye)

[install documentation](https://rye-up.com/guide/installation/#installing-rye)

Linux
```bash
curl -sSf https://rye-up.com/get | bash
echo 'source "$HOME/.rye/env"' >> ~/.bashrc
source ~/.bashrc
```

Windows  
see [install documentation](https://rye-up.com/guide/installation/)


### 2. Create virtual environment

1 pyproject.toml 파일을 만들고 다음과 같이 작성합니다.
```toml
# pyproject.toml
dependencies = [
    "jinja2>=3.1.3",
    "flake8>=7.1.1",
    "black>=24.10.0",
    "fastapi>=0.115.0",
    "isort>=5.13.2",
    "uvicorn>=0.31.1",
    "googletrans==4.0.0rc1",
    "ipython>=8.28.0",
    "python-dotenv>=1.0.1",
    "python-multipart>=0.0.12",
    "requests>=2.32.3",
    "markdown>=3.7",
]
```

2. 가상환경을 만듭니다.

```bash
rye sync
```

## 코드 구현
```python
import weather_query

result = weather_query.query("내일 서울 날씨 어때?")

print(result)

```
실행하면 다음과 같이 문자열이 출력됩니다.

```
2024년 11월 05일 서울 날씨는 구름조금입니다.
```

## 웹 서버 실행하기
API 서버는 다음과 같이 실행합니다.
```sh
rye run uvicorn app.server:app --host=127.0.0.1 --port=8000 --reload
```

### 폴더 구성
```
├── app
│   ├── __pycache__
│   ├── server.py
│   └── templates
├── main.py
├── pyproject.toml
├── requirements-dev.lock
├── requirements.lock
├── tests
│   ├── __pycache__
│   └── test_query.py
└── weather_forecast
    ├── __init__.py
    ├── __pycache__
    ├── client.py
    ├── preprocess.py
    └── setting.py
```
