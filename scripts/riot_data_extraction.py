import requests
import time
import json
import os
from collections import defaultdict

# Extracción de matchups de la API de Riot (Rango Esmeralda+)
# Procesa el historial de jugadores para calcular Win Rates reales.

# API Key
API_KEY = "RGAPI-3d95ba04-1787-43a8-800c-3e4531e6a4d6"

# Endpoints estandarizados
REGION = "euw1" # Usado para invocadores y ligas
ROUTING = "europe" # Usado para las partidas (Match V5)

HEADERS = {
    "X-Riot-Token": API_KEY
}

def get_emerald_players(page=1):
    """
    Obtiene una página de jugadores en la liga ESMERALDA I.
    Retorna una lista de Summoner IDs.
    """
    print(f"[1] Obteniendo jugadores Esmeralda (Página {page})...")
    url = f"https://{REGION}.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/EMERALD/I?page={page}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        entries = response.json()
        # Riot Games API updates replaced summonerId with puuid in some endpoints.
        # We try to get puuid first, otherwise summonerId.
        players = []
        for entry in entries:
            pid = entry.get("puuid") or entry.get("summonerId")
            if pid:
                players.append(pid)
        return players
    else:
        print(f"Error {response.status_code} al obtener jugadores.")
        return []

def get_puuid_by_summoner_id(summoner_id):
    """
    Convierte el Summoner ID a PUUID, que es el identificador requerido 
    para la API de historiales de partidas (Match V5).
    """
    url = f"https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        return response.json().get("puuid")
    return None

def get_recent_matches(puuid, count=50):
    """
    Obtiene los IDs de las últimas partidas clasificatorias de un jugador.
    Se filtra por queue=420 (Ranked Solo/Duo). En producción 'count' rondaría las 100 partidas.
    """
    url = f"https://{ROUTING}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue=420&start=0&count={count}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        return response.json()
    return []

def analyze_match_for_matchups(match_id):
    """
    Descarga el detalle de la partida, identifica qué campeones se enfrentaron 
    en la misma posición (por ejemplo, TOP vs TOP) y determina quién ganó.
    """
    url = f"https://{ROUTING}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        return []

    match_data = response.json()
    participants = match_data['info']['participants']
    
    # Agrupar participantes por posición (TOP, JUNGLE, MID, BOTTOM, UTILITY)
    positions = defaultdict(list)
    for p in participants:
        pos = p.get('teamPosition')
        if pos:  # Ignorar posiciones inválidas ("" o None)
            positions[pos].append({
                "champion": p['championName'],
                "win": p['win']
            })
            
    matchups = []
    # Analizar quién le ganó a quién en cada línea
    for pos, players in positions.items():
        if len(players) == 2:
            p1, p2 = players[0], players[1]
            if p1['win']:
                matchups.append({"winner": p1['champion'], "loser": p2['champion'], "lane": pos})
            elif p2['win']:
                matchups.append({"winner": p2['champion'], "loser": p1['champion'], "lane": pos})
                
    return matchups

def main():
    print("Iniciando extracción de datos (Riot API)...")
    
    # 1. Obtenemos un bloque de jugadores de Esmeralda (La paginación permite recorrer miles de jugadores)
    summoner_ids = get_emerald_players(page=1)
    
    # Estructura para almacenar estadísticas globales (Memoria/Consolidado)
    # Ejemplo: stats["Aatrox"]["Darius"] = {"wins": 10, "losses": 5}
    stats = defaultdict(lambda: defaultdict(lambda: {"wins": 0, "losses": 0}))
    
    # IMPORTANTE PARA EL TFG: 
    # Aquí se limitan los parámetros para poder hacer una demostración en vivo o evitar superar
    # el Rate Limit de la API en modo desarrollo de forma innecesaria.
    TOTAL_PLAYERS_TO_SCAN = 3
    TOTAL_MATCHES_PER_PLAYER = 5
    
    for i, summoner_id in enumerate(summoner_ids[:TOTAL_PLAYERS_TO_SCAN]):
        print(f"\n[+] Procesando Jugador {i+1}/{TOTAL_PLAYERS_TO_SCAN} (Summoner ID: {summoner_id})")
        
        # Si la API ya nos devolvió el PUUID, no hace falta buscarlo (Riot Games actualizó esto recientemente)
        if len(summoner_id) > 65:
            puuid = summoner_id
        else:
            puuid = get_puuid_by_summoner_id(summoner_id)
            
        if not puuid:
            print("  [!] No se pudo obtener el PUUID. Respetando el Rate limit y saltando...")
            time.sleep(1.2) 
            continue
            
        matches = get_recent_matches(puuid, count=TOTAL_MATCHES_PER_PLAYER)
        print(f"  Analizando {len(matches)} partidas recientes...")
        
        for match_id in matches:
            # Rate limit: Riot API permite ~20 peticiones/seg. Ponemos sleep para evitar HTTP 429
            time.sleep(1) 
            matchups_in_game = analyze_match_for_matchups(match_id)
            
            # Registrar victorias y derrotas en nuestra base de datos para promediar los winrates reales
            for m in matchups_in_game:
                winner = m['winner']
                loser = m['loser']
                
                # Win para el ganador
                stats[winner][loser]["wins"] += 1
                # Loss para el perdedor
                stats[loser][winner]["losses"] += 1
                
        time.sleep(1.5) # Pausa estratégica tras cada jugador
        
    print("\nExtracción completada.")
    
    # Simulación de la escritura en un formato útil (similar a lo que acabaría en champions.json)
    for champ, matchups_record in list(stats.items())[:5]: # Mostramos 5 personajes a modo de ejemplo
        for enemy, record in matchups_record.items():
            total_games = record["wins"] + record["losses"]
            if total_games > 0:
                win_rate = (record["wins"] / total_games) * 100
                print(f"[{champ} vs {enemy}] Muestras: {total_games} | Win Rate {champ}: {win_rate:.1f}%")

if __name__ == "__main__":
    main()
