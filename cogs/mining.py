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

        # minpool Pool
        headers={"user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36"}
        try:
            async with ClientSession() as session:
                async with session.get("https://minpool.net/api/currencies", headers=headers) as response:
                    responseRaw = await response.read()
                    miningData = json.loads(responseRaw)["HLIX"]

                    workers = miningData["workers"]
                    shares = miningData["shares"]
                    hashrate = miningData["hashrate"]
                    hashrate_Ghs = hashrate/1000000000
                    lastblock = miningData["lastblock"]
                    blocks24h = miningData["24h_blocks"]
                    timesincelast = miningData["timesincelast"]

                    embed= discord.Embed(colour=0x00FF00)
                    embed.set_author(name='Minpool.net Pool Information', icon_url="https://pbs.twimg.com/profile_images/947108830495854593/XFrI4e8G_400x400.jpg")
                    embed.add_field(name="Workers", value='{}'.format(workers))
                    embed.add_field(name="Pool Hashrate", value='{0:.2f} GH/s'.format(hashrate_Ghs))
                    embed.add_field(name="Shares", value='{}'.format(shares))
                    embed.add_field(name="24hr Blocks", value='{}'.format(blocks24h))
                    embed.add_field(name="Last Block Found", value='{}'.format(lastblock))
                    embed.add_field(name="Time Since Last Block", value='{0:.2f} min'.format(timesincelast/60))
                    embed.set_footer(text="ccminer-x64 -a quark -o stratum+tcp://minpool.net:6300 -u your_wallet_address -p c=HLIX")
                    await self.bot.say(embed=embed)

        except:
            await self.bot.say(":warning: Error fetching BSOD information!")

        #Erstweal Pool
        try:
            async with ClientSession() as session:
                async with session.get("https://minepool.online/api/currencies", headers=headers) as response:
                    responseRaw = await response.read()
                    miningData = json.loads(responseRaw)["HLIX"]

                    workers = miningData["workers"]
                    shares = miningData["shares"]
                    hashrate = miningData["hashrate"]
                    hashrate_Ghs = hashrate/1000000000
                    lastblock = miningData["lastblock"]
                    blocks24h = miningData["24h_blocks"]
                    timesincelast = miningData["timesincelast"]

                    embed= discord.Embed(colour=0x00FF00)
                    embed.set_author(name='minepool.online Pool Information')
                    embed.add_field(name="Workers", value='{}'.format(workers))
                    embed.add_field(name="Pool Hashrate", value='{0:.2f} GH/s'.format(hashrate_Ghs))
                    embed.add_field(name="Shares", value='{}'.format(shares))
                    embed.add_field(name="24hr Blocks", value='{}'.format(blocks24h))
                    embed.add_field(name="Last Block Found", value='{}'.format(lastblock))
                    embed.add_field(name="Time Since Last Block", value='{0:.2f} min'.format(timesincelast/60))
                    embed.set_footer(text="ccminer-x64 -a quark -o stratum+tcp://minepool.online:4045 -u <Wallet_Address> -p c=HLIX")
                    await self.bot.say(embed=embed)

        except:
            await self.bot.say(":warning: Error fetching Erstweal information!")

def setup(bot):
    bot.add_cog(Mining(bot))

