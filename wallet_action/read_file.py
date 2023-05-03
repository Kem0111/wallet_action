import aiofiles
import json


async def read_messages():
    async with aiofiles.open('response_messages.json', 'r') as f:
        content = await f.read()
        text = json.loads(content)
    return text
