import os
from dotenv import load_dotenv
from discord.ext import commands
from db import Database
from loguru import logger
from tabulate import tabulate


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
db = Database()

bot = commands.Bot(command_prefix='!')


@bot.command(name='submit')
async def submit(ctx):
    """Create new submission entry for message author in database"""
    author = ctx.author.name
    message = ctx.message

    db.add_submission(author)
    try:
        img_url = message.attachments[0].url
        logger.debug(f"Image URL from message: {img_url}")
    except IndexError:
        logger.debug(f"No image in message")

    response = f"Submitted ({db.get_weekly_user_count(author)}/6)"
    logger.info(f"Responding: {response}")
    await ctx.send(response)


@bot.command(name='summary')
async def summary(ctx):
    """Print the weekly submission count of all participants."""
    df = db.get_weekly_summary()
    response = tabulate(df, tablefmt='psql', showindex=False)
    response = "```\nWeekly Summary\n" + response + "\n```"
    logger.info(f"Responding:\n{response}")
    await ctx.send(response)


if __name__ == '__main__':
    bot.run(TOKEN)
