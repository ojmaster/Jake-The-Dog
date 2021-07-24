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


  @commands.command(aliases = ["poke"])
  async def pokemon(self, ctx, pimg, poke = None):
    """
    Pokeedex entry for Pokemon
    Usage: poke {back} <pokemon>
    {back} is optional
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

  @commands.command()
  async def shiny(self, ctx, pimg, poke = None):
    """
    Shiny entry for pokemon
    Usage: shiny {back} <pokemon>
    {back} is optional
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


  @commands.command()
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


  @commands.command()
  async def pdata(self, ctx, pokemon):
        """
        Pokemon Detailed Info
        """
        if not any(map(str.isdigit, pokemon)):
          pokemon = await self.pknamecheck(pokemon)
        pkid = pykemon.get_pokemon(pokemon).name
        pimg = f'http://play.pokemonshowdown.com/sprites/xyani/{pkid}.gif'
        stat = pykemon.get_pokemon(pokemon)
        embed = discord.Embed(title = await self.pokename(pokemon), description = await self.pdatadesc(pokemon), color = discord.Color.dark_magenta())
        embed.set_image(url = pimg)
        embed.add_field(name = "Base Stats", value = await self.pstat(pokemon))
        embed.add_field(name = "Type", value = await self.ptype(pokemon, "data"))
        embed.add_field(name = "Abilities", value = await self.pability(pokemon))
        embed.add_field(name = "Height & Weight", value = f'{await self.pheight(pokemon)}/{await self.pweight(pokemon)}')
        embed.add_field(name = "EV Yield", value = await self.pev(pokemon))
        embed.add_field(name = "Growth & Capture Rates", value = await self.gcr(pokemon))
        embed.add_field(name = "Gender Ratio", value = await self.gender(pokemon))
        embed.add_field(name = "Egg Groups", value = await self.egggroup(pokemon))
        embed.add_field(name = "Hatch Time", value = await self.hatchtime(pokemon))
        await ctx.send(embed = embed)

  async def pstat(self, pokemon):
        pstat = pykemon.get_pokemon(pokemon)
        data = [[str(pstat.stats[0].base_stat), str(pstat.stats[1].base_stat), str(pstat.stats[2].base_stat)], [str(pstat.stats[3].base_stat), str(pstat.stats[4].base_stat), str(pstat.stats[5].base_stat)]]
        pkst =  "`{: >0} {: >12} {: >12}`\n".format("HP", "Atk", "Def")
        row = data[0]
        pkst = pkst + "`{: >0} {: >11} {: >12}`\n".format(*row)
        pkst += "`{: >0} {: >11} {: >8}`\n".format("Sp. Atk", "Sp. Def", "Spe")
        row = data[1]
        pkst = pkst + "`{: >0} {: >11} {: >12}`\n".format(*row)
        return pkst

  async def ptype(self, pokemon, ptyp = "urmom"):
    if ptyp == "data":
        pokem = pypokedex.get(name=pokemon)
        ptype = ""
        pokem.types = [typ.capitalize() for typ in pokem.types]
        for typ in pokem.types:
          icon = await self.typeicon(typ)
          ptype += f'{icon} {typ}\n'
    else: 
        pokem = pypokedex.get(name=pokemon)
        ptype = ""
        pokem.types = [typ.capitalize() for typ in pokem.types]
        for typ in pokem.types:
          icon = await self.typeicon(typ)
          ptype += f'{icon} {typ} '
    return ptype


  async def pokename(self, pokemon):
    if any(map(str.isdigit, pokemon)):
        pk = pykemon.get_pokemon_species(pokemon)
        name = pk.name.capitalize()
    else: 
        pk = await self.pknamecheck(pokemon)
        name = pk.capitalize()
    return name

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
    checkpk = difflib.get_close_matches(pokemon, lst)
    checkpk = checkpk[0]
    return checkpk

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
        return "<:water_type:847958750400217098>"
    elif type == 'Steel':
        return "<:steel_type:847958750383439882>"
    elif type == 'Rock':
        return "<:rock_type:847958750307942400>"
    elif type == 'Psychic':
        return "<:psychic_type:847958750350671932>"
    elif type == 'Poison':
        return "<:poison_type:847958750383571024>"
    elif type == 'Normal':
        return "<:normal_type:847958750294966283>"
    elif type == 'Ice':
        return "<:ice_type:847958750228774932>"
    elif type == 'Ground':
        return "<:ground_type:847958750231920647>"
    elif type == 'Grass':
        return "<:grass_type:847958750341234718>"
    elif type == 'Ghost':
        return "<:ghost_type:847958750321049620>"
    elif type == 'Flying':
        return "<:flying_type:847958750249222174>"
    elif type == 'Fire':
        return "<:fire_type:847958750072930325>"
    elif type == 'Fighting':
        return "<:fighting_type:847958750245683200>"
    elif type == 'Electric':
        return "<:electric_type:847958750207541310>"
    elif type == 'Dragon':
        return "<:dragon_type:847958750123655188>"
    elif type == 'Bug':
        return "<:bug_type:847958749679583252>"
    elif type == 'Fairy':
        return "<:fairy_type:847958750253285436>"
    elif type == 'Dark':
        return "<:dark_type:847958749862821888>"
    
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
    return str(255 * (hatch + 1)) + " Steps"

def setup(bot):
	bot.add_cog(Pokemon(bot))