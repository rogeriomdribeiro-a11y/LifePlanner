"""
Centralized dark stylesheet for LifePlanner.

Structure:
- get_theme(): public function used by the app.
- DARK_THEME: current production dark theme.

Note:
This file is grouped by application areas/pages.
Avoid adding page-specific styles randomly at the bottom; create or use the correct section.
"""


def _join_styles(*styles):
    return "\n\n".join(style.strip() for style in styles if style and style.strip())


# ============================================
# Global_And_Auth
# ============================================

GLOBAL_AND_AUTH_STYLE = r'''
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
'''

# ============================================
# Custom Dialog
# ============================================

CUSTOM_DIALOG_STYLE = r'''
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
'''

# ============================================
# Dashboard
# ============================================

DASHBOARD_STYLE = r'''
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
'''

# ============================================
# App Layout
# ============================================

APP_LAYOUT_STYLE = r'''
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
        border: none;
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
'''

# ============================================
# Sections
# ============================================

SECTIONS_STYLE = r'''
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
    }
'''

# ============================================
# Dashboard
# ============================================

DASHBOARD_STYLE_2 = r'''
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
'''

# ============================================
# Task Items
# ============================================

TASK_ITEMS_STYLE = r'''
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
'''

# ============================================
# Event Items
# ============================================

EVENT_ITEMS_STYLE = r'''
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
'''

# ============================================
# Goal Progress
# ============================================

GOAL_PROGRESS_STYLE = r'''
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
'''

# ============================================
# Tasks Page
# ============================================

TASKS_PAGE_STYLE = r'''
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
'''

# ============================================
# Tasks Page - Header
# ============================================

TASKS_PAGE_HEADER_STYLE = r'''
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
'''

# ============================================
# Task Form Inputs
# ============================================

TASK_FORM_INPUTS_STYLE = r'''
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
'''

# ============================================
# Task Action Icon Buttons
# ============================================

TASK_ACTION_ICON_BUTTONS_STYLE = r'''
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
'''

# ============================================
# Calendar Page
# ============================================

CALENDAR_PAGE_STYLE = r'''
QWidget#calendarPage {
        background-color: #0F172A;
    }

    QScrollArea#calendarScrollArea {
        background-color: #0F172A;
        border: none;
    }

    QWidget#calendarContent {
        background-color: #0F172A;
    }

    QFrame#eventFormCard,
    QFrame#eventListCard {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 16px;
    }

    QLabel#eventFormTitle,
    QLabel#eventListTitle {
        color: #F8FAFC;
        font-size: 18px;
        font-weight: 700;
    }

    QPushButton#eventToggleFormButton,
    QPushButton#eventAddButton {
        background-color: #2563EB;
        border: none;
        border-radius: 10px;
        color: white;
        padding: 10px 18px;
        font-size: 14px;
        font-weight: 700;
    }

    QPushButton#eventToggleFormButton:hover,
    QPushButton#eventAddButton:hover {
        background-color: #1D4ED8;
    }

    QLineEdit#eventInput,
    QComboBox#eventCombo,
    QDateEdit#eventDate,
    QTimeEdit#eventTimeEdit {
        background-color: #0F172A;
        border: 1px solid #334155;
        border-radius: 10px;
        color: #F8FAFC;
        padding: 10px 12px;
        font-size: 14px;
        min-height: 22px;
    }

    QLineEdit#eventInput:focus,
    QComboBox#eventCombo:focus,
    QDateEdit#eventDate:focus,
    QTimeEdit#eventTimeEdit:focus {
        border: 1px solid #3B82F6;
    }

    QComboBox#eventCombo::drop-down,
    QDateEdit#eventDate::drop-down {
        border: none;
        background-color: transparent;
        width: 28px;
    }

    QComboBox#eventCombo::down-arrow,
    QDateEdit#eventDate::down-arrow {
        image: none;
        width: 0;
        height: 0;
    }

    QTimeEdit#eventTimeEdit::up-button,
    QTimeEdit#eventTimeEdit::down-button,
    QTimeEdit#eventTimeEdit::up-arrow,
    QTimeEdit#eventTimeEdit::down-arrow {
        width: 0;
        height: 0;
        border: none;
        image: none;
        background-color: transparent;
    }

    QLabel#eventListCounter {
        color: #94A3B8;
        font-size: 13px;
        font-weight: 600;
    }

    QFrame#eventRow {
        background-color: transparent;
        border-bottom: 1px solid #334155;
    }

    QLabel#eventRowTitle {
        color: #F8FAFC;
        font-size: 14px;
        font-weight: 600;
    }

    QLabel#eventRowSubtitle {
        color: #94A3B8;
        font-size: 12px;
    }

    QLabel#eventRowDate {
        color: #CBD5E1;
        font-size: 13px;
        min-width: 170px;
    }

    QPushButton#eventIconDangerButton {
        background-color: rgba(239, 68, 68, 0.12);
        border: none;
        border-radius: 8px;
    }

    QPushButton#eventIconDangerButton:hover {
        background-color: rgba(239, 68, 68, 0.22);
    }
'''

# ============================================
# Month Calendar
# ============================================

