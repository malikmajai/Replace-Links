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
        if "www.ebay" in message.content:
            if match := ebay_user(message.content):
                await message.delete()
                new = []
                words = message.content.split(' ')
                for word in words:
                    if 'www.ebay' in word:
                        new.append(f"{match[0] if match[0].startswith('https://') else 'https://'+match[0]+EBAY_USERNAME}")
                    else:
                        new.append(word)
                new = ' '.join(new)
                await message.channel.send(f"**{message.author.mention} has posted an eBay Profile:**\n{new}")

            elif match := ebay(message.content):
                await message.delete()
                new = []
                words = message.content.split(' ')
                for word in words:
                    if 'www.ebay' in word:
                        new.append(f"{match[0] if match[0].startswith('https://') else 'https://'+match[0]+EBAY}")
                    else:
                        new.append(word)
                new = ' '.join(new)
                await message.channel.send(f"**{message.author.mention} has posted an eBay link:**\n{new}")
            
        elif "https://www.amazon" in message.content:
            if match := amazon(message.content):
                await message.delete()
                new = []
                words = message.content.split(' ')
                for word in words:
                    if 'www.amazon' in word:
                        match = match[0] if match[0].startswith('https://') else f'https://{match[0]}'
                        new.append(f"{match+AMAZON_CA if 'amazon.ca' in match else match+AMAZON}")
                    else:
                        new.append(word)
                new = ' '.join(new)
                await message.channel.send(f"**{message.author.mention} has posted an Amazon link:**\n{new}")

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
