import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import TELEGRAM_TOKEN
from database import init_db
from database_duel import create_duel_tables

from handlers.start import start
from handlers.profile import show_profile, receive_char_name
from handlers.duel import (
    duel_menu_handler,
    duel_create,
    duel_list,
    duel_receive_input,
)

# ======================
# LOGS
# ======================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


# ======================
# ROUTER DE BOTÕES
# ======================
async def button_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "profile":
        await show_profile(update, context)

    elif data == "duel":
        await duel_menu_handler(update, context)

    elif data == "duel_create":
        await duel_create(update, context)

    elif data == "duel_list":
        await duel_list(update, context)

    elif data == "back_main":
        await start(update, context)

    else:
        await query.edit_message_text("⚠️ Opção inválida.")


# ======================
# MAIN
# ======================
def main():
    # Inicializa bancos
    init_db()
    create_duel_tables()

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Comandos
    app.add_handler(CommandHandler("start", start))

    # Botões
    app.add_handler(CallbackQueryHandler(button_router))

    # Inputs de texto (perfil e duelo)
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, receive_char_name)
    )
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, duel_receive_input)
    )

    print("🔥 RedMask Bot iniciado com sucesso")

    app.run_polling(allowed_updates=Update.ALL_TYPES)


# ======================
# ENTRYPOINT
# ======================
if __name__ == "__main__":
    main()
