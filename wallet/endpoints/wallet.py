import os
from uuid import UUID

from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from starlette import status
from wallet.db.connection import get_db
from wallet.db.models import Wallet
from wallet.db.schemas import WalletSchema, WalletOperation



router = APIRouter(prefix= os.getenv("API_PREFIX"))



@router.post("/create",
            status_code= status.HTTP_201_CREATED,
            response_model=WalletSchema)
async def create_wallet(db: AsyncSession = Depends(get_db)):
    """Create a new wallet."""
    wallet = Wallet(balance="0.00")
    db.add(wallet)
    await db.commit()
    await db.refresh(wallet)
    return WalletSchema(uuid = wallet.uuid,
                        balance = wallet.balance)

@router.get("/{wallet_id}",
            status_code=status.HTTP_200_OK)
async def get_wallet(wallet_id: UUID, db: AsyncSession = Depends(get_db)):
    """Get wallet from UUID"""
    wallet = await db.get(Wallet, wallet_id)
    if not wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found")
    return {"balance": str(wallet.balance)}

@router.post("/{wallet_id}/operation",
            status_code=status.HTTP_200_OK,
            response_model=WalletSchema)
async def operate_wallet(wallet_id: UUID, wp: WalletOperation, db: AsyncSession = Depends(get_db)):
    """Operate wallet with deposit or withdraw."""
    try:
        async with db.begin():
            state = await db.execute(
                select(Wallet).
                where(Wallet.uuid == wallet_id).with_for_update())
            wallet = state.scalar()
            if not wallet:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Wallet not found")
            if wp.operation_type == "DEPOSIT":
                wallet.balance += wp.amount
            elif wp.operation_type == 'WITHDRAW':
                if wallet.balance - wp.amount < 0:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                        detail="Not enough balance")
                wallet.balance -= wp.amount
            db.add(wallet)
        await db.refresh(wallet)
        return WalletSchema(uuid=wallet.uuid,
                            balance=wallet.balance)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
