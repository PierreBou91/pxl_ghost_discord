import discord
from discord.ext import commands
from os import environ
import db_discord_helper as db
import random
import aws_connect_helper as s3

#########################################
#           BOILER PLATE CODE           #
#########################################
bot = commands.Bot(
    command_prefix='/',
    description="Discord bot on Heroku",
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
        await message.channel.send('F')
    
    # Necessary command for the command to work
    await bot.process_commands(message)

#########################################
#              COMMANDS                 #
#########################################
@bot.command()
async def add_user(ctx, wallet):
    db.add_user(ctx, wallet)

@bot.command()
async def ghost(ctx, number: int):
    r = random.randint(1,10000)
    try:
        if (number == 0):
            file = discord.File(s3.get_ghost(r), filename='ghost.png')
            await ctx.reply(file=file, content=f'''You called a random ghost, I'm the number {r}''')
        elif (number in (9903,9904,9905)):
            file = discord.File(s3.get_ghost(number), filename='ghost.png')
            await ctx.reply(file=file, content=f'''Hello, I'm the ghost number {number}''')
        elif (number > 9900 and number < 10001):
            file = file = discord.File(s3.get_ghost('mystery'), filename='ghost.png')
            await ctx.reply(file=file, content=f'''Hello, I'm the mystery ghost...''')
        else:
            file = discord.File(s3.get_ghost(number), filename='ghost.png')
            await ctx.reply(file=file, content=f'''Hello, I'm the ghost number {number}''')
    except Exception:
        await ctx.reply('You have to give a number between 1 and 10000')
        return

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