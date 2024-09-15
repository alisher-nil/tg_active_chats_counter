import logging
import os
from datetime import datetime, timedelta, timezone
from enum import StrEnum

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.events import NewMessage
from telethon.tl.custom.dialog import Dialog

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)
load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
USER_PASSWORD = os.getenv("USER_PASSWORD")
USER_PHONE = os.getenv("USER_PHONE")
client = TelegramClient("dev", API_ID, API_HASH)


class TimeMapping(StrEnum):
    h = "hours"
    d = "days"
    w = "weeks"


@client.on(
    NewMessage(
        outgoing=True,
        forwards=False,
        pattern=(
            r"^\/stats"  # trigger
            r"( (?P<length>\d{1,3})(?P<period>[hwd]))"  # length and period
            r"(?P<verbosity> -v)?$"  # verbosity
        ),
    )
)
async def handler(event: NewMessage.Event):
    chat = await event.get_chat()
    sender = await event.get_sender()
    if sender.is_self and chat == sender:
        params = event.pattern_match.groupdict()
        length = params["length"]
        period = params["period"]

        start_date, end_date = calculate_start_end_date(length, period)
        active_chats = await get_active_private_chats(start_date, end_date)
        await event.reply(
            f"Active private chats in the last {length} {TimeMapping[period]}: {len(active_chats)}"
        )
        if params.get("verbosity"):
            response = get_verbose_response(active_chats)
            await event.reply(response)


def get_verbose_response(active_chats: list[Dialog]):
    result = []
    for chat in active_chats:
        username_link = (
            f"@{chat.entity.username}"
            if chat.entity.username
            else "No username"
        )
        name = chat.name if not chat.entity.deleted else "☠️ <deleted> ☠️"
        result.append(f"{name} (`{chat.entity.id}`) - {username_link}")

    return "\n".join(result)


def calculate_start_end_date(length: int, period: str):
    end_date = datetime.now(timezone.utc)

    time_delta_params = {TimeMapping[period]: int(length)}
    start_date = end_date - timedelta(**time_delta_params)

    return start_date, end_date


async def get_active_private_chats(start_date, end_date):
    dialogs = await client.get_dialogs()
    me = await client.get_me()

    active_chats = set()
    for dialog in dialogs:
        if (
            dialog.is_user
            and dialog.entity != me
            and not dialog.entity.bot
            and not dialog.entity.support
        ):
            last_message = dialog.message
            if start_date <= last_message.date <= end_date:
                active_chats.add(dialog)
    return active_chats


client.start(USER_PHONE, USER_PASSWORD)
client.run_until_disconnected()
