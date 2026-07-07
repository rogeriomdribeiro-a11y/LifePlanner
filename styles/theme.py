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

    """