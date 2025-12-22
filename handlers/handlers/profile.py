from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters

from database import add_user, add_or_update_character, get_characters
from scraper.character import get_character


async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    username = update.effective_user.username

    add_user(telegram_id, username)

    chars = get_characters(telegram_id)

    text = "👤 *Meu Perfil*\n\n"

    if not chars:
        text += "Você ainda não adicionou nenhum personagem.\n\n"
        text += "✏️ Envie agora o *nome do personagem* para adicionar."
    else:
        text += "Seus personagens:\n"
        for c in chars:
            text += f"• `{c}`\n"
        text += "\n✏️ Envie o nome de um novo personagem para adicionar."

    await update.callback_query.edit_message_text(
        text=text,
        parse_mode="Markdown"
    )

    context.user_data["awaiting_char_name"] = True


async def receive_char_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("awaiting_char_name"):
        return

    char_name = update.message.text.strip()
    telegram_id = update.effective_user.id

    char = get_character(char_name)

    if not char:
        await update.message.reply_text("❌ Personagem não encontrado no Tibia.")
        return

    add_or_update_character(telegram_id, char)

    await update.message.reply_text(
        f"✅ Personagem *{char['name']}* adicionado com sucesso!\n"
        f"🌍 Mundo: {char['world']}\n"
        f"⚔️ Level: {char['level']}\n"
        f"🧙 Vocação: {char['voc']}",
        parse_mode="Markdown"
    )

    context.user_data["awaiting_char_name"] = False
