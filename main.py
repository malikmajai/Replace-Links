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
        if "https://www.amazon" in message.content or "www.ebay" in message.content:
            FOUND = False
            line = []
            for word in message.content.split(' '):
                if match := ebay_user(word):
                    line.append(f"{match[0] if match[0].startswith('https://') else 'https://'+match[0]+EBAY_USERNAME}")
                    name = 'Ebay Link'
                    FOUND = True
                elif match := ebay(word):
                    line.append(f"{match[0] if match[0].startswith('https://') else 'https://'+match[0]+EBAY}")
                    name = 'Ebay Link'
                    FOUND = True
                elif match := amazon(word):
                    match = match[0] if match[0].startswith('https://') else f'https://{match[0]}'
                    line.append(f"{match+AMAZON_CA if 'amazon.ca' in match else match+AMAZON}")
                    name = 'Amazon Link'
                    FOUND = True
                else:
                    line.append(word)
            if FOUND:
                await message.delete()
                new = ' '.join(line)
                await message.channel.send(f"**{message.author.mention} has posted an {name}:**\n{new}")

def ebay(input_text):
    pattern = re.compile(r"www.ebay.+([a-z]+)+/itm/+([0-9]+)")
    return pattern.search(input_text)

def ebay_user(input_text):
    pattern = re.compile(r"www.ebay.+([a-z]+)+/usr/+([a-zA-Z0-9]+)")
    return pattern.search(input_text)

def amazon(input_text):
    pattern = re.compile(r"www.amazon.+([a-z]+)+/+([a-zA-Z0-9_-]+)/dp/+([a-zA-Z0-9]+)")
    return pattern.search(input_text)

bot.run(TOKEN)
