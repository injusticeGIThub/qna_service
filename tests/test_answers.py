import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_answer_success(client: AsyncClient):
    # сперва создаём вопрос
    q_resp = await client.post("/questions/", json={"text": "Первый вопрос"})
    assert q_resp.status_code == 201
    question_id = q_resp.json()["id"]

    payload = {
        "question_id": question_id,
        "user_id": "user-123",
        "text": "Первый ответ",
    }

    a_resp = await client.post("/answers/", json=payload)
    assert a_resp.status_code == 201

    data = a_resp.json()
    assert data["question_id"] == question_id
    assert data["user_id"] == "user-123"
    assert data["text"] == "Первый ответ"
    assert "created_at" in data


@pytest.mark.asyncio
async def test_create_answer_for_nonexistent_question(client: AsyncClient):
    payload = {
        "question_id": 999,
        "user_id": "user-123",
        "text": "Ответ к несуществующему вопросу",
    }

    resp = await client.post("/answers/", json=payload)
    assert resp.status_code == 404

    data = resp.json()
    assert data["error"] == "Question not found"
    assert data["code"] == "not_found"


@pytest.mark.asyncio
async def test_list_answers_for_question(client: AsyncClient):
    q_resp = await client.post("/questions/", json={"text": "Вопрос с ответами"})
    assert q_resp.status_code == 201
    question_id = q_resp.json()["id"]

    for i in range(2):
        resp = await client.post(
            "/answers/",
            json={
                "question_id": question_id,
                "user_id": f"user-{i}",
                "text": f"Ответ {i}",
            },
        )
        assert resp.status_code == 201

    list_resp = await client.get(f"/questions/{question_id}/answers")
    assert list_resp.status_code == 200

    answers = list_resp.json()
    assert len(answers) == 2
    assert answers[0]["text"] == "Ответ 0"
    assert answers[1]["text"] == "Ответ 1"


@pytest.mark.asyncio
async def test_cascade_delete_question_deletes_answers(client: AsyncClient):
    # создаём вопрос
    q_resp = await client.post("/questions/", json={"text": "Удаляемый вопрос"})
    assert q_resp.status_code == 201
    question_id = q_resp.json()["id"]

    # создаём ответ
    a_resp = await client.post(
        "/answers/",
        json={
            "question_id": question_id,
            "user_id": "user-x",
            "text": "Ответ, который тоже должен исчезнуть",
        },
    )
    assert a_resp.status_code == 201

    list_before = await client.get(f"/questions/{question_id}/answers")
    assert list_before.status_code == 200
    assert len(list_before.json()) == 1

    del_resp = await client.delete(f"/questions/{question_id}")
    assert del_resp.status_code == 204

    q_get = await client.get(f"/questions/{question_id}")
    assert q_get.status_code == 404

    list_after = await client.get(f"/questions/{question_id}/answers")
    assert list_after.status_code == 404
