from telethon.events import NewMessage

from client import client


@client.on(NewMessage(incoming=True, forwards=False))
async def new_user_handler(event: NewMessage.Event):
    if not event.is_private:
        return

    print(event.stringify())
    print(type(event))
