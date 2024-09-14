import asyncio
import os

from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")


async def main():
    async with TelegramClient("anon", api_id, api_hash) as client:
        await client.send_message("me", "Hello, myself!")


if __name__ == "__main__":
    asyncio.run(main())
