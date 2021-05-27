import discord
from discord.ext import commands
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
    if ctx.author == self.bot.appinfo.owner or ctx.author.id == 534232070487146517:
      embed = discord.Embed(title = "What would you like to change the presence to?", color = discord.Color.gold())
      embed.add_field(name = "Watching", value = ":one:", inline = True)
      embed.add_field(name = "⠀", value = "⠀")
      embed.add_field(name = "Listening", value = ":two:", inline = True)
      embed.add_field(name = "Streaming", value = ":three:", inline = True)
      embed.add_field(name = "⠀", value = "⠀")
      embed.add_field(name = "Playing", value = ":four:", inline = True)
      msg = await ctx.send(embed = embed)
      await msg.add_reaction("1️⃣")
      await msg.add_reaction("2️⃣")
      await msg.add_reaction("3️⃣")
      await msg.add_reaction("4️⃣")

      def check(reaction, user):
        return user == ctx.message.author and str(reaction.emoji) in ['1️⃣', '2️⃣', '3️⃣', '4️⃣']

      try: 
        reaction, user = await self.bot.wait_for('reaction_add', timeout = 7, check = check)
        if reaction.emoji == '1️⃣':
          watch = discord.Embed(title = "What am I watching?", color = discord.Color.dark_red())
          await msg.delete()
          msg = await ctx.send(embed = watch)
          presence = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
          presence = (presence.content)
          await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=presence))
          watch = discord.Embed(title = f'Watching {presence}', color = discord.Color.red())
          await msg.delete()
          await ctx.send(embed = watch) 
        elif reaction.emoji == '2️⃣':
          listen = discord.Embed(title = "What am I listening to?", color = discord.Color.dark_green())
          await msg.delete()
          msg = await ctx.send(embed = listen)
          presence = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
          presence = (presence.content)
          await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=presence))
          listen = discord.Embed(title = f'Listening to {presence}', color = discord.Color.dark_green())
          await msg.delete()
          await ctx.send(embed = listen) 
        elif reaction.emoji == '3️⃣':
          stream = discord.Embed(title = "What is the title of the stream?", color = discord.Color.dark_purple())
          await msg.delete()
          msg = await ctx.send(embed = stream)
          presence = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
          presence = (presence.content)
          stream = discord.Embed(title = "What is the link to the stream?", color = discord.Color.dark_purple())
          await msg.delete()
          msg = await ctx.send(embed = stream)
          slink = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
          slink = (slink.content)
          stream = discord.Embed(title = f'Sreaming {presence} with link {slink}', color = discord.Color.dark_purple())
          await msg.delete()
          await self.bot.change_presence(activity=discord.Streaming(name=presence, url=slink))
          await ctx.send(embed = stream)
        elif reaction.emoji == '4️⃣':
          play = discord.Embed(title = "What am I playing?", color = discord.Color.dark_blue())
          await msg.delete()
          msg = await ctx.send(embed = play)
          presence = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
          presence = (presence.content)
          await self.bot.change_presence(activity=discord.Game(name=presence))
          play = discord.Embed(title = f'Playing {presence}', color = discord.Color.dark_green())
          await msg.delete()
          await ctx.send(embed = play) 

      except asyncio.TimeoutError:
        embed = discord.Embed(title = 'Took too long to respond', color = discord.Color.dark_red())
        await ctx.send(embed = embed)


def setup(bot):
	bot.add_cog(Owner(bot))