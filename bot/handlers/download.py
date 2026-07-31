from aiogram import Router
from aiogram.types import Message

from bot.services.downloader import download_media


router = Router()


@router.message()
async def link_handler(message: Message):

    text = message.text

    if not text:
        return

    if text.startswith(("http://", "https://")):

        status = await message.answer(
            "⏳ جاري تحميل الرابط..."
        )

        try:
            file_path = download_media(text)

            await message.answer_document(
                document=open(file_path, "rb")
            )

            await status.delete()

        except Exception as e:
            await status.edit_text(
                f"❌ حدث خطأ:\n{e}"
            )

    else:
        await message.answer(
            "📎 أرسل رابطًا صحيحًا."
        )
