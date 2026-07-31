from aiogram import Router
from aiogram.types import Message


router = Router()


@router.message()
async def link_handler(message: Message):

    text = message.text

    if not text:
        return

    if text.startswith(("http://", "https://")):
        await message.answer(
            "⏳ جاري معالجة الرابط...\n\n"
            f"🔗 {text}"
        )
    else:
        await message.answer(
            "📎 أرسل رابطًا صالحًا للتحميل."
        )
