import json
import os

matchups = {
    "Shyvana": 0.5887,
    "Wukong": 0.555,
    "Trundle": 0.5409,
    "Nasus": 0.5356,
    "Dr. Mundo": 0.5307,
    "Warwick": 0.5258,
    "Illaoi": 0.5212,
    "Cho'Gath": 0.5197,
    "Rumble": 0.518,
    "Sett": 0.5155,
    "Vladimir": 0.5153,
    "Poppy": 0.515,
    "Volibear": 0.5147,
    "Olaf": 0.5132,
    "Zaahen": 0.5102,
    "Gwen": 0.5097,
    "Sion": 0.509,
    "Tryndamere": 0.5076,
    "Ornn": 0.5068,
    "Gangplank": 0.5051,
    "Varus": 0.5048,
    "K'Sante": 0.5042,
    "Shen": 0.5023,
    "Yorick": 0.5015,
    "Tahm Kench": 0.5013,
    "Akali": 0.5008,
    "Jax": 0.5004,
    "Riven": 0.5,
    "Yasuo": 0.4983,
    "Gragas": 0.4978,
    "Darius": 0.4971,
    "Garen": 0.4929,
    "Jayce": 0.4916,
    "Gnar": 0.4913,
    "Kled": 0.4897,
    "Renekton": 0.4885,
    "Pantheon": 0.4881,
    "Kayle": 0.4881,
    "Urgot": 0.4855,
    "Teemo": 0.4836,
    "Camille": 0.4798,
    "Mordekaiser": 0.4776,
    "Yone": 0.4772,
    "Ambessa": 0.4758,
    "Irelia": 0.4746,
    "Malphite": 0.471,
    "Vayne": 0.4704,
    "Fiora": 0.4677,
    "Kennen": 0.4461,
    "Singed": 0.4382
}

json_path = 'c:/Users/Oscar/Documents/GitHub/sistema-experto-tfg-unir/data/champions.json'

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

if "Aatrox" in data:
    data["Aatrox"]["matchups"] = matchups
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Matchups de Aatrox actualizados de forma limpia: {len(matchups)} rivales.")

try:
    os.remove(__file__)
except Exception:
    pass
