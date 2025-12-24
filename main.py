# main.py
import os
import sys
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)

from bot.menu import menu_router

print("🤖 Iniciando RedMask Tibia...")

# ============================
# TOKEN
# ============================
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    try:
        from config import BOT_TOKEN
        TOKEN = BOT_TOKEN
        print("⚠️ BOT_TOKEN carregado do config.py")
    except Exception:
        pass

if not TOKEN or ":" not in TOKEN:
    print("❌ ERRO CRÍTICO: BOT_TOKEN inválido ou inexistente")
    sys.exit(1)

# ============================
# APP
# ============================
app = ApplicationBuilder().token(TOKEN).build()

# ============================
# HANDLERS (FORMA CERTA)
# ============================
app.add_handler(CommandHandler("start", menu_router))
app.add_handler(CallbackQueryHandler(menu_router))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_router))

print("✅ Handlers carregados")
print("🚀 Bot rodando em polling")

app.run_polling(allowed_updates=["message", "callback_query"])
