import discord
from discord.ext import commands
import random
import asyncio # Импортируем asyncio для asyncio.sleep
from typing import List

class Games(commands.Cog):
    """
    Ког для мини-игр.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.emojis = ["🍎", "🍋", "💎", "7️⃣", "🍒", "🍇", "🍊"] # Эмодзи для слотов
        self.win_conditions = {
            "7️⃣": 50,  # Самый большой выигрыш
            "💎": 20,
            "🍎": 10,
            "🍋": 5,
            "🍒": 3,
            "🍇": 2,
            "🍊": 1,
        }

    @commands.command(name="slots", help="Сыграть в слот-машину.")
    @commands.cooldown(1, 10, commands.BucketType.user) # 1 использование каждые 10 секунд на пользователя
    async def slots(self, ctx: commands.Context) -> None:
        """
        Мини-игра "Слот-машина".
        Визуально имитирует вращение барабанов и подводит итог.
        """
        results: List[str] = random.choices(self.emojis, k=3) # Выбираем 3 случайных смайлика

        # Имитация вращения (необязательно, но добавляет интерактивности)
        spinning_emojis = ["🌀", "💫", "✨"]
        spinning_message = await ctx.send(f"🎰 Вращаем барабаны... {random.choice(spinning_emojis)}{random.choice(spinning_emojis)}{random.choice(spinning_emojis)}")

        await asyncio.sleep(2) # Задержка для "вращения"

        # Формирование визуального вывода слотов
        slot_display = f"```\n" \
                       f"| {results[0]} | {results[1]} | {results[2]} |\n" \
                       f"```"

        embed = discord.Embed(
            title="🎰 Слот-машина 🎰",
            color=discord.Color.gold()
        )
        embed.add_field(name="Результат:", value=slot_display, inline=False)

        # Проверка на выигрыш
        if results[0] == results[1] == results[2]:
            winnings = self.win_conditions.get(results[0], 0) * 10 # Увеличиваем выигрыш за 3 одинаковых
            embed.description = f"🎉 Поздравляем! Тройной выигрыш! Вы выиграли {winnings} очков!"
            embed.color = discord.Color.green()
        elif results[0] == results[1] or results[1] == results[2] or results[0] == results[2]:
            # Можно сделать более сложную логику, но для примера хватит
            # Если два одинаковых, то выигрыш меньше
            winning_emoji = ""
            if results[0] == results[1]: winning_emoji = results[0]
            elif results[1] == results[2]: winning_emoji = results[1]
            elif results[0] == results[2]: winning_emoji = results[0]
            
            winnings = self.win_conditions.get(winning_emoji, 0) * 3
            if winnings > 0:
                embed.description = f"🥳 Отличный результат! Два одинаковых символа! Вы выиграли {winnings} очков!"
                embed.color = discord.Color.light_grey()
            else:
                embed.description = "К сожалению, вы ничего не выиграли."
                embed.color = discord.Color.red()
        else:
            embed.description = "К сожалению, вы ничего не выиграли."
            embed.color = discord.Color.red()

        embed.set_footer(text=f"Сыграл: {ctx.author.display_name}")
        
        await spinning_message.edit(content=None, embed=embed) # Редактируем сообщение с вращением на результат

    @slots.error
    async def slots_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Эта команда на перезарядке. Попробуйте снова через {error.retry_after:.2f} секунд.", ephemeral=True)
        else:
            await ctx.send(f"Произошла ошибка в слот-машине: {error}", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    """
    Функция setup для загрузки кога.
    """
    await bot.add_cog(Games(bot))
