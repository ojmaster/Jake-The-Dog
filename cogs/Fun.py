import discord
from discord import guild
from discord.ext import commands
import random
from discord_slash.utils.manage_commands import create_option
from urbandictionary_top import udtop
import  aiohttp
import asyncio
import json
from discord_slash.context import MenuContext, ComponentContext
from discord_slash.model import ContextMenuType, ButtonStyle
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from typing import Union

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
client = discord.Client()

class Fun(commands.Cog):
  """
  Its fun time!
  """
  def __init__(self, bot):
    self.bot = bot

  async def r34(self, ctx):
      await ctx.send('https://rb.gy/tkbdmz')

  @cog_ext.cog_slash(name = "Rule34")
  async def rule34cm(self, ctx: SlashContext):
    await Fun.r34(self, ctx)
 
  @commands.command(name = "rule34")
  async def rule34(self, ctx):
      """Horny Time"""
      await Fun.r34(self, ctx)

  async def slotcmd(self, ctx):
      emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
      a = random.choice(emojis)
      b = random.choice(emojis)
      c = random.choice(emojis)

      slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

      if (a == b == c):
          await ctx.send(f"{slotmachine} All matching, you won! 🎉")
      elif (a == b) or (a == c) or (b == c):
          await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")
      else:
          await ctx.send(f"{slotmachine} No match, you lost 😢")

  @commands.command(aliases=["bet"])
  @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
  async def slots(self ,ctx):
      """Roll the slot machine"""
      await Fun.slotcmd(self, ctx)

  @cog_ext.cog_slash(name = "Slots", description= "Play slots!")
  async def slotslash(self, ctx:SlashContext):
      await Fun.slotcmd(self, ctx)

  @cog_ext.cog_context_menu(target=ContextMenuType.USER, name = "Slots")
  async def slotscm(self, ctx: MenuContext):
    await Fun.slotcmd(self, ctx)

  @cog_ext.cog_slash(name = "8ball", description="Consult the wise 8ball", options=[
                                                                                    create_option(
                                                                                        name = "question",
                                                                                        description = "Your humble question",
                                                                                        option_type = 3,
                                                                                        required= True
                                                                                    )
                                                                                ])
  async def slasheightball(self, ctx: SlashContext, question: str):
    responses = ["As I see it, yes", "Yes", "No", "Very likely", "Not even close", "Maybe", "Very unlikely", "Ur mom told me yes", "Ur mom told me no", "Ask again later", "Better not tell you now", "Concentrate and ask again", "Don't count on it", " It is certain", "My sources say no", "Outlook good", "You may rely on it", "Very Doubtful", "Without a doubt"]
    response = random.choice(responses)
    await ctx.send(content = f'__Question:__ {question} \n__Response:__ {response}')
  
  @commands.command(name="8ball")
  async def eightball(self, ctx, question):
    """Consult the wise master for the answer to your questions"""
    responses = ["As I see it, yes", "Yes", "No", "Very likely", "Not even close", "Maybe", "Very unlikely", "Ur mom told me yes", "Ur mom told me no", "Ask again later", "Better not tell you now", "Concentrate and ask again", "Don't count on it", " It is certain", "My sources say no", "Outlook good", "You may rely on it", "Very Doubtful", "Without a doubt"]
    response = random.choice(responses)
    await ctx.reply(response)

  async def coinflipcmd(self, ctx):
      coinsides = ["Heads", "Tails"]
      await ctx.send(f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!")

  @commands.command(aliases=["flip", "coin"])
  async def coinflip(self, ctx):
      """ Coinflip! """
      await Fun.coinflipcmd(self, ctx)

  @cog_ext.cog_context_menu(target=ContextMenuType.USER, name = "Coin Flip")
  async def coinflipcm(self, ctx: MenuContext):
      await Fun.coinflipcmd(self, ctx)

  @cog_ext.cog_slash(name = "CoinFlip", description = "Flip a coin!")
  async def slashcoinflip(self, ctx: SlashContext):
      await Fun.coinflipcmd(self, ctx)
  
  @commands.command(aliases = ["urbandictionary", "urbandict"])
  async def urban(self, ctx, *, search):
      """ Find the 'best' definition to your words """
      term = udtop(search)
      search = search.capitalize()
      embed = discord.Embed(title = f'__{search}__', description = term, color=discord.Color.purple())
      await ctx.send(embed = embed)

  @cog_ext.cog_slash(name = "UrbanDictionary", description="Find the urban definition of your words", options=[
                                                                                                                create_option(
                                                                                                                    name = "word",
                                                                                                                    description = "Your 'urban' word",
                                                                                                                    option_type = 3,
                                                                                                                    required= True
                                                                                                                )
                                                                                                            ])
  async def slashurban(self, ctx: SlashContext, word: str):
      term = udtop(word)
      search = word.capitalize()
      embed = discord.Embed(title = f'__{search}__', description = term, color=discord.Color.purple())
      await ctx.send(embed = embed)


  @commands.command()
  async def pick(self, ctx, *arg):
    """
    Pick from a list of choices
    """
    choices = list(arg)
    choices.pop(0)
    await ctx.send(f'{random.choice(choices)}')
    return


  async def cog_command_error(self, ctx, error):
      print('Error in {0.command.qualified_name}: {1}'.format(ctx, error))

  def userOnline(self, memberList):
      online = []
      for i in memberList:
          if i.status == discord.Status.online and i.bot == False:
              online.append(i)
      return online


  @commands.command()
  async def countdown(self, ctx):
      '''It's the final countdown'''
      countdown = ['five', 'four', 'three', 'two', 'one']
      for num in countdown:
          await ctx.send('**:{0}:**'.format(num))
          await asyncio.sleep(1)
      await ctx.send('**:ok:** DING DING DING')

  @commands.command(aliases=['cat', 'randomcat'])
  async def neko(self, ctx):
      '''NEEKO NEEKO NEEE'''
      #http://discordpy.readthedocs.io/en/latest/faq.html#what-does-blocking-mean
      async with aiohttp.ClientSession() as cs:
          async with cs.get('http://aws.random.cat/meow') as r:
              res = await r.json()
              emojis = [':cat2: ', ':cat: ', ':heart_eyes_cat: ']
              await ctx.send(random.choice(emojis) + res['file'])

  @commands.command(aliases=['rand'])
  async def random(self, ctx, *arg):
      '''Returns a random number or member'''
      if ctx.invoked_subcommand is None:
          if not arg:
              start = 1
              end = 100
          elif arg[0] == 'choice':
              choices = list(arg)
              choices.pop(0)
              await ctx.send(f':congratulations: The winner is {random.choice(choices)}')
              return
          elif arg[0] == 'user':
              online = self.userOnline(ctx.guild.members)
              randomuser = random.choice(online)
              if ctx.channel.permissions_for(ctx.author).mention_everyone:
                  user = randomuser.mention
              else:
                  user = randomuser.display_name
              await ctx.send(f':congratulations: The winner is {user}')
              return
          elif len(arg) == 1:
              start = 1
              end = int(arg[0])
          elif len(arg) == 2:
              start = int(arg[0])
              end = int(arg[1])
          await ctx.send(f'**:arrows_counterclockwise:** Random number ({start} - {end}): {random.randint(start, end)}')

  @cog_ext.cog_context_menu(target=ContextMenuType.USER, name = "RIP")
  async def ripcm(self, ctx: MenuContext):
      await ctx.send(f'R.I.P. {ctx.target_author.mention}\nhttps://tenor.com/bipRq.gif')

  @commands.command()
  async def rip(self, ctx, member:str):
      """RIP MY GUY"""
      await ctx.send(f'R.I.P. {member}\nhttps://tenor.com/bipRq.gif')

  async def hypecmd(self, ctx):
      hypu = ['https://cdn.discordapp.com/attachments/102817255661772800/219514281136357376/tumblr_nr6ndeEpus1u21ng6o1_540.gif',
              'https://cdn.discordapp.com/attachments/102817255661772800/219518372839161859/tumblr_n1h2afSbCu1ttmhgqo1_500.gif',
              'https://gfycat.com/HairyFloweryBarebirdbat',
              'https://i.imgur.com/PFAQSLA.gif',
              'https://abload.de/img/ezgif-32008219442iq0i.gif',
              'https://i.imgur.com/vOVwq5o.jpg',
              'https://i.imgur.com/Ki12X4j.jpg',
              'https://media.giphy.com/media/b1o4elYH8Tqjm/giphy.gif']
      msg = f':train2: CHOO CHOO {random.choice(hypu)}'
      await ctx.send(msg)

  @commands.command()
  async def hype(self, ctx):
      '''HYPE TRAIN CHOO CHOO'''
      await Fun.hypecmd(self, ctx)

  async def puncmd(self, ctx):
    data = json.load(open('./config/pun.json', encoding = "utf8", errors = 'ignore'))
    emojis = ['😆', '😄', '😂', '😭', '🤣']
    puns = [v for d in data['pun'] for k, v in d.items()]
    msg = f'{random.choice(puns)}'
    pn = await ctx.send(msg)
    await pn.add_reaction(random.choice(emojis))

  @commands.command(aliases=['joke'])
  async def pun(self, ctx):
    '''Because everybody likes bad jokes'''
    await Fun.puncmd(self, ctx)

  @cog_ext.cog_context_menu(target=ContextMenuType.USER, name = "Send a Pun")
  async def puncm(self, ctx: MenuContext):
    await Fun.puncmd(self, ctx)

  async def tordcmd(self, ctx, player):
    embed = discord.Embed(title = "Truth or Dare", color = discord.Color.dark_orange())
    embed.add_field(name = "Truth", value = "🇹")
    embed.add_field(name = "Dare", value = "🇩")
    buttons = [
                  create_button(
                    style = ButtonStyle.blue,
                    label = "Truth",
                    custom_id="truth"
                  ),
                  create_button(
                    style = ButtonStyle.red,
                    label = "Dare",
                    custom_id="dare"
                  )
                ]
    action_row = create_actionrow(*buttons)
    if player != "":
        msg = await ctx.send(content = f'{player.mention}', embed = embed, components = [action_row])
    else:
        msg = await ctx.send(embed = embed, components = [action_row])

    def check(res):
        return ctx.author == res.author and res.channel == ctx.channel

    try: 
      res: ComponentContext = await wait_for_component(ctx.bot, components = [action_row], timeout=7, check = check)
      if res.component_id == 'truth':
          await msg.delete()
          data = json.load(open('./config/tord.json', encoding = "utf8", errors = 'ignore'))
          values = [v for d in data['truth'] for k, v in d.items()]
          truthem = discord.Embed(title = "Truth", description = random.choice(values), color = discord.Color.green())
          await ctx.send(embed = truthem)
      elif res.component_id == 'dare':
          await msg.delete()
          data = json.load(open('./config/tord.json', encoding = "utf8", errors = 'ignore'))
          values = [v for d in data['dare'] for k, v in d.items()]
          dareem = discord.Embed(title = "Dare", description = random.choice(values), color = discord.Color.dark_magenta())
          await ctx.send(embed = dareem)

    except asyncio.TimeoutError:
      embed = discord.Embed(title = 'Took too long to respond', color = discord.Color.dark_red())
      await ctx.send(embed = embed)

  @commands.command(aliases=["TruthOrDare", "truthdare", "td"])
  async def tord(self, ctx, user: discord.Member = ""):
    """Truth or Dare"""
    await Fun.tordcmd(self, ctx, user)

  @cog_ext.cog_context_menu(target=ContextMenuType.USER, name = "Truth or Dare")
  async def tordcm(self, ctx: Union[ComponentContext, MenuContext]):
    await Fun.tordcmd(self, ctx, ctx.target_author)

  @cog_ext.cog_slash(name = "TruthOrDare", description="A fun game of Truth or Dare", options = [
                                                                                                create_option(
                                                                                                    name = "user",
                                                                                                    description = "User to ask",
                                                                                                    option_type = 6,
                                                                                                    required= False
                                                                                                )
                                                                                            ])
  async def slashtord(self, ctx: SlashContext, user = ""):
    await Fun.tordcmd(self, ctx, user)

def setup(bot):
	bot.add_cog(Fun(bot))