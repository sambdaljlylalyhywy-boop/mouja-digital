import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    BOT_TOKEN = os.getenv("8988274598:AAELLmdfj4FuFOu3_r9FxvdjTCV9pqlZJOw")
    ADMIN_ID = int(os.getenv("7021626074", 0))
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite+aiosqlite:///database/mouja.db"
    )
    ENVIRONMENT = os.getenv(
        "ENVIRONMENT",
        "development"
    )


settings = Settings()
