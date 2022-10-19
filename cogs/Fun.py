import asyncio
from code import interact
import json
import random
from logging import error
from typing import Union

from urllib.request import urlopen
import interactions
from interactions import CommandContext, ComponentContext, Guild
from urbandictionary_top import udtop

class Fun(interactions.Extension):
    """
    Its fun time!
    """

    def __init__(self, bot: interactions.Client):
        self.bot: interactions.Client = bot

    @interactions.extension_command(description="Bonk", scope = [651230389171650560])
    async def bonk(self, ctx: CommandContext):
        await ctx.get_channel()
        embed = interactions.Embed(title="", color = 0x00008B)
        embed.set_image(url="https://rb.gy/tkbdmz")
        embed.set_footer(text=f"Bonk by: {ctx.user.username}")
        await ctx.send(embeds = embed)


    async def slotcmd(self, ctx):
        await ctx.get_channel()
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.user.username}**,"

        if (a == b == c):
            await ctx.send(f"{slotmachine} All matching, you won! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")
        else:
            await ctx.send(f"{slotmachine} No match, you lost 😢")

    @interactions.extension_command(description = "Slots", scope = [651230389171650560])
    async def slots(self, ctx: CommandContext):
        await self.slotcmd(ctx)

    @interactions.extension_user_command(name = "Slots", scope = [651230389171650560])
    async def slotscm(self, ctx):
        await self.slotcmd(ctx)

    
    @interactions.extension_command(name = "8ball", description = "Let the wisdowm of the 8ball give you the answers you seek", scope = [651230389171650560], options = [interactions.Option(
                                                                                            type = interactions.OptionType.STRING,
                                                                                            name = "question",
                                                                                            description = "Your humble question",
                                                                                            required = True
                                                                                            )])
    async def eigthball(self, ctx: CommandContext, question):
        await ctx.get_channel()
        data = json.load(
            open('./config/choices.json', encoding="utf8", errors='ignore'))
        responses = [v for d in data['eightball'] for k, v in d.items()]
        msg = f'{random.choice(responses)}'
        await ctx.send(content=f'__Question:__ {question} \n__Response:__ {msg}')
        
    
    @interactions.extension_command(name = "coinflip", description = "Flip a coin", scope = [651230389171650560])
    async def coinflip(self, ctx: CommandContext):
        await ctx.get_channel()
        coinsides = ["Heads", "Tails"]
        await ctx.send(f"**{ctx.user.username}** flipped a coin and got **{random.choice(coinsides)}**!")

    @interactions.extension_user_command(name = "Coinflip", scope = [651230389171650560])
    async def coinflipcm(self, ctx: ComponentContext):
        coinsides = ["Heads", "Tails"]
        await ctx.send(f"**{ctx.user.username}** flipped a coin and got **{random.choice(coinsides)}**!")


    @interactions.extension_command(name = "urbandictionary", description = "Look up the urban diction of your word", scope = [651230389171650560],  options = [interactions.Option(
                                                                                                                                    type = interactions.OptionType.STRING,
                                                                                                                                    name = "search",
                                                                                                                                    description = "Word to search",
                                                                                                                                    required = True
                                                                                                                                )])
    async def urban(self, ctx, search):
        await ctx.get_channel()
        term = udtop(search)
        embed = interactions.Embed(
            title=f'__{search.capitalize()}__', description=str(term).replace("Example:", "__Example:__"), color=interactions.Color.blurple())
        await ctx.send(embed=embed)

    @interactions.extension_command(name = "choose", description = "Pick from a list of choices", scope = [651230389171650560])
    @interactions.option(name = "option", required = True, type = interactions.OptionType.STRING)
    @interactions.option(name = "option2", required = True, type = interactions.OptionType.STRING)
    @interactions.option(name = "option3", required = False, type = interactions.OptionType.STRING)
    @interactions.option(name = "option4", required = False, type = interactions.OptionType.STRING)
    @interactions.option(name = "option5", required = False, type = interactions.OptionType.STRING)
    @interactions.option(name = "option6", required = False, type = interactions.OptionType.STRING)
    @interactions.option(name = "option7", required = False, type = interactions.OptionType.STRING)
    @interactions.option(name = "option8", required = False, type = interactions.OptionType.STRING)
    async def pick(self, ctx: CommandContext, option, option2, option3 = None, option4 = None, option5 = None, option6 = None, option7 = None, option8 = None):
        await ctx.get_channel()
        options = [option, option2, option3, option4, option5, option6, option7, option8]
        options = [x for x in options if x is not None]
        await ctx.send(f'{random.choice(options)}')
        

    @interactions.extension_command(name = "countdown", description = "Set a timer in seconds", scope = [651230389171650560], options = [interactions.Option(
                                                                                                        name = "seconds",
                                                                                                        description = "Time in seconds", 
                                                                                                        type = interactions.OptionType.INTEGER, 
                                                                                                        required = True)])
    async def countdown(self, ctx: CommandContext, seconds: int):
        '''Set a timer in seconds'''
        await ctx.get_channel()
        mins, sec = divmod(seconds, 60)
        timer = '{:02d}:{:02d}'.format(mins, sec)
        count = await ctx.send(f"`{timer}`")
        while seconds >= 0:
            mins, sec = divmod(seconds, 60)
            timer = '{:02d}:{:02d}'.format(mins, sec)
            await count.edit(content = f"`{timer}`")
            await asyncio.sleep(1)
            seconds -= 1
        await ctx.edit(f"{ctx.user.mention}\n**DING DING DING :alarm_clock:**")

