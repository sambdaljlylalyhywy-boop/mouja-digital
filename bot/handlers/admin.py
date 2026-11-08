import asyncio
from aiogram import Router, F
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest

from config.settings import get_settings
from database.users import get_all_users, get_users_count

router = Router()


class AdminStates(StatesGroup):
    waiting_for_message = State()


def is_admin(user_id):
    return user_id in get_settings().admin_ids_list


def admin_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📊 الإحصائيات",
                callback_data="admin_stats"
            )
        ],
        [
            InlineKeyboardButton(
                text="📢 إرسال إعلان",
                callback_data="admin_broadcast"
            )
        ],
    ])


@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "👑 لوحة تحكم Mouja Digital\n\n"
        "مرحبًا بك في لوحة المشرف.",
        reply_markup=admin_keyboard()
    )


@router.callback_query(F.data == "admin_stats")
async def admin_stats(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("غير مصرح لك.", show_alert=True)
        return

    count = await get_users_count()

    await callback.message.answer(
        f"📊 إحصائيات البوت\n\n"
        f"👥 إجمالي المستخدمين: {count}"
    )
    await callback.answer()


@router.callback_query(F.data == "admin_broadcast")
async def start_broadcast(
    callback: CallbackQuery,
    state: FSMContext
):
    if not is_admin(callback.from_user.id):
        await callback.answer("غير مصرح لك.", show_alert=True)
        return

    await state.set_state(AdminStates.waiting_for_message)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="❌ إلغاء",
                callback_data="admin_cancel"
            )
        ]
    ])

    await callback.message.answer(
        "📢 أرسل الآن الإعلان الذي تريد نشره.\n\n"
        "يمكنك إرسال نص أو صورة أو فيديو مع وصف.\n"
        "ويمكنك إرفاق أزرار من لوحة إنشاء الرسالة إن كانت متاحة.",
        reply_markup=keyboard
    )

    await callback.answer()


@router.callback_query(F.data == "admin_cancel")
async def cancel_broadcast(
    callback: CallbackQuery,
    state: FSMContext
):
    if not is_admin(callback.from_user.id):
        await callback.answer("غير مصرح لك.", show_alert=True)
        return

    await state.clear()
    await callback.message.answer("تم إلغاء الإرسال.")
    await callback.answer()


@router.message(AdminStates.waiting_for_message)
async def send_broadcast(
    message: Message,
    state: FSMContext
):
    if not is_admin(message.from_user.id):
        return

    users = await get_all_users()

    if not users:
        await state.clear()
        await message.answer("لا يوجد مستخدمون مسجلون.")
        return

    await state.clear()

    sent = 0
    failed = 0

    status = await message.answer(
        f"⏳ بدأ إرسال الإعلان إلى {len(users)} مستخدم..."
    )

    for user_id in users:
        try:
            await message.bot.copy_message(
                chat_id=user_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id,
                reply_markup=message.reply_markup
            )
            sent += 1

        except (TelegramForbiddenError, TelegramBadRequest):
            failed += 1

        except Exception:
            failed += 1

        await asyncio.sleep(0.05)

    await status.edit_text(
        "✅ انتهى الإرسال\n\n"
        f"📨 تم الإرسال بنجاح: {sent}\n"
        f"❌ تعذر الإرسال: {failed}\n"
        f"👥 إجمالي المستهدفين: {len(users)}"
    )
