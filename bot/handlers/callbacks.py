from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.services.downloader import download_video, download_audio
from bot.utils.files import delete_file, get_file_size


router = Router()

# تخزين الروابط مؤقتًا (سيتم تطويره لاحقًا إلى قاعدة بيانات)
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
        "🎬 جاري تحميل الفيديو..."
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

        with open(file_path, "rb") as video:
            await callback.message.answer_video(
                video=video,
                caption="✅ تم تحميل الفيديو بواسطة Mouja Digital"
            )

    except Exception as e:
        await callback.message.answer(
            f"❌ حدث خطأ أثناء التحميل:\n{e}"
        )

    finally:
        if file_path:
            delete_file(file_path)

    await callback.answer()


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
        "🎵 جاري استخراج الصوت MP3..."
    )

    file_path = None

    try:
        file_path = download_audio(url)

        size = get_file_size(file_path)

        if size > MAX_FILE_SIZE:
            await callback.message.answer(
                f"❌ حجم الملف كبير ({size}MB)"
            )
            return

        with open(file_path, "rb") as audio:
            await callback.message.answer_audio(
                audio=audio,
                caption="✅ تم استخراج الصوت بواسطة Mouja Digital"
            )

    except Exception as e:
        await callback.message.answer(
            f"❌ حدث خطأ أثناء التحميل:\n{e}"
        )

    finally:
        if file_path:
            delete_file(file_path)

    await callback.answer()
