import requests
import json
import os

def fetch_latest_version():
    """Obtiene el último parche de DataDragon."""
    url = "https://ddragon.leagueoflegends.com/api/versions.json"
    response = requests.get(url)
    if response.status_code == 200:
        versions = response.json()
        return versions[0]
    return "14.1.1" # Fallback

def sync_champions(version):
    """Descarga campeones de DataDragon y fusiona con datos locales."""
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/es_ES/champion.json"
    print(f"Buscando datos estáticos en DataDragon (Versión {version})...")
    
    response = requests.get(url)
    if response.status_code != 200:
        print("Error al descargar los datos de DataDragon.")
        return

    data = response.json()
    champions_data = data['data']
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    champions_path = os.path.join(base_dir, 'data', 'champions.json')
    
    local_champs = {}
    if os.path.exists(champions_path):
        with open(champions_path, 'r', encoding='utf-8') as f:
            local_champs = json.load(f)

    updated_champs = {}
    
    for champ_id, champ_info in champions_data.items():
        name = champ_info['name']
        tags = [tag.lower() for tag in champ_info.get('tags', [])]
        
        existing = local_champs.get(champ_id, {})

        # Fusiona tags Riot con tags custom
        custom_tags = existing.get('tags', [])
        combined_tags = list(set(tags + custom_tags))
        
        updated_champs[champ_id] = {
            "id": champ_id,
            "name": existing.get('name', name),
            "role": existing.get('role', tags[0] if tags else 'Unknown'),
            "tags": combined_tags,
            "base_winrate": existing.get('base_winrate', 50.0),
            "matchups": existing.get('matchups', {})
        }
    
    with open(champions_path, 'w', encoding='utf-8') as f:
        json.dump(updated_champs, f, indent=4, ensure_ascii=False)
        
    print(f"Éxito: Se han sincronizado {len(updated_champs)} campeones en 'data/champions.json'.")
    print("Nota: Los winrates, matchups y custom tags asignados manualmente se han conservado intactos.")

if __name__ == "__main__":
    latest_version = fetch_latest_version()
    sync_champions(latest_version)
    print("Sincronización mediante Riot DataDragon (Script 1) Finalizada.")
