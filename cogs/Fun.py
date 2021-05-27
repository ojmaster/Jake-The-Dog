import discord
from discord.ext import commands
import random
from urbandictionary_top import udtop
import  aiohttp
import asyncio
import json, asyncpraw

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
client = discord.Client()

class Fun(commands.Cog):
  """
  Its fun time!
  """
  def __init__(self, bot):
    self.bot = bot


  @commands.command()
  async def rule34(self, ctx):
    """Horny Time"""
    await ctx.send('https://rb.gy/tkbdmz')

  @commands.command(aliases=["bet"])
  @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
  async def slot(self, ctx):
      """ Roll the slot machine """
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

  @commands.command(name="8ball")
  async def eightball(self, ctx, question):
    """Consult the wise master for the answer to your questions"""
    responses = ["As I see it, yes", "Yes", "No", "Very likely", "Not even close", "Maybe", "Very unlikely", "Ur mom told me yes", "Ur mom told me no", "Ask again later", "Better not tell you now", "Concentrate and ask again", "Don't count on it", " It is certain", "My sources say no", "Outlook good", "You may rely on it", "Very Doubtful", "Without a doubt"]
    response = random.choice(responses)
    await ctx.send(response)

  @commands.command(aliases=["flip", "coin"])
  async def coinflip(self, ctx):
      """ Coinflip! """
      coinsides = ["Heads", "Tails"]
      await ctx.send(f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!")
  
  @commands.command()
  async def urban(self, ctx, *, search):
      """ Find the 'best' definition to your words """
      term = udtop(search)
      search = search.capitalize()
      embed = discord.Embed(title = f'__{search}__', description = term, color=discord.Color.purple())
      await ctx.send(embed = embed)


  @commands.command()
  async def pick(self, ctx, *arg):
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
  async def praise(self, ctx):
      '''Praise the Sun'''
      await ctx.send('https://i.imgur.com/K8ySn3e.gif')

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
      reddit = asyncpraw.Reddit(client_id='ywFPprh9AzkjrA', client_secret = 'Y49u2M2O6hLtPbUF060F2lyzXVZezg', user_agent = 'Jake the Dog')
      submission = await reddit.subreddit("catpics")
      submission = await submission.random()
      embed = discord.Embed(title = submission.title, color = discord.Color.red(), url = submission.shortlink)
      embed.set_image(url = submission.url)
      await ctx.send(embed = embed)
      await reddit.close()

  @commands.command()
  async def rip(self, ctx, member:str):
      '''Rest in Peace'''
      await ctx.send(f'R.I.P. {member}\nhttps://tenor.com/bipRq.gif')

  @commands.command(aliases=['hypu', 'train'])
  async def hype(self, ctx):
      '''HYPE TRAIN CHOO CHOO'''
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


  @commands.command(aliases=['joke'])
  async def pun(self, ctx):
      '''Because everybody likes bad jokes'''
      puns = ['How do you throw a space party? \nYou planet.',
              'I would avoid the sushi if I was you. \nIt’s a little fishy.',
              'Want to hear a joke about paper? \nNevermind it’s tearable.',
              'Did you hear about the guy who lost the left side of his body? \nHe\'s alright now.',
              'My cat was just sick on the carpet, \nI don’t think it’s feline well.',
              'Towels can’t tell jokes. \nThey have a dry sense of humor.',
              'To write with a broken pencil is pointless.',
              'I went to a seafood disco last week... and pulled a mussel.',
              'What do beavers like to put on their salads? \nBranch dressing.',
              'How did the farmer find his wife? \nHe tractor down.',
              'Why are ambulance drivers called paramedics? \nBecause that\'s what they are, a pair-of-medics.',
              'A friend of mine runs a funeral home.\nPeople are dying to go there.',
              'My friend Tony asked me not to say his name backwards.\nI said, "Y not?"',
              'To the person who stole my MS Office License.\nI will find you. You have my Word.',
              'What’s brown and sticky? \nA stick.',
              'How do celebrities stay cool? \nThey have many fans.']
      emojis = ['😆', '😄', '😂', '😭', '🤣']
      msg = f'{random.choice(puns)}'
      pn = await ctx.send(msg)
      await pn.add_reaction(random.choice(emojis))

  @commands.command()
  async def tord(self, ctx):
    """Truth or Dare"""
    embed = discord.Embed(title = "Truth or Dare", color = discord.Color.dark_orange())
    embed.add_field(name = "Truth", value = "🇹")
    embed.add_field(name = "Dare", value = "🇩")
    msg = await ctx.send(embed = embed)
    await msg.add_reaction("🇹")
    await msg.add_reaction("🇩")

    def check(reaction, user):
      return user == ctx.message.author and str(reaction.emoji) in ['🇹', '🇩']

    try: 
      reaction, user = await self.bot.wait_for('reaction_add', timeout = 7, check = check)
      if reaction.emoji == "🇹":
          await msg.delete()
          data = json.load(open('./cogs/TruthOrDare/truth.json', encoding = "utf8", errors = 'ignore'))
          values = [v for d in data['truth'] for k, v in d.items()]
          truthem = discord.Embed(title = "Truth", description = random.choice(values), color = discord.Color.green())
          await ctx.send(embed = truthem)
      if reaction.emoji == "🇩":
          await msg.delete()
          data = json.load(open('./cogs/TruthOrDare/dare.json', encoding = "utf8", errors = 'ignore'))
          values = [v for d in data['dare'] for k, v in d.items()]
          dareem = discord.Embed(title = "Dare", description = random.choice(values), color = discord.Color.dark_magenta())
          await ctx.send(embed = dareem)

    except asyncio.TimeoutError:
      embed = discord.Embed(title = 'Took too long to respond', color = discord.Color.dark_red())
      await ctx.send(embed = embed)

def setup(bot):
	bot.add_cog(Fun(bot))