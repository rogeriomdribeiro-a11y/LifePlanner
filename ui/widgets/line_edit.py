from PySide6.QtWidgets import QLineEdit


class LPLineEdit(QLineEdit):
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)

        self.setPlaceholderText(placeholder)
        self.setFixedHeight(40)


class LPPasswordEdit(LPLineEdit):
    def __init__(self, placeholder="Password", parent=None):
        super().__init__(placeholder, parent)

        self.setEchoMode(QLineEdit.Password)