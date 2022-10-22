import json
import time
import sqlite3
import interactions
from interactions import CommandContext, ComponentContext

class Utility(interactions.Extension):
  """
  Find out more about the bot
  """
  def __init__(self, bot):
    self.bot = bot


  @interactions.extension_command(name = "ping", description = "Pong!", scope = [651230389171650560])
  async def ping(self, ctx):
    """Pong!"""
    await ctx.get_channel()
    time_1 = time.perf_counter()
    await ctx.trigger_typing()
    time_2 = time.perf_counter()
    ping = round((time_2-time_1)*1000)
    await ctx.send(f"Ping = {ping} ms")


  @interactions.extension_command(name = "serverinfo", description= "Info about your server", scope = [651230389171650560])
  async def serverinfo(self, ctx: CommandContext):
      await ctx.get_guild()
      embed = interactions.Embed(
          title = ctx.guild.name,
          color = interactions.Color.black(),
          thumbnail = interactions.EmbedImageStruct(url= ctx.guild.icon_url)
      )
      owner = await interactions.get(bot, interactions.User, object_id = ctx.guild.owner_id)
      embed.add_field(name = "Owner", value=f"{owner.username}#{owner.discriminator}", inline = True)
      embed.add_field(name = "Members", value = ctx.guild.member_count, inline= True)
      embed.add_field(name = "Region", value = ctx.guild.region, inline = True)
      embed.set_footer(text = f"ID: {int(ctx.guild.id)}")
      await ctx.send(embeds = embed)


#  @commands.command()
#  @has_permissions(manage_guild = True)
#  async def setprefix(self, ctx, prefix):
#    """Sets bot prefix for server"""
#    try:
#      conn = sqlite3.connect('config/prefixes.sqlite')
#      c = conn.cursor()
#      c.execute("UPDATE prefixes SET prefix = ? WHERE guild= ?", (prefix, ctx.guild.id))
#      conn.commit()
#      conn.close()
#      embed = discord.Embed(
#          title=f"Prefix set to {prefix}",
#          color=discord.Color.from_rgb(236, 180, 61),
#      )
#      await ctx.send(embed = embed)
#    except:
#      await ctx.send('Something went wrong!')
#
#
#  @commands.command(hidden=True)
#  async def dm(self, ctx, member: discord.Member, *, content):
#    if ctx.author == self.bot.appinfo.owner:
#      channel = await member.create_dm()
#      await channel.send(content)
#
#  @commands.command()
#  @has_permissions(manage_guild=True)
#  async def updates(self, ctx):
#    """See all recent updates to the bot!"""
#    await ctx.message.delete()
#    embed=discord.Embed(title="__**Bot Updates**__", color=0x7d1ddd)
#    embed.add_field(name="Shiny Command Integrated in Pokedex", value="The `/shinypokedex` command has been integrated into the `/pokedex` command with it now being a choice when in the slash command and an option at the end of the regular command (e.g. >pokemon <pokemon> {back} {shiny})", inline=True)
#    await ctx.send(embed=embed)
#
#  async def invitecmd(self, ctx):
#    embed = discord.Embed(title = "Invite me to your server!", color = discord.Color.from_rgb(236, 180, 61))
#    buttons = [
#          create_button(
#            style = ButtonStyle.URL, 
#            label = "Invite Link", 
#            url = "https://discord.com/api/oauth2/authorize?client_id=811673970004721694&permissions=277062478952&scope=bot%20applications.commands"
#          )
#    ]
#    action_row = create_actionrow(*buttons)
#    await ctx.send(embed = embed, components = [action_row])
#
#  @commands.command()
#  async def invite(self, ctx):
#    """
#    Sends the bot's invite link
#    """
#    await Utility.invitecmd(self, ctx)
#
#  @cog_ext.cog_slash(name="Invite", description="Create an Invite for this bot")
#  async def slashinvite(self, ctx: SlashContext):
#    await Utility.invitecmd(self, ctx)

def setup(bot):
    Utility(bot)


