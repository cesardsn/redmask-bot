from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import BOT_TOKEN
from handlers.start import start, text_handler
from bot.menu import menu_router
from services.db import init_db

# Inicializa banco
init_db()

app = ApplicationBuilder().token(BOT_TOKEN).build()

# Comandos e handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(menu_router))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

print("🤖 RedMask Tibia iniciado")
app.run_polling()
