from database import init_db
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from config import TELEGRAM_TOKEN
from handlers.start import start
import logging


# LOGS (importante para Railway)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


# Roteador de botões (menu)
async def button_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "profile":
        await query.edit_message_text("👤 Perfil do personagem (em construção)")
    elif data == "guild":
        await query.edit_message_text("🏰 Sistema de Guild / Claimed (em construção)")
    elif data == "war":
        await query.edit_message_text("⚔️ Guild War (em construção)")
    elif data == "duel":
        await query.edit_message_text("🤺 Sistema de Duelos (em construção)")
    elif data == "bounty":
        await query.edit_message_text("🎯 Sistema de Pistoleiros (em construção)")
    elif data == "premium":
        await query.edit_message_text("⭐ Premium & Vantagens (em construção)")


def main():
     init_db()  # cria o banco automaticamente
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_router))

    print("RedMask Bot iniciado...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
