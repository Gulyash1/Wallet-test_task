import uuid
from uuid import uuid4
from starlette import status


async def test_wallet_deposit(test_client, test_wallet, get_url):
    response = await test_client.post(f"{get_url}/{test_wallet.uuid}/operation",
                                      json={"operation_type": "DEPOSIT",
                                            "amount": 100})
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["uuid"] == str(test_wallet.uuid)
    assert result["balance"] == '225.00'

async def test_wallet_deposit_wrong_uuid(test_client, test_wallet, get_url):
    response = await test_client.post(f"{get_url}/{uuid.uuid4()}/operation",
                                      json={'operation_type': 'DEPOSIT',
                                            'amount': 100})
    assert response.status_code == status.HTTP_404_NOT_FOUND

async def test_wallet_deposit_negative_amount(test_client, test_wallet,get_url):
    response = await test_client.post(f"{get_url}/{test_wallet.uuid}/operation",
                                      json={"operation_type": "DEPOSIT",
                                            "amount": -100})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

async def test_wallet_wrong_operation_type(test_client, test_wallet, get_url):
    response = await test_client.post(f"{get_url}/{test_wallet.uuid}/operation",
                                      json={"operation_type": "MULTIPLY",
                                            "amount": 2})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT