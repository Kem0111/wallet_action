import pytest
from wallet_action.validator import is_valid_ethereum_address


@pytest.mark.asyncio
async def test_is_valid_ethereum_address():
    valid_address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
    invalid_address = "0xInvalidEthereumAddress"

    assert await is_valid_ethereum_address(valid_address) is True
    assert await is_valid_ethereum_address(invalid_address) is False
