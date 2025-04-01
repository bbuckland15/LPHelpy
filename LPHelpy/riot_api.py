import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_summoner_data(summoner_name):
    API_KEY = os.getenv("RIOT_API_KEY")
    url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
    headers = {
        "X-Riot-Token": API_KEY
    }
    response = requests.get(url, headers=headers)
    return response.json()
