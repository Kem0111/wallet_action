from aiogram import types, Dispatcher
from wallet_action.models import User
from settings import bot
import logging

ADMIN_ID = 414160073


async def admin_post(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    logging.info("Fetching users from DB")
    text = message.text.split(' ', 1)[1]
    for user in await User.all():
        await bot.send_message(user.telegram_id, text)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(
        admin_post,
        commands=['post'],
        user_id=ADMIN_ID
    )
