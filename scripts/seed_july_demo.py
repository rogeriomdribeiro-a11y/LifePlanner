import sys
from pathlib import Path
from datetime import datetime

import bcrypt


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from database.connection import get_connection


DEMO_EMAIL = "exemplo@exemplo.com"
DEMO_PASSWORD = "123abc"
DEMO_NAME = "Utilizador Exemplo"

YEAR = 2026
MONTH = 7


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_columns(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    return [column[1] for column in cursor.fetchall()]


def insert_dynamic(cursor, table_name, data):
    columns = get_columns(cursor, table_name)

    filtered_data = {
        key: value
        for key, value in data.items()
        if key in columns
    }

    column_names = ", ".join(filtered_data.keys())
    placeholders = ", ".join(["?"] * len(filtered_data))

    cursor.execute(
        f"""
        INSERT INTO {table_name} ({column_names})
        VALUES ({placeholders})
        """,
        tuple(filtered_data.values()),
    )

    return cursor.lastrowid


def create_or_update_demo_user(cursor):
    password_hash = bcrypt.hashpw(
        DEMO_PASSWORD.encode("utf-8"),
        bcrypt.gensalt(),
    ).decode("utf-8")

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE email = ?
        """,
        (DEMO_EMAIL,),
    )

    user = cursor.fetchone()

    if user:
        user_id = user["id"]

        cursor.execute(
            """
            UPDATE users
            SET
                full_name = ?,
                password_hash = ?,
                provider = ?,
                oauth_user_id = NULL,
                profile_picture = NULL,
                email_verified = 1,
                is_active = 1,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                DEMO_NAME,
                password_hash,
                "local",
                user_id,
            ),
        )

        return user_id

    cursor.execute(
        """
        INSERT INTO users (
            full_name,
            email,
            password_hash,
            provider,
            email_verified,
            is_active,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """,
        (
            DEMO_NAME,
            DEMO_EMAIL,
            password_hash,
            "local",
            1,
            1,
        ),
    )

    return cursor.lastrowid


def clear_demo_user_data(cursor, user_id):
    cursor.execute(
        """
        DELETE FROM goal_steps
        WHERE goal_id IN (
            SELECT id
            FROM goals
            WHERE user_id = ?
        )
        """,
        (user_id,),
    )

    for table in ["tasks", "events", "notes", "goals"]:
        columns = get_columns(cursor, table)

        if "user_id" in columns:
            cursor.execute(
                f"""
                DELETE FROM {table}
                WHERE user_id = ?
                """,
                (user_id,),
            )


def seed_tasks(cursor, user_id):
    tasks = [
        ("2026-07-01", "Rever plano mensal", "Planeamento", "Alta", 1),
        ("2026-07-02", "Organizar ficheiros do projeto", "Trabalho", "Média", 1),
        ("2026-07-03", "Atualizar lista de tarefas", "Pessoal", "Média", 1),
        ("2026-07-04", "Preparar compras da semana", "Pessoal", "Baixa", 1),
        ("2026-07-05", "Rever objetivos de julho", "Objetivos", "Alta", 1),
        ("2026-07-06", "Estudar documentação PySide6", "Estudo", "Alta", 1),
        ("2026-07-07", "Melhorar interface do dashboard", "Projeto", "Alta", 1),
        ("2026-07-08", "Testar módulo de tarefas", "Projeto", "Média", 1),
        ("2026-07-09", "Criar notas de apresentação", "Estudo", "Média", 1),
        ("2026-07-10", "Rever calendário da semana", "Planeamento", "Baixa", 1),
        ("2026-07-11", "Organizar ambiente de trabalho", "Pessoal", "Baixa", 1),
        ("2026-07-12", "Fazer backup do projeto", "Projeto", "Alta", 1),
        ("2026-07-13", "Testar login Google", "Projeto", "Alta", 1),
        ("2026-07-14", "Adicionar dados de demonstração", "Projeto", "Média", 0),
        ("2026-07-15", "Rever README", "Projeto", "Média", 0),
        ("2026-07-16", "Preparar relatório final", "Estudo", "Alta", 0),
        ("2026-07-17", "Corrigir detalhes visuais", "Projeto", "Média", 0),
        ("2026-07-18", "Planear apresentação", "Estudo", "Alta", 0),
        ("2026-07-19", "Rever objetivos principais", "Objetivos", "Média", 0),
        ("2026-07-20", "Testar calendário completo", "Projeto", "Alta", 0),
        ("2026-07-21", "Criar notas finais", "Estudo", "Média", 0),
        ("2026-07-22", "Validar relatórios", "Projeto", "Alta", 0),
        ("2026-07-23", "Rever base de dados", "Projeto", "Média", 0),
        ("2026-07-24", "Ensaiar demonstração", "Estudo", "Alta", 0),
        ("2026-07-25", "Preparar perguntas possíveis", "Estudo", "Média", 0),
        ("2026-07-26", "Organizar screenshots", "Projeto", "Baixa", 0),
        ("2026-07-27", "Rever entrega final", "Projeto", "Alta", 0),
        ("2026-07-28", "Fazer teste final da aplicação", "Projeto", "Alta", 0),
        ("2026-07-29", "Preparar ficheiros para entrega", "Projeto", "Alta", 0),
        ("2026-07-30", "Confirmar GitHub atualizado", "Projeto", "Média", 0),
        ("2026-07-31", "Entrega final do projeto", "Estudo", "Alta", 0),
    ]

    for date, title, category, priority, completed in tasks:
        insert_dynamic(cursor, "tasks", {
            "user_id": user_id,
            "title": title,
            "description": "Tarefa de exemplo criada para demonstrar o planeamento mensal.",
            "category": category,
            "priority": priority,
            "due_date": date,
            "due_time": "10:00",
            "is_completed": completed,
            "completed_at": f"{date} 12:00:00" if completed else None,
            "created_at": now(),
            "updated_at": now(),
        })


