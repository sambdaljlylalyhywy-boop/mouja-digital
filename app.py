from contextlib import asynccontextmanager
from fastapi import FastAPI
import asyncio
import traceback

from bot.main import main


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("✅ FastAPI lifespan started", flush=True)

    async def run_bot():
        try:
            print("🚀 Starting bot...", flush=True)
            await main()
        except Exception:
            print("❌ Bot crashed:", flush=True)
            traceback.print_exc()

    task = asyncio.create_task(run_bot())
    yield
    task.cancel()


app = FastAPI(
    title="Mouja Digital Bot",
    version="0.2.0",
    lifespan=lifespan,
)


@app.get("/")
async def home():
    return {
        "name": "Mouja Digital Bot",
        "status": "running"
    }
