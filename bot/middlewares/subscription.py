import logging

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from bot.services.subscription import is_subscribed
from bot.keyboards.subscription import subscription_keyboard


class SubscriptionMiddleware(BaseMiddleware):

    def __init__(self, settings):
        self.settings = settings

    async def __call__(self, handler, event, data):

        user = getattr(event, "from_user", None)

        if not user:
            return await handler(event, data)

        # السماح بأمر البداية
        if isinstance(event, Message):
            if event.text and event.text.split()[0].split("@")[0] == "/start":
                return await handler(event, data)

        # السماح بزر التحقق
        if isinstance(event, CallbackQuery):
            if event.data == "check_subscription":
                return await handler(event, data)

        try:
            subscribed = await is_subscribed(
                data["bot"],
                user.id,
                self.settings.CHANNEL_ID
            )
        except Exception:
            logging.exception("Subscription check failed")

            text = (
                "⚠️ تعذر التحقق من اشتراكك حاليًا.\n"
                "يرجى التأكد من إعداد البوت مشرفًا في القناة."
            )

            if isinstance(event, Message):
                await event.answer(text)
            elif isinstance(event, CallbackQuery):
                await event.answer(text, show_alert=True)

            return

        if subscribed:
            return await handler(event, data)

        keyboard = subscription_keyboard(
            self.settings.CHANNEL_URL
        )

        text = (
            "🔒 عذرًا، يجب الاشتراك في قناتنا أولًا "
            "حتى تتمكن من استخدام البوت.\n\n"
            "اشترك ثم اضغط على زر التحقق."
        )

        if isinstance(event, Message):
            await event.answer(text, reply_markup=keyboard)

        elif isinstance(event, CallbackQuery):
            await event.answer(
                "يجب الاشتراك في القناة أولًا.",
                show_alert=True
            )

            if event.message:
                await event.message.answer(
                    text,
                    reply_markup=keyboard
                )
