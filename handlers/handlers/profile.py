from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import get_connection
import requests
from bs4 import BeautifulSoup

# =========================
# TECLADO PROFILE
# =========================

def profile_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Vincular Char", callback_data="add_char")],
        [InlineKeyboardButton("⬅️ Voltar", callback_data="menu")]
    ])

# =========================
# MOSTRAR PERFIL
# =========================

async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        "SELECT char_name, server, level, vocation FROM characters WHERE telegram_id=?",
        (query.from_user.id,)
    )
    chars = c.fetchall()
    conn.close()

    if not chars:
        text = (
            "👤 *Seu Perfil*\n\n"
            "Nenhum personagem vinculado ainda.\n"
            "Clique abaixo para adicionar."
        )
    else:
        text = "👤 *Seus Personagens*\n\n"
        for char in chars:
            text += (
                f"• *{char[0]}*\n"
                f"  Servidor: {char[1]}\n"
                f"  Level: {char[2]}\n"
                f"  Vocação: {char[3]}\n\n"
            )

    await query.edit_message_text(
        text,
        reply_markup=profile_keyboard(),
        parse_mode="Markdown"
    )

# =========================
# RECEBER NOME DO CHAR
# =========================

async def receive_char_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    char_name = update.message.text.strip()
    telegram_id = update.message.from_user.id

    await update.message.reply_text("🔍 Buscando informações do personagem...")

    url = f"https://www.tibia.com/community/?name={char_name.replace(' ', '+')}"
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        await update.message.reply_text("❌ Erro ao consultar o Tibia.")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    if "Character does not exist" in soup.text:
        await update.message.reply_text("❌ Personagem não encontrado.")
        return

    data = soup.find_all("td", class_="LabelV")
    values = soup.find_all("td", class_="LabelV")  # fallback seguro

    rows = soup.find_all("tr")

    server = level = vocation = None

    for row in rows:
        cols = row.find_all("td")
        if len(cols) != 2:
            continue

        label = cols[0].text.strip()
        value = cols[1].text.strip()

        if label == "World:":
            server = value
        elif label == "Level:":
            level = int(value)
        elif label == "Vocation:":
            vocation = value

    if not server or not level or not vocation:
        await update.message.reply_text("❌ Não foi possível ler os dados do personagem.")
        return

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        """
        INSERT INTO characters (telegram_id, char_name, server, level, vocation)
        VALUES (?, ?, ?, ?, ?)
        """,
        (telegram_id, char_name, server, level, vocation)
    )

    conn.commit()
    conn.close()

    await update.message.reply_text(
        f"✅ Personagem *{char_name}* vinculado com sucesso!\n\n"
        f"Servidor: {server}\n"
        f"Level: {level}\n"
        f"Vocação: {vocation}",
        parse_mode="Markdown"
    )
