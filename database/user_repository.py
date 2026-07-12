import sqlite3
import bcrypt

from database.connection import get_connection


class UserRepository:
    def __init__(self):
        self.connection = get_connection()

    def get_user_by_id(self, user_id):
        cursor = self.connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,),
        )

        return cursor.fetchone()

    def get_user_by_email(self, email):
        cursor = self.connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,),
        )

        return cursor.fetchone()

    def create_user(self, full_name, email, password):
        if self.get_user_by_email(email):
            return False, "Este email já está registado."

        if len(password) < 6:
            return False, "A password deve ter pelo menos 6 caracteres."

        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt(),
        ).decode("utf-8")

        try:
            cursor = self.connection.cursor()

            cursor.execute(
                """
                INSERT INTO users (
                    full_name,
                    email,
                    password_hash
                )
                VALUES (?, ?, ?)
                """,
                (
                    full_name,
                    email,
                    password_hash,
                ),
            )

            self.connection.commit()

            return True, "Conta criada com sucesso."

        except sqlite3.Error:
            return False, "Ocorreu um erro ao criar a conta."

    def authenticate_user(self, email, password):
        user = self.get_user_by_email(email)

        if user is None:
            return False, "Utilizador não encontrado.", None

        password_ok = bcrypt.checkpw(
            password.encode("utf-8"),
            user["password_hash"].encode("utf-8"),
        )

        if not password_ok:
            return False, "Credenciais inválidas.", None

        return True, "Login efetuado com sucesso.", user

    def update_full_name(self, user_id, full_name):
        if not full_name.strip():
            return False, "O nome completo não pode estar vazio."

        try:
            cursor = self.connection.cursor()

            cursor.execute(
                """
                UPDATE users
                SET
                    full_name = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    full_name.strip(),
                    user_id,
                ),
            )

            self.connection.commit()

            return True, "Nome atualizado com sucesso."

        except sqlite3.Error:
            return False, "Ocorreu um erro ao atualizar o nome."

    def change_password(self, user_id, current_password, new_password):
        user = self.get_user_by_id(user_id)

        if user is None:
            return False, "Utilizador não encontrado."

        password_ok = bcrypt.checkpw(
            current_password.encode("utf-8"),
            user["password_hash"].encode("utf-8"),
        )

        if not password_ok:
            return False, "A password atual está incorreta."

        new_password_hash = bcrypt.hashpw(
            new_password.encode("utf-8"),
            bcrypt.gensalt(),
        ).decode("utf-8")

        try:
            cursor = self.connection.cursor()

            cursor.execute(
                """
                UPDATE users
                SET
                    password_hash = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    new_password_hash,
                    user_id,
                ),
            )

            self.connection.commit()

            return True, "Password alterada com sucesso."

        except sqlite3.Error:
            return False, "Ocorreu um erro ao alterar a password."