import bcrypt

from database.connection import get_connection



class UserRepository:

    def __init__(self):
        self.connection = get_connection()

    def create_user(self, full_name, email, password):

        cursor = self.connection.cursor()

        password_hash = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()

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

        return cursor.lastrowid
    
