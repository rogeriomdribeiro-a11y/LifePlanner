from database.connection import get_connection


class NoteRepository:
    def __init__(self):
        self.connection = get_connection()

    def create_note(
        self,
        user_id,
        title,
        content="",
        category="Geral",
        color="#8B5CF6",
        is_pinned=False,
    ):
        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT INTO notes (
                user_id,
                title,
                content,
                category,
                color,
                is_pinned
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            title,
            content,
            category,
            color,
            1 if is_pinned else 0,
        ))

        self.connection.commit()

        return cursor.lastrowid

    def get_notes_by_user(self, user_id):
        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT *
            FROM notes
            WHERE user_id = ?
            ORDER BY
                is_pinned DESC,
                updated_at DESC,
                created_at DESC
        """, (user_id,))

        return cursor.fetchall()

    def get_recent_notes(self, user_id, limit=5):
        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT *
            FROM notes
            WHERE user_id = ?
            ORDER BY
                updated_at DESC,
                created_at DESC
            LIMIT ?
        """, (user_id, limit))

        return cursor.fetchall()

    def count_notes_by_user(self, user_id):
        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM notes
            WHERE user_id = ?
        """, (user_id,))

        result = cursor.fetchone()

        return result["total"] if result else 0

    def update_note(
        self,
        note_id,
        user_id,
        title,
        content="",
        category="Geral",
        color="#8B5CF6",
        is_pinned=False,
    ):
        cursor = self.connection.cursor()

        cursor.execute("""
            UPDATE notes
            SET title = ?,
                content = ?,
                category = ?,
                color = ?,
                is_pinned = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
              AND user_id = ?
        """, (
            title,
            content,
            category,
            color,
            1 if is_pinned else 0,
            note_id,
            user_id,
        ))

        self.connection.commit()

    def delete_note(self, note_id, user_id):
        cursor = self.connection.cursor()

        cursor.execute("""
            DELETE FROM notes
            WHERE id = ?
              AND user_id = ?
        """, (note_id, user_id))


    def toggle_note_pin(self, note_id, user_id, is_pinned):
        cursor = self.connection.cursor()

        cursor.execute("""
            UPDATE notes
            SET is_pinned = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            AND user_id = ?
        """, (
            1 if is_pinned else 0,
            note_id,
            user_id,
        ))

        self.connection.commit()
        self.connection.commit()