from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, Field


class WalletSchema(BaseModel):
    uuid: UUID
    balance: Decimal

class WalletOperation(BaseModel):
    operation_type: str = Field(..., pattern="^(DEPOSIT|WITHDRAW)$")
    amount: Decimal = Field(..., gt=0.0)
