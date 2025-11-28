# tests/conftest.py
import sys
import asyncio

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app
from app.db.session import get_db  # будем его переопределять

# ВАЖНО: здесь должен быть Base с моделями.
# Скорее всего у тебя что-то вроде app.db.base или app.models
from app.db.base import Base  # если у тебя другой путь — поправь


# === 1. Нормальный event loop на Windows ===
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# === 2. Один event loop на всю сессию тестов ===
@pytest.fixture(scope="session")
def event_loop():
    """
    Pytest-asyncio по умолчанию создаёт новый loop на каждый тест.
    Для async SQLAlchemy/anyio это часто ломает всё.
    Здесь один loop на всю сессию тестов.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


# === 3. ТЕСТОВЫЙ движок и сессии (SQLite + aiosqlite) ===

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    future=True,
)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


# === 4. Создаём/чистим таблицы один раз перед всеми тестами ===

@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    """
    Создаёт структуру БД для тестов (SQLite), использует Base.metadata.
    """
    async with test_engine.begin() as conn:
        # На всякий случай дропаем, потом создаём
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    # После всех тестов — закрываем движок
    await test_engine.dispose()


# === 5. Правильный override get_db, но уже на ТЕСТОВЫЙ движок ===

async def override_get_db():
    """
    Для каждого запроса создаём НОВУЮ AsyncSession поверх тестового движка.
    """
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


app.dependency_overrides[get_db] = override_get_db


# === 6. Клиент для тестов ===

@pytest.fixture
async def client():
    """
    Httpx AsyncClient поверх FastAPI-приложения.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
