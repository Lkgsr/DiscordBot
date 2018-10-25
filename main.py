import random
import asyncio
import aiohttp
import json
from discord import Game, Embed
from discord.ext.commands import Bot
import os

description_play = ''

BOT_PREFIX = ("!")
with open('TOKEN.txt', 'r') as f:
    TOKEN = f.readline()

client = Bot(command_prefix=BOT_PREFIX)
player, voice = None, None


@client.event
async def on_ready():
    await client.change_presence(game=Game(name="PUBG MOBILE"))
    print("Logged in as " + client.user.name)


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)

if __name__ == '__main__':
    for extension in 'CatOrDog', 'Sounds', 'LevelingSystem':
        client.load_extension(extension)
    client.loop.create_task(list_servers())
    client.run(TOKEN)
