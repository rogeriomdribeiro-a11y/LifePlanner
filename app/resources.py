"""Funções auxiliares para carregar recursos gráficos da aplicação."""

from PySide6.QtGui import QIcon

from app.path import ICONS_DIR


def get_icon(folder: str, filename: str) -> QIcon:
    """Devolver um ícone localizado numa subpasta de ``assets/icons``."""
    return QIcon(str(ICONS_DIR / folder / filename))
