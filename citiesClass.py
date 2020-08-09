import discord
import random
import cogs.GetCitiesClass
import cogs.GetProductsClass
import math
import copy

citiesId = "Cities"
priceVariance = 5

class City: 
    def __init__(self, cityId, name, shop, bank, economicState, image, population, products=[]): # *products is a variable argument for the products, similar to *args
        self.cityId = cityId
        self.name = name
        self.shop = shop
        self.bank = bank
        self.economicState = economicState # Economic State of 0 means getting worse (Decline) 1 means normal(Normal) and 2 means booming(Booming)
        self.image = image
        self.population = population
        self.products = products

    def updatePrice(self, productChanged, amountChangedBy):
        getCitiesClass = cogs.GetCitiesClass.GetCities()

        for product in self.products:
            if product.productId == productChanged.productId:
                changedPrice = calculatePrice(product, amountChangedBy)
                print(changedPrice)

                product.currentPrice = changedPrice
                getCitiesClass.updateCityProduct(self, product, product.amount)

    def checkProduct(self, productToCheck):
        for product in self.products:
            if product.productId == productToCheck.productId:
                return True
            else:
                pass
        return False
    
    def removeProduct(self, productToRemove, amountToRemove):
        for product in self.products:
            if product.productId == productToRemove.productId:
                product.amount -= amountToRemove
                self.updatePrice(productToRemove, amountToRemove)

    def addProduct(self, productToAdd, amountToAdd):
        for product in self.products:
            if product.productId == productToAdd.productId:
                product.amount += amountToAdd
                self.updatePrice(productToAdd, amountToAdd)

    def getProductFromCity(self, productToGet):
        for product in self.products:
            if product.productId == productToGet.productId:
                return product

def calculatePrice(product, amountChangedBy=0):
        if amountChangedBy > 0:
            productPercentage = ((amountChangedBy / product.baseAmount))
            maxPriceDifference = product.priceMax - product.currentPrice
            priceAddition = (maxPriceDifference * productPercentage) * priceVariance
            priceToChange = product.currentPrice + priceAddition
            
            if priceToChange >= product.priceMax:
                priceToChange = product.priceMax
            elif priceToChange <= product.priceMin:
                priceToChange = product.priceMin
            
            return priceToChange
        else:
            amountChangedBy = product.baseAmount - product.amount

            productPercentage = ((amountChangedBy / product.baseAmount))
            maxPriceDifference = product.priceMax - product.currentPrice
            priceAddition = (maxPriceDifference * productPercentage) * priceVariance
            priceToChange = product.currentPrice + priceAddition
            
            if priceToChange >= product.priceMax:
                priceToChange = product.priceMax
            elif priceToChange <= product.priceMin:
                priceToChange = product.priceMin

            return priceToChange


    

