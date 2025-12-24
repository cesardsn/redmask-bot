from bot.keyboards import sponsor_menu, back
from services.payments import create_payment
from services.db import get_connection
from datetime import datetime

async def run(q):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT char_name, value FROM sponsors ORDER BY value DESC LIMIT 3")
    sponsors = c.fetchall()
    conn.close()
    
    text = "👑 *Patrocinadores do Dia*\n\n"
    if sponsors:
        for i, s in enumerate(sponsors, 1):
            text += f"{i}º *{s['char_name']}* — {s['value']} TC\n"
    else:
        text += "Nenhum nome domina hoje.\n"
    
    await q.edit_message_text(text, parse_mode="Markdown", reply_markup=sponsor_menu())

async def sponsor_pay(q, context):
    context.user_data["awaiting_payment"] = True
    await q.edit_message_text(
        "💎 *Patrocínio RedMask*\nEnvie qualquer valor de TC para: *cesar eto*\n"
        "Após pagar, clique '✅ Já paguei' e digite: NomeDoChar Valor",
        parse_mode="Markdown"
    )
