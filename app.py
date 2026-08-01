from fastapi import FastAPI
import asyncio
import traceback

from bot.main import main

app = FastAPI(
    title="Mouja Digital Bot",
    version="0.2.0"
)


@app.get("/")
async def home():
    return {
        "name": "Mouja Digital Bot",
        "version": "0.2.0",
        "status": "running"
    }


@app.on_event("startup")
async def startup_event():
    print("✅ FastAPI Started")

    async def run_bot():
        try:
            print("🚀 Starting Bot...")
            await main()
        except Exception as e:
            print("❌ BOT ERROR:", e)
            traceback.print_exc()

    asyncio.create_task(run_bot())
