import asyncio
import logging
import traceback

from aiogram import Bot, Dispatcher

from config.settings import get_settings
from bot.handlers import start, help, download, callbacks


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


async def main():
    try:
        print("🚀 main() started")

        settings = get_settings()
        print("✅ Settings loaded")
        print("BOT_TOKEN exists:", bool(settings.BOT_TOKEN))

        bot = Bot(token=settings.BOT_TOKEN)
        print("✅ Bot created")

        dp = Dispatcher()

        dp.include_router(start.router)
        dp.include_router(help.router)
        dp.include_router(download.router)
        dp.include_router(callbacks.router)

        print("✅ Routers loaded")
        print("🤖 Bot is starting polling...")

        await dp.start_polling(bot)

    except Exception:
        print("❌ Error while starting the bot:")
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
