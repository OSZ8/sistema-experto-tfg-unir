import json
import os

class DataLoader:
    """
    Singleton Data Loader to cache JSON files in RAM.
    Avoids opening disk files on every HTTP REST request (O(N) -> O(1)).
    """
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
        
        champs_path = os.path.join(base_dir, 'data', 'champions.json')
        if os.path.exists(champs_path):
            with open(champs_path, 'r', encoding='utf-8') as f:
                self._champions = json.load(f)
        else:
            self._champions = {}

        items_path = os.path.join(base_dir, 'data', 'items.json')
        if os.path.exists(items_path):
            with open(items_path, 'r', encoding='utf-8') as f:
                self._items = json.load(f)
        else:
            self._items = {}

    def get_champions(self):
        return self._champions

    def get_items(self):
        return self._items
