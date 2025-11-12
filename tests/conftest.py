import os
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from wallet.main import app
from wallet.db.connection import Base, get_db
from wallet.db.models import Wallet
from decimal import Decimal


TEST_DB_URL = "sqlite+aiosqlite:///:memory:"



@pytest.fixture(scope="session")
async def test_db_engine():
    engine = create_async_engine(
        TEST_DB_URL, future=True
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
async def test_session_factory(test_db_engine):
    async_session = sessionmaker(test_db_engine,class_=AsyncSession, expire_on_commit=False)
    return async_session

@pytest.fixture
async def test_session(test_session_factory):
    async with test_session_factory() as session:
        yield session
        await session.rollback()

@pytest.fixture
async def test_client(test_db_engine):
    async def override_get_db():
        async_session = async_sessionmaker(
            test_db_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        async with async_session() as session:
            yield session

    # Подменяем зависимость
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as ac:
        yield ac

@pytest.fixture
async def test_wallet(test_session):
    wallet = Wallet(balance=Decimal("125.00"))
    test_session.add(wallet)
    await test_session.commit()
    await test_session.refresh(wallet)
    return wallet


@pytest.fixture
def get_url():
    url = os.getenv("API_PREFIX")
    return url