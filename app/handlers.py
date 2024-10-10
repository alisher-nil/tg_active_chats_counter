from telethon.events import NewMessage
from telethon.types import UpdateNewMessage, UpdateShortMessage, User

from client import client


@client.on(NewMessage(incoming=True, forwards=False))
async def new_user_handler(event: NewMessage.Event):
    if not event.is_private:
        return
    if not isinstance(
        event.original_update,
        (UpdateShortMessage, UpdateNewMessage),
    ):
        return
    sender: User = await event.get_sender()
    print(sender.first_name, sender.last_name, sender.username, sender.id)
    print("it's a new incoming message")
