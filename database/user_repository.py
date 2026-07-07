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