import logging

logging.basicConfig(level=logging.INFO)

from anitopy import parse
from swibots import (
    BotApp,
    RegisterCommand,
    CommandEvent,
    BotContext,
    DownloadProgress,
    UploadProgress,
)
from redis import Redis

app = BotApp(
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTIwNCwiaXNfYm90Ijp0cnVlLCJhY3RpdmUiOnRydWUsImlhdCI6MTY5MzEzNzczMSwiZXhwIjoyMzI0Mjg5NzMxfQ.xise4b6GtcssFDJZvLDrAF_uMqY1W7RgxidkDYIfpuw"
)

db = Redis(
    "redis-10791.c285.us-west-2-2.ec2.cloud.redislabs.com",
    port=10791,
    password="NBvAqmWbyHdBLzfd9zx7MbKi3xTsM42O",
    encoding="utf-8"
)
if db.ping():
    print("Started redis!")

app.register_command(
    [
        RegisterCommand("start", "Start the bot.", True),
        RegisterCommand("rename", "rename a file", True),
        RegisterCommand("setformat", "set file format", True),
        RegisterCommand("getformat", "Get file format", True)
    ]
)


@app.on_command("start")
async def getStart(ctx: BotContext[CommandEvent]):
    event = ctx.event.message
    await event.reply_text(
        """Hi, I am a file renamer bot!\nSend me a file and reply `/rename filename.ext` to it!
**Example of Auto Renaming:**
Before:
file Name: `[Anime Time] One Piece - 0213 - Round 3! The Round-and-Round Roller Race!.mkv`\

Formats:
'file_extension': 'mkv'
'episode_number': '0213'
'anime_title': 'One Piece'
'release_group': 'Anime Time'
'episode_title': 'Round 3! The Round-and-Round Roller Race!'

**Setting format**
/setformat [ChannelName] {episode_name} ({release_group}).{file_extension}
"""
    )


def get_progress_bar_string(pct):
    p = min(max(pct, 0), 100)
    cFull = int(p // 8)
    p_str = "■" * cFull
    p_str += "□" * (12 - cFull)
    return f"[{p_str}]"


def humanbytes(size):
    if not size:
        return "0 B"
    for unit in ["", "K", "M", "G", "T"]:
        if size < 1024:
            break
        size /= 1024
    if isinstance(size, int):
        size = f"{size}{unit}B"
    elif isinstance(size, float):
        size = f"{size:.2f}{unit}B"
    return size

@app.on_command("setformat")
async def setFileFormat(ctx: BotContext[CommandEvent]):
    event = ctx.event.message
    if not ctx.event.params:
        return await event.reply_text("Provide a format!\nRead /start for detailed info.")
    db.set(event.user_id, ctx.event.params)
    await event.reply_text("Updated!")

@app.on_command("getformat")
async def getFormat(ctx: BotContext[CommandEvent]):
    event = ctx.event.message
    getFormat = db.get(event.user_id)
    if not getFormat:
        return await event.reply_text("Format is not set!")
    await event.reply_text(f"Format:\n{getFormat.decode()}")

@app.on_command("rename")
async def renameBot(ctx: BotContext[CommandEvent]):
    event = ctx.event.message

    if not ctx.event.params:
        return await event.reply_text("Provide a file name")
    replied = await event.get_replied_message()
    if not replied or not replied.is_media:
        return await event.reply_text("Reply to a media message!")
    await processFile(event, replied, ctx.event.params)


async def processFile(event, replied, command):
    msg = await event.reply_text("Starting Process!")

    async def downloadCallback(clb: DownloadProgress):
        try:
            progress = (clb.downloaded / clb.total) * 100
        except ZeroDivisionError:
            progress = 0
        message = f"""
FileName: {clb.file_name}
{get_progress_bar_string(progress)} {int(progress)}
Size: {humanbytes(clb.total)}
"""
        await msg.edit_text(message)

    file = await replied.download(progress=downloadCallback)

    async def uploadCallback(clb: UploadProgress):
        try:
            progress = (clb.readed / clb.total) * 100
        except ZeroDivisionError:
            progress = 0
        message = f"""
Uploading {clb.file_name}
{get_progress_bar_string(progress)} {int(progress)}
Size: {humanbytes(clb.total)}r
"""
        await msg.edit_text(message)

    await event.reply_media(
        document=file,
        message="",
        description=command,
        progress=uploadCallback
    )
    await msg.delete()

@app.on_message()
async def onMessage(ctx: BotContext[CommandEvent]):
    event = ctx.event.message
    print(event)
    if event.media_link and event.is_media:
        print(event.media_link)
        nameFormat = db.get(event.user_id)
        print(nameFormat)
        if not nameFormat:
            return
        name = event.media_info.description
        parsed = parse(name)
        print(parsed)
        if not parsed:
            return
        try:
            new_name = nameFormat.decode().format(parsed)
        except Exception as er:
            return await event.reply_text(str(er))
        await processFile(event, event, new_name)

app.run()
