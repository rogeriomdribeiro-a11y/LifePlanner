from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QScrollArea,
    QDialog,
)

from app.session import Session
from database.note_repository import NoteRepository
from ui.dialogs.custom_dialog import CustomDialog
from ui.dialogs.note_form_dialog import NoteFormDialog
from ui.widgets.note_card import LPNoteCard


class NotesPage(QWidget):
    """Apresentar, criar e organizar as notas do utilizador."""
    def __init__(self):
        super().__init__()

        self.note_repository = NoteRepository()

        self.setObjectName("notesPage")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("notesScrollArea")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.content = QWidget()
        self.content.setObjectName("notesContent")

        self.layout = QVBoxLayout(self.content)
        self.layout.setContentsMargins(40, 32, 40, 40)
        self.layout.setSpacing(18)

        self.scroll_area.setWidget(self.content)
        main_layout.addWidget(self.scroll_area)

        self.create_header()
        self.create_notes_area()

    def create_header(self):
        header = QHBoxLayout()
        header.setSpacing(16)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)

        title = QLabel("Notas")
        title.setObjectName("notesPageTitle")

        subtitle = QLabel("Guarda ideias, lembretes e informação importante.")
        subtitle.setObjectName("notesPageSubtitle")

        text_layout.addWidget(title)
        text_layout.addWidget(subtitle)

        new_note_button = QPushButton("+ Nova nota")
        new_note_button.setObjectName("notePrimaryButton")
        new_note_button.setCursor(Qt.PointingHandCursor)
        new_note_button.setFixedHeight(42)
        new_note_button.clicked.connect(self.open_note_form)

        header.addLayout(text_layout)
        header.addStretch()
        header.addWidget(new_note_button)

        self.layout.addLayout(header)

    def create_notes_area(self):
        self.notes_card = QFrame()
        self.notes_card.setObjectName("notesListCard")

        card_layout = QVBoxLayout(self.notes_card)
        card_layout.setContentsMargins(22, 20, 22, 22)
        card_layout.setSpacing(16)

        header = QHBoxLayout()

        title = QLabel("As minhas notas")
        title.setObjectName("notesListTitle")

        self.total_label = QLabel()
        self.total_label.setObjectName("notesListCounter")

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.total_label)

        self.notes_grid = QGridLayout()
        self.notes_grid.setSpacing(16)

        card_layout.addLayout(header)
        card_layout.addLayout(self.notes_grid)

        self.layout.addWidget(self.notes_card)
        self.layout.addStretch()

    def open_note_form(self, note=None):
        """Abrir o formulário e guardar uma nota nova ou editada."""
        user = Session.current_user

        if not user:
            return

        dialog = NoteFormDialog(self, note)

        if dialog.exec() != QDialog.Accepted:
            return

        data = dialog.get_data()

        if note:
            self.note_repository.update_note(
                note_id=note["id"],
                user_id=user["id"],
                title=data["title"],
                content=data["content"],
                category=data["category"],
                color=data["color"],
                is_pinned=data["is_pinned"],
            )
        else:
            self.note_repository.create_note(
                user_id=user["id"],
                title=data["title"],
                content=data["content"],
                category=data["category"],
                color=data["color"],
                is_pinned=data["is_pinned"],
            )

        self.refresh()

    def refresh(self):
        """Atualizar a interface com os dados do utilizador autenticado."""
        user = Session.current_user

        self.clear_layout(self.notes_grid)

        if not user:
            self.total_label.setText("0 notas")
            return

        notes = self.note_repository.get_notes_by_user(user["id"])

        total = len(notes)
        self.total_label.setText(
            f"{total} nota" if total == 1 else f"{total} notas"
        )

        if not notes:
            empty_label = QLabel("Ainda não tens notas criadas.")
            empty_label.setObjectName("emptyStateLabel")
            self.notes_grid.addWidget(empty_label, 0, 0)
            return

        columns = 3

        for index, note in enumerate(notes):
            row = index // columns
            column = index % columns

            card = LPNoteCard(
                note,
                on_edit=self.open_note_form,
                on_delete=self.delete_note,
                on_toggle_pin=self.toggle_pin,
            )

            self.notes_grid.addWidget(card, row, column)

        for column in range(columns):
            self.notes_grid.setColumnStretch(column, 1)

    def toggle_pin(self, note):
        """Fixar ou desafixar a nota selecionada."""
        user = Session.current_user

        if not user:
            return

        self.note_repository.toggle_note_pin(
            note_id=note["id"],
            user_id=user["id"],
            is_pinned=not bool(note["is_pinned"]),
        )

        self.refresh()

    def delete_note(self, note):
        """Confirmar e eliminar a nota selecionada."""
        user = Session.current_user

        if not user:
            return

        confirmed = CustomDialog.confirm(
            self,
            f'Tens a certeza que queres eliminar a nota "{note["title"]}"?',
            "Eliminar nota",
            "Eliminar",
            "Cancelar",
            "warning",
            True,
        )

        if not confirmed:
            return

        self.note_repository.delete_note(
            note_id=note["id"],
            user_id=user["id"],
        )

        self.refresh()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()