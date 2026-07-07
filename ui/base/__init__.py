from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QLabel


BASE_DIR = Path(__file__).resolve().parents[2]
IMAGES_DIR = BASE_DIR / "assets" / "images" / "login"


class BasePage(QWidget):
    def image_label(self, filename, width, height):
        label = QLabel()
        label.setFixedSize(width, height)
        label.setAlignment(Qt.AlignCenter)

        image_path = IMAGES_DIR / filename

        if image_path.exists():
            pixmap = QPixmap(str(image_path))
            pixmap = pixmap.scaled(
                width,
                height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            label.setPixmap(pixmap)
        else:
            label.setText(f"Imagem não encontrada:\n{filename}")
            label.setStyleSheet("color: #EF4444;")

        return label