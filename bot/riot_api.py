import logging
from riotwatcher import LolWatcher, RiotWatcher, ApiError
import config

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# Shared API instances
lol_watcher = LolWatcher(config.riotAPI['key'])
riot_watcher = RiotWatcher(config.riotAPI['key'])

# Riot platform/region constants
PLATFORM_REGION = 'na1'       # Summoner, League, etc.
REGIONAL_ROUTING = 'americas' # Match, Account, etc.

def safe_api_call(func, *args, **kwargs):
    """Helper to make safe Riot API calls with error handling."""
    try:
        return func(*args, **kwargs)
    except ApiError as err:
        logger.error(f"API error: {err}")
    except Exception as e:
        logger.exception(f"Unexpected error during API call")
    return None

def get_player_by_id(summoner_id):
    """Returns ranked info from encrypted Summoner ID."""
    return safe_api_call(lol_watcher.league.by_summoner, PLATFORM_REGION, summoner_id)

def get_player_id_by_name(name):
    """Returns encrypted Summoner ID from summoner name."""
    data = safe_api_call(lol_watcher.summoner.by_name, PLATFORM_REGION, name)
    if data:
        logger.info(f"Found ID for {name}: {data['id']}")
        return data['id']
    return None

def get_player_puuid_by_riot_tag(name, tag):
    """Returns PUUID from Riot ID (name + tag)."""
    data = safe_api_call(riot_watcher.account.by_riot_id, REGIONAL_ROUTING, name, tag)
    if data:
        logger.info(f"Found PUUID for {name}#{tag}: {data['puuid']}")
        return data['puuid']
    return None

def get_player_id_by_puuid(puuid):
    """Returns encrypted Summoner ID from a PUUID."""
    data = safe_api_call(lol_watcher.summoner.by_puuid, PLATFORM_REGION, puuid)
    if data:
        logger.info(f"Found Summoner ID for PUUID {puuid}: {data['id']}")
        return data['id']
    return None
