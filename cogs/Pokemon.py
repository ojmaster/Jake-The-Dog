import difflib
import os
import urllib.request

import discord
import pokepy
import pypokedex
import requests
from discord.ext import commands
from discord.ext.commands.errors import TooManyArguments
from discord_slash import SlashContext, cog_ext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_commands import create_choice, create_option
from PIL import Image, ImageSequence

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


  @commands.command(aliases = ["poke"])
  async def pokemon(self, ctx, poke, pimg = None, shiny = None):
    """
    Pokeedex entry for Pokemon
    Usage: poke <pokemon> {back} 
    {back} is optional (Defaults to `front` if left empty)
    """
    if pimg == "shiny":
      pimg = None
      shiny = "shiny"
    await Pokemon.pokemoncmd(self, ctx, poke, pimg, shiny)

  @cog_ext.cog_slash(name = "Pokedex", description= "Search up a pokemon", options = [
      create_option(
        name = "pokemon",
        description = "Pokemon to search",
        option_type = 3,
        required = True
      ),
      create_option(
        name = "sprite",
        description = "Back sprite (Leave empty for Front)",
        option_type = 3,
        required = False,
        choices = [
          create_choice(
            name = "front",
            value = "front"
          ),
          create_choice(
            name = "back",
            value = "back"
          )
        ]
      ),
      create_option(
        name = "shiny",
        description = "Shiny sprite (Leave empty for Normal)",
        option_type = 3,
        required = False,
        choices = [
          create_choice(
            name = "shiny",
            value = "shiny"
          ),
          create_choice(
            name = "normal",
            value = "normal"
          )
        ]
      )
    ])
  async def slashpokemon(self, ctx: SlashContext, pokemon: str, sprite: str = None, shiny: str = None):
    await Pokemon.pokemoncmd(self, ctx, pokemon, sprite, shiny)


  async def pokemoncmd(self, ctx, poke, pimg, shiny):
    try:
      embed = discord.Embed(title = await self.pokename(poke), color = discord.Color.red())
      poke = str(await self.pokename(poke)).lower()
      embed.add_field(name = "ID", value = pykemon.get_pokemon(poke).id)
      embed.add_field(name = "Type", value = await self.ptype(poke))
      embed.add_field(name = "Species", value = await self.pspecies(poke))
      embed.add_field(name = "Height", value = await self.pheight(poke))
      embed.add_field(name = "Weight", value = await self.pweight(poke))
      embed.add_field(name = "Main Region", value = await self.region(poke))
      embed.add_field(name = "Entry", value = await self.entry(poke), inline = False)
      if shiny == "shiny":
        if pimg == "back":
          await self.bsimg(poke)
          embed.set_image(url=f"attachment://{poke}sb.png")
          await ctx.send(file = discord.File(f"{poke}sb.png"), embed = embed)
          os.remove(f"{poke}sb.png")
        else:
          await self.psimg(poke)
          embed.set_image(url=f"attachment://{poke}sf.png")
          await ctx.send(file = discord.File(f"{poke}sf.png"), embed = embed)
          os.remove(f"{poke}sf.png")
      else:
        if pimg == "back":
          await self.bimg(poke)
          embed.set_image(url=f"attachment://{poke}b.png")
          await ctx.send(file = discord.File(f"{poke}b.png"), embed = embed)
          os.remove(f"{poke}b.png")
        else:
          await self.pimg(poke)
          embed.set_image(url=f"attachment://{poke}.png")
          await ctx.send(file = discord.File(f"{poke}.png"), embed = embed)
          os.remove(f"{poke}.png")
    except IndexError:
      embed = discord.Embed(title = 'Incorrect Input!', color = discord.Color.dark_red())
      await ctx.send(embed = embed)

  @commands.command()
  async def pitem(self, ctx, item):
    """
    Pokedex entry for PokeItem! 
    Usage: pitem <item>
    """
    await Pokemon.pitemcmd(self, ctx, item)

  @cog_ext.cog_slash(name = "PokeItem", description = "Search up any pokemon item", options = [
      create_option(
        name = "item",
        description = "Item to search",
        option_type= 3,
        required = True
      )
    ])
  async def slashpitem(self, ctx: SlashContext, item):
    await Pokemon.pitemcmd(self, ctx, item)

  async def pitemcmd(self, ctx, item):
    try:
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
    except IndexError:
      embed = discord.Embed(title = 'Incorrect Input!', color = discord.Color.dark_red())
      await ctx.send(embed = embed)

  @commands.command(aliases = ["pokedata"])
  async def pdata(self, ctx, pokemon):
    """
    Pokemon Detailed Info
    """
    await Pokemon.pdatacmd(self, ctx, pokemon)

  @cog_ext.cog_slash(name = "PokeData", description = "In-Depth data of a Pokemon", options = [
      create_option(
        name = "pokemon",
        description = "Pokemon to search",
        option_type = 3,
        required = True  
      )
    ])
  async def slashpdata(self, ctx: SlashContext, pokemon):
    await Pokemon.pdatacmd(self, ctx, pokemon)


  async def pdatacmd(self, ctx, pokemon):
    try:
      if not any(map(str.isdigit, pokemon)):
        pokemon = await self.pknamecheck(pokemon)
      pkid = pykemon.get_pokemon(pokemon).name
      pimg = f'http://play.pokemonshowdown.com/sprites/xyani/{pkid}.gif'
      stat = pykemon.get_pokemon(pokemon)
      embed = discord.Embed(title = await self.pokename(pokemon), description = await self.pdatadesc(pokemon), color = discord.Color.dark_magenta())
      embed.set_image(url = pimg)
      embed.add_field(name = "Base Stats", value = await self.pstat(pokemon))
      embed.add_field(name = "Type", value = await self.ptype(pokemon))
      embed.add_field(name = "Abilities", value = await self.pability(pokemon))
      embed.add_field(name = "Height & Weight", value = f'{await self.pheight(pokemon)}/{await self.pweight(pokemon)}')
      embed.add_field(name = "EV Yield", value = await self.pev(pokemon))
      embed.add_field(name = "Growth & Capture Rates", value = await self.gcr(pokemon))
      embed.add_field(name = "Gender Ratio", value = await self.gender(pokemon))
      embed.add_field(name = "Egg Groups", value = await self.egggroup(pokemon))
      embed.add_field(name = "Hatch Time", value = await self.hatchtime(pokemon))
      await ctx.send(embed = embed)
    except IndexError:
      embed = discord.Embed(title = 'Incorrect Input!', color = discord.Color.dark_red())
      await ctx.send(embed = embed)

  async def pstat(self, pokemon):
    pstat = pykemon.get_pokemon(pokemon)
    data = [
        [
            str(pstat.stats[0].base_stat),
            str(pstat.stats[1].base_stat),
            str(pstat.stats[2].base_stat),
        ],
        [
            str(pstat.stats[3].base_stat),
            str(pstat.stats[4].base_stat),
            str(pstat.stats[5].base_stat),
        ],
    ]
    row = data[0]
    pkst = "`{: >0} {: >13} {: >13}`\n".format(
        "HP", "Atk", "Def") + "`{: >0} {: >12} {: >13}`\n".format(*row)
    pkst += "`{: >0} {: >12} {: >9}`\n".format("Sp. Atk", "Sp. Def", "Spe")
    row = data[1]
    pkst += "`{: >0} {: >12} {: >13}`\n".format(*row)
    return pkst

  async def ptype(self, pokemon):
    pokem = pypokedex.get(name=pokemon)
    ptype = ""
    pokem.types = [typ.capitalize() for typ in pokem.types]
    for typ in pokem.types:
      icon = await self.typeicon(typ)
      ptype += f'{icon} {typ} \n'
    return ptype


  async def pokename(self, pokemon):
    if any(map(str.isdigit, pokemon)):
      pk = pykemon.get_pokemon_species(pokemon)
      return pk.name.capitalize()
    else: 
      pk = await self.pknamecheck(pokemon)
      return pk.capitalize()

  async def pdatadesc(self, pokemon):
        pdesc = "__**#"
        pdesc += str(pykemon.get_pokemon(pokemon).id)
        pdesc += " | "
        pdesc += str(pykemon.get_pokemon_species(pokemon).generation.name.upper())
        pdesc += "**__"
        pdesc = pdesc.replace('GENERATION-', 'Generation ')
        return pdesc

  async def pspecies(self, pokemon):
    pk = pykemon.get_pokemon_species(pokemon)
    return pk.genera[7].genus


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
    for i in range(6, len(entry), 6):
      entry.insert(i, "\n")
    entry = ' '.join(str(elem) for elem in entry)
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
    urllib.request.urlretrieve(pokem.sprites.front.get("default"), f"{pokem.name}.png")
    img = Image.open(f"{pokem.name}.png")
    img = img.resize((200,200), Image.ANTIALIAS)
    img.save(f"{pokem.name}.png")


  async def psimg(self, pokemon):
    pokem = pypokedex.get(name=pokemon)
    urllib.request.urlretrieve(pokem.sprites.front.get("shiny"), f"{pokem.name}sf.png")
    img = Image.open(f"{pokem.name}sf.png")
    img = img.resize((200,200), Image.ANTIALIAS)
    img.save(f"{pokem.name}sf.png")
  
  async def bimg(self, pokemon):
    pokem = pypokedex.get(name=pokemon)
    urllib.request.urlretrieve(pokem.sprites.back.get("default"), f"{pokem.name}b.png")
    img = Image.open(f"{pokem.name}b.png")
    img = img.resize((200,200), Image.ANTIALIAS)
    img.save(f"{pokem.name}b.png")

  async def bsimg(self, pokemon):
    pokem = pypokedex.get(name=pokemon)
    urllib.request.urlretrieve(pokem.sprites.back.get("shiny"), f"{pokem.name}sb.png")
    img = Image.open(f"{pokem.name}sb.png")
    img = img.resize((200,200), Image.ANTIALIAS)
    img.save(f"{pokem.name}sb.png")
  
  async def iname(self, name):
    if any(map(str.isdigit, name)):
        pit = pykemon.get_item(name)
        return pit.name.replace("-", " ").title()
    else:
        name = await self.namecheck(name)
        return name.replace("-", " ").title()

  async def iid(self, id):
    pit = pykemon.get_item(id)
    return str(pit.id)

  async def icat(self, category):
    return pykemon.get_item(category).category.name.title()

  async def ieffect(self, effect):
    return pykemon.get_item(effect).effect_entries[0].effect.replace("\n", " ")

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
    return pykemon.get_generation(await self.gen(pykemon.get_pokemon_species(gen).generation.name)).main_region.name.capitalize()

  async def namecheck(self, iitem):
    items = requests.get('https://pokeapi.co/api/v2/item/?limit=1005')
    item = items.json()
    item = item['results']
    lst = [name['name'] for name in item]
    return difflib.get_close_matches(iitem, lst)[0]

  async def pknamecheck(self, pokemon):
    pokemons = requests.get('https://pokeapi.co/api/v2/pokemon/?limit=898')
    pkm = pokemons.json()
    pkm = pkm['results']
    lst = [name['name'] for name in pkm]
    return difflib.get_close_matches(pokemon, lst)[0]

  async def pability(self, pokemon):
    pklink = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
    abilities = requests.get(pklink)
    abs = abilities.json()
    abs = abs['abilities']
    pkab = ""
    x = 1
    y = 0
    for ability in abs:
      if ability['is_hidden'] == False:
        y += 1
        pkab += str(ability['ability']['name']).title()
        pkab = pkab.replace("-", " ")
        if x == 1:
          pkab += "/"
          x += 1
      else: 
        pkab += "\n"
        pkab += str(ability['ability']['name']).title()
        pkab = pkab.replace("-", " ")
    if y == 1:
        pkab = pkab.replace("/", "")
    return pkab

  async def typeicon(self, type):
    if type == 'Water':
        return "<:water:946555702032367616>"
    elif type == 'Steel':
        return "<:steel:946555701977825290>"
    elif type == 'Rock':
        return "<:rock_type:946555701965250630>"
    elif type == 'Psychic':
        return "<:psychic:946555701814239233>"
    elif type == 'Poison':
        return "<:poison:946555702078505030>"
    elif type == 'Normal':
        return "<:normal:946555701742952509>"
    elif type == 'Ice':
        return "<:ice:946555701608734721>"
    elif type == 'Ground':
        return "<:ground:946555701805850624>"
    elif type == 'Grass':
        return "<:grass:946555702011375647>"
    elif type == 'Ghost':
        return "<:ghost:946555701780676668>"
    elif type == 'Flying':
        return "<:flying:946555701424177173>"
    elif type == 'Fire':
        return "<:fire:946555701797457920>"
    elif type == 'Fighting':
        return "<:fighting:946555701638094899>"
    elif type == 'Electric':
        return "<:electric:946555701789077514>"
    elif type == 'Dragon':
        return "<:dragon:946555702133010482>"
    elif type == 'Bug':
        return "<:bug:946555689613021244>"
    elif type == 'Fairy':
        return "<:fairy:946555701663252553>"
    elif type == 'Dark':
        return "<:dark:946555693387907072>"
    
  async def pev(self, pokemon):
    stats = pykemon.get_pokemon(pokemon).stats
    x = 1
    for effort in stats:
        if str(effort) != "<Pokemon_Stat | 0>":
            for c in str(effort):
                if c.isdigit():
                   return f'{c} {await self.statname(x)}'
        else:
            x += 1

  async def statname(self, stat):
      if stat == 1:
          return 'HP'
      elif stat == 2:
          return 'Atk'
      elif stat == 3:
          return 'Def'
      elif stat == 4:
          return 'Sp. Atk'
      elif stat == 5:
          return 'Sp. Def'
      elif stat == 6:
          return 'Spe'

  async def gcr(self, pokemon):
    gcr = pykemon.get_pokemon_species(pokemon)
    growth = gcr.growth_rate.name.title() + "/"
    capturerate = str(gcr.capture_rate)
    growth = growth.replace("-", " ")
    return growth + capturerate

  async def gender(self, pokemon):
    gender = pykemon.get_pokemon_species(pokemon).gender_rate
    if gender == -1:
        return "Genderless"
    else: 
        return str(gender) + "/8 ♀️"

  async def egggroup(self, pokemon):
    egggroup = pykemon.get_pokemon_species(pokemon)
    egroup = ""
    x = 0
    for group in egggroup.egg_groups:
       egroup += str(group.name).title()
       if x == 0:
           egroup += "/"
           x += 1
    if egroup[-1] == "/":
        egroup = egroup[:-1]
    egroup = egroup.replace("-", " ")
    return egroup

  async def hatchtime(self, pokemon):
    hatch = pykemon.get_pokemon_species(pokemon).hatch_counter
    return f'{str(255 * (hatch + 1))} Steps'

def setup(bot):
	bot.add_cog(Pokemon(bot))
