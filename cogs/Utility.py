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

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if isinstance(error, commands.MissingPermissions):
      await ctx.send("Hah you don't have the right permissions for that")
    if isinstance(error, commands.MissingRequiredArgument):
      await ctx.send("Please enter all required arguements.")

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
      description = str(ctx.guild.description)

      owner = str(ctx.guild.owner)
      id = str(ctx.guild.id)
      region = str(ctx.guild.region)
      memberCount = str(ctx.guild.member_count)

      icon = str(ctx.guild.icon_url)

      embed = discord.Embed(
          title=name + " Server Information",
          description=description,
          color=discord.Color.blue()
      )
      embed.set_thumbnail(url=icon)
      embed.add_field(name="Owner", value=owner, inline=True)
      embed.add_field(name="Server ID", value=id, inline=True)
      embed.add_field(name="Region", value=region, inline=True)
      embed.add_field(name="Member Count", value=memberCount, inline=True)
      await ctx.send(embed=embed)


  @commands.command()
  @has_permissions(manage_messages=True)
  async def purge(self, ctx, amount : int):
    """Deletes X amount of messages"""
    await ctx.channel.purge(limit=amount)

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
    embed.add_field(name="Pokemon", value="Pokemon & PokeItem command will get\ncorrect item if spelled incorrectly", inline=True)
    embed.add_field(name = "Minecraft", value = "Search up minecraft players with the 'mc' command")
    embed.set_footer(text="v0.5")
    await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Utility(bot))

