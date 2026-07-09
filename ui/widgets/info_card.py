from PySide6.QtCore import Qt
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
)

from app.path import ICONS_DIR


def hex_to_rgba(hex_color, opacity=0.16):
    hex_color = hex_color.replace("#", "")

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return f"rgba({r}, {g}, {b}, {opacity})"


class LPInfoCard(QFrame):
    def __init__(
        self,
        title,
        value,
        subtitle="",
        icon_name=None,
        accent_color="#3B82F6",
    ):
        super().__init__()

        self.setObjectName("infoCard")
        self.setMinimumHeight(165)
        self.setMinimumWidth(260)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 20, 22, 20)
        layout.setSpacing(14)

        # Header
        header = QHBoxLayout()
        header.setSpacing(14)

        if icon_name:
            icon_container = QWidget()
            icon_container.setObjectName("infoCardIcon")
            icon_container.setFixedSize(52, 52)
            icon_container.setStyleSheet(f"""
                QWidget#infoCardIcon {{
                    background-color: {hex_to_rgba(accent_color, 0.16)};
                    border-radius: 14px;
                }}
            """)

            icon_layout = QVBoxLayout(icon_container)
            icon_layout.setContentsMargins(0, 0, 0, 0)

            icon = QSvgWidget(str(ICONS_DIR / "sidebar" / icon_name))
            icon.setFixedSize(28, 28)

            icon_layout.addWidget(icon, alignment=Qt.AlignCenter)

            header.addWidget(icon_container)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        title_label = QLabel(title)
        title_label.setObjectName("infoCardTitle")

        value_label = QLabel(value)
        value_label.setObjectName("infoCardValue")

        subtitle_label = QLabel(subtitle)
        subtitle_label.setObjectName("infoCardSubtitle")

        text_layout.addWidget(title_label)
        text_layout.addWidget(value_label)
        text_layout.addWidget(subtitle_label)

        header.addLayout(text_layout)
        header.addStretch()

        layout.addLayout(header)

        # Accent bar
        accent_bar = QFrame()
        accent_bar.setObjectName("infoCardAccent")
        accent_bar.setFixedHeight(4)
        accent_bar.setStyleSheet(f"""
            QFrame#infoCardAccent {{
                background-color: {accent_color};
                border-radius: 2px;
            }}
        """)

        layout.addStretch()
        layout.addWidget(accent_bar)