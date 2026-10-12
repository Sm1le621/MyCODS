import discord
from discord.ext import commands
from datetime import datetime
from discord.utils import format_dt, utcnow
import platform

class Info(commands.Cog):
    """
    Ког для информационных команд, таких как информация о сервере.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="server", help="Показывает информацию о текущем сервере.")
    @commands.guild_only()
    async def server_info(self, ctx: commands.Context) -> None:
        """
        Выводит стильный Embed с информацией о сервере.
        """
        guild = ctx.guild
        if not guild:
            await ctx.send("Эту команду можно использовать только на сервере.", ephemeral=True)
            return

        # Получаем количество участников онлайн
        online_members = sum(1 for member in guild.members if member.status != discord.Status.offline)

        embed = discord.Embed(
            title=f"Информация о сервере: {guild.name}",
            color=discord.Color.blue(),
            timestamp=utcnow()
        )
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        if guild.owner:
            embed.add_field(name="Владелец", value=guild.owner.mention, inline=True)
        
        embed.add_field(name="ID сервера", value=guild.id, inline=True)
        embed.add_field(name="Создан", value=format_dt(guild.created_at, "F"), inline=False)
        embed.add_field(name="Участники", value=f"Всего: {guild.member_count}\nОнлайн: {online_members}", inline=True)
        embed.add_field(name="Каналы", value=f"Текстовых: {len(guild.text_channels)}\nГолосовых: {len(guild.voice_channels)}", inline=True)
        
        boost_level = guild.premium_tier
        boost_count = guild.premium_subscription_count
        embed.add_field(name="Уровень буста", value=f"Уровень {boost_level} ({boost_count} бустов)", inline=True)

        # Если есть описание сервера
        if guild.description:
            embed.add_field(name="Описание", value=guild.description, inline=False)

        # Выводим количество ролей
        embed.add_field(name="Роли", value=len(guild.roles), inline=True)
        
        # Добавляем изображение баннера, если есть
        if guild.banner:
            embed.set_image(url=guild.banner.url)

        embed.set_footer(text=f"Запрошено: {ctx.author.display_name}")
        await ctx.send(embed=embed)

    @server_info.error
    async def server_info_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("Эту команду можно использовать только на сервере.", ephemeral=True)
        else:
            await ctx.send(f"Произошла ошибка при получении информации о сервере: {error}", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    """
    Функция setup для загрузки кога.
    """
    await bot.add_cog(Info(bot))
