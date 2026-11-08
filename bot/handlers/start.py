from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from config.settings import get_settings
from database.users import add_user
from bot.services.subscription import is_subscribed
from bot.keyboards.subscription import subscription_keyboard

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):

    settings = get_settings()

    await add_user(message.from_user)

    try:
        subscribed = await is_subscribed(
            message.bot,
            message.from_user.id,
            settings.CHANNEL_ID
        )
    except Exception:
        await message.answer(
            "⚠️ تعذر التحقق من الاشتراك حاليًا. حاول لاحقًا."
        )
        return

    if not subscribed:
        await message.answer(
            "🔒 لاستخدام Mouja Digital Bot، "
            "يجب الاشتراك في قناتنا أولًا.",
            reply_markup=subscription_keyboard(
                settings.CHANNEL_URL
            )
        )
        return

    await message.answer(
        "👋 أهلًا بك في Mouja Digital Bot\n\n"
        "🤖 بوت تحميل الوسائط\n\n"
        "أرسل الرابط وسأقوم بمعالجته."
    )
