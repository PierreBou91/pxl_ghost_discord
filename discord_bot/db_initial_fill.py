import discord
from discord.ext import commands
from os import environ
import db_discord_helper as db

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


@bot.command()
async def add_all_members(ctx):
    member_list = []
    members = ctx.guild.members
    for mem in members:
        member_list.append(db.GhostMember(
                mem.id,
                mem.name,
                mem.display_name,
                mem.nick,
                mem.discriminator,
                mem.mention,
                mem.created_at,
                mem.joined_at,
                mem.top_role.id,
                mem.bot
                )
            )
    db.add_multiple_users(member_list)
    print("done")

bot.run(environ['CYBER_GHOST_TOKEN'])