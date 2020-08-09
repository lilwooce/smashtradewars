import discord
import random

class SDCard():
    def __init__(self, cardID, name, capacity, price):
        self.cardId = cardID
        self.name = name
        self.capacity = capacity
        self.price = price