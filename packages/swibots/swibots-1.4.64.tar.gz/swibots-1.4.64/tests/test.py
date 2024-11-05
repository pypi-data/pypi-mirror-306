from swibots import (
    BotApp,
    MessageEvent,
    BotContext,
    CommandEvent,
    InlineMarkup,
    InlineKeyboardButton,
    CallbackQueryEvent,
    EmbeddedMedia,
    EmbedInlineField,
    Message,
    RegisterCommand,
    MediaUploadRequest,
    filters
)

import logging
import os

logging.basicConfig(level=logging.INFO)
import asyncio

app = BotApp(
  
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6OTc1LCJpc19ib3QiOnRydWUsImFjdGl2ZSI6dHJ1ZSwiaWF0IjoxNjg5MTU5NjEzLCJleHAiOjIzMjAzMTE2MTN9.lfLspX1PKUdOdKDPMFHe3PtGSycdUEnA95QbUahSB6k"
      #  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6OTgyLCJpc19ib3QiOnRydWUsImFjdGl2ZSI6dHJ1ZSwiaWF0IjoxNjg5NDE0NTE3LCJleHAiOjIzMjA1NjY1MTd9.DNlqVeGHmlQIEKfj-H9SF9Hb654rMc48YLLWkc1fJoQ"
)
app.register_command([RegisterCommand("start", "Get start", True)])
app.register_command(
    [RegisterCommand("testcancel", "r", True)]
).register_command([
    RegisterCommand("cancel", "a")
])

global client
client = None

@app.on_callback_query()
async def eee(e):
    print(type(e.event.message.user_id))

@app.on_message(filters.community("30338819-7b57-4877-821f-b4ce2521614c"))
async def cce(e: BotContext[MessageEvent]):
#    print(e.event.message.replied_to)
    print(e.user.id, type(e.user.id))
    return
    await e.event.message.reply_text("Hi", inline_markup=InlineMarkup(
        [[
            InlineKeyboardButton("ij", callback_data="aa")
        ]]
    ))
    return
    print(e.event.message.replied_to, e.event.message.replied_to_id)

#    ct = await e.event.message.reply_text("https://google.com")
    return
#    m = await e.event.message.reply_text("Hello")
    c = await e.event.message.reply_text("hi")
    print(c.replied_to, c.replied_to_id)
    return
    print(m.replied_to_id, type(m.replied_to_id))
    print(m.replied_to)

#    print(await (await m.get_replied_message()).get_replied_message())

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

FILE =  r"C:\Users\Deves\Downloads\lineage-14.1-20170911-UNOFFICIAL-mocha.zip" # "../Switch.zip" # "test1.bin" # r"C:\Users\Deves\Downloads\5GB.bin" #"../Switch.zip" #r"C:\Users\Deves\Downloads\lineage-14.1-20170911-UNOFFICIAL-mocha.zip"

@app.on_command("cancel")
async def cance(e):
    global client
    client.cancel()
    await e.event.message.reply_text("cancelled!")

@app.on_command("start"#, filter=filters.community("30338819-7b57-4877-821f-b4ce2521614c")
                )
async def _eeee(e: BotContext[CommandEvent]):
#    print(e.event.message)
    m = e.event.message
    print(m)
    filesize = humanbytes(os.path.getsize(FILE))
    test = await m.reply_text("Processing")
    global last
    last = 0

    async def progress(c):
        print("Uploaded", humanbytes(c.readed), "Total", filesize)
        #global last
       # _is = last / c.readed > 10*1024*1024
       # last = c.readed
       # if _is:
        global client
        client = c.client
        await test.edit_text(
                f"Uploaded: {humanbytes(c.readed)}\nTotal: {filesize}"
        )#
#        if c.readed > 1024*2:
#         c.client.cancel()

    msg = await e.event.message.send("see", MediaUploadRequest(
        FILE,
        callback=progress,
#        block=
    ))
    print(msg)
    print("async")
    return



    async def progress(c):
        print("Uploaded", humanbytes(c.readed), "Total", filesize)
#        c.client.cancel()
 #       if c.readed > 1024*2:
 #       c.client.cancel()

    await e.event.message.send("see", MediaUploadRequest(
        FILE,
        callback=progress,
#        block=False
    ))
    print("async")

    return
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
    print(await e.enable_messages(m.community_id,
                            channel_id=m.channel_id,
                            group_id=m.group_id))
    return
    print(type(e.event.message.replied_to), 
          type(await e.event.message.get_replied_message()))
