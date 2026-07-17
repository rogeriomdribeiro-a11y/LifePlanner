from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)

from app.path import ICONS_DIR


def hex_to_rgba(hex_color, opacity=0.16):
    hex_color = hex_color.replace("#", "")

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return f"rgba({r}, {g}, {b}, {opacity})"


class LPNoteCard(QFrame):
    """Apresentar o conteúdo e as ações de uma nota."""
    def __init__(
        self,
        note,
        on_edit=None,
        on_delete=None,
        on_toggle_pin=None,
    ):
        super().__init__()

        self.note = note
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.on_toggle_pin = on_toggle_pin

        note_color = note["color"] or "#8B5CF6"
        is_pinned = bool(note["is_pinned"])

        self.setObjectName("noteCard")
        self.setMinimumHeight(210)
        self.setMinimumWidth(280)

        self.setStyleSheet(f"""
            QFrame#noteCard {{
                background-color: {hex_to_rgba(note_color, 0.10)};
                border: 1px solid {hex_to_rgba(note_color, 0.42)};
                border-radius: 16px;
            }}

            QFrame#noteCard:hover {{
                background-color: {hex_to_rgba(note_color, 0.14)};
                border: 1px solid {hex_to_rgba(note_color, 0.70)};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        # Header
        header = QHBoxLayout()
        header.setSpacing(8)

        title = QLabel(note["title"])
        title.setObjectName("noteCardTitle")
        title.setWordWrap(True)

        header.addWidget(title)
        header.addStretch()

        if is_pinned:
            pin_badge = QLabel()
            pin_badge.setObjectName("noteCardPinBadge")
            pin_badge.setPixmap(
                QIcon(str(ICONS_DIR / "actions" / "pin.svg")).pixmap(
                    QSize(18, 18)
                )
            )

            header.addWidget(pin_badge)

        # Content
        content_text = note["content"] or "Sem conteúdo."

        if len(content_text) > 150:
            content_text = content_text[:147] + "..."

        content = QLabel(content_text)
        content.setObjectName("noteCardContent")
        content.setWordWrap(True)

        # Category
        category = QLabel(note["category"] or "Geral")
        category.setObjectName("noteCardCategory")
        category.setStyleSheet(f"""
            QLabel#noteCardCategory {{
                background-color: {hex_to_rgba(note_color, 0.18)};
                color: {note_color};
                border-radius: 8px;
                padding: 4px 10px;
                font-size: 11px;
                font-weight: 700;
            }}
        """)

        # Footer buttons
        footer = QHBoxLayout()
        footer.setSpacing(8)

        pin_button = QPushButton()
        pin_button.setObjectName("noteUnpinButton" if is_pinned else "notePinButton")
        pin_button.setCursor(Qt.PointingHandCursor)
        pin_button.setFixedSize(34, 34)

        pin_icon = "unpin.svg" if is_pinned else "pin.svg"
        pin_button.setIcon(QIcon(str(ICONS_DIR / "actions" / pin_icon)))
        pin_button.setIconSize(QSize(18, 18))
        pin_button.clicked.connect(self.handle_toggle_pin)

        edit_button = QPushButton()
        edit_button.setObjectName("noteIconButton")
        edit_button.setCursor(Qt.PointingHandCursor)
        edit_button.setFixedSize(34, 34)
        edit_button.setIcon(QIcon(str(ICONS_DIR / "actions" / "edit.svg")))
        edit_button.setIconSize(QSize(18, 18))
        edit_button.clicked.connect(self.handle_edit)

        delete_button = QPushButton()
        delete_button.setObjectName("noteIconDangerButton")
        delete_button.setCursor(Qt.PointingHandCursor)
        delete_button.setFixedSize(34, 34)
        delete_button.setIcon(QIcon(str(ICONS_DIR / "actions" / "trash.svg")))
        delete_button.setIconSize(QSize(18, 18))
        delete_button.clicked.connect(self.handle_delete)

        footer.addWidget(category)
        footer.addStretch()
        footer.addWidget(pin_button)
        footer.addWidget(edit_button)
        footer.addWidget(delete_button)

        layout.addLayout(header)
        layout.addWidget(content)
        layout.addStretch()
        layout.addLayout(footer)

    def handle_edit(self):
        if self.on_edit:
            self.on_edit(self.note)

    def handle_delete(self):
        if self.on_delete:
            self.on_delete(self.note)

    def handle_toggle_pin(self):
        if self.on_toggle_pin:
            self.on_toggle_pin(self.note)