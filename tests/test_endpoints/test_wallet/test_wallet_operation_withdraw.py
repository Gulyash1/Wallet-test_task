import os
import pytest
from starlette import status

async def test_wallet_operation_withdraw(test_client, test_wallet, get_url):
    response = await test_client.post(f"{get_url}/{test_wallet.uuid}/operation",
                                      json={"operation_type": "WITHDRAW",
                                            "amount": 25})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['uuid'] == str(test_wallet.uuid)
    assert response.json()['balance'] == '100.00'

async def test_wallet_operation_withdraw_over_balance(test_client, test_wallet, get_url):
    response = await test_client.post(f"{get_url}/{test_wallet.uuid}/operation",
                                      json={"operation_type": "WITHDRAW",
                                            "amount": 500})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
