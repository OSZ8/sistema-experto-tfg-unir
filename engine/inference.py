import json
import os
from .knowledge_base import Engine, Fact, Rule
from data.data_loader import DataLoader

def create_expert_system():
    engine = Engine()

    # Rule 1: Anti-Heal
    def cond_healing(facts):
        for f in facts:
            if f.key == 'enemy_champion_tag' and f.value in ('healing_self', 'healing_support'):
                return True
        return False
        
    def act_healing(e):
        e.add_fact(Fact('recommend_item_tag', 'antiheal'))

    engine.add_rule(Rule(
        name="Regla Anti-Curaciones",
        condition=cond_healing,
        action=act_healing,
        description="El equipo enemigo tiene mucha capacidad de curación. Recomendamos comprar objetos Cortacuras (Heridas Graves)."
    ))

    # Rule 2: Anti-Tanks
    def cond_tanks(facts):
        tanks_count = sum(1 for f in facts if f.key == 'enemy_champion_tag' and f.value == 'tank')
        return tanks_count >= 2
        
    def act_tanks(e):
        e.add_fact(Fact('recommend_item_tag', 'armor_penetration'))
        e.add_fact(Fact('recommend_item_tag', 'true_damage'))

    engine.add_rule(Rule(
        name="Regla Anti-Tanques",
        condition=cond_tanks,
        action=act_tanks,
        description="La composición enemiga es muy robusta (2 o más tanques). Es vital adquirir Penetración de Armadura y Daño Verdadero."
    ))

    # Rule 3: Anti-Autoattacks
    def cond_aa(facts):
        aa_count = sum(1 for f in facts if f.key == 'enemy_champion_tag' and f.value in ('auto_attacker', 'marksman'))
        return aa_count >= 2

    def act_aa(e):
        e.add_fact(Fact('recommend_item_tag', 'anti_auto_attacker'))
        e.add_fact(Fact('recommend_item_tag', 'anti_crit'))
        e.add_fact(Fact('recommend_item_tag', 'armor'))

    engine.add_rule(Rule(
        name="Regla Anti-Ataques Básicos",
        condition=cond_aa,
        action=act_aa,
        description="Los enemigos dependen en su mayoría de Ataques Básicos y Golpes Críticos. Comprar armadura y reducción de daño es prioritario."
    ))

    # Rule 4: Magic Resist
    def cond_magic(facts):
        md_count = sum(1 for f in facts if f.key == 'enemy_champion_tag' and f.value == 'magic_damage')
        return md_count >= 2

    def act_magic(e):
        e.add_fact(Fact('recommend_item_tag', 'magic_resist'))

    engine.add_rule(Rule(
        name="Regla Resistencia Mágica",
        condition=cond_magic,
        action=act_magic,
        description="Alta presencia de daño mágico enemigo. Las opciones de Resistencia Mágica aumentarán mucho la supervivencia."
    ))

    # Rule 5: Anti-Shields
    def cond_shields(facts):
        for f in facts:
            if f.key == 'enemy_champion_tag' and f.value == 'shielding':
                return True
        return False

    def act_shields(e):
        e.add_fact(Fact('recommend_item_tag', 'anti_shield'))

    engine.add_rule(Rule(
        name="Regla Anti-Escudos",
        condition=cond_shields,
        action=act_shields,
        description="Fuerte presencia de mitigación y escudos en el equipo enemigo. Recomendado adquirir Rompe-Escudos."
    ))

    # Rule 6: Tenacity (Anti CC)
    def cond_cc(facts):
        cc_count = sum(1 for f in facts if f.key == 'enemy_champion_tag' and f.value == 'cc_heavy')
        return cc_count >= 2

    def act_cc(e):
        e.add_fact(Fact('recommend_item_tag', 'tenacity'))

    engine.add_rule(Rule(
        name="Regla Tenacidad",
        condition=cond_cc,
        action=act_cc,
        description="El enemigo posee un alto Control de Adversario (CC). Priorizar opciones de Tenacidad o Limpiar es crítico."
    ))

    # Rule 7: Survival / Anti-Assassin
    def cond_assassin(facts):
        assassin_count = sum(1 for f in facts if f.key == 'enemy_champion_tag' and f.value == 'assassin')
        return assassin_count >= 1

    def act_assassin(e):
        e.add_fact(Fact('recommend_item_tag', 'survival'))
        e.add_fact(Fact('recommend_item_tag', 'anti_assassin'))

    engine.add_rule(Rule(
        name="Regla Supervivencia",
        condition=cond_assassin,
        action=act_assassin,
        description="El oponente cuenta con Asesinos de daño explosivo. Necesitas objetos de Supervivencia extrema y Estasis temporal."
    ))

    # Rule 8: Ally Needs Frontline
    def cond_need_tank(facts):
        ally_count = sum(1 for f in facts if f.key == 'ally_champion_tag')
        if ally_count == 0: return False
        tanks = sum(1 for f in facts if f.key == 'ally_champion_tag' and f.value in ('tank', 'bruiser'))
        return tanks == 0

    def act_need_tank(e):
        e.add_fact(Fact('recommend_champion_tag', 'tank'))
        e.add_fact(Fact('recommend_champion_tag', 'bruiser'))

    engine.add_rule(Rule(
        name="Regla Aliada: Frontline",
        condition=cond_need_tank,
        action=act_need_tank,
        description="Falta capacidad de aguante (Tanque/Bruiser) en tu composición aliada."
    ))

    # Rule 9: Ally Needs Magic Damage (AP)
    def cond_need_ap(facts):
        ally_count = sum(1 for f in facts if f.key == 'ally_champion_tag')
        if ally_count == 0: return False
        
        ap = sum(1 for f in facts if f.key == 'ally_champion_tag' and f.value in ('magic_damage', 'mage'))
        ad = sum(1 for f in facts if f.key == 'ally_champion_tag' and f.value in ('physical_damage', 'marksman', 'assassin'))
        
        return ap == 0 and ad >= 2

    def act_need_ap(e):
        e.add_fact(Fact('recommend_champion_tag', 'magic_damage'))
        e.add_fact(Fact('recommend_champion_tag', 'mage'))

    engine.add_rule(Rule(
        name="Regla Aliada: Daño Mágico",
        condition=cond_need_ap,
        action=act_need_ap,
        description="Falta Daño Mágico en el equipo aliado, el enemigo comprará mucha armadura si no se balancea."
    ))

    return engine

