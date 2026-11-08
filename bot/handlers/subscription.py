from aiogram import Router
from aiogram.types import CallbackQuery

from config.settings import get_settings
from bot.services.subscription import is_subscribed

router = Router()


@router.callback_query(lambda c: c.data == "check_subscription")
async def check_subscription_handler(callback: CallbackQuery):

    settings = get_settings()

    try:
        subscribed = await is_subscribed(
            callback.bot,
            callback.from_user.id,
            settings.CHANNEL_ID
        )

    except Exception:
        await callback.answer(
            "تعذر التحقق الآن. حاول لاحقًا.",
            show_alert=True
        )
        return

    if not subscribed:
        await callback.answer(
            "لم يتم العثور على اشتراكك. اشترك ثم حاول مجددًا.",
            show_alert=True
        )
        return

    await callback.answer("تم التحقق بنجاح ✅")

    if callback.message:
        await callback.message.edit_text(
            "🎉 تم التحقق من اشتراكك!\n\n"
            "أهلًا بك في Mouja Digital Bot.\n"
            "أرسل رابط الوسائط للبدء."
        )
