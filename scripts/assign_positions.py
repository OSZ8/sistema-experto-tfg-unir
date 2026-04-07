import json
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
champs_path = os.path.join(base_dir, 'data', 'champions.json')

with open(champs_path, 'r', encoding='utf-8') as f:
    champions = json.load(f)

for cid, cdata in champions.items():
    tags = [t.lower() for t in cdata.get('tags', [])]
    
    positions = []
    
    if cid == "Akshan": positions = ["Top", "Medio"]
    elif cid == "Akali": positions = ["Top", "Medio"]
    elif cid == "Ahri": positions = ["Medio"]
    elif cid == "Vladimir": positions = ["Top", "Medio"]
    elif cid == "Vex": positions = ["Medio"]
    elif cid == "Xayah": positions = ["ADC"]
    elif cid in ("Aatrox", "Darius", "Garen", "Shen", "Fiora", "Ornn", "Malphite", "Tryndamere", "DrMundo", "Kled", "Illaoi", "Sett", "Renekton", "Camille"):
        positions = ["Top"]
    elif cid in ("Amumu", "XinZhao", "Vi", "Khazix", "Rammus", "Sejuani", "LeeSin", "Zac", "Kayn", "Nunu", "Olaf", "Rengar"):
        positions = ["Jungla"]
    elif cid in ("Yasuo", "Yone", "Zed", "Orianna", "Syndra", "Sylas", "Katarina", "Talon", "Fizz", "Leblanc", "Viktor"):
        positions = ["Medio", "Top"] if cid in ("Yasuo", "Yone") else ["Medio"]
    elif cid in ("Jinx", "Vayne", "Ashe", "Ezreal", "Jhin", "Caitlyn", "Kaisa", "Lucian", "Tristana", "MissFortune", "Draven"):
        positions = ["ADC"]
    elif cid in ("Soraka", "Leona", "Thresh", "Lulu", "Blitzcrank", "Nautilus", "Nami", "Braum", "Janna", "Karma", "Pyke"):
        positions = ["Apoyo"]
    else:
        if "support" in tags or "healing_support" in tags:
            positions.append("Apoyo")
        if "marksman" in tags:
            positions.append("ADC")
        if "assassin" in tags or "mage" in tags:
            positions.append("Medio")
        if "fighter" in tags or "tank" in tags or "bruiser" in tags:
            positions.append("Top")
            positions.append("Jungla")
            
        if not positions:
            positions = ["Top", "Jungla", "Medio", "ADC", "Apoyo"]
            
    # Sin duplicados
    seen = set()
    positions = [x for x in positions if not (x in seen or seen.add(x))]
    
    role = cdata.get('role', 'Desconocido')
    cdata['role_class'] = role
    cdata['positions'] = positions
    
with open(champs_path, 'w', encoding='utf-8') as f:
    json.dump(champions, f, indent=2, ensure_ascii=False)
    
print("Nuevos atributos 'positions' (Carriles Meta) e inyección de clases secundaria inyectada a todos los 172 campeones.")
