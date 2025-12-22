from telegram import Update
from telegram.ext import ContextTypes
from keyboards import main_menu


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🔥 *RedMask – Inteligência Tibiana*\n\n"
        "Domine informações que outros players não veem.\n"
        "Controle guerras, claimed hunts, duelos e recompensas\n"
        "em *tempo real*, direto no Telegram.\n\n"
        "⚠️ Tudo automático\n"
        "⚠️ Sem comandos\n"
        "⚠️ Vantagem real\n\n"
        "Escolha uma opção abaixo 👇"
    )

    await update.message.reply_text(
        text=text,
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )
