import asyncio
import json
import random

from urllib.request import urlopen
import interactions
from interactions import CommandContext, ComponentContext
from urbandictionary_top import udtop

class Fun(interactions.Extension):
    """
    Its fun time!
    """

    def __init__(self, bot: interactions.Client):
        self.bot: interactions.Client = bot

    @interactions.extension_command(description="Bonk")
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

    @interactions.extension_command(description = "Slots")
    async def slots(self, ctx: CommandContext):
        await self.slotcmd(ctx)

    @interactions.extension_user_command(name = "Slots")
    async def slotscm(self, ctx):
        await self.slotcmd(ctx)

    
    @interactions.extension_command(name = "8ball", description = "Let the wisdowm of the 8ball give you the answers you seek", options = [interactions.Option(
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
        
    
    @interactions.extension_command(name = "coinflip", description = "Flip a coin")
    async def coinflip(self, ctx: CommandContext):
        await ctx.get_channel()
        coinsides = ["Heads", "Tails"]
        await ctx.send(f"**{ctx.user.username}** flipped a coin and got **{random.choice(coinsides)}**!")

    @interactions.extension_user_command(name = "Coinflip")
    async def coinflipcm(self, ctx: ComponentContext):
        coinsides = ["Heads", "Tails"]
        await ctx.send(f"**{ctx.user.username}** flipped a coin and got **{random.choice(coinsides)}**!")


    @interactions.extension_command(name = "urbandictionary", description = "Look up the urban diction of your word",  options = [interactions.Option(
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

    @interactions.extension_command(name = "choose", description = "Pick from a list of choices")
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
        

    @interactions.extension_command(name = "countdown", description = "Set a timer in seconds", options = [interactions.Option(
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

  
    @interactions.extension_user_command(name="RIP")
    async def ripcm(self, ctx: ComponentContext):
        await ctx.send(f'R.I.P. {ctx.target.mention}\nhttps://tenor.com/bipRq.gif')

    @interactions.extension_command(name = "hype", description = "HYPE HYPE HYPE HYPE!!!!")
    async def hypecmd(self, ctx: CommandContext):
        await ctx.get_channel()
        hypu = ['https://cdn.discordapp.com/attachments/102817255661772800/219514281136357376/tumblr_nr6ndeEpus1u21ng6o1_540.gif',
                'https://cdn.discordapp.com/attachments/102817255661772800/219518372839161859/tumblr_n1h2afSbCu1ttmhgqo1_500.gif',
                'https://gfycat.com/HairyFloweryBarebirdbat',
                'https://i.imgur.com/PFAQSLA.gif',
                'https://abload.de/img/ezgif-32008219442iq0i.gif',
                'https://i.imgur.com/vOVwq5o.jpg',
                'https://i.imgur.com/Ki12X4j.jpg',
                'https://media.giphy.com/media/b1o4elYH8Tqjm/giphy.gif']
        msg = f':train2: CHOO CHOO {random.choice(hypu)}'
        await ctx.send(msg)


    async def puncmd(self, ctx):
        await ctx.get_channel()
        data = json.load(
            open('./config/choices.json', encoding="utf8", errors='ignore'))
        emojis = ['😆', '😄', '😂', '😭', '🤣']
        url = "https://raw.githubusercontent.com/dabbers/OPun/main/data.json"
        response = urlopen(url)
        data_json = json.loads(response.read())["data"]["posts"]
        pn = await ctx.send(random.choice(data_json)["plaintext"])
        await pn.create_reaction(random.choice(emojis))


    @interactions.extension_command(name = "pun", description = "Because everybody likes a bad joke")
    async def pun(self, ctx: CommandContext):
        await Fun.puncmd(self, ctx)

    @interactions.extension_user_command(name="Send a Pun")
    async def puncm(self, ctx: ComponentContext):
        await Fun.puncmd(self, ctx)


    async def tordcmd(self, ctx, player):
        embed = interactions.Embed(title="Truth or Dare",
                              color= 0xF4975F)
        button = interactions.Button(
            style= interactions.ButtonStyle.SUCCESS,
            label="Truth",
            custom_id="Truth"
        )
        button2 = interactions.Button(
            style= interactions.ButtonStyle.DANGER,
            label="Dare",
            custom_id="Dare"
        )
        action_row = interactions.ActionRow(components=[button, button2])
        if player != "":
            await ctx.send(content=f'{ctx.user.mention}', embeds=embed, components=[action_row])
        else:
            await ctx.send(embeds=embed, components=[action_row])



    @interactions.extension_component("Truth")
    async def truther(self, ctx):
        data = json.load(
            open('./config/choices.json', encoding="utf8", errors='ignore'))
        values = [v for d in data['truth']
                    for k, v in d.items()]
        embed = interactions.Embed(title = "Truth", description = random.choice(values), color = interactions.Color.green())
        await ctx.message.delete()
        await ctx.send(embeds=embed, components = [])
        


    @interactions.extension_component("Dare")
    async def darer(self, ctx):
        data = json.load(
            open('./config/choices.json', encoding="utf8", errors='ignore'))
        values = [v for d in data['dare']
                    for k, v in d.items()]
        embed = interactions.Embed(title = "Dare", description = random.choice(values), color = interactions.Color.red())
        await ctx.message.delete()
        await ctx.send(embeds=embed, components = [])
        


    @interactions.extension_command(name="truthordare", description="A fun game of Truth or Dare", options=[
        interactions.Option(
            type = interactions.OptionType.USER,
            name="user",
            description="User to ask",
            required=False
        )
    ])
    async def slashtord(self, ctx: CommandContext, user: interactions.User = ""):
        await Fun.tordcmd(self, ctx, user)


def setup(bot):
    Fun(bot)