import discord
from discord.ext import commands
from config import *
import re

bot = commands.Bot(command_prefix=".", help_command=None, intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready!")

@bot.event
async def on_message(message : discord.Message):
    if not message.author.bot:
        if "https://www.ebay" in message.content:
            if match := ebay(message.content):
                await message.delete()
                url = f"**{message.author.mention} has posted an eBay link:**\n{match[0]+EBAY}"
                await message.channel.send(url)
        elif "https://www.amazon" in message.content:
            if match := amazon(message.content):
                await message.delete()
                url = f"**{message.author.mention} has posted an Amazon link:**\n{match[0]+AMAZON_CA if 'amazon.ca' in match[0] else match[0]+AMAZON}"
                await message.channel.send(url)            

def ebay(input_text):
    pattern = re.compile(r"https://www.ebay.+([a-z]+)+/itm/+([0-9]+)")
    return pattern.match(input_text)

def amazon(input_text):
    pattern = re.compile(r"https://www.amazon.+([a-z]+)+/+([a-zA-Z0-9_-]+)/dp/+([a-zA-Z0-9]+)")
    return pattern.search(input_text)

bot.run(TOKEN)