import discord
from discord.ext import commands
import asyncpraw
import random

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
client = discord.Client()

reddit = asyncpraw.Reddit(client_id='ywFPprh9AzkjrA', client_secret = 'Y49u2M2O6hLtPbUF060F2lyzXVZezg', user_agent = 'Jake the Dog')

class NSFW(commands.Cog):
  """
  smh my head...
  """
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def kim(self, ctx):
    """Hentai"""
    submission = await reddit.subreddit("hentai")
    submission = await submission.random()
    embed = discord.Embed(title = submission.title, color = discord.Color.red(), url = submission.shortlink)
    embed.set_image(url = submission.url)
    await ctx.send(embed = embed)


def setup(bot):
	bot.add_cog(NSFW(bot))
