from wallet_action.create_bot import dp
from aiogram.utils import executor
from wallet_action.models import init_db
import asyncio


def start_bot():
    """
    Start the bot and run it in polling mode.
    """
    from handlers import client

    client.register_handlers_client(dp)
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    start_bot()
