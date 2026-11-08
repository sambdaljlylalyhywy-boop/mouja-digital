async def is_subscribed(bot, user_id, channel_id):
    member = await bot.get_chat_member(
        chat_id=channel_id,
        user_id=user_id
    )

    if member.status in ("member", "administrator", "creator"):
        return True

    if member.status == "restricted" and member.is_member:
        return True

    return False
