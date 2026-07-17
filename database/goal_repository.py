"""Operações de persistência relacionadas com objetivos e respetivas etapas."""

from database.connection import get_connection

class GoalRepository:
    """Gerir objetivos, etapas, progresso automático e objetivo principal."""

    def __init__(self) -> None:
        self.connection = get_connection()

    def create_goal(
        self,
        user_id,
        title,
        description="",
        category="Pessoal",
        target_date=None,
        progress=0,
        status="Em progresso",
        color="#10B981",
        steps=None,
        is_main=False,
    ):
        """Criar um objetivo e as suas etapas numa única transação.

        O argumento ``progress`` é mantido por compatibilidade com a interface,
        mas o valor guardado é sempre calculado a partir das etapas concluídas.
        """
        del progress
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO goals (
                    user_id,
                    title,
                    description,
                    category,
                    target_date,
                    progress,
                    status,
                    color,
                    is_main
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    title,
                    description,
                    category,
                    target_date,
                    0,
                    status,
                    color,
                    1 if is_main else 0,
                ),
            )

            goal_id = cursor.lastrowid

            # As etapas são inseridas antes do cálculo inicial do progresso.
            if steps:
                self._create_goal_steps(cursor, goal_id, steps)

            if is_main:
                self._set_main_goal(cursor, goal_id, user_id)

            self._recalculate_goal_progress(cursor, goal_id, user_id)
            self.connection.commit()
            return goal_id

        except Exception:
            self.connection.rollback()
            raise

    def get_goals_by_user(self, user_id):
        """Listar objetivos por estado, destaque, prazo e atualização."""
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM goals
            WHERE user_id = ?
            ORDER BY
                CASE
                    WHEN status = 'Em progresso' THEN 0
                    WHEN status = 'Pausado' THEN 1
                    WHEN status = 'Concluído' THEN 2
                    ELSE 3
                END,
                is_main DESC,
                target_date IS NULL,
                target_date ASC,
                updated_at DESC
            """,
            (user_id,),
        )

        return cursor.fetchall()

    def get_goal_by_id(self, goal_id, user_id):
        """Obter um objetivo apenas quando pertence ao utilizador indicado."""
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM goals
            WHERE id = ?
              AND user_id = ?
            """,
            (goal_id, user_id),
        )

        return cursor.fetchone()

    def get_main_goal(self, user_id):
        """Obter o objetivo principal ou, na falta dele, o mais relevante."""
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM goals
            WHERE user_id = ?
              AND status != 'Concluído'
            ORDER BY
                is_main DESC,
                progress DESC,
                target_date IS NULL,
                target_date ASC,
                updated_at DESC
            LIMIT 1
            """,
            (user_id,),
        )

        return cursor.fetchone()

    def count_goals_by_user(self, user_id) -> int:
        """Contar todos os objetivos do utilizador."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM goals WHERE user_id = ?", (user_id,))
        return cursor.fetchone()[0]

    def count_active_goals(self, user_id) -> int:
        """Contar objetivos que ainda não foram concluídos."""
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM goals
            WHERE user_id = ?
              AND status != 'Concluído'
            """,
            (user_id,),
        )
        return cursor.fetchone()[0]

    def count_completed_goals(self, user_id) -> int:
        """Contar objetivos cujo progresso chegou aos 100%."""
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM goals
            WHERE user_id = ?
              AND status = 'Concluído'
            """,
            (user_id,),
        )
        return cursor.fetchone()[0]

    def update_goal(
        self,
        goal_id,
        user_id,
        title,
        description="",
        category="Pessoal",
        target_date=None,
        progress=0,
        status="Em progresso",
        color="#10B981",
        steps=None,
        is_main=False,
    ) -> None:
        """Atualizar o objetivo e substituir as etapas quando necessário."""
        del progress
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                """
                UPDATE goals
                SET
                    title = ?,
                    description = ?,
                    category = ?,
                    target_date = ?,
                    status = ?,
                    color = ?,
                    is_main = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                  AND user_id = ?
                """,
                (
                    title,
                    description,
                    category,
                    target_date,
                    status,
                    color,
                    1 if is_main else 0,
                    goal_id,
                    user_id,
                ),
            )

            # Interrompe a operação se o objetivo não pertencer ao utilizador.
            if cursor.rowcount == 0:
                self.connection.rollback()
                return

            if steps is not None:
                cursor.execute("DELETE FROM goal_steps WHERE goal_id = ?", (goal_id,))
                self._create_goal_steps(cursor, goal_id, steps)

            if is_main:
                self._set_main_goal(cursor, goal_id, user_id)

            self._recalculate_goal_progress(cursor, goal_id, user_id)
            self.connection.commit()

        except Exception:
            self.connection.rollback()
            raise

    def delete_goal(self, goal_id, user_id) -> None:
        """Eliminar um objetivo; as etapas são removidas por cascata."""
        cursor = self.connection.cursor()
        cursor.execute(
            "DELETE FROM goals WHERE id = ? AND user_id = ?",
            (goal_id, user_id),
        )
        self.connection.commit()

    def set_main_goal(self, goal_id, user_id) -> None:
        """Definir um único objetivo principal para o utilizador."""
        cursor = self.connection.cursor()

        try:
            self._set_main_goal(cursor, goal_id, user_id)
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise

    def _set_main_goal(self, cursor, goal_id, user_id) -> None:
        """Aplicar o destaque principal dentro de uma transação existente."""
        cursor.execute(
            "UPDATE goals SET is_main = 0 WHERE user_id = ?",
            (user_id,),
        )
        cursor.execute(
            """
            UPDATE goals
            SET
                is_main = 1,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
              AND user_id = ?
            """,
            (goal_id, user_id),
        )

    def _create_goal_steps(self, cursor, goal_id, steps) -> None:
        """Inserir etapas usando o cursor da transação atual."""
        for index, step in enumerate(steps):
            title = step.get("title", "").strip()
            description = step.get("description", "").strip()
            is_completed = 1 if step.get("is_completed", False) else 0

            # Etapas sem título são ignoradas para não criar linhas vazias.
            if not title:
                continue

            cursor.execute(
                """
                INSERT INTO goal_steps (
                    goal_id,
                    title,
                    description,
                    is_completed,
                    position
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (goal_id, title, description, is_completed, index),
            )

    def get_goal_steps(self, goal_id):
        """Listar as etapas pela posição definida no formulário."""
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT *
            FROM goal_steps
            WHERE goal_id = ?
            ORDER BY position ASC, id ASC
            """,
            (goal_id,),
        )
        return cursor.fetchall()

    def toggle_goal_step(self, step_id, goal_id, user_id, is_completed) -> None:
        """Alterar o estado de uma etapa e recalcular o progresso do objetivo."""
        cursor = self.connection.cursor()

        try:
            # A cláusula EXISTS impede alterar etapas de outro utilizador.
            cursor.execute(
                """
                UPDATE goal_steps
                SET
                    is_completed = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                  AND goal_id = ?
                  AND EXISTS (
                      SELECT 1
                      FROM goals
                      WHERE goals.id = goal_steps.goal_id
                        AND goals.user_id = ?
                  )
                """,
                (
                    1 if is_completed else 0,
                    step_id,
                    goal_id,
                    user_id,
                ),
            )

            if cursor.rowcount:
                self._recalculate_goal_progress(cursor, goal_id, user_id)

            self.connection.commit()

        except Exception:
            self.connection.rollback()
            raise

    def _recalculate_goal_progress(self, cursor, goal_id, user_id) -> None:
        """Calcular a percentagem com base nas etapas dentro da transação atual."""
        cursor.execute(
            "SELECT COUNT(*) FROM goal_steps WHERE goal_id = ?",
            (goal_id,),
        )
        total_steps = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM goal_steps
            WHERE goal_id = ?
              AND is_completed = 1
            """,
            (goal_id,),
        )
        completed_steps = cursor.fetchone()[0]

        progress = 0 if total_steps == 0 else round(
            (completed_steps / total_steps) * 100
        )

        if total_steps > 0 and completed_steps == total_steps:
            status = "Concluído"
        else:
            cursor.execute(
                "SELECT status FROM goals WHERE id = ? AND user_id = ?",
                (goal_id, user_id),
            )
            current_goal = cursor.fetchone()
            status = (
                "Pausado"
                if current_goal and current_goal["status"] == "Pausado"
                else "Em progresso"
            )

        cursor.execute(
            """
            UPDATE goals
            SET
                progress = ?,
                status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
              AND user_id = ?
            """,
            (progress, status, goal_id, user_id),
        )
