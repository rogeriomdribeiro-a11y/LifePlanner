from datetime import date

from database.connection import get_connection


class EventRepository:
    def __init__(self):
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
        cursor = self.connection.cursor()

        cursor.execute("""
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
        """, (
            user_id,
            title,
            description,
            event_date,
            start_time,
            end_time,
            location,
            color,
        ))

        self.connection.commit()

        return cursor.lastrowid

    def get_events_by_user(self, user_id):
        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT *
            FROM events
            WHERE user_id = ?
            ORDER BY
                event_date ASC,
                start_time IS NULL,
                start_time ASC,
                created_at DESC
        """, (user_id,))

        return cursor.fetchall()

    def get_today_events(self, user_id, limit=5):
        today = date.today().isoformat()

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT *
            FROM events
            WHERE user_id = ?
              AND event_date = ?
            ORDER BY
                start_time IS NULL,
                start_time ASC,
                created_at DESC
            LIMIT ?
        """, (user_id, today, limit))

        return cursor.fetchall()

    def count_today_events(self, user_id):
        today = date.today().isoformat()

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM events
            WHERE user_id = ?
              AND event_date = ?
        """, (user_id, today))

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
    ):
        cursor = self.connection.cursor()

        cursor.execute("""
            UPDATE events
            SET title = ?,
                description = ?,
                event_date = ?,
                start_time = ?,
                end_time = ?,
                location = ?,
                color = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
              AND user_id = ?
        """, (
            title,
            description,
            event_date,
            start_time,
            end_time,
            location,
            color,
            event_id,
            user_id,
        ))

        self.connection.commit()

    def delete_event(self, event_id, user_id):
        cursor = self.connection.cursor()

        cursor.execute("""
            DELETE FROM events
            WHERE id = ?
              AND user_id = ?
        """, (event_id, user_id))

        self.connection.commit()

    def ensure_sample_events_for_today(self, user_id):
        if self.count_today_events(user_id) > 0:
            return

        today = date.today().isoformat()

        sample_events = [
            (
                "Reunião de equipa",
                "Revisão semanal do projeto",
                today,
                "15:00",
                "16:00",
                "Sala 2B",
                "#3B82F6",
            ),
            (
                "Ginásio",
                "Treino de força",
                today,
                "18:30",
                "19:30",
                "Fitness Club",
                "#10B981",
            ),
            (
                "Aniversário da Ana",
                "Jantar de aniversário",
                today,
                "20:00",
                "22:00",
                "Restaurante",
                "#8B5CF6",
            ),
        ]

        for title, description, event_date, start_time, end_time, location, color in sample_events:
            self.create_event(
                user_id=user_id,
                title=title,
                description=description,
                event_date=event_date,
                start_time=start_time,
                end_time=end_time,
                location=location,
                color=color,
            )