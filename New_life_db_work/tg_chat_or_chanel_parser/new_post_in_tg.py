from telethon import types
from telethon import TelegramClient, events
import csv


api_id = 19863647
api_hash = 'f85fc6d1c6baa9922236b5f30fe2294c'

client = TelegramClient('session_name', api_id=api_id, api_hash=api_hash)
client.start()


@client.on(events.NewMessage(chats=['Makcemjoi', 'u_job', 'myresume_ru', 'scrip_chillzone', 'prbezgranic']))
async def normal_handler(event):
    if isinstance(event.chat, types.Channel):
        username = event.chat.username
        add_chat_name = '@' + str(username)
        print('всё ок')

        with open("chat.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(add_chat_name)
            print('запись готова')
        await client.send_message("https://t.me/Makcemjoi", event.message)

if __name__ == '__main__':
    client.run_until_disconnected()
