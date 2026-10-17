import discord
from discord.ext import commands
from discord.ui import Button, View
import random
import asyncio

# Размеры поля
BOARD_SIZE_X = 5
BOARD_SIZE_Y = 5
NUM_MINES = 3  # Количество мин на поле

# Эмодзи для кнопок
EMOJI_HIDDEN = "⬜"
EMOJI_MINE = "💣"
EMOJI_REVEALED_SAFE = "✔️" # Смайлик для пустых безопасных ячеек
EMOJI_LOSE = "💥" # Смайлик для проигрыша

class MinesweeperButton(Button):
    """
    Кнопка для ячейки поля Сапера.
    """
    def __init__(self, row: int, col: int, is_mine: bool, adjacent_mines: int):
        super().__init__(style=discord.ButtonStyle.secondary, label=EMOJI_HIDDEN, row=row)
        self.row = row
        self.col = col
        self.is_mine = is_mine
        self.adjacent_mines = adjacent_mines
        self.is_revealed = False

    async def callback(self, interaction: discord.Interaction):
        """
        Обрабатывает нажатие на кнопку.
        """
        view: MinesweeperView = self.view  # type: ignore
        
        if view.game_over or self.is_revealed:
            await interaction.response.defer()  # Игнорируем нажатия на раскрытые ячейки или после завершения игры
            return

        self.is_revealed = True

        if self.is_mine:
            # Игрок наткнулся на мину
            self.style = discord.ButtonStyle.danger
            self.label = EMOJI_MINE
            view.game_over = True
            
            # Раскрываем все мины при проигрыше
            for r in range(BOARD_SIZE_Y):
                for c in range(BOARD_SIZE_X):
                    btn = view.board_buttons[r][c]
                    if btn.is_mine:
                        btn.style = discord.ButtonStyle.danger
                        btn.label = EMOJI_MINE
                    elif not btn.is_revealed:
                        btn.style = discord.ButtonStyle.grey
                        btn.label = "\u200b" # Отображаем нераскрытые безопасные как пустые серые с использованием символа нулевой ширины

            embed = discord.Embed(
                title=f"{EMOJI_LOSE} БАХ! Вы подорвались на мине! {EMOJI_LOSE}",
                description=f"Пользователь {interaction.user.mention} проиграл в экстремальный Сапер!",
                color=discord.Color.red()
            )
            
            # Отключаем все кнопки и убеждаемся, что все метки кнопок явно установлены
            for r in range(BOARD_SIZE_Y):
                for c in range(BOARD_SIZE_X):
                    btn = view.board_buttons[r][c]
                    btn.disabled = True # Все кнопки становятся неактивными

                    if btn.is_mine:
                        btn.label = EMOJI_MINE # Метка для мины
                        btn.style = discord.ButtonStyle.danger
                    elif btn.is_revealed:
                        # Уже раскрытые безопасные ячейки сохраняют свою метку
                        btn.label = str(btn.adjacent_mines) if btn.adjacent_mines > 0 else EMOJI_REVEALED_SAFE
                        btn.style = discord.ButtonStyle.green
                    else:
                        # Нераскрытые безопасные ячейки, которые не были выбраны
                        btn.label = EMOJI_HIDDEN # Показываем как скрытые ячейки
                        btn.style = discord.ButtonStyle.secondary # Возвращаем к стандартному стилю

            await interaction.response.edit_message(embed=embed, view=view)

            # Попытка забанить пользователя
            if isinstance(interaction.user, discord.Member) and interaction.guild:
                try:
                    # delete_message_days=0 означает, что сообщения пользователя за последние 0 дней не будут удалены.
                    await interaction.user.ban(reason="Проигрыш в экстремальный Сапер", delete_message_days=0)
                    # Используем followup.send, так как interaction.response.edit_message уже был вызван
                    await interaction.followup.send(f"Пользователь {interaction.user.mention} был забанен! Урок усвоен.")
                except discord.Forbidden:
                    await interaction.followup.send(
                        f"Я не могу забанить пользователя {interaction.user.mention} из-за иерархии ролей! "
                        "Но он всё равно проиграл..."
                    )
                except Exception as e:
                    await interaction.followup.send(f"Произошла непредвиденная ошибка при попытке бана: {e}")
            

        else:
            # Игрок открыл безопасную ячейку
            self.style = discord.ButtonStyle.green
            self.label = str(self.adjacent_mines) if self.adjacent_mines > 0 else EMOJI_REVEALED_SAFE
            view.revealed_count += 1

            if view.revealed_count == view.total_safe_cells:
                # Победа!
                view.game_over = True
                embed = discord.Embed(
                    title="🎉 Поздравляем! Вы прошли экстремальный Сапер! 🎉",
                    description=f"Пользователь {interaction.user.mention} успешно разминировал поле!",
                    color=discord.Color.green()
                )
                
                # Отключаем все кнопки
                for item in view.children:
                    if isinstance(item, Button):
                        item.disabled = True

                await interaction.response.edit_message(embed=embed, view=view)
            else:
                await interaction.response.edit_message(view=view)


