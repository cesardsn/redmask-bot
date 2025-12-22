from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def duel_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⚔️ Criar duelo", callback_data="duel_create")],
        [InlineKeyboardButton("📥 Duelo disponível", callback_data="duel_list")],
        [InlineKeyboardButton("⬅️ Voltar", callback_data="menu")]
    ])
