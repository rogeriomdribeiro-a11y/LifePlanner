def get_theme():
    return """
    QWidget {
        font-family: Segoe UI;
        font-size: 14px;
        color: #F8FAFC;
    }

    QWidget#loginWindow {
        background-color: #0F172A;
    }

    QFrame#loginPanel {
        background-color: #1E293B;
        border-radius: 16px;
        
    }

    QLabel#loginWelcome {
        font-size: 34px;
        font-weight: 700;
        color: #F8FAFC;
        
    }

    QLabel#loginDescription {
        font-size: 23px;
        color: #CBD5E1;
        line-height: 150%;
    }

    QLabel#loginTitle {
        font-size: 32px;
        font-weight: 700;
        color: #F8FAFC;
    }

    QLabel#loginSubtitle {
        font-size: 13px;
        color: #CBD5E1;
    }

    QLabel#separator {
        color: #020617;
        font-size: 13px;
    }

    QLabel#recoverPassword {
        font-size: 11px;
        color: #CBD5E1;
        text-decoration: underline;
    }

    QLineEdit {
        background-color: #020617;
        border: none;
        border-radius: 9px;
        padding: 8px 12px;
        color: #F8FAFC;
    }

    QLineEdit::placeholder {
        color: #64748B;
    }

    QPushButton#googleButton {
        background-color: transparent;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        padding: 9px 14px;
        color: #F8FAFC;
        font-weight: 500;
    }

    QPushButton#googleButton:hover {
        background-color: rgba(255, 255, 255, 0.08);
    }

    QPushButton#lpButton {
    background-color: transparent;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    color: #F8FAFC;
    font-size: 15px;
    font-weight: 600;
    }

    QPushButton#lpButton:hover {
    background-color: rgba(255,255,255,0.08);
    }
    QFrame#titleBar {
    background-color: #0F172A;
    }


    QPushButton#windowButton,
    QPushButton#closeButton {
    background-color: transparent;
    border: none;
    border-radius: 6px;
    }

    QPushButton#windowButton:hover {
    background-color: rgba(255,255,255,0.08);
    }

    QPushButton#closeButton:hover {
    background-color: #EF4444;
    }

    QLabel#separatorLabel {
    color: #64748B;
    font-size: 12px;
    font-weight: 500;
    }
    QFrame {
    color:#8C9CB6;
    }   
    QPushButton#textLinkButton {
    background-color: transparent;
    border: none;
    color: #60A5FA;
    font-size: 12px;
    text-decoration: underline;
}

    QPushButton#textLinkButton:hover {
    color: #93C5FD;
    }


    QDialog#customDialog {
        background-color: #1E293B;
        border-radius: 16px;
    }

    QLabel#dialogTitle {
        color: #F8FAFC;
        font-size: 20px;
        font-weight: 700;
    }

    QLabel#dialogMessage {
        color: #CBD5E1;
        font-size: 14px;
    }

    QPushButton#dialogButton {
        background-color: #3B82F6;
        border: none;
        border-radius: 8px;
        color: #FFFFFF;
        font-weight: 600;
        padding: 8px 20px;
    }

    QPushButton#dialogButton:hover {
        background-color: #2563EB;
    }

    /* ============================================
    CUSTOM DIALOG
    ============================================ */

    QFrame#dialogContainer {
    background-color: #263145;
    border: 1px solid #334155;
    border-radius: 16px;
    }

    QLabel#dialogTitle {
        color: #F8FAFC;
        font-size: 20px;
        font-weight: 700;
    }

    QLabel#dialogMessage {
        color: #CBD5E1;
        font-size: 14px;
    }

    QPushButton#dialogButton {
        background-color: #3B82F6;
        border: none;
        border-radius: 8px;
        color: white;
        font-size: 14px;
        font-weight: 600;
    }

    QPushButton#dialogButton:hover {
        background-color: #2563EB;
    }

    QPushButton#dialogButton:pressed {
        background-color: #1D4ED8;
    }

     /* ============================================
    DASHBOARD
    ============================================ */

    QWidget#dashboardPage {
    background-color: #0F172A;
    }

    QLabel#dashboardTitle {
        color: #F8FAFC;
        font-size: 32px;
        font-weight: 700;
    }

    QLabel#dashboardSubtitle {
        color: #CBD5E1;
        font-size: 16px;
    }



 /* ============================================
    APP LAYOUT
    ============================================ */
    QWidget#appLayout {
    background-color: #0F172A;
    }

    QPushButton#sidebarButton {
    background-color: transparent;
    border: none;
    border-radius: 10px;
    color: #CBD5E1;
    font-size: 15px;
    font-weight: 500;
    text-align: left;
    padding: 12px 16px;
    }

    QPushButton#sidebarButton:hover {
        background-color: #1E293B;
        color: white;
    }

    QPushButton#sidebarButton:checked {
        background-color: #2563EB;
        color: white;
    }

    QFrame#topbar {
        background-color: #0F172A;
        border-bottom: 1px solid #1E293B;
    }

    QLabel#topbarTitle {
        color: #F8FAFC;
        font-size: 26px;
        font-weight: 700;
    }

    QLineEdit#searchInput {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
        color: #F8FAFC;
        padding: 10px;
    }

    QPushButton#topbarIconButton {
        background-color: #1E293B;
        border: none;
        border-radius: 8px;
        color: #F8FAFC;
        min-width: 42px;
        min-height: 42px;
    }

    QWidget#contentArea {
        background-color: #0F172A;
    }

    QLabel#pagePlaceholder {
        color: #94A3B8;
        font-size: 20px;
        padding: 40px;
    }

    
    QFrame#infoCard {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 16px;
    }

    QFrame#infoCard:hover {
        border: 1px solid #475569;
    }

    QLabel#infoCardTitle {
        color: #CBD5E1;
        font-size: 14px;
        font-weight: 600;
    }

    QLabel#infoCardValue {
        color: white;
        font-size: 34px;
        font-weight: 700;
    }

    QLabel#infoCardSubtitle {
        color: #94A3B8;
        font-size: 13px;
    }

    /* ============================================
   SECTIONS
    ============================================ */

    QFrame#sectionCard {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 16px;
    }

    QFrame#sectionCard:hover {
        border: 1px solid #475569;
    }

    QLabel#sectionTitle {
        color: #F8FAFC;
        font-size: 17px;
        font-weight: 700;
    }

    QPushButton#sectionAction {
        background-color: transparent;
        border: none;
        color: #60A5FA;
        font-size: 13px;
        font-weight: 600;
    }

    QPushButton#sectionAction:hover {
        color: #93C5FD;
    }

    QLabel#sectionItem {
        color: #CBD5E1;
        font-size: 14px;
        padding: 6px 0;
    }/* ============================================
   DASHBOARD
    ============================================ */

    QFrame#dashboardWelcomeCard {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 18px;
    }

    QLabel#dashboardWelcomeTitle {
        color: #F8FAFC;
        font-size: 24px;
        font-weight: 700;
    }

    QLabel#dashboardWelcomeSubtitle {
        color: #94A3B8;
        font-size: 14px;
    }

    QLabel#dashboardWelcomeSummary {
        color: #CBD5E1;
        font-size: 15px;
        font-weight: 500;
        margin-top: 8px;
    }

    QLabel#dashboardDateLabel {
        color: #94A3B8;
        font-size: 14px;
        font-weight: 600;
    }

    QProgressBar#goalProgressBar {
        background-color: #334155;
        border: none;
        border-radius: 8px;
        height: 18px;
        color: #F8FAFC;
        font-size: 12px;
        font-weight: 600;
        text-align: center;
    }

    QProgressBar#goalProgressBar::chunk {
        background-color: #10B981;
        border-radius: 8px;
    }

    QWidget#dashboardPage {
    background-color: #0F172A;
    }

    QScrollArea#dashboardScrollArea {
        background-color: #0F172A;
        border: none;
    }

    QWidget#dashboardContent {
        background-color: #0F172A;
    }

    QScrollBar:vertical {
        background-color: #0F172A;
        width: 10px;
        margin: 0;
    }

    QScrollBar::handle:vertical {
        background-color: #334155;
        border-radius: 5px;
        min-height: 30px;
    }

    QScrollBar::handle:vertical:hover {
        background-color: #475569;
    }

    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {
        height: 0;
    }

    /* ============================================
   TASK ITEMS
    ============================================ */

    QFrame#taskItem {
        background-color: transparent;
        border-bottom: 1px solid #334155;
    }

    QLabel#taskCheckbox {
        color: #94A3B8;
        font-size: 20px;
        font-weight: 600;
    }

    QLabel#taskTitle {
        color: #F8FAFC;
        font-size: 14px;
        font-weight: 500;
    }

    QLabel#taskCategory {
    border-radius: 8px;
    font-size: 11px;
    font-weight: 600;
    }

    QLabel#taskTime {
        color: #CBD5E1;
        font-size: 13px;
        min-width: 48px;
    }

    /* ============================================
    EVENT ITEMS
    ============================================ */

    QFrame#eventItem {
        background-color: transparent;
        border-bottom: 1px solid #334155;
    }

    QLabel#eventTime {
        color: #60A5FA;
        font-size: 14px;
        font-weight: 700;
    }

    QLabel#eventTitle {
        color: #F8FAFC;
        font-size: 14px;
        font-weight: 600;
    }

    QLabel#eventSubtitle {
        color: #94A3B8;
        font-size: 12px;
    }

    /* ============================================
    GOAL PROGRESS
    ============================================ */

    QFrame#goalProgressWidget {
        background-color: transparent;
        border: none;
    }

    QLabel#goalProgressTitle {
        color: #F8FAFC;
        font-size: 18px;
        font-weight: 700;
    }

    QLabel#goalProgressSubtitle {
        color: #CBD5E1;
        font-size: 13px;
    }

    QLabel#goalProgressPercent {
        color: #10B981;
        font-size: 28px;
        font-weight: 800;
    }

    QLabel#goalProgressInfo {
        color: #94A3B8;
        font-size: 13px;
    }

    QProgressBar#goalProgressBar {
        background-color: #334155;
        border: none;
        border-radius: 8px;
        height: 16px;
    }

    QProgressBar#goalProgressBar::chunk {
        background-color: #10B981;
        border-radius: 8px;
    }


    /* ============================================
    TASKS PAGE
    ============================================ */

    QWidget#tasksPage {
        background-color: #0F172A;
    }

    QScrollArea#tasksScrollArea {
        background-color: #0F172A;
        border: none;
    }

    QWidget#tasksContent {
        background-color: #0F172A;
    }

    QFrame#taskFormCard,
    QFrame#taskListCard {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 16px;
    }

    QLabel#taskFormTitle,
    QLabel#taskListTitle {
        color: #F8FAFC;
        font-size: 18px;
        font-weight: 700;
    }
    /* ============================================
    TASKS PAGE - HEADER
    ============================================ */

    QWidget#tasksContent QLabel#contentPageTitle {
        color: #F8FAFC;
        font-size: 32px;
        font-weight: 800;
    }

    QWidget#tasksContent QLabel#contentPageSubtitle {
        color: #94A3B8;
        font-size: 15px;
        font-weight: 500;
    }
    /* ============================================
    TASK FORM INPUTS
    ============================================ */

    QLineEdit#taskInput,
    QComboBox#taskCombo,
    QDateEdit#taskDate,
    QTimeEdit#taskTimeEdit {
        background-color: #0F172A;
        border: 1px solid #334155;
        border-radius: 10px;
        color: #F8FAFC;
        padding: 10px 12px;
        font-size: 14px;
        min-height: 22px;
    }

    QLineEdit#taskInput:focus,
    QComboBox#taskCombo:focus,
    QDateEdit#taskDate:focus,
    QTimeEdit#taskTimeEdit:focus {
        border: 1px solid #3B82F6;
    }

    QComboBox#taskCombo::drop-down,
    QDateEdit#taskDate::drop-down {
        border: none;
        background-color: transparent;
        width: 28px;
        border-top-right-radius: 10px;
        border-bottom-right-radius: 10px;
    }

    QComboBox#taskCombo::down-arrow,
    QDateEdit#taskDate::down-arrow {
        image: none;
        width: 0;
        height: 0;
    }

    QTimeEdit#taskTimeEdit::up-button,
    QTimeEdit#taskTimeEdit::down-button {
        width: 0;
        height: 0;
        border: none;
        background-color: transparent;
    }

    QTimeEdit#taskTimeEdit::up-arrow,
    QTimeEdit#taskTimeEdit::down-arrow {
        image: none;
        width: 0;
        height: 0;
    }


    /* ============================================
    TASK ACTION ICON BUTTONS
    ============================================ */

    QPushButton#taskIconButton {
        background-color: rgba(148, 163, 184, 0.10);
        border: none;
        border-radius: 8px;
    }

    QPushButton#taskIconButton:hover {
        background-color: rgba(148, 163, 184, 0.20);
    }

    QPushButton#taskIconDangerButton {
        background-color: rgba(239, 68, 68, 0.12);
        border: none;
        border-radius: 8px;
    }

    QPushButton#taskIconDangerButton:hover {
        background-color: rgba(239, 68, 68, 0.22);
    }
    QLineEdit#taskInput,
    QComboBox#taskCombo,
    QDateEdit#taskDate,
    QTimeEdit#taskTimeEdit {
        background-color: #0F172A;
        border: 1px solid #334155;
        border-radius: 10px;
        color: #F8FAFC;
        padding: 10px;
        font-size: 14px;
        min-height: 22px;
    }

    QLineEdit#taskInput:focus,
    QComboBox#taskCombo:focus,
    QDateEdit#taskDate:focus,
    QTimeEdit#taskTimeEdit:focus {
        border: 1px solid #3B82F6;
    }

    QPushButton#taskAddButton {
        background-color: #2563EB;
        border: none;
        border-radius: 10px;
        color: white;
        padding: 10px 18px;
        font-size: 14px;
        font-weight: 700;
    }

    QPushButton#taskAddButton:hover {
        background-color: #1D4ED8;
    }

    QLabel#taskListCounter {
        color: #94A3B8;
        font-size: 13px;
        font-weight: 600;
    }

    QFrame#taskRow {
        background-color: transparent;
        border-bottom: 1px solid #334155;
    }

    QPushButton#taskStatusButton {
        background-color: transparent;
        border: none;
        color: #60A5FA;
        font-size: 20px;
        font-weight: 700;
        min-width: 32px;
    }

    QLabel#taskRowTitle {
        color: #F8FAFC;
        font-size: 14px;
        font-weight: 500;
    }

    QLabel#taskRowTitleCompleted {
        color: #64748B;
        font-size: 14px;
        font-weight: 500;
        text-decoration: line-through;
    }

    QLabel#taskRowCategory {
        background-color: rgba(59, 130, 246, 0.15);
        color: #60A5FA;
        border-radius: 8px;
        padding: 4px 10px;
        font-size: 12px;
        font-weight: 600;
    }

    QLabel#taskRowDate {
        color: #CBD5E1;
        font-size: 13px;
        min-width: 130px;
    }

    QPushButton#taskDeleteButton {
        background-color: rgba(239, 68, 68, 0.12);
        border: none;
        border-radius: 8px;
        color: #F87171;
        padding: 6px 10px;
        font-size: 12px;
        font-weight: 700;
    }

    QPushButton#taskDeleteButton:hover {
        background-color: rgba(239, 68, 68, 0.22);
    }

    QLabel#emptyStateLabel {
        color: #94A3B8;
        font-size: 14px;
        padding: 20px 0;
    }

    QPushButton#dialogCancelButton {
    background-color: #334155;
    border: none;
    border-radius: 10px;
    color: #CBD5E1;
    font-size: 13px;
    font-weight: 700;
    }

    QPushButton#dialogCancelButton:hover {
        background-color: #475569;
        color: #F8FAFC;
    }

    QPushButton#dialogDangerButton {
        background-color: #DC2626;
        border: none;
        border-radius: 10px;
        color: white;
        font-size: 13px;
        font-weight: 700;
    }

    QPushButton#dialogDangerButton:hover {
        background-color: #B91C1C;
    }

    QLabel#taskGroupTitle {
    color: #CBD5E1;
    font-size: 15px;
    font-weight: 700;
    margin-top: 8px;
    }

    QLabel#taskGroupCounter {
        background-color: #334155;
        color: #CBD5E1;
        border-radius: 8px;
        padding: 4px 10px;
        font-size: 12px;
        font-weight: 700;
    }
   QPushButton#taskStatusButtonCompleted {
    background-color: transparent;
    border: none;
    color: #10B981;
    font-size: 20px;
    font-weight: 700;
    min-width: 32px;
    }

    QPushButton#taskStatusButtonCompleted:hover {
        color: #34D399;
    }
    QPushButton#taskToggleFormButton {
    background-color: #2563EB;
    border: none;
    border-radius: 10px;
    color: white;
    padding: 10px 18px;
    font-size: 14px;
    font-weight: 700;
    }

    QPushButton#taskToggleFormButton:hover {
        background-color: #1D4ED8;
    }
    """