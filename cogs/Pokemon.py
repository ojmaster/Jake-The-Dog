import discord
from discord.ext import commands
import pypokedex
import urllib.request
from PIL import Image
import os, json
import requests
import pokepy


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
client = discord.Client()
pykemon = pokepy.V2Client()


class Pokemon(commands.Cog):
  """
  Gotta Catch Em All!
  """
  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases = ["pokemon", "poke"])
  async def pokedex(self, ctx, pimg, poke = None):
    """
    Search up a pokemon
    Usage: pokedex <pokemon>
    """
    if pimg == "back":
      pokem = pypokedex.get(name=poke)
      embed = discord.Embed(title = await self.pokename(poke), color = discord.Color.red())
      embed.add_field(name = "ID", value = str(pokem.dex))
      embed.add_field(name = "Type", value = await self.ptype(poke))
      embed.add_field(name = "Species", value = await self.pspecies(poke))
      embed.add_field(name = "Height", value = await self.pheight(poke))
      embed.add_field(name = "Weight", value = await self.pweight(poke))
      embed.add_field(name = "Entry", value = await self.entry(poke), inline = False)
      await self.bimg(poke)
      embed.set_image(url="attachment://pokemonb.png")
      await ctx.send(file = discord.File("pokemonb.png"), embed = embed)
      os.remove("pokemonb.png")
    else: 
      pokem = pypokedex.get(name=pimg)
      embed = discord.Embed(title = await self.pokename(pimg), color = discord.Color.red())
      embed.add_field(name = "ID", value = str(pokem.dex))
      embed.add_field(name = "Type", value = await self.ptype(pimg))
      embed.add_field(name = "Species", value = await self.pspecies(pimg))
      embed.add_field(name = "Height", value = await self.pheight(pimg))
      embed.add_field(name = "Weight", value = await self.pweight(pimg))
      embed.add_field(name = "Entry", value = await self.entry(pimg), inline = False)
      await self.pimg(pimg)
      embed.set_image(url="attachment://pokemonf.png")
      await ctx.send(file = discord.File("pokemonf.png"), embed = embed)
      os.remove("pokemonf.png")

  @commands.command()
  async def shiny(self, ctx, pimg, poke=None):
    """
    Pokemon Shiny Sprite
    Usage: shiny <pokemon>
    """
    if pimg == "back":
      pokem = pypokedex.get(name=poke)
      stitle = str(await self.pokename(poke))
      embedtitle = f'Shiny {stitle}'
      embed = discord.Embed(title = embedtitle, color = discord.Color.red())
      embed.add_field(name = "ID", value = str(pokem.dex))
      embed.add_field(name = "Type", value = await self.ptype(poke))
      embed.add_field(name = "Species", value = await self.pspecies(poke))
      embed.add_field(name = "Height", value = await self.pheight(poke))
      embed.add_field(name = "Weight", value = await self.pweight(poke))
      embed.add_field(name = "Entry", value = await self.entry(poke), inline = False)
      await self.bsimg(poke)
      embed.set_image(url="attachment://shinyb.png")
      await ctx.send(file = discord.File("shinyb.png"), embed = embed)
      os.remove("shinyb.png")
    else: 
      pokem = pypokedex.get(name=pimg)
      stitle = str(await self.pokename(pimg))
      embedtitle = f'Shiny {stitle}'
      embed = discord.Embed(title = embedtitle, color = discord.Color.red())
      embed.add_field(name = "ID", value = str(pokem.dex))
      embed.add_field(name = "Type", value = await self.ptype(pimg))
      embed.add_field(name = "Species", value = await self.pspecies(pimg))
      embed.add_field(name = "Height", value = await self.pheight(pimg))
      embed.add_field(name = "Weight", value = await self.pweight(pimg))
      embed.add_field(name = "Entry", value = await self.entry(pimg), inline = False)
      await self.psimg(pimg)
      embed.set_image(url="attachment://shinyf.png")
      await ctx.send(file = discord.File("shinyf.png"), embed = embed)
      os.remove("shinyf.png")


  async def ptype(self, pokemon):
    pokem = pypokedex.get(name=pokemon)
    ptype = ""
    pokem.types = [typ.capitalize() for typ in pokem.types]
    for typ in pokem.types:
      ptype += f'{typ} '
    return ptype


  async def pokename(self, pokemon):
    pk = pykemon.get_pokemon_species(pokemon)
    name = pk.name.capitalize()
    return name


  async def pspecies(self, pokemon):
    pk = pykemon.get_pokemon_species(pokemon)
    species = pk.genera[7].genus
    return species


  async def entry(self, pokemon):
    pk = pykemon.get_pokemon_species(pokemon)
    entry = pk.flavor_text_entries[1].flavor_text
    entry = entry.replace("\n", " ")
    entry = entry.split()
    i = 6
    while i < len(entry):
      entry.insert(i, "\n")
      i += 6
    entry = ' '.join([str(elem) for elem in entry])
    return entry
      

  async def pheight(self, pokemon):
    pk = pykemon.get_pokemon(pokemon)
    pk = pk.height
    pk = pk / 10
    ft = int(round(pk / 0.3048))
    inch = int(round(pk / 0.3048 % 1 * 12))
    pk = str(pk) + " m " + f"({ft}' {inch:02d}\")"
    return str(pk)


  async def pweight(self, pokemon):
    pk = pykemon.get_pokemon(pokemon)
    pk = pk.weight
    pk = pk / 10
    lbs = pk * 2.205
    pk = str(pk) + " kg " + f'({lbs:0.1f} lbs)'
    return str(pk)


  async def pimg(self, pokemon):
    pokem = pypokedex.get(name=pokemon)
    urllib.request.urlretrieve(pokem.sprites.front.get("default"), "pokemonf.png")
    img = Image.open("pokemonf.png")
    img = img.resize((200,200), Image.ANTIALIAS)
    img.save("pokemonf.png")


  async def psimg(self, pokemon):
    pokem = pypokedex.get(name=pokemon)
    urllib.request.urlretrieve(pokem.sprites.front.get("shiny"), "shinyf.png")
    img = Image.open("shinyf.png")
    img = img.resize((200,200), Image.ANTIALIAS)
    img.save("shinyf.png")
  
  async def bimg(self, pokemon):
    pokem = pypokedex.get(name=pokemon)
    urllib.request.urlretrieve(pokem.sprites.back.get("default"), "pokemonb.png")
    img = Image.open("pokemonb.png")
    img = img.resize((200,200), Image.ANTIALIAS)
    img.save("pokemonb.png")

  async def bsimg(self, pokemon):
    pokem = pypokedex.get(name=pokemon)
    urllib.request.urlretrieve(pokem.sprites.back.get("shiny"), "shinyb.png")
    img = Image.open("shinyb.png")
    img = img.resize((200,200), Image.ANTIALIAS)
    img.save("shinyb.png")
  


def setup(bot):
	bot.add_cog(Pokemon(bot))