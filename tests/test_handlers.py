import pytest
from aiogram import types
from unittest.mock import AsyncMock
from wallet_action.models import User
from wallet_action.read_file import read_messages
from wallet_action.keyboards import wallet_keyboard
from wallet_action.handlers.client import on_start


@pytest.mark.asyncio
async def test_on_start(mocker):
    # Create a mock of a message and a user
    message = types.Message()
    message.from_user = types.User(id=12345)
    message.answer = AsyncMock()  # Use AsyncMock instead of Mock

    # Mock database calls and the read_messages and wallet_keyboard functions
    mocker.patch.object(User, "get_or_create", return_value=(AsyncMock(),
                                                             False))
    # Call the handler
    await on_start(message)
    keyboard = await wallet_keyboard()
    # Check that the message was sent with the correct parameters
    response = await read_messages()
    message.answer.assert_called_once_with(response['start'],
                                           reply_markup=keyboard)
