import os

# Criar pasta de dados caso não exista
DB_FOLDER = "./data"
os.makedirs(DB_FOLDER, exist_ok=True)

# Caminho do banco de dados
DB_FILE = os.path.join(DB_FOLDER, "redmask_tibia.db")

# Limite diário de uso para Free users
DAILY_LIMIT = 1
