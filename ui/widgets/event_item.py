from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel


class LPEventItem(QFrame):
    def __init__(self, time, title, subtitle="", accent_color="#3B82F6"):
        super().__init__()

        self.setObjectName("eventItem")
        self.setMinimumHeight(54)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 6, 0, 6)
        layout.setSpacing(14)

        time_label = QLabel(time)
        time_label.setObjectName("eventTime")
        time_label.setFixedWidth(58)
        time_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        dot = QFrame()
        dot.setObjectName("eventDot")
        dot.setFixedSize(9, 9)
        dot.setStyleSheet(f"""
            QFrame#eventDot {{
                background-color: {accent_color};
                border-radius: 4px;
            }}
        """)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        title_label = QLabel(title)
        title_label.setObjectName("eventTitle")

        subtitle_label = QLabel(subtitle)
        subtitle_label.setObjectName("eventSubtitle")

        text_layout.addWidget(title_label)

        if subtitle:
            text_layout.addWidget(subtitle_label)

        layout.addWidget(time_label)
        layout.addWidget(dot)
        layout.addLayout(text_layout)
        layout.addStretch()