def evaluate_draft(enemy_champions, ally_champions_dict=None):
    if ally_champions_dict is None:
        ally_champions_dict = {}
        
    ally_champions = [cid for cid in ally_champions_dict.values() if cid]
        
    loader = DataLoader()
    champs = loader.get_champions()
    items = loader.get_items()
    engine = create_expert_system()

    # Fact loading
    for champ_id in enemy_champions:
        if champ_id in champs:
            champ = champs[champ_id]
            for tag in champ.get('tags', []):
                engine.add_fact(Fact('enemy_champion_tag', tag))
                
    for champ_id in ally_champions:
        if champ_id in champs:
            champ = champs[champ_id]
            for tag in champ.get('tags', []):
                engine.add_fact(Fact('ally_champion_tag', tag))
    
    # Run Inference Engine
    engine.run()

    # Items Logic
    recommended_item_tags = engine.get_recommendations()
    recommended_items = []
    
    for item_name, item_data in items.items():
        item_tags = item_data.get('tags', [])
        intersection = set(recommended_item_tags).intersection(set(item_tags))
        if intersection:
            score = len(intersection)
            recommended_items.append({
                "id": item_data.get('id', item_name),
                "name": item_data.get('name', item_name),
                "description": item_data.get('description', ''),
                "icon": item_data.get('icon', ''),
                "score": score,
                "matching_tags": list(intersection)
            })
    
    recommended_items.sort(key=lambda x: x['score'], reverse=True)

    # Champions Logic (Matchups vs Base Winrate)
    recommended_champ_tags = [f.value for f in engine.facts if f.key == 'recommend_champion_tag']
    champ_scores = []
    
    for candidate_id, candidate_data in champs.items():
        if candidate_id in enemy_champions or candidate_id in ally_champions:
            continue
        
        base_wr = candidate_data.get('base_winrate', 50.0)
        matchup_wr_sum = 0
        matchup_count = 0
        
        matchups = candidate_data.get('matchups', {})
        for enemy in enemy_champions:
            if enemy in matchups:
                matchup_count += 1
                matchup_wr_sum += matchups[enemy]
        
        if matchup_count > 0:
            avg_matchup_wr = matchup_wr_sum / matchup_count
            final_score = (avg_matchup_wr * 0.7) + (base_wr * 0.3)
            reason = f"{matchup_count} counters registrados."
        else:
            final_score = base_wr
            reason = f"Winrate base estable."
            
        # Synergy Bonus for Allies Component
        synergy_bonus = 0.0
        candidate_tags = candidate_data.get('tags', [])
        intersection = set(recommended_champ_tags).intersection(set(candidate_tags))
        if intersection:
            synergy_bonus = len(intersection) * 15.0 # Adds 15 to the heuristic score
            reason += f" Compensador de draft sinérgico (+15%)."
            
        final_score += synergy_bonus
            
        champ_scores.append({
            "id": candidate_data['id'],
            "name": candidate_data['name'],
            "role": candidate_data.get('role_class', candidate_data.get('role', '')),
            "positions": candidate_data.get('positions', []),
            "score": round(final_score, 2),
            "reason": reason
        })

    champ_scores.sort(key=lambda x: x['score'], reverse=True)

    # 1. Determinar posiciones faltantes en el equipo aliado
    if ally_champions_dict:
        missing_positions = [pos for pos, cid in ally_champions_dict.items() if not cid]
    else:
        missing_positions = ["Top", "Jungla", "Medio", "ADC", "Apoyo"]

    grouped_recommendations = {}
    
    # 2. Para cada posición que falte, devolvemos los 3 mejores campeones (sin repetir posiciones dentro del bloque)
    for pos in missing_positions:
        pos_candidates = []
        for champ in champ_scores:
            if pos in champ['positions']:
                pos_candidates.append(champ)
            if len(pos_candidates) == 3:
                break
        grouped_recommendations[pos] = pos_candidates

    return {
        "recommended_items": recommended_items[:6],
        "recommended_champions_grouped": grouped_recommendations,
        "explanations": engine.explanations
    }
