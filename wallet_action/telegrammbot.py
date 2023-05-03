import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from wallet_action.read_file import read_messages
from wallet_action.keyboard import wallet_keyboard

logging.basicConfig(level=logging.INFO)
API_TOKEN = "6148435016:AAFsRNgFZZBg26lRjnkOltGzs2BD_o--szU"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


async def on_start(message: types.Message):
    response = await read_messages()
    board = wallet_keyboard()
    await message.answer(response['start'], reply_markup=board)


@dp.message_handler(commands=['start'])
async def start_cmd_handler(message: types.Message):
    await on_start(message)


@dp.message_handler(lambda message: message.text == 'Добавить кошелек')
async def add_wallet_handler(message: types.Message):
    response = await read_messages()
    await message.answer(response['add_wallet'])


def start_bot():
    executor.start_polling(dp, skip_updates=True)