MONTH_CALENDAR_STYLE = r'''
QFrame#calendarMonthCard {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 16px;
    }

    QPushButton#calendarToolbarButton,
    QPushButton#calendarNavButton,
    QPushButton#calendarViewButton {
        background-color: #273449;
        border: none;
        border-radius: 8px;
        color: #CBD5E1;
        padding: 8px 12px;
        font-size: 13px;
        font-weight: 700;
    }

    QPushButton#calendarToolbarButton:hover,
    QPushButton#calendarNavButton:hover,
    QPushButton#calendarViewButton:hover {
        background-color: #334155;
        color: #F8FAFC;
    }

    QPushButton#calendarNavButton {
        font-size: 22px;
        padding: 4px 12px;
    }

    QLabel#calendarMonthTitle {
        color: #F8FAFC;
        font-size: 26px;
        font-weight: 700;
    }

    QLabel#calendarWeekday {
        color: #CBD5E1;
        font-size: 14px;
        font-weight: 700;
        padding: 8px 0;
    }

    QFrame#calendarDayCell,
    QFrame#calendarDayCellMuted,
    QFrame#calendarDayCellToday {
        background-color: #0F172A;
        border: 1px solid #334155;
    }

    QFrame#calendarDayCell:hover,
    QFrame#calendarDayCellToday:hover {
        background-color: #111C30;
        border: 1px solid #475569;
    }

    QFrame#calendarDayCellMuted {
        background-color: #111827;
    }

    QFrame#calendarDayCellToday {
        background-color: #13213A;
        border: 1px solid #3B82F6;
    }

    QLabel#calendarDayNumber {
        color: #F8FAFC;
        font-size: 14px;
        font-weight: 600;
    }

    QLabel#calendarDayNumberMuted {
        color: #64748B;
        font-size: 14px;
        font-weight: 600;
    }

    QLabel#calendarDayNumberToday {
        background-color: #2563EB;
        color: white;
        border-radius: 13px;
        font-size: 14px;
        font-weight: 800;
        min-width: 26px;
        max-width: 26px;
        min-height: 26px;
        max-height: 26px;
    }

    QLabel#calendarMoreEvents {
        color: #94A3B8;
        font-size: 11px;
        font-weight: 600;
        padding-left: 4px;
    }
'''

# ============================================
# Event Popup Dialogs
# ============================================

EVENT_POPUP_DIALOGS_STYLE = r'''
QFrame#eventDialogContainer {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 18px;
    }

    QLabel#eventDialogTitle {
        color: #F8FAFC;
        font-size: 24px;
        font-weight: 800;
    }

    QLabel#eventDialogSubtitle {
        color: #94A3B8;
        font-size: 14px;
        font-weight: 500;
    }

    QLabel#eventDialogText {
        color: #CBD5E1;
        font-size: 14px;
        line-height: 20px;
    }

    QLabel#eventDialogInfo {
        color: #94A3B8;
        font-size: 13px;
        font-weight: 600;
    }

    QLabel#eventDialogError {
        color: #F87171;
        font-size: 13px;
        font-weight: 600;
    }

    QLineEdit#eventDialogInput,
    QComboBox#eventDialogCombo,
    QDateEdit#eventDialogDate,
    QTimeEdit#eventDialogTime {
        background-color: #0F172A;
        border: 1px solid #334155;
        border-radius: 10px;
        color: #F8FAFC;
        padding: 10px 12px;
        font-size: 14px;
        min-height: 22px;
    }

    QLineEdit#eventDialogInput:focus,
    QComboBox#eventDialogCombo:focus,
    QDateEdit#eventDialogDate:focus,
    QTimeEdit#eventDialogTime:focus {
        border: 1px solid #3B82F6;
    }

    QComboBox#eventDialogCombo::drop-down,
    QDateEdit#eventDialogDate::drop-down {
        border: none;
        background-color: transparent;
        width: 28px;
    }

    QComboBox#eventDialogCombo::down-arrow {
    image: none;
    width: 0;
    height: 0;
    }

    QTimeEdit#eventDialogTime::up-button,
    QTimeEdit#eventDialogTime::down-button,
    QTimeEdit#eventDialogTime::up-arrow,
    QTimeEdit#eventDialogTime::down-arrow {
        width: 0;
        height: 0;
        border: none;
        image: none;
        background-color: transparent;
    }

    QPushButton#eventDialogPrimaryButton {
        background-color: #2563EB;
        border: none;
        border-radius: 10px;
        color: white;
        font-size: 13px;
        font-weight: 700;
    }

    QPushButton#eventDialogPrimaryButton:hover {
        background-color: #1D4ED8;
    }

    QPushButton#eventDialogCancelButton {
        background-color: #334155;
        border: none;
        border-radius: 10px;
        color: #CBD5E1;
        font-size: 13px;
        font-weight: 700;
    }

    QPushButton#eventDialogCancelButton:hover {
        background-color: #475569;
        color: #F8FAFC;
    }

    QPushButton#eventDialogDangerButton {
        background-color: #DC2626;
        border: none;
        border-radius: 10px;
        color: white;
        font-size: 13px;
        font-weight: 700;
    }

    QPushButton#eventDialogDangerButton:hover {
        background-color: #B91C1C;
    }

    QPushButton#calendarNavIconButton {
    background-color: #273449;
    border: none;
    border-radius: 8px;
    }

    QPushButton#calendarNavIconButton:hover {
        background-color: #334155;
    }

    QPushButton#calendarTodayButton {
    background-color: #2563EB;
    border: none;
    border-radius: 8px;
    color: white;
    padding: 8px 14px;
    font-size: 13px;
    font-weight: 800;
    }

    QPushButton#calendarTodayButton:hover {
        background-color: #1D4ED8;
    }
    QLabel#eventDialogFieldLabel {
    color: #CBD5E1;
    font-size: 12px;
    font-weight: 700;
    }
    QComboBox#eventDialogCombo QAbstractItemView {
    background-color: #0F172A;
    border: 1px solid #334155;
    color: #F8FAFC;
    selection-background-color: #334155;
    selection-color: #F8FAFC;
    padding: 6px;
    }
'''

