import discord
from discord.ext import commands
import time
import json
from discord.ext.commands import has_permissions

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
client = discord.Client()

class Utility(commands.Cog):
  """
  Find out more about the bot
  """
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def ping(self, ctx):
    """Pong!"""
    time_1 = time.perf_counter()
    await ctx.trigger_typing()
    time_2 = time.perf_counter()
    ping = round((time_2-time_1)*1000)
    await ctx.send(f"Ping = {ping} ms")

  @commands.command()
  async def server(self, ctx):
      """Shows info about the server"""
      name = str(ctx.guild.name)
      owner = str(ctx.guild.owner)
      id = str(ctx.guild.id)
      region = str(ctx.guild.region)
      memberCount = str(ctx.guild.member_count)

      icon = str(ctx.guild.icon_url)

      embed = discord.Embed(
          title=name + " Server Information",
          color=discord.Color.blue()
      )
      embed.set_thumbnail(url=icon)
      embed.add_field(name="Owner", value=owner, inline=True)
      embed.add_field(name="Server ID", value=id, inline=True)
      embed.add_field(name="Region", value=region, inline=True)
      embed.add_field(name="Member Count", value=memberCount, inline=True)
      await ctx.send(embed=embed)

  @commands.command()
  @has_permissions(manage_guild = True)
  async def setprefix(self, ctx, prefix):
    """Sets bot prefix for server"""
    with open('prefixes.json', 'r') as pr:
      prefixes = json.load(pr)
    prefixes[str(ctx.guild.id)] = prefix
    with open('prefixes.json', 'w') as pr:
      json.dump(prefixes, pr, indent = 4)
    await ctx.send(f'Prefix changed to: {prefix}')
    return prefix

  @commands.command(hidden=True)
  @has_permissions(manage_guild=True)
  async def dm(self, ctx, member: discord.Member, *, content):
      channel = await member.create_dm()
      await channel.send(content)

  @commands.command()
  @has_permissions(manage_guild=True)
  async def updates(self, ctx):
    """See all recent updates to the bot!"""
    embed=discord.Embed(title="__**Bot Updates**__", color=0x7d1ddd)
    embed.add_field(name="Entertainment", value="`activities` - An early beta Discord feature that allows you to play games with friends through a Discord server vc and watch Youtube videos together. \nNOTE: This only works on desktop versions as it has not been implemented in mobile", inline=True)
    embed.set_footer(text="v1.0.8")
    await ctx.send(embed=embed)

  @commands.command()
  async def invite(self, ctx):
      """
      Sends the bot's invite link
      """
      await ctx.send("https://discord.com/api/oauth2/authorize?client_id=811673970004721694&permissions=2146954879&scope=bot")


def setup(bot):
	bot.add_cog(Utility(bot))

