from fastapi import FastAPI
import asyncio

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
    asyncio.create_task(main())
