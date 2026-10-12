import discord
from discord.ext import commands
from discord import app_commands
from typing import List, Dict, Any
from BIG_PROJECTS.dsbot.config import LOG_CHANNEL_ID

class ReportModal(discord.ui.Modal, title="Подача жалобы"):
    """
    Модальное окно для сбора информации о жалобе.
    """
    target_user_name = discord.ui.TextInput(
        label="Ник нарушителя (или его ID)",
        placeholder="Введите ник или ID пользователя...",
        required=True,
        style=discord.TextStyle.short
    )

    reason = discord.ui.TextInput(
        label="Причина жалобы",
        placeholder="Опишите нарушение подробно...",
        required=True,
        style=discord.TextStyle.long
    )

    def __init__(self, bot: commands.Bot, reports_storage: List[Dict[str, Any]]):
        super().__init__()
        self.bot = bot
        self.reports_storage = reports_storage

    async def on_submit(self, interaction: discord.Interaction) -> None:
        """
        Обрабатывает отправку модального окна.
        """
        report_data = {
            "reporter_id": interaction.user.id,
            "reporter_name": interaction.user.display_name,
            "target_user_name": self.target_user_name.value,
            "reason": self.reason.value,
            "guild_id": interaction.guild_id,
            "timestamp": discord.utils.utcnow().isoformat()
        }
        self.reports_storage.append(report_data)

        embed = discord.Embed(
            title="✅ Жалоба принята!",
            description="Спасибо за вашу бдительность. Модераторы рассмотрят вашу жалобу.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True) # ephemeral=True делает сообщение видимым только отправителю

        # Отправка отчета в скрытый канал для модераторов
        if LOG_CHANNEL_ID:
            log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
            if log_channel and isinstance(log_channel, discord.TextChannel):
                report_embed = discord.Embed(
                    title="🚨 Новый отчет о нарушении",
                    color=discord.Color.red()
                )
                report_embed.add_field(name="Сообщил", value=f"{interaction.user.mention} (`{interaction.user.id}`)", inline=False)
                report_embed.add_field(name="Нарушитель (указано)", value=self.target_user_name.value, inline=False)
                report_embed.add_field(name="Причина", value=self.reason.value, inline=False)
                report_embed.add_field(name="Сервер", value=interaction.guild.name, inline=False)
                report_embed.set_footer(text=f"Время: {discord.utils.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
                await log_channel.send(embed=report_embed)
            else:
                print(f"Ошибка: Не удалось найти лог-канал с ID {LOG_CHANNEL_ID}. Отчет не отправлен модераторам.")
        else:
            print("LOG_CHANNEL_ID не настроен. Отчет не отправлен модераторам.")


class ReportView(discord.ui.View):
    """
    View с кнопкой для вызова модального окна жалоб.
    """
    def __init__(self, bot: commands.Bot, reports_storage: List[Dict[str, Any]]):
        super().__init__(timeout=None) # timeout=None делает View постоянным
        self.bot = bot
        self.reports_storage = reports_storage

    @discord.ui.button(label="Подать жалобу", style=discord.ButtonStyle.red, custom_id="report_button")
    async def report_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        """
        Callback для кнопки "Подать жалобу". Открывает модальное окно.
        """
        await interaction.response.send_modal(ReportModal(self.bot, self.reports_storage))


class Moderation(commands.Cog):
    """
    Ког для команд модерации и системы жалоб.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.reports: List[Dict[str, Any]] = [] # Временное хранилище жалоб

    @commands.command(name="report_panel", help="Отправляет панель для подачи жалоб.")
    @commands.has_permissions(manage_messages=True) # Только пользователи с правами на управление сообщениями могут вызвать
    async def report_panel(self, ctx: commands.Context) -> None:
        """
        Отправляет Embed-сообщение с кнопкой "Подать жалобу" в текущий канал.
        """
        embed = discord.Embed(
            title="Система жалоб",
            description="Если вы стали свидетелем нарушения правил, пожалуйста, нажмите кнопку ниже, чтобы подать жалобу. Ваша информация поможет модераторам поддерживать порядок на сервере.",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Все жалобы анонимны для нарушителя, но видны модераторам.")
        await ctx.send(embed=embed, view=ReportView(self.bot, self.reports))

    @report_panel.error
    async def report_panel_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("У вас нет прав для отправки панели жалоб.", ephemeral=True)
        else:
            await ctx.send(f"Произошла ошибка при отправке панели жалоб: {error}", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    """
    Функция setup для загрузки кога.
    """
    await bot.add_cog(Moderation(bot))
