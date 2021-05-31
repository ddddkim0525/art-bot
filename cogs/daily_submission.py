from core.base_cog import BaseDBCog
from discord.ext import commands
from loguru import logger
from tabulate import tabulate


class DailySubmissions(BaseDBCog):
    def __init__(self, bot, database):
        super().__init__(bot, database)
        self.db = database

    """Daily submissions related commands"""
    @commands.command()
    async def submit(self, ctx):
        """Create new submission entry for message author in database"""
        author = ctx.author.name
        message = ctx.message

        self.db.add_submission(author)
        try:
            img_url = message.attachments[0].url
            logger.debug(f"Image URL from message: {img_url}")
        except IndexError:
            logger.debug(f"No image in message")

        response = f"Submitted ({self.db.get_weekly_user_count(author)}/6)"
        logger.info(f"Responding: {response}")
        await ctx.send(response)

    @commands.command()
    async def summary(self, ctx):
        """Print the weekly submission count of all participants."""
        df = self.db.get_weekly_summary()
        response = tabulate(df, tablefmt='psql', showindex=False)
        response = "```\nWeekly Summary\n" + response + "\n```"
        logger.info(f"Responding:\n{response}")
        await ctx.send(response)


def setup(bot, db):
    bot.add_cog(DailySubmissions(bot, db))
