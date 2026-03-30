import requests
from bs4 import BeautifulSoup
import json
import os

def mock_scrape_winrates():
    """
    Este script simula o hace proof-of-concept de la recolección de estadísticas (Counters) desde webs de terceros.
    
    ¿Por qué usamos raspado web y no base de datos nativas?
    Para recoger datos de enfrentamientos estructurados requeriríamos un clúster de Big Data que procese la API de Riot continuamente,
    algo insostenible para el alcance de un TFG monousuario.
    """
    print("Iniciando Módulo de Web Scraper...")
    
    # Directorio y Base de Datos (JSON)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    champions_path = os.path.join(base_dir, 'data', 'champions.json')
    
    if os.path.exists(champions_path):
        with open(champions_path, 'r', encoding='utf-8') as f:
            local_champs = json.load(f)
    else:
        print("La base de hechos no existe. Ejecuta primero fetch_datadragon.py")
        return

    # A nivel de PoC Académica (no se puede desatar un robot masivo), se muestran los métodos de extracción:
    print("Scrapeando U.GG / OP.GG para extraer matrices de Matchup y Win Rates...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Academia/TFG'
    }

    # Aquí iría el código real (Que podría vulnerar ToS o requerir JavaScript rendering con Selenium)
    '''
    # Ejemplo de Extracción:
    for champ_id in local_champs.keys():
        url = f"https://u.gg/lol/champions/{champ_id.lower()}/counter"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extraer las tablas de counters...
            # best_winrate_against = soup.select_one('.counter-wr').text 
    '''
    
    # Inyectando datos sintéticos de demostración del script ETL:
    if "Teemo" in local_champs:
        local_champs["Teemo"]["base_winrate"] = 51.5
        local_champs["Teemo"]["matchups"] = {
            "Garen": 55.2,
            "Tryndamere": 53.0
        }
    
    # Guardado de Base de Hechos
    with open(champions_path, 'w', encoding='utf-8') as f:
        json.dump(local_champs, f, indent=4, ensure_ascii=False)
        
    print("Módulo de Scraping y Carga (Data Lake) finalizado exitosamente.")

if __name__ == "__main__":
    mock_scrape_winrates()
