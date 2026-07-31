from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.services.downloader import download_video, download_audio


router = Router()

# تخزين الروابط مؤقتًا (سيتم استبداله لاحقًا بقاعدة بيانات)
user_links = {}


@router.callback_query(F.data == "download_video")
async def download_video_handler(callback: CallbackQuery):

    user_id = callback.from_user.id
    url = user_links.get(user_id)

    if not url:
        await callback.answer(
            "❌ لم يتم العثور على الرابط",
            show_alert=True
        )
        return

    await callback.message.answer(
        "🎬 جاري تحميل الفيديو..."
    )

    try:
        file_path = download_video(url)

        await callback.message.answer_video(
            video=open(file_path, "rb"),
            caption="✅ تم تحميل الفيديو بواسطة Mouja Digital"
        )

    except Exception as e:
        await callback.message.answer(
            f"❌ حدث خطأ أثناء التحميل:\n{e}"
        )

    await callback.answer()


@router.callback_query(F.data == "download_audio")
async def download_audio_handler(callback: CallbackQuery):

    user_id = callback.from_user.id
    url = user_links.get(user_id)

    if not url:
        await callback.answer(
            "❌ لم يتم العثور على الرابط",
            show_alert=True
        )
        return

    await callback.message.answer(
        "🎵 جاري استخراج الصوت MP3..."
    )

    try:
        file_path = download_audio(url)

        await callback.message.answer_audio(
            audio=open(file_path, "rb"),
            caption="✅ تم استخراج الصوت بواسطة Mouja Digital"
        )

    except Exception as e:
        await callback.message.answer(
            f"❌ حدث خطأ أثناء التحميل:\n{e}"
        )

    await callback.answer()
