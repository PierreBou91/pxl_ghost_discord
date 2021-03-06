import discord
from discord.ext import commands
from os import environ
import texts
import db_discord_helper as db
import re

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

    if message.channel.id == 931679915248594944:
        if db.check_if_ongoing_giveaway():
            if not bool(re.match(r"^0x[a-fA-F0-9]{40}$", message.content)):
                await message.reply(texts.channel_reserved())
                await message.reply(texts.wrong_wallet_address())
        else:
            await message.channel.send(texts.no_ongoing_giveway())

    # necessary call for the commands to work
    await bot.process_commands(message)

@bot.command()
@commands.has_any_role("Admin")
async def add_wandering(ctx):
    pass

bot.run(environ['CYBER_GHOST_TOKEN'])
