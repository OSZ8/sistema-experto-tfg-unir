import requests
import os

# Esto simula cómo se cargarían las variables de entorno de .env
from dotenv import load_dotenv
load_dotenv()

# IMPORTANTE: Reemplaza esto en el archivo .env
API_KEY = os.getenv("RIOT_API_KEY", "RGAPI-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
REGION = os.getenv("REGION", "euw1")

def get_puuid_by_riot_id(game_name, tag_line):
    """
    Llama a la API de Account-v1 para conseguir el PUUID universal de la cuenta
    """
    url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}?api_key={API_KEY}"
    print(f"Llamando a {url}")
    return "MOCK-PUUID-12345" # Devuelve dato Mock en caso de no tener API key real

def get_recent_matches(puuid, count=5):
    """
    Devuelve las últimas N partidas jugadas por este ID (Match V5)
    """
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}&api_key={API_KEY}"
    print(f"Llamando a {url}")
    return ["EUW1_12345678", "EUW1_87654321"]

def analyze_matchup_in_match(match_id):
    """
    Examina los detalles de la partida para procesar qué campeón ganó contra quién en el rol.
    """
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={API_KEY}"
    print(f"Llamando a {url}")
    print(f"Analizando estadísticas de oro al minuto 15 para la Top Lane...")
    # Código demostrativo que extraería y procesaría los eventos
    return {"campeon_ganador": "Malphite", "campeon_perdedor": "Tryndamere", "winrate_impact": 1}

def prototype_pipeline():
    """
    Flujo base para calcular dinámicamente WinRates (Omitido en la app final por la cuota de peticiones).
    - Rate Limits Dev Key de Riot API: 20 pet. / s y 100 pet. / min.
    - Para analizar una muestra de 50.000 partidas, se tardarían horas/días con la Key base,
      por eso se descarta en favor del ETL propuesto (Web Scraping). 
    """
    print("--- [POC] Riot API Match v5 Analytics Pipeline ---")
    
    # 1. Traer PUUID del jugador (Top Challenger de EUW)
    puuid = get_puuid_by_riot_id("Hide on bush", "KR1")
    
    # 2. Descargar lote de 10 últimas partidas
    matches = get_recent_matches(puuid, 10)
    
    print("\nSimulando Análisis en Stream de Partidas:")
    for m in matches:
        analyze_matchup_in_match(m)
        
    print("\n[INFO] PoC Completado. Limitaciones del sistema justificadas para Memoria TFG.")

if __name__ == "__main__":
    prototype_pipeline()
