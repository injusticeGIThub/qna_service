
# Q&A API — сервис вопросов и ответов

REST API-сервис «Вопросы и ответы» — проект с CRUD для вопросов и ответов, валидацией, тестами и Docker.

# Стек

- Python 3.9+
- FastAPI
- SQLAlchemy 2.0 async
- PostgreSQL 15
- Alembic
- Pytest + HTTPX
- Docker Compose

# 🚀 Установка и запуск
### Создать `.env`:
```
POSTGRES_USER=qna_user
POSTGRES_PASSWORD=qna_password
POSTGRES_DB=qna
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql+asyncpg://qna_user:qna_password@db:5432/qna
```

## Локальный запуск без Docker
```
git clone https://github.com/injusticeGIThub/qna_service.git
cd qna_service
python -m venv venv
. venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

## Запуск в Docker
```
docker compose up --build
```

## Примеры работы с API
* *POST /questions/*
```r
REQUEST JSON: 
{
	"text": "Кто такой Джанго и почему он освобождён?"
}

RESPONSE (201): 
{
	"text": "Кто такой Джанго и почему он освобождён?",
	"id": 1,
	"created_at": "2025-01-28T01:17:31.492746Z"
}
```
* *GET /questions/*
```r

 RESPONSE (200):
 [
	{
		"text": "Кто такой Джанго и почему он освобождён?",
		"id": 1,
		"created_at": "2025-01-28T01:17:31.492746Z"
	}
]
```
# Запуск тестов
```
pytest -vv
```


## Автор
[Андрей - InjusticeGIThub](https://github.com/injusticeGIThub)
