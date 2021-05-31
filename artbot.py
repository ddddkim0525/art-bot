import os
import sys
import importlib
import discord
from dotenv import load_dotenv
from discord.ext import commands
from core.db import Database
from loguru import logger


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

db = Database()
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    logger.info("Bot is online")


# Load cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        cog = filename[:-3]
        lib = importlib.import_module('cogs.' + cog)

        if not hasattr(lib, 'setup'):
            del lib
            del sys.modules[cog]
            raise discord.ClientException("extension does not have a setup function")

        lib.setup(bot, db)


if __name__ == "__main__":
    bot.run(TOKEN)
