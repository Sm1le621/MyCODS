import discord
from discord.ext import commands
import random
from typing import Dict, List, Any, Optional

class Quotes(commands.Cog):
    """
    Ког для управления цитатами участников сервера.
    Цитаты сохраняются в памяти.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Словарь для хранения цитат: {guild_id: {user_id: [quote1, quote2, ...]}}
        self.quotes_storage: Dict[int, Dict[int, List[str]]] = {}

    def _get_quotes_for_user(self, guild_id: int, user_id: int) -> List[str]:
        """
        Вспомогательная функция для получения списка цитат пользователя.
        """
        if guild_id not in self.quotes_storage:
            self.quotes_storage[guild_id] = {}
        if user_id not in self.quotes_storage[guild_id]:
            self.quotes_storage[guild_id][user_id] = []
        return self.quotes_storage[guild_id][user_id]

    @commands.command(name="add_quote", help="Добавить цитату участника.")
    @commands.guild_only()
    async def add_quote(self, ctx: commands.Context, member: discord.Member, *, quote_text: str) -> None:
        """
        Сохраняет цитату указанного участника.
        """
        if not quote_text:
            await ctx.send("Пожалуйста, укажите текст цитаты.", ephemeral=True)
            return
        
        # Простая проверка на дубликаты
        quotes = self._get_quotes_for_user(ctx.guild.id, member.id)
        if quote_text in quotes:
            await ctx.send(f"Эта цитата уже существует для {member.mention}.", ephemeral=True)
            return

        quotes.append(quote_text)
        await ctx.send(f"Цитата от {member.mention} успешно добавлена!", ephemeral=True)

    @add_quote.error
    async def add_quote_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Использование: `!add_quote <@участник> <текст цитаты>`", ephemeral=True)
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Не удалось найти указанного участника. Пожалуйста, убедитесь, что вы правильно его упомянули.", ephemeral=True)
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send("Эту команду можно использовать только на сервере.", ephemeral=True)
        else:
            await ctx.send(f"Произошла ошибка при добавлении цитаты: {error}", ephemeral=True)


    @commands.command(name="quote", help="Вывести случайную цитату участника.")
    @commands.guild_only()
    async def get_quote(self, ctx: commands.Context, member: discord.Member) -> None:
        """
        Выводит случайную цитату указанного участника в виде красивой карточки.
        """
        quotes = self._get_quotes_for_user(ctx.guild.id, member.id)

        if not quotes:
            await ctx.send(f"У {member.mention} пока нет сохраненных цитат.", ephemeral=True)
            return

        chosen_quote = random.choice(quotes)

        embed = discord.Embed(
            description=f"«_{chosen_quote}_»", # Оформление курсивом и кавычками
            color=discord.Color.dark_teal()
        )
        embed.set_author(name=f"Цитата от {member.display_name}", icon_url=member.display_avatar.url)
        embed.set_footer(text=f"Запросил: {ctx.author.display_name}")

        await ctx.send(embed=embed)

    @get_quote.error
    async def get_quote_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Использование: `!quote <@участник>`", ephemeral=True)
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Не удалось найти указанного участника. Пожалуйста, убедитесь, что вы правильно его упомянули.", ephemeral=True)
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send("Эту команду можно использовать только на сервере.", ephemeral=True)
        else:
            await ctx.send(f"Произошла ошибка при получении цитаты: {error}", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    """
    Функция setup для загрузки кога.
    """
    await bot.add_cog(Quotes(bot))
