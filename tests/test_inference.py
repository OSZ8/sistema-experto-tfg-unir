import pytest
from engine.knowledge_base import Engine, Fact
from engine.inference import create_expert_system

@pytest.fixture
def engine():
    """Proporciona una instancia limpia del sistema experto para cada test."""
    return create_expert_system()

def test_regla_anticuraciones(engine):
    """Verifica regla anti-curaciones."""
    engine.add_fact(Fact('enemy_champion_tag', 'healing_support'))
    engine.run()
    recomendaciones = engine.get_recommendations()
    
    assert 'antiheal' in recomendaciones
    assert "Regla Anti-Curaciones" in engine.triggered_rules

def test_regla_antitanques(engine):
    """Verifica regla anti-tanques."""
    engine.add_fact(Fact('enemy_champion_tag', 'tank'))
    engine.run()
    # Con un tanque no debería dispararse
    assert 'armor_penetration' not in engine.get_recommendations()
    
    # Inyectamos el segundo tanque
    engine.add_fact(Fact('enemy_champion_tag', 'tank'))
    engine.run()
    recomendaciones = engine.get_recommendations()
    assert 'armor_penetration' in recomendaciones
    assert 'true_damage' in recomendaciones

def test_regla_antiautoataques(engine):
    """Verifica regla anti-ataques."""
    engine.add_fact(Fact('enemy_champion_tag', 'marksman'))
    engine.add_fact(Fact('enemy_champion_tag', 'auto_attacker'))
    engine.run()
    recomendaciones = engine.get_recommendations()
    
    assert 'anti_auto_attacker' in recomendaciones
    assert 'anti_crit' in recomendaciones

def test_regla_resistencia_magica(engine):
    """Verifica regla resistencia mágica."""
    engine.add_fact(Fact('enemy_champion_tag', 'magic_damage'))
    engine.add_fact(Fact('enemy_champion_tag', 'magic_damage'))
    engine.run()
    
    assert 'magic_resist' in engine.get_recommendations()

def test_regla_antiescudos(engine):
    """Verifica regla anti-escudos."""
    engine.add_fact(Fact('enemy_champion_tag', 'shielding'))
    engine.run()
    
    assert 'anti_shield' in engine.get_recommendations()

def test_regla_tenacidad(engine):
    """Verifica regla tenacidad."""
    # Menos de 2 cc_heavy no debería disparar
    engine.add_fact(Fact('enemy_champion_tag', 'cc_heavy'))
    engine.run()
    assert 'tenacity' not in engine.get_recommendations()
    
    engine.add_fact(Fact('enemy_champion_tag', 'cc_heavy'))
    engine.run()
    assert 'tenacity' in engine.get_recommendations()

def test_regla_supervivencia_asesinos(engine):
    """Verifica regla supervivencia para asesinos."""
    engine.add_fact(Fact('enemy_champion_tag', 'assassin'))
    engine.run()
    
    assert 'survival' in engine.get_recommendations()
    assert 'anti_assassin' in engine.get_recommendations()

def test_integracion_mixta(engine):
    """Verifica draft mixto realista."""
    # Soraka (Healing), Zed (Assassin), Malphite (Tank/MagicDamage)
    engine.add_fact(Fact('enemy_champion_tag', 'healing_support'))
    engine.add_fact(Fact('enemy_champion_tag', 'assassin'))
    engine.add_fact(Fact('enemy_champion_tag', 'tank'))
    engine.add_fact(Fact('enemy_champion_tag', 'magic_damage'))
    
    engine.run()
    recomendaciones = engine.get_recommendations()
    
    # Debe recomendar cortar curaciones (por Soraka)
    assert 'antiheal' in recomendaciones
    # Debe recomendar supervivencia (por Zed)
    assert 'survival' in recomendaciones
    # NO debe recomendar anti tanques porque sólo hay 1 tanque
    assert 'armor_penetration' not in recomendaciones

def test_regla_aliada_frontline(engine):
    """Verifica carencia aliada de frontline."""
    engine.add_fact(Fact('ally_champion_tag', 'marksman')) # ADC
    engine.add_fact(Fact('ally_champion_tag', 'mage')) # Mid
    engine.run()
    
    recomendaciones = [f.value for f in engine.facts if f.key == 'recommend_champion_tag']
    assert 'tank' in recomendaciones
    assert 'bruiser' in recomendaciones
    assert "Regla Aliada: Frontline" in engine.triggered_rules

def test_regla_aliada_frontline_satisfecha(engine):
    """Verifica cumplimiento aliado de frontline."""
    engine.add_fact(Fact('ally_champion_tag', 'tank')) 
    engine.run()
    
    recomendaciones = [f.value for f in engine.facts if f.key == 'recommend_champion_tag']
    assert 'tank' not in recomendaciones

def test_regla_aliada_ap_carente(engine):
    """Verifica carencia de AP aliado."""
    engine.add_fact(Fact('ally_champion_tag', 'physical_damage'))
    engine.add_fact(Fact('ally_champion_tag', 'marksman'))
    engine.run()
    
    recomendaciones = [f.value for f in engine.facts if f.key == 'recommend_champion_tag']
    assert 'magic_damage' in recomendaciones
    assert "Regla Aliada: Daño Mágico" in engine.triggered_rules
