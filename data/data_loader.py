import json
import sqlite3
import os


class DataLoader:
    """Singleton: carga datos desde SQLite; fallback a JSON."""
    _instance = None
    _champions = None
    _items = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataLoader, cls).__new__(cls)
            cls._instance._load_all_data()
        return cls._instance

    def _load_all_data(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(base_dir, 'data', 'knowledge.db')

        if os.path.exists(db_path):
            self._champions = self._load_from_sqlite(db_path)
        else:

            champs_path = os.path.join(base_dir, 'data', 'champions.json')
            with open(champs_path, 'r', encoding='utf-8') as f:
                self._champions = json.load(f)

        items_path = os.path.join(base_dir, 'data', 'items.json')
        if os.path.exists(items_path):
            with open(items_path, 'r', encoding='utf-8') as f:
                self._items = json.load(f)
        else:
            self._items = {}

    def _load_from_sqlite(self, db_path):
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row

        champions = {}

        for row in conn.execute("SELECT * FROM champions"):
            champ_id = row['id']
            champions[champ_id] = {
                'id': champ_id,
                'name': row['name'],
                'role': row['role'],
                'role_class': row['role_class'],
                'tags': json.loads(row['tags'] or '[]'),
                'base_winrate': row['base_winrate'],
                'positions': json.loads(row['positions'] or '[]'),
                'matchups': {}
            }

        for row in conn.execute("SELECT champion_id, enemy_id, winrate FROM matchups"):
            champ_id = row['champion_id']
            if champ_id in champions:
                champions[champ_id]['matchups'][row['enemy_id']] = row['winrate']

        conn.close()
        return champions

    def get_champions(self):
        return self._champions

    def get_items(self):
        return self._items
