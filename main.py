import interactions
import os
from interactions import CommandContext, Guild
from interactions.ext.tasks import IntervalTrigger, create_task
from configparser import ConfigParser
import random
import asyncio

config = ConfigParser()
config.read('./config/options.ini')
TOKEN = config.get('Bot_Config', 'TOKEN')

#def get_prefix(bot, message):
#  if not message.guild:
#    return commands.when_mentioned_or(">")(bot, message)
#  conn = sqlite3.connect('config/prefixes.sqlite')
#  c = conn.cursor()
#  c.execute("SELECT prefix FROM prefixes WHERE guild = ?", (message.guild.id,))
#  prefix = c.fetchone()[0]
#  conn.close()
#  return prefix

_ready: bool = False
bot = interactions.Client(token = TOKEN, intents = interactions.Intents.DEFAULT | interactions.Intents.GUILD_PRESENCES | interactions.Intents.GUILD_MEMBERS)

async def presence():
    act = random.randint(1, 5)
    if act == 1:
      dact = interactions.PresenceActivity(
                type = interactions.PresenceActivityType.GAME,
                name="BMO"
              )
    elif act == 2:
      dact = interactions.PresenceActivity(
                type = interactions.PresenceActivityType.STREAMING,
                name="Pirates of the Enchiridion",
                url="https://www.twitch.tv/0jmaster"
              )
    elif act == 3:
      dact = interactions.PresenceActivity(
                type = interactions.PresenceActivityType.LISTENING,
                name="Island Song"
              )
    elif act == 4:
      dact = interactions.PresenceActivity(
                type = interactions.PresenceActivityType.WATCHING,
                name="Distant Lands"
              )
    elif act == 5:
      dact = interactions.PresenceActivity(
                type = interactions.PresenceActivityType.COMPETING,
                name="Card Wars"
              )
    return await bot.change_presence(presence=interactions.ClientPresence(status = interactions.StatusType.ONLINE, activities = [dact]))


@bot.event
async def on_ready():
  global _ready
  if not _ready:
      print('------')
      print('Logged in as')
      u = interactions.User(**await bot._http.get_self())
      print(u.username)
      print(u.id)
      print('------')
      await listservers()
      await presence()
      change_stat.start()
      _ready = True

@create_task(IntervalTrigger(10800))
async def change_stat():
    await presence()

async def listservers():
    print("Server List:")
    for guild in bot.guilds:
      print(f" Name: {str(guild.name)} || ID: {str(guild.id)}")


#@bot.event
#async def on_guild_create(guild):
#    embed = interactions.Embed(title = "**Jake the Dog**", 
#                          description = f"Hello {guild.name}!",
#                          color = 0xA020F0
#    )
#    if guild.joined_at 
#      for channel in guild.channels:
#          if channel.type is interactions.ChannelType.GUILD_TEXT and channel.name.contains("general"):
#              await channel.send(embeds = embed)


#@bot.event
#async def on_guild_remove(guild):
#    conn = sqlite3.connect('config/prefixes.sqlite')
#    c = conn.cursor()
#    c.execute("DELETE FROM prefixes WHERE guild = ?", (guild.id,))
#    conn.commit()
#    conn.close()
#
#
#for filename in os.listdir('./cogs'):
#    if filename.endswith('.py') and not filename.startswith('Owner'):
#        bot.load_extension(f'cogs.{filename[:-3]}')
#        print(f'cogs.{filename[:-3]}')
#
#

@bot.command(description = "All servers bot is in", scope = [651230389171650560])
async def servercount(ctx: CommandContext):
    await ctx.get_guild()
    count = sum(1 for _ in bot.guilds)
    embed = interactions.Embed(title = "**Server Count**", description = count, color = interactions.Color.red())
    await ctx.send(embeds = embed)

cogchoices = [
  interactions.Choice(
    name = "Fun",
    value = "Fun"),
  interactions.Choice(
    name = "Minecraft",
    value = "Minecraft"),
  interactions.Choice(
    name = "Pokemon",
    value = "Pokemon"),
  interactions.Choice(
    name = "Utility",
    value = "Utility"),
]

@bot.command(description='Reloads extension (cogs, etc)', scope = [651230389171650560], options = [interactions.Option(
                                                                                                    type = interactions.OptionType.STRING,
                                                                                                    name = "extension",
                                                                                                    description = "What extension to load",
                                                                                                    required = True,
                                                                                                    choices = cogchoices
                                                                                                  )])
async def reload(ctx: CommandContext, extension):
  await ctx.get_guild()
  bot.reload(f'cogs.{extension}')
  await ctx.send(f'Extension "{extension}" reloaded!')

@bot.command(description = "Loads extension", scope = [651230389171650560], options = [interactions.Option(
                                                                                        type = interactions.OptionType.STRING,
                                                                                        name = "extension",
                                                                                        description = "What extension to load",
                                                                                        required = True,
                                                                                        choices = cogchoices
                                                                                      )])
async def load(ctx: CommandContext, extension):
  await ctx.get_guild()
  bot.load(f'cogs.{extension}')
  await ctx.send(f'Extension "{extension}" loaded')

@bot.command(description = "Unloads extension", scope = [651230389171650560], options = [interactions.Option(
                                                                                        type = interactions.OptionType.STRING,
                                                                                        name = "extension",
                                                                                        description = "What extension to load",
                                                                                        required = True,
                                                                                        choices = cogchoices
                                                                                      )])
async def unload(ctx: CommandContext, extension):
  await ctx.get_guild()  
  bot.remove(f'cogs.{extension}')
  await ctx.send(f'Extension "{extension}" unloaded')


bot.start()
