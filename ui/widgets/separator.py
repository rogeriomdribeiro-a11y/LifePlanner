from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QFrame


class LPSeparator(QWidget):
    """Separar alternativas de autenticação com um texto central."""
    def __init__(self, text="ou"):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        left = QFrame()
        left.setFrameShape(QFrame.HLine)

        right = QFrame()
        right.setFrameShape(QFrame.HLine)

        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setObjectName("separatorLabel")
        
        layout.addWidget(left)
        layout.addWidget(label)
        layout.addWidget(right)