from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def wallet_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    add_wallet_button = KeyboardButton("Добавить кошелек")
    keyboard.add(add_wallet_button)
    return keyboard
