from discord.ext import commands


class BaseCog(commands.Cog):
    """Base class for an cog extension"""
    def __init__(self, bot):
        self.bot = bot


class BaseDBCog(BaseCog):
    def __init__(self, bot, database):
        super().__init__(bot)
        self.database = database

    async def on_ready(self):
        pass
