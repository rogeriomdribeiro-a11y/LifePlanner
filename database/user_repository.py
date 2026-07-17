"""Operações de persistência e autenticação relacionadas com utilizadores."""

import sqlite3

import bcrypt

from database.connection import get_connection


class UserRepository:
    """Gerir contas locais, contas Google e dados do perfil."""

    def __init__(self) -> None:
        self.connection = get_connection()

    def get_user_by_id(self, user_id):
        """Obter um utilizador pelo identificador interno."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()

    def get_user_by_email(self, email):
        """Procurar um utilizador usando um email normalizado."""
        normalized_email = email.lower().strip()
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE email = ?",
            (normalized_email,),
        )
        return cursor.fetchone()

    def get_user_by_oauth_id(self, oauth_user_id):
        """Procurar uma conta previamente associada ao Google."""
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE oauth_user_id = ?",
            (oauth_user_id,),
        )
        return cursor.fetchone()

    def create_user(self, full_name, email, password):
        """Criar uma conta local com a password protegida por bcrypt."""
        full_name = full_name.strip()
        email = email.lower().strip()

        if not full_name:
            return False, "O nome completo não pode estar vazio."

        if not email or "@" not in email:
            return False, "Introduz um email válido."

        if self.get_user_by_email(email):
            return False, "Este email já está registado."

        if len(password) < 6:
            return False, "A password deve ter pelo menos 6 caracteres."

        # A aplicação nunca guarda a password original; apenas o hash bcrypt.
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
                (full_name, email, password_hash, "local"),
            )
            self.connection.commit()
            return True, "Conta criada com sucesso."

        except sqlite3.IntegrityError:
            self.connection.rollback()
            return False, "Este email já está registado."
        except sqlite3.Error:
            self.connection.rollback()
            return False, "Ocorreu um erro ao criar a conta."

    def authenticate_user(self, email, password):
        """Validar uma conta local e devolver o respetivo registo."""
        user = self.get_user_by_email(email)

        if user is None:
            return False, "Utilizador não encontrado.", None

        if not bool(user["is_active"]):
            return False, "Esta conta encontra-se desativada.", None

        if not user["password_hash"]:
            return (
                False,
                "Esta conta foi criada com Google. Use o botão Continuar com Google.",
                None,
            )

        try:
            password_ok = bcrypt.checkpw(
                password.encode("utf-8"),
                user["password_hash"].encode("utf-8"),
            )
        except (TypeError, ValueError):
            return False, "Não foi possível validar as credenciais.", None

        if not password_ok:
            return False, "Credenciais inválidas.", None

        self.update_last_login(user["id"])
        return True, "Login efetuado com sucesso.", self.get_user_by_id(user["id"])

    def get_or_create_google_user(self, google_user):
        """Obter, associar ou criar o utilizador autenticado pelo Google."""
        oauth_user_id = google_user["oauth_user_id"]
        email = google_user["email"].lower().strip()
        full_name = google_user["full_name"].strip()
        profile_picture = google_user.get("profile_picture")
        email_verified = int(google_user.get("email_verified", 0))

        if not email_verified:
            return False, "O email da conta Google não está verificado.", None

        try:
            # Primeiro procura a associação direta pelo identificador Google.
            existing_user = self.get_user_by_oauth_id(oauth_user_id)

            if existing_user:
                if not bool(existing_user["is_active"]):
                    return False, "Esta conta encontra-se desativada.", None

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

            # Se já existir uma conta local com o mesmo email verificado,
            # associa-a ao Google em vez de criar um registo duplicado.
            existing_email_user = self.get_user_by_email(email)

            if existing_email_user:
                if not bool(existing_email_user["is_active"]):
                    return False, "Esta conta encontra-se desativada.", None

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

        except sqlite3.IntegrityError:
            self.connection.rollback()
            return False, "Esta conta Google já se encontra associada.", None
        except sqlite3.Error:
            self.connection.rollback()
            return False, "Ocorreu um erro ao autenticar com Google.", None

    def update_google_user_data(
        self,
        user_id,
        full_name,
        email,
        profile_picture,
        email_verified,
        oauth_user_id,
    ) -> None:
        """Atualizar os dados recebidos da conta Google."""
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

    def update_last_login(self, user_id) -> None:
        """Registar o momento da última autenticação local."""
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
        """Alterar o nome apresentado na aplicação."""
        full_name = full_name.strip()

        if not full_name:
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
                (full_name, user_id),
            )
            self.connection.commit()

            if cursor.rowcount == 0:
                return False, "Utilizador não encontrado."

            return True, "Nome atualizado com sucesso."

        except sqlite3.Error:
            self.connection.rollback()
            return False, "Ocorreu um erro ao atualizar o nome."

    def change_password(self, user_id, current_password, new_password):
        """Validar a password atual e guardar um novo hash bcrypt."""
        user = self.get_user_by_id(user_id)

        if user is None:
            return False, "Utilizador não encontrado."

        if not user["password_hash"]:
            return (
                False,
                "Esta conta foi criada com Google e ainda não tem password local.",
            )

        try:
            password_ok = bcrypt.checkpw(
                current_password.encode("utf-8"),
                user["password_hash"].encode("utf-8"),
            )
        except (TypeError, ValueError):
            return False, "Não foi possível validar a password atual."

        if not password_ok:
            return False, "A password atual está incorreta."

        if len(new_password) < 6:
            return False, "A nova password deve ter pelo menos 6 caracteres."

        try:
            same_password = bcrypt.checkpw(
                new_password.encode("utf-8"),
                user["password_hash"].encode("utf-8"),
            )
        except (TypeError, ValueError):
            return False, "Não foi possível validar a nova password."

        if same_password:
            return False, "A nova password deve ser diferente da atual."

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
                (new_password_hash, user_id),
            )
            self.connection.commit()
            return True, "Password alterada com sucesso."

        except sqlite3.Error:
            self.connection.rollback()
            return False, "Ocorreu um erro ao alterar a password."
