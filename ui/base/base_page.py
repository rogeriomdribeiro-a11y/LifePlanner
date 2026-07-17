"""Base partilhada pelos ecrãs de autenticação."""

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QWidget

from app.path import IMAGES_DIR


LOGIN_IMAGES_DIR = IMAGES_DIR / "login"


class BasePage(QWidget):
    """Disponibilizar o carregamento consistente das imagens de autenticação."""

    def image_label(self, filename, width, height):
        """Criar uma etiqueta com uma imagem redimensionada sem deformação."""
        label = QLabel()
        label.setFixedSize(width, height)
        label.setAlignment(Qt.AlignCenter)

        image_path = LOGIN_IMAGES_DIR / filename

        if image_path.exists():
            pixmap = QPixmap(str(image_path)).scaled(
                width,
                height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
            label.setPixmap(pixmap)
        else:
            label.setText(f"Imagem não encontrada:\n{filename}")
            label.setStyleSheet("color: #EF4444;")

        return label
