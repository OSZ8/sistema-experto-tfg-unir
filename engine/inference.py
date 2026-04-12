import json
import os
from .knowledge_base import Engine, Fact, Rule
from data.data_loader import DataLoader

def create_expert_system():
    engine = Engine()

    # Anti-Curaciones
    def cond_healing(facts):
        sources = [f.source for f in facts if f.key == 'enemy_champion_tag' and f.value in ('healing_self', 'healing_support')]
        return sources if sources else False
        
    def act_healing(e):
        e.add_fact(Fact('recommend_item_tag', 'antiheal'))

    engine.add_rule(Rule(
        name="Regla Anti-Curaciones",
        condition=cond_healing,
        action=act_healing,
        description="Regla Anti-Curaciones disparada por [{sources}]. El equipo enemigo tiene alta capacidad de curación. Recomendamos comprar objetos Cortacuras (Heridas Graves)."
    ))

    # Anti-Tanques
    def cond_tanks(facts):
        sources = [f.source for f in facts if f.key == 'enemy_champion_tag' and f.value == 'tank']
        return sources if len(sources) >= 2 else False
        
    def act_tanks(e):
        e.add_fact(Fact('recommend_item_tag', 'armor_penetration'))
        e.add_fact(Fact('recommend_item_tag', 'true_damage'))

    engine.add_rule(Rule(
        name="Regla Anti-Tanques",
        condition=cond_tanks,
        action=act_tanks,
        description="Regla Anti-Tanques activada frente a: [{sources}]. Composición robusta (2 o más tanques). Es vital adquirir Penetración de Armadura y Daño Verdadero."
    ))

    # Anti-Ataques Básicos
    def cond_aa(facts):
        sources = [f.source for f in facts if f.key == 'enemy_champion_tag' and f.value in ('auto_attacker', 'marksman')]
        return sources if len(sources) >= 2 else False

    def act_aa(e):
        e.add_fact(Fact('recommend_item_tag', 'anti_auto_attacker'))
        e.add_fact(Fact('recommend_item_tag', 'anti_crit'))
        e.add_fact(Fact('recommend_item_tag', 'armor'))

    engine.add_rule(Rule(
        name="Regla Anti-Ataques Básicos",
        condition=cond_aa,
        action=act_aa,
        description="Regla Anti-Ataques Básicos disparada por presencia de Tiradores/ADCs: [{sources}]. Comprar armadura y reducción de daño progresivo es prioritario."
    ))

    # Resistencia Mágica
    def cond_magic(facts):
        sources = [f.source for f in facts if f.key == 'enemy_champion_tag' and f.value == 'magic_damage']
        return sources if len(sources) >= 2 else False

    def act_magic(e):
        e.add_fact(Fact('recommend_item_tag', 'magic_resist'))

    engine.add_rule(Rule(
        name="Regla Resistencia Mágica",
        condition=cond_magic,
        action=act_magic,
        description="Regla Resistencia Mágica disparada por múltiples fuentes de AP en el rival: [{sources}]. Recomendadas opciones de Resistencia Mágica y escudos hechizo."
    ))

    # Anti-Escudos
    def cond_shields(facts):
        sources = [f.source for f in facts if f.key == 'enemy_champion_tag' and f.value == 'shielding']
        return sources if sources else False

    def act_shields(e):
        e.add_fact(Fact('recommend_item_tag', 'anti_shield'))

    engine.add_rule(Rule(
        name="Regla Anti-Escudos",
        condition=cond_shields,
        action=act_shields,
        description="Regla Anti-Escudos detectada por protección otorgada por: [{sources}]. Recomendado adquirir armamento Rompe-Escudos letal."
    ))

    # Tenacidad
    def cond_cc(facts):
        sources = [f.source for f in facts if f.key == 'enemy_champion_tag' and f.value == 'cc_heavy']
        return sources if len(sources) >= 2 else False

    def act_cc(e):
        e.add_fact(Fact('recommend_item_tag', 'tenacity'))

    engine.add_rule(Rule(
        name="Regla Tenacidad",
        condition=cond_cc,
        action=act_cc,
        description="Regla Tenacidad encendida por Control de Masas severo procedente de: [{sources}]. Priorizar opciones de Limpiar o botas de Tenacidad."
    ))

    # Supervivencia / Anti-Asesinos
    def cond_assassin(facts):
        sources = [f.source for f in facts if f.key == 'enemy_champion_tag' and f.value == 'assassin']
        return sources if sources else False

    def act_assassin(e):
        e.add_fact(Fact('recommend_item_tag', 'survival'))
        e.add_fact(Fact('recommend_item_tag', 'anti_assassin'))

    engine.add_rule(Rule(
        name="Regla Supervivencia",
        condition=cond_assassin,
        action=act_assassin,
        description="Regla Supervivencia detecta un foco Asesino fulminante por presencia de: [{sources}]. Necesitas objetos de Estasis temporal o aguante."
    ))

    # Frontline aliada
    def cond_need_tank(facts):
        ally_sources = [f.source for f in facts if f.key == 'ally_champion_tag']
        if not ally_sources: return False
        tanks = [f for f in facts if f.key == 'ally_champion_tag' and f.value in ('tank', 'bruiser')]
        return ally_sources if len(tanks) == 0 else False

    def act_need_tank(e):
        e.add_fact(Fact('recommend_champion_tag', 'tank'))
        e.add_fact(Fact('recommend_champion_tag', 'bruiser'))

    engine.add_rule(Rule(
        name="Regla Aliada: Frontline",
        condition=cond_need_tank,
        action=act_need_tank,
        description="Alerta de Composición: Tu equipo carece de Frontline sólido (Tanque/Bruiser). Alta prioridad de aguante en próximas selecciones."
    ))

    # Daño mágico aliado
    def cond_need_ap(facts):
        ally_sources = [f.source for f in facts if f.key == 'ally_champion_tag']
        if not ally_sources: return False
        
        ap = sum(1 for f in facts if f.key == 'ally_champion_tag' and f.value in ('magic_damage', 'mage'))
        ad = sum(1 for f in facts if f.key == 'ally_champion_tag' and f.value in ('physical_damage', 'marksman', 'assassin'))
        
        return ally_sources if (ap == 0 and ad >= 2) else False

    def act_need_ap(e):
        e.add_fact(Fact('recommend_champion_tag', 'magic_damage'))
        e.add_fact(Fact('recommend_champion_tag', 'mage'))

    engine.add_rule(Rule(
        name="Regla Aliada: Daño Mágico",
        condition=cond_need_ap,
        action=act_need_ap,
        description="Alerta de Composición: Alta concentración de Daño Físico aliado. Se recomienda Daño Mágico (AP) para balancear."
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

    # Carga hechos
    for champ_id in enemy_champions:
        if champ_id in champs:
            champ = champs[champ_id]
            for tag in champ.get('tags', []):
                engine.add_fact(Fact('enemy_champion_tag', tag, source=champ.get('name', champ_id)))
                
    for champ_id in ally_champions:
        if champ_id in champs:
            champ = champs[champ_id]
            for tag in champ.get('tags', []):
                engine.add_fact(Fact('ally_champion_tag', tag, source=champ.get('name', champ_id)))
    
    engine.run()

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
            
            if avg_matchup_wr <= 1.0:
                avg_matchup_wr *= 100.0
                
            final_score = (avg_matchup_wr * 0.7) + (base_wr * 0.3)
            reason = f"Win rate medio vs. {matchup_count} enemigo{'s' if matchup_count > 1 else ''}: {avg_matchup_wr:.1f}%."
        else:
            final_score = base_wr
            reason = "Sin datos de matchup directos. Basado en win rate general."
            
        # Sinergia aliada
        synergy_bonus = 0.0
        candidate_tags = candidate_data.get('tags', [])
        intersection = set(recommended_champ_tags).intersection(set(candidate_tags))
        if intersection:
            synergy_bonus = len(intersection) * 3.0
            reason += f" Sinergia de draft detectada."
            
        final_score = min(final_score + synergy_bonus, 99.0)
            
        champ_scores.append({
            "id": candidate_data['id'],
            "name": candidate_data['name'],
            "role": candidate_data.get('role_class', candidate_data.get('role', '')),
            "positions": candidate_data.get('positions', []),
            "score": round(final_score, 2),
            "reason": reason
        })

    champ_scores.sort(key=lambda x: x['score'], reverse=True)

    # Posiciones faltantes
    if ally_champions_dict:
        missing_positions = [pos for pos, cid in ally_champions_dict.items() if not cid]
    else:
        missing_positions = ["Top", "Jungla", "Medio", "ADC", "Apoyo"]

    grouped_recommendations = {}
    
    # Agrupa top 3 por posición
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
        "explanations": engine.explanations,
        "debug_info": {
            "triggered_rules": list(engine.triggered_rules),
            "raw_champ_scores_top10": champ_scores[:10]
        }
    }
