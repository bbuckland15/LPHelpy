import os
from dotenv import load_dotenv

load_dotenv()  # Load values from .env file

riotAPI = {
    'key': os.getenv("RIOT_API_KEY")
}
