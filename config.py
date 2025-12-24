# ==============================
# CONFIGURAÇÕES DO BOT
# ==============================
BOT_TOKEN = "8465541862:AAF01AdPI_CqTy5yBTMmYpffxr6AuI41yT4"
TC_RECEIVER = "cesar eto"
PREMIUM_PRICE = 25
DAILY_LIMIT = 1


import os

# Criar pasta de dados caso não exista
DB_FOLDER = "./data"
os.makedirs(DB_FOLDER, exist_ok=True)

# Caminho do banco de dados
DB_FILE = os.path.join(DB_FOLDER, "redmask_tibia.db")



