from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu():
    keyboard = [
        [InlineKeyboardButton("👤 Meu Perfil", callback_data="profile")],
        [InlineKeyboardButton("🏰 Guild / Claimed", callback_data="guild")],
        [InlineKeyboardButton("⚔️ Guild War", callback_data="war")],
        [InlineKeyboardButton("🤺 Duelos", callback_data="duel")],
        [InlineKeyboardButton("🎯 Pistoleiros", callback_data="bounty")],
        [InlineKeyboardButton("⭐ Premium & Vantagens", callback_data="premium")],
    ]

    return InlineKeyboardMarkup(keyboard)
