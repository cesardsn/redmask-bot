import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

from config import TELEGRAM_TOKEN

# Banco de dados
from database import init_db
from database_duel import create_duel_tables

# Handlers
from handlers.start import start
from handlers.profile import (
    show_profile,
    receive_char_name,
    receive_char_data,
    profile_button_router
)
from handlers.duel import (
    duel_menu_handler,
    duel_create,
    duel_list
)

# ======================
# LOGS (Railway / Debug)
# ======================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ======================
# ROUTER PRINCIPAL DE BOTÕES
# ======================
async def button_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # PERFIL
    if data == "profile":
        await show_profile(update, context)

    # DUEL
    elif data == "duel":
        await duel_menu_handler(update, context)

    elif data == "duel_create":
        await duel_create(update, context)

    elif data == "duel_list":
        await duel_list(update, context)

    # PLACEHOLDERS (futuro)
    elif data == "guild":
        await query.edit_message_text("🏰 Sistema de Guild / Claimed (em construção)")

    elif data == "war":
        await query.edit_message_text("⚔️ Guild War (em construção)")

    elif data == "bounty":
        await query.edit_message_text("🎯 Sistema de Pistoleiros (em construção)")

    elif data == "premium":
        await query.edit_message_text("⭐ Premium & Vantagens (em construção)")

    elif data == "back_main":
        await start(update, context)

# ======================
# MAIN
# ======================
def main():
    # Inicializa banco principal
    init_db()

    # Inicializa tabelas de duelo
    create_duel_tables()

    # Cria aplicação
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Comando inicial
    app.add_handler(CommandHandler("start", start))

    # Router geral de botões
    app.add_handler(CallbackQueryHandler(button_router))

    # Router específico do perfil
    app.add_handler(CallbackQueryHandler(profile_button_router))

    # Recebe textos (nome do char / dados do char)
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, receive_char_name)
    )

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, receive_char_data)
    )

    print("🔥 RedMask Bot iniciado com sucesso")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

# ======================
# ENTRYPOINT
# ======================
if __name__ == "__main__":
    main()
