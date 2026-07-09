from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel


def hex_to_rgba(hex_color, opacity=0.16):
    hex_color = hex_color.replace("#", "")

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return f"rgba({r}, {g}, {b}, {opacity})"


class LPCategoryBadge(QLabel):
    COLORS = {
        "Pessoal": "#3B82F6",
        "Trabalho": "#10B981",
        "Saúde": "#8B5CF6",
        "Estudo": "#F59E0B",
    }

    def __init__(self, category="Pessoal", color=None):
        super().__init__()

        self.setObjectName("categoryBadge")
        self.setFixedWidth(86)
        self.setFixedHeight(24)
        self.setAlignment(Qt.AlignCenter)

        self.set_category(category, color)

    def set_category(self, category, color=None):
        category = category or "Pessoal"
        color = color or self.COLORS.get(category, "#3B82F6")

        self.setText(category)

        self.setStyleSheet(f"""
            QLabel#categoryBadge {{
                background-color: {hex_to_rgba(color, 0.16)};
                color: {color};
                border-radius: 8px;
                font-size: 11px;
                font-weight: 600;
            }}
        """)