from aiogram import types, Dispatcher
from wallet_action.read_file import read_messages
from wallet_action.keyboards import (wallet_keyboard,
                                     wallets_list_keyboard,
                                     create_wallet_buttons)
from wallet_action.validator import is_valid_ethereum_address
from wallet_action.models import User, Wallet
from wallet_action.wallet_manager import (get_transactions,
                                          get_balance)
from wallet_action.states import TransactionParams
from aiogram.dispatcher import FSMContext


async def on_start(message: types.Message):
    """
    Process the /start command.
    Create a new user in the database if it doesn't exist
    and send a welcome message with a keyboard.
    """
    user_id = message.from_user.id
    await User.get_or_create(telegram_id=user_id)
    response = await read_messages()
    board = await wallet_keyboard()
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
    await message.answer(response['send_wallet'])


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
    response = await read_messages()

    if not wallets:
        await message.answer(response["not_wallet"])
        return
    else:
        keyboard = await wallets_list_keyboard(wallets)
        await message.answer(response["your_wallet"], reply_markup=keyboard)


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


async def show_wallet_callback_handler(callback_query: types.CallbackQuery):
    """
    Handle the 'wallet: ' command.
    Extract the wallet address from the command and
    display a keyboard with wallet-related actions.
    """
    response = await read_messages()
    wallet_address = callback_query.data.replace("wallet:", "").strip()
    wallet_buttons = await create_wallet_buttons(wallet_address)
    await callback_query.message.answer(response["select_action"],
                                        reply_markup=wallet_buttons)


async def show_transactions_callback_handler(callback_query:
                                             types.CallbackQuery,
                                             state: FSMContext):
    """
    Handle the 'get_transactions: ' command.
    Extract the wallet address from the command, and prompt
    the user to input the number of transactions to display and
    the minimum token amount.
    Store the wallet address in the FSM state.
    """
    wallet_address = callback_query.data.replace(
        "get_transactions:", ""
    ).strip()
    await state.update_data(wallet_address=wallet_address)
    response = await read_messages()
    await callback_query.message.answer(response["enter_transactions_count"])
    await TransactionParams.input_count.set()


async def receive_transactions_count_handler(message: types.Message,
                                             state: FSMContext):
    """
    Handle the user input with the number of transactions to display.
    Validate the input and store the count in the FSM state.
    Prompt the user to input the minimum token amount.
    """
    response = await read_messages()
    try:
        count = int(message.text.strip())
    except ValueError:
        await message.reply(response["invalid_data"])
        return

    await state.update_data(input_count=count)

    await message.answer(response["enter_min_token_amount"])
    await TransactionParams.input_min_token_amount.set()


async def receive_min_token_amount_handler(message: types.Message,
                                           state: FSMContext):
    """
    Handle the user input with the minimum token amount.
    Validate the input and call the get_transactions function
    to display the transactions based on the input parameters.
    Finish the FSM state after displaying the transactions.
    """
    response = await read_messages()
    try:
        min_token_amount = int(message.text.strip())
    except ValueError:
        await message.reply(response["invalid_data"])
        return

    user_data = await state.get_data()
    count = user_data.get("input_count")
    wallet_address = user_data.get("wallet_address")
    await message.answer(response["transactions_for"].format(wallet_address))
    await get_transactions(wallet_address, message, count, min_token_amount)

    await state.finish()


async def show_token_balances_callback_handler(callback_query:
                                               types.CallbackQuery):
    """
    Handle the 'Показать балансы токенов: ' command.
    Extract the wallet address from the command and
    call the get_balance function to display the token balances.
    """
    response = await read_messages()
    wallet_address = callback_query.data.replace(
        "get_balance:", ""
    ).strip()
    await callback_query.message.answer(
        response["token_balances_for"].format(wallet_address)
    )
    await get_balance(wallet_address, callback_query)


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
    dp.register_callback_query_handler(
        show_wallet_callback_handler,
        lambda c: c.data.startswith("wallet:")
    )
    dp.register_callback_query_handler(
        show_transactions_callback_handler,
        lambda c: c.data.startswith("get_transactions:")
    )
    dp.register_callback_query_handler(
        show_transactions_callback_handler,
        lambda c: c.data.startswith("get_transactions:")
    )
    dp.register_callback_query_handler(
        show_token_balances_callback_handler,
        lambda c: c.data.startswith("get_balance:")
    )
    dp.register_message_handler(
        receive_transactions_count_handler,
        lambda message: message.text.isdigit(),
        state=TransactionParams.input_count,
    )
    dp.register_message_handler(
        receive_min_token_amount_handler,
        lambda message: message.text.isdigit(),
        state=TransactionParams.input_min_token_amount,
    )
