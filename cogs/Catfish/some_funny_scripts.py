import discord
from discord.ext import commands

bot = commands.Bot(intents=intents)

@bot.slash_command()
async def stress_test(ctx: discord.ApplicationContext):
    await ctx.respond('Эта функция ничего пока не умеет')