"""
Migra champions.json a una base de datos SQLite (data/knowledge.db).
Crea dos tablas: champions y matchups.
Ejecutar una sola vez (o cuando se actualice el JSON).
"""
import json
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE_DIR, 'data', 'champions.json')
DB_PATH = os.path.join(BASE_DIR, 'data', 'knowledge.db')


def create_tables(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS champions (
            id          TEXT PRIMARY KEY,
            name        TEXT NOT NULL,
            role        TEXT,
            role_class  TEXT,
            tags        TEXT,
            base_winrate REAL,
            positions   TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS matchups (
            champion_id TEXT NOT NULL,
            enemy_id    TEXT NOT NULL,
            winrate     REAL NOT NULL,
            PRIMARY KEY (champion_id, enemy_id),
            FOREIGN KEY (champion_id) REFERENCES champions(id)
        )
    ''')
    conn.commit()


def migrate(conn, data):
    for champ_id, champ in data.items():
        conn.execute('''
            INSERT OR REPLACE INTO champions (id, name, role, role_class, tags, base_winrate, positions)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            champ_id,
            champ.get('name', champ_id),
            champ.get('role', ''),
            champ.get('role_class', ''),
            json.dumps(champ.get('tags', [])),
            champ.get('base_winrate', 50.0),
            json.dumps(champ.get('positions', []))
        ))

        for enemy_id, winrate in champ.get('matchups', {}).items():
            conn.execute('''
                INSERT OR REPLACE INTO matchups (champion_id, enemy_id, winrate)
                VALUES (?, ?, ?)
            ''', (champ_id, enemy_id, winrate))

    conn.commit()


def main():
    print(f"Leyendo {JSON_PATH}...")
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Conectando a {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)

    create_tables(conn)
    migrate(conn, data)

    champ_count = conn.execute("SELECT COUNT(*) FROM champions").fetchone()[0]
    matchup_count = conn.execute("SELECT COUNT(*) FROM matchups").fetchone()[0]

    conn.close()
    print(f"Migración completada: {champ_count} campeones, {matchup_count} matchups.")


if __name__ == '__main__':
    main()
