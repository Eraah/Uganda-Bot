import discord
from discord.ext import commands
import os
import dotenv

dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))
intents = discord.Intents.all()
bot = commands.Bot(intents=intents)

for foldername in os.listdir('./cogs'):  # for every folder in cogs
    for filename in os.listdir(f'./cogs/{foldername}'):  # for every file in a folder in cogs
        if filename.endswith('.py') and not filename in ['util.py', 'error.py']:  # if the file is a python file
            bot.load_extension(f'cogs.{foldername}.{filename[:-3]}')  # load the extension


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


bot.run(token)
