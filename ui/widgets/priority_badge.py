from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel


def hex_to_rgba(hex_color, opacity=0.16):
    hex_color = hex_color.replace("#", "")

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return f"rgba({r}, {g}, {b}, {opacity})"


class LPPriorityBadge(QLabel):
    """Apresentar a prioridade de uma tarefa com cor própria."""
    COLORS = {
        "Baixa": "#10B981",
        "Normal": "#3B82F6",
        "Alta": "#F59E0B",
        "Urgente": "#EF4444",
    }

    def __init__(self, priority="Normal"):
        super().__init__()

        self.setObjectName("priorityBadge")
        self.setFixedWidth(82)
        self.setFixedHeight(24)
        self.setAlignment(Qt.AlignCenter)

        self.set_priority(priority)

    def set_priority(self, priority):
        priority = priority or "Normal"
        color = self.COLORS.get(priority, "#3B82F6")

        self.setText(priority)

        self.setStyleSheet(f"""
            QLabel#priorityBadge {{
                background-color: {hex_to_rgba(color, 0.16)};
                color: {color};
                border-radius: 8px;
                font-size: 11px;
                font-weight: 700;
            }}
        """)