from PySide6.QtGui import QIcon, QPixmap

from app.path import ICONS_DIR, IMAGES_DIR


def get_icon(folder: str, filename: str) -> QIcon:
    return QIcon(str(ICONS_DIR / folder / filename))


def get_pixmap(folder: str, filename: str) -> QPixmap:
    return QPixmap(str(IMAGES_DIR / folder / filename))