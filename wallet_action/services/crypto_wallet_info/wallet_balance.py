from wallet_action.services.crypto_wallet_info.common import WalletManager


class WalletTokens(WalletManager):
    """
    WalletTokens is a class for retrieving token balances
    of an Ethereum wallet address.
    It inherits from WalletManager and implements the get_url
    method specific to token transactions.
    """

    async def get_tokens(self):
        """
        Returns the token balances of the wallet address
        by processing the token transactions.
        """

        # Fetch the transaction data from Etherscan API
        data = await self.request()

        if not data:
            return False

        # Initialize an empty dictionary to store token balances
        token_balances = {}

        # Iterate through the transactions and update the token balances
        # The `token_decimals` variable can have different values for different
        # tokens.In this code, the value of `token_decimals` is extracted from
        # the transaction information for each token using:
        # `token_decimals = int(tx["tokenDecimal"])`.

        # For Ethereum, the value of `token_decimals` is 18, but for other
        # ERC-20 tokens, this value can be different.
        for tx in data["result"]:
            token_symbol = tx["tokenSymbol"]
            token_decimals = int(tx["tokenDecimal"])

            # Initialize the balance for the token if not already present
            if token_symbol not in token_balances:
                token_balances[token_symbol] = 0

            # If the wallet address is the recipient, add the token amount
            if tx["to"].lower() == self.address.lower():
                token_balances[token_symbol] += (
                    int(tx["value"]) / (self._DECIMAL_BASE ** token_decimals)
                )
            # If the wallet address is the sender, subtract the token amount
            elif tx["from"].lower() == self.address.lower():
                token_balances[token_symbol] -= (
                    int(tx["value"]) / (self._DECIMAL_BASE ** token_decimals)
                )

        return token_balances

    async def get_result(self):
        """
        Yields the token balances as formatted strings.
        """
        token_balances = await self.get_tokens()

        for token, balance in token_balances.items():
            yield f"{token}: {balance}"
