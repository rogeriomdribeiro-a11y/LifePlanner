"""Operações de persistência relacionadas com tarefas."""

from datetime import date

from database.connection import get_connection


class TaskRepository:
    """Disponibilizar operações CRUD e contagens usadas no Dashboard."""

    def __init__(self) -> None:
        self.connection = get_connection()

    def create_task(
        self,
        user_id,
        title,
        description="",
        category="Pessoal",
        due_date=None,
        due_time=None,
        priority="Normal",
    ):
        """Criar uma tarefa pendente e devolver o identificador gerado."""
        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO tasks (
                user_id,
                title,
                description,
                category,
                due_date,
                due_time,
                priority
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                title,
                description,
                category,
                due_date,
                due_time,
                priority,
            ),
        )

        self.connection.commit()
        return cursor.lastrowid

    def get_tasks_by_user(self, user_id):
        """Listar todas as tarefas do utilizador numa ordem cronológica."""
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM tasks
            WHERE user_id = ?
            ORDER BY
                is_completed ASC,
                due_date IS NULL,
                due_date ASC,
                due_time IS NULL,
                due_time ASC,
                created_at DESC
            """,
            (user_id,),
        )

        return cursor.fetchall()

    def get_today_tasks(self, user_id, limit=5):
        """Obter as tarefas do dia atual apresentadas no Dashboard."""
        today = date.today().isoformat()
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM tasks
            WHERE user_id = ?
              AND due_date = ?
            ORDER BY
                is_completed ASC,
                due_time IS NULL,
                due_time ASC,
                created_at DESC
            LIMIT ?
            """,
            (user_id, today, limit),
        )

        return cursor.fetchall()

    def count_today_tasks(self, user_id) -> int:
        """Contar todas as tarefas com data igual ao dia atual."""
        today = date.today().isoformat()
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM tasks
            WHERE user_id = ?
              AND due_date = ?
            """,
            (user_id, today),
        )

        result = cursor.fetchone()
        return result["total"] if result else 0

    def count_completed_today_tasks(self, user_id) -> int:
        """Contar as tarefas de hoje que já foram concluídas."""
        today = date.today().isoformat()
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM tasks
            WHERE user_id = ?
              AND due_date = ?
              AND is_completed = 1
            """,
            (user_id, today),
        )

        result = cursor.fetchone()
        return result["total"] if result else 0

    def update_task(
        self,
        task_id,
        user_id,
        title,
        description="",
        category="Pessoal",
        due_date=None,
        due_time=None,
        priority="Normal",
    ) -> None:
        """Editar uma tarefa pendente pertencente ao utilizador."""
        cursor = self.connection.cursor()

        cursor.execute(
            """
            UPDATE tasks
            SET
                title = ?,
                description = ?,
                category = ?,
                due_date = ?,
                due_time = ?,
                priority = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
              AND user_id = ?
              AND is_completed = 0
            """,
            (
                title,
                description,
                category,
                due_date,
                due_time,
                priority,
                task_id,
                user_id,
            ),
        )

        self.connection.commit()

    def update_task_status(self, task_id, user_id, is_completed) -> None:
        """Marcar uma tarefa como concluída ou voltar a colocá-la pendente."""
        cursor = self.connection.cursor()

        cursor.execute(
            """
            UPDATE tasks
            SET
                is_completed = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
              AND user_id = ?
            """,
            (
                1 if is_completed else 0,
                task_id,
                user_id,
            ),
        )

        self.connection.commit()

    def delete_task(self, task_id, user_id) -> None:
        """Eliminar uma tarefa pertencente ao utilizador autenticado."""
        cursor = self.connection.cursor()

        cursor.execute(
            """
            DELETE FROM tasks
            WHERE id = ?
              AND user_id = ?
            """,
            (task_id, user_id),
        )

        self.connection.commit()
