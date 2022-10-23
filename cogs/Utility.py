#import json
#import sqlite3
import interactions
from interactions import CommandContext
class Utility(interactions.Extension):
  """
  Find out more about the bot
  """

  def __init__(self, bot: interactions.Client):
      self.bot: interactions.Client = bot


  @interactions.extension_command(name = "serverinfo", description= "Info about your server")
  async def serverinfo(self, ctx: CommandContext):
      await ctx.get_guild()
      embed = interactions.Embed(
          title = ctx.guild.name,
          color = interactions.Color.black(),
          thumbnail = interactions.EmbedImageStruct(url= ctx.guild.icon_url)
      )
      text_channels = 0
      voice_channels = 0
      for channel in ctx.guild.channels:
        if channel.type == interactions.ChannelType.GUILD_TEXT:
          text_channels+=1
        if channel.type == interactions.ChannelType.GUILD_VOICE:
          voice_channels+=1 
      owner = await interactions.get(self.client, interactions.User, object_id = ctx.guild.owner_id)
      embed.add_field(name = "Owner", value=f"{owner.username}#{owner.discriminator}", inline = True)
      embed.add_field(name = "Members", value = ctx.guild.member_count, inline= True)
      embed.add_field(name = "Region", value = ctx.guild.region, inline = True)
      embed.add_field(name = "Text Channels", value = text_channels, inline = True)
      embed.add_field(name = "Voice Channels", value = voice_channels, inline = True)
      embed.add_field(name = "Roles", value = len(ctx.guild.roles), inline = True)
      embed.set_footer(text = f"**ID**: {int(ctx.guild.id)}")
      await ctx.send(embeds = embed)


  @interactions.extension_command(name = "invite", description = "My invite link")
  async def invitecmd(self, ctx):
    embed = interactions.Embed(title = "Invite me to your server!", description= "I am also available to find in the new App Directory!", color = 0xecb53d)
    button = interactions.Button(
                style = interactions.ButtonStyle.LINK, 
                label = "Invite Link", 
                url = "https://discord.com/api/oauth2/authorize?client_id=811673970004721694&permissions=277062478952&scope=bot%20applications.commands"
              )
    action_row = interactions.ActionRow(components = [button])
    await ctx.send(embeds = embed, components = [action_row])


def setup(bot):
    Utility(bot)


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