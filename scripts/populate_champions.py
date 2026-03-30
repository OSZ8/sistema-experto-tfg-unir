import json
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
champs_path = os.path.join(base_dir, 'data', 'champions.json')

with open(champs_path, 'r', encoding='utf-8') as f:
    champions = json.load(f)

new_champs = {
    "Darius": {"id": "Darius", "name": "Darius", "role": "Top", "tags": ["bruiser", "physical_damage", "tank_melter"], "base_winrate": 50.1, "matchups": {"Malphite": 47.0}},
    "Garen": {"id": "Garen", "name": "Garen", "role": "Top", "tags": ["bruiser", "tank", "physical_damage"], "base_winrate": 51.2, "matchups": {"Darius": 48.0}},
    "Shen": {"id": "Shen", "name": "Shen", "role": "Top", "tags": ["tank", "engage", "magic_damage"], "base_winrate": 49.8, "matchups": {}},
    "Fiora": {"id": "Fiora", "name": "Fiora", "role": "Top", "tags": ["fighter", "true_damage", "healing_self"], "base_winrate": 50.5, "matchups": {"Aatrox": 52.0}},
    "Ornn": {"id": "Ornn", "name": "Ornn", "role": "Top", "tags": ["tank", "engage", "cc_heavy"], "base_winrate": 50.0, "matchups": {}},
    "Amumu": {"id": "Amumu", "name": "Amumu", "role": "Jungle", "tags": ["tank", "engage", "cc_heavy", "magic_damage"], "base_winrate": 51.5, "matchups": {}},
    "XinZhao": {"id": "XinZhao", "name": "Xin Zhao", "role": "Jungle", "tags": ["bruiser", "physical_damage", "engage"], "base_winrate": 50.3, "matchups": {}},
    "Vi": {"id": "Vi", "name": "Vi", "role": "Jungle", "tags": ["bruiser", "engage", "physical_damage"], "base_winrate": 49.5, "matchups": {}},
    "Khazix": {"id": "Khazix", "name": "Kha'Zix", "role": "Jungle", "tags": ["assassin", "physical_damage", "mobility"], "base_winrate": 50.2, "matchups": {}},
    "Rammus": {"id": "Rammus", "name": "Rammus", "role": "Jungle", "tags": ["tank", "armor_stacking", "engage"], "base_winrate": 51.0, "matchups": {"Jinx": 55.0, "Vayne": 42.0, "Yasuo": 54.0}},
    "Ahri": {"id": "Ahri", "name": "Ahri", "role": "Mid", "tags": ["mage", "magic_damage", "mobility", "assassin"], "base_winrate": 50.8, "matchups": {"Yasuo": 48.0}},
    "Yasuo": {"id": "Yasuo", "name": "Yasuo", "role": "Mid", "tags": ["fighter", "physical_damage", "critical_strike", "mobility"], "base_winrate": 49.0, "matchups": {"Ahri": 52.0}},
    "Zed": {"id": "Zed", "name": "Zed", "role": "Mid", "tags": ["assassin", "physical_damage", "mobility"], "base_winrate": 48.5, "matchups": {}},
    "Orianna": {"id": "Orianna", "name": "Orianna", "role": "Mid", "tags": ["mage", "magic_damage", "shielding"], "base_winrate": 49.5, "matchups": {"Zed": 47.0}},
    "Syndra": {"id": "Syndra", "name": "Syndra", "role": "Mid", "tags": ["mage", "magic_damage", "cc_heavy"], "base_winrate": 50.0, "matchups": {}},
    "Ashe": {"id": "Ashe", "name": "Ashe", "role": "ADC", "tags": ["marksman", "physical_damage", "cc_heavy", "engage"], "base_winrate": 51.0, "matchups": {}},
    "Ezreal": {"id": "Ezreal", "name": "Ezreal", "role": "ADC", "tags": ["marksman", "physical_damage", "mobility"], "base_winrate": 48.5, "matchups": {}},
    "Jhin": {"id": "Jhin", "name": "Jhin", "role": "ADC", "tags": ["marksman", "physical_damage", "critical_strike"], "base_winrate": 50.5, "matchups": {}},
    "Caitlyn": {"id": "Caitlyn", "name": "Caitlyn", "role": "ADC", "tags": ["marksman", "physical_damage", "critical_strike"], "base_winrate": 49.8, "matchups": {"Vayne": 52.0}},
    "Kaisa": {"id": "Kaisa", "name": "Kai'Sa", "role": "ADC", "tags": ["marksman", "magic_damage", "physical_damage", "assassin", "mobility"], "base_winrate": 50.2, "matchups": {}},
    "Thresh": {"id": "Thresh", "name": "Thresh", "role": "Support", "tags": ["tank", "engage", "cc_heavy", "shielding"], "base_winrate": 49.5, "matchups": {"Leona": 51.0}},
    "Lulu": {"id": "Lulu", "name": "Lulu", "role": "Support", "tags": ["enchanter", "magic_damage", "shielding"], "base_winrate": 50.0, "matchups": {}},
    "Blitzcrank": {"id": "Blitzcrank", "name": "Blitzcrank", "role": "Support", "tags": ["tank", "engage", "cc_heavy"], "base_winrate": 51.2, "matchups": {"Soraka": 54.0}},
    "Nautilus": {"id": "Nautilus", "name": "Nautilus", "role": "Support", "tags": ["tank", "engage", "cc_heavy"], "base_winrate": 50.5, "matchups": {}},
    "Nami": {"id": "Nami", "name": "Nami", "role": "Support", "tags": ["enchanter", "healing_support", "magic_damage", "cc_heavy"], "base_winrate": 50.8, "matchups": {}},
    "Katarina": {"id": "Katarina", "name": "Katarina", "role": "Mid", "tags": ["assassin", "magic_damage", "mobility"], "base_winrate": 49.5, "matchups": {"Yasuo": 45.0}}
}

champions.update(new_champs)

with open(champs_path, 'w', encoding='utf-8') as f:
    json.dump(champions, f, indent=2, ensure_ascii=False)

print(f"Base de datos de campeones actualizada con éxito. Total campeones instalados: {len(champions)}")
