import sqlite3
import discord
from discord.ext import commands, tasks
import os
from configparser import ConfigParser
import random
from discord_slash import SlashCommand
import asyncio

config = ConfigParser()
config.read('./config/options.ini')
TOKEN = config.get('Bot_Config', 'TOKEN')

def get_prefix(bot, message):
    if not message.guild:
      return commands.when_mentioned_or(">")(bot, message)
    conn = sqlite3.connect('config/prefixes.sqlite')
    c = conn.cursor()
    c.execute("SELECT prefix FROM prefixes WHERE guild = ?", (message.guild.id,))
    prefix = c.fetchone()[0]
    conn.close()
    return prefix

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=get_prefix, intents=intents, case_insensitive=True)
client = discord.Client()
slash = SlashCommand(bot, sync_commands=True) 

bot.remove_command('help')

async def presence():
    act = random.randint(1, 5)
    if act == 1:
      dact = discord.Game(name="BMO")
    elif act == 2:
      dact = discord.Streaming(name="Pirates of the Enchiridion", url="https://www.twitch.tv/0jmaster")
    elif act == 3:
      dact = discord.Activity(type=discord.ActivityType.listening, name="Island Song")
    elif act == 4:
      dact = discord.Activity(type=discord.ActivityType.watching, name="Distant Lands")
    elif act == 5:
      dact = discord.Activity(type=5,name="Card Wars")
    return await bot.change_presence(activity=dact)


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


@bot.event
async def on_guild_join(guild):
    conn = sqlite3.connect('config/prefixes.sqlite')
    c = conn.cursor()
    c.execute("INSERT INTO prefixes VALUES (?, ?)", (guild.id, ">"))
    conn.commit()
    conn.close()
    bs = False
    embed = discord.Embed(title="**Jake the Dog**",
                          description="Heyo!",
                          color=discord.Color.purple())
    embed.add_field(
        name="My default prefix is '>''",
        value="You can change my prefix with the `>setprefix <prefix>`",
        inline=False)
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
            await asyncio.sleep(0.1)
            await channel.send(embed=embed)
            bs = True
            break
    if not bs:
        for channel in guild.channels:
            if (
                channel.type is discord.ChannelType.text
                and channel.permissions_for(guild.me).send_messages
            ):
                await asyncio.sleep(0.1)
                await channel.send(embed=embed)
                break


@bot.event
async def on_guild_remove(guild):
    conn = sqlite3.connect('config/prefixes.sqlite')
    c = conn.cursor()
    c.execute("DELETE FROM prefixes WHERE guild = ?", (guild.id,))
    conn.commit()
    conn.close()


for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and not filename.startswith('Owner'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f'cogs.{filename[:-3]}')


@bot.command(name = "serverlist", 
            description = "All servers bot is in", 
            hidden = True)
async def servers(ctx):
  if ctx.author == bot.appinfo.owner:
      count = 0
      for guild in bot.guilds:
        count += 1
      embed = discord.Embed(title = "**Server Count**", description = count, color = discord.Color.red())
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
