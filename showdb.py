import sqlite3
from typing import List, Dict, Any

def load_messages() -> List[Dict[str, Any]]:
    conn = sqlite3.connect('2025-01-iamge.db')
    c = conn.cursor()
    c.execute('SELECT id, session_id, message FROM message_store')
    rows = c.fetchall()
    conn.close()
    messages = []
    for row in rows:
        message = {'id': row[0], 'session_id': row[1], 'message': row[2]}
        messages.append(message)

    return messages


def get_table_info(table_name: str):
    conn = sqlite3.connect('2025-01-iamge.db')
    c = conn.cursor()
    c.execute(f'PRAGMA table_info({table_name})')
    columns = c.fetchall()
    conn.close()
    return columns

def list_tables() -> List[str]:
    conn = sqlite3.connect('2025-01-iamge.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in c.fetchall()]
    conn.close()
    return tables

if __name__ == '__main__':
    print(load_messages())