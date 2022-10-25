import requests
import interactions
from interactions import CommandContext
from mcstatus import JavaServer, BedrockServer
from mojang import MojangAPI


class Minecraft(interactions.Extension):
    """
    Minecraft searches!
    """

    def __init__(self, bot: interactions.Client):
        self.bot: interactions.Client = bot


    @interactions.extension_command(name = "mcplayerinfo", description = "Search a Minecraft player", options = [
        interactions.Option(name = "player", description = "Minecraft Player", type = interactions.OptionType.STRING, required = True)])
    @interactions.autodefer()
    async def mcpcmd(self, ctx: CommandContext, player):
        uuid = MojangAPI.get_uuid(player)
        if not uuid:
            await ctx.send(f'{player} does not exist.')
        else:
            profile = MojangAPI.get_profile(uuid)
            embed = interactions.Embed(
                title="UUID", description=f'`{uuid}`', color= 0x023020)
            embed.set_author(name=profile.name, icon_url='https://images-ext-1.discordapp.net/external/ha2UA0g2Fsh0wn67g6bU49JA1YOJFqyn2LgPvDS2W2w/https/orig00.deviantart.net/34de/f/2012/204/b/c/grass_block_by_barakaldo-d58bi3u.gif')
            mcfull = f'https://cravatar.eu/helmhead/{uuid}/68.png'
            embed.set_thumbnail(url=mcfull)
            mcskin = profile.skin_url
            embed.add_field(name="Textures", value=f"[MC Skin]({mcskin})", inline = True)
            embed.add_field(name='Skin Type',
                            value=profile.skin_model.capitalize(), inline = True)
            await ctx.send(embeds=embed)


    @interactions.extension_command(name = "mcserver", description = "Minecraft Java Server Info", options = [
        interactions.Option(name = "ip", description = "Minecraft Server IP", type = interactions.OptionType.STRING, required = True),
        interactions.Option(name = "port", description = "Server Port", type = interactions.OptionType.INTEGER, required = False)])
    @interactions.autodefer()
    async def slashmcserver(self, ctx: CommandContext, ip, port = ''):
        await ctx.get_channel()
        if port != '':
            mcserv = requests.get(
                f'https://api.mcsrvstat.us/2/{ip}:{port}').json() 
        else:
            mcserv = requests.get(
                f'https://api.mcsrvstat.us/2/{ip}').json()
        server = JavaServer.lookup(f'{ip}:{port}')
        status = server.status()
        try:
            online = mcserv['players']['online']
        except Exception:
            online = status.players.online
        try:
            max = mcserv['players']['max']
        except Exception:
            max = status.players.max
        try:            
            motd = mcserv['motd']['clean']
        except Exception:
            motd = status.description
        try:
            version = mcserv['version']
        except Exception:
            version = status.version.name
        latency = round(status.latency)
        embed = interactions.Embed(
            title=ip, description="🟢 Server is online", color=0x023020)
        embed.add_field(name="Type", value="Java", inline=False)
        embed.add_field(name="MOTD", value=str(motd)[2:-2])
        embed.add_field(
            name="Players", value=f'{online}/{max}', inline=False)
        embed.add_field(name="Version", value=version, inline=False)
        embed.add_field(name="Latency", value=f'{latency}ms')
        if port.isdigit():
            embed.set_thumbnail(
                url=f'https://mc-api.net/v3/server/favicon/{ip}:{port}')
        else:
            embed.set_thumbnail(
                url=f'https://mc-api.net/v3/server/favicon/{ip}')
        embed.set_footer(text='Generated by Jake the Dog')
        await ctx.send(embeds=embed)


 
    @interactions.extension_command(name = "mcbedrock", description = "Minecraft Bedrock Server Info", options = [
        interactions.Option(name = "ip", description = "Minecraft Server IP", type = interactions.OptionType.STRING, required = True),
        interactions.Option(name = "port", description = "Server Port", type = interactions.OptionType.INTEGER, required = False)])
    @interactions.autodefer()
    async def mcbedrockcmd(self, ctx: CommandContext, ip, port = ''):
        await ctx.get_channel()
        if port != '':
            mcserv = requests.get(
                f'https://api.mcsrvstat.us/bedrock/2/{ip}:{port}').json()
        else:
            mcserv = requests.get(
                f'https://api.mcsrvstat.us/bedrock/2/{ip}').json()
        server = BedrockServer.lookup(f'{ip}:{port}')
        status = server.status()
        try:
            online = mcserv['players']['online']
        except Exception:
            online = status.players_online
        try:
            max = mcserv['players']['max']
        except Exception:
            max = status.players_max
        try:            
            motd = mcserv['motd']['clean']
        except Exception:
            motd = status.motd
        try:
            version = mcserv['version']
        except Exception:
            version = status.version.version
        embed = interactions.Embed(
            title=ip, description="🟢 Server is online", color=0x023020)
        embed.add_field(name="Type", value="Bedrock", inline=False)
        embed.add_field(name="MOTD", value=str(motd)[2:-2])
        embed.add_field(
            name="Players", value=f'{online}/{max}', inline=False)
        embed.add_field(name="Version", value=version, inline=False)
        if port.isdigit():
            embed.set_thumbnail(
                url=f'https://api.mcsrvstat.us/icon/{ip}:{port}')
        else:
            embed.set_thumbnail(url=f'https://api.mcsrvstat.us/icon/{ip}')
        embed.set_footer(text=f'Generated by Jake the Dog')
        await ctx.send(embeds=embed)



def setup(bot):
    Minecraft(bot)