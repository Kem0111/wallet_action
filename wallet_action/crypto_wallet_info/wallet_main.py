import asyncio
from wallet_action.crypto_wallet_info.\
    wallet_transactions import TokenTransactions
from wallet_action.crypto_wallet_info.wallet_balance import WalletTokens


async def main():
    address = "0x974CaA59e49682CdA0AD2bbe82983419A2ECC400"

    transactions = TokenTransactions(address, count=10, min_token_amount=5000)
    wallet_tokens = WalletTokens(address)

    print(f"Транзакции для кошелька {address}:")
    async for tx in transactions.get_result():
        print(f"Дата и время: {tx['datetime_obj']}")
        print(f"Транзакция: {tx['tx_hash']}")
        print(f"Отправитель: {tx['from_address']}")
        print(f"Получатель: {tx['to_address']}")
        print(f"Сумма: {tx['value']}")
        print("-----------------------")

    print(f"Балансы токенов для кошелька {address}:")
    async for token_result in wallet_tokens.get_result():
        print(token_result)


if __name__ == "__main__":
    asyncio.run(main())
