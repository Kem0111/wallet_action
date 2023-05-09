from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           InlineKeyboardMarkup,
                           InlineKeyboardButton)
from typing import List
from wallet_action.read_file import read_messages


async def wallet_keyboard() -> ReplyKeyboardMarkup:
    """
    Create and return a ReplyKeyboardMarkup object with wallet-related options.

    Returns:
        ReplyKeyboardMarkup: A keyboard containing buttons
        for wallet-related actions.
    """
    button_names = await read_messages()
    buttons = [
        KeyboardButton(button_names["add_wallet"]),
        KeyboardButton(button_names["wallet_list"])
    ]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard


async def wallets_list_keyboard(wallets: List[str]) -> InlineKeyboardMarkup:
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
    button_names = await read_messages()
    for wallet in wallets:
        keyboard.row(
            InlineKeyboardButton(
                wallet.address,
                callback_data=f"wallet:{wallet.address}"
            ),
            InlineKeyboardButton(
                button_names["delete"],
                callback_data=f"delete_wallet:{wallet.address}")
        )
    return keyboard


async def create_wallet_buttons(wallet_address: str) -> InlineKeyboardMarkup:
    wallet_buttons = InlineKeyboardMarkup(row_width=1)
    button_names = await read_messages()
    wallet_buttons.add(
        InlineKeyboardButton(
            text=button_names["get_balance"],
            callback_data=f"get_balance:{wallet_address}"
        ),
        InlineKeyboardButton(
            text=button_names["get_transactions"],
            callback_data=f"get_transactions:{wallet_address}"
        )
    )
    return wallet_buttons
