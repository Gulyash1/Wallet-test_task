import uuid
from starlette import status

async def test_get_wallet_success(test_client, test_wallet, get_url):
    response = await test_client.get(f"{get_url}/{test_wallet.uuid}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['balance'] == str(test_wallet.balance)

async def test_get_wallet_fail(test_client, get_url):
    response = await test_client.get(f"{get_url}/{uuid.uuid4()}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

async def test_get_wallet_wrong_data(test_client, get_url):
    response = await test_client.get(f"{get_url}/1234")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
