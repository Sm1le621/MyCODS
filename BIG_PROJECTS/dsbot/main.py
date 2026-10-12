import os
import discord
from discord.ext import commands
from BIG_PROJECTS.dsbot.config import TOKEN, PREFIX

class MyBot(commands.Bot):
    """
    Основной класс Discord-бота.
    Отвечает за инициализацию, загрузку когов и управление жизненным циклом бота.
    """
    def __init__(self):
        # Определение необходимых интентов
        intents = discord.Intents.default()
        intents.members = True          # Для отслеживания участников (кики, баны, изменения ролей, ников)
        intents.guilds = True           # Для получения информации о серверах и аудитных логов
        intents.voice_states = True     # Для голосовых логов
        intents.message_content = True  # Для обработки содержимого сообщений (требуется для команд)

        super().__init__(command_prefix=PREFIX, intents=intents)

    async def setup_hook(self) -> None:
        """
        Метод вызывается перед подключением к Discord.
        Здесь происходит загрузка всех когов.
        """
        cogs_dir = os.path.join(os.path.dirname(__file__), 'cogs')
        for filename in os.listdir(cogs_dir):
            if filename.endswith(".py"):
                try:
                    await self.load_extension(f"cogs.{filename[:-3]}")
                    print(f"Ког {filename[:-3]} успешно загружен.")
                except Exception as e:
                    print(f"Не удалось загрузить ког {filename[:-3]}: {e}")

    async def on_ready(self) -> None:
        """
        Событие, которое вызывается при успешном подключении бота к Discord.
        """
        print(f"Бот {self.user} подключен к Discord!")
        print(f"ID: {self.user.id}")
        print(f"Префикс команд: {PREFIX}")

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        """
        Глобальный обработчик ошибок команд.
        """
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("У вас недостаточно прав для выполнения этой команды.", ephemeral=True)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Отсутствует необходимый аргумент: `{error.param}`. Пожалуйста, проверьте синтаксис команды.", ephemeral=True)
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"Неверный тип аргумента: {error}. Пожалуйста, убедитесь, что вы ввели корректные данные.", ephemeral=True)
        elif isinstance(error, commands.CommandNotFound):
            pass # Игнорируем ошибки "команда не найдена"
        else:
            print(f"Произошла ошибка в команде {ctx.command}: {error}")
            await ctx.send(f"Произошла неизвестная ошибка: `{error}`", ephemeral=True)


def run_bot() -> None:
    """
    Запускает бота.
    """
    if TOKEN == "ВАШ_ТОКЕН_БОТА":
        print("ВНИМАНИЕ: Пожалуйста, замените 'ВАШ_ТОКЕН_БОТА' в dsbot/config.py или установите переменную окружения DISCORD_BOT_TOKEN.")
        return

    bot = MyBot()
    bot.run(TOKEN)

if __name__ == "__main__":
    run_bot()
