import json
import time
import sqlite3
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord_slash import SlashContext, cog_ext
from discord_slash.context import ComponentContext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import (create_actionrow,
                                                   create_button)

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
    if isinstance(error, commands.MissingRequiredArgument):
      em = discord.Embed(title="Hey! You're missing arguements!", color=ctx.author.color) 
      await ctx.send(embed=em)
    if isinstance(error, commands.MissingPermissions):
      em = discord.Embed(title="I don't have the right permissions 😢", color=ctx.author.color) 
      await ctx.send(embed=em)
    if isinstance(error, commands.CommandNotFound):
      pass

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
    try:
      conn = sqlite3.connect('config/prefixes.sqlite')
      c = conn.cursor()
      c.execute("UPDATE prefixes SET prefix = ? WHERE guild= ?", (prefix, ctx.guild.id))
      conn.commit()
      conn.close()
      embed = discord.Embed(
          title=f"Prefix set to {prefix}",
          color=discord.Color.from_rgb(236, 180, 61),
      )
      await ctx.send(embed = embed)
    except:
      await ctx.send('Something went wrong!')

  @commands.command(hidden=True)
  async def dm(self, ctx, member: discord.Member, *, content):
    if ctx.author == self.bot.appinfo.owner:
      channel = await member.create_dm()
      await channel.send(content)

  @commands.command()
  @has_permissions(manage_guild=True)
  async def updates(self, ctx):
    """See all recent updates to the bot!"""
    await ctx.message.delete()
    embed=discord.Embed(title="__**Bot Updates**__", color=0x7d1ddd)
    embed.add_field(name="Shiny Command Integrated in Pokedex", value="The `/shinypokedex` command has been integrated into the `/pokedex` command with it now being a choice when in the slash command and an option at the end of the regular command (e.g. >pokemon <pokemon> {back} {shiny})", inline=True)
    await ctx.send(embed=embed)

  async def invitecmd(self, ctx):
    embed = discord.Embed(title = "Invite me to your server!", color = discord.Color.from_rgb(236, 180, 61))
    buttons = [
          create_button(
            style = ButtonStyle.URL, 
            label = "Invite Link", 
            url = "https://discord.com/api/oauth2/authorize?client_id=811673970004721694&permissions=277062478952&scope=bot%20applications.commands"
          )
    ]
    action_row = create_actionrow(*buttons)
    await ctx.send(embed = embed, components = [action_row])

  @commands.command()
  async def invite(self, ctx):
    """
    Sends the bot's invite link
    """
    await Utility.invitecmd(self, ctx)

  @cog_ext.cog_slash(name="Invite", description="Create an Invite for this bot")
  async def slashinvite(self, ctx: SlashContext):
    await Utility.invitecmd(self, ctx)

def setup(bot):
	bot.add_cog(Utility(bot))

