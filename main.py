"""Ponto de entrada da aplicação LifePlanner.

Este módulo cria o controlador principal da aplicação e inicia o ciclo de eventos
Qt. A lógica da aplicação permanece em app/app.py para manter este ficheiro
simples e fácil de executar.
"""

from app.app import LifePlannerApp


def main() -> None:
    """Criar e executar a aplicação desktop."""
    application = LifePlannerApp()
    application.run()


if __name__ == "__main__":
    main()
