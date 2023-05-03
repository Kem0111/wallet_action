from wallet_action.telegrammbot import start_bot
from wallet_action.db_manager import init_db
import asyncio


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    start_bot()
