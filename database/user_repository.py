import sqlite3
import bcrypt

from database.connection import get_connection


class UserRepository:
    def __init__(self):
        self.connection = get_connection()

    def get_user_by_email(self, email):
        cursor = self.connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        )

        return cursor.fetchone()

    def create_user(self, full_name, email, password):
        if self.get_user_by_email(email):
            return False, "Este email já está registado."

        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        try:
            cursor = self.connection.cursor()

            cursor.execute("""
                INSERT INTO users (
                    full_name,
                    email,
                    password_hash
                )
                VALUES (?, ?, ?)
            """, (
                full_name,
                email,
                password_hash
            ))

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
            user["password_hash"].encode("utf-8")
        )

        if not password_ok:
            return False, "Credenciais inválidas.", None

        return True, "Login efetuado com sucesso.", user