import difflib
import os
import urllib.request

import pokepy
import pypokedex
import requests
import interactions
from interactions import CommandContext, ComponentContext
from PIL import Image, ImageSequence


pykemon = pokepy.V2Client()

class Pokemon(interactions.Extension):
  """
  Gotta Catch Em All!
  """
  def __init__(self, bot: interactions.Client):
      self.bot: interactions.Client = bot


  @interactions.extension_command(name = "pokedex", description = "Pokeedex entry for Pokemon", scope = [651230389171650560], options = [
    interactions.Option(name = "pokemon", description = "Pokemon to search for", type = interactions.OptionType.STRING, required = True),
    interactions.Option(name = "shiny", description = "Show shiny sprite", type = interactions.OptionType.BOOLEAN, required = False),
    interactions.Option(name = "back", description = "Show back sprite", type = interactions.OptionType.BOOLEAN, required = False)
  ])
  @interactions.autodefer()
  async def slashpokemon(self, ctx: CommandContext, pokemon: str, back: str = None, shiny: str = None):
    await Pokemon.pokemoncmd(self, ctx, pokemon, shiny, back)


  async def pokemoncmd(self, ctx, poke, shiny, pimg):
    await ctx.get_channel()
    try:
      poke = str(await self.pokename(poke)).lower()
      embed = interactions.Embed(title = await self.pknameformat(poke), color = interactions.Color.red())
      embed.add_field(name = "ID", value = pykemon.get_pokemon(poke).id, inline = True)
      embed.add_field(name = "Type", value = await self.ptype(poke), inline = True)
      embed.add_field(name = "Species", value = await self.pspecies(poke), inline = True)
      embed.add_field(name = "Height", value = await self.pheight(poke), inline = True)
      embed.add_field(name = "Weight", value = await self.pweight(poke), inline = True)
      embed.add_field(name = "Main Region", value = await self.region(poke), inline = True)
      embed.add_field(name = "Entry", value = await self.entry(poke), inline = False)
      if shiny == True:
        if pimg == True:
          await self.bsimg(poke)
          embed.set_image(url=f"attachment://{poke}sb.png") 
          await ctx.send(files = interactions.File(filename = f"{poke}sb.png"), embeds = embed)
          os.remove(f"{poke}sb.png")
        else:
          await self.psimg(poke)
          embed.set_image(url=f"attachment://{poke}sf.png")
          await ctx.send(files = interactions.File(filename = f"{poke}sf.png"), embeds = embed)
          os.remove(f"{poke}sf.png")
      else:
        if pimg == True:
          await self.bimg(poke)
          embed.set_image(url=f"attachment://{poke}b.png")
          await ctx.send(files = interactions.File(filename = f"{poke}b.png"), embeds = embed)
          os.remove(f"{poke}b.png")
        else:
          await self.pimg(poke)
          embed.set_image(url=f"attachment://{poke}.png")
          await ctx.send(files = interactions.File(filename = f"{poke}.png"), embeds = embed)
          os.remove(f"{poke}.png")
    except:
      embed = interactions.Embed(title = 'Incorrect Input!', color = interactions.Color.red())
      await ctx.send(embeds = embed)


  @interactions.extension_command(name = "pokeitem", description = "Search up any pokemon item", scope = [651230389171650560], options = [
    interactions.Option(name = "item", description = "Item to search", type = interactions.OptionType.STRING, required = True)
  ])
  @interactions.autodefer()
  async def slashitem(self, ctx: CommandContext, item: str):
    await Pokemon.pitemcmd(self, ctx, item)
    

  async def pitemcmd(self, ctx, item):
    await ctx.get_channel()
    try:
      embed = interactions.Embed(title = await self.iname(item), color = interactions.Color.green())
      if not any(map(str.isdigit, item)):
        item = await self.namecheck(item)
      embed.add_field(name = "ID", value = await self.iid(item))
      embed.add_field(name = "Category", value = await self.icat(item))
      embed.add_field(name = "Entry", value = await self.iflvtxt(item))
      embed.add_field(name = "Effect", value = await self.ieffect(item))
      await self.ipic(item)
      embed.set_thumbnail(url = "attachment://item.png")
      await ctx.send(files = interactions.File(filename = "item.png"), embeds = embed)
      os.remove("item.png")
    except:
      embed = interactions.Embed(title = 'Incorrect Input!', color = interactions.Color.red())
      await ctx.send(embeds = embed)

  
  @interactions.extension_command(name = "pokedata", description = "In-Depth data of a Pokemon", scope = [651230389171650560], options = [
    interactions.Option(name = "pokemon", description = "Pokemon to search", type = interactions.OptionType.STRING, required = True)
  ])
  @interactions.autodefer()
  async def slashpdata(self, ctx: CommandContext, pokemon):
    await Pokemon.pdatacmd(self, ctx, pokemon)


  async def pdatacmd(self, ctx, pokemon):
    await ctx.get_channel()
    try:
      if not any(map(str.isdigit, pokemon)):
        pokemon = await self.pknamecheck(pokemon)
      pkid = pykemon.get_pokemon(pokemon).name
      pkid = pkid.split('-', 1)[0]
      pimg = f'http://play.pokemonshowdown.com/sprites/xyani/{pkid}.gif'
      embed = interactions.Embed(title = pkid.capitalize(), description = await self.pdatadesc(pokemon), color = 0x8b008b)
      embed.set_image(url = pimg)
      embed.add_field(name = "Base Stats", value = await self.pstat(pokemon), inline = True)
      embed.add_field(name = "Type", value = await self.ptype(pokemon), inline = True)
      embed.add_field(name = "Abilities", value = await self.pability(pokemon), inline = True)
      embed.add_field(name = "Height & Weight", value = f'{await self.pheight(pokemon)}/{await self.pweight(pokemon)}', inline = True)
      embed.add_field(name = "EV Yield", value = await self.pev(pokemon), inline = True)
      embed.add_field(name = "Growth & Capture Rates", value = await self.gcr(pokemon), inline = True)
      embed.add_field(name = "Gender Ratio", value = await self.gender(pokemon), inline = True)
      embed.add_field(name = "Egg Groups", value = await self.egggroup(pokemon), inline = True)
      embed.add_field(name = "Hatch Time", value = await self.hatchtime(pokemon), inline = True)
      await ctx.send(embeds = embed)
    except :
      embed = interactions.Embed(title = 'Incorrect Input!', color = interactions.Color.red())
      await ctx.send(embeds = embed)

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


  async def pknameformat(self, poke):
    poke = poke.split('-', 1)[0]
    return poke.capitalize()


  async def ptype(self, pokemon):
    pokem = pypokedex.get(name=pokemon)
    ptype = ""
    pokem.types = [typ.capitalize() for typ in pokem.types]
    for typ in pokem.types:
      icon = await self.typeicon(typ)
      ptype += f'{icon} {typ} \n'
    return ptype


  async def pokename(self, pokemon):
    if any(map(str.isdigit, str(pokemon))):
      pokemon = pykemon.get_pokemon_species(pokemon).name
    pk = await self.pknamecheck(pokemon)
    return pk.capitalize()

  async def pdatadesc(self, pokemon):
    pk = pokemon.split('-', 1)[0]
    return f"__**#{str(pykemon.get_pokemon(pokemon).id)} | {pykemon.get_pokemon_species(pk).generation.name.upper()}**__".replace(
        'GENERATION-', 'Generation ')

  async def pspecies(self, pokemon):
    pokemon = pokemon.split('-', 1)[0]
    pk = pykemon.get_pokemon_species(pokemon)
    return pk.genera[7].genus


  async def entry(self, pokemon):
    pokemon = pokemon.split('-', 1)[0]
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
    pk = f"{str(pk)} m " + f"({ft}' {inch:02d}\")"
    return str(pk)


  async def pweight(self, pokemon):
    pk = pykemon.get_pokemon(pokemon)
    pk = pk.weight
    pk = pk / 10
    lbs = pk * 2.205
    pk = f"{str(pk)} kg " + f'({lbs:0.1f} lbs)'
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
    switcher = {
      "generation-i":1,
      "generation-ii":2,
      "generation-iii":3,
      "generation-iv":4,
      "generation-v":5,
      "generation-vi":6,
      "generation-vii":7,
      "generation-viii":8
    }
    return switcher.get(gen, "nothing")


  async def game(self, game):
    switcher = {
      1:"red",
      2:"gold",
      3:"ruby",
      4:"diamond",
      5:"black",
      6:"x",
      7:"sun",
      8:"sword"
    }
    return switcher.get(game, "nothing")

  async def region(self, gen):
    gen = gen.split('-', 1)[0]
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
    pokemon = f"{pokemon}-"
    pokemon = difflib.get_close_matches(pokemon, lst)[0]
    pokemon = pokemon.split('-', 1)[0]
    pokemon = pykemon.get_pokemon_species(pokemon).name
    pokemon = f"{pokemon}-"
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
    switcher = {
      "Water":"<:water:946555702032367616>",
      "Steel":"<:steel:946555701977825290>",
      "Rock":"<:rock_type:946555701965250630>",
      "Psychic":"<:psychic:946555701814239233>",
      "Poison":"<:poison:946555702078505030>",
      "Normal":"<:normal:946555701742952509>",
      "Ice":"<:ice:946555701608734721>",
      "Ground":"<:ground:946555701805850624>",
      "Grass":"<:grass:946555702011375647>",
      "Ghost":"<:ghost:946555701780676668>",
      "Flying":"<:flying:946555701424177173>",
      "Fire":"<:fire:946555701797457920>",
      "Fighting":"<:fighting:946555701638094899>",
      "Electric":"<:electric:946555701789077514>",
      "Dragon":"<:dragon:946555702133010482>",
      "Bug":"<:bug:946555689613021244>",
      "Fairy":"<:fairy:946555701663252553>",
      "Dark":"<:dark:946555693387907072>"
    }
    return switcher.get(type, "nothing")
    
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
    switcher = {
      1:"HP",
      2:"Atk",
      3:"Def",
      4:"Sp. Atk",
      5:"Sp. Def",
      6:"Spe"
    }
    return switcher.get(stat, "nothing")

  async def gcr(self, pokemon):
    pokemon = pokemon.split('-', 1)[0]
    gcr = pykemon.get_pokemon_species(pokemon)
    growth = f"{gcr.growth_rate.name.title()}/"
    capturerate = str(gcr.capture_rate)
    growth = growth.replace("-", " ")
    return growth + capturerate

  async def gender(self, pokemon):
    pokemon = pokemon.split('-', 1)[0]
    gender = pykemon.get_pokemon_species(pokemon).gender_rate
    return "Genderless" if gender == -1 else f"{str(gender)}/8 ♀️"

  async def egggroup(self, pokemon):
    pokemon = pokemon.split('-', 1)[0]
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
    pokemon = pokemon.split('-', 1)[0]
    hatch = pykemon.get_pokemon_species(pokemon).hatch_counter
    return f'{str(255 * (hatch + 1))} Steps'

def setup(bot):
    Pokemon(bot)
