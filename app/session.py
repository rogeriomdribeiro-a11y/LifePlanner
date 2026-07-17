"""Estado simples da sessão do utilizador autenticado."""


class Session:
    """Guardar em memória o utilizador autenticado durante a execução."""

    current_user = None

    @classmethod
    def login(cls, user) -> None:
        """Iniciar a sessão com o registo devolvido pela base de dados."""
        cls.current_user = user

    @classmethod
    def logout(cls) -> None:
        """Terminar a sessão atual."""
        cls.current_user = None

    @classmethod
    def is_authenticated(cls) -> bool:
        """Indicar se existe um utilizador autenticado."""
        return cls.current_user is not None
