import json
import time
import cloudscraper
import random
import os
from bs4 import BeautifulSoup

# Configuración de Archivos
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
CHAMPIONS_FILE = os.path.join(DATA_DIR, 'champions.json')

def load_champions():
    with open(CHAMPIONS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_champions(data):
    with open(CHAMPIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def scrape_matchups_for_champion(scraper, champ_id, champ_name):
    # Formatear el nombre (Aurelion Sol -> aurelionsol, Nunu & Willump -> nunu)
    # Algunos casos especiales: Wukong es monkeyking en algunos sitios, pero en LoG es wukong.
    clean_name = champ_name.lower().replace(' ', '').replace("'", "").replace(".", "")
    if clean_name == "nunu&willump": clean_name = "nunu"
    if clean_name == "renataglasc": clean_name = "renata"
    # Ambessa / Aurora / Mel ya son de 1 palabra.
    
    url = f"https://www.leagueofgraphs.com/champions/counters/{clean_name}"
    
    matchups = {}
    try:
        response = scraper.get(url, timeout=12)
        if response.status_code != 200:
            print(f"[!] HTTP {response.status_code} para {champ_name}. Saltando...")
            return matchups

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscar la tabla estática de enfrentamientos
        tables = soup.find_all('table', class_='data_table')
        if not tables:
            print(f"[!] No table found in DOM for {champ_name}")
            return matchups
            
        for table in tables:
            rows = table.find_all('tr')
            for row in rows[1:]: # Saltar header
                cols = row.find_all('td')
                if len(cols) >= 3:
                    enemy_name_block = cols[1].find('span', class_='name')
                    if not enemy_name_block:
                        continue
                        
                    enemy_name = enemy_name_block.text.strip()
                    
                    winrate_block = cols[2].find('progressbar')
                    if not winrate_block:
                        winrate_text = cols[2].text.strip()
                    else:
                        winrate_text = winrate_block.get('data-value', '50.0')

                    try:
                        winrate_float = float(winrate_text.replace('%', ''))
                        matchups[enemy_name] = round(winrate_float / 100.0, 3)
                    except ValueError:
                        continue

    except Exception as e:
        print(f"[ERROR] Extrayendo a {champ_name}: {str(e)}")

    return matchups

def run_scraper():
    print("====================================")
    print(" INICIANDO SCRAPER XAI (CLOUDSCRAPER) ")
    print("====================================")
    
    champions_data = load_champions()
    total = len(champions_data)
    
    # Iniciar bypasser de CloudFlare
    scraper = cloudscraper.create_scraper()
    
    current = 1
    for champ_id, details in champions_data.items():
        print(f"[{current}/{total}] Scrapeando reales de {details['name']}...")
        
        if 'matchups' not in details:
            details['matchups'] = {}
            
        real_matchups = scrape_matchups_for_champion(scraper, champ_id, details['name'])
        
        if real_matchups:
            # Pisar las heuristicas con los datos REALES
            details['matchups'] = real_matchups
            print(f"  |-> Extraídos {len(real_matchups)} counters reales.")
        else:
            print(f"  |-> No se encontraron. Conservará heurística o base 50%.")
            
        # Guardar iterativo por si falla a medias
        save_champions(champions_data)
        
        time.sleep(1.0) # Rapido pero estable (1 seg)
        current += 1

    print("\n[✔] WINRATES REALES INYECTADOS CORRECTAMENTE.")

if __name__ == "__main__":
    run_scraper()
