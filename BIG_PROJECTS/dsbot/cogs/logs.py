import discord
from discord.ext import commands
from discord.utils import format_dt, utcnow
from typing import List, Dict, Any, Optional
from BIG_PROJECTS.dsbot.config import MODERATOR_ROLE_ID

class PaginatorView(discord.ui.View):
    """
    View для пагинации Embed-сообщений.
    """
    def __init__(self, embeds: List[discord.Embed], author: discord.Member):
        super().__init__(timeout=180) # Таймаут 3 минуты
        self.embeds = embeds
        self.current_page = 0
        self.author = author
        self.update_buttons()

    def update_buttons(self) -> None:
        self.children[0].disabled = (self.current_page == 0) # "Предыдущая"
        self.children[1].disabled = (self.current_page == len(self.embeds) - 1) # "Следующая"

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True
        if self.message:
            await self.message.edit(view=self)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.author:
            await interaction.response.send_message("Вы не можете управлять этим меню.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="⬅️ Предыдущая", style=discord.ButtonStyle.blurple)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self.current_page -= 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)

    @discord.ui.button(label="Следующая ➡️", style=discord.ButtonStyle.blurple)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        self.current_page += 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)


class Logs(commands.Cog):
    """
    Ког для отслеживания событий на сервере и хранения логов.
    Логи сохраняются в памяти.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logs: List[Dict[str, Any]] = []

    def _add_log(self, event_type: str, guild: discord.Guild, description: str, moderator: Optional[discord.User] = None) -> None:
        """
        Вспомогательная функция для добавления записи в лог.
        """
        log_entry = {
            "timestamp": utcnow().isoformat(),
            "event_type": event_type,
            "guild_id": guild.id,
            "guild_name": guild.name,
            "description": description,
            "moderator_id": moderator.id if moderator else None,
            "moderator_name": moderator.display_name if moderator else None,
        }
        self.logs.append(log_entry)
        # Ограничиваем количество логов, чтобы не переполнять память (например, до 1000 записей)
        if len(self.logs) > 1000:
            self.logs.pop(0)

    async def _get_audit_log_entry(self, guild: discord.Guild, action: discord.AuditLogAction, target_id: int) -> Optional[discord.AuditLogEntry]:
        """
        Вспомогательная функция для поиска соответствующей записи в аудит-логах.
        """
        async for entry in guild.audit_logs(limit=5, action=action):
            if entry.target and entry.target.id == target_id:
                return entry
        return None

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: discord.User) -> None:
        """Отслеживает событие бана участника."""
        entry = await self._get_audit_log_entry(guild, discord.AuditLogAction.ban, user.id)
        moderator_info = f"Администратор: {entry.user.display_name} ({entry.user.id})" if entry and entry.user else "Неизвестно"
        reason_info = f"Причина: {entry.reason}" if entry and entry.reason else "Причина не указана"
        self._add_log(
            "MEMBER_BAN",
            guild,
            f"Пользователь {user.display_name} ({user.id}) был забанен. {moderator_info}. {reason_info}.",
            entry.user if entry else None
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        """
        Отслеживает событие ухода/кика участника.
        Пытаемся определить, был ли это кик через аудит-логи.
        """
        await self.bot.wait_until_ready() # Убедиться, что аудит-логи доступны

        entry = await self._get_audit_log_entry(member.guild, discord.AuditLogAction.kick, member.id)

        if entry:
            moderator_info = f"Администратор: {entry.user.display_name} ({entry.user.id})" if entry.user else "Неизвестно"
            reason_info = f"Причина: {entry.reason}" if entry.reason else "Причина не указана"
            self._add_log(
                "MEMBER_KICK",
                member.guild,
                f"Пользователь {member.display_name} ({member.id}) был кикнут. {moderator_info}. {reason_info}.",
                entry.user if entry else None
            )
        else:
            self._add_log(
                "MEMBER_LEAVE",
                member.guild,
                f"Пользователь {member.display_name} ({member.id}) покинул сервер.",
            )

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member) -> None:
        """
        Отслеживает смену никнейма и изменение ролей.
        """
        # Смена никнейма
        if before.nick != after.nick:
            entry = await self._get_audit_log_entry(after.guild, discord.AuditLogAction.member_update, after.id)
            moderator_info = f" (Кем: {entry.user.display_name})" if entry and entry.user else ""
            self._add_log(
                "NICKNAME_CHANGE",
                after.guild,
                f"Никнейм пользователя {after.display_name} ({after.id}) изменен с '{before.nick or before.name}' на '{after.nick or after.name}'.{moderator_info}",
                entry.user if entry else None
            )

        # Изменение ролей
        if before.roles != after.roles:
            added_roles = [role for role in after.roles if role not in before.roles]
            removed_roles = [role for role in before.roles if role not in after.roles]

            entry = await self._get_audit_log_entry(after.guild, discord.AuditLogAction.member_role_update, after.id)
            moderator_info = f" (Кем: {entry.user.display_name})" if entry and entry.user else ""

            for role in added_roles:
                self._add_log(
                    "ROLE_ADD",
                    after.guild,
                    f"Роль '{role.name}' ({role.id}) была добавлена пользователю {after.display_name} ({after.id}).{moderator_info}",
                    entry.user if entry else None
                )
            for role in removed_roles:
                self._add_log(
                    "ROLE_REMOVE",
                    after.guild,
                    f"Роль '{role.name}' ({role.id}) была удалена у пользователя {after.display_name} ({after.id}).{moderator_info}",
                    entry.user if entry else None
                )

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message) -> None:
        """Отслеживает удаление сообщения."""
        if message.guild: # Убедимся, что это сообщение в гильдии, а не в ЛС
            entry = await self._get_audit_log_entry(message.guild, discord.AuditLogAction.message_delete, message.author.id)
            moderator_info = f" (Удалил: {entry.user.display_name})" if entry and entry.user else ""
            self._add_log(
                "MESSAGE_DELETE",
                message.guild,
                f"Сообщение от {message.author.display_name} ({message.author.id}) было удалено в канале {message.channel.name} (`{message.channel.id}`). "
                f"Содержимое: '{message.content[:100]}...' (или полностью, если короткое).{moderator_info}",
                entry.user if entry else None
            )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        """Отслеживает присоединение нового участника."""
        self._add_log(
            "MEMBER_JOIN",
            member.guild,
            f"Новый участник {member.display_name} ({member.id}) присоединился к серверу.",
        )

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState) -> None:
        """
        Отслеживает голосовые события: отключение микрофона/звука, кик из голосового канала.
        """
        if not member.guild:
            return

        # Кик из голосового канала
        if before.channel and not after.channel:
            entry = await self._get_audit_log_entry(member.guild, discord.AuditLogAction.member_disconnect, member.id)
            moderator_info = f" (Кем: {entry.user.display_name})" if entry and entry.user else ""
            self._add_log(
                "VOICE_DISCONNECT",
                member.guild,
                f"Пользователь {member.display_name} ({member.id}) был отключен от голосового канала '{before.channel.name}'.{moderator_info}",
                entry.user if entry else None
            )
        # Отключение/включение звука (mute)
        if before.self_mute != after.self_mute:
            mute_state = "выключил" if after.self_mute else "включил"
            self._add_log(
                "VOICE_SELF_MUTE",
                member.guild,
                f"Пользователь {member.display_name} ({member.id}) {mute_state} себе микрофон."
            )
        elif before.mute != after.mute: # Отключение звука администратором
            entry = await self._get_audit_log_entry(member.guild, discord.AuditLogAction.member_update, member.id)
            moderator_info = f" (Кем: {entry.user.display_name})" if entry and entry.user else ""
            mute_state = "выключил" if after.mute else "включил"
            self._add_log(
                "VOICE_SERVER_MUTE",
                member.guild,
                f"Администратор {mute_state} микрофон пользователю {member.display_name} ({member.id}).{moderator_info}",
                entry.user if entry else None
            )

        # Отключение/включение динамиков (deafen)
        if before.self_deaf != after.self_deaf:
            deaf_state = "выключил" if after.self_deaf else "включил"
            self._add_log(
                "VOICE_SELF_DEAF",
                member.guild,
                f"Пользователь {member.display_name} ({member.id}) {deaf_state} себе динамики."
            )
        elif before.deaf != after.deaf: # Отключение динамиков администратором
            entry = await self._get_audit_log_entry(member.guild, discord.AuditLogAction.member_update, member.id)
            moderator_info = f" (Кем: {entry.user.display_name})" if entry and entry.user else ""
            deaf_state = "выключил" if after.deaf else "включил"
            self._add_log(
                "VOICE_SERVER_DEAF",
                member.guild,
                f"Администратор {deaf_state} динамики пользователю {member.display_name} ({member.id}).{moderator_info}",
                entry.user if entry else None
            )

    @commands.command(name="show_logs", help="Показывает накопленные логи сервера (только для модераторов).")
    @commands.has_any_role(MODERATOR_ROLE_ID) # Доступно только модераторам по ID роли
    @commands.guild_only() # Команда должна быть вызвана на сервере
    async def show_logs(self, ctx: commands.Context) -> None:
        """
        Выводит накопленные логи в Embed-сообщении с пагинацией.
        """
        if not self.logs:
            await ctx.send("Накопленных логов пока нет.", ephemeral=True)
            return

        # Фильтруем логи по текущему серверу
        guild_logs = [log for log in self.logs if log["guild_id"] == ctx.guild.id]
        if not guild_logs:
            await ctx.send("Накопленных логов для этого сервера пока нет.", ephemeral=True)
            return

        # Сортируем логи по времени, самые новые в начале
        guild_logs.sort(key=lambda x: x["timestamp"], reverse=True)

        embeds: List[discord.Embed] = []
        logs_per_page = 5 # Количество логов на страницу

        for i in range(0, len(guild_logs), logs_per_page):
            chunk = guild_logs[i:i + logs_per_page]
            embed = discord.Embed(
                title=f"Логи сервера: {ctx.guild.name}",
                description="Последние события на сервере:",
                color=discord.Color.dark_grey()
            )
            embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)

            for log in chunk:
                timestamp_obj = discord.utils.parse_time(log["timestamp"]) # Парсим ISO-формат
                embed.add_field(
                    name=f"{log['event_type']} - {format_dt(timestamp_obj, 'R')}", # 'R' для относительного времени
                    value=log["description"],
                    inline=False
                )
            embed.set_footer(text=f"Страница {len(embeds) + 1}/{((len(guild_logs) - 1) // logs_per_page) + 1}")
            embeds.append(embed)

        if len(embeds) == 1:
            await ctx.send(embed=embeds[0])
        else:
            view = PaginatorView(embeds, ctx.author)
            message = await ctx.send(embed=embeds[0], view=view)
            view.message = message # Сохраняем сообщение для отключения кнопок после таймаута

    @show_logs.error
    async def show_logs_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send("У вас нет прав для просмотра логов.", ephemeral=True)
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send("Эту команду можно использовать только на сервере.", ephemeral=True)
        else:
            await ctx.send(f"Произошла ошибка при получении логов: {error}", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    """
    Функция setup для загрузки кога.
    """
    await bot.add_cog(Logs(bot))
