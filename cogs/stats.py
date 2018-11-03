import discord, os
from discord.ext import commands
from utils import checks, output, parsing
from aiohttp import ClientSession
import urllib.request
import json

class Stats:
    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def stats(self, ctx, amount=1):
        """
        Show stats about HLIX
        """
        channel_name = ctx.message.channel.name
        allowed_channels = parsing.parse_json('config.json')['command_channels'][ctx.command.name]
        if channel_name not in allowed_channels:
            return

        headers={"user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36"}
        try:
            async with ClientSession() as session:
                async with session.get("https://api.coingecko.com/api/v3/coins/helix", headers=headers) as response:
                    responseRaw = await response.read()
                    priceData = json.loads(responseRaw)
                    for item in priceData:
                        embed= discord.Embed(colour=0x00FF00)
                        embed.set_author(name='HLIX Information', icon_url="https://i.imgur.com/ZnwpZ3r.png")
                        embed.add_field(name="Price (USD)", value="${}".format(item['price_usd:']))
                        embed.add_field(name="Price (BTC)", value="{} BTC".format(item['price_btc:']))
                        embed.add_field(name='\u200b',value='\u200b')
                        embed.add_field(name="Volume (USD)", value="${}".format(item['24h_volume_usd:']))
                        embed.add_field(name="Market Cap", value="${}".format(item['market_cap_usd:']))
                        embed.add_field(name='\u200b',value='\u200b')
                        embed.add_field(name="% 1h", value="{}%".format(item['percent_change_1h:']))
                        embed.add_field(name="% 24h", value="{}%".format(item['percent_change_24h:']))
                        embed.add_field(name="% 7d", value="{}%".format(item['percent_change_7d:']))
                        embed.add_field(name="Circulating Supply", value="{} HLIX".format(item['available_supply:']))
                        embed.add_field(name="Total Supply", value="{} HLIX".format(item['total_supply:']))
                        embed.add_field(name="Maximum Supply", value="500,000,000 HLIX")
                        embed.set_footer(text="", icon_url="https://i.imgur.com/ZnwpZ3r.png")
                    await self.bot.say(embed=embed)
        except:
            await self.bot.say(":warning: Error fetching prices!")


def setup(bot):
    bot.add_cog(Stats(bot))
