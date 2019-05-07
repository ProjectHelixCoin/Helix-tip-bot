import discord, json, requests, math
from discord.ext import commands
from utils import rpc_module as rpc, parsing
from aiohttp import ClientSession


class Mining:
    def __init__(self, bot):
        self.bot = bot
        self.rpc = rpc.Rpc()

    @commands.command(pass_context=True)
    async def mining(self, ctx):
        """Show mining info"""
        channel_name = ctx.message.channel.name
        allowed_channels = parsing.parse_json('config.json')['command_channels'][ctx.command.name]
        if channel_name not in allowed_channels:
            return

        mining_info = self.rpc.getmininginfo()
        height = mining_info["blocks"]
        difficulty = mining_info["difficulty"]
        network_hs = mining_info["networkhashps"]
        network_Ghs = network_hs/1000000000
        
        embed= discord.Embed(colour=0x00FF00)
        embed.set_author(name='HLIX Mining Information', icon_url="https://i.imgur.com/ZnwpZ3r.png")
        embed.add_field(name="Current Height", value='{}'.format(height))
        embed.add_field(name="Network Difficulty", value='{0:.2f}'.format(difficulty))
        embed.add_field(name="Network Hashrate", value='{0:.2f} GH/s'.format(network_Ghs))
        await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(Mining(bot))

