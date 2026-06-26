import discord
from discord.ext import commands
import random
from datetime import datetime

# --- Конфигурация ---
TOKEN = 'YOUR_SECRET_HERE'
PREFIX = '^'
# Укажите ID текстового канала, куда бот будет отправлять логи.
# Вы можете получить ID канала, включив режим разработчика в Discord,
# затем щелкнув правой кнопкой мыши по каналу и выбрав "Копировать ID".
LOG_CHANNEL_ID = 123456789012345678  # <<< ЗАМЕНИТЕ ЭТОТ ID НА ID ВАШЕГО КАНАЛА ЛОГОВ

# --- Intents (Намерения) ---
# Намерения сообщают Discord, какие события бот хочет получать.
# Для полноценного функционала модерации и информации о пользователях/сервере
# необходимы members и message_content.
intents = discord.Intents.default()
intents.members = True          # Требуется для on_member_update, подсчета участников, аудит-логов
intents.message_content = True  # Требуется для обработки аргументов команд

# --- Инициализация бота ---
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# --- Вспомогательная функция для отправки сообщений в канал логов ---
async def send_log_message(guild, message_content):
    """
    Отправляет заданное сообщение в канал логов.
    Обрабатывает ошибки, если канал не найден или у бота нет прав.
    """
    log_channel = guild.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        try:
            await log_channel.send(message_content)
        except discord.Forbidden:
            print(f"Ошибка: У меня нет прав для отправки сообщений в канал логов {log_channel.name} ({log_channel.id}) в гильдии {guild.name}.")
        except Exception as e:
            print(f"Неизвестная ошибка при отправке в канал логов {log_channel.name}: {e}")
    else:
        print(f"Ошибка: Канал логов с ID {LOG_CHANNEL_ID} не найден в гильдии {guild.name}.")

# --- События бота ---
@bot.event
async def on_ready():
    """Вызывается, когда бот готов и подключен к Discord."""
    print(f'Бот запущен как {bot.user.name} ({bot.user.id})')
    print('------')

@bot.event
async def on_member_update(before, after):
    """
    Логирует изменение никнеймов пользователей.
    Срабатывает при любом изменении профиля пользователя, включая никнейм.
    """
    if before.nick != after.nick:
        guild = after.guild
        await send_log_message(
            guild,
            f"**Изменение никнейма:** Пользователь `{before.name}` (ID: {before.id}) изменил никнейм:\n"
            f"Старый: `{before.nick or 'Не установлен'}`\n"
            f"Новый: `{after.nick or 'Не установлен'}`"
        )

@bot.event
async def on_member_remove(member):
    """
    Логирует выход пользователя из гильдии, пытаясь определить, был ли он кикнут.
    Использует аудит-логи для определения модератора и причины.
    """
    # Ждем, пока аудит-логи станут доступны после загрузки бота
    await bot.wait_until_ready()
    guild = member.guild
    try:
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
            if entry.target == member and (datetime.utcnow() - entry.created_at).total_seconds() < 5:
                await send_log_message(
                    guild,
                    f"**Кик пользователя:** `{member.name}` (ID: {member.id}) был кикнут.\n"
                    f"**Причина:** `{entry.reason or 'Не указана'}`\n"
                    f"**Модератор:** `{entry.user.display_name}` (ID: {entry.user.id})"
                )
                return
    except discord.Forbidden:
        print(f"Ошибка: У меня нет прав для просмотра аудит-логов в гильдии {guild.name}.")
    
    await send_log_message(guild, f"**Пользователь покинул сервер:** `{member.name}` (ID: {member.id}). Возможно, был кикнут, но запись в аудит-логах не найдена или у бота нет прав для их просмотра.")


@bot.event
async def on_member_ban(guild, user):
    """
    Логирует бан пользователя.
    Использует аудит-логи для определения модератора и причины.
    """
    # Ждем, пока аудит-логи станут доступны после загрузки бота
    await bot.wait_until_ready()
    try:
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
            if entry.target == user and (datetime.utcnow() - entry.created_at).total_seconds() < 5:
                await send_log_message(
                    guild,
                    f"**Бан пользователя:** `{user.name}` (ID: {user.id}) был забанен.\n"
                    f"**Причина:** `{entry.reason or 'Не указана'}`\n"
                    f"**Модератор:** `{entry.user.display_name}` (ID: {entry.user.id})"
                )
                return
    except discord.Forbidden:
        print(f"Ошибка: У меня нет прав для просмотра аудит-логов в гильдии {guild.name}.")
    
    await send_log_message(guild, f"**Пользователь забанен:** `{user.name}` (ID: {user.id}). Причина или модератор не найдены в аудит-логах или у бота нет прав для их просмотра.")