class MinesweeperView(View):
    """
    Представление для игры Сапер с кнопками.
    """
    def __init__(self):
        super().__init__(timeout=300)  # Таймаут 5 минут
        # board: 0-8 для количества мин, 9 для мины
        self.board = [[0 for _ in range(BOARD_SIZE_X)] for _ in range(BOARD_SIZE_Y)]
        self.board_buttons = [[None for _ in range(BOARD_SIZE_X)] for _ in range(BOARD_SIZE_Y)]
        self.game_over = False
        self.revealed_count = 0
        self.total_safe_cells = BOARD_SIZE_X * BOARD_SIZE_Y - NUM_MINES
        self._place_mines()
        self._calculate_adjacent_mines()
        self._add_buttons_to_view()
        self.message = None # Будет установлено после отправки сообщения

    def _place_mines(self):
        """Размещает мины на поле."""
        mine_positions = random.sample(range(BOARD_SIZE_X * BOARD_SIZE_Y), NUM_MINES)
        for pos in mine_positions:
            r = pos // BOARD_SIZE_X
            c = pos % BOARD_SIZE_X
            self.board[r][c] = 9  # 9 означает мину

    def _calculate_adjacent_mines(self):
        """Вычисляет количество мин в соседних ячейках."""
        for r in range(BOARD_SIZE_Y):
            for c in range(BOARD_SIZE_X):
                if self.board[r][c] == 0:  # Только для безопасных ячеек
                    count = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue  # Пропускаем саму ячейку
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < BOARD_SIZE_Y and 0 <= nc < BOARD_SIZE_X and self.board[nr][nc] == 9:
                                count += 1
                    self.board[r][c] = count  # Записываем количество соседних мин

    def _add_buttons_to_view(self):
        """Добавляет кнопки на представление."""
        for r in range(BOARD_SIZE_Y):
            for c in range(BOARD_SIZE_X):
                is_mine = (self.board[r][c] == 9)  # Если это мина
                adjacent_mines = self.board[r][c] if not is_mine else 0  # Количество мин для безопасных ячеек

                button = MinesweeperButton(r, c, is_mine, adjacent_mines)
                self.board_buttons[r][c] = button
                self.add_item(button)

    async def on_timeout(self):
        """Обрабатывается при таймауте игры."""
        self.game_over = True
        for item in self.children:
            if isinstance(item, Button):
                item.disabled = True
        
        # Обновляем сообщение, чтобы показать, что игра окончена
        if self.message:
            # Извлекаем текущее сообщение, чтобы обновить его embed
            original_message = await self.message.channel.fetch_message(self.message.id)
            if original_message:
                embed = original_message.embeds[0] if original_message.embeds else discord.Embed(
                    title="💣 Экстремальный Сапер 💣",
                    description="Игра Сапер. Нажмите на ячейку. Если это мина - вы будете забанены!",
                    color=discord.Color.blue()
                )
                embed.description = (embed.description or "") + "\n\n**Время вышло! Игра завершена.**"
                await original_message.edit(embed=embed, view=self)


class Minesweeper(commands.Cog):
    """
    Экстремальная игра "Сапер".
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mines", aliases=["sapyor"], help="Запустить экстремальный Сапер!")
    @commands.guild_only()  # Убедиться, что команда используется только на сервере (для бана)
    # has_permissions для команды проверяет права пользователя, для бота нужна ручная проверка
    async def start_minesweeper(self, ctx: commands.Context):
        """
        Запускает новую игру Сапер.
        """
        # Проверка, есть ли у бота права на бан
        if not ctx.guild or not ctx.guild.me or not ctx.guild.me.guild_permissions.ban_members:
            await ctx.send("У меня нет прав на бан участников! Пожалуйста, дайте мне разрешение 'Ban Members'.")
            return

        embed = discord.Embed(
            title="💣 Экстремальный Сапер 💣",
            description="Нажмите на ячейку. Если это мина - вы будете забанены!\n"
                        f"Поле: {BOARD_SIZE_Y}x{BOARD_SIZE_X}, Мин: {NUM_MINES}",
            color=discord.Color.blue()
        )
        view = MinesweeperView()
        
        # Сохраняем сообщение, чтобы view мог обновить его при таймауте
        message = await ctx.send(embed=embed, view=view)
        view.message = message  # Привязываем сообщение к View для on_timeout


async def setup(bot):
    """Регистрирует ког Minesweeper."""
    await bot.add_cog(Minesweeper(bot))
