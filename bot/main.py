from aiogram import Bot, Dispatcher
from config.settings import settings


bot = Bot(
    token=settings.8988274598:AAELLmdfj4FuFOu3_r9FxvdjTCV9pqlZJOw
)

dp = Dispatcher()


async def start_bot():
    print("Mouja Digital Bot Started")
