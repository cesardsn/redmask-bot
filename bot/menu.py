from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboards import main_menu
from bot.texts import MENU_TEXT
from handlers import (
    analysis, progress, routine, quests,
    avoid, events, premium, sponsor
)

async def menu_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    data = q.data

    if data == "menu":
        await q.edit_message_text(
            MENU_TEXT,
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
    elif data == "analysis":
        await analysis.run(q)
    elif data == "progress":
        await progress.run(q)
    elif data == "routine":
        await routine.run(q)
    elif data == "quests":
        await quests.run(q)
    elif data == "avoid":
        await avoid.run(q)
    elif data == "events":
        await events.run(q)
    elif data == "premium":
        await premium.run(q)
    elif data == "sponsor":
        await sponsor.run(q)
    elif data == "sponsor_pay":
        await sponsor.sponsor_pay(q, context)
