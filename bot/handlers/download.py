from aiogram import Router
from aiogram.types import Message
from bot.keyboards.download import download_keyboard


router = Router()


@router.message()
async def link_handler(message: Message):

    text = message.text

    if not text:
        return

    if text.startswith(("http://", "https://")):

        await message.answer(
            "🔗 تم استلام الرابط\n\n"
            "اختر نوع التحميل:",
            reply_markup=download_keyboard()
        )

    else:
        await message.answer(
            "📎 أرسل رابطًا صحيحًا."
        )
