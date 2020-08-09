import player
import citiesClass
import discord
from discord.ext import commands
import os
import json

client = commands.Bot(command_prefix = "$")

def getToken():
    with open (r"config.json", "r") as f:
        data = json.load(f)
        return data["token"]

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

token = getToken()

client.run(token)
