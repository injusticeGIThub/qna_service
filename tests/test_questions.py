import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_question_success(client: AsyncClient):
    payload = {"text": "Кто такой Джанго и почему он освобождён?"}

    resp = await client.post("/questions/", json=payload)
    assert resp.status_code == 201

    data = resp.json()

    # вместо жёсткого assert data["id"] == 1:
    assert isinstance(data["id"], int)
    assert data["id"] > 0
    assert data["text"] == payload["text"]


@pytest.mark.asyncio
async def test_create_question_empty_text_validation(client: AsyncClient):
    payload = {"text": "   "}

    resp = await client.post("/questions/", json=payload)
    assert resp.status_code == 422

    data = resp.json()
    assert data["error"] == "Validation error"
    assert data["code"] == "validation_error"
    assert any(err["loc"][-1] == "text" for err in data["details"])


@pytest.mark.asyncio
async def test_get_question_not_found(client: AsyncClient):
    resp = await client.get("/questions/999")
    assert resp.status_code == 404

    data = resp.json()
    assert data["error"] == "Question not found"
    assert data["code"] == "not_found"
