from PySide6.QtWidgets import QFrame, QHBoxLayout


class Topbar(QFrame):
    def __init__(self):
        super().__init__()

        self.setObjectName("topbar")
        self.setFixedHeight(28)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 140, 0)
        layout.setSpacing(0)

    def refresh_user(self):
        pass