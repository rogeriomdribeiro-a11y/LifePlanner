from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel

from ui.widgets.category_badge import LPCategoryBadge
from ui.widgets.priority_badge import LPPriorityBadge


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

        category_label = LPCategoryBadge(category, category_color)

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