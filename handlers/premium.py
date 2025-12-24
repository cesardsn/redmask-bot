from bot.keyboards import back
from config import PREMIUM_PRICE, TC_RECEIVER

async def run(q):
    await q.edit_message_text(
        f"🪙 *Premium RedMask*\n\n"
        f"Uso ilimitado diário.\n"
        f"Valor: {PREMIUM_PRICE} TC\n\n"
        f"Enviar para:\n*{TC_RECEIVER}*",
        parse_mode="Markdown",
        reply_markup=back()
    )
