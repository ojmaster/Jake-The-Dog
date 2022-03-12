import asyncio
import time

import discord
from discord.ext import commands
from discord_slash.context import ComponentContext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import (create_actionrow,
                                                   create_button,
                                                   wait_for_component)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
client = discord.Client()

class Owner(commands.Cog):
  """
  Bot Owner Commands
  """
  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=['cp'])
  async def changepresence(self, ctx):
    """
    Change Bot Presence
    """
    # Check if user is bot owner
    # Send list embed if true
    if ctx.author == self.bot.appinfo.owner or ctx.author.id == 762193946407338044:
      embed = discord.Embed(title = "What would you like to change the presence to?", color = discord.Color.gold())
      embed.add_field(name = "Watching", value = ":one:", inline = True)
      embed.add_field(name = "Listening", value = ":two:", inline = True)
      embed.add_field(name = "Streaming", value = ":three:", inline = True)
      embed.add_field(name = "Playing", value = ":four:", inline = True)
      embed.add_field(name = "Competing", value = ":five:")
      buttons = [
                  create_button(style = ButtonStyle.gray, label = "Watching", custom_id = "watching"), 
                  create_button(style = ButtonStyle.green, label = "Listening", custom_id = "listening"),
                  create_button(style = ButtonStyle.blue, label = "Streaming", custom_id = "streaming"),
                  create_button(style = ButtonStyle.red, label = "Playing", custom_id = "playing"),
                  create_button(style = ButtonStyle.gray, label = "Competing", custom_id = "competing")
                ]
      action_row = create_actionrow(*buttons)
      msg = await ctx.send(embed = embed, components = [action_row])

      # Basic check for user
      def check(res):
          return ctx.author == res.author and res.channel == ctx.channel

      # Responses
      try: 
        res: ComponentContext = await wait_for_component(ctx.bot, components = [action_row], timeout=7, check = check)
        if res.component_id == 'watching':
          watch = discord.Embed(title = "What am I watching?", color = discord.Color.dark_red())
          await msg.delete()
          msg = await ctx.send(embed = watch)
          presence = await self.bot.wait_for('message')
          presence = (presence.content)
          await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=presence))
          watch = discord.Embed(title = f'Watching {presence}', color = discord.Color.red())
          await msg.delete()
          await ctx.send(embed = watch) 
        elif res.component_id == 'listening':
          listen = discord.Embed(title = "What am I listening to?", color = discord.Color.dark_green())
          await msg.delete()
          msg = await ctx.send(embed = listen)
          presence = await self.bot.wait_for('message')
          presence = (presence.content)
          await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=presence))
          listen = discord.Embed(title = f'Listening to {presence}', color = discord.Color.dark_green())
          await msg.delete()
          await ctx.send(embed = listen) 
        elif res.component_id == 'streaming':
          stream = discord.Embed(title = "What is the title of the stream?", color = discord.Color.dark_purple())
          await msg.delete()
          msg = await ctx.send(embed = stream)
          presence = await self.bot.wait_for('message')
          presence = (presence.content)
          stream = discord.Embed(title = "What is the link to the stream?", color = discord.Color.dark_purple())
          await msg.delete()
          msg = await ctx.send(embed = stream)
          slink = await self.bot.wait_for('message')
          slink = (slink.content)
          stream = discord.Embed(title = f'Sreaming {presence} with link {slink}', color = discord.Color.dark_purple())
          await msg.delete()
          await self.bot.change_presence(activity=discord.Streaming(name=presence, url=slink))
          await ctx.send(embed = stream)
        elif res.component_id == 'playing':
          play = discord.Embed(title = "What am I playing?", color = discord.Color.dark_blue())
          await msg.delete()
          msg = await ctx.send(embed = play)
          presence = await self.bot.wait_for('message')
          presence = (presence.content)
          await self.bot.change_presence(activity=discord.Game(name=presence))
          play = discord.Embed(title = f'Playing {presence}', color = discord.Color.dark_green())
          await msg.delete()
          await ctx.send(embed = play) 
        elif res.component_id == 'competing':
          compete = discord.Embed(title = "What am I competing in?", color = discord.Color.orange())
          await msg.delete()
          msg = await ctx.send(embed = compete)
          presence = await self.bot.wait_for('message')
          presence = (presence.content)
          await self.bot.change_presence(activity=discord.Activity(type=5,name=presence))
          compete = discord.Embed(title = f'Competing in {presence}', color = discord.Color.orange())
          await msg.delete()
          await ctx.send(embed = compete) 

      except asyncio.TimeoutError:
        embed = discord.Embed(title = 'Took too long to respond', color = discord.Color.dark_red())
        await ctx.send(embed = embed)


def setup(bot):
	bot.add_cog(Owner(bot))
