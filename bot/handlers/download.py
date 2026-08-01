from aiogram import Router
from aiogram.types import Message

from bot.handlers.callbacks import user_links
from bot.keyboards.download import download_keyboard

router = Router()


@router.message()
async def link_handler(message: Message):
    text = message.text

    if not text:
        return

    if text.startswith(("http://", "https://")):
        user_links[message.from_user.id] = text

        await message.answer(
            "🔗 تم استلام الرابط\n\n"
            "اختر نوع التحميل:",
            reply_markup=download_keyboard()
        )
    else:
        await message.answer(
            "❌ أرسل رابطًا صحيحًا يبدأ بـ http:// أو https://"
        )
