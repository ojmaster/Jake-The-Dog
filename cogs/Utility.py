import discord
from discord.ext import commands
import time
import json
from discord_components import  Button, ButtonStyle
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
    with open('prefixes.json', 'r') as pr:
      prefixes = json.load(pr)
    prefixes[str(ctx.guild.id)] = prefix
    with open('prefixes.json', 'w') as pr:
      json.dump(prefixes, pr, indent = 4)
    await ctx.send(f'Prefix changed to: {prefix}')
    return prefix

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
    embed.add_field(name="Context Menus!", value="Right click a user and navigate to the **Apps** tab, there you can find a few fun commands to use!", inline=True)
    embed.add_field(name = "Slash Commands", value = "Starting to slowly add slash commands! Look forward to them!", inline = False)
    await ctx.send(embed=embed)

  @commands.command()
  async def invite(self, ctx):
      """
      Sends the bot's invite link
      """
      embed = discord.Embed(title = "Invite me to your server!", color = discord.Color.from_rgb(236, 180, 61))
      await ctx.send(embed = embed, components = [
                [
                  Button(style = ButtonStyle.URL, label = "Invite Link", url = "https://discord.com/api/oauth2/authorize?client_id=811673970004721694&permissions=261992349303&scope=bot%20applications.commands")
                ]
          ]
      )
      
  @commands.command(hidden = True)
  async def mass(self, ctx):
      embed = discord.Embed(title = "Announcement!", color = discord.Color.dark_purple())
      embed.add_field(name = "Attention Server Owners!", value = "Hey all, I have some new features such as slash commands (wip) and context menus. Unfortunately in order for these features to work, you will need to reinvite me to the server!\nAttached in the button is my invite link, you don't need to kick me.\nYou can find out my new features with the `updates` command!")
      embed.set_footer(text = "Apologies if this was sent multiple times, a check for if you are owner of multiple servers was not made don't hate me")
      for guild in self.bot.guilds:
        for member in guild.members:
          if member.id == guild.owner_id and member.id != 649337844074020866 and member.id != 455788606838013963 and member.id != 215170188847480832:
            channel = await member.create_dm()
            await channel.send(embed = embed, components = [
                [
                  Button(style = ButtonStyle.URL, label = "Invite Link", url = "https://discord.com/api/oauth2/authorize?client_id=811673970004721694&permissions=261992349303&scope=bot%20applications.commands")
                ]
              ]
            )

def setup(bot):
	bot.add_cog(Utility(bot))

