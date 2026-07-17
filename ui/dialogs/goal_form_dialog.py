from PySide6.QtCore import Qt, QSize, QDate
from PySide6.QtGui import QColor, QPixmap, QPainter, QIcon
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QDateEdit,
    QCheckBox,
    QPushButton,
    QGraphicsDropShadowEffect,
    QScrollArea,
    QWidget,
)



class GoalStepEditor(QFrame):
    """Editar uma etapa individual dentro do formulário de objetivos."""
    def __init__(self, number, step=None, on_remove=None):
        super().__init__()

        self.on_remove = on_remove
        self.is_completed = bool(step["is_completed"]) if step else False

        self.setObjectName("goalStepEditor")
        self.setMinimumHeight(165)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(10)

        header = QHBoxLayout()
        header.setSpacing(10)

        self.number_label = QLabel(f"Etapa {number}")
        self.number_label.setObjectName("goalStepEditorTitle")

        remove_button = QPushButton("Remover")
        remove_button.setObjectName("goalStepRemoveButton")
        remove_button.setCursor(Qt.PointingHandCursor)
        remove_button.setFixedSize(86, 30)
        remove_button.clicked.connect(self.handle_remove)

        header.addWidget(self.number_label)
        header.addStretch()
        header.addWidget(remove_button)

        self.title_input = QLineEdit()
        self.title_input.setObjectName("goalDialogInput")
        self.title_input.setPlaceholderText("Título da etapa")
        self.title_input.setFixedHeight(38)

        self.description_input = QTextEdit()
        self.description_input.setObjectName("goalDialogSmallTextEdit")
        self.description_input.setPlaceholderText("Descrição da etapa...")
        self.description_input.setFixedHeight(76)

        layout.addLayout(header)
        layout.addWidget(self.title_input)
        layout.addWidget(self.description_input)

        if step:
            self.title_input.setText(step["title"] or "")
            self.description_input.setPlainText(step["description"] or "")

    def set_number(self, number):
        self.number_label.setText(f"Etapa {number}")

    def handle_remove(self):
        if self.on_remove:
            self.on_remove(self)

    def get_data(self):
        """Devolver os dados normalizados introduzidos no formulário."""
        return {
            "title": self.title_input.text().strip(),
            "description": self.description_input.toPlainText().strip(),
            "is_completed": self.is_completed,
        }


