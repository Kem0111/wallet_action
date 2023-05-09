from wallet_action.services.crypto_wallet_info.\
    wallet_transactions import TokenTransactions
from wallet_action.services.crypto_wallet_info.\
    wallet_balance import WalletTokens
from wallet_action.read_file import read_messages


async def get_transactions(address, message, tr_count, token_amount):
    transactions = TokenTransactions(address, count=tr_count,
                                     min_token_amount=token_amount)
    fields = await read_messages()

    if not transactions:
        return fields["error"]

    async for tx in transactions.get_result():
        await message.answer(
            f"{fields['date']}: {tx['datetime_obj']}\n"
            f"{fields['transaction']}: {tx['tx_hash']}\n"
            f"{fields['sendler']}: {tx['from_address']}\n"
            f"{fields['receiver']}: {tx['to_address']}\n"
            f"{fields['sum']}: {tx['value']}\n"
            "-----------------------"
        )


async def get_balance(address, callback_query):
    wallet_tokens = WalletTokens(address)
    fields = await read_messages()

    if not wallet_tokens:
        return fields["error"]

    async for token_result in wallet_tokens.get_result():
        await callback_query.message.answer(token_result)
