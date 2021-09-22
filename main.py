import discord
import time
from discord.ext import commands, tasks
import json
from configparser import ConfigParser
import os
import random
from discord_slash.context import MenuContext
from discord_slash.model import ContextMenuType
from discord_slash import SlashCommand

config = ConfigParser()
config.read('./config/options.ini')
TOKEN = config.get('Bot_Config', 'TOKEN')

def get_prefix(bot, message):
    with open('prefixes.json', 'r') as pr:
      prefixes = json.load(pr)
    if not message.guild:
      return commands.when_mentioned_or(">")(bot, message)
    return prefixes[str(message.guild.id)]

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=get_prefix, intents=intents, case_insensitive=True)
client = discord.Client()
slash = SlashCommand(bot, sync_commands=True) 

bot.remove_command('help')

async def presence():
    act = random.randint(1, 5)
    if act == 1:
      dact = bot.change_presence(activity=discord.Game(name="BMO"))
    elif act == 2:
      dact = bot.change_presence(activity=discord.Streaming(name="Pirates of the Enchiridion", url="https://www.twitch.tv/0jmaster"))
    elif act == 3:
      dact = bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Island Song"))
    elif act == 4:
      dact = bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Distant Lands"))
    elif act == 5:
      dact = bot.change_presence(activity=discord.Activity(type=5,name="Card Wars"))
    dact = await dact
    return dact


@bot.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await listservers()
    await presence()
    if not hasattr(bot, 'appinfo'):
        bot.appinfo = await bot.application_info()
    await client.login(TOKEN)
    change_stat.start()


@tasks.loop(hours = 3)
async def change_stat():
    await presence()

async def listservers():
    print("Server List:")
    for guild in bot.guilds:
        print(" Name: " + str(guild.name) + " || " + "ID: " + str(guild.id))

global count

@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as pr:
        prefixes = json.load(pr)
    prefixes[str(guild.id)] = '>'
    with open('prefixes.json', 'w') as pr:
        json.dump(prefixes, pr, indent=4)
    bs = False
    global inv
    for channel in guild.channels:
        if (
            channel.type is discord.ChannelType.text
            and (
                "chat" in channel.name
                or "staff" in channel.name
                or "main" in channel.name
                or "general" in channel.name
            )
            and channel.permissions_for(guild.me).send_messages
        ):
            time.sleep(0.1)
            embed = discord.Embed(title="**Jake the Dog**",
                                  description="Heyo!",
                                  color=discord.Color.purple())
            embed.add_field(
                name="My default prefix is '>''",
                value="You can change my prefix with the `>setprefix <prefix>`",
                inline=False)
            await channel.send(embed=embed)
            inv = await channel.create_invite()
            bs = True
            break
    if not bs:
        for channel in guild.channels:
            if (
                channel.type is discord.ChannelType.text
                and channel.permissions_for(guild.me).send_messages
            ):
                time.sleep(0.1)
                embed = discord.Embed(title="**Jake the Dog**",
                                      description="Heyo!",
                                      color=discord.Color.purple())
                embed.add_field(
                    name="My default prefix is '>''",
                    value="You can change my prefix with the `>setprefix <prefix>`",
                    inline=False)
                await channel.send(embed=embed)
                inv = await channel.create_invite()
                break
    global count
    count = sum(
        member.status != discord.Status.offline for member in guild.members
    )
    await send_join(guild, inv)


@bot.event
async def on_guild_remove(guild):
  msg = bot.get_channel(837556075305500672)
  embed = discord.Embed(title = "**Left Guild**", color=discord.Color.blurple())
  embed.add_field(name = "__Name__", value = str(guild.name))
  embed.add_field(name = "__ID__", value = str(guild.id))
  embed.add_field(name = "__Guild Owner__", value = str(guild.owner))
  embed.add_field(name = "__Members__", value = str(guild.member_count))
  count = 0
  for member in guild.members:
    if member.status != discord.Status.offline:
      count +=1
  embed.add_field(name = "__Online__", value = str(count))
  embed.set_thumbnail(url = str(guild.icon_url))
  await msg.send(embed = embed)
  with open('prefixes.json', 'r') as pr:
      prefixes = json.load(pr)
  with open('prefixes.json', 'w') as pr:
      json.dump(prefixes, pr, indent=4)


async def send_join(guild, invite):
    msg = bot.get_channel(837555246691254346)
    embed = discord.Embed(title = "**Joined New Guild**", color=discord.Color.blurple())
    embed.add_field(name = "__Name__", value = str(guild.name))
    embed.add_field(name = "__ID__", value = str(guild.id))
    embed.add_field(name = "__Guild Owner__", value = str(guild.owner))
    embed.add_field(name = "__Members__", value = str(guild.member_count))
    embed.add_field(name = "__Online__", value = str(count))
    embed.add_field(name = "__Invite__", value = str(invite))
    embed.set_thumbnail(url = str(guild.icon_url))
    await msg.send(embed = embed)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f'cogs.{filename[:-3]}')
bot.unload_extension('cogs.Owner')

@bot.command(name = "serverlist", 
            description = "All servers bot is in", 
            hidden = True)
async def servers(ctx):
  if ctx.author == bot.appinfo.owner:
      embed = discord.Embed(title = "**Server List**", color = discord.Color.red())
      for guild in bot.guilds:
        srvid = guild.id
        embed.add_field(name = f'__{guild.name}__', value = f'Member Count: {guild.member_count}\nID: {srvid}', inline = True)
      await ctx.reply(embed = embed)
  else:
    ctx.reply("Only available to Bot Owner")


@bot.command(name="reload",
             description='Reloads extension (cogs, etc)',
             hidden=True)
async def reload(ctx, extension):
  if ctx.author == bot.appinfo.owner:
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.reply(f'Extension "{extension}" reloaded!')
  else:
    ctx.reply("Insufficient Permissions")

@bot.command(name="load", description = "Loads extension", hidden = True)
async def load(ctx, extension):
  if ctx.author == bot.appinfo.owner:
    bot.load_extension(f'cogs.{extension}')
    await ctx.reply(f'Extension "{extension}" loaded')
  else:
    ctx.reply("Insufficient Permissions")

@bot.command(name= "unload", description = "Unloads extension", hidden = True)
async def unload(ctx, extension):
  if ctx.author == bot.appinfo.owner:
    bot.unload_extension(f'cogs.{extension}')
    await ctx.reply(f'Extension "{extension}" unloaded')
  else:
    ctx.reply("Insufficient Permissions")

bot.run(TOKEN)
