import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle
import asyncio

import time

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
    if ctx.author == self.bot.appinfo.owner:
      embed = discord.Embed(title = "What would you like to change the presence to?", color = discord.Color.gold())
      embed.add_field(name = "Watching", value = ":one:", inline = True)
      embed.add_field(name = "Listening", value = ":two:", inline = True)
      embed.add_field(name = "Streaming", value = ":three:", inline = True)
      embed.add_field(name = "Playing", value = ":four:", inline = True)
      embed.add_field(name = "Competing", value = ":five:")
      components = [
                    [
                      Button(style = ButtonStyle.gray, label = "Watching"), 
                      Button(style = ButtonStyle.green, label = "Listening"),
                      Button(style = ButtonStyle.blue, label = "Streaming"),
                      Button(style = ButtonStyle.red, label = "Playing"),
                      Button(style = ButtonStyle.gray, label = "Competing")
                    ]
                  ]
      msg = await ctx.send(embed = embed, components = components)

      # Basic check for user
      def check(res):
          return ctx.author == res.user and res.channel == ctx.channel

      # Responses
      try: 
        res = await self.bot.wait_for('button_click', timeout = 7, check = check)
        if res.component.label == 'Watching':
          watch = discord.Embed(title = "What am I watching?", color = discord.Color.dark_red())
          await msg.delete()
          msg = await ctx.send(embed = watch)
          presence = await self.bot.wait_for('message')
          presence = (presence.content)
          await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=presence))
          watch = discord.Embed(title = f'Watching {presence}', color = discord.Color.red())
          await msg.delete()
          await ctx.send(embed = watch) 
        elif res.component.label == 'Listening':
          listen = discord.Embed(title = "What am I listening to?", color = discord.Color.dark_green())
          await msg.delete()
          msg = await ctx.send(embed = listen)
          presence = await self.bot.wait_for('message')
          presence = (presence.content)
          await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=presence))
          listen = discord.Embed(title = f'Listening to {presence}', color = discord.Color.dark_green())
          await msg.delete()
          await ctx.send(embed = listen) 
        elif res.component.label == 'Streaming':
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
        elif res.component.label == 'Playing':
          play = discord.Embed(title = "What am I playing?", color = discord.Color.dark_blue())
          await msg.delete()
          msg = await ctx.send(embed = play)
          presence = await self.bot.wait_for('message')
          presence = (presence.content)
          await self.bot.change_presence(activity=discord.Game(name=presence))
          play = discord.Embed(title = f'Playing {presence}', color = discord.Color.dark_green())
          await msg.delete()
          await ctx.send(embed = play) 
        elif res.component.label == 'Competing':
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