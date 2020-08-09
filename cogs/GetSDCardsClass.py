import discord
from discord.ext import commands
import json
import asyncio
import cards

cardsId = "SDCards"

class GetSDCards(commands.Cog):
    def __init__(self, bot=None):
        self.bot = bot

        with open(r"C:\Users\krypt\Desktop\TradeWars\Cards.json", "r") as f:
            self.cardData = json.load(f)
        
        newCardList = []
        for card in self.cardData[cardsId]:
            newCardList.append(cards.SDCard(card["id"], card["name"], card["capacity"], card["price"]))
        self.cardList = newCardList

    def getCardList(self):
        return self.cardList
        
def setup(bot=None):
    if bot:
        bot.add_cog(GetSDCards(bot))