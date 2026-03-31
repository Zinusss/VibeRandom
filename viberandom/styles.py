def get_stylesheet(colors):
    return f"""
QMainWindow {{
    background-color: {colors['bg_window']};
}}

QWidget {{
    background-color: transparent;
    color: {colors['text_primary']};
    font-family: 'Segoe UI', Arial, sans-serif;
}}

QTabWidget::pane {{
    border: 2px solid {colors['border']};
    border-radius: 20px;
    background-color: {colors['bg_card']};
}}

QTabBar::tab {{
    background-color: {colors['bg_button']};
    color: {colors['text_secondary']};
    padding: 15px 30px;
    margin: 2px 3px;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
    font-size: 13px;
    font-weight: bold;
    min-width: 150px;
}}

QTabBar::tab:selected {{
    background-color: {colors['accent']};
    color: #ffffff;
}}

QTabBar::tab:hover:!selected {{
    background-color: {colors['bg_button_hover']};
    color: {colors['text_primary']};
}}

.QFrame#card {{
    background-color: {colors['bg_card']};
    border: 2px solid {colors['accent']};
    border-radius: 20px;
}}

.QFrame#statCard {{
    background-color: {colors['bg_card_alt']};
    border-radius: 15px;
    border: 1px solid {colors['border']};
}}

.QFrame#header {{
    background-color: {colors['bg_card']};
    border-radius: 15px;
    border: 1px solid {colors['border']};
}}

QPushButton {{
    background-color: {colors['accent']};
    color: #ffffff;
    border: none;
    border-radius: 15px;
    padding: 15px 40px;
    font-size: 15px;
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: {colors['accent_hover']};
}}

QPushButton:pressed {{
    background-color: {colors['accent']};
}}

QPushButton:disabled {{
    background-color: {colors['bg_button']};
    color: {colors['text_muted']};
}}

QPushButton#secondaryBtn {{
    background-color: {colors['bg_button']};
    font-size: 13px;
    padding: 14px 28px;
}}

QPushButton#secondaryBtn:hover {{
    background-color: {colors['bg_button_hover']};
}}

QPushButton#successBtn {{
    background-color: {colors['success']};
}}

QPushButton#successBtn:hover {{
    background-color: {colors['success_hover']};
}}

QPushButton#dangerBtn {{
    background-color: {colors['danger']};
}}

QPushButton#dangerBtn:hover {{
    background-color: {colors['danger_hover']};
}}

QTextEdit {{
    background-color: {colors['bg_input']};
    color: {colors['text_primary']};
    border: 2px solid {colors['accent']};
    border-radius: 12px;
    padding: 15px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 13px;
    selection-background-color: {colors['accent']};
}}

QTextEdit:focus {{
    border: 2px solid {colors['accent_hover']};
}}

QTextEdit::placeholder {{
    color: {colors['text_muted']};
}}

QLabel#title {{
    font-size: 34px;
    font-weight: bold;
    color: {colors['accent']};
    qproperty-alignment: AlignVCenter;
}}

QLabel#subtitle {{
    font-size: 13px;
    color: {colors['text_secondary']};
    qproperty-alignment: AlignVCenter;
}}

QLabel#heading {{
    font-size: 18px;
    font-weight: bold;
    color: {colors['text_primary']};
}}

QLabel#result {{
    font-size: 36px;
    font-weight: bold;
    color: {colors['accent']};
    background-color: {colors['bg_input']};
    border-radius: 25px;
    padding: 35px 55px;
    qproperty-wordWrap: false;
    qproperty-alignment: AlignCenter;
}}

QLabel#stat {{
    font-size: 13px;
    color: {colors['text_primary']};
    padding: 12px 24px;
    background-color: {colors['bg_card_alt']};
    border-radius: 12px;
    border: 1px solid {colors['border']};
}}

QLabel#info {{
    font-size: 12px;
    color: {colors['text_secondary']};
}}

QCheckBox {{
    color: {colors['text_primary']};
    font-size: 13px;
    spacing: 10px;
    padding: 8px 12px;
    background-color: {colors['bg_card_alt']};
    border-radius: 8px;
    border: 1px solid {colors['border']};
}}

QCheckBox::indicator {{
    width: 20px;
    height: 20px;
    border-radius: 5px;
    border: 2px solid {colors['border']};
    background-color: {colors['bg_input']};
}}

QCheckBox::indicator:checked {{
    background-color: {colors['danger']};
    border-color: {colors['danger']};
}}

QCheckBox::indicator:hover {{
    border-color: {colors['accent']};
}}

QCheckBox:hover {{
    background-color: {colors['bg_card']};
}}

QScrollBar:vertical {{
    background-color: {colors['bg_button']};
    width: 12px;
    border-radius: 6px;
    margin: 2px;
}}

QScrollBar::handle:vertical {{
    background-color: {colors['accent']};
    border-radius: 6px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {colors['accent_hover']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: none;
}}
"""
