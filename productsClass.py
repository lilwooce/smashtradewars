import discord
import random
import math
import copy

class Product:
    def __init__(self, id, name, priceMin, currentPrice, priceMax, amount, baseAmount, desc, image = None):
        self.productId = id
        self.name = name
        self.priceMin = priceMin
        self.currentPrice = currentPrice
        self.priceMax = priceMax
        self.amount = amount
        self.baseAmount = baseAmount
        self.desc = desc
        self.image = image