from database.connection import get_connection


class GoalRepository:
    def __init__(self):
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
        cursor = self.connection.cursor()

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

        if steps:
            self.create_goal_steps(goal_id, steps)

        if is_main:
            self.set_main_goal(goal_id, user_id)

        self.recalculate_goal_progress(goal_id, user_id)

        self.connection.commit()
        return goal_id

    def get_goals_by_user(self, user_id):
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
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM goals
            WHERE id = ?
              AND user_id = ?
            """,
            (
                goal_id,
                user_id,
            ),
        )

        return cursor.fetchone()

    def get_active_goals(self, user_id):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM goals
            WHERE user_id = ?
              AND status != 'Concluído'
            ORDER BY
                is_main DESC,
                target_date IS NULL,
                target_date ASC,
                progress DESC,
                updated_at DESC
            """,
            (user_id,),
        )

        return cursor.fetchall()

    def get_main_goal(self, user_id):
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

    def count_goals_by_user(self, user_id):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM goals
            WHERE user_id = ?
            """,
            (user_id,),
        )

        return cursor.fetchone()[0]

    def count_active_goals(self, user_id):
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

    def count_completed_goals(self, user_id):
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
    ):
        cursor = self.connection.cursor()

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

        if steps is not None:
            self.replace_goal_steps(goal_id, steps)

        if is_main:
            self.set_main_goal(goal_id, user_id)

        self.recalculate_goal_progress(goal_id, user_id)

        self.connection.commit()

    def delete_goal(self, goal_id, user_id):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            DELETE FROM goals
            WHERE id = ?
              AND user_id = ?
            """,
            (
                goal_id,
                user_id,
            ),
        )

        self.connection.commit()

    def set_main_goal(self, goal_id, user_id):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            UPDATE goals
            SET is_main = 0
            WHERE user_id = ?
            """,
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
            (
                goal_id,
                user_id,
            ),
        )

        self.connection.commit()

    def create_goal_steps(self, goal_id, steps):
        cursor = self.connection.cursor()

        for index, step in enumerate(steps):
            title = step.get("title", "").strip()
            description = step.get("description", "").strip()
            is_completed = 1 if step.get("is_completed", False) else 0

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
                (
                    goal_id,
                    title,
                    description,
                    is_completed,
                    index,
                ),
            )

    def replace_goal_steps(self, goal_id, steps):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            DELETE FROM goal_steps
            WHERE goal_id = ?
            """,
            (goal_id,),
        )

        self.create_goal_steps(goal_id, steps)

    def get_goal_steps(self, goal_id):
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

    def count_goal_steps(self, goal_id):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM goal_steps
            WHERE goal_id = ?
            """,
            (goal_id,),
        )

        return cursor.fetchone()[0]

    def count_completed_goal_steps(self, goal_id):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM goal_steps
            WHERE goal_id = ?
              AND is_completed = 1
            """,
            (goal_id,),
        )

        return cursor.fetchone()[0]

    def toggle_goal_step(self, step_id, goal_id, user_id, is_completed):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            UPDATE goal_steps
            SET
                is_completed = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
              AND goal_id = ?
            """,
            (
                1 if is_completed else 0,
                step_id,
                goal_id,
            ),
        )

        self.recalculate_goal_progress(goal_id, user_id)

        self.connection.commit()

    def recalculate_goal_progress(self, goal_id, user_id):
        total_steps = self.count_goal_steps(goal_id)
        completed_steps = self.count_completed_goal_steps(goal_id)

        if total_steps == 0:
            progress = 0
        else:
            progress = round((completed_steps / total_steps) * 100)

        if total_steps > 0 and completed_steps == total_steps:
            status = "Concluído"
        else:
            current_goal = self.get_goal_by_id(goal_id, user_id)

            if current_goal and current_goal["status"] == "Pausado":
                status = "Pausado"
            else:
                status = "Em progresso"

        cursor = self.connection.cursor()

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
            (
                progress,
                status,
                goal_id,
                user_id,
            ),
        )

    def normalize_progress(self, progress):
        try:
            progress = int(progress)
        except (TypeError, ValueError):
            progress = 0

        if progress < 0:
            return 0

        if progress > 100:
            return 100

        return progress