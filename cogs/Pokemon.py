import discord
from discord.ext import commands
import pypokedex
import urllib.request
from PIL import Image
import os, requests, json, difflib
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


  @commands.command(aliases = ["poke", "Poke", "Pokemon"])
  async def pokemon(self, ctx, pimg, poke = None):
    """
    Pokeedex entry for Pokemon
    Usage: pokedex <pokemon>
    """
    if pimg == "back":
      embed = discord.Embed(title = await self.pokename(poke), color = discord.Color.red())
      if not any(map(str.isdigit, poke)):
          poke = await self.pknamecheck(poke)
      embed.add_field(name = "ID", value = pykemon.get_pokemon(poke).id)
      embed.add_field(name = "Type", value = await self.ptype(poke))
      embed.add_field(name = "Species", value = await self.pspecies(poke))
      embed.add_field(name = "Height", value = await self.pheight(poke))
      embed.add_field(name = "Weight", value = await self.pweight(poke))
      embed.add_field(name = "Main Region", value = await self.region(poke))
      embed.add_field(name = "Entry", value = await self.entry(poke), inline = False)
      await self.bimg(poke)
      embed.set_image(url="attachment://pokemonb.png")
      await ctx.send(file = discord.File("pokemonb.png"), embed = embed)
      os.remove("pokemonb.png")
    else: 
      embed = discord.Embed(title = await self.pokename(pimg), color = discord.Color.red())
      if not any(map(str.isdigit, pimg)):
          pimg = await self.pknamecheck(pimg)
      embed.add_field(name = "ID", value = pykemon.get_pokemon(pimg).id)
      embed.add_field(name = "Type", value = await self.ptype(pimg))
      embed.add_field(name = "Species", value = await self.pspecies(pimg))
      embed.add_field(name = "Height", value = await self.pheight(pimg))
      embed.add_field(name = "Weight", value = await self.pweight(pimg))
      embed.add_field(name = "Main Region", value = await self.region(pimg))
      embed.add_field(name = "Entry", value = await self.entry(pimg), inline = False)
      await self.pimg(pimg)
      embed.set_image(url="attachment://pokemonf.png")
      await ctx.send(file = discord.File("pokemonf.png"), embed = embed)
      os.remove("pokemonf.png")

  @commands.command(aliases = ["Shiny"])
  async def shiny(self, ctx, pimg, poke=None):
    """
    Shiny entry for pokemon
    Usage: shiny <pokemon>
    """
    if pimg == "back":
      stitle = str(await self.pokename(poke))
      embedtitle = f'Shiny {stitle}'
      embed = discord.Embed(title = embedtitle, color = discord.Color.red())
      if not any(map(str.isdigit, poke)):
          poke = await self.pknamecheck(poke)
      embed.add_field(name = "ID", value = pykemon.get_pokemon(poke).id)
      embed.add_field(name = "Type", value = await self.ptype(poke))
      embed.add_field(name = "Species", value = await self.pspecies(poke))
      embed.add_field(name = "Height", value = await self.pheight(poke))
      embed.add_field(name = "Weight", value = await self.pweight(poke))
      embed.add_field(name = "Main Region", value = await self.region(poke))
      embed.add_field(name = "Entry", value = await self.entry(poke), inline = False)
      await self.bsimg(poke)
      embed.set_image(url="attachment://shinyb.png")
      await ctx.send(file = discord.File("shinyb.png"), embed = embed)
      os.remove("shinyb.png")
    else: 
      stitle = str(await self.pokename(pimg))
      embedtitle = f'Shiny {stitle}'
      embed = discord.Embed(title = embedtitle, color = discord.Color.red())
      if not any(map(str.isdigit, pimg)):
          pimg = await self.pknamecheck(pimg)
      embed.add_field(name = "ID", value = pykemon.get_pokemon(pimg).id)
      embed.add_field(name = "Type", value = await self.ptype(pimg))
      embed.add_field(name = "Species", value = await self.pspecies(pimg))
      embed.add_field(name = "Height", value = await self.pheight(pimg))
      embed.add_field(name = "Weight", value = await self.pweight(pimg))
      embed.add_field(name = "Main Region", value = await self.region(pimg))
      embed.add_field(name = "Entry", value = await self.entry(pimg), inline = False)
      await self.psimg(pimg)
      embed.set_image(url="attachment://shinyf.png")
      await ctx.send(file = discord.File("shinyf.png"), embed = embed)
      os.remove("shinyf.png")


  @commands.command(aliases = ["Pitem"])
  async def pitem(self, ctx, item):
    """
    Pokedex entry for PokeItem! 
    Usage: pitem <item>
    """
    embed = discord.Embed(title = await self.iname(item), color = discord.Color.green())
    if not any(map(str.isdigit, item)):
      item = await self.namecheck(item)
    embed.add_field(name = "ID", value = await self.iid(item))
    embed.add_field(name = "Category", value = await self.icat(item))
    embed.add_field(name = "Entry", value = await self.iflvtxt(item))
    embed.add_field(name = "Effect", value = await self.ieffect(item))
    await self.ipic(item)
    embed.set_thumbnail(url = "attachment://item.png")
    await ctx.send(file = discord.File("item.png"), embed = embed)
    os.remove("item.png")


  async def ptype(self, pokemon):
    pokem = pypokedex.get(name=pokemon)
    ptype = ""
    pokem.types = [typ.capitalize() for typ in pokem.types]
    for typ in pokem.types:
      ptype += f'{typ} '
    return ptype



  async def pokename(self, pokemon):
    if any(map(str.isdigit, pokemon)):
        pk = pykemon.get_pokemon_species(pokemon)
        name = pk.name.capitalize()
    else: 
        pk = await self.pknamecheck(pokemon)
        name = pk.capitalize()
    return name


  async def pspecies(self, pokemon):
    pk = pykemon.get_pokemon_species(pokemon)
    species = pk.genera[7].genus
    return species


  async def entry(self, pokemon):
    pk = pykemon.get_pokemon_species(pokemon)
    vers = pk.generation.name
    vers = await self.gen(vers)
    vers = await self.game(vers)
    for flavor in pk.flavor_text_entries:
      if flavor.language.name == 'en' and flavor.version.name == vers:
        entry = flavor.flavor_text
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
  
  async def iname(self, name):
    if any(map(str.isdigit, name)):
        pit = pykemon.get_item(name)
        name = pit.name.replace("-", " ").title()
    else:
        name = await self.namecheck(name)
        name = name.replace("-", " ").title()
    return name

  async def iid(self, id):
    pit = pykemon.get_item(id)
    pid = str(pit.id)
    return pid

  async def icat(self, category):
    pit = pykemon.get_item(category)
    category = pit.category.name.title()
    return category

  async def ieffect(self, effect):
    pit = pykemon.get_item(effect)
    effect = pit.effect_entries[0].effect
    effect = effect.replace("\n", " ")
    return effect

  async def iflvtxt(self, flvtxt):
    pit = pykemon.get_item(flvtxt)
    for flavor in pit.flavor_text_entries:
      if flavor.language.name == 'en':
        flvtxt = flavor.text
    return flvtxt

  async def ipic(self, pic):
    pic = pykemon.get_item(pic)
    urllib.request.urlretrieve(pic.sprites.default, "item.png")
    img = Image.open("item.png")
    img = img.resize((200,200), Image.ANTIALIAS)
    img.save("item.png")

  async def gen(self, gen):
    if gen == "generation-i":
      return 1
    elif gen == "generation-ii":
      return 2
    elif gen == "generation-iii":
      return 3
    elif gen == 'generation-iv':
      return 4
    elif gen == 'generation-v':
      return 5
    elif gen == 'generation-vi':
      return 6
    elif gen == 'generation-vii':
      return 7
    elif gen == 'generation-viii':
      return 8

  async def game(self, game):
    if game == 1:
      return 'red'
    elif game == 2:
      return 'gold'
    elif game == 3:
      return 'ruby'
    elif game == 4:
      return 'diamond'
    elif game == 5:
      return 'black'
    elif game == 6:
      return 'x'
    elif game == 7:
      return 'sun'
    elif game == 8:
      return 'sword'

  async def region(self, gen):
    poke = pykemon.get_pokemon_species(gen).generation.name
    poke = await self.gen(poke)
    reg = pykemon.get_generation(poke)
    return reg.main_region.name.capitalize()


  async def namecheck(self, iitem):
    lst = []
    items = requests.get('https://pokeapi.co/api/v2/item/?limit=1005')
    item = items.json()
    item = item['results']
    for name in item:
        lst.append(name['name'])
    checkitem = difflib.get_close_matches(iitem, lst)
    checkitem = checkitem[0]
    return checkitem

  async def pknamecheck(self, pokemon):
    lst = []
    pokemons = requests.get('https://pokeapi.co/api/v2/pokemon/?limit=898')
    pkm = pokemons.json()
    pkm = pkm['results']
    for name in pkm:
        lst.append(name['name'])
    checkitem = difflib.get_close_matches(pokemon, lst)
    checkitem = checkitem[0]
    return checkitem

def setup(bot):
	bot.add_cog(Pokemon(bot))