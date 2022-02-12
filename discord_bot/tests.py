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
async def add_user(ctx, wallet):
    result = db.add_user(ctx, wallet)
    if result == "UniqueViolation":
        print(f"{ctx.author.name} is already in the database")
        return

@bot.command()
async def rules(ctx):
    await ctx.send(texts.rules())

@bot.command()
@commands.has_any_role("Admin")
async def giveaway(ctx, name, is_owner=False):
    result = db.safe_giveaway_launch(ctx, name, is_owner)
    if result == "UniqueViolation":
        await ctx.send(f"The giveaway {name} is already ongoing !")
        return
    elif result == "OwnerUnique":
        await ctx.send(f"There already is an owner giveaway ongoing !")
        return      
    elif result == "NonOwnerUnique":
        await ctx.send(f"There already is a non-owner giveaway ongoing !")
        return
    else:
        await ctx.send(texts.giveaway(name,is_owner))

@bot.command()
@commands.has_any_role("Admin")
async def delete(ctx, giveaway):
    result = db.delete_giveaway(giveaway)
    if result == "Done":
        await ctx.reply(f"Giveaway {giveaway} deleted !")
    else:
        await ctx.reply(f"No giveaway named: {giveaway}... error: {result}")

@bot.command()
async def giv(ctx, wallet):
    db.add_user(ctx, wallet)
    db.safe_add_to_giveaway(ctx)

@bot.command()
@commands.has_any_role("Admin")
async def update_db(ctx):
    # Load members from server
    server_members = []
    for mem in ctx.guild.members:
        server_members.append(db.member_adapter_from_discord(mem))

    # Load members from db
    db_members = db.get_members()

    # Update the "is_here value"
    has_left = []
    for mem in db_members:
        if (mem not in server_members):
            has_left.append(mem)
    for mem in has_left:
        db.update_is_here(mem, False)
    
    # Update diplay_name and nick
    for mem in db_members:
        pass

bot.run(environ['CYBER_GHOST_TOKEN'])