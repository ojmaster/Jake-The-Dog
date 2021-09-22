import asyncio

import discord
import yaml
from discord.ext import commands
from discord.http import Route
from discord_slash import SlashContext, cog_ext
from discord_slash.context import ComponentContext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import (create_actionrow,
                                                   create_button,
                                                   wait_for_component)


class VCGames(commands.Cog):
    """
    Discord VC Games!!
    """
    def __init__(self, bot):
        self.bot = bot
        self.known_activities = yaml.safe_load(open("config/activities.yaml", "r"))

    @commands.command()
    async def activities(self, ctx):
        await VCGames.activitiescmd(self, ctx)

    @cog_ext.cog_slash(name="Activities", description="Discords Beta VC Games")
    async def slashactivties(self, ctx: SlashContext):
        await VCGames.activitiescmd(self, ctx)

    async def activitiescmd(self, ctx):
        """
        The base command for all VC games
        """
        buttons = []
        for k, _i in self.known_activities.items():
            buttons.append(create_button(style=ButtonStyle.blue, label=f'{k}', custom_id=f'{k}'))
        action_row = create_actionrow(*buttons)

        m = await ctx.send(
            content="Here are your choices.", components=[action_row]
        )

        try:
            res: ComponentContext = await wait_for_component(ctx.bot, components = action_row, timeout=60)
            voice = ctx.author.voice

            if not voice:
                return await ctx.send(
                    content="You have to be in a voice channel to use this command."
                )

            r = Route(
                "POST", "/channels/{channel_id}/invites", channel_id=voice.channel.id
            )

            payload = {
                "max_age": 60,
                "target_type": 2,
                "target_application_id": self.known_activities[res.component_id],
            }

            try:
                code = (await self.bot.http.request(r, json=payload))["code"]
            except discord.Forbidden:

                return await ctx.send(
                    content="I Need the `Create Invite` permission."
                )
            
            await ctx.send(
                embed=discord.Embed(
                    description=f"[Click here!](https://discord.gg/{code})\nLink expires in 1 minute",
                    color=discord.Colour.red(),
                )
            )

        except asyncio.TimeoutError:
            embed = discord.Embed(title = 'Took too long to respond', color = discord.Color.dark_red())
            await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(VCGames(bot))
