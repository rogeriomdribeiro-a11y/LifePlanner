from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
)


class LPGoalProgress(QFrame):
    """Apresentar visualmente o progresso de um objetivo."""
    def __init__(
        self,
        title,
        subtitle,
        progress,
        left_info="",
        right_info="",
    ):
        super().__init__()

        self.setObjectName("goalProgressWidget")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 6, 0, 0)
        layout.setSpacing(12)

        header = QHBoxLayout()

        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)

        title_label = QLabel(title)
        title_label.setObjectName("goalProgressTitle")

        subtitle_label = QLabel(subtitle)
        subtitle_label.setObjectName("goalProgressSubtitle")

        text_layout.addWidget(title_label)
        text_layout.addWidget(subtitle_label)

        progress_label = QLabel(f"{progress}%")
        progress_label.setObjectName("goalProgressPercent")

        header.addLayout(text_layout)
        header.addStretch()
        header.addWidget(progress_label)

        progress_bar = QProgressBar()
        progress_bar.setObjectName("goalProgressBar")
        progress_bar.setValue(progress)
        progress_bar.setTextVisible(False)

        footer = QHBoxLayout()

        left_label = QLabel(left_info)
        left_label.setObjectName("goalProgressInfo")

        right_label = QLabel(right_info)
        right_label.setObjectName("goalProgressInfo")

        footer.addWidget(left_label)
        footer.addStretch()
        footer.addWidget(right_label)

        layout.addLayout(header)
        layout.addWidget(progress_bar)
        layout.addLayout(footer)