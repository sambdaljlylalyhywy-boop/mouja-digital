import asyncio
import logging
import traceback

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config.settings import get_settings
from database.users import init_db
from bot.middlewares.subscription import SubscriptionMiddleware

from bot.handlers import (
    start, help, download, callbacks,
    subscription, admin
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


async def main():
    try:
        print("🚀 main() started")

        settings = get_settings()

        if not settings.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is missing")

        await init_db()
        print("✅ Database initialized")

        bot = Bot(token=settings.BOT_TOKEN)

        dp = Dispatcher(storage=MemoryStorage())

        middleware = SubscriptionMiddleware(settings)

        dp.message.middleware(middleware)
        dp.callback_query.middleware(middleware)

        dp.include_router(start.router)
        dp.include_router(subscription.router)
        dp.include_router(admin.router)
        dp.include_router(help.router)
        dp.include_router(download.router)
        dp.include_router(callbacks.router)

        print("✅ All routers loaded")
        print("👑 Admin panel enabled")
        print("🤖 Bot is starting polling...")

        await dp.start_polling(bot)

    except Exception:
        print("❌ Error while starting the bot:")
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
