from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QTabWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from .config import config, theme
from .styles import get_stylesheet
from .tabs import RandomizerTab, ExcludeTab, SettingsTab, ValuesTab


class VibeRandomApp(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.is_dark = True
        self.current_theme = theme.DARK
        self._init_ui()
        
    def _init_ui(self):
        self.setWindowTitle(config.WINDOW_TITLE)
        self.setMinimumSize(config.WINDOW_MIN_WIDTH, config.WINDOW_MIN_HEIGHT)
        self.resize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        
        self._center_window()
        
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(30, 25, 30, 25)
        main_layout.setSpacing(20)
        
        self._create_header(main_layout)
        
        self.tabs = QTabWidget()
        self.tabs.setObjectName("mainTabs")
        main_layout.addWidget(self.tabs)
        
        self.randomizer = RandomizerTab()
        self.exclude_tab = ExcludeTab(on_exclude_changed=self.randomizer.set_excluded)
        self.settings = SettingsTab(on_theme_change=self._toggle_theme)
        self.values = ValuesTab(on_values_changed=self._on_values_changed)
        
        self.tabs.addTab(self.randomizer, "Рандомайзер")
        self.tabs.addTab(self.exclude_tab, "Виключення")
        self.tabs.addTab(self.settings, "Налаштування")
        self.tabs.addTab(self.values, "Значення")
        
        self._apply_theme()
        
    def _center_window(self):
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)
        
    def _create_header(self, layout):
        header = QFrame()
        header.setObjectName("header")
        header.setFixedHeight(90)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(30, 15, 30, 15)
        header_layout.setSpacing(25)
        header_layout.setAlignment(Qt.AlignVCenter)

        logo = QLabel("?")
        logo.setFont(QFont("Segoe UI Emoji", 48))
        logo.setAlignment(Qt.AlignVCenter)
        header_layout.addWidget(logo)

        title_frame = QFrame()
        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(15, 8, 15, 8)
        title_layout.setSpacing(3)
        title_layout.setAlignment(Qt.AlignVCenter)

        title = QLabel("VibeRandom")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignVCenter)
        title_layout.addWidget(title)

        header_layout.addWidget(title_frame)
        header_layout.addStretch()

        layout.addWidget(header)
        
    def _apply_theme(self):
        self.current_theme = theme.DARK if self.is_dark else theme.LIGHT
        self.setStyleSheet(get_stylesheet(self.current_theme))
        
    def _on_values_changed(self, values):
        self.randomizer.set_values(values)
        self.exclude_tab.set_values(values)
        
    def _toggle_theme(self, is_dark):
        self.is_dark = is_dark
        self._apply_theme()


def main():
    app = QApplication([])
    
    app.setApplicationName("VibeRandom")
    app.setApplicationVersion("1.0")
    
    window = VibeRandomApp()
    window.show()
    
    import sys
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
