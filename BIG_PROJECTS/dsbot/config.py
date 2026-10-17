import os

# Google Gemini API Key
# Рекомендуется установить через переменную окружения: export GEMINI_API_KEY="ВАШ_КЛЮЧ"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")

# Discord Bot Token
# Рекомендуется установить через переменную окружения: export TOKEN="ВАШ_ТОКЕН"
# Примечание: для реального использования ОБЯЗАТЕЛЬНО используйте переменные окружения для токена!
TOKEN = os.getenv("TOKEN", "YOUR_DISCORD_TOKEN_HERE")

# Префикс команд для бота
PREFIX = "^" # Вы можете изменить этот префикс на любой другой

# ID роли модератора для кога Logs (замените на актуальный ID)
MODERATOR_ROLE_ID = 1491498905571954910

# ID канала для отправки отчетов модераторам в коге Moderation (замените на актуальный ID)
LOG_CHANNEL_ID = 1508187350226960474
