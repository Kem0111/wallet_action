from wallet_action.services.crypto_wallet_info.common import WalletManager
import datetime


class TokenTransactions(WalletManager):
    """
    TokenTransactions is a class for fetching
    ERC-20 token transactions of a specific wallet.
    It extends the WalletManager class to handle
    token transaction-specific operations.
    """

    def __init__(self, address: str, count: int = 1,
                 min_token_amount: int = 1) -> None:
        """
        Initialize the TokenTransactions class with an
        Ethereum wallet address,
        a count for the number of transactions to fetch,
        and a minimum token amount
        for filtering transactions.
        """
        super().__init__(address)
        self.count = count
        self.min_token_amount = min_token_amount

    async def get_transactions(self):
        """
        Fetches token transactions from the Etherscan API and filters
        them based on the minimum token amount specified.
        """
        # Fetch data from the Etherscan API
        data = await self.request()

        if not data:
            return False
        # Filter transactions based on the minimum token amount
        transactions = [
            tx for tx in data["result"]
            if tx["to"].lower() == self.address.lower() or
            tx["from"].lower() == self.address.lower() and
            int(tx["value"]) / (
                self._DECIMAL_BASE ** int(tx["tokenDecimal"])
            ) >= self.min_token_amount
        ][:self.count]

        return transactions

    async def get_result(self):
        """
        Yields token transaction data as dictionaries containing the timestamp,
        hash, sender address, receiver address,
        and transaction value with token symbol.
        """
        # Fetch transactions
        transactions = await self.get_transactions()

        # Yield transaction data as dictionaries
        for transaction in transactions:
            timestamp = int(transaction['timeStamp'])
            token_decimal = int(transaction["tokenDecimal"])
            token_symbol = transaction["tokenSymbol"]

            yield {
                "datetime_obj": datetime.datetime.fromtimestamp(timestamp),
                "tx_hash": transaction['hash'],
                "from_address": transaction['from'],
                "to_address": transaction['to'],
                "token_symbol": transaction["tokenSymbol"],
                "value": f"""{int(transaction['value']) / (
                    self._DECIMAL_BASE ** token_decimal
                )} {token_symbol}""",
            }
