import logging
import os

from dotenv import load_dotenv
from icecream import ic  # noqa: F401
from telethon import TelegramClient, events

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.WARNING,
)
load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
client = TelegramClient("dev", api_id, api_hash)


@client.on(events.NewMessage)
async def counter(event):
    pass


client.start()
client.run_until_disconnected()
