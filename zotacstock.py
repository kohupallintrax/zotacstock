from bs4 import BeautifulSoup
import requests
from random import randint
from time import sleep
import asyncio

import discord
from discord.ext import commands, tasks
from redbot.core import Config, checks, commands
from redbot.core.bot import Red
from redbot.core.commands import Cog
from redbot.core.data_manager import cog_data_path
from redbot.core.utils.chat_formatting import box, pagify

DEFAULT_MESSAGES = [
    # "Example message. Uncomment and overwrite to use",
    # "Example message 2. Each message is in quotes and separated by a comma"
]


class CheckZotac(Cog):


    def __init__(self, bot: Red):
        super().__init__()
        self.bot = bot
        self.config = Config.get_conf(self, identifier=0, force_registration=True)

        default_guild = {"iids": []}  # List of tuple pairs (channel_id, website)

        self.config.register_guild(**default_guild)



    @commands.command(alias=["zotacstock"])
    async def zotacstock(self, ctx: commands.Context, startstop):
        if startstop == "start":
            self.zotacstockcheck.start(ctx)
            await ctx.maybe_send_embed("stock checker started")
        elif startstop == "stop":
            self.zotacstockcheck.stop()
            await ctx.maybe_send_embed("stock checker stopped")
        else:
             await ctx.maybe_send_embed("start or stop needed after command")

    @tasks.loop(seconds=5.0)
    async def zotacstockcheck(self, ctx):
        """
        Check if the 5000 is in stock

        Alias: zotacstock
        """
        url = url = "https://www.zotacstore.com/us/graphics-cards/geforce-rtx-50-series"

        #with requests.Session() as session: #closes session after with block
        success = False
        try:
            results = self.CheckStock(url)
        except AssertionError:
            await ctx.maybe_send_embed("something went wrong")
            return
        
        for index, result in enumerate(results):
            if result.get("inStock") == False:
                #await ctx.maybe_send_embed(f"{result.get('product')} is out of stock!") #send alert to server
                pass
            elif result.get("inStock") == True:
                await ctx.maybe_send_embed(f"@everyone {result.get('product')} is IN STOCK!! Get it HERE: {result.get('productLink')} ") #send alert to server
                await ctx.author.create_dm()
                await ctx.author.dm_channel.send(f"{result.get('product')} is IN STOCK!! Get it HERE: {result.get('productLink')} ")
                success = True
            else:
                await ctx.maybe_send_embed("something wrong happend")
        if success == False:
            rando = (randint(1,10))
            #await ctx.maybe_send_embed(f"no stock sleeping for {str(rando + 10)}") #send alert to server
            await asyncio.sleep(rando)
        else:
            await asyncio.sleep(60)



    #def CheckStock(idk, url, session):
    def CheckStock(idk, url):
        #page = session.get(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.text,'html.parser')
        products = soup.select('li.item.product.product-item-info.product-item')
    
    
        print(len(products))

        results= []

        for index, product in enumerate(products):
            productName = product.find('h5', class_="product name product-item-name")
            productStock = product.find('span',class_='product-label sold-out-label')
            productLink = product.find('a', class_="product photo product-item-photo").get('href')
            if productStock != None:
                results.append({'product':productName.text.strip(),'inStock':False,'productLink':productLink})
            else:
                results.append({'product':productName.text.strip(),'inStock':True,'productLink':productLink})
        return results
    
        