# ============================================
# Event Date Picker Calendar
# ============================================

EVENT_DATE_PICKER_CALENDAR_STYLE = r'''
QCalendarWidget#eventDateCalendar {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        color: #F8FAFC;
    }

    QCalendarWidget#eventDateCalendar QWidget {
        background-color: #1E293B;
        color: #F8FAFC;
    }

    QCalendarWidget#eventDateCalendar QWidget#qt_calendar_navigationbar {
        background-color: #1E293B;
        border-bottom: 1px solid #334155;
    }

    QCalendarWidget#eventDateCalendar QToolButton {
        background-color: #273449;
        border: none;
        border-radius: 6px;
        color: #F8FAFC;
        padding: 5px 8px;
        font-size: 12px;
        font-weight: 700;
    }

    QCalendarWidget#eventDateCalendar QToolButton:hover {
        background-color: #334155;
    }

    QCalendarWidget#eventDateCalendar QMenu {
        background-color: #0F172A;
        border: 1px solid #334155;
        color: #F8FAFC;
    }

    QCalendarWidget#eventDateCalendar QSpinBox {
    background-color: #0F172A;
    border: 1px solid #334155;
    border-radius: 6px;
    color: #F8FAFC;
    padding: 3px 22px 3px 6px;
    font-size: 12px;
    font-weight: 700;
    selection-background-color: #2563EB;
    selection-color: white;
    }

    QCalendarWidget#eventDateCalendar QAbstractItemView {
        background-color: #0F172A;
        alternate-background-color: #0F172A;
        color: #CBD5E1;
        selection-background-color: #2563EB;
        selection-color: white;
        gridline-color: #334155;
        outline: none;
    }

    QCalendarWidget#eventDateCalendar QAbstractItemView:item:hover {
        background-color: #1E293B;
        color: #F8FAFC;
    }
    QCalendarWidget#eventDateCalendar QSpinBox {
    background-color: #0F172A;
    border: 1px solid #334155;
    border-radius: 6px;
    color: #F8FAFC;
    padding: 3px 6px;
    font-size: 12px;
    font-weight: 700;
    selection-background-color: #2563EB;
    selection-color: white;
    }

    QCalendarWidget#eventDateCalendar QSpinBox {
    background-color: #0F172A;
    border: 1px solid #334155;
    border-radius: 6px;
    color: #F8FAFC;
    padding: 3px;
    font-size: 12px;
    font-weight: 700;
    selection-background-color: #2563EB;
    selection-color: white;
    }
'''

# ============================================
# Day Events Dialog
# ============================================

DAY_EVENTS_DIALOG_STYLE = r'''
QFrame#dayEventsDialogContainer {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 18px;
    }

    QLabel#dayEventsDialogTitle {
        color: #F8FAFC;
        font-size: 24px;
        font-weight: 800;
    }

    QLabel#dayEventsDialogSubtitle {
        color: #94A3B8;
        font-size: 14px;
        font-weight: 500;
    }

    QScrollArea#dayEventsScrollArea {
        background-color: transparent;
        border: none;
    }

    QWidget#dayEventsScrollContent {
        background-color: transparent;
    }

    QPushButton#calendarMoreEventsButton {
        background-color: transparent;
        border: none;
        color: #94A3B8;
        font-size: 11px;
        font-weight: 700;
        text-align: left;
        padding-left: 4px;
    }

    QPushButton#calendarMoreEventsButton:hover {
        color: #F8FAFC;
    }
'''

# ============================================
# Notes Page
# ============================================

NOTES_PAGE_STYLE = r'''
QWidget#notesPage {
        background-color: #0F172A;
    }

    QScrollArea#notesScrollArea {
        background-color: #0F172A;
        border: none;
    }

    QWidget#notesContent {
        background-color: #0F172A;
    }

    QFrame#notesListCard {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 16px;
    }

    QLabel#notesListTitle {
        color: #F8FAFC;
        font-size: 18px;
        font-weight: 700;
    }

    QLabel#notesListCounter {
        color: #94A3B8;
        font-size: 13px;
        font-weight: 600;
    }

    QPushButton#notePrimaryButton {
        background-color: #2563EB;
        border: none;
        border-radius: 10px;
        color: white;
        padding: 10px 18px;
        font-size: 14px;
        font-weight: 700;
    }

    QPushButton#notePrimaryButton:hover {
        background-color: #1D4ED8;
    }

    QPushButton#notePinButton {
        background-color: rgba(251, 191, 36, 0.14);
        border: none;
        border-radius: 8px;
    }

    QPushButton#notePinButton:hover {
    background-color: rgba(251, 191, 36, 0.24);
    }

    QPushButton#noteUnpinButton {
        background-color: rgba(148, 163, 184, 0.12);
        border: none;
        border-radius: 8px;
    }

    QPushButton#noteUnpinButton:hover {
        background-color: rgba(148, 163, 184, 0.22);
    }

    QPushButton#noteIconButton {
        background-color: rgba(96, 165, 250, 0.12);
        border: none;
        border-radius: 8px;
    }

    QPushButton#noteIconButton:hover {
        background-color: rgba(96, 165, 250, 0.22);
    }

    QPushButton#noteIconDangerButton {
        background-color: rgba(248, 113, 113, 0.12);
        border: none;
        border-radius: 8px;
    }

    QPushButton#noteIconDangerButton:hover {
        background-color: rgba(248, 113, 113, 0.22);
    }
'''

