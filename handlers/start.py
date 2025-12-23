from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboards import main_menu
from bot.texts import MENU_TEXT
from services.users import register_user, get_user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    if not user:
        await update.message.reply_text(
            "👤 Bem-vindo Tibiano! Por favor, digite o nome do seu char principal:"
        )
        context.user_data["awaiting_char"] = True
        return
    await update.message.reply_text(
        MENU_TEXT,
        parse_mode="Markdown",
        reply_markup=main_menu()
    )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_char"):
        char_name = update.message.text
        register_user(update.effective_user.id, char_name)
        context.user_data["awaiting_char"] = False
        await update.message.reply_text(
            f"✅ Char '{char_name}' cadastrado!\nVocê já pode usar o bot.",
            parse_mode="Markdown"
        )
