from services.limits import check_limit
from services.scraper import events
from bot.keyboards import back

async def run(q):
    if not check_limit(q.from_user.id, "events"):
        await q.edit_message_text("⚠️ Limite diário atingido.", reply_markup=back())
        return
    text = "🏰 *Eventos do Tibia*\n\n"
    for e in events():
        text += f"• {e}\n"
    await q.edit_message_text(text, parse_mode="Markdown", reply_markup=back())