# ============================================
# Note Card
# ============================================

NOTE_CARD_STYLE = r'''
QFrame#noteCard {
        background-color: #0F172A;
        border: 1px solid #334155;
        border-radius: 14px;
    }

    QFrame#noteCard:hover {
        border: 1px solid #475569;
    }

    QLabel#noteCardTitle {
        color: #F8FAFC;
        font-size: 16px;
        font-weight: 800;
    }

    QLabel#noteCardContent {
        color: #CBD5E1;
        font-size: 13px;
        line-height: 18px;
    }
    QLabel#noteCardPinBadge {
        min-width: 22px;
        min-height: 22px;
    }

    QLabel#noteCardPin {
        font-size: 16px;
    }


    QPushButton#noteIconButton {
        background-color: rgba(96, 165, 250, 0.12);
        border: none;
        border-radius: 8px;
    }

    QPushButton#noteIconButton:hover {
        background-color: rgba(96, 165, 250, 0.22);
    }

    QPushButton#noteIconDangerButton {
        background-color: rgba(248, 113, 113, 0.12);
        border: none;
        border-radius: 8px;
    }

    QPushButton#noteIconDangerButton:hover {
        background-color: rgba(248, 113, 113, 0.22);
    }
'''

# ============================================
# Note Dialog
# ============================================

