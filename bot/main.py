import asyncio
import logging

from aiogram import Bot, Dispatcher

from config.settings import get_settings

from bot.handlers import start, help, download, callbacks


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


async def main():
    settings = get_settings()

    bot = Bot(token=settings.BOT_TOKEN)

    dp = Dispatcher()

    # تسجيل أوامر البوت
    dp.include_router(start.router)
    dp.include_router(help.router)
    dp.include_router(download.router)
    dp.include_router(callbacks.router)

    logging.info("🚀 Mouja Digital Bot Started")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
