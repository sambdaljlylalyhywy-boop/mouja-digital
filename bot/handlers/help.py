from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command


router = Router()


@router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(
        "📖 المساعدة\n\n"
        "/start - تشغيل البوت\n"
        "/help - عرض المساعدة\n\n"
        "أرسل أي رابط للمعالجة."
    )
