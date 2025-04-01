import os
import logging
from bot.riot_tracker import track_player_progress
from discord.ext import commands
from dotenv import load_dotenv
from bot.riot_api import get_player_id_by_name, get_player_by_id

# Load .env variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Initialize bot
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    logger.info(f'{bot.user} has connected to Discord!')

@bot.command()
async def summoner(ctx, *, name):
    """Lookup a summoner's rank by name."""
    summoner_id = get_player_id_by_name(name)
    if not summoner_id:
        await ctx.send("❌ Summoner not found.")
        return

    ranked_data = get_player_by_id(summoner_id)
    if not ranked_data:
        await ctx.send("⚠️ Could not retrieve ranked data.")
        return

    # Find solo queue entry
    solo = next((q for q in ranked_data if q['queueType'] == 'RANKED_SOLO_5x5'), None)
    if solo:
        await ctx.send(f"{solo['summonerName']} is **{solo['tier']} {solo['rank']}** with {solo['leaguePoints']} LP.")
    else:
        await ctx.send("🧾 No solo queue rank found.")

@bot.command()
async def trackrank(ctx, *, name):
    """Tracks a summoner's solo queue rank progress."""
    result = track_player_progress(name)
    await ctx.send(result)


def run_bot():
    token = os.getenv("DISCORD_TOKEN")
    bot.run(token)