@bot.event
async def on_command_error(ctx, error):
    """
    Глобальный обработчик ошибок команд.
    Предоставляет пользователю понятные сообщения об ошибках.
    """
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply(f"Вы пропустили обязательный аргумент для этой команды. Правильное использование: `{ctx.prefix}{ctx.command.name} {ctx.command.signature}`")
    elif isinstance(error, commands.BadArgument):
        await ctx.reply("Неверный тип аргумента. Убедитесь, что вы предоставили правильное значение.")
    elif isinstance(error, commands.CommandNotFound):
        # Игнорировать неизвестные команды, чтобы не спамить в чат
        pass
    elif isinstance(error, commands.MissingPermissions):
        perms = ', '.join(error.missing_permissions)
        await ctx.reply(f"У вас нет необходимых прав ({perms}) для выполнения этой команды.")
    elif isinstance(error, commands.BotMissingPermissions):
        perms = ', '.join(error.missing_permissions)
        await ctx.reply(f"У меня нет необходимых прав ({perms}) для выполнения этой команды.")
    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.reply("Эту команду нельзя использовать в личных сообщениях.")
    else:
        print(f"Неизвестная ошибка команды {ctx.command}: {error}")
        await ctx.reply("Произошла неизвестная ошибка. Пожалуйста, попробуйте еще раз позже.")


# --- Команды бота ---

@bot.command()
async def hello(ctx):
    """
    Отвечает приветствием.
    Пример использования: `^hello`
    """
    await ctx.reply(f"Hello {ctx.author.display_name}!")

@bot.command()
async def user(ctx, member: discord.Member):
    """
    Отображает подробную информацию о пользователе.
    Пример использования: `^user @ИмяПользователя`
    """
    role_names = [role.name for role in member.roles if role.name != "@everyone"]
    embed = discord.Embed(
        title = member.display_name,
        description = (f"**--- ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ ---**\n"
                       f"**Имя пользователя**: {member.name}\n"
                       f"**ID**: {member.id}\n"
                       f"**Роли**: {", ".join(role_names) if role_names else "Нет ролей"}\n"
                       f"**Статус**: {member.status.name.capitalize()}\n"
                       f"**Активность**: {member.activity.name if member.activity else 'Нет активности'}\n"
                       f"**Присоединился**: {member.joined_at.strftime('%d.%m.%Y %H:%M:%S') if member.joined_at else 'Неизвестно'}\n"
                       f"**Аккаунт создан**: {member.created_at.strftime('%d.%m.%Y %H:%M:%S')}\n"
                       f"**Бот**: {'Да' if member.bot else 'Нет'}"),
        color=member.color if member.color != discord.Color.default() else discord.Color.blue()
    )
    if member.avatar:
        embed.set_thumbnail(url=member.avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def sendls(ctx, member: discord.Member, *text):
    """
    Отправляет личное сообщение указанному пользователю.
    Пример использования: `^sendls @ИмяПользователя Привет, как дела?`
    """
    if not text:
        await ctx.reply("Вы должны указать текст для отправки личного сообщения.")
        return
    try:
        message_to_send = " ".join(text)
        await member.send(f"**Сообщение от**: *{ctx.author.display_name} ({ctx.author.name})*:\n\n{message_to_send}")
        await ctx.reply(f"Сообщение успешно отправлено {member.display_name}.")
    except discord.Forbidden:
        await ctx.reply(f"Не удалось отправить сообщение {member.display_name}. Возможно, у него закрыты личные сообщения или он заблокировал бота.")
    except Exception as e:
        await ctx.reply(f"Произошла ошибка при отправке сообщения: {e}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    """
    Удаляет указанное количество сообщений из текущего канала.
    Бот должен иметь право "Управление сообщениями".
    Пример использования: `^clear 5`
    """
    if amount <= 0:
        await ctx.reply("Количество сообщений для удаления должно быть положительным числом.")
        return
    
    try:
        # Удаляем на 1 сообщение больше, чтобы удалить и саму команду clear
        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Удалено {len(deleted) - 1} сообщений.", delete_after=5)
    except discord.Forbidden:
        await ctx.reply("У меня нет прав для удаления сообщений в этом канале. Убедитесь, что у меня есть право 'Управление сообщениями'.")
    except discord.HTTPException as e:
        await ctx.reply(f"Произошла ошибка при удалении сообщений: {e}")

@bot.command(name='server')
async def server_info(ctx):
    """
    Выводит подробную информацию о сервере.
    Пример использования: `^server`
    """
    guild = ctx.guild
    
    # Подсчет текстовых и голосовых каналов
    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)
    
    # Подсчет участников онлайн
    online_members = len([m for m in guild.members if m.status != discord.Status.offline])
    
    embed = discord.Embed(
        title=f"Информация о сервере: {guild.name}",
        description=f"**ID сервера:** {guild.id}\n",
        color=discord.Color.gold(),
        timestamp=datetime.utcnow()
    )
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    
    embed.add_field(name="Владелец", value=guild.owner.mention if guild.owner else "Неизвестно", inline=True)
    embed.add_field(name="Создан", value=guild.created_at.strftime("%d.%m.%Y %H:%M:%S"), inline=True)
    embed.add_field(name="Участники", value=f"Всего: {guild.member_count}\nОнлайн: {online_members}", inline=True)
    embed.add_field(name="Каналы", value=f"Текстовые: {text_channels}\nГолосовые: {voice_channels}", inline=True)
    embed.add_field(name="Роли", value=f"{len(guild.roles) - 1} (без @everyone)", inline=True) # -1 потому что @everyone всегда является ролью
    embed.add_field(name="Уровень буста", value=f"Уровень {guild.premium_tier} ({guild.premium_subscription_count} бустов)", inline=True)

    if guild.banner:
        embed.set_image(url=guild.banner.url)

    embed.set_footer(text=f"Запрошено {ctx.author.display_name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
    await ctx.send(embed=embed)


# --- Мини-игра: Угадай число ---

# Словарь для хранения состояний игр по ID пользователя
# Пример: {user_id: {'number': secret_number, 'attempts': remaining_attempts}}
game_states = {} 

@bot.command(name='guess')
async def guess_the_number(ctx):
    """
    Начинает игру "Угадай число" (от 1 до 10).
    Пример использования: `^guess`
    """
    user_id = ctx.author.id
    if user_id in game_states:
        await ctx.reply("Вы уже начали игру. Угадайте число или скажите `!отмена`, чтобы закончить.")
        return

    secret_number = random.randint(1, 10)
    game_states[user_id] = {'number': secret_number, 'attempts': 3}
    await ctx.reply("Я загадал число от 1 до 10. У вас есть 3 попытки, чтобы угадать его! Ответьте своим предположением (например, `5`). Для отмены игры напишите `!отмена`.")

@bot.listen('on_message')
async def handle_guess(message):
    """
    Обрабатывает попытки угадывания числа для активных игр.
    Эта функция слушает все сообщения и реагирует, если пользователь участвует в игре.
    """
    # Игнорировать сообщения от ботов и сообщения не из гильдии
    if message.author.bot or not message.guild:
        return

    user_id = message.author.id
    
    # Если пользователь участвует в игре
    if user_id in game_states:
        game_data = game_states[user_id]
        
        # Если пользователь хочет отменить игру
        if message.content.lower() == '!отмена':
            del game_states[user_id]
            await message.reply("Игра отменена.")
            return

        # Если сообщение является числом
        if message.content.isdigit():
            guess = int(message.content)

            if not (1 <= guess <= 10):
                await message.reply("Пожалуйста, угадайте число от 1 до 10.")
                return

            game_data['attempts'] -= 1

            if guess == game_data['number']:
                await message.reply(f"Поздравляю, {message.author.display_name}! Вы угадали число `{game_data['number']}`!")
                del game_states[user_id] # Удалить игру после победы
            elif game_data['attempts'] > 0:
                hint = "меньше" if guess > game_data['number'] else "больше"
                await message.reply(f"Неправильно! Загаданное число **{hint}**, чем `{guess}`. Осталось попыток: {game_data['attempts']}.")
            else:
                await message.reply(f"К сожалению, у вас закончились попытки. Загаданное число было `{game_data['number']}`.")
                del game_states[user_id] # Удалить игру после проигрыша
        # Если сообщение не число и не отмена, но игра активна
        else:
            await message.reply(f"Пожалуйста, введите число для вашей догадки или `!отмена` для завершения игры. Осталось попыток: {game_data['attempts']}.")


# --- Запуск бота ---
if __name__ == '__main__':
    bot.run(TOKEN)
