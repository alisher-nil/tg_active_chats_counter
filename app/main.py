import asyncio
import logging

import handlers  # noqa: F401
from client import client
from config import settings

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)


async def main():
    await client.start(settings.user_phone, settings.user_password)
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