#    @interactions.extension_user_command(name="RIP", scope = [651230389171650560])
#    async def ripcm(self, ctx: ComponentContext):
#        await ctx.send(f'R.I.P. {ctx.target.mention}\nhttps://tenor.com/bipRq.gif')
#
#    @commands.command()
#    async def rip(self, ctx, member: str):
#        """RIP MY GUY"""
#        await ctx.send(f'R.I.P. {member}\nhttps://tenor.com/bipRq.gif')
#
#    async def hypecmd(self, ctx):
#        hypu = ['https://cdn.discordapp.com/attachments/102817255661772800/219514281136357376/tumblr_nr6ndeEpus1u21ng6o1_540.gif',
#                'https://cdn.discordapp.com/attachments/102817255661772800/219518372839161859/tumblr_n1h2afSbCu1ttmhgqo1_500.gif',
#                'https://gfycat.com/HairyFloweryBarebirdbat',
#                'https://i.imgur.com/PFAQSLA.gif',
#                'https://abload.de/img/ezgif-32008219442iq0i.gif',
#                'https://i.imgur.com/vOVwq5o.jpg',
#                'https://i.imgur.com/Ki12X4j.jpg',
#                'https://media.giphy.com/media/b1o4elYH8Tqjm/giphy.gif']
#        msg = f':train2: CHOO CHOO {random.choice(hypu)}'
#        await ctx.send(msg)
#
#    @commands.command()
#    async def hype(self, ctx):
#        '''HYPE TRAIN CHOO CHOO'''
#        await Fun.hypecmd(self, ctx)
#
#    async def puncmd(self, ctx):
#        data = json.load(
#            open('./config/choices.json', encoding="utf8", errors='ignore'))
#        emojis = ['😆', '😄', '😂', '😭', '🤣']
#        url = "https://raw.githubusercontent.com/dabbers/OPun/main/data.json"
#        response = urlopen(url)
#        data_json = json.loads(response.read())["data"]["posts"]
#        pn = await ctx.send(random.choice(data_json)["plaintext"])
#        await pn.add_reaction(random.choice(emojis))
#
#    @commands.command(aliases=['joke'])
#    async def pun(self, ctx):
#        '''Because everybody likes bad jokes'''
#        await Fun.puncmd(self, ctx)
#
#    @cog_ext.cog_context_menu(target=ContextMenuType.USER, name="Send a Pun")
#    async def puncm(self, ctx: MenuContext):
#        await Fun.puncmd(self, ctx)
#
#    @cog_ext.cog_slash(name="Pun", description="Send a Pun")
#    async def slashpun(self, ctx: SlashContext):
#        await Fun.puncmd(self, ctx)
#
#    async def tordcmd(self, ctx, player):
#        embed = discord.Embed(title="Truth or Dare",
#                              color=discord.Color.dark_orange())
#        embed.add_field(name="Truth", value="🇹")
#        embed.add_field(name="Dare", value="🇩")
#        buttons = [
#            create_button(
#                style=ButtonStyle.blue,
#                label="Truth",
#                custom_id="truth"
#            ),
#            create_button(
#                style=ButtonStyle.red,
#                label="Dare",
#                custom_id="dare"
#            )
#        ]
#        action_row = create_actionrow(*buttons)
#        if player != "":
#            msg = await ctx.send(content=f'{player.mention}', embed=embed, components=[action_row])
#        else:
#            msg = await ctx.send(embed=embed, components=[action_row])
#
#        try:
#            res: ComponentContext = await wait_for_component(ctx.bot, components=[action_row], timeout=15)
#            await msg.delete()
#            data = json.load(
#                open('./config/choices.json', encoding="utf8", errors='ignore'))
#            values = [v for d in data[f'{res.component_id}']
#                      for k, v in d.items()]
#            if str(res.component_id) == 'truth':
#                embcolor = discord.Color.green()
#                embtitle = 'Truth'
#            elif str(res.component_id) == 'dare':
#                embcolor = discord.Color.red()
#                embtitle = 'Dare'
#            embed = discord.Embed(
#                title=embtitle, description=random.choice(values), color=embcolor)
#            await ctx.send(embed=embed)
#
#        except asyncio.TimeoutError:
#            embed = discord.Embed(
#                title='Took too long to respond', color=discord.Color.dark_red())
#            await ctx.send(embed=embed)
#
#    @commands.command(aliases=["TruthOrDare", "truthdare", "td"])
#    async def tord(self, ctx, user: discord.Member = ""):
#        """Truth or Dare"""
#        await Fun.tordcmd(self, ctx, user)
#
#    @cog_ext.cog_context_menu(target=ContextMenuType.USER, name="Truth or Dare")
#    async def tordcm(self, ctx: Union[ComponentContext, MenuContext]):
#        await Fun.tordcmd(self, ctx, ctx.target_author)
#
#    @cog_ext.cog_slash(name="TruthOrDare", description="A fun game of Truth or Dare", options=[
#        create_option(
#            name="user",
#            description="User to ask",
#            option_type=6,
#            required=False
#        )
#    ])
#    async def slashtord(self, ctx: SlashContext, user=""):
#        await Fun.tordcmd(self, ctx, user)


def setup(bot):
    Fun(bot)
