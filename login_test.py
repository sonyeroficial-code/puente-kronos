import os
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE")

client = TelegramClient("sesion_puente", api_id, api_hash)

async def main():
    await client.start(phone=phone)
    me = await client.get_me()
    print("✅ Conectado correctamente")
    print("Usuario:", me.username or me.first_name)

with client:
    client.loop.run_until_complete(main())
