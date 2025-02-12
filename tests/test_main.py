import pytest


@pytest.mark.asyncio
async def test_authenticate_user(client):
    response = client.post(
        "/api/auth",
        json={
            "username": "testuser",
            "password": "testpass",
        },
    )
    assert response.status_code == 200
    assert "token" in response.json()


@pytest.mark.asyncio
async def test_get_info(client):
    auth_response = client.post(
        "/api/auth",
        json={
            "username": "testuser",
            "password": "testpass",
        },
    )
    token = auth_response.json()["token"]

    response = client.get(
        "/api/info", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "coins" in response.json()


@pytest.mark.asyncio
async def test_send_coin(client):
    user1 = client.post(
        "/api/auth",
        json={
            "username": "user1",
            "password": "testpass",
        },
    ).json()

    user2 = client.post(
        "/api/auth",
        json={
            "username": "user2",
            "password": "testpass",
        },
    ).json()

    response = client.post(
        "/api/sendCoin",
        json={"toUser": "user2", "amount": 100},
        headers={"Authorization": f"Bearer {user1['token']}"},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_buy_item(client):
    auth_response = client.post(
        "/api/auth",
        json={
            "username": "testuser",
            "password": "testpass",
        },
    )
    token = auth_response.json()["token"]

    response = client.get(
        "/api/buy/t-shirt",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_reset_coins(client):
    auth_response = client.post(
        "/api/auth",
        json={
            "username": "testuser",
            "password": "testpass",
        },
    )
    token = auth_response.json()["token"]

    response = client.post(
        "/api/reset_coins",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code in [200, 403]
