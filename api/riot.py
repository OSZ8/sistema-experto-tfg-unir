import requests
import os

API_KEY = os.getenv("RIOT_API_KEY", "RGAPI-3d95ba04-1787-43a8-800c-3e4531e6a4d6")
HEADERS = {"X-Riot-Token": API_KEY}
REGION = "euw1"
ROUTING = "europe"

def get_league_entries(tier="EMERALD", division="I", page=1):
    url = f"https://{REGION}.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/{tier}/{division}?page={page}"
    return requests.get(url, headers=HEADERS).json()

def get_match_ids(puuid, count=20):
    url = f"https://{ROUTING}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue=420&count={count}"
    return requests.get(url, headers=HEADERS).json()

def get_match_detail(match_id):
    url = f"https://{ROUTING}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    return requests.get(url, headers=HEADERS).json()
