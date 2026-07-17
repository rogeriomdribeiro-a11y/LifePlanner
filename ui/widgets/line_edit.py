from PySide6.QtWidgets import QLineEdit


class LPLineEdit(QLineEdit):
    """Campo de texto com o estilo padrão da autenticação."""
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)

        self.setPlaceholderText(placeholder)
        self.setFixedHeight(40)


class LPPasswordEdit(LPLineEdit):
    """Campo de password com caracteres ocultos."""
    def __init__(self, placeholder="Password", parent=None):
        super().__init__(placeholder, parent)

        self.setEchoMode(QLineEdit.Password)