import player
import citiesClass
import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix = "$")
botCreator = "Juhwooce#0939"

for cog in os.listdir(".\\cogs"):
    if cog.endswith(".py"):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            client.load_extension(cog)
        except Exception as e:
            print(f"{cog} cannot be loaded")
            raise e

@client.event
async def on_ready():
    print("Ready!")
    #cities.City.addProductsToCity()

client.run('NzE5NjcwMjAyNjUxOTAxOTgz.Xt6zNw.OZa9NGh0ucFARjGhoN6KMxO8NFM')
