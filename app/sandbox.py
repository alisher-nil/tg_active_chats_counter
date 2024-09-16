import logging
import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.custom.dialog import Dialog

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)
load_dotenv()

LOCAL_TZ = timezone(timedelta(hours=5))
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
USER_PASSWORD = os.getenv("USER_PASSWORD")
USER_PHONE = os.getenv("USER_PHONE")
MESSAGE_MAX_LENGTH = 4096
client = TelegramClient("dev", API_ID, API_HASH)


async def get_first_time_users(start_date: datetime) -> list[Dialog]:
    await client.start(USER_PHONE, USER_PASSWORD)
    me = await client.get_me()
    async for dialog in client.iter_dialogs(ignore_migrated=True):
        if (
            dialog.is_user
            and dialog.entity != me
            and not dialog.entity.bot
            and not dialog.entity.support
            and not dialog.entity.deleted
        ):
            if dialog.date < start_date:
                break
            messages = await client.get_messages(
                dialog,
                limit=1,
                reverse=True,
            )
            first_message = messages[0]
            print(dialog.name, first_message.date, first_message.text)


def compile_chat_info(chat: Dialog) -> str:
    username_link = (
        f"@{chat.entity.username}" if chat.entity.username else "No username"
    )
    display_name = chat.name if not chat.entity.deleted else "☠️ <deleted> ☠️"
    return f"{display_name} (`{chat.entity.id}`) - {username_link}"


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


end_date = datetime.now(timezone.utc)
local_time = datetime.now(LOCAL_TZ)
start_date = local_time.replace(
    hour=0,
    minute=0,
    second=0,
    microsecond=0,
).astimezone(timezone.utc)
with client:
    first_time_users = client.loop.run_until_complete(
        get_first_time_users(start_date)
    )

    # responses = get_verbose_responses(first_time_users)
    # for response in responses:
    #     print(response)
