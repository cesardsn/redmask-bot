# main.py
import os
import sys
from telegram.ext import ApplicationBuilder
from bot.menu import menu_router

print("🤖 Iniciando RedMask Tibia...")

# =====================================================
# TOKEN
# =====================================================
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN or ":" not in TOKEN:
    print("❌ ERRO CRÍTICO: BOT_TOKEN não encontrado ou inválido")
    print("👉 Configure a variável de ambiente BOT_TOKEN no Railway")
    sys.exit(1)

# =====================================================
# APP
# =====================================================
app = ApplicationBuilder().token(TOKEN).build()

# registra todos os handlers/menus
app.include_router(menu_router)

# =====================================================
# START
# =====================================================
print("✅ Bot inicializado com sucesso")
print("🚀 Iniciando polling...")

app.run_polling(
    allowed_updates=["message", "callback_query"]
)
