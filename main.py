# ==============================
# REDMASK BOT - MAIN
# ==============================

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from config import TELEGRAM_TOKEN


# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 RedMask Bot online!\n\nTudo pronto para começar."
    )


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("RedMask Bot iniciado...")
    app.run_polling()


if __name__ == "__main__":
    main()
