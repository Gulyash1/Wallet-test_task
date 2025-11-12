import uuid

from sqlalchemy import Column, Numeric
from sqlalchemy.dialects.postgresql import UUID

from wallet.db.connection import Base

class Wallet(Base):
    """Wallet model for database."""
    __tablename__ = "wallets"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    balance = Column(Numeric(12, 2), nullable=False, default=0)
