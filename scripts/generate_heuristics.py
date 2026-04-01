import json
import random
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
CHAMPIONS_FILE = os.path.join(DATA_DIR, 'champions.json')

def load_champions():
    with open(CHAMPIONS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_champions(data):
    with open(CHAMPIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Matriz de Modificadores Heurísticos (Rock-Paper-Scissors Extendido de League of Legends)
# Determina la VENTAJA BASE que tiene un Tag sobre otro.
CLASS_ADVANTAGES = {
    'assassin': {'marksman': 0.05, 'mage': 0.03, 'tank': -0.04, 'fighter': -0.02},
    'tank': {'assassin': 0.04, 'fighter': -0.01, 'mage': 0.02, 'marksman': -0.04},
    'marksman': {'tank': 0.04, 'fighter': 0.03, 'assassin': -0.05, 'mage': -0.02},
    'mage': {'marksman': 0.02, 'fighter': 0.04, 'assassin': -0.03, 'tank': -0.02},
    'fighter': {'tank': 0.01, 'assassin': 0.02, 'mage': -0.04, 'marksman': -0.03},
    'support': {'assassin': -0.02, 'fighter': -0.01} # Supports escalan distinto
}

def calculate_heuristic_winrate(champ_tags, enemy_tags):
    """Calcula el winrate base heurístico cruzando todos los tags de A vs B."""
    base_winrate = 0.50 # Comienzan equilibrados
    
    for c_tag in champ_tags:
        if c_tag in CLASS_ADVANTAGES:
            for e_tag in enemy_tags:
                if e_tag in CLASS_ADVANTAGES[c_tag]:
                    base_winrate += CLASS_ADVANTAGES[c_tag][e_tag]
    
    # Ruido matemático sintético (Realismo para el TFG)
    # Variación del +/- 1.5% aleatoria para que no todos los magos vs asesinos sean idénticos
    noise = random.uniform(-0.015, 0.015)
    
    # Acotar máximo entre 40% (0.4) y 60% (0.6) que es el standard real de League
    final_wr = max(0.40, min(0.60, base_winrate + noise))
    return round(final_wr, 3)

def generate_expert_system_matchups():
    print("====================================")
    print(" GENERADOR HEURÍSTICO DE SINERGIA ")
    print("====================================")
    
    data = load_champions()
    champs = list(data.keys())
    
    total_matchups = 0
    
    for champ_id, details in data.items():
        champ_tags = details.get('tags', [])
        matchups = {}
        
        for enemy_id in champs:
            if champ_id == enemy_id:
                continue # No juega contra si mismo
            
            enemy_tags = data[enemy_id].get('tags', [])
            
            # Calculamos Winrate (A vs B)
            wr = calculate_heuristic_winrate(champ_tags, enemy_tags)
            matchups[data[enemy_id]['name']] = wr
            total_matchups += 1
            
        details['matchups'] = matchups
        print(f"[*] Set Heurístico 171x1 vs {details['name']} inyectado.")
    
    save_champions(data)
    print(f"\n[✔] ÉXITO: {total_matchups} Matchups generados al instante y guardados en JSON.")

if __name__ == "__main__":
    generate_expert_system_matchups()
