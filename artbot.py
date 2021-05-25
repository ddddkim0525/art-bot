# bot.py
import os
import pickle
import datetime
from dotenv import load_dotenv

# 1
import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# 2
intents = discord.Intents().default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)
filename = 'records'

@bot.command(name='setup')
async def scan(ctx):
    outfile = open(filename,'wb')
    members = {}
    for member in ctx.guild.members:
        members[member.name] = 0
        print(member.name)
    pickle.dump(members,outfile)
    outfile.close()
    await ctx.send("Setup Complete")

@bot.command(name='submit')
async def submit(ctx):
    infile = open(filename,'rb')
    members = pickle.load(infile)
    infile.close()
    author = ctx.author.name
    if datetime.datetime.today().weekday() == 0:
        for key in members:
            members[key] = 0
    members[author] += 1
    
    response = "Thanks " + author + "!"
    submit_count = members[author]
    response += f'\nSubmit Count: {submit_count}/6'
    if submit_count == 6:
        response += '\nCongratulations for another week of daily submissions!'
    elif submit_count > 6:
        response += '\nYou already satisfied the quota, but great job working on anyways!'
    outfile = open(filename,'wb')
    pickle.dump(members,outfile)
    outfile.close()

    await ctx.send(response)

@bot.command(name='set')
async def set(ctx, number):
    infile = open(filename,'rb')
    members = pickle.load(infile)
    infile.close()
    author = ctx.author.name
    members[author] = number
    outfile = open(filename,'wb')
    pickle.dump(members,outfile)
    outfile.close()

    await ctx.send(f'Set {author} count to {number}')
bot.run(TOKEN)