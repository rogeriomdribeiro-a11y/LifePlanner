"""Configuração e arranque da aplicação LifePlanner."""

import sys

from PySide6.QtWidgets import QApplication

from database.connection import get_connection
from database.schema import create_tables
from styles.theme import get_theme
from ui.main_window import MainWindow


class LifePlannerApp:
    """Controlador principal responsável pelo ciclo de vida da aplicação."""

    def __init__(self) -> None:
        # Reutiliza uma QApplication existente quando o módulo é carregado em
        # testes; numa execução normal é criada uma nova instância.
        self.qt_app = QApplication.instance() or QApplication(sys.argv)
        self.qt_app.setApplicationName("LifePlanner")
        self.qt_app.setOrganizationName("LifePlanner")
        self.qt_app.setStyleSheet(get_theme())

        self.current_window = None
        self._initialize_database()

    def _initialize_database(self) -> None:
        """Criar a base de dados e aplicar a estrutura necessária.

        A ligação usada no arranque é fechada imediatamente depois da criação
        das tabelas. Cada repositório abre a sua própria ligação quando é criado.
        """
        connection = get_connection()

        try:
            create_tables(connection)
        finally:
            connection.close()

    def show_login(self) -> None:
        """Criar a janela principal e apresentar o ecrã de autenticação."""
        self.close_current_window()

        self.current_window = MainWindow(app_controller=self)
        self.current_window.maximize_custom()
        self.current_window.show()

    def close_current_window(self) -> None:
        """Fechar e libertar a janela atualmente apresentada, caso exista."""
        if self.current_window is not None:
            self.current_window.close()
            self.current_window = None

    def run(self) -> None:
        """Apresentar a janela inicial e iniciar o ciclo de eventos Qt."""
        self.show_login()
        exit_code = self.qt_app.exec()
        raise SystemExit(exit_code)
