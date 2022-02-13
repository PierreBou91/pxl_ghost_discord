import discord
from discord.ext import commands
from os import environ
import re

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

@bot.event
async def on_message(message):
    # don't respond to ourselves
    if message.author.id == 931674481628434503:
        return

    # giveaway channel id: 931945712290258994
    # testbot channel id: 931679915248594944
    if message.channel.id == 931679915248594944:
        pass    
    # print(message.channel.name)
    # print(message.channel.id)
    # bool(re.match(r"^0x[a-fA-F0-9]{40}$", message.content))
    # if bool(re.match(r"^0x[a-fA-F0-9]{40}$", message.content)):
    #     print(message.author)
    #     print(db.member_adapter_from_discord(message.author).__dict__)
    #     wallet_is_in, wallet_owner = db.wallet_already_in_db(message.content)
    #     db.add_wallet(db.member_adapter_from_discord(message.author), message.content)
    print(db.get_members()["375291554543173632"].__dict__)
    
    # necessary call for the commands to work
    await bot.process_commands(message)

@bot.command()
async def giv(ctx, wallet):
    db.add_user(ctx, wallet)
    db.safe_add_to_giveaway(ctx)

bot.run(environ['CYBER_GHOST_TOKEN'])