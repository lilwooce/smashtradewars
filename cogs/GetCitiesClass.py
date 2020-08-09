import discord
from discord.ext import commands
import json
import asyncio
import citiesClass
import cogs.GetProductsClass as GetProductsClass
import copy

citiesId = "Cities"

productClassInstance = GetProductsClass.GetProducts()
productList = productClassInstance.getProductList()

class GetCities(commands.Cog):
    def __init__(self, bot=None):
        self.bot = bot
        self.cityList = []
       

        with open(r"C:\Users\krypt\Desktop\TradeWars\Cities.json", "r") as f:
            self.cityData = json.load(f)
        
        for city in self.cityData[citiesId]:
            productsToAddToCity = []
            
            for product in productList:
                itemId = product.productId
                jsonProductAmount = self.cityData[citiesId][city["id"]]["products"][str(itemId)]
                newCityItem = copy.deepcopy(product)

                newCityItem.amount = jsonProductAmount
                newPrice = citiesClass.calculatePrice(newCityItem)
                newCityItem.currentPrice = newPrice

                productsToAddToCity.append(newCityItem)
            
            self.cityList.append(citiesClass.City(city["id"],city["name"],city["shop"], city["bank"], city["economicState"], city["image"], city["population"], productsToAddToCity))
            
    def getCityList(self):
        return self.cityList

    def giveCityData(self):
        return self.cityData

    def updateCityProduct(self, city, product, amountOfProduct):
        cityId = city.cityId
        productId = product.productId
        self.cityData[citiesId][cityId]["products"][str(productId)] = amountOfProduct
        print(product.currentPrice)

        print(f"dumping {amountOfProduct} to change the amount of a product")

        with open(r"C:\Users\krypt\Desktop\TradeWars\Cities.json", "w") as f:
                json.dump(self.cityData, f, indent=4)
    


        
def setup(bot):
    if bot != None:
        bot.add_cog(GetCities(bot))