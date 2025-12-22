# ==============================
# ARQUIVO PRINCIPAL DO BOT
# ==============================

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# COMANDO /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Bot RedMask ligado com sucesso!"
    )

def main():
    # IMPORTA O TOKEN DO BOT
    from config import TELEGRAM_TOKEN

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # REGISTRA O COMANDO /start
    app.add_handler(CommandHandler("start", start))

    print("🤖 Bot iniciado...")
    app.run_polling()

if __name__ == "__main__":
    main()
