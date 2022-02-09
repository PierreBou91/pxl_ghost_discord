import discord
from discord.ext import commands
from os import environ
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
async def add_user(ctx, wallet):
    db.add_user(ctx, wallet)


bot.run(environ['CYBER_GHOST_TOKEN'])