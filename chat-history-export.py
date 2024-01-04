import os
import json
import datetime
from telethon import TelegramClient, events, sync
from settings import *
import asyncio

api_id = API_ID
api_hash = API_HASH
phone_number = PHONE_NUMBER
client = TelegramClient('session_name', api_id, api_hash)

import base64


def serialize(obj):
    """A custom serializer for non-serializable objects."""
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()  # Convert datetime objects to ISO format string
    elif isinstance(obj, bytes):
        return base64.b64encode(obj).decode('utf-8')  # Convert bytes to base64 string
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

async def dump_chat_history(chat_id):
    chat = await client.get_entity(chat_id)
    chat_title = ''.join(e for e in chat.title if e.isalnum())

    async for message in client.iter_messages(chat, reverse=True):
        date_str = message.date.strftime('%Y-%m-%d')
        directory = f'./{chat_title}/{date_str}'
        os.makedirs(directory, exist_ok=True)
        file_path = f'{directory}/messages.json'

        with open(file_path, 'a') as file:
            message_dict = message.to_dict()
            # Serialize the message dict with the custom serialize function
            json.dump(message_dict, file, default=serialize)
            file.write('\n')

async def main():
    await client.start()
    async for dialog in client.iter_dialogs():
        if dialog.is_group or dialog.is_channel:
            await dump_chat_history(dialog.id)
    await client.stop()

if __name__ == '__main__':
    asyncio.run(main())


async def main():
    # Fetching all the chats
    async for dialog in client.iter_dialogs():
        if dialog.is_group or dialog.is_channel:
            await dump_chat_history(dialog.id)

with client:
    client.loop.run_until_complete(main())
