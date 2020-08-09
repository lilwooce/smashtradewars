import discord
from discord.ext import commands
import json
import asyncio
import player
import cogs.GetSDCardsClass as SDCardModule
import cogs.GetProductsClass
import cogs.GetCitiesClass

startingCash = 1000

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.playerList = []

        self.bot.loop.create_task(self.save_users())

        with open(r"C:\Users\krypt\Desktop\TradeWars\UserData.json", "r") as f:
            self.users = json.load(f)
            
        for user in self.users:
            self.playerList.append(player.Player(user, self.users[user]["currentCity"], self.users[user]["money"], self.users[user]["capacity"], self.users[user]["maxCapacity"], self.users[user]["inventory"], self.users[user]["currentCard"]))
            
    async def save_users(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            with open(r"C:\Users\krypt\Desktop\TradeWars\UserData.json", "w") as f:
                json.dump(self.users, f, indent=4)

            await asyncio.sleep(5)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        author_id = str(message.author.id)

        for player in self.playerList:
            if player.plrId == author_id:
                playerToUse = player

        if author_id in self.users:
            self.users[author_id]["money"] += 1
            playerToUse.money += 1

    @commands.command()
    async def start(self, ctx):
        author_id = str(ctx.author.id)

        getCardsClass = SDCardModule.GetSDCards()
        cardsList = getCardsClass.getCardList()

        getCitiesClass = cogs.GetCitiesClass.GetCities()
        citiesList = getCitiesClass.getCityList()

        startingCapacity = cardsList[0].capacity
        startingCity = citiesList[0].cityId
        startingCard = cardsList[0].cardId

        if not author_id in self.users:
            self.users[author_id] = {}
            self.users[author_id]["inventory"] = {} #The key is the id of the product and the value is the amount owned of it
            self.users[author_id]["money"] = startingCash
            self.users[author_id]["capacity"] = startingCapacity
            self.users[author_id]["maxCapacity"] = startingCapacity
            self.users[author_id]["currentCity"] = startingCity
            self.users[author_id]["currentCard"] = startingCard
            self.playerList.append(player.Player(author_id, self.users[author_id]["currentCity"], self.users[author_id]["money"], self.users[author_id]["capacity"], self.users[author_id]["maxCapacity"], self.users[author_id]["inventory"], self.users[author_id]["currentCard"]))

            await ctx.send("Congratulations " + ctx.author.mention + " you have created your own Trade Wars character!")
            print(self.users)
        else:
            await ctx.send("Why are you trying to start if you already have a character created?")

    @commands.command()
    async def buy(self, ctx, productToBuyName, amountToBuy=1,  member: discord.Member=None):
        getProductsClass = cogs.GetProductsClass.GetProducts()
        productList = getProductsClass.getProductList()

        getCitiesClass = cogs.GetCitiesClass.GetCities()
        citiesList = getCitiesClass.getCityList()
        
        playerBuying = None
        productToBuy = None
        playerId = None

        member = ctx.author
        member_id = str(member.id)

        for product in productList:
            if product.name == productToBuyName:
                productToBuy = product

        for player in self.playerList:
            if player.plrId == str(ctx.author.id):
                playerBuying = player
                playerId = str(ctx.author.id)
            else:
                pass

        if playerBuying.travelling == False:
            if playerBuying.money >= (productToBuy.currentPrice * amountToBuy):
                if player.maxCapacity >= amountToBuy:
                    for city in citiesList:
                        if city.cityId == playerBuying.currentCityId:
                            if city.checkProduct(productToBuy):
                                cityProduct = city.getProductFromCity(productToBuy)


                                embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)
                                embed.set_author(name=f"{member}", icon_url=member.avatar_url)
                                embed.title = "Successful Transaction"

                                if amountToBuy > 1:
                                    amountSpent = cityProduct.currentPrice * amountToBuy
                                    embed.add_field(name="\u200b", value=f"You bought {amountToBuy} {cityProduct.name}s for {amountSpent} cash.")
                                else:
                                    embed.add_field(name="\u200b", value=f"You bought {amountToBuy} {cityProduct.name} for {cityProduct.currentPrice} cash.")

                                if not playerBuying.checkInventory(cityProduct):
                                    print("adding new item")
                                    self.users[playerId]["money"] -= cityProduct.currentPrice * amountToBuy
                                    self.users[playerId]["capacity"] -= amountToBuy
                                    playerBuying.money -= cityProduct.currentPrice * amountToBuy
                                    playerBuying.capacity -= amountToBuy
                                    playerBuying.inventory[cityProduct.productId] = amountToBuy

                                    city.removeProduct(cityProduct, amountToBuy)
                                else:
                                    print("increasing old item")
                                    self.users[playerId]["money"] -= cityProduct.currentPrice * amountToBuy
                                    self.users[playerId]["capacity"] -= amountToBuy
                                    playerBuying.money -= cityProduct.currentPrice * amountToBuy
                                    playerBuying.capacity -= amountToBuy
                                    playerBuying.increaseProduct(cityProduct, amountToBuy)

                                    city.removeProduct(cityProduct, amountToBuy)
                            else:
                                await ctx.send("This product does not exist here.")
                                pass

                            await ctx.send(embed=embed)
                        else:
                            pass
                else:
                    await ctx.send("Insuficient capacity.")
            else: 
                await ctx.send("Insufficient money.")
        else:
            await ctx.send("You are travelling right now, please wait.")
            pass

    @commands.command()
    async def sell(self, ctx, productToSellName, amountToSell=1,  member: discord.Member=None):
        getProductsClass = cogs.GetProductsClass.GetProducts()
        productList = getProductsClass.getProductList()

        getCitiesClass = cogs.GetCitiesClass.GetCities()
        citiesList = getCitiesClass.getCityList()
        
        playerSelling = None
        productToSell = None
        playerId = None

        member = ctx.author
        member_id = str(member.id)

        for product in productList:
            if product.name == productToSellName:
                productToSell = product

        for player in self.playerList:
            if player.plrId == str(ctx.author.id):
                playerSelling = player
                playerId = str(ctx.author.id)
            else:
                pass
            
        if playerSelling.travelling == False:
            for city in citiesList:
                if city.cityId == playerSelling.currentCityId:
                    if city.checkProduct(productToSell):
                        cityProduct = city.getProductFromCity(productToSell)
                        
                        if not playerSelling.checkInventory(productToSell):
                            await ctx.send("You do not own this product")
                            pass
                        else:
                            embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)
                            embed.set_author(name=f"{member}", icon_url=member.avatar_url)
                            embed.title = "Successful Transaction"

                            if amountToSell > 1:
                                amountSpent = cityProduct.currentPrice * amountToSell
                                embed.add_field(name="\u200b", value=f"You sold {amountToSell} {cityProduct.name}s and got {amountSpent} cash for it.")
                            else:
                                embed.add_field(name="\u200b", value=f"You sold {amountToSell} {cityProduct.name} and got {cityProduct.currentPrice} cash for it.")

                            self.users[playerId]["inventory"].pop(str(cityProduct.productId), None)
                            playerSelling.decreaseProduct(cityProduct, amountToSell)
                            self.users[playerId]["capacity"] += amountToSell
                            
                            self.users[playerId]["money"] += cityProduct.currentPrice * amountToSell
                            playerSelling.money += cityProduct.currentPrice * amountToSell
                            playerSelling.capacity += amountToSell

                            city.addProduct(cityProduct, amountToSell)
                    else:
                        await ctx.send("You cannot sell this here")
                        pass
                    await ctx.send(embed=embed)
                else:
                    pass
        else:
            await ctx.send("You are travelling right now, please wait.")


    def getPlayerList(self):
        return self.playerList
        
    @commands.command()
    async def shop(self, ctx):
        getProductsClass = cogs.GetProductsClass.GetProducts()
        productList = getProductsClass.getProductList()

        getCitiesClass = cogs.GetCitiesClass.GetCities()
        citiesList = getCitiesClass.getCityList()

        member = ctx.author
        member_id = str(member.id)

        if not member_id in self.users:
            await ctx.send("Player does not have a character, please use $start in order to create one.")
        else:
            playerToUse = None

            for player in self.playerList:
                if player.plrId == member_id:
                    playerToUse = player

        embed = discord.Embed(timestamp=ctx.message.created_at)
        embed.title = "Shop"
        
        playerCity = playerToUse.currentCityId
        playerCurrentCity = None
        for city in citiesList:
            if city.cityId == playerCity:
                playerCurrentCity = city


        for product in productList:
            cityProductVersion = playerCurrentCity.getProductFromCity(product)
            for attribute, value in cityProductVersion.__dict__.items():
                if not value == None:
                    if str(attribute) == "productId":
                        pass
                    elif str(attribute) == "priceMin":
                        pass
                    elif str(attribute) == "priceMax":
                        pass
                    elif str(attribute) == "baseAmount":
                        pass
                    elif str(attribute) == "desc":
                        embed.add_field(name="Description", value=value, inline=False)
                    elif str(attribute) == "currentPrice":
                        embed.add_field(name="Price", value=cityProductVersion.currentPrice, inline=True)
                    elif str(attribute) == "name":
                        embed.add_field(name="Name", value=value, inline=False)
                    else:
                        embed.add_field(name=attribute, value=value, inline=True)
                else:
                    pass
        await ctx.send(embed=embed)

    @commands.command()
    async def cities(self, ctx):
        getCitiesClass = cogs.GetCitiesClass.GetCities()
        citiesList = getCitiesClass.getCityList()

        embed = discord.Embed(timestamp=ctx.message.created_at)
        embed.title = "Cities"

        for city in citiesList:
            for attribute, value in city.__dict__.items():
                if not value == None:
                    if str(attribute) == "cityId":
                        pass
                    elif str(attribute) == "shop":
                        pass
                    elif str(attribute) == "image":
                        pass
                    elif str(attribute) == "bank":
                        pass
                    elif str(attribute) == "products":
                        pass
                    elif str(attribute) == "economicState":
                        economicStateString = None
                        if value == 0:
                            economicStateString = "Decline"
                        elif value == 1:
                            economicStateString = "Normal"
                        elif value == 0:
                            economicStateString = "Booming"
                        embed.add_field(name="Economic State", value=economicStateString, inline=True)
                    elif str(attribute) == "name":
                        embed.add_field(name=attribute, value=value, inline=False)
                    else:
                        embed.add_field(name=attribute, value=value, inline=True)
                else:
                    pass
        await ctx.send(embed=embed)


    @commands.command(aliases=["prof"])
    async def profile(self, ctx, member: discord.Member=None):
        getCitiesClass = cogs.GetCitiesClass.GetCities()
        citiesList = getCitiesClass.getCityList()

        getProductsClass = cogs.GetProductsClass.GetProducts()
        productList = getProductsClass.getProductList()

        getCardsClass = SDCardModule.GetSDCards()
        cardsList = getCardsClass.getCardList()

        member = ctx.author if not member else member
        member_id = str(member.id)

        if not member_id in self.users:
            await ctx.send("Player does not have a character, please use $start in order to create one.")
        else:
            playerToUse = None

            for player in self.playerList:
                if player.plrId == member_id:
                    playerToUse = player

            embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)
            embed.set_author(name=f"{member}", icon_url=member.avatar_url)

            for attribute, value in playerToUse.__dict__.items():
                if str(attribute) == "currentCityId":
                    cityNameToUse = None
                    for city in citiesList:
                        if city.cityId == value:
                            cityNameToUse = city.name
                            embed.add_field(name="Current City", value=cityNameToUse, inline=False)
                elif str(attribute) == "currentSDCard":
                    cardNameToUse = None
                    for card in cardsList:
                        if card.cardId == value:
                            cardNameToUse = card.name
                            embed.add_field(name="Current SD Card", value=cardNameToUse, inline=False)
                elif str(attribute) == "money":
                    playerCash = self.users[member_id]["money"]
                    embed.add_field(name=attribute, value=playerCash, inline=True)
                elif str(attribute) == "plrId":
                    pass
                elif str(attribute) == "travelling":
                    pass
                elif str(attribute) == "inventory":
                    pass
                else:
                    embed.add_field(name=attribute, value=value, inline=True)
            await ctx.send(embed=embed)
    
    @commands.command(aliases=["inv"])
    async def inventory(self, ctx, member: discord.Member=None):
        getCitiesClass = cogs.GetCitiesClass.GetCities()
        citiesList = getCitiesClass.getCityList()

        getProductsClass = cogs.GetProductsClass.GetProducts()
        productList = getProductsClass.getProductList()

        member = ctx.author if not member else member
        member_id = str(member.id)

        if not member_id in self.users:
            await ctx.send("Player does not have a character, please use $start in order to create one.")
        else:
            playerToUse = None

            for player in self.playerList:
                if player.plrId == member_id:
                    playerToUse = player

            embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)
            embed.set_author(name=f"{member}", icon_url=member.avatar_url)
            embed.title = "Inventory"

            for product in productList:
                for item in playerToUse.inventory:
                    if str(product.productId) == str(item):
                        embed.add_field(name="Item", value=product.name)
                        embed.add_field(name="Amount", value=self.users[member_id]["inventory"][item])
                        embed.add_field(name="Description", value=product.desc)
                    elif str(item) == 0:
                        print(item + " not in inventory")
                        embed.remove_field(int(len(embed.fields)) - 1)
            
            await ctx.send(embed=embed)

    

    @commands.command(aliases=["go"])
    async def move(self, ctx, cityToMove=None, member: discord.Member=None):
        getCitiesClass = cogs.GetCitiesClass.GetCities()
        citiesList = getCitiesClass.getCityList()

        def checkMoveMessage(response):
            return response.author == ctx.author and response

        member = ctx.author
        member_id = str(member.id)
        if cityToMove != None:
            placeToMove = cityToMove.lower()
            placeToMoveId = None
            
            if not member_id in self.users:
                await ctx.send("You do not have a character, please use $start in order to create one.")
            else:
                playerToUse = None

                for player in self.playerList:
                    if player.plrId == member_id:
                        playerToUse = player
                
                for city in citiesList:
                    if placeToMove == city.name.lower():
                        print("found city")
                        await ctx.send("Would you like to spend cash to go to this city now or wait the travel time? (Y) to use cash (N) to wait.")

                        try:
                            response = await self.bot.wait_for("message", timeout=5.0, check=checkMoveMessage)
                        except asyncio.TimeoutError:
                            await ctx.send("You have waited too long to choose, you will be waiting the travel time.")
                            travelTime = 5

                            playerToUse.travelling = True
                            await asyncio.sleep(travelTime)
                            placeToMoveId = city.cityId
                            playerToUse.travelling = False
                        else:
                            if response.content.lower() == "y":
                                travelCost = 2

                                self.users[member_id]["money"] -= travelCost
                                playerToUse.money -= travelCost

                                placeToMoveId = city.cityId
                                await ctx.send(f"You have spend {travelCost} cash in order to fast travel to {cityToMove}.")
                            elif response.content.lower() == "n":
                                travelTime = 5

                                await ctx.send(f"You have chosen to wait {travelTime} seconds in order to travel to {cityToMove}.")
                                playerToUse.travelling = True
                                await asyncio.sleep(travelTime)
                                placeToMoveId = city.cityId
                                playerToUse.travelling = False
                            else:
                                await ctx.send("Please provide a valid response to the command and try again.")
                                break
                        embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)
                        embed.set_author(name=f"{member}", icon_url=member.avatar_url)
                        embed.title = "Travelling"

                        if (playerToUse.currentCityId != placeToMoveId):
                            playerToUse.currentCityId = placeToMoveId
                            self.users[member_id]["currentCity"] = placeToMoveId
                            embed.add_field(name="\u200b", value=f"You have travelled to {cityToMove}.")
                        elif placeToMoveId == None:
                            await ctx.send("No city found.")
                        else:
                            await ctx.send("You are already in this city, what are you trying to move there for?")

                        if embed:
                            await ctx.send(embed=embed)
                        else:
                            pass
                    else:
                        pass
        else:
            await ctx.send("No city provided, please give a city to move to.")

    @commands.command(aliases=["nc"])
    async def nextcard(self, ctx):
        getCardsClass = SDCardModule.GetSDCards()
        cardsList = getCardsClass.getCardList()

        member = ctx.author
        member_id = str(member.id)
        playerToUse = None

        if not member_id in self.users:
            await ctx.send("You do not have a character, please use $start in order to create one.")
        else:
            playerToUse = None

        for player in self.playerList:
            if player.plrId == member_id:
                playerToUse = player

        embed = discord.Embed(timestamp=ctx.message.created_at)
        embed.title = "Next Upgrade"
        
        nextCard = None

        for card in cardsList:
            if int(playerToUse.currentSDCard + 1) <= len(cardsList) - 1:
                playerNextCard = playerToUse.currentSDCard + 1
                nextCard = cardsList[playerNextCard]
            else:
                await ctx.send("No Upgrades Available")
                break

        if nextCard != None:
            for attribute, value in nextCard.__dict__.items():
                if str(attribute) == "cardId":
                    pass
                elif str(attribute) == "name":
                    embed.add_field(name=attribute, value=value, inline=False)
                else:
                    embed.add_field(name=attribute, value=value, inline=True)
            await ctx.send(embed=embed)

    @commands.command()
    async def upgrade(self, ctx, member: discord.Member=None):
        getCardsClass = SDCardModule.GetSDCards()
        cardsList = getCardsClass.getCardList()

        member = ctx.author
        member_id = str(member.id)
        playerToUse = None

        if not member_id in self.users:
            await ctx.send("You do not have a character, please use $start in order to create one.")
        else:
            playerToUse = None

        for player in self.playerList:
            if player.plrId == member_id:
                playerToUse = player

        for card in cardsList:
            if card.cardId == playerToUse.currentSDCard:
                nextCard = int(playerToUse.currentSDCard + 1)
                print(nextCard)
                print(len(cardsList))
                if nextCard <= int(len(cardsList) - 1):
                    newCard = cardsList[nextCard]
                    if playerToUse.money >= newCard.price:
                        playerToUse.money -= newCard.price
                        self.users[member_id]["money"] -= newCard.price

                        playerToUse.currentSDCard = newCard.cardId
                        self.users[member_id]["currentCard"] = newCard.cardId

                        playerToUse.maxCapacity = newCard.capacity
                        self.users[member_id]["maxCapacity"] = newCard.capacity

                        playerToUse.capacity = playerToUse.maxCapacity
                        self.users[member_id]["capacity"] = self.users[member_id]["maxCapacity"]

                        await ctx.send(f"You have upgraded your {card.name} to a {newCard.name}.")
                        break
                    else:
                        await ctx.send("Insufficient money.")
                        break
                else:
                    await ctx.send("No upgrades available.")
                    pass
            else:
                pass
'''
    @commands.command(name="leaderboard", aliases="lb")
    async def display_leaderboard(self, ctx):
        thisServer = ctx.guild
        serverMembers = thisServer.members
        botUsers = []

        embed = discord.Embed(timestamp=ctx.message.created_at)
        embed.title = "Leaderboard"

        def sortMoney(user):
            return botUser["money"]

        for user in members:
            if user.id in self.users:
                botUsers.add(user)

        if len(botUsers) > 1:
            botUsers.sort(key=sortMoney)
            embed.add_field() '''

def setup(bot):
    bot.add_cog(Stats(bot))