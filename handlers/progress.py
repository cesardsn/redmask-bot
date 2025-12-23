from services.limits import check_limit
from services.logic import progress
from bot.keyboards import back

async def run(q):
    if not check_limit(q.from_user.id, "progress"):
        await q.edit_message_text("⚠️ Limite diário atingido.", reply_markup=back())
        return
    await q.edit_message_text(progress(), reply_markup=back())
