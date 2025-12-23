from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import (
    add_user,
    get_characters,
    add_or_update_character
)

# =========================
# MOSTRAR PERFIL
# =========================
async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user

    add_user(user.id, user.username)

    chars = get_characters(user.id)

    text = "👤 *SEU PERFIL*\n\n"

    if not chars:
        text += "❌ Nenhum personagem vinculado.\n"
    else:
        text += "🧙 Personagens vinculados:\n"
        for c in chars:
            text += f"• {c}\n"

    keyboard = [
        [InlineKeyboardButton("➕ Adicionar personagem", callback_data="add_char")],
        [InlineKeyboardButton("🔄 Atualizar personagem", callback_data="update_char")],
        [InlineKeyboardButton("🔙 Voltar", callback_data="back_main")]
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


# =========================
# RECEBER NOME DO CHAR
# =========================
async def receive_char_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "awaiting_char_name" not in context.user_data:
        return

    char_name = update.message.text.strip()
    telegram_id = update.effective_user.id

    # salva nome provisoriamente
    context.user_data["char_name"] = char_name
    context.user_data["awaiting_char_name"] = False
    context.user_data["awaiting_char_data"] = True

    await update.message.reply_text(
        "✅ Nome salvo!\n\n"
        "Agora envie os dados no formato:\n\n"
        "`Mundo | Level | Vocação | Guild`\n\n"
        "Exemplo:\n"
        "`Antica | 350 | Sorcerer | RedMask`",
        parse_mode="Markdown"
    )


# =========================
# RECEBER DADOS DO CHAR
# =========================
async def receive_char_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("awaiting_char_data"):
        return

    try:
        parts = [p.strip() for p in update.message.text.split("|")]
        world, level, voc, guild = parts

        char = {
            "name": context.user_data["char_name"],
            "world": world,
            "level": int(level),
            "voc": voc,
            "guild": guild if guild else "Sem guild"
        }

        add_or_update_character(update.effective_user.id, char)

        context.user_data.clear()

        await update.message.reply_text(
            "✅ Personagem salvo com sucesso!\n\n"
            "Use /start para voltar ao menu."
        )

    except Exception:
        await update.message.reply_text(
            "❌ Formato inválido.\n"
            "Use exatamente:\n"
            "`Mundo | Level | Vocação | Guild`",
            parse_mode="Markdown"
        )


# =========================
# CALLBACKS DO PERFIL
# =========================
async def profile_button_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data == "add_char" or data == "update_char":
        context.user_data.clear()
        context.user_data["awaiting_char_name"] = True

        await query.edit_message_text(
            "🧙 Envie o *nome do personagem* exatamente como no Tibia:",
            parse_mode="Markdown"
        )
