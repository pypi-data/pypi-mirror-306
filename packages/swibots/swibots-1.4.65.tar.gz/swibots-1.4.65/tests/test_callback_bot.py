import logging

logging.basicConfig(level=logging.INFO)

from swibots import (
    BotApp,
    RegisterCommand,
    CommandEvent,
    BotContext,
    InlineMarkup,
    InlineKeyboardButton,
    CallbackQueryEvent,
)


TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6OTgyLCJpc19ib3QiOnRydWUsImFjdGl2ZSI6dHJ1ZSwiaWF0IjoxNjg5NDE0NTE3LCJleHAiOjIzMjA1NjY1MTd9.DNlqVeGHmlQIEKfj-H9SF9Hb654rMc48YLLWkc1fJoQ"
app = BotApp(TOKEN).register_command([RegisterCommand("start", "get message")])


@app.on_command("start")
async def an(ctx: BotContext[CommandEvent]):
    await ctx.event.message.respond(
        "Hello",
        inline_markup=InlineMarkup(
            [
                [
                    InlineKeyboardButton("With Alert", callback_data="waler"),
                    InlineKeyboardButton("Without", callback_data="wwal"),
                ],
            ]
        ),
    )


@app.on_callback_query()
async def callback(ctx: BotContext[CallbackQueryEvent]):
    show_alert = ctx.event.callback_data == "waler"
    print(ctx.event.query_id)
    print(
        await ctx.event.answer(
            "This is a long text\n\nDo you agree?\nThis is a secret box!\n\nGood if you know",
            show_alert=show_alert,
        )
    )


app.run()
