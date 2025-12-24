# main.py
import os
import sys
from telegram.ext import ApplicationBuilder
from bot.menu import menu_router

print("🤖 Iniciando RedMask Tibia...")

# =====================================================
# TOKEN (env > config.py)
# =====================================================
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    try:
        from config import BOT_TOKEN as CONFIG_TOKEN
        TOKEN = CONFIG_TOKEN
        print("⚠️ BOT_TOKEN carregado do config.py")
    except Exception:
        TOKEN = None

if not TOKEN or ":" not in TOKEN:
    print("❌ ERRO CRÍTICO: BOT_TOKEN não encontrado")
    print("👉 Defina BOT_TOKEN no Railway OU em config.py")
    sys.exit(1)

# =====================================================
# APP
# =====================================================
app = ApplicationBuilder().token(TOKEN).build()

# 👉 REGISTRA OS HANDLERS CORRETAMENTE
menu_router(app)

print("✅ Bot inicializado com sucesso")
print("🚀 Iniciando polling...")

app.run_polling(
    allowed_updates=["message", "callback_query"]
)
