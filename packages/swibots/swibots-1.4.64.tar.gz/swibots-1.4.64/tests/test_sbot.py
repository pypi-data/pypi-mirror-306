import logging

logging.basicConfig(level=logging.INFO)

import asyncio
from glob import glob
from swibots import (
    BotApp,
    BotContext,
    CommandEvent,
    InlineMarkup,
    InlineKeyboardButton,
    MediaUploadRequest,
    RegisterCommand,
    CommandHandler,
    UploadProgress
)

app = BotApp(
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6OTc1LCJpc19ib3QiOnRydWUsImFjdGl2ZSI6dHJ1ZSwiaWF0IjoxNjg5MTU5NjEzLCJleHAiOjIzMjAzMTE2MTN9.lfLspX1PKUdOdKDPMFHe3PtGSycdUEnA95QbUahSB6k"
).register_command(
    [RegisterCommand("start", "Ok", False), RegisterCommand("handler", "ok")]
)

# app.update_bot_commands()

@app.on_command("start")
async def pas(ctx: BotContext[CommandEvent]):
    m = ctx.event.message
    app.register_command(
        [RegisterCommand("hiii", "d")]
    )
    return
    for _ in range(5):
        message = m._prepare_response()
        message.message = "Text"
        await m.reply(message, MediaUploadRequest(
            "../Switch.zip",   
            block=True
        ))
    print("no blocking")
    return
    ctx.bot.update_bot_commands()
    app.register_command(
        [
            RegisterCommand("standup", "lot see")
        ]
    )
    await ctx.update_bot_commands()
    await m.send("Hi")
    print(m)
    async def prog(ct: UploadProgress):
         print(ct.file_name, ct.current, ct.readed)
    return
    print(await asyncio.gather(*[
         message.send("hmm", MediaUploadRequest("file.zip", callback=prog, block=True))  for _ in range(10)
     ]))

    #    print(ctx.handlers)
#    for f in glob("swibots/api/*py"):
 #       await m.send("hi", MediaUploadRequest(f))
#     async def prog(ct: UploadProgress):
#         print(ct.file_name, ct.current, ct.readed)
#     print(await asyncio.gather(*[
#         m.send("hmm", MediaUploadRequest("../Switch.zip", callback=prog, block=True))  for _ in range(10)
#     ]))
# #        ]:
#  #       await _
#     #    async def mm(ct):
#     #       print(ct)
#     #  ctx.bot.add_handler(CommandHandler("handler", mm))
#     return
#     for file in glob("swibots/api/bot/***py"):
#         print(file)
#         await m.respond(media=MediaUploadRequest(file))
#     #        return
#     return
    c = await m.respond(
        "Hi", inline_markup=InlineMarkup([[InlineKeyboardButton("See", url="uo")]])
    )
    await asyncio.sleep(2)
    await c.edit_text(
        "Hello",
        inline_markup=InlineMarkup(
            [
                [InlineKeyboardButton("Koila", url="aa")],
                [InlineKeyboardButton("Hmm", url="aa")],
            ]
        ),
    )

app.register_command(
    [RegisterCommand("hello", "description")]
)

async def start_and_edit():
    await app.start()
    print(app._register_commands)
    print(await app.get_message(75555))

app.run()

#app._loop.run_until_complete(start_and_edit())
#app._loop.run_forever()


# app.run()
