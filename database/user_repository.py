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
            (email.lower().strip(),),
        )

        return cursor.fetchone()

    def get_user_by_oauth_id(self, oauth_user_id):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE oauth_user_id = ?
            """,
            (oauth_user_id,),
        )

        return cursor.fetchone()

    def create_user(self, full_name, email, password):
        email = email.lower().strip()

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
                    password_hash,
                    provider
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    full_name.strip(),
                    email,
                    password_hash,
                    "local",
                ),
            )

            self.connection.commit()

            return True, "Conta criada com sucesso."

        except sqlite3.Error:
            return False, "Ocorreu um erro ao criar a conta."

    def authenticate_user(self, email, password):
        email = email.lower().strip()

        user = self.get_user_by_email(email)

        if user is None:
            return False, "Utilizador não encontrado.", None

        if not user["password_hash"]:
            return (
                False,
                "Esta conta foi criada com Google. Use o botão Continuar com Google.",
                None,
            )

        password_ok = bcrypt.checkpw(
            password.encode("utf-8"),
            user["password_hash"].encode("utf-8"),
        )

        if not password_ok:
            return False, "Credenciais inválidas.", None

        self.update_last_login(user["id"])
        user = self.get_user_by_id(user["id"])

        return True, "Login efetuado com sucesso.", user

    def get_or_create_google_user(self, google_user):
        oauth_user_id = google_user["oauth_user_id"]
        email = google_user["email"].lower().strip()
        full_name = google_user["full_name"].strip()
        profile_picture = google_user.get("profile_picture")
        email_verified = int(google_user.get("email_verified", 0))

        try:
            existing_user = self.get_user_by_oauth_id(oauth_user_id)

            if existing_user:
                self.update_google_user_data(
                    user_id=existing_user["id"],
                    full_name=full_name,
                    email=email,
                    profile_picture=profile_picture,
                    email_verified=email_verified,
                    oauth_user_id=oauth_user_id,
                )

                return (
                    True,
                    "Login Google efetuado com sucesso.",
                    self.get_user_by_id(existing_user["id"]),
                )

            existing_email_user = self.get_user_by_email(email)

            if existing_email_user:
                self.update_google_user_data(
                    user_id=existing_email_user["id"],
                    full_name=existing_email_user["full_name"] or full_name,
                    email=email,
                    profile_picture=profile_picture,
                    email_verified=email_verified,
                    oauth_user_id=oauth_user_id,
                )

                return (
                    True,
                    "Conta associada ao Google com sucesso.",
                    self.get_user_by_id(existing_email_user["id"]),
                )

            cursor = self.connection.cursor()

            cursor.execute(
                """
                INSERT INTO users (
                    full_name,
                    email,
                    password_hash,
                    provider,
                    oauth_user_id,
                    profile_picture,
                    email_verified,
                    last_login
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """,
                (
                    full_name,
                    email,
                    "",
                    "google",
                    oauth_user_id,
                    profile_picture,
                    email_verified,
                ),
            )

            self.connection.commit()

            user_id = cursor.lastrowid

            return (
                True,
                "Conta Google criada com sucesso.",
                self.get_user_by_id(user_id),
            )

        except sqlite3.Error as error:
            return False, f"Ocorreu um erro ao autenticar com Google: {error}", None

    def update_google_user_data(
        self,
        user_id,
        full_name,
        email,
        profile_picture,
        email_verified,
        oauth_user_id,
    ):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            UPDATE users
            SET
                full_name = ?,
                email = ?,
                provider = ?,
                oauth_user_id = ?,
                profile_picture = ?,
                email_verified = ?,
                last_login = CURRENT_TIMESTAMP,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                full_name,
                email,
                "google",
                oauth_user_id,
                profile_picture,
                email_verified,
                user_id,
            ),
        )

        self.connection.commit()

    def update_last_login(self, user_id):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            UPDATE users
            SET
                last_login = CURRENT_TIMESTAMP,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (user_id,),
        )

        self.connection.commit()

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

        if not user["password_hash"]:
            return (
                False,
                "Esta conta foi criada com Google e ainda não tem password local.",
            )

        password_ok = bcrypt.checkpw(
            current_password.encode("utf-8"),
            user["password_hash"].encode("utf-8"),
        )

        if not password_ok:
            return False, "A password atual está incorreta."

        if len(new_password) < 6:
            return False, "A nova password deve ter pelo menos 6 caracteres."

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