NOTE_DIALOG_STYLE = r'''
QFrame#noteDialogContainer {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 18px;
    }

    QLabel#noteDialogTitle {
        color: #F8FAFC;
        font-size: 24px;
        font-weight: 800;
    }

    QLabel#noteDialogSubtitle {
        color: #94A3B8;
        font-size: 14px;
        font-weight: 500;
    }

    QLabel#noteDialogFieldLabel {
        color: #CBD5E1;
        font-size: 12px;
        font-weight: 700;
    }

    QLabel#noteDialogError {
        color: #F87171;
        font-size: 13px;
        font-weight: 600;
    }

    QLineEdit#noteDialogInput,
    QComboBox#noteDialogCombo {
        background-color: #0F172A;
        border: 1px solid #334155;
        border-radius: 10px;
        color: #F8FAFC;
        padding: 10px 12px;
        font-size: 14px;
        min-height: 22px;
    }

    QTextEdit#noteDialogTextEdit {
        background-color: #0F172A;
        border: 1px solid #334155;
        border-radius: 10px;
        color: #F8FAFC;
        padding: 10px 12px;
        font-size: 14px;
    }

    QLineEdit#noteDialogInput:focus,
    QTextEdit#noteDialogTextEdit:focus,
    QComboBox#noteDialogCombo:focus {
        border: 1px solid #8B5CF6;
    }

    QComboBox#noteDialogCombo::drop-down {
        border: none;
        background-color: transparent;
        width: 28px;
    }

    QComboBox#noteDialogCombo::down-arrow {
        image: none;
        width: 0;
        height: 0;
    }

    QComboBox#noteDialogCombo QAbstractItemView {
        background-color: #0F172A;
        border: 1px solid #334155;
        color: #F8FAFC;
        selection-background-color: #334155;
        selection-color: #F8FAFC;
        padding: 6px;
    }

    QCheckBox#noteDialogCheckbox {
        color: #CBD5E1;
        font-size: 13px;
        font-weight: 600;
    }

    QPushButton#noteDialogPrimaryButton {
        background-color: #2563EB;
        border: none;
        border-radius: 10px;
        color: white;
        font-size: 13px;
        font-weight: 700;
    }

    QPushButton#noteDialogPrimaryButton:hover {
        background-color: #1D4ED8;
    }

    QPushButton#noteDialogCancelButton {
        background-color: #334155;
        border: none;
        border-radius: 10px;
        color: #CBD5E1;
        font-size: 13px;
        font-weight: 700;
    }

    QPushButton#noteDialogCancelButton:hover {
        background-color: #475569;
        color: #F8FAFC;
    }

    QPushButton#notePinToggleButton {
    background-color: rgba(251, 191, 36, 0.14);
    border: none;
    border-radius: 10px;
    color: #FBBF24;
    padding: 9px 14px;
    font-size: 13px;
    font-weight: 700;
    }

    QPushButton#notePinToggleButton:hover {
        background-color: rgba(251, 191, 36, 0.24);
    }

    QPushButton#notePinToggleButton:checked {
        background-color: rgba(148, 163, 184, 0.14);
        color: #CBD5E1;
    }

    QPushButton#notePinToggleButton:checked:hover {
        background-color: rgba(148, 163, 184, 0.24);
    }
    /* Goals page */

    QWidget#goalsPage {
        background-color: transparent;
    }

    QScrollArea#goalsScrollArea {
        background-color: transparent;
        border: none;
    }

    QWidget#goalsContent {
        background-color: transparent;
    }

    QLabel#goalsPageTitle {
        color: #F8FAFC;
        font-size: 28px;
        font-weight: 800;
    }

    QLabel#goalsPageSubtitle {
        color: #94A3B8;
        font-size: 14px;
    }

    QPushButton#goalsPrimaryButton {
        background-color: #2563EB;
        color: #FFFFFF;
        border: none;
        border-radius: 12px;
        font-size: 14px;
        font-weight: 700;
    }

    QPushButton#goalsPrimaryButton:hover {
        background-color: #1D4ED8;
    }

    QFrame#goalsSummaryCard,
    QFrame#goalsListCard {
        background-color: rgba(15, 23, 42, 0.86);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 18px;
    }

    QFrame#goalsSummaryItem {
        background-color: rgba(30, 41, 59, 0.62);
        border: 1px solid rgba(148, 163, 184, 0.10);
        border-radius: 14px;
    }

    QLabel#goalsSummaryValue {
        color: #F8FAFC;
        font-size: 24px;
        font-weight: 800;
    }

    QLabel#goalsSummaryLabel {
        color: #94A3B8;
        font-size: 12px;
        font-weight: 600;
    }

    QLabel#goalsListTitle {
        color: #F8FAFC;
        font-size: 18px;
        font-weight: 800;
    }

    QLabel#goalsListCount {
        color: #94A3B8;
        font-size: 13px;
        font-weight: 600;
    }

    QLabel#goalsEmptyLabel {
        color: #64748B;
        font-size: 14px;
        padding: 34px;
    }

    /* Goal card */

    QLabel#goalCardTitle {
        color: #F8FAFC;
        font-size: 16px;
        font-weight: 800;
    }

    QLabel#goalCardDescription {
        color: #CBD5E1;
        font-size: 13px;
        line-height: 18px;
    }

    QLabel#goalCardDate {
        color: #94A3B8;
        font-size: 12px;
        font-weight: 600;
    }

    QLabel#goalCardProgressLabel {
        color: #94A3B8;
        font-size: 12px;
        font-weight: 700;
    }

    QLabel#goalCardProgressValue {
        color: #F8FAFC;
        font-size: 13px;
        font-weight: 800;
    }

    QPushButton#goalSmallButton {
        background-color: rgba(59, 130, 246, 0.12);
        color: #60A5FA;
        border: none;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 800;
    }

    QPushButton#goalSmallButton:hover {
        background-color: rgba(59, 130, 246, 0.22);
    }

    QPushButton#goalIconButton {
        background-color: rgba(96, 165, 250, 0.12);
        border: none;
        border-radius: 8px;
    }

    QPushButton#goalIconButton:hover {
        background-color: rgba(96, 165, 250, 0.22);
    }

    QPushButton#goalIconDangerButton {
        background-color: rgba(248, 113, 113, 0.12);
        border: none;
        border-radius: 8px;
    }

    QPushButton#goalIconDangerButton:hover {
        background-color: rgba(248, 113, 113, 0.22);
    }

    /* Goal dialog */

    QFrame#goalDialogContainer {
        background-color: #0F172A;
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 22px;
    }

    QLabel#goalDialogTitle {
        color: #F8FAFC;
        font-size: 24px;
        font-weight: 800;
    }

    QLabel#goalDialogSubtitle {
        color: #94A3B8;
        font-size: 13px;
    }

    QLabel#goalDialogFieldLabel {
        color: #CBD5E1;
        font-size: 12px;
        font-weight: 700;
    }

    QLabel#goalDialogError {
        color: #F87171;
        font-size: 12px;
        font-weight: 700;
    }

    QLineEdit#goalDialogInput,
    QTextEdit#goalDialogTextEdit,
    QComboBox#goalDialogCombo,
    QDateEdit#goalDialogDateInput,
    QSpinBox#goalDialogSpinBox {
        background-color: rgba(15, 23, 42, 0.96);
        color: #F8FAFC;
        border: 1px solid rgba(148, 163, 184, 0.20);
        border-radius: 10px;
        padding: 9px 11px;
        font-size: 13px;
    }

    QTextEdit#goalDialogTextEdit {
        padding: 10px;
    }

    QLineEdit#goalDialogInput:focus,
    QTextEdit#goalDialogTextEdit:focus,
    QComboBox#goalDialogCombo:focus,
    QDateEdit#goalDialogDateInput:focus,
    QSpinBox#goalDialogSpinBox:focus {
        border: 1px solid #3B82F6;
    }

    QCheckBox#goalDialogCheckbox {
        color: #CBD5E1;
        font-size: 13px;
        font-weight: 600;
    }

    QPushButton#goalDialogPrimaryButton {
        background-color: #2563EB;
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 800;
    }

    QPushButton#goalDialogPrimaryButton:hover {
        background-color: #1D4ED8;
    }

    QPushButton#goalDialogCancelButton {
        background-color: rgba(148, 163, 184, 0.12);
        color: #CBD5E1;
        border: none;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 700;
    }

    QPushButton#goalDialogCancelButton:hover {
        background-color: rgba(148, 163, 184, 0.20);
    }

    /* Goal steps */

    QLabel#goalDialogSectionTitle {
        color: #F8FAFC;
        font-size: 15px;
        font-weight: 800;
    }

    QLabel#goalDialogSectionCount {
        color: #94A3B8;
        font-size: 12px;
        font-weight: 700;
        padding-left: 8px;
    }

    QPushButton#goalAddStepButton {
        background-color: rgba(59, 130, 246, 0.14);
        color: #60A5FA;
        border: none;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 800;
    }

    QPushButton#goalAddStepButton:hover {
        background-color: rgba(59, 130, 246, 0.24);
    }

    QScrollArea#goalStepsScrollArea {
        background-color: transparent;
        border: none;
    }

    QWidget#goalStepsContainer {
        background-color: transparent;
    }

    QFrame#goalStepEditor {
        background-color: rgba(30, 41, 59, 0.50);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 14px;
    }

    QLabel#goalStepEditorTitle {
        color: #F8FAFC;
        font-size: 13px;
        font-weight: 800;
    }

    QPushButton#goalStepRemoveButton {
        background-color: rgba(248, 113, 113, 0.12);
        color: #F87171;
        border: none;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 700;
    }

    QPushButton#goalStepRemoveButton:hover {
        background-color: rgba(248, 113, 113, 0.22);
    }

    QTextEdit#goalDialogSmallTextEdit {
        background-color: rgba(15, 23, 42, 0.96);
        color: #F8FAFC;
        border: 1px solid rgba(148, 163, 184, 0.20);
        border-radius: 10px;
        padding: 8px 10px;
        font-size: 13px;
    }

    QTextEdit#goalDialogSmallTextEdit:focus {
        border: 1px solid #3B82F6;
    }

    QLabel#goalCardStepsTitle {
        color: #F8FAFC;
        font-size: 13px;
        font-weight: 800;
    }

    QFrame#goalStepRow {
        background-color: rgba(30, 41, 59, 0.46);
        border: 1px solid rgba(148, 163, 184, 0.08);
        border-radius: 10px;
    }

    QLabel#goalStepTitle {
        color: #E2E8F0;
        font-size: 13px;
        font-weight: 700;
    }

    QLabel#goalStepTitleDone {
        color: #94A3B8;
        font-size: 13px;
        font-weight: 700;
        text-decoration: line-through;
    }

    QLabel#goalStepDescription {
        color: #94A3B8;
        font-size: 12px;
    }

    QCheckBox#goalStepCheckbox {
        spacing: 8px;
    }

   QPushButton#goalMainButton {
    background-color: rgba(148, 163, 184, 0.10);
    border: none;
    border-radius: 8px;
    }

    QPushButton#goalMainButton:hover {
        background-color: rgba(148, 163, 184, 0.20);
    }

    QPushButton#goalMainButtonActive {
        background-color: rgba(251, 191, 36, 0.18);
        border: 1px solid rgba(251, 191, 36, 0.55);
        border-radius: 8px;
    }

    QPushButton#goalMainButtonActive:hover {
        background-color: rgba(251, 191, 36, 0.28);
    }

    /* Calendar polish */

    QLabel#calendarPageTitle {
        color: #F8FAFC;
        font-size: 28px;
        font-weight: 800;
    }

    QLabel#calendarPageSubtitle {
        color: #94A3B8;
        font-size: 14px;
    }

    QPushButton#calendarPrimaryButton,
    QPushButton#calendarNewEventButton,
    QPushButton#newEventButton {
        background-color: #2563EB;
        color: #FFFFFF;
        border: none;
        border-radius: 12px;
        font-size: 14px;
        font-weight: 700;
    }

    QPushButton#calendarPrimaryButton:hover,
    QPushButton#calendarNewEventButton:hover,
    QPushButton#newEventButton:hover {
        background-color: #1D4ED8;
    }

    /* Notes title polish */

    QLabel#notesPageTitle {
        color: #F8FAFC;
        font-size: 28px;
        font-weight: 800;
    }

    QLabel#notesPageSubtitle {
        color: #94A3B8;
        font-size: 14px;
    }

    /* Global date inputs */

    QDateEdit::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 34px;
        border: none;
    }

    QDateEdit::down-arrow {
        image: url("assets/icons/actions/calendar.svg");
        width: 16px;
        height: 16px;
        margin-right: 10px;
    }

    QLabel#calendarPageTitle {
    color: #F8FAFC;
    font-size: 28px;
    font-weight: 800;
    }

    QLabel#calendarPageSubtitle {
        color: #94A3B8;
        font-size: 14px;
    }

    QPushButton#calendarPrimaryButton {
    background-color: #2563EB;
    color: #FFFFFF;
    border: none;
    border-radius: 12px;
    font-size: 14px;
    font-weight: 700;
    }

    QPushButton#calendarPrimaryButton:hover {
        background-color: #1D4ED8;
    }

    QLabel#notesPageTitle {
    color: #F8FAFC;
    font-size: 28px;
    font-weight: 800;
    }

    QLabel#notesPageSubtitle {
        color: #94A3B8;
        font-size: 14px;
    }

    QScrollArea#goalFormScrollArea {
    background-color: transparent;
    border: none;
    }

    QWidget#goalFormScrollContent {
        background-color: transparent;
    }

    QWidget#goalStepsContainer {
        background-color: transparent;
    }

    /* Task dialog */

    QFrame#taskDialogContainer {
        background-color: #0F172A;
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 22px;
    }

    QLabel#taskDialogTitle {
        color: #F8FAFC;
        font-size: 24px;
        font-weight: 800;
    }

    QLabel#taskDialogSubtitle {
        color: #94A3B8;
        font-size: 13px;
    }

    QLabel#taskDialogFieldLabel {
        color: #CBD5E1;
        font-size: 12px;
        font-weight: 700;
    }

    QLabel#taskDialogError {
        color: #F87171;
        font-size: 12px;
        font-weight: 700;
    }

    QLineEdit#taskDialogInput,
    QComboBox#taskDialogCombo,
    QDateEdit#taskDialogDateInput,
    QTimeEdit#taskDialogTimeInput {
        background-color: rgba(15, 23, 42, 0.96);
        color: #F8FAFC;
        border: 1px solid rgba(148, 163, 184, 0.20);
        border-radius: 10px;
        padding: 9px 11px;
        font-size: 13px;
    }

    QLineEdit#taskDialogInput:focus,
    QComboBox#taskDialogCombo:focus,
    QDateEdit#taskDialogDateInput:focus,
    QTimeEdit#taskDialogTimeInput:focus {
        border: 1px solid #3B82F6;
    }

    QPushButton#taskDialogPrimaryButton {
        background-color: #2563EB;
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 800;
    }

    QPushButton#taskDialogPrimaryButton:hover {
        background-color: #1D4ED8;
    }

    QPushButton#taskDialogCancelButton {
        background-color: rgba(148, 163, 184, 0.12);
        color: #CBD5E1;
        border: none;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 700;
    }

    QPushButton#taskDialogCancelButton:hover {
        background-color: rgba(148, 163, 184, 0.20);
    }

    QLabel#taskOverdueBadge {
    background-color: rgba(248, 113, 113, 0.16);
    color: #F87171;
    border-radius: 8px;
    padding: 4px 9px;
    font-size: 11px;
    font-weight: 800;
    }

    QLabel#taskRowDateOverdue {
        color: #F87171;
        font-size: 12px;
        font-weight: 700;
    }

    /* Reports page */

    QWidget#reportsPage {
        background-color: transparent;
    }

    QScrollArea#reportsScrollArea {
        background-color: transparent;
        border: none;
    }

    QWidget#reportsContent {
        background-color: transparent;
    }

    QLabel#reportsStatTitle {
        color: #94A3B8;
        font-size: 13px;
        font-weight: 700;
    }

    QLabel#reportsStatValue {
        color: #F8FAFC;
        font-size: 28px;
        font-weight: 800;
    }

    QLabel#reportsStatSubtitle {
        color: #CBD5E1;
        font-size: 12px;
        font-weight: 600;
    }

    QFrame#reportsSectionCard {
        background-color: rgba(15, 23, 42, 0.86);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 18px;
    }

    QLabel#reportsSectionTitle {
        color: #F8FAFC;
        font-size: 17px;
        font-weight: 800;
    }

    QLabel#reportsMetricLabel {
        color: #94A3B8;
        font-size: 13px;
        font-weight: 600;
    }

    QLabel#reportsMetricValue {
        color: #F8FAFC;
        font-size: 13px;
        font-weight: 800;
    }

    QLabel#reportsProgressLabel {
        color: #CBD5E1;
        font-size: 12px;
        font-weight: 700;
    }

    QProgressBar#reportsProgressBar {
        background-color: rgba(148, 163, 184, 0.16);
        border: none;
        border-radius: 6px;
    }

    QProgressBar#reportsProgressBar::chunk {
        background-color: #3B82F6;
        border-radius: 6px;
    }

    QFrame#reportsChartCard {
    background-color: rgba(15, 23, 42, 0.86);
    border: 1px solid rgba(148, 163, 184, 0.12);
    border-radius: 18px;
    }

    QLabel#reportsChartTitle {
        color: #F8FAFC;
        font-size: 16px;
        font-weight: 800;
    }

    QLabel#reportsChartSubtitle {
        color: #94A3B8;
        font-size: 13px;
        font-weight: 600;
    }

    QLabel#contentPageTitle {
    color: #F8FAFC;
    font-size: 28px;
    font-weight: 800;
    }

    QLabel#contentPageSubtitle {
        color: #94A3B8;
        font-size: 14px;
    }

    /* Settings page */

    QWidget#settingsPage {
        background-color: transparent;
    }

    QScrollArea#settingsScrollArea {
        background-color: transparent;
        border: none;
    }

    QWidget#settingsContent {
        background-color: transparent;
    }

    QFrame#settingsSectionCard {
        background-color: rgba(15, 23, 42, 0.86);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 18px;
    }

    QLabel#settingsSectionTitle {
        color: #F8FAFC;
        font-size: 18px;
        font-weight: 800;
    }

    QLabel#settingsFieldLabel {
        color: #94A3B8;
        font-size: 13px;
        font-weight: 700;
    }

    QLabel#settingsInfoValue {
        color: #F8FAFC;
        font-size: 13px;
        font-weight: 800;
    }

    QLabel#settingsRowTitle {
        color: #F8FAFC;
        font-size: 14px;
        font-weight: 800;
    }

    QLabel#settingsRowSubtitle {
        color: #94A3B8;
        font-size: 13px;
        font-weight: 600;
    }

    QLineEdit#settingsInput,
    QLineEdit#settingsInputReadOnly {
        background-color: rgba(15, 23, 42, 0.96);
        color: #F8FAFC;
        border: 1px solid rgba(148, 163, 184, 0.20);
        border-radius: 10px;
        padding: 9px 11px;
        font-size: 13px;
    }

    QLineEdit#settingsInput:focus {
        border: 1px solid #3B82F6;
    }

    QLineEdit#settingsInputReadOnly {
        color: #94A3B8;
        background-color: rgba(30, 41, 59, 0.48);
    }

    QPushButton#settingsPrimaryButton {
        background-color: #2563EB;
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 800;
    }

    QPushButton#settingsPrimaryButton:hover {
        background-color: #1D4ED8;
    }

    QPushButton#settingsSecondaryButton {
        background-color: rgba(59, 130, 246, 0.12);
        color: #60A5FA;
        border: none;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 800;
    }

    QPushButton#settingsSecondaryButton:hover {
        background-color: rgba(59, 130, 246, 0.22);
    }

    /* Settings dialog */

    QFrame#settingsDialogContainer {
        background-color: #0F172A;
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 22px;
    }

    QLabel#settingsDialogTitle {
        color: #F8FAFC;
        font-size: 24px;
        font-weight: 800;
    }

    QLabel#settingsDialogSubtitle {
        color: #94A3B8;
        font-size: 13px;
    }

    QLabel#settingsDialogError {
        color: #F87171;
        font-size: 12px;
        font-weight: 700;
    }

    QPushButton#settingsDialogPrimaryButton {
        background-color: #2563EB;
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 800;
    }

    QPushButton#settingsDialogPrimaryButton:hover {
        background-color: #1D4ED8;
    }

    QPushButton#settingsDialogCancelButton {
        background-color: rgba(148, 163, 184, 0.12);
        color: #CBD5E1;
        border: none;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 700;
    }

    QPushButton#settingsDialogCancelButton:hover {
        background-color: rgba(148, 163, 184, 0.20);
    }
    /* Task filters */

    QFrame#taskFiltersCard {
        background-color: rgba(15, 23, 42, 0.86);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 16px;
    }

    QLabel#taskFilterLabel {
        color: #94A3B8;
        font-size: 13px;
        font-weight: 700;
    }

    QCheckBox#taskFilterCheckbox {
        color: #CBD5E1;
        font-size: 13px;
        font-weight: 700;
        spacing: 8px;
    }

    QDateEdit#taskFilterDate,
    QComboBox#taskFilterCombo {
        background-color: rgba(15, 23, 42, 0.96);
        color: #F8FAFC;
        border: 1px solid rgba(148, 163, 184, 0.20);
        border-radius: 10px;
        padding: 8px 11px;
        font-size: 13px;
    }

    QDateEdit#taskFilterDate:focus,
    QComboBox#taskFilterCombo:focus {
        border: 1px solid #3B82F6;
    }

    QComboBox#taskFilterCombo::drop-down,
    QDateEdit#taskFilterDate::drop-down {
        border: none;
        background-color: transparent;
        width: 28px;
    }

    QComboBox#taskFilterCombo::down-arrow {
        image: none;
        width: 0;
        height: 0;
    }

    QPushButton#taskClearFilterButton {
        background-color: rgba(148, 163, 184, 0.12);
        color: #CBD5E1;
        border: none;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 800;
    }

    QPushButton#taskClearFilterButton:hover {
        background-color: rgba(148, 163, 184, 0.20);
        color: #F8FAFC;
    }
'''



DARK_THEME = _join_styles(
    GLOBAL_AND_AUTH_STYLE,
    CUSTOM_DIALOG_STYLE,
    DASHBOARD_STYLE,
    APP_LAYOUT_STYLE,
    SECTIONS_STYLE,
    DASHBOARD_STYLE_2,
    TASK_ITEMS_STYLE,
    EVENT_ITEMS_STYLE,
    GOAL_PROGRESS_STYLE,
    TASKS_PAGE_STYLE,
    TASKS_PAGE_HEADER_STYLE,
    TASK_FORM_INPUTS_STYLE,
    TASK_ACTION_ICON_BUTTONS_STYLE,
    CALENDAR_PAGE_STYLE,
    MONTH_CALENDAR_STYLE,
    EVENT_POPUP_DIALOGS_STYLE,
    EVENT_DATE_PICKER_CALENDAR_STYLE,
    DAY_EVENTS_DIALOG_STYLE,
    NOTES_PAGE_STYLE,
    NOTE_CARD_STYLE,
    NOTE_DIALOG_STYLE,
)

def get_theme():
    """Return the LifePlanner dark theme stylesheet."""
    return DARK_THEME
