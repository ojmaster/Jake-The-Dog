import yaml
import discord
from discord.ext import commands
from discord.http import Route
from discord_components import DiscordComponents, Button, ButtonStyle


class Entertainment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dc = DiscordComponents(self.bot)
        self.known_activities = yaml.safe_load(open("config/activities.yaml", "r"))

    @commands.command()
    async def activities(self, ctx, hidden=False):
        components = []
        for k, _i in self.known_activities.items():
            components.append(Button(style=ButtonStyle.blue, label=k))
        m = await ctx.send(
            content="Here are your choices.", components=components, hidden=hidden
        )
        res = await self.bot.wait_for("button_click", timeout=60)
        if not res:
            await ctx.channel.send("Too Late")
        else:
            voice = ctx.author.voice

            if not voice:
                return await res.respond(
                    content="You have to be in a voice channel to use this command.",
                    type=7,
                )

            r = Route(
                "POST", "/channels/{channel_id}/invites", channel_id=voice.channel.id
            )

            payload = {
                "max_age": 60,
                "target_type": 2,
                "target_application_id": self.known_activities[res.component.label],
            }

            try:
                code = (await self.bot.http.request(r, json=payload))["code"]
            except discord.Forbidden:

                return await res.respond(
                    content="I Need the `Create Invite` permission.", type=7
                )

            await res.respond(
                embed=discord.Embed(
                    description=f"[Click here!](https://discord.gg/{code})\nLink expires in 1 minute",
                    color=discord.Colour.red(),
                ),
                type=7,
            )


def setup(bot):
    bot.add_cog(Entertainment(bot))
