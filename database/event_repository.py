"""Operações de persistência relacionadas com eventos do calendário."""

from datetime import date

from database.connection import get_connection


class EventRepository:
    """Disponibilizar operações CRUD e contagens de eventos."""

    def __init__(self) -> None:
        self.connection = get_connection()

    def create_event(
        self,
        user_id,
        title,
        description="",
        event_date=None,
        start_time=None,
        end_time=None,
        location="",
        color="#3B82F6",
    ):
        """Criar um evento e devolver o identificador gerado."""
        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO events (
                user_id,
                title,
                description,
                event_date,
                start_time,
                end_time,
                location,
                color
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                title,
                description,
                event_date,
                start_time,
                end_time,
                location,
                color,
            ),
        )

        self.connection.commit()
        return cursor.lastrowid

    def get_events_by_user(self, user_id):
        """Listar todos os eventos do utilizador por data e hora."""
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM events
            WHERE user_id = ?
            ORDER BY
                event_date ASC,
                start_time IS NULL,
                start_time ASC,
                created_at DESC
            """,
            (user_id,),
        )

        return cursor.fetchall()

    def get_today_events(self, user_id, limit=5):
        """Obter os próximos eventos do dia atual para o Dashboard."""
        today = date.today().isoformat()
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM events
            WHERE user_id = ?
              AND event_date = ?
            ORDER BY
                start_time IS NULL,
                start_time ASC,
                created_at DESC
            LIMIT ?
            """,
            (user_id, today, limit),
        )

        return cursor.fetchall()

    def count_today_events(self, user_id) -> int:
        """Contar os eventos marcados para o dia atual."""
        today = date.today().isoformat()
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM events
            WHERE user_id = ?
              AND event_date = ?
            """,
            (user_id, today),
        )

        result = cursor.fetchone()
        return result["total"] if result else 0

    def update_event(
        self,
        event_id,
        user_id,
        title,
        description="",
        event_date=None,
        start_time=None,
        end_time=None,
        location="",
        color="#3B82F6",
    ) -> None:
        """Atualizar um evento pertencente ao utilizador autenticado."""
        cursor = self.connection.cursor()

        cursor.execute(
            """
            UPDATE events
            SET
                title = ?,
                description = ?,
                event_date = ?,
                start_time = ?,
                end_time = ?,
                location = ?,
                color = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
              AND user_id = ?
            """,
            (
                title,
                description,
                event_date,
                start_time,
                end_time,
                location,
                color,
                event_id,
                user_id,
            ),
        )

        self.connection.commit()

    def delete_event(self, event_id, user_id) -> None:
        """Eliminar um evento pertencente ao utilizador autenticado."""
        cursor = self.connection.cursor()

        cursor.execute(
            """
            DELETE FROM events
            WHERE id = ?
              AND user_id = ?
            """,
            (event_id, user_id),
        )

        self.connection.commit()
