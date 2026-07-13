from app.path import BASE_DIR

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import AuthorizedSession


GOOGLE_CLIENT_FILE = BASE_DIR / "config" / "google_oauth_client.json"

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]


class GoogleAuthService:
    def authenticate(self):
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
                "https://www.googleapis.com/oauth2/v3/userinfo"
            )

            if response.status_code != 200:
                return False, "Não foi possível obter os dados da conta Google.", None

            user_info = response.json()

            google_user = {
                "oauth_user_id": user_info.get("sub"),
                "email": user_info.get("email", "").lower(),
                "full_name": user_info.get("name") or user_info.get("email"),
                "profile_picture": user_info.get("picture"),
                "email_verified": 1 if user_info.get("email_verified") else 0,
            }

            if not google_user["oauth_user_id"] or not google_user["email"]:
                return False, "A conta Google não devolveu dados suficientes.", None

            return True, "Login Google efetuado com sucesso.", google_user

        except Exception as error:
            return False, f"Não foi possível iniciar sessão com Google.\n{error}", None