from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "👋 أهلاً بك في Mouja Digital Bot\n\n"
        "🤖 بوت تحميل الوسائط\n\n"
        "أرسل الرابط وسأقوم بمعالجته."
    )
