from services.limits import check_limit
from services.logic import avoid
from bot.keyboards import back

async def run(q):
    if not check_limit(q.from_user.id, "avoid"):
        await q.edit_message_text("⚠️ Limite diário atingido.", reply_markup=back())
        return
    await q.edit_message_text(avoid(), reply_markup=back())
