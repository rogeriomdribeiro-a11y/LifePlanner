from PySide6.QtWidgets import QLabel

from ui.base.base_content_page import BaseContentPage


class DashboardPage(BaseContentPage):
    def __init__(self):
        super().__init__(
            "Dashboard",
            "Resumo geral da tua organização pessoal."
        )

        placeholder = QLabel("Dashboard em desenvolvimento")
        placeholder.setObjectName("pagePlaceholder")

        self.layout.addWidget(placeholder)
        self.layout.addStretch()