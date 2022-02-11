import discord
from discord.ext import commands
from os import environ
import db_discord_helper as db
import random
import texts

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

bot.run(environ['CYBER_GHOST_TOKEN'])