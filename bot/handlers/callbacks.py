import os
from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from bot.services.downloader import download_video, download_audio
from bot.utils.files import delete_file, get_file_size


router = Router()

# تخزين الروابط مؤقتًا
user_links = {}

MAX_FILE_SIZE = 50  # MB


@router.callback_query(F.data == "download_video")
async def download_video_handler(callback: CallbackQuery):

    user_id = callback.from_user.id
    url = user_links.get(user_id)

    if not url:
        await callback.answer(
            "❌ الرابط غير موجود",
            show_alert=True
        )
        return

    await callback.message.answer(
        "📥 جاري تحميل المحتوى..."
    )

    file_path = None

    try:
        file_path = download_video(url)

        size = get_file_size(file_path)

        if size > MAX_FILE_SIZE:
            await callback.message.answer(
                f"❌ حجم الملف كبير ({size}MB)"
            )
            return

        file = FSInputFile(file_path)

        extension = os.path.splitext(file_path)[1].lower()

        if extension in [".jpg", ".jpeg", ".png", ".webp"]:
            await callback.message.answer_photo(
                photo=file,
                caption="✅ تم تحميل الصورة بواسطة Mouja Digital"
            )

        elif extension in [".mp4", ".mov", ".mkv", ".webm"]:
            await callback.message.answer_video(
                video=file,
                caption="✅ تم تحميل الفيديو بواسطة Mouja Digital"
            )

        else:
            await callback.message.answer_document(
                document=file,
                caption="✅ تم تحميل الملف بواسطة Mouja Digital"
            )

    except Exception as e:
        await callback.message.answer(
            f"❌ حدث خطأ أثناء التحميل:\n{e}"
        )

    finally:
        if file_path:
            delete_file(file_path)


@router.callback_query(F.data == "download_audio")
async def download_audio_handler(callback: CallbackQuery):

    user_id = callback.from_user.id
    url = user_links.get(user_id)

    if not url:
        await callback.answer(
            "❌ الرابط غير موجود",
            show_alert=True
        )
        return

    await callback.message.answer(
        "🎵 جاري تحميل الصوت..."
    )

    file_path = None

    try:
        file_path = download_audio(url)

        audio = FSInputFile(file_path)

        await callback.message.answer_audio(
            audio=audio,
            caption="✅ تم تحميل الصوت بواسطة Mouja Digital"
        )

    except Exception as e:
        await callback.message.answer(
            f"❌ حدث خطأ أثناء التحميل:\n{e}"
        )

    finally:
        if file_path:
            delete_file(file_path)
