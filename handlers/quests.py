from services.limits import check_limit
from services.logic import quests
from bot.keyboards import back

async def run(q):
    if not check_limit(q.from_user.id, "quests"):
        await q.edit_message_text("⚠️ Limite diário atingido.", reply_markup=back())
        return
    text = "🧩 *Quests Relevantes*\n\n"
    for qst, reward in quests():
        text += f"*{qst}* → {reward}\n"
    await q.edit_message_text(text, parse_mode="Markdown", reply_markup=back())
