import discord
from discord.ext import commands

TOKEN = 'YOUR_SECRET_HERE'
PREFIX = '^'
intents = discord.Intents().all()

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.command()
async def hello(ctx):
    await ctx.reply(f"Hello {ctx.author.display_name}!")
    
@bot.command()
async def user(ctx, member: discord.Member):
    role_names = [role.name for role in member.roles if role.name != "@everyone"]
    embed = discord.Embed(
        title = member.display_name,
        description = f"**---INFO---**\n**Username**: {member.name}\n**Id**: {member.id}\n**Roles**: {", ".join(role_names)}\n**Status**: {member.status}\n**Activity**: {member.activity}\n**Joined in**: {member.joined_at}\n**Account create in**: {member.created_at}\n **Bot**: {member.bot}",
        color=member.color
    )
    embed.set_thumbnail(url=member.avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def sendls(ctx, member: discord.Member, *text):
    await member.send(f"**Сообщение от**: *{ctx.author.display_name} ({ctx.author.name})*:\n\n{" ".join(text)}")

@bot.command()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)

@bot.command()
async def serverinf(ctx):
    await ctx.send(f"Name: {ctx.channel.guild.name}")

@bot.command()
async def serverinfo(ctx):
    role_names = [role.name for role in ctx.guild.roles if role.name != "@everyone"]
    embed = discord.Embed(
        title = ctx.channel.guild.name,
        description = f"**Server owner**: {ctx.channel.guild.owner}\n**Roles**: {", ".join(role_names)}\n**Members**: {len(ctx.channel.guild.members)}",
        color = discord.Color.gold()
    )
    embed.set_image(url=ctx.channel.guild.icon.url)
    await ctx.send(embed=embed)
bot.run(TOKEN)