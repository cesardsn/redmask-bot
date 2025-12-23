from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🧠 Análise do Char", callback_data="analysis")],
        [InlineKeyboardButton("📈 Progresso Ideal", callback_data="progress")],
        [InlineKeyboardButton("🧭 Rotina Diária", callback_data="routine")],
        [InlineKeyboardButton("🧩 Quests Relevantes", callback_data="quests")],
        [InlineKeyboardButton("⚠️ Evitar Agora", callback_data="avoid")],
        [InlineKeyboardButton("🏰 Eventos Ativos", callback_data="events")],
        [InlineKeyboardButton("👑 Patrocinadores", callback_data="sponsor")],
        [InlineKeyboardButton("🪙 Premium", callback_data="premium")]
    ])

def back():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Menu", callback_data="menu")]
    ])

def sponsor_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 Quero Patrocinar", callback_data="sponsor_pay")],
        [InlineKeyboardButton("⬅️ Menu", callback_data="menu")]
    ])