def seed_events(cursor, user_id):
    events = [
        ("2026-07-01", "Reunião de planeamento mensal", "09:30", "10:30", "Online"),
        ("2026-07-03", "Consulta de organização pessoal", "15:00", "16:00", "Fafe"),
        ("2026-07-06", "Sessão de estudo PySide6", "18:00", "19:30", "Casa"),
        ("2026-07-08", "Revisão do projeto LifePlanner", "20:00", "21:00", "Casa"),
        ("2026-07-10", "Caminhada ao fim da tarde", "19:00", "20:00", "Parque"),
        ("2026-07-13", "Teste geral da aplicação", "17:30", "18:30", "Casa"),
        ("2026-07-15", "Reunião sobre relatório final", "14:00", "15:00", "Online"),
        ("2026-07-18", "Preparação da apresentação", "10:00", "12:00", "Casa"),
        ("2026-07-21", "Revisão dos objetivos", "18:30", "19:00", "Casa"),
        ("2026-07-24", "Ensaio da demonstração", "16:00", "17:30", "Casa"),
        ("2026-07-28", "Teste final completo", "15:00", "16:30", "Casa"),
        ("2026-07-31", "Entrega do projeto", "09:00", "10:00", "Escola"),
    ]

    for date, title, start_time, end_time, location in events:
        insert_dynamic(cursor, "events", {
            "user_id": user_id,
            "title": title,
            "description": "Evento de exemplo criado para demonstrar o calendário.",
            "event_date": date,
            "start_time": start_time,
            "end_time": end_time,
            "location": location,
            "color": "#60A5FA",
            "created_at": now(),
            "updated_at": now(),
        })


def seed_notes(cursor, user_id):
    notes = [
        (
            "Ideias para apresentação",
            "Mostrar login, dashboard, tarefas, calendário, notas, objetivos, relatórios e meteorologia.",
            "Projeto",
            1,
        ),
        (
            "Pontos fortes do LifePlanner",
            "Interface moderna, organização pessoal, dados locais em SQLite e integração com Google OAuth.",
            "Projeto",
            1,
        ),
        (
            "Checklist de entrega",
            "Confirmar README, testar aplicação, verificar GitHub e preparar demonstração final.",
            "Estudo",
            0,
        ),
        (
            "Melhorias futuras",
            "Adicionar lembretes, alteração da localização da meteorologia e notificações.",
            "Ideias",
            0,
        ),
        (
            "Resumo de julho",
            "Julho foi usado como mês de demonstração para apresentar tarefas, eventos e objetivos.",
            "Pessoal",
            0,
        ),
    ]

    for title, content, category, pinned in notes:
        insert_dynamic(cursor, "notes", {
            "user_id": user_id,
            "title": title,
            "content": content,
            "category": category,
            "is_pinned": pinned,
            "created_at": now(),
            "updated_at": now(),
        })


def seed_goals(cursor, user_id):
    goals = [
        {
            "title": "Finalizar projeto LifePlanner",
            "description": "Concluir a aplicação, testar funcionalidades e preparar a entrega final.",
            "category": "Projeto",
            "target_date": "2026-07-31",
            "status": "Ativo",
            "is_main": 1,
            "steps": [
                ("Implementar funcionalidades principais", 1),
                ("Adicionar meteorologia", 1),
                ("Atualizar README", 1),
                ("Criar dados de demonstração", 0),
                ("Testar aplicação final", 0),
            ],
        },
        {
            "title": "Melhorar organização pessoal",
            "description": "Usar o LifePlanner para planear tarefas, eventos e objetivos do mês.",
            "category": "Pessoal",
            "target_date": "2026-07-31",
            "status": "Ativo",
            "is_main": 0,
            "steps": [
                ("Planear tarefas semanais", 1),
                ("Registar eventos importantes", 1),
                ("Criar notas úteis", 0),
                ("Acompanhar progresso", 0),
            ],
        },
        {
            "title": "Preparar apresentação final",
            "description": "Preparar uma demonstração clara e objetiva da aplicação.",
            "category": "Estudo",
            "target_date": "2026-07-28",
            "status": "Ativo",
            "is_main": 0,
            "steps": [
                ("Definir ordem da apresentação", 1),
                ("Ensaiar demonstração", 0),
                ("Preparar respostas a perguntas", 0),
            ],
        },
    ]

    for goal in goals:
        goal_id = insert_dynamic(cursor, "goals", {
            "user_id": user_id,
            "title": goal["title"],
            "description": goal["description"],
            "category": goal["category"],
            "target_date": goal["target_date"],
            "status": goal["status"],
            "is_main": goal["is_main"],
            "created_at": now(),
            "updated_at": now(),
        })

        for index, step in enumerate(goal["steps"], start=1):
            step_title, completed = step

            insert_dynamic(cursor, "goal_steps", {
                "goal_id": goal_id,
                "title": step_title,
                "description": "",
                "is_completed": completed,
                "step_order": index,
                "created_at": now(),
                "updated_at": now(),
            })


def main():
    connection = get_connection()
    cursor = connection.cursor()

    user_id = create_or_update_demo_user(cursor)

    clear_demo_user_data(cursor, user_id)

    seed_tasks(cursor, user_id)
    seed_events(cursor, user_id)
    seed_notes(cursor, user_id)
    seed_goals(cursor, user_id)

    connection.commit()
    connection.close()

    print("Dados de demonstração criados com sucesso.")
    print(f"Email: {DEMO_EMAIL}")
    print(f"Password: {DEMO_PASSWORD}")


if __name__ == "__main__":
    main()