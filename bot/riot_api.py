import logging
import requests
import config

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# Riot platform/region constants
PLATFORM_REGION = 'na1'
REGIONAL_ROUTING = 'americas'

def safe_api_call(func, *args, **kwargs):
    """Helper to make safe Riot API calls with error handling."""
    try:
        return func(*args, **kwargs)
    except Exception as err:
        logger.error(f"API error: {err}")
    return None

import requests
import config

def get_summoner_by_puuid(puuid):
    """Returns summoner info from PUUID using the correct Riot API endpoint."""
    url = f"https://{PLATFORM_REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    headers = {
        "X-Riot-Token": config.riotAPI['key']
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            summoner_data = response.json()  # Parse the JSON response
            return summoner_data
        else:
            logger.error(f"API error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error making the request: {e}")
        return None

def get_ranked_data_by_puuid(puuid):
    """Returns ranked data from PUUID using the correct Riot API endpoint."""
    url = f"https://{PLATFORM_REGION}.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}"
    headers = {
        "X-Riot-Token": config.riotAPI['key']
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            ranked_data = response.json()  # Parse the JSON response
            # Ensure ranked data is a list
            if isinstance(ranked_data, list):
                return ranked_data
            else:
                logger.error(f"Expected a list for ranked data, but got {type(ranked_data)}")
                return None
        else:
            logger.error(f"API error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error making the request: {e}")
        return None


def get_player_puuid_by_riot_tag(name, tag):
    """Returns PUUID from Riot ID (name + tag)."""
    url = f"https://{REGIONAL_ROUTING}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}"
    headers = {
        "X-Riot-Token": config.riotAPI['key']
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            logger.info(f"Found PUUID for {name}#{tag}: {data['puuid']}")
            return data['puuid']
        else:
            logger.error(f"API error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error making the request: {e}")
        return None
