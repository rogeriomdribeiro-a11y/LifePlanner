from pathlib import Path

from PySide6.QtGui import QIcon


BASE_DIR = Path(__file__).resolve().parent.parent

ASSETS_DIR = BASE_DIR / "assets"
ICONS_DIR = ASSETS_DIR / "icons"


def get_icon(folder, filename):
    return QIcon(str(ICONS_DIR / folder / filename))