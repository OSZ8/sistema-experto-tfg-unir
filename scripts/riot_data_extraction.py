import sys
import os
import time
import csv
from collections import defaultdict

# Añadir raíz del proyecto al path para importar api/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from api.riot import get_league_entries, get_match_ids, get_match_detail

# Extracción de matchups (Rango Esmeralda+) → exporta raw_matchups.csv

TOTAL_PLAYERS_TO_SCAN = 3
TOTAL_MATCHES_PER_PLAYER = 5


def get_emerald_players(page=1):
    print(f"Obteniendo jugadores Esmeralda (página {page})...")
    entries = get_league_entries(tier="EMERALD", division="I", page=page)
    if not isinstance(entries, list):
        print("Error al obtener jugadores.")
        return []
    players = []
    for entry in entries:
        pid = entry.get("puuid") or entry.get("summonerId")
        if pid:
            players.append(pid)
    return players


def analyze_match(match_id):
    data = get_match_detail(match_id)
    if 'info' not in data:
        return []

    positions = defaultdict(list)
    for p in data['info']['participants']:
        pos = p.get('teamPosition')
        if pos:
            positions[pos].append({'champion': p['championName'], 'win': p['win']})

    matchups = []
    for players in positions.values():
        if len(players) == 2:
            p1, p2 = players
            if p1['win']:
                matchups.append((p1['champion'], p2['champion']))
            elif p2['win']:
                matchups.append((p2['champion'], p1['champion']))
    return matchups


def main():
    print("Iniciando extracción de datos (Riot API)...")

    summoner_ids = get_emerald_players(page=1)
    stats = defaultdict(lambda: defaultdict(lambda: {"wins": 0, "losses": 0}))

    for i, pid in enumerate(summoner_ids[:TOTAL_PLAYERS_TO_SCAN]):
        print(f"\n[+] Jugador {i+1}/{TOTAL_PLAYERS_TO_SCAN} ({pid[:20]}...)")

        # Riot ya devuelve PUUID directamente en League V4
        puuid = pid if len(pid) > 65 else None
        if not puuid:
            time.sleep(1.2)
            continue

        match_ids = get_match_ids(puuid, count=TOTAL_MATCHES_PER_PLAYER)
        print(f"  Analizando {len(match_ids)} partidas...")

        for match_id in match_ids:
            time.sleep(1)
            for winner, loser in analyze_match(match_id):
                stats[winner][loser]["wins"] += 1
                stats[loser][winner]["losses"] += 1

        time.sleep(1.5)

    print("\nExtracción completada.")

    output_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'data', 'raw_matchups.csv'))
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['champion', 'enemy', 'wins', 'losses', 'total_games', 'winrate'])
        for champ, rivals in stats.items():
            for enemy, record in rivals.items():
                total = record["wins"] + record["losses"]
                if total > 0:
                    writer.writerow([champ, enemy, record["wins"], record["losses"], total, round(record["wins"] / total, 4)])

    print(f"Datos guardados en: {output_path}")


if __name__ == "__main__":
    main()
