# main.py
import os
import sys
import asyncio
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)

from bot.menu import menu_router  # função original (sync)

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
    print("❌ BOT_TOKEN inválido")
    sys.exit(1)

# ============================
# ADAPTADOR ASYNC (A CHAVE)
# ============================
async def menu_adapter(update, context):
    # permite função sync dentro do PTB v20
    result = menu_router(update, context)
    if asyncio.iscoroutine(result):
        await result

# ============================
# APP
# ============================
app = ApplicationBuilder().token(TOKEN).build()

# ============================
# HANDLERS
# ============================
app.add_handler(CommandHandler("start", menu_adapter))
app.add_handler(CallbackQueryHandler(menu_adapter))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_adapter))

print("✅ Bot online e escutando comandos")
print("🚀 Polling iniciado")

app.run_polling(allowed_updates=["message", "callback_query"])
