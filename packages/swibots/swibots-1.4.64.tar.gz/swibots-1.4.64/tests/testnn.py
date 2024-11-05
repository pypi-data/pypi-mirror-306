from pyrogram.client import Client
from pyrogram import filters
from datetime import datetime

app = Client(
    "bot",
    api_id=6,
    api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e",
    workers=100,
    bot_token="6248620141:AAFvCZVXdbe9OPS0R2Yc-9xfnMAnsM9VL4E"
)

@app.on_message(filters.document)
async def download(client, message):
    st = datetime.now()
    await message.download()
    print((datetime.now() - st).total_seconds() / 60)
app.run()