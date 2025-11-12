from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from wallet.endpoints import wallet
from wallet.db.connection import engine, Base



@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create all tables in the database when the application starts,
     and dispose of the database engine when the application stops."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(title="Wallet API", lifespan=lifespan)
app.include_router(wallet.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
