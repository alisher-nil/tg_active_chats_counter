import asyncio
import logging
from datetime import datetime

from telethon.events import NewMessage
from telethon.tl.custom.dialog import Dialog
from telethon.tl.patched import MessageService
from telethon.tl.types import MessageActionContactSignUp

from client import client
from config import settings
from utils import (
    TimeMapping,
    calculate_start_end_date,
    calculate_start_of_the_day,
    get_verbose_responses,
)

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)


@client.on(
    NewMessage(
        outgoing=True,
        forwards=False,
        pattern=(
            r"^\/stats"  # trigger
            r"( (?P<length>\d{1,3})(?P<period>[hwd]))?"  # length and period
            r"(?P<verbosity> -v)?$"  # verbosity
        ),
    )
)
async def handler(event: NewMessage.Event):
    chat = await event.get_chat()
    sender = await event.get_sender()
    if sender.is_self and chat == sender:
        params = event.pattern_match.groupdict()
        length = params.get("length")
        period = params.get("period")
        if length is None and period is None:
            await respond_with_first_time_users(event, params)
        else:
            await respond_with_active_chats(event, params)


async def respond_with_active_chats(event: NewMessage.Event, params: dict):
    length = params.get("length")
    period = params.get("period")
    start_date, end_date = calculate_start_end_date(length, period)
    active_chats = await get_active_private_chats(start_date, end_date)
    await event.reply(
        f"Active private chats in the last {length} {TimeMapping[period]}: {len(active_chats)}"
    )
    if params.get("verbosity") and active_chats:
        messages = get_verbose_responses(active_chats)
        for message in messages:
            await event.reply(message)


async def respond_with_first_time_users(event: NewMessage.Event, params: dict):
    start_date = calculate_start_of_the_day()
    first_time_chats = await get_first_time_users(start_date)
    await event.reply(f"New private chats dotay: {len(first_time_chats)}")
    if params.get("verbosity") and first_time_chats:
        messages = get_verbose_responses(first_time_chats)
        for message in messages:
            await event.reply(message)


async def get_first_time_users(start_date: datetime) -> list[Dialog]:
    first_time_users = []
    me = await client.get_me()
    async for dialog in client.iter_dialogs(
        ignore_migrated=True,
        archived=False,
        ignore_pinned=True,
    ):
        if (
            dialog.is_user
            and dialog.entity != me
            and not dialog.entity.bot
            and not dialog.entity.support
            and not dialog.entity.deleted
        ):
            if dialog.date < start_date:
                break

            if isinstance(
                dialog.message,
                MessageService,
            ) and isinstance(
                dialog.message.action,
                MessageActionContactSignUp,
            ):
                continue

            messages = await client.get_messages(
                dialog,
                limit=1,
                reverse=True,
            )
            first_message = messages[0]
            if first_message.date >= start_date:
                first_time_users.append(dialog)

    return first_time_users


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


async def main():
    await client.start(settings.user_phone, settings.user_password)
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
