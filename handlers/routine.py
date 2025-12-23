from services.limits import check_limit
from services.logic import routine
from bot.keyboards import back

async def run(q):
    if not check_limit(q.from_user.id, "routine"):
        await q.edit_message_text("⚠️ Limite diário atingido.", reply_markup=back())
        return
    text = "🧭 *Rotina Ideal Hoje*\n\n"
    for step in routine():
        text += f"• {step}\n"
    await q.edit_message_text(text, parse_mode="Markdown", reply_markup=back())
