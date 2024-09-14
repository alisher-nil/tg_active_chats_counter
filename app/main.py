import logging
import os

from dotenv import load_dotenv
from icecream import ic  # noqa: F401
from telethon import TelegramClient, events
from telethon.types import Channel, Chat, User

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.WARNING,
)
load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
USER_PASSWORD = os.getenv("USER_PASSWORD")
USER_PHONE = os.getenv("USER_PHONE")
client = TelegramClient("dev", API_ID, API_HASH)


@client.on(events.NewMessage(incoming=True))
async def counter(event: events.NewMessage.Event):
    print("Incoming message")

    if event.is_private:
        from_user: User = await event.get_chat()
        print(
            f"Private message from {from_user.first_name} "
            f"{from_user.last_name} ({from_user.id})"
        )
    else:
        from_channel: Channel = await event.get_chat()
        print(
            f"Group message in channel {from_channel.title} ({from_channel.id})",
            event.chat_id,
        )


client.start(USER_PHONE, USER_PASSWORD)
client.run_until_disconnected()
