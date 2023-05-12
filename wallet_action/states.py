from aiogram.dispatcher.filters.state import StatesGroup, State


class TransactionParams(StatesGroup):
    WalletAddress = State()
    input_count = State()
    input_min_token_amount = State()
