import json
import os
import logging
from bot.riot_api import get_player_puuid_by_riot_tag, get_ranked_data_by_puuid, get_summoner_by_puuid


# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

TRACK_FILE = "tracked_players.json"

def load_tracked():
    if os.path.exists(TRACK_FILE):
        with open(TRACK_FILE, "r") as f:
            return json.load(f)
    return {}

def save_tracked(data):
    with open(TRACK_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_solo_queue_entry(entries):
    """Extracts the solo queue entry from the ranked data."""
    if entries is None:
        logger.error("No ranked data available")
        return None
    return next((q for q in entries if q['queueType'] == 'RANKED_SOLO_5x5'), None)

def track_player_progress(puuid):
    """Tracks the progress of the player by their PUUID."""
    tracked = load_tracked()

    # Fetch summoner data using PUUID
    summoner_data = get_summoner_by_puuid(puuid)  # Use get_summoner_by_puuid instead
    if not summoner_data:
        logger.error(f"Failed to retrieve summoner data for PUUID {puuid}")
        return "⚠️ Failed to retrieve summoner data from Riot API."

    # Fetch ranked data using PUUID
    ranked_data = get_ranked_data_by_puuid(puuid)
    if not ranked_data:
        logger.error(f"Failed to retrieve ranked data for PUUID {puuid}")
        return "⚠️ Failed to retrieve ranked data from Riot API."

    # Extract solo queue data
    solo = get_solo_queue_entry(ranked_data)
    if not solo:
        return f"⚠️ No solo queue data for this player."

    # Prepare current progress
    current = {
        "tier": solo['tier'],
        "rank": solo['rank'],
        "lp": solo['leaguePoints'],
        "wins": solo['wins'],
        "losses": solo['losses']
    }

    # Use summoner name as key for readability
    name_key = summoner_data.get('name', 'Unknown Summoner')

    if name_key not in tracked:
        tracked[name_key] = current
        save_tracked(tracked)
        return f"✅ Started tracking `{name_key}` at {current['tier']} {current['rank']} {current['lp']} LP ({current['wins']}W / {current['losses']}L)."

    # Track changes
    prev = tracked[name_key]
    lp_change = current['lp'] - prev['lp']
    wins_change = current['wins'] - prev['wins']
    losses_change = current['losses'] - prev['losses']

    return (
        f"📊 `{name_key}` Progress:\n"
        f"Current: {current['tier']} {current['rank']} {current['lp']} LP ({current['wins']}W / {current['losses']}L)\n"
        f"Change: {lp_change:+} LP, {wins_change:+}W / {losses_change:+}L"
    )
