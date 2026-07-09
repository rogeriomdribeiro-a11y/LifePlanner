from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)


class LPSection(QFrame):
    def __init__(self, title, action_text=None):
        super().__init__()

        self.setObjectName("sectionCard")
        self.setMinimumHeight(180)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(14)

        header = QHBoxLayout()

        title_label = QLabel(title)
        title_label.setObjectName("sectionTitle")

        header.addWidget(title_label)
        header.addStretch()

        if action_text:
            action_button = QPushButton(action_text)
            action_button.setObjectName("sectionAction")
            action_button.setCursor(Qt.PointingHandCursor)
            header.addWidget(action_button)

        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(10)

        layout.addLayout(header)
        layout.addLayout(self.content_layout)
        layout.addStretch()

    def add_text_item(self, text):
        item = QLabel(text)
        item.setObjectName("sectionItem")
        self.content_layout.addWidget(item)