import aiohttp
import json
from typing import Optional


class WalletManager:
    """
    WalletManager is a base class for managing
    Ethereum wallet-related operations.
    It handles requests to the Etherscan API for fetching transaction data.
    """

    _ETHERSCAN_API_KEY = "YGFEJ9PR36IKH4EDHK3FDTC8E2RT3XEX54"
    _DECIMAL_BASE = 10

    def __init__(self, address: str) -> None:
        """
        Initialize the WalletManager with an Ethereum wallet address.
        """
        self.address = address

    async def request(self) -> Optional[dict]:
        """
        Sends a request to the Etherscan API and returns the JSON data.
        In case of errors, returns an error message or None.
        """
        try:
            # Create an HTTP session and fetch the URL
            async with aiohttp.ClientSession() as session:
                url = await self.get_url()

                async with session.get(url) as response:
                    if response.status != 200:
                        return "An error occurred, please try again later"

                    data = await response.text()
        except aiohttp.ClientError as e:
            print(f"Request error: {e}")
            return None

        try:
            # Load JSON data from the response text
            data = json.loads(data)
        except json.JSONDecodeError:
            return "An error occurred, please try again later"

        return data
