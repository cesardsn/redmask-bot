from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database import get_characters
from database_duel import create_duel, get_open_duels, accept_duel


async def duel_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.edit_message_text(
        "⚔️ *Sistema de Duelo*\n\n"
        "• Taxa: 25 TC por jogador\n"
        "• Sem premiação\n"
        "• Apenas mesmo servidor\n\n"
        "Escolha uma opção:",
        parse_mode="Markdown",
        reply_markup=None
    )


async def duel_create(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["duel_step"] = "MIN_LEVEL"
    await update.callback_query.edit_message_text(
        "Informe o *nível mínimo* do desafio:",
        parse_mode="Markdown"
    )


async def duel_receive_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data.get("duel_step")
    if not step:
        return

    try:
        value = int(update.message.text.strip())
    except:
        await update.message.reply_text("Digite apenas números.")
        return

    if step == "MIN_LEVEL":
        context.user_data["min_level"] = value
        context.user_data["duel_step"] = "MAX_LEVEL"
        await update.message.reply_text("Informe o *nível máximo*:")
        return

    if step == "MAX_LEVEL":
        context.user_data["max_level"] = value

        chars = get_characters(update.effective_user.id)
        if not chars:
            await update.message.reply_text("Você não tem personagem cadastrado.")
            return

        # Primeiro personagem como padrão
        challenger = chars[0]

        # World será resolvido depois (já está no banco)
        create_duel(
            challenger=challenger,
            world=None,
            min_lvl=context.user_data["min_level"],
            max_lvl=context.user_data["max_level"]
        )

        await update.message.reply_text(
            "✅ Duelo criado!\n\n"
            "Jogadores elegíveis receberão notificação."
        )

        context.user_data.clear()


async def duel_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chars = get_characters(update.effective_user.id)
    if not chars:
        await update.callback_query.edit_message_text("Sem personagem cadastrado.")
        return

    # Usaremos o primeiro char
    char = chars[0]

    duels = get_open_duels(world=None, level=0)

    if not duels:
        await update.callback_query.edit_message_text("Nenhum duelo disponível.")
        return

    buttons = []
    for d in duels:
        duel_id, challenger, min_lvl, max_lvl = d
        buttons.append([
            InlineKeyboardButton(
                f"⚔️ {challenger} ({min_lvl}-{max_lvl})",
                callback_data=f"duel_accept_{duel_id}"
            )
        ])

    await update.callback_query.edit_message_text(
        "📥 *Duelos disponíveis:*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
