from telethon import TelegramClient

from config import settings

client = TelegramClient("dev", settings.api_id, settings.api_hash)
