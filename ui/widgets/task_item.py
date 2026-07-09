from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel

from ui.widgets.priority_badge import LPPriorityBadge


def hex_to_rgba(hex_color, opacity=0.16):
    hex_color = hex_color.replace("#", "")

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return f"rgba({r}, {g}, {b}, {opacity})"


class LPTaskItem(QFrame):
    def __init__(
        self,
        title,
        category="",
        time="",
        category_color="#3B82F6",
        priority="",
    ):
        super().__init__()

        self.setObjectName("taskItem")
        self.setMinimumHeight(40)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 6, 0, 6)
        layout.setSpacing(12)

        checkbox = QLabel("○")
        checkbox.setObjectName("taskCheckbox")
        checkbox.setFixedWidth(18)
        checkbox.setAlignment(Qt.AlignCenter)

        title_label = QLabel(title)
        title_label.setObjectName("taskTitle")
        title_label.setMinimumWidth(240)

        category_label = QLabel(category)
        category_label.setObjectName("taskCategory")
        category_label.setFixedWidth(86)
        category_label.setFixedHeight(24)
        category_label.setAlignment(Qt.AlignCenter)

        category_label.setStyleSheet(f"""
            QLabel#taskCategory {{
                background-color: {hex_to_rgba(category_color, 0.16)};
                color: {category_color};
                border-radius: 8px;
                font-size: 11px;
                font-weight: 600;
            }}
        """)

        priority_label = LPPriorityBadge(priority)

        time_label = QLabel(time)
        time_label.setObjectName("taskTime")
        time_label.setFixedWidth(58)
        time_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout.addWidget(checkbox)
        layout.addWidget(title_label)
        layout.addStretch()

        if category:
            layout.addWidget(category_label)

        if priority:
            layout.addWidget(priority_label)

        if time:
            layout.addWidget(time_label)