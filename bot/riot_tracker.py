import json
import os
import logging
from bot.riot_api import get_player_by_puuid  # Use get_player_by_puuid

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
    return next((q for q in entries if q['queueType'] == 'RANKED_SOLO_5x5'), None)

def track_player_progress(puuid):
    tracked = load_tracked()

    # Fetch ranked data using PUUID directly
    ranked_data = get_player_by_puuid(puuid)  # Use PUUID directly
    if not ranked_data:
        logger.error(f"Failed to retrieve ranked data for PUUID {puuid}")
        return "⚠️ Failed to retrieve ranked data from Riot API."

    solo = get_solo_queue_entry(ranked_data)

    if not solo:
        return f"⚠️ No solo queue data for this player."

    current = {
        "tier": solo['tier'],
        "rank": solo['rank'],
        "lp": solo['leaguePoints'],
        "wins": solo['wins'],
        "losses": solo['losses']
    }

    # Use summoner name as key for readability
    name_key = solo.get('summonerName', 'Unknown Summoner')

    if name_key not in tracked:
        tracked[name_key] = current
        save_tracked(tracked)
        return f"✅ Started tracking `{name_key}` at {current['tier']} {current['rank']} {current['lp']} LP ({current['wins']}W / {current['losses']}L)."

    prev = tracked[name_key]
    lp_change = current['lp'] - prev['lp']
    wins_change = current['wins'] - prev['wins']
    losses_change = current['losses'] - prev['losses']

    return (
        f"📊 `{name_key}` Progress:\n"
        f"Current: {current['tier']} {current['rank']} {current['lp']} LP ({current['wins']}W / {current['losses']}L)\n"
        f"Change: {lp_change:+} LP, {wins_change:+}W / {losses_change:+}L"
    )
