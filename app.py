import uvicorn
from fastapi import FastAPI

from bot.main import start_bot


app = FastAPI(
    title="Mouja Digital",
    description="Telegram Downloader Platform",
    version="1.0.0"
)


@app.get("/")
async def home():
    return {
        "project": "Mouja Digital",
        "status": "running"
    }


@app.on_event("startup")
async def startup():
    await start_bot()


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000
    )
