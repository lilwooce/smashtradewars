import discord
from discord.ext import commands
import json
import asyncio
import productsClass

productId = "Products"

class GetProducts(commands.Cog):
    def __init__(self, bot=None):
        self.bot = bot
        self.productList = []
        
        with open(r"C:\Users\krypt\Desktop\TradeWars\Products.json", "r") as f:
            self.productData = json.load(f)
            
        for product in self.productData[productId]:
            self.productList.append(productsClass.Product(product["id"], product["name"], product["minPrice"], product["currentPrice"], product["maxPrice"], product["amount"], product["baseAmount"], product["desc"]))
            
    def getProductList(self):
        return self.productList

def setup(bot=None):
    if bot:
        bot.add_cog(GetProducts(bot))