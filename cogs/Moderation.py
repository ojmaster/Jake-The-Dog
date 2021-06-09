import discord
from discord.ext import commands
from mojang import MojangAPI
import requests, json


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
client = discord.Client()

class Minecraft(commands.Cog):
  """
  Search up a minecraft player!
  """
	  
  def __init__(self, bot):
    self.bot = bot


  @commands.command(aliases = ["mc"])
  async def mcprofile(self, ctx, player):
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

def setup(bot):
	bot.add_cog(Minecraft(bot))

