from aiogram import types, Dispatcher
from wallet_action.read_file import read_messages
from wallet_action.keyboards import wallet_keyboard, wallets_list_keyboard
from wallet_action.validator import is_valid_ethereum_address
from wallet_action.models import User, Wallet


async def on_start(message: types.Message):
    """
    Process the /start command.
    Create a new user in the database if it doesn't exist
    and send a welcome message with a keyboard.
    """
    user_id = message.from_user.id
    await User.get_or_create(telegram_id=user_id)
    response = await read_messages()
    board = wallet_keyboard()
    await message.answer(response['start'], reply_markup=board)


async def start_cmd_handler(message: types.Message):
    """
    Handle the /start command and call the on_start function.
    """
    await on_start(message)


async def add_wallet_handler(message: types.Message):
    """
    Handle the "Добавить кошелек" button click and prompt
    the user to input their wallet address.
    """
    response = await read_messages()
    await message.answer(response['add_wallet'])


async def receive_wallet_handler(message: types.Message):
    """
    Handle the user input with a wallet address.
    Validate the address, and if it's valid, add it
    to the user's wallets in the database.
    Send a confirmation message if the wallet is added, or an error message
    if it's already added.
    """
    wallet_address = message.text.strip()
    response = await read_messages()

    if not await is_valid_ethereum_address(wallet_address):
        await message.answer(response['invalid_wallet'])
        return

    user = await User.get(telegram_id=message.from_user.id)
    wallet, _ = await Wallet.get_or_create(address=wallet_address)

    if not await user.wallets.filter(id=wallet.id).exists():
        await user.wallets.add(wallet)
        await message.answer(response['wallet_added'])
    else:
        await message.answer(response['wallet_already_added'])


async def list_wallets_handler(message: types.Message):
    """
    Handle the 'Список кошельков' button click.
    Retrieve the list of wallets associated with the user
    and display them in a formatted list. If the user
    has no wallets, send a message indicating that no wallets
    have been added.
    """
    user = await User.get(telegram_id=message.from_user.id)
    wallets = await user.wallets.all()

    if not wallets:
        response = "У вас нет добавленных кошельков."
    else:
        response = "Ваши кошельки:"
        keyboard = wallets_list_keyboard(wallets)
        await message.answer(response, reply_markup=keyboard)


async def delete_wallet_callback_handler(callback_query: types.CallbackQuery):
    """
    Handle the 'Удалить кошелек: ' command.
    Extract the wallet address from the command,
    find the wallet associated with the user,
    and remove it from the user's wallets.
    Send a confirmation message if the wallet is removed,
    or an error message if the wallet is not found.
    """
    wallet_address = callback_query.data.replace("delete_wallet:", "").strip()
    user = await User.get(telegram_id=callback_query.from_user.id)
    response = await read_messages()

    wallet = await Wallet.get_or_none(address=wallet_address)

    await user.wallets.remove(wallet)
    await callback_query.answer(response['wallet_removed'],
                                show_alert=True)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(
        start_cmd_handler,
        commands=['start', 'help']
    )
    dp.register_message_handler(
        add_wallet_handler,
        lambda message: message.text == 'Добавить кошелек'
    )
    dp.register_message_handler(
        list_wallets_handler,
        lambda message: message.text == 'Список кошельков'
    )
    dp.register_message_handler(
        receive_wallet_handler,
        lambda message: message.text.startswith("0x")
    )
    dp.register_callback_query_handler(
        delete_wallet_callback_handler,
        lambda c: c.data.startswith("delete_wallet:")
    )
