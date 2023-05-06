import re


ETHEREUM_ADDRESS_REGEX = re.compile("^0x[a-fA-F0-9]{40}$")


async def is_valid_ethereum_address(address: str) -> bool:
    return bool(ETHEREUM_ADDRESS_REGEX.match(address))
