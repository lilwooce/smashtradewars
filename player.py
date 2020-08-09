import discord
import random

class Player:
    def __init__(self, plrId, currentCityId, money, capacity, maxCapacity, inventory, currentSDCard, travelling=False):
        self.plrId = plrId
        self.currentCityId = currentCityId
        self.money = money
        self.capacity = capacity
        self.maxCapacity = maxCapacity
        self.inventory = inventory
        self.currentSDCard = currentSDCard
        self.travelling = travelling

    def checkInventory(self, itemToCheck):
        for attr in self.inventory:
            realItemId = int(attr)
            if not itemToCheck.productId == realItemId:
                pass
            else:
                return True
        return False

    def increaseProduct(self, itemToIncrease, amountToIncrease):
        for attr in self.inventory:
            realItemId = int(attr)
            if itemToIncrease.productId == realItemId:
                currentProductAmount = self.inventory[attr]
                self.inventory[attr] = currentProductAmount + amountToIncrease
            else:
                pass
    
    def decreaseProduct(self, itemToDecrease, amountToDecrease):
        itemToRemove = None
        for attr in self.inventory:
            realItemId = int(attr)
            if itemToDecrease.productId == realItemId:
                if self.inventory[attr] - amountToDecrease == 0:
                    itemToRemove = itemToDecrease.productId
                else:
                    currentProductAmount = self.inventory[attr]
                    self.inventory[attr] = currentProductAmount - amountToDecrease
            else:
                pass
        if itemToRemove:
            print("removing item")
            for prodID in self.inventory:
                print(prodID)
            self.inventory.pop(itemToDecrease.productId)

    
