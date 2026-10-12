import discord
from discord.ext import commands
import google.genai as genai # Используем новую рекомендованную библиотеку google.genai
import os
from collections import deque
import re

from BIG_PROJECTS.dsbot.config import GEMINI_API_KEY

# Проверяем наличие ключа API Gemini
if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
    print("ПРЕДУПРЕЖДЕНИЕ: GEMINI_API_KEY не установлен в dsbot/config.py или через переменную окружения.")
    print("ИИ-чат может не работать. Пожалуйста, укажите ваш ключ Google Gemini API.")
else:
    # Конфигурируем Google Generative AI
    genai.configure(api_key=GEMINI_API_KEY) # configure() в genai это set_api_key
    # Для genai 0.8.0+, genai.configure(api_key=...) работает так же, как set_api_key.
    # Если возникают ошибки, возможно, потребуется установить старую версию или использовать genai.set_api_key().


# Инициализируем модель генерации
MODEL_NAME = "gemini-pro" # Используем gemini-pro, так как gemini-1.5-flash может быть недоступен или требовать другого доступа
GENERATION_CONFIG = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}
SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]


class AIChat(commands.Cog):
    """
    Интеграция ИИ-чата с использованием Google Gemini.
    Бот отвечает на команду !ai и упоминания, сохраняя контекст диалога.
    """

    def __init__(self, bot):
        self.bot = bot
        self._chat_sessions = {}  # Словарь для хранения активных чат-сессий по ID пользователя
        if GEMINI_API_KEY and GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE":
            self.model = genai.GenerativeModel( # Используем GenerativeModel из новой библиотеки
                model_name=MODEL_NAME,
                generation_config=GENERATION_CONFIG,
                safety_settings=SAFETY_SETTINGS,
            )
        else:
            self.model = None
            print("ИИ-чат деактивирован, так как отсутствует GEMINI_API_KEY.")


    def _get_chat_history_deque(self, user_id):
        """
        Получает или создает очередь сообщений для пользователя,
        сохраняя последние 7 сообщений для контекста.
        """
        if user_id not in self._chat_sessions:
            # Инициализируем новую сессию с историей из 7 отдельных сообщений
            # (например, 3 пары "пользователь-модель" + 1 сообщение пользователя)
            self._chat_sessions[user_id] = deque(maxlen=7)
        return self._chat_sessions[user_id]

    async def _generate_response(self, user_id, message_text: str):
        """
        Генерирует ответ от ИИ, используя контекст диалога.
        """
        if not self.model:
            return "ИИ-чат сейчас недоступен из-за отсутствия ключа API."

        chat_history_deque = self._get_chat_history_deque(user_id)

        # Конвертируем deque в список для вызова API
        # История, передаваемая в start_chat(), включает ВСЕ предыдущие реплики
        history_for_api = list(chat_history_deque)

        try:
            chat = self.model.start_chat(history=history_for_api)
            response = await chat.send_message(message_text)

            # Добавляем сообщение пользователя и ответ модели в локальный deque для будущего контекста
            chat_history_deque.append({"role": "user", "parts": [message_text]})
            if response.text: # Убедимся, что ответ не пуст
                chat_history_deque.append({"role": "model", "parts": [response.text]})
            
            return response.text
        except genai.BlockedPromptException as e: # Используем исключение из новой библиотеки
            print(f"Prompt blocked: {e}")
            return "Извините, ваш запрос был заблокирован из-за правил безопасности."
        except Exception as e:
            print(f"Ошибка при обращении к Gemini API: {e}")
            return "Извините, произошла ошибка при получении ответа от ИИ. Попробуйте еще раз позже."

    @commands.command(name="ai", help="Пообщаться с ИИ Google Gemini.")
    async def ai_command(self, ctx: commands.Context, *, message: str):
        """
        Обрабатывает команду !ai для взаимодействия с ИИ.
        """
        user_id = ctx.author.id
        async with ctx.typing():
            response_text = await self._generate_response(user_id, message)
            await ctx.send(response_text)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
        Автоматически обрабатывает сообщения, где упомянут бот.
        Игнорирует сообщения от самого бота или если сообщение является командой.
        """
        # Игнорируем сообщения от самого бота или если это команда
        if message.author.bot or message.content.startswith(self.bot.command_prefix):
            return

        # Проверяем, упомянут ли бот
        if self.bot.user and self.bot.user.mentioned_in(message):
            # Удаляем упоминание бота из текста сообщения
            # Регулярное выражение для удаления упоминаний бота (например, <@!123456789012345678>)
            pattern = re.compile(r"<@!?" + str(self.bot.user.id) + r">")
            cleaned_message = pattern.sub("", message.content).strip()

            if not cleaned_message:
                # Если сообщение состоит только из упоминания, игнорируем его
                return

            user_id = message.author.id
            async with message.channel.typing():
                response_text = await self._generate_response(user_id, cleaned_message)
                await message.channel.send(response_text)


async def setup(bot):
    """Регистрирует ког AIChat."""
    await bot.add_cog(AIChat(bot))
