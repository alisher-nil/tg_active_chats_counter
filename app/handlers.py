from telethon.events import NewMessage
from telethon.types import UpdateNewMessage, UpdateShortMessage, User

from app.core.db import get_async_session
from app.crud.users import CRUDUsers
from client import client


@client.on(NewMessage(incoming=True, forwards=False))
async def new_user_handler(event: NewMessage.Event):
    # TODO make session with dependency injection like FastAPI
    if not event.is_private or not isinstance(
        event.original_update,
        (UpdateShortMessage, UpdateNewMessage),
    ):
        return

    async for session in get_async_session():
        user = await CRUDUsers.get_user_by_telegram_id(event.chat_id, session)
        if user is None:
            sender: User = await event.get_sender()
            print(
                sender.first_name, sender.last_name, sender.username, sender.id
            )
            user = await CRUDUsers.create(sender.to_dict(), session)
            print(user)
        else:
            print("an old friend wrote something")
