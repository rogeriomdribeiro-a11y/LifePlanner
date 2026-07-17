"""Operações de persistência relacionadas com notas."""

from database.connection import get_connection


class NoteRepository:
    """Disponibilizar operações CRUD para as notas de um utilizador."""

    def __init__(self) -> None:
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
        """Criar uma nota e devolver o respetivo identificador."""
        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO notes (
                user_id,
                title,
                content,
                category,
                color,
                is_pinned
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                title,
                content,
                category,
                color,
                1 if is_pinned else 0,
            ),
        )

        self.connection.commit()
        return cursor.lastrowid

    def get_notes_by_user(self, user_id):
        """Listar as notas, apresentando primeiro as notas fixadas."""
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM notes
            WHERE user_id = ?
            ORDER BY
                is_pinned DESC,
                updated_at DESC,
                created_at DESC
            """,
            (user_id,),
        )

        return cursor.fetchall()

    def count_notes_by_user(self, user_id) -> int:
        """Contar as notas do utilizador para o resumo do Dashboard."""
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM notes
            WHERE user_id = ?
            """,
            (user_id,),
        )

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
    ) -> None:
        """Atualizar uma nota pertencente ao utilizador autenticado."""
        cursor = self.connection.cursor()

        cursor.execute(
            """
            UPDATE notes
            SET
                title = ?,
                content = ?,
                category = ?,
                color = ?,
                is_pinned = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
              AND user_id = ?
            """,
            (
                title,
                content,
                category,
                color,
                1 if is_pinned else 0,
                note_id,
                user_id,
            ),
        )

        self.connection.commit()

    def delete_note(self, note_id, user_id) -> None:
        """Eliminar definitivamente uma nota do utilizador."""
        cursor = self.connection.cursor()

        cursor.execute(
            """
            DELETE FROM notes
            WHERE id = ?
              AND user_id = ?
            """,
            (note_id, user_id),
        )

        # O commit é necessário para a eliminação persistir após reiniciar a app.
        self.connection.commit()

    def toggle_note_pin(self, note_id, user_id, is_pinned) -> None:
        """Fixar ou desafixar uma nota e atualizar a data de modificação."""
        cursor = self.connection.cursor()

        cursor.execute(
            """
            UPDATE notes
            SET
                is_pinned = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
              AND user_id = ?
            """,
            (
                1 if is_pinned else 0,
                note_id,
                user_id,
            ),
        )

        self.connection.commit()
