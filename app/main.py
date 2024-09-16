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

LOCAL_TZ = timezone(offset=timedelta(hours=3))
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
USER_PASSWORD = os.getenv("USER_PASSWORD")
USER_PHONE = os.getenv("USER_PHONE")
MESSAGE_MAX_LENGTH = 4096
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
            messages = get_verbose_responses(active_chats)
            for message in messages:
                await event.reply(message)


def get_verbose_responses(active_chats: list[Dialog]) -> list[str]:
    result = []
    active_chat_details = []
    message_length = 0
    for chat in active_chats:
        chat_info = compile_chat_info(chat)
        message_length += len(chat_info) + 1
        if message_length > MESSAGE_MAX_LENGTH:
            result.append("\n".join(active_chat_details))
            active_chat_details = []
        active_chat_details.append(chat_info)

    result.append("\n".join(active_chat_details))
    return result


def compile_chat_info(chat: Dialog) -> str:
    username_link = (
        f"@{chat.entity.username}" if chat.entity.username else "No username"
    )
    display_name = chat.name if not chat.entity.deleted else "☠️ <deleted> ☠️"
    return f"{display_name} (`{chat.entity.id}`) - {username_link}"


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
