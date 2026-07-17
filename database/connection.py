"""Criação de ligações SQLite usadas pelos repositórios."""

import sqlite3

from app.path import DATA_DIR


DB_PATH = DATA_DIR / "lifeplanner.db"


def get_connection() -> sqlite3.Connection:
    """Abrir uma ligação configurada à base de dados local.

    ``sqlite3.Row`` permite aceder aos valores pelo nome da coluna, por exemplo
    ``user["email"]``. As chaves estrangeiras são ativadas em todas as ligações
    para que as eliminações em cascata sejam respeitadas.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 10000")

    return connection
