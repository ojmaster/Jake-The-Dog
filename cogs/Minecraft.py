import discord
from discord.ext import commands
from mojang import MojangAPI
import requests, json
from mcstatus import MinecraftServer


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
client = discord.Client()

class Minecraft(commands.Cog):
  """
  Minecraft searches!
  """
	  
  def __init__(self, bot):
    self.bot = bot


  @commands.command(aliases = ["mcp"])
  async def mcprofile(self, ctx, player):
      """
      Search up a minecraft player!
      Usage: mcp <username>
      """
      uuid = MojangAPI.get_uuid(player)
      if not uuid:
          await ctx.send(f'{player} does not exist.')
      else:
          profile = MojangAPI.get_profile(uuid)
          embed = discord.Embed(title = "UUID", description = f'`{uuid}`', color = discord.Color.dark_green())
          embed.set_author(name = profile.name, url = 'https://images-ext-1.discordapp.net/external/ha2UA0g2Fsh0wn67g6bU49JA1YOJFqyn2LgPvDS2W2w/https/orig00.deviantart.net/34de/f/2012/204/b/c/grass_block_by_barakaldo-d58bi3u.gif')
          embed.set_thumbnail(url = f'https://visage.surgeplay.com/full/512/{uuid}')
          mcskin = profile.skin_url
          embed.add_field(name = "Textures", value = f"[MC Skin]({mcskin})")
          embed.add_field(name = 'Skin Type', value = profile.skin_model.capitalize())
          embed.add_field(name = "Username History", value = await self.namehistory(uuid), inline = False)
          await ctx.send(embed = embed)
  
  async def namehistory(self, player):
      name_history = MojangAPI.get_name_history(player)
      npf = MojangAPI.get_profile(player)
      names = []
      nm = ""
      x = 0
      for data in name_history:
          names.append("`" + data['name'] + "`")
      names = "\n".join(names)
      return names

  @commands.command(aliases = ['mcs'])
  async def mcserver(self, ctx, ip, port = ''):
      """
      Search up a minecraft server
      Usage: mcs <ip> <port> (port optional)
      """
      try: 
          if port.isdigit():
            mcserv = requests.get(f'https://api.mcsrvstat.us/2/{ip}:{port}').json()
          else:
            mcserv = requests.get(f'https://api.mcsrvstat.us/2/{ip}').json()
          server = MinecraftServer.lookup(f'{ip}:{port}')
          status = server.status()
          online = mcserv['players']['online']
          max = mcserv['players']['max']
          motd = mcserv['motd']['clean']
          version = mcserv['version']
          latency = round(status.latency)
          embed = discord.Embed(title = ip, description = "<:online:854498244658593802> Server is online", color = discord.Color.dark_green())
          embed.add_field(name = "Type", value = "Java", inline = False)
          embed.add_field(name = "MOTD", value = str(motd)[2:-2])
          embed.add_field(name = "Players", value = f'{online}/{max}', inline = False)
          embed.add_field(name = "Version", value = version, inline = False)
          embed.add_field(name = "Latency", value = f'{latency}ms')
          if port.isdigit():
              embed.set_thumbnail(url = f'https://mc-api.net/v3/server/favicon/{ip}:{port}')
          else:
              embed.set_thumbnail(url = f'https://mc-api.net/v3/server/favicon/{ip}')
          embed.set_footer(text = f'Generated by {self.bot.appinfo.name}')
          await ctx.send(embed = embed)
      except Exception as e:
          embed = discord.Embed(title = ip, description = "<:dnd:854498244453335050> Server is offline", color = discord.Color.dark_red())
          await ctx.send(embed = embed)


  @commands.command(aliases = ['mcb'])
  async def mcbedrock(self, ctx, ip, port = ''):
      """
      Search up a minecraft server
      Usage: mcb <ip> <port> (port optional)
      """
      try: 
          if port.isdigit():
            mcserv = requests.get(f'https://api.mcsrvstat.us/bedrock/2/{ip}:{port}').json()
          else:
            mcserv = requests.get(f'https://api.mcsrvstat.us/bedrock/2/{ip}').json()
          online = mcserv['players']['online']
          max = mcserv['players']['max']
          motd = mcserv['motd']['clean']
          version = mcserv['version']
          embed = discord.Embed(title = ip, description = "<:online:854498244658593802> Server is online", color = discord.Color.dark_green())
          embed.add_field(name = "Type", value = "Bedrock", inline = False)
          embed.add_field(name = "MOTD", value = str(motd)[2:-2])
          embed.add_field(name = "Players", value = f'{online}/{max}', inline = False)
          embed.add_field(name = "Version", value = version, inline = False)
          if port.isdigit():
              embed.set_thumbnail(url = f'https://api.mcsrvstat.us/icon/{ip}:{port}')
          else:
              embed.set_thumbnail(url = f'https://api.mcsrvstat.us/icon/{ip}')
          embed.set_footer(text = f'Generated by {self.bot.appinfo.name}')
          await ctx.send(embed = embed)
      except Exception as e:
          embed = discord.Embed(title = ip, description = "<:dnd:854498244453335050> Server is offline", color = discord.Color.dark_red())
          embed.add_field(name = "Did you put in the right IP?", value = "Make sure the right IP is used")
          await ctx.send(embed = embed)


def setup(bot):
	bot.add_cog(Minecraft(bot))

