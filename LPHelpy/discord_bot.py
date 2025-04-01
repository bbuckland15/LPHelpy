import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from bot.riot_api import get_summoner_data

load_dotenv()

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected!')

@bot.command()
async def summoner(ctx, *, name):
    data = get_summoner_data(name)
    if "status" in data:
        await ctx.send("Summoner not found.")
    else:
        await ctx.send(f"{data['name']} is level {data['summonerLevel']}")

def run_bot():
    token = os.getenv("DISCORD_TOKEN")
    bot.run(token)
