from flask import Flask, render_template, request, jsonify
from engine.inference import evaluate_draft
from data.data_loader import DataLoader
import json

app = Flask(__name__)
loader = DataLoader()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/champions', methods=['GET'])
def get_champions():
    champions = loader.get_champions()
    champs_list = sorted([vars for key, vars in champions.items()], key=lambda x: x['name'])
    return jsonify(champs_list)

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Estructura JSON (Payload) inválida o en blanco"}), 400

    enemy_draft = data.get('enemy_draft', [])
    ally_draft_dict = data.get('ally_draft', {}) # Dict: {"Top": "A", "Jungla": "B"}
    
    # Extraer IDs válidas de aliados
    ally_draft = [cid for cid in ally_draft_dict.values() if cid]

    # 1. Validación de Longitud (Protección contra Spam)
    if len(enemy_draft) > 5 or len(ally_draft) > 5:
        return jsonify({"error": "No puedes seleccionar más de 5 campeones por equipo"}), 400
        
    # 2. Validación de Duplicados
    if len(enemy_draft) != len(set(enemy_draft)) or len(ally_draft) != len(set(ally_draft)):
        return jsonify({"error": "Existen campeones duplicados en la misma selección"}), 400
        
    # 3. Validación Mínima Operacional
    if not enemy_draft:
        return jsonify({"error": "Debes introducir al menos a un campeón enemigo"}), 400
        
    try:
        recommendations = evaluate_draft(enemy_draft, ally_draft_dict)
        return jsonify({
            "success": True,
            "data": recommendations
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
