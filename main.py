import discord
import time
from discord.ext import commands, tasks
import json
from decouple import config
import os
import random


Token = config('TOKEN')


def get_prefix(bot, message):
    with open('prefixes.json', 'r') as pr:
        prefixes = json.load(pr)
    if not message.guild:
      return commands.when_mentioned_or("!")(bot, message)
    return prefixes[str(message.guild.id)]


intents = discord.Intents.all()
bot = commands.Bot(command_prefix=get_prefix, intents=intents)
client = discord.Client()

bot.remove_command('help')

act = random.randint(1, 4)
if act == 1:
  dact = bot.change_presence(activity=discord.Game(name="BMO"))
elif act == 2:
  dact = bot.change_presence(activity=discord.Streaming(name="Pirates of the Enchiridion", url="https://www.twitch.tv/0jmaster"))
elif act == 3:
  dact = bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Island Song"))
elif act == 4:
  dact = bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Distant Lands"))

@tasks.loop(hours=1.5)
async def change_status():
    act()
    await dact

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await listservers()
    await dact
    if not hasattr(bot, 'appinfo'):
        bot.appinfo = await bot.application_info()
    await client.login(config('TOKEN'))


async def listservers():
    print("Server List:")
    for guild in bot.guilds:
        print(" Name: " + str(guild.name) + " || " + "ID: " + str(guild.id))

global count

@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as pr:
        prefixes = json.load(pr)
    prefixes[str(guild.id)] = '!'
    with open('prefixes.json', 'w') as pr:
        json.dump(prefixes, pr, indent=4)
    bs = False
    for channel in guild.channels:
        if "chat" in channel.name or "staff" in channel.name:
            time.sleep(0.1)
            embed = discord.Embed(title="**Jake the Dog**",
                                  description="Heyo!",
                                  color=discord.Color.purple())
            embed.add_field(
                name="My default prefix is '!''",
                value="You can change my prefix with the !setprefix",
                inline=False)
            await channel.send(embed=embed)
            inv = await channel.create_invite()
            bs = True
            break
    if bs == False:
        for channel in guild.channels:
            if channel.type is discord.ChannelType.text:
                time.sleep(0.1)
                embed = discord.Embed(title="**Jake the Dog**",
                                      description="Heyo!",
                                      color=discord.Color.purple())
                embed.add_field(
                    name="My default prefix is '!''",
                    value="You can change my prefix with the !setprefix",
                    inline=False)
                await channel.send(embed=embed)
                inv = await channel.create_invite()
                break
    global count
    count = 0
    for member in guild.members:
      if member.status != discord.Status.offline:
        count +=1
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
    if filename.endswith('.py') and not filename.startswith('__init__'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f'cogs.{filename[:-3]}')
bot.unload_extension('cogs.Owner')


@bot.command(name = "servers", 
            description = "All servers bot is in", 
            hidden = True)
async def servers(ctx):
  embed = discord.Embed(title = "**Server List**", color = discord.Color.red())
  for guild in bot.guilds:
    embed.add_field(name = f'__{guild.name}__', value = f'Member Count: {guild.member_count}', inline = True)
  await ctx.send(embed = embed)


@bot.command(name="reload",
             description='Reloads extension (cogs, etc)',
             hidden=True)
async def reload(ctx, extension):
  if ctx.author == bot.appinfo.owner:
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'Extension "{extension}" reloaded!')
  else:
    ctx.send("Insufficient Permissions")

@bot.command(name="load", description = "Loads extension", hidden = True)
async def load(ctx, extension):
  if ctx.author == bot.appinfo.owner:
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'Extension "{extension}" loaded')
  else:
    ctx.send("Insufficient Permissions")

@bot.command(name= "unload", description = "Unloads extension", hidden = True)
async def unload(ctx, extension):
  if ctx.author == bot.appinfo.owner:
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'Extension "{extension}" unloaded')
  else:
    ctx.send("Insufficient Permissions")


bot.run(config('TOKEN'))
