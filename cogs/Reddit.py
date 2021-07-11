import discord
from discord.ext import commands
import asyncpraw
import random

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
client = discord.Client()


class Reddit(commands.Cog):
  """
  smh my head...
  """
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def rslash(self, ctx, sr):
    """Hentai"""
    reddit = asyncpraw.Reddit(client_id='ywFPprh9AzkjrA', client_secret = 'Y49u2M2O6hLtPbUF060F2lyzXVZezg', user_agent = 'Jake the Dog')
    submission = await reddit.subreddit(f'{sr}')
    submission = await submission.random()
    embed = discord.Embed(title = submission.title, color = discord.Color.red())
    embed.set_image(url = submission.url)
    await ctx.send(embed = embed)
    await reddit.close()

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if isinstance(error, commands.errors.NSFWChannelRequired):
       embed = discord.Embed(title = "NSFW Command", description = error.args[0], color = discord.Color.dark_red())
       await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(Reddit(bot))
