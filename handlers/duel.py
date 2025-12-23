from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from database_duel import (
    create_duel_tables,
    create_duel,
    get_open_duels,
    get_user_active_duel,
)
from database import get_characters

# ==============================
# MENU PRINCIPAL DE DUELOS
# ==============================
async def duel_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("➕ Criar Duelo", callback_data="duel_create")],
        [InlineKeyboardButton("📜 Ver Duelos Abertos", callback_data="duel_list")],
        [InlineKeyboardButton("⬅️ Voltar", callback_data="back_main")]
    ]

    await update.callback_query.edit_message_text(
        "🤺 *Sistema de Duelos*\n\n"
        "• Crie duelos por nível\n"
        "• Apenas jogadores do mesmo servidor\n"
        "• Sem premiação (apenas taxa futuramente)\n\n"
        "Escolha uma opção:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


# ==============================
# INICIAR CRIAÇÃO DE DUELO
# ==============================
async def duel_create(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.callback_query.from_user.id

    # verifica se já existe duelo ativo
    active = get_user_active_duel(telegram_id)
    if active:
        await update.callback_query.edit_message_text(
            "❌ Você já possui um duelo ativo.\n"
            "Finalize ou cancele antes de criar outro."
        )
        return

    chars = get_characters(telegram_id)

    if not chars:
        await update.callback_query.edit_message_text(
            "⚠️ Você precisa cadastrar ao menos um personagem primeiro."
        )
        return

    # salva estado
    context.user_data["duel_step"] = "min_level"

    await update.callback_query.edit_message_text(
        "🔢 Informe o *NÍVEL MÍNIMO* do duelo:",
        parse_mode="Markdown"
    )


# ==============================
# LISTAR DUELOS ABERTOS
# ==============================
async def duel_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.callback_query.from_user.id
    chars = get_characters(telegram_id)

    if not chars:
        await update.callback_query.edit_message_text(
            "⚠️ Cadastre um personagem primeiro."
        )
        return

    duels = list_open_duels(chars)

    if not duels:
        await update.callback_query.edit_message_text(
            "📭 Nenhum duelo disponível no seu servidor no momento."
        )
        return

    text = "📜 *Duelos Abertos*\n\n"
    for d in duels:
        text += (
            f"👤 Criador: {d['creator_char']}\n"
            f"🌍 Servidor: {d['world']}\n"
            f"🎯 Nível: {d['min_level']} - {d['max_level']}\n"
            f"🕒 Criado em: {d['created_at']}\n\n"
        )

    await update.callback_query.edit_message_text(
        text,
        parse_mode="Markdown"
    )


# ==============================
# RECEBER INPUTS (NÍVEIS)
# ==============================
async def duel_receive_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "duel_step" not in context.user_data:
        return

    text = update.message.text.strip()

    if not text.isdigit():
        await update.message.reply_text("❌ Digite apenas números.")
        return

    value = int(text)

    # PASSO 1 — nível mínimo
    if context.user_data["duel_step"] == "min_level":
        context.user_data["duel_min"] = value
        context.user_data["duel_step"] = "max_level"

        await update.message.reply_text(
            "🔢 Agora informe o *NÍVEL MÁXIMO* do duelo:",
            parse_mode="Markdown"
        )
        return

    # PASSO 2 — nível máximo
    if context.user_data["duel_step"] == "max_level":
        min_level = context.user_data["duel_min"]

        if value < min_level:
            await update.message.reply_text(
                "❌ O nível máximo não pode ser menor que o mínimo."
            )
            return

        telegram_id = update.message.from_user.id
        chars = get_characters(telegram_id)

        # usa o primeiro personagem como padrão
        creator_char = chars[0]

        create_duel(
            telegram_id=telegram_id,
            creator_char=creator_char["name"],
            world=creator_char["world"],
            min_level=min_level,
            max_level=value
        )

        # limpa estado
        context.user_data.clear()

        await update.message.reply_text(
            "✅ *Duelo criado com sucesso!*\n\n"
            "Jogadores compatíveis receberão notificação.",
            parse_mode="Markdown"
        )
