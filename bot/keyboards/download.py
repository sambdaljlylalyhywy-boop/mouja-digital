from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def download_keyboard():

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎬 فيديو",
                    callback_data="download_video"
                ),
                InlineKeyboardButton(
                    text="🎵 صوت MP3",
                    callback_data="download_audio"
                )
            ]
        ]
    )

    return keyboard
