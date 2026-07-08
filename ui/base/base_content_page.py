from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class BaseContentPage(QWidget):
    def __init__(self, title, subtitle=""):
        super().__init__()

        self.setObjectName("contentPage")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 40, 40, 40)
        self.layout.setSpacing(12)

        self.title = QLabel(title)
        self.title.setObjectName("contentPageTitle")

        self.layout.addWidget(self.title)

        if subtitle:
            self.subtitle = QLabel(subtitle)
            self.subtitle.setObjectName("contentPageSubtitle")
            self.layout.addWidget(self.subtitle)

        self.layout.addSpacing(20)