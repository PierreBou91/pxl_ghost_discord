import discord
from discord.ext import commands
from os import environ

from zmq import has
import db_discord_helper as db
import texts

#########################################
#           BOILER PLATE CODE           #
#########################################
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(
    command_prefix='/',
    description="Discord bot on Heroku",
    intents=intents)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

#########################################
#              COMMANDS                 #
#########################################

@bot.command()
async def giv(ctx, wallet):
    db.add_user(ctx, wallet)
    db.safe_add_to_giveaway(ctx)

bot.run(environ['CYBER_GHOST_TOKEN'])