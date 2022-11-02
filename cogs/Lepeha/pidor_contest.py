import sqlite3
import discord
import asyncio
import random
from discord.ext import commands
import os
import dotenv

dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(intents=intents)

DbName = 'discord.db'
headers = ['guild_id', 'user_id', 'message_content']
connection = sqlite3.connect(DbName)
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS discord(user_id, channel_id, message_content)")
cursor.execute("CREATE TABLE IF NOT EXISTS pidors(user_id INTEGER, user_name TEXT, score INTEGER DEFAULT 0)")
connection.commit()


@bot.slash_command()
async def registration(ctx: discord.ApplicationContext):
    await ctx.respond('Проверяю документы, секунду')
    users = []
    for user_id in cursor.execute("SELECT user_id FROM pidors"):
        users.append(int(''.join(map(str, user_id))))
    await asyncio.sleep(1.5)
    if ctx.author.id in users:
        await ctx.send_followup('Ты уже записан, дурачек')
    else:
        cursor.execute("INSERT INTO pidors VALUES(?, ?, ?)", (ctx.author.id, ctx.author.name, 0))
        connection.commit()
        await ctx.send_followup('Отлично, ты в игре!')


@bot.slash_command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def contest(ctx: discord.ApplicationContext):
    users = []
    for user_id in cursor.execute("SELECT user_id FROM pidors"):
        users.append(int(''.join(map(str, user_id))))
    winner_id = random.choice(users)
    print(winner_id)
    winner_name = str(
        ''.join(map(str, cursor.execute("SELECT user_name FROM pidors where user_id = ?", (winner_id,)).fetchone())))
    print(winner_name)
    new_score = int(
        ''.join(map(str, cursor.execute("SELECT score FROM pidors where user_id = ?", (winner_id,)).fetchone()))) + 1
    print(new_score)
    cursor.execute("UPDATE pidors SET score = ? WHERE user_id = ?", (new_score, winner_id))
    scores = []
    for user_id in cursor.execute("SELECT score FROM pidors"):
        scores.append(int(''.join(map(str, user_id))))
    print(scores)
    connection.commit()
    await ctx.respond(
        f'Вы объявлены пидором ~~дня~~ этих пяти секунд, {winner_name}. На вашем счету это {new_score} раз!')


@bot.slash_command()
async def top(ctx: discord.ApplicationContext):
    top = []
    for row in cursor.execute("SELECT user_name, score FROM pidors order by score DESC"):
        top.append(' - '.join(map(str, row)))
        print(row)
    print(top)
    await ctx.respond(f'Топ пидоров на данный момент: {str(top)}')


@bot.event
async def on_application_command_error(
        ctx: discord.ApplicationContext, error: discord.DiscordException
):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond("Эта команда еще в кд.")
    else:
        raise error


bot.run(token)
