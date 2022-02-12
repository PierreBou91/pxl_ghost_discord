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
@commands.has_any_role("Admin")
async def giveaway(ctx, is_owner=None):
    is_owner = True if (is_owner == "owner") else False
    is_only_giveaway = True if db.check_only_giveaway(is_owner) else False
    if is_only_giveaway:
        db.launch_giveaway(ctx, is_owner)
        await ctx.reply(texts.giveaway(is_owner))
    else:
        await ctx.reply(texts.already_giveaway(is_owner))

@bot.command()
@commands.has_any_role("Admin")
async def delete(ctx, giveaway_id):
    db.delete_giveaway(giveaway_id)

@bot.command()
async def giv(ctx, wallet):
    db.add_user(ctx, wallet)
    db.safe_add_to_giveaway(ctx)

bot.run(environ['CYBER_GHOST_TOKEN'])