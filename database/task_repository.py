from datetime import date

from database.connection import get_connection


class TaskRepository:
    def __init__(self):
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
        cursor = self.connection.cursor()

        cursor.execute("""
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
        """, (
            user_id,
            title,
            description,
            category,
            due_date,
            due_time,
            priority,
        ))

        self.connection.commit()

        return cursor.lastrowid

    def get_tasks_by_user(self, user_id):
        cursor = self.connection.cursor()

        cursor.execute("""
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
        """, (user_id,))

        return cursor.fetchall()

    def get_today_tasks(self, user_id, limit=5):
        today = date.today().isoformat()

        cursor = self.connection.cursor()

        cursor.execute("""
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
        """, (user_id, today, limit))

        return cursor.fetchall()

    def count_today_tasks(self, user_id):
        today = date.today().isoformat()

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM tasks
            WHERE user_id = ?
              AND due_date = ?
        """, (user_id, today))

        result = cursor.fetchone()

        return result["total"] if result else 0

    def count_completed_today_tasks(self, user_id):
        today = date.today().isoformat()

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM tasks
            WHERE user_id = ?
              AND due_date = ?
              AND is_completed = 1
        """, (user_id, today))

        result = cursor.fetchone()

        return result["total"] if result else 0

    def update_task_status(self, task_id, user_id, is_completed):
        cursor = self.connection.cursor()

        cursor.execute("""
            UPDATE tasks
            SET is_completed = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
              AND user_id = ?
        """, (
            1 if is_completed else 0,
            task_id,
            user_id,
        ))

        self.connection.commit()

    def delete_task(self, task_id, user_id):
        cursor = self.connection.cursor()

        cursor.execute("""
            DELETE FROM tasks
            WHERE id = ?
              AND user_id = ?
        """, (task_id, user_id))

        self.connection.commit()

    def ensure_sample_tasks_for_today(self, user_id):
        if self.count_today_tasks(user_id) > 0:
            return

        today = date.today().isoformat()

        sample_tasks = [
            ("Comprar leite", "Pessoal", "09:00"),
            ("Preparar apresentação", "Trabalho", "11:30"),
            ("Marcar consulta", "Saúde", "14:00"),
            ("Responder a e-mails", "Trabalho", "16:00"),
            ("Rever relatório mensal", "Trabalho", "17:30"),
        ]

        for title, category, due_time in sample_tasks:
            self.create_task(
                user_id=user_id,
                title=title,
                category=category,
                due_date=today,
                due_time=due_time,
            )