#    print(e.event.message)
#    await e.event.message.reply_text("Hi")

app.run()
exit()

async def main():
#    print(app.bot.user_name)
#    app.bot.
    await app.start()
    print(await app.get_user(972))
    return
    print(app.user, type(app.user))
    m = await app.get_message(799507)
    nm = m._prepare_response()
    nm.message = "Hello"
    chat = await m.reply(
        nm
    )
    print(chat.replied_to)
    await app.stop()
    return
    app.get_all_channels()
    print(await app.get_message(782235))
    app.list_restricted_users()
    app.get_bot_info()
    app.get_tournaments
    return
    await app.send_message(Message(
        app,
        community_id="28375c0f-ef39-485f-9aa6-8eeafab03a5c",
        group_id="640ee738-8ee9-4112-b894-5c4097cdfdad"
    ), media=MediaUploadRequest(
        path="docs/static/img/switch-logo.png",
        thumbnail="y.png"
    ),)
#    msg = Message(
#        app,
 #       group_id=""
  #  )
#    print(await app.get_bot_info(972))

#    print((await app.get_user(972)).name)
    return
    await app.send_message(Message(
        app,
        group_id="640ee738-8ee9-4112-b894-5c4097cdfdad",
        community_id="28375c0f-ef39-485f-9aa6-8eeafab03a5c",
        message="Hi",
        request_id=1
    ), media=MediaUploadRequest(
        path=".gitignore",
        description="OK"
    ))
 #   print(await app.get_messaging_enabled("f84cd816-cd4b-4e93-9202-695a6f9db55b", "bd3a805c-7987-4b39-a66d-f2afd6e6d1ec",))
  #  print(
   #     await app.get_messaging_enabled("f84cd816-cd4b-4e93-9202-695a6f9db55b", "bd3a805c-7987-4b39-a66d-f2afd6e6d1ec")
    #)
    
#    await app.enable_messages("")
  #  game = await app.update_leaderboard(
 #       "02d82f33-7f54-4538-a6e5-bea4956c809f", 973, 260
#    )
    #   print(game)
#    print(await app.get_global_leaderboard())
    return
    message = Message(app)
    message.message = "Hello"
    message.receiver_id = 972
    #    message.inline_markup = InlineMarkup([[
    #       InlineKeyboardButton("Test")
    #  ]])
    ok = await app.send_message(
        message,
        media=EmbeddedMedia(
            thumbnail="D:\Switch-Bots-Python-Library\docs\static\img\logo.png",
            description="J",
            inline_fields=[[EmbedInlineField("", "", "e")]],
        ),
    )
    await ok.edit_text(
        "hea",
        EmbeddedMedia(
            title="E",
            thumbnail="D:\Switch-Bots-Python-Library\docs\static\img\docusaurus.png",
            inline_fields=[[EmbedInlineField("", "", "c")]],
        ),
    )
    print(ok.id)
    return
    print(
        await ok.edit_text(
            None,
            EmbeddedMedia(
                thumbnail=None,
                description="HELLOOOOO",
                inline_fields=[[EmbedInlineField("", "", "Sorry")]],
            ),
        )
    )


#    print(ok)
# print(
#     (
#         await app.get_messaging_enabled(
#             "f84cd816-cd4b-4e93-9202-695a6f9db55b",
#             "bd3a805c-7987-4b39-a66d-f2afd6e6d1ec",
#         )
#     )[0].bot_id
# )


asyncio.run(main())
exit()


@app.on_message()
async def onMessage(ctx: BotContext[MessageEvent]):
    await ctx.event.message.send(
        EmbeddedMedia(
            thumbnail=None,
            header_icon="",
            title="a",
            description="a",
            inline_fields=[[EmbedInlineField("", "a", "aa")]],
        )
    )
    #    print(ctx.event.message)
    #    return
    x = await ctx.event.message.respond(
        "hi",
        inline_markup=InlineMarkup(
            [
                [
                    InlineKeyboardButton("Hi", callback_data="a"),
                    InlineKeyboardButton("C", callback_data="d"),
                ]
            ],
        ),
    )
    await x.edit_text("bye")


@app.on_callback_query()
async def ee(e: BotContext[CallbackQueryEvent]):
    print(e.event.callback_data)
    await e.event.message.send("hi")


@app.on_member_joined()
async def onJoin(ctx):
    print(ctx.event)


app.run()
