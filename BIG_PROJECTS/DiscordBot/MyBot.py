import disnake
from disnake.ext import commands

bot = commands.Bot(command_prefix=".", intents=disnake.Intents.all(), test_guilds=None)

@bot.event
async def ready():
    print(f"{bot.user}, ready to play!")

@bot.event
async def role_give(member):
    role = await disnake.utils.get(guild_id=member.guild.id, role_id=1117890499328618717)
    chanel = member.guild.system_chanel

    embed = disnake.Embed(
        title="New user!",
        description=f"{member.name}#{member.discriminator}",
        color=(120, 100, 50)
    )

    await member.add_roles(role)
    await chanel.send(embed=embed)
    

bot.run("YOUR_DISCORD_TOKEN_HERE")
