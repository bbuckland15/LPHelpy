import os
import logging
import hikari  
import lightbulb
from dotenv import load_dotenv
from bot.riot_api import get_player_puuid_by_riot_tag, get_ranked_data_by_puuid
from bot.riot_tracker import track_player_progress

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Initialize Lightbulb Bot
bot = lightbulb.BotApp(
    token=os.getenv("DISCORD_TOKEN"),
    prefix="!",
    intents=hikari.Intents.ALL,  # Use hikari.Intents.ALL for intents
    default_enabled_guilds=(854544102917931018,)  # Your server ID for faster slash command syncing
)

# Slash command: trackrank
@bot.command()
@lightbulb.option("tag", "Summoner tag (e.g. NA1)", type=str)
@lightbulb.option("name", "Summoner name (e.g. Faker)", type=str)
@lightbulb.command("trackrank", "Track a summoner's ranked progress")
@lightbulb.implements(lightbulb.SlashCommand)
async def trackrank(ctx: lightbulb.Context) -> None:
    name = ctx.options.name
    tag = ctx.options.tag

    # Fetch PUUID using the Riot ID (name and tag)
    puuid = get_player_puuid_by_riot_tag(name, tag)
    if not puuid:
        await ctx.respond("❌ Summoner not found via Riot ID.")
        return

    # Track progress directly using PUUID
    result = track_player_progress(puuid)  # Pass PUUID directly
    await ctx.respond(result)

# Slash command: summoner
@bot.command()
@lightbulb.option("tag", "Summoner tag (e.g. KR1)", type=str)
@lightbulb.option("name", "Summoner name (e.g. Faker)", type=str)
@lightbulb.command("summoner", "Get summoner level by Riot ID")
@lightbulb.implements(lightbulb.SlashCommand)
async def summoner(ctx: lightbulb.Context) -> None:
    name = ctx.options.name
    tag = ctx.options.tag

    # Fetch PUUID using the Riot ID (name and tag)
    puuid = get_player_puuid_by_riot_tag(name, tag)
    if not puuid:
        await ctx.respond("❌ Summoner not found via Riot ID.")
        return

    # Get ranked data using PUUID directly
    ranked_data = get_ranked_data_by_puuid(puuid)  # Use PUUID directly
    if not ranked_data:
        await ctx.respond("⚠️ Could not retrieve ranked data.")
        return

    solo = next((q for q in ranked_data if q['queueType'] == 'RANKED_SOLO_5x5'), None)
    if solo:
        await ctx.respond(f"{solo['summonerName']} is **{solo['tier']} {solo['rank']}** with {solo['leaguePoints']} LP.")
    else:
        await ctx.respond("🧾 No solo queue data found.")
