# main.py
import os
from telegram.ext import ApplicationBuilder
from bot.menu import menu_router

TOKEN = os.environ.get("BOT_TOKEN")  # variável de ambiente do token
PORT = int(os.environ.get("PORT", 8443))

# Crie a aplicação do bot
app = ApplicationBuilder().token(TOKEN).build()

# Inclua todos os handlers/menu
app.include_router(menu_router)

# URL do webhook (substitua pelo domínio ou URL do Railway)
WEBHOOK_URL = f"https://{os.environ.get('RAILWAY_STATIC_URL')}/{TOKEN}"

# Inicialização via webhook
app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    webhook_url=WEBHOOK_URL
)
