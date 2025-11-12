import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
load_dotenv()

def get_url():
    """Get database URL from environment variables."""
    db = os.getenv('POSTGRES_DB')
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_PORT')
    url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
    return url

engine = create_async_engine(get_url(), echo=True, future=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()
async def get_db():
    """Get database session."""
    async with AsyncSessionLocal() as session:
        yield session
