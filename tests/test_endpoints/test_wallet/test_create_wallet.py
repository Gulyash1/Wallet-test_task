from starlette import status

async def test_create_wallet(test_client, get_url):
    response = await test_client.post(f"{get_url}/create")
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "uuid" in data
    assert data["balance"] == "0.00"





