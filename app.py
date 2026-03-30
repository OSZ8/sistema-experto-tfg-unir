from flask import Flask, render_template, request, jsonify
from engine.inference import evaluate_draft
import json
import os

app = Flask(__name__)

def load_champions():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, 'data', 'champions.json'), 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def index():
    champions = load_champions()
    # Sort champions by name for the UI
    champs_list = sorted([vars for key, vars in champions.items()], key=lambda x: x['name'])
    return render_template('index.html', champions=champs_list)

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    enemy_draft = data.get('enemy_draft', [])
    
    if not enemy_draft:
        return jsonify({"error": "No se han seleccionado campeones enemigos"}), 400
        
    try:
        recommendations = evaluate_draft(enemy_draft)
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
