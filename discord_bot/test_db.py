import discord
from discord.ext import commands
import os
import db_discord_helper as db

bot = commands.Bot(
    command_prefix='/',
    description="Test discord bot on Heroku",
    intents=discord.Intents.default())

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def add_user(ctx):
    db.add_user(ctx)


bot.run(os.environ['CYBER_GHOST_TOKEN'])