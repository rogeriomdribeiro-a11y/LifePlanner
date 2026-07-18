"""Definição da estrutura SQLite utilizada pelo LifePlanner."""


def create_tables(connection) -> None:
    """
    Criar as tabelas e os índices necessários ao funcionamento da aplicação.

    A função pode ser executada em todos os arranques, porque utiliza
    CREATE TABLE IF NOT EXISTS e CREATE INDEX IF NOT EXISTS.
    """
    cursor = connection.cursor()

    # Utilizadores locais e contas associadas ao Google OAuth.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            provider TEXT NOT NULL DEFAULT 'local',
            oauth_user_id TEXT,
            profile_picture TEXT,
            email_verified INTEGER NOT NULL DEFAULT 0,
            is_active INTEGER NOT NULL DEFAULT 1,
            last_login DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # Tarefas pessoais associadas ao utilizador autenticado.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT DEFAULT 'Pessoal',
            due_date TEXT,
            due_time TEXT,
            priority TEXT DEFAULT 'Normal',
            is_completed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
        """
    )

    # Eventos apresentados no calendário mensal.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            event_date TEXT NOT NULL,
            start_time TEXT,
            end_time TEXT,
            location TEXT,
            color TEXT DEFAULT '#3B82F6',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
        """
    )

    # Notas livres, com categoria, cor e opção de destaque.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT,
            category TEXT DEFAULT 'Geral',
            color TEXT DEFAULT '#8B5CF6',
            is_pinned INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
        """
    )

    # Objetivos pessoais e respetivo progresso.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT DEFAULT 'Pessoal',
            target_date TEXT,
            progress INTEGER DEFAULT 0,
            status TEXT DEFAULT 'Em progresso',
            color TEXT DEFAULT '#10B981',
            is_main INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
        """
    )

    # Etapas pertencentes a um objetivo.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS goal_steps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            is_completed INTEGER DEFAULT 0,
            position INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (goal_id)
                REFERENCES goals(id)
                ON DELETE CASCADE
        )
        """
    )

    # Índices utilizados nas consultas mais frequentes.
    cursor.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_users_oauth_user_id
        ON users(oauth_user_id)
        WHERE oauth_user_id IS NOT NULL
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_tasks_user_date
        ON tasks(user_id, due_date, is_completed)
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_events_user_date
        ON events(user_id, event_date)
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_notes_user_updated
        ON notes(user_id, is_pinned, updated_at)
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_goals_user_status
        ON goals(user_id, status, is_main)
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_goal_steps_goal_position
        ON goal_steps(goal_id, position)
        """
    )

    connection.commit()