class GoalFormDialog(QDialog):
    """Recolher e validar um objetivo e as respetivas etapas."""
    COLORS = {
        "Verde": "#10B981",
        "Azul": "#3B82F6",
        "Roxo": "#8B5CF6",
        "Laranja": "#F59E0B",
        "Vermelho": "#EF4444",
    }

    CATEGORIES = [
        "Pessoal",
        "Trabalho",
        "Estudo",
        "Saúde",
        "Financeiro",
        "Projeto",
    ]

    def __init__(self, parent=None, goal=None, steps=None):
        super().__init__(parent)

        self.goal_data = goal
        self.steps_data = steps or []
        self.step_editors = []

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)
        self.setFixedSize(760, 720)

        wrapper_layout = QVBoxLayout(self)
        wrapper_layout.setContentsMargins(12, 12, 12, 12)

        container = QFrame()
        container.setObjectName("goalDialogContainer")

        shadow = QGraphicsDropShadowEffect(container)
        shadow.setBlurRadius(35)
        shadow.setOffset(0, 5)
        shadow.setColor(QColor(0, 0, 0, 150))
        container.setGraphicsEffect(shadow)

        wrapper_layout.addWidget(container)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(28, 24, 28, 22)
        layout.setSpacing(12)

        title_text = "Editar objetivo" if goal else "Novo objetivo"

        title = QLabel(title_text)
        title.setObjectName("goalDialogTitle")

        subtitle = QLabel(
            "Divide o objetivo em etapas e acompanha o progresso automaticamente."
        )
        subtitle.setObjectName("goalDialogSubtitle")
        subtitle.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.form_scroll_area = QScrollArea()
        self.form_scroll_area.setObjectName("goalFormScrollArea")
        self.form_scroll_area.setWidgetResizable(True)
        self.form_scroll_area.setFrameShape(QFrame.NoFrame)
        self.form_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        form_content = QWidget()
        form_content.setObjectName("goalFormScrollContent")

        self.form_layout = QVBoxLayout(form_content)
        self.form_layout.setContentsMargins(0, 0, 0, 0)
        self.form_layout.setSpacing(14)

        self.title_input = QLineEdit()
        self.title_input.setObjectName("goalDialogInput")
        self.title_input.setPlaceholderText("Ex: Concluir o projeto LifePlanner")
        self.title_input.setFixedHeight(40)

        self.description_input = QTextEdit()
        self.description_input.setObjectName("goalDialogTextEdit")
        self.description_input.setPlaceholderText("Descreve o objetivo principal...")
        self.description_input.setFixedHeight(100)

        self.category_input = QComboBox()
        self.category_input.setObjectName("goalDialogCombo")
        self.category_input.addItems(self.CATEGORIES)
        self.category_input.setFixedHeight(40)

        self.color_input = QComboBox()
        self.color_input.setObjectName("goalDialogCombo")
        self.color_input.setIconSize(QSize(14, 14))
        self.color_input.setFixedHeight(40)

        for color_name, color_value in self.COLORS.items():
            self.color_input.addItem(
                self.create_color_icon(color_value),
                color_name,
            )

        self.date_input = QDateEdit()
        self.date_input.setObjectName("goalDialogDateInput")
        self.date_input.setFixedHeight(40)
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("dd/MM/yyyy")
        self.date_input.setDate(QDate.currentDate())

        self.no_date_checkbox = QCheckBox("Sem data objetivo")
        self.no_date_checkbox.setObjectName("goalDialogCheckbox")
        self.no_date_checkbox.stateChanged.connect(self.toggle_date_input)

        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(12)

        grid.addLayout(self.create_field("Categoria", self.category_input), 0, 0)
        grid.addLayout(self.create_field("Cor", self.color_input), 0, 1)
        grid.addLayout(self.create_field("Data objetivo", self.date_input), 1, 0)
        grid.addWidget(self.no_date_checkbox, 1, 1, alignment=Qt.AlignBottom)

        steps_header = QHBoxLayout()
        steps_header.setSpacing(10)

        steps_title = QLabel("Etapas do objetivo")
        steps_title.setObjectName("goalDialogSectionTitle")

        self.steps_count_label = QLabel("0 etapas")
        self.steps_count_label.setObjectName("goalDialogSectionCount")

        add_step_button = QPushButton("+ Adicionar etapa")
        add_step_button.setObjectName("goalAddStepButton")
        add_step_button.setCursor(Qt.PointingHandCursor)
        add_step_button.setFixedSize(160, 38)
        add_step_button.clicked.connect(self.add_empty_step)

        steps_header.addWidget(steps_title)
        steps_header.addWidget(self.steps_count_label)
        steps_header.addStretch()
        steps_header.addWidget(add_step_button)

        self.steps_container = QWidget()
        self.steps_container.setObjectName("goalStepsContainer")

        self.steps_layout = QVBoxLayout(self.steps_container)
        self.steps_layout.setContentsMargins(0, 0, 0, 0)
        self.steps_layout.setSpacing(12)

        self.form_layout.addLayout(self.create_field("Título", self.title_input))
        self.form_layout.addLayout(
            self.create_field("Descrição", self.description_input)
        )
        self.form_layout.addLayout(grid)
        self.form_layout.addSpacing(4)
        self.form_layout.addLayout(steps_header)
        self.form_layout.addWidget(self.steps_container)
        self.form_layout.addStretch()

        self.form_scroll_area.setWidget(form_content)
        layout.addWidget(self.form_scroll_area)

        self.error_label = QLabel("")
        self.error_label.setObjectName("goalDialogError")
        self.error_label.setFixedHeight(20)

        layout.addWidget(self.error_label)

        buttons = QHBoxLayout()
        buttons.setSpacing(10)
        buttons.addStretch()

        cancel_button = QPushButton("Cancelar")
        cancel_button.setObjectName("goalDialogCancelButton")
        cancel_button.setCursor(Qt.PointingHandCursor)
        cancel_button.setFixedSize(130, 40)
        cancel_button.clicked.connect(self.reject)

        save_text = "Guardar alterações" if goal else "Criar objetivo"

        save_button = QPushButton(save_text)
        save_button.setObjectName("goalDialogPrimaryButton")
        save_button.setCursor(Qt.PointingHandCursor)
        save_button.setFixedSize(180, 40)
        save_button.clicked.connect(self.validate_and_accept)

        buttons.addWidget(cancel_button)
        buttons.addWidget(save_button)

        layout.addLayout(buttons)

        self.load_data()

    def create_field(self, label_text, widget):
        field_layout = QVBoxLayout()
        field_layout.setSpacing(6)

        label = QLabel(label_text)
        label.setObjectName("goalDialogFieldLabel")

        field_layout.addWidget(label)
        field_layout.addWidget(widget)

        return field_layout

    def create_color_icon(self, color_value):
        pixmap = QPixmap(14, 14)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(color_value))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(1, 1, 12, 12)
        painter.end()

        return QIcon(pixmap)

    def load_data(self):
        if not self.goal_data:
            self.category_input.setCurrentText("Pessoal")
            self.color_input.setCurrentText("Verde")
            self.no_date_checkbox.setChecked(False)

            self.add_empty_step()
            self.add_empty_step()
            self.add_empty_step()
            return

        self.title_input.setText(self.goal_data["title"] or "")
        self.description_input.setPlainText(self.goal_data["description"] or "")
        self.category_input.setCurrentText(self.goal_data["category"] or "Pessoal")

        color_name = self.get_color_name(self.goal_data["color"] or "#10B981")
        self.color_input.setCurrentText(color_name)

        target_date = self.goal_data["target_date"]

        if target_date:
            year, month, day = map(int, target_date.split("-"))
            self.date_input.setDate(QDate(year, month, day))
            self.no_date_checkbox.setChecked(False)
        else:
            self.no_date_checkbox.setChecked(True)

        self.toggle_date_input()

        if self.steps_data:
            for step in self.steps_data:
                self.add_step_editor(step)
        else:
            self.add_empty_step()

    def add_empty_step(self):
        self.add_step_editor()

    def add_step_editor(self, step=None):
        editor = GoalStepEditor(
            len(self.step_editors) + 1,
            step=step,
            on_remove=self.remove_step_editor,
        )

        self.step_editors.append(editor)
        self.steps_layout.addWidget(editor)
        self.update_steps_count()

        self.form_scroll_area.ensureWidgetVisible(editor)

    def remove_step_editor(self, editor):
        if len(self.step_editors) == 1:
            self.error_label.setText("O objetivo precisa de pelo menos uma etapa.")
            return

        self.step_editors.remove(editor)
        editor.deleteLater()

        self.update_steps_count()

    def update_steps_count(self):
        for index, editor in enumerate(self.step_editors, start=1):
            editor.set_number(index)

        total = len(self.step_editors)

        if total == 1:
            self.steps_count_label.setText("1 etapa")
        else:
            self.steps_count_label.setText(f"{total} etapas")

    def toggle_date_input(self):
        self.date_input.setEnabled(not self.no_date_checkbox.isChecked())

    def validate_and_accept(self):
        """Validar os campos antes de aceitar o formulário."""
        if not self.title_input.text().strip():
            self.error_label.setText("O título do objetivo é obrigatório.")
            return

        steps = []

        for editor in self.step_editors:
            step_data = editor.get_data()

            has_title = bool(step_data["title"])
            has_description = bool(step_data["description"])

            if has_description and not has_title:
                self.error_label.setText(
                    "Todas as etapas com descrição precisam de título."
                )
                return

            if has_title:
                steps.append(step_data)

        if not steps:
            self.error_label.setText("Adiciona pelo menos uma etapa ao objetivo.")
            return

        self.accept()

    def get_color_name(self, color_value):
        for name, value in self.COLORS.items():
            if value.lower() == color_value.lower():
                return name

        return "Verde"

    def get_data(self):
        """Devolver os dados normalizados introduzidos no formulário."""
        color_name = self.color_input.currentText()

        target_date = None

        if not self.no_date_checkbox.isChecked():
            target_date = self.date_input.date().toString("yyyy-MM-dd")

        steps = []

        for editor in self.step_editors:
            step_data = editor.get_data()

            if step_data["title"]:
                steps.append(step_data)

        return {
            "title": self.title_input.text().strip(),
            "description": self.description_input.toPlainText().strip(),
            "category": self.category_input.currentText(),
            "target_date": target_date,
            "status": "Em progresso",
            "color": self.COLORS.get(color_name, "#10B981"),
            "steps": steps,
        }