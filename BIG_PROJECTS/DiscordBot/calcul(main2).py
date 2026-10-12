import disnake
from disnake.ext import commands

bot = commands.Bot(command_prefix=".", intents=disnake.Intents.all(), test_guilds=None)
@bot.event
async def on_ready():
    print("Машина вийшла з ангару!")

@bot.slash_command(name='calculate', description='calculate')
async def calculate(inter, num1: str, oper: str, num2: str):
    author = inter.author
    guild = bot.get_guild()

    a = eval(num1+oper+num2)
    await inter.send(embed = disnake.Embed(title='Ваш результат: ', description=a, color=0x123123))

    await author.send(embed = disnake.Embed(title='Ваш результат: ', description=a, color=0x123123))
    await guild.create_role(name=str(a))
    motorola = disnake.utils.get(guild.roles, name=str(a))
    await author.add_roles(motorola)
bot.run('')