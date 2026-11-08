from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def subscription_keyboard(channel_url):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 اشترك في القناة",
                    url=channel_url
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ اشتركت، تحقق",
                    callback_data="check_subscription"
                )
            ]
        ]
    )
