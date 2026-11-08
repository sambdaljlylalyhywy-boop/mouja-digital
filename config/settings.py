import os
from functools import lru_cache

def load_env():
    env_path = ".env"

    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#") or "=" not in line:
                    continue

                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

class Settings:
    def __init__(self):
        load_env()

        self.BOT_TOKEN = os.getenv("BOT_TOKEN", "")
        self.ADMIN_IDS = os.getenv("ADMIN_IDS", "7021626074")
        self.CHANNEL_ID = os.getenv("CHANNEL_ID", "@mouja_digital")
        self.CHANNEL_URL = os.getenv(
            "CHANNEL_URL",
            "https://t.me/mouja_digital"
        )

    @property
    def admin_ids_list(self):
        return [
            int(x.strip())
            for x in self.ADMIN_IDS.split(",")
            if x.strip()
        ]

@lru_cache
def get_settings():
    return Settings()
