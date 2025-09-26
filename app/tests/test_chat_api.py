import pytest


@pytest.mark.asyncio
async def test_chat_endpoint_returns_reply(async_client):
    payload = {
        "session_id": None,
        "messages": [
            {
                "role": "user",
                "content": "Hola, ¿puedes presentarte?",
            }
        ],
    }

    response = await async_client.post("/api/v1/chat", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data["session_id"], str)
    assert data["reply"]["role"] == "assistant"
    assert "Stub response" in data["reply"]["content"]
    assert len(data["history"]) == 2


@pytest.mark.asyncio
async def test_chat_endpoint_validates_last_message_role(async_client):
    payload = {
        "session_id": "session-1",
        "messages": [
            {
                "role": "assistant",
                "content": "Mensaje previo",
            }
        ],
    }

    response = await async_client.post("/api/v1/chat", json=payload)
    assert response.status_code == 400
    assert "Last message" in response.json()["detail"]
