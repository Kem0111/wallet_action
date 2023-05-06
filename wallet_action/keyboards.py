from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           InlineKeyboardMarkup,
                           InlineKeyboardButton)
from typing import List


def wallet_keyboard() -> ReplyKeyboardMarkup:
    """
    Create and return a ReplyKeyboardMarkup object with wallet-related options.

    Returns:
        ReplyKeyboardMarkup: A keyboard containing buttons
        for wallet-related actions.
    """
    buttons = [
        KeyboardButton("Добавить кошелек"),
        KeyboardButton("Список кошельков")
    ]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard


def wallets_list_keyboard(wallets: List[str]) -> InlineKeyboardMarkup:
    """
    Create and return an InlineKeyboardMarkup object with a list of wallets and
    corresponding action buttons.

    Args:
        wallets (List[str]): A list of wallet addresses.

    Returns:
        InlineKeyboardMarkup: A keyboard containing rows
        with wallet addresses and action buttons.
    """
    keyboard = InlineKeyboardMarkup()
    for wallet in wallets:
        keyboard.row(
            InlineKeyboardButton(
                wallet.address,
                callback_data=f"wallet:{wallet.address}"
            ),
            InlineKeyboardButton(
                "Удалить",
                callback_data=f"delete_wallet:{wallet.address}")
        )
    return keyboard
