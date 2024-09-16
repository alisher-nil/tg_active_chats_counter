from datetime import datetime, timedelta, timezone
from enum import StrEnum

from telethon.tl.custom.dialog import Dialog

MESSAGE_MAX_LENGTH = 4096
LOCAL_TZ = timezone(timedelta(hours=5))


class TimeMapping(StrEnum):
    h = "hours"
    d = "days"
    w = "weeks"


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


def calculate_start_of_the_day():
    local_time = datetime.now(LOCAL_TZ)
    start_date = local_time.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    ).astimezone(timezone.utc)

    now = datetime.now(timezone.utc)
    start_date = now - timedelta(minutes=30)
    return start_date


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
