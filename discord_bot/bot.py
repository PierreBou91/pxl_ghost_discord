import discord
from discord.ext import commands
from os import environ
import db_discord_helper as db

#########################################
#           BOILER PLATE CODE           #
#########################################
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

#########################################
#               ON MESSAGE              #
#########################################
@bot.event
async def on_message(message):
    # don't respond to ourselves
    if message.author.id == 931674481628434503:
        return

    if str(message.content).casefold() == 'ping':
        await message.channel.send('pong')
    elif str(message.content).casefold() == 'pong':
        await message.channel.send('NO, YOU have to say ping and ONLY I get to say pong !')
    elif str(message.content).casefold() == 'f':
        await message.channel.send('f')
    
    # Necessary command for the command to work
    await bot.process_commands(message)

#########################################
#              COMMANDS                 #
#########################################
@bot.command()
async def add_user(ctx, wallet):
    db.add_user(ctx, wallet)

@bot.command()
async def test(ctx):
    await ctx.send("Heroku works")

#########################################
#             ON MEMBER JOIN            #
#########################################
@bot.event
async def on_member_join(member):
    await member.add_roles(932799395865444382)


#########################################
#          TESTING COMMANDS             #
#########################################

bot.run(environ['CYBER_GHOST_TOKEN'])