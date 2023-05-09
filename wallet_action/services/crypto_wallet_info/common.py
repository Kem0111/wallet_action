import aiohttp
import json
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()


class WalletManager:
    """
    WalletManager is a base class for managing
    Ethereum wallet-related operations.
    It handles requests to the Etherscan API for fetching transaction data.
    """

    _ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
    _DECIMAL_BASE = 10

    def __init__(self, address: str) -> None:
        """
        Initialize the WalletManager with an Ethereum wallet address.
        """
        self.address = address

    async def get_url(self, page: int = 1, offset: int = 10000):
        """
        Returns the URL for fetching token transactions or
        balance of the wallet address.
        """
        return (
            f"https://api.etherscan.io/api?module=account&"
            f"action=tokentx&address={self.address}&startblock=0&"
            f"endblock=99999999&sort=desc&apikey={self._ETHERSCAN_API_KEY}"
            f"&page={page}&offset={offset}"
        )

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
                        return False

                    data = await response.text()
        except aiohttp.ClientError:
            return False

        try:
            # Load JSON data from the response text
            data = json.loads(data)
        except json.JSONDecodeError:
            return False

        return data
