from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtSvgWidgets import QSvgWidget

from app.path import ICONS_DIR


class LPInfoCard(QFrame):
    def __init__(self, title, value, subtitle="", icon_name=None):
        super().__init__()

        self.setObjectName("infoCard")
        self.setMinimumHeight(130)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(10)

        header = QHBoxLayout()

        title_label = QLabel(title)
        title_label.setObjectName("infoCardTitle")

        header.addWidget(title_label)
        header.addStretch()

        if icon_name:
            icon = QSvgWidget(str(ICONS_DIR / "sidebar" / icon_name))
            icon.setFixedSize(24, 24)
            header.addWidget(icon)

        value_label = QLabel(value)
        value_label.setObjectName("infoCardValue")

        subtitle_label = QLabel(subtitle)
        subtitle_label.setObjectName("infoCardSubtitle")

        layout.addLayout(header)
        layout.addStretch()
        layout.addWidget(value_label)
        layout.addWidget(subtitle_label)