"""Autenticação do utilizador através do Google OAuth 2.0."""

from google.auth.transport.requests import AuthorizedSession
from google_auth_oauthlib.flow import InstalledAppFlow

from app.path import CONFIG_DIR


GOOGLE_CLIENT_FILE = CONFIG_DIR / "google_oauth_client.json"
SCOPES = (
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
)


class GoogleAuthService:
    """Executar o fluxo OAuth e normalizar os dados devolvidos pelo Google."""

    def authenticate(self):
        """Abrir o browser, autenticar a conta e devolver os dados essenciais."""
        if not GOOGLE_CLIENT_FILE.exists():
            return False, (
                "O ficheiro de credenciais Google não foi encontrado.\n\n"
                "Guarda o ficheiro em:\n"
                "config/google_oauth_client.json"
            ), None

        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(GOOGLE_CLIENT_FILE),
                scopes=SCOPES,
            )
            credentials = flow.run_local_server(
                host="localhost",
                port=0,
                authorization_prompt_message=(
                    "A abrir o browser para iniciar sessão com Google..."
                ),
                success_message=(
                    "Login efetuado com sucesso. Pode fechar esta janela."
                ),
                open_browser=True,
            )

            session = AuthorizedSession(credentials)
            response = session.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                timeout=10,
            )
            response.raise_for_status()
            user_info = response.json()

            google_user = {
                "oauth_user_id": user_info.get("sub"),
                "email": user_info.get("email", "").lower().strip(),
                "full_name": (
                    user_info.get("name")
                    or user_info.get("email")
                    or "Utilizador Google"
                ).strip(),
                "profile_picture": user_info.get("picture"),
                "email_verified": int(bool(user_info.get("email_verified"))),
            }

            if not google_user["oauth_user_id"] or not google_user["email"]:
                return (
                    False,
                    "A conta Google não devolveu os dados necessários.",
                    None,
                )

            return True, "Login Google efetuado com sucesso.", google_user

        except Exception as error:
            return (
                False,
                "Não foi possível iniciar sessão com Google.\n"
                f"Detalhe técnico: {error}",
                None,
            )
