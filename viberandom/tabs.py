from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QFileDialog, QMessageBox, QScrollArea, QSplitter,
    QCheckBox, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import random
import json
import os

from .config import config
from .components import GlowFrame, ResultDisplay, ConfettiWidget


MAIN_MARGIN_SIDES = 50
MAIN_MARGIN_TOP = 30
MAIN_MARGIN_BOTTOM = 40
MAIN_SPACING = 35

CARD_MARGIN_SIDES = 60
CARD_MARGIN_TOP = 35
CARD_MARGIN_BOTTOM = 50
CARD_SPACING = 60

STATS_SPACING = 20
STATS_MARGIN = 15


class RandomizerTab(QWidget):
    
    def __init__(self):
        super().__init__()
        self.all_values = config.DEFAULT_VALUES.copy()
        self.excluded = set()
        self.is_spinning = False
        
        self._init_ui()
        
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(MAIN_MARGIN_SIDES, MAIN_MARGIN_TOP, MAIN_MARGIN_SIDES, MAIN_MARGIN_BOTTOM)
        layout.setSpacing(MAIN_SPACING)
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("Рандомайзер")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        card = GlowFrame()
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(CARD_MARGIN_SIDES, CARD_MARGIN_TOP, CARD_MARGIN_SIDES, CARD_MARGIN_BOTTOM)
        card_layout.setSpacing(CARD_SPACING)
        card_layout.setAlignment(Qt.AlignTop)

        self.result_display = ResultDisplay()
        self.result_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        card_layout.addWidget(self.result_display, alignment=Qt.AlignCenter)

        self.spin_button = QPushButton("🎲 Крутити!")
        self.spin_button.clicked.connect(self._start_spin)
        self.spin_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        card_layout.addWidget(self.spin_button, alignment=Qt.AlignCenter)

        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(STATS_SPACING)
        stats_layout.setContentsMargins(STATS_MARGIN, STATS_MARGIN, STATS_MARGIN, STATS_MARGIN)

        active_count = len(self.all_values) - len(self.excluded)
        self.count_stat = QLabel(f"📊 {active_count} з {len(self.all_values)}")
        self.count_stat.setObjectName("stat")
        stats_layout.addWidget(self.count_stat)

        stats_layout.addStretch()

        self.status_stat = QLabel("✨ Готовий")
        self.status_stat.setObjectName("stat")
        stats_layout.addWidget(self.status_stat)

        card_layout.addLayout(stats_layout)
        layout.addWidget(card)

        self.confetti = ConfettiWidget(self)
        self.confetti.setGeometry(0, 0, self.width(), 400)
        self.confetti.hide()

        self.resize_timer = QTimer()
        self.resize_timer.timeout.connect(self._update_confetti)
        self.resize_timer.start(500)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'confetti'):
            self.confetti.setGeometry(0, 0, self.width(), 400)

    def _update_confetti(self):
        if hasattr(self, 'confetti'):
            self.confetti.setGeometry(0, 0, self.width(), 400)

    def _start_spin(self):
        active_values = self._get_active_values()

        if not active_values:
            QMessageBox.warning(self, "Увага", "Додайте хоча б одне значення!")
            return

        if self.is_spinning:
            return

        self.is_spinning = True
        self.spin_button.setEnabled(False)
        self.status_stat.setText("⏳ Крутиться...")
        self.result_display.start_spin()

        total_spins = config.SPIN_ITERATIONS
        current_spin = 0
        speed = 60

        def animate():
            nonlocal current_spin, speed

            if current_spin < total_spins:
                self.result_display.set_result(random.choice(active_values))
                current_spin += 1

                if current_spin > total_spins - 8:
                    speed += 50

                QTimer.singleShot(speed, animate)
            else:
                final = random.choice(active_values)
                self.result_display.set_result(final)
                self.result_display.stop_spin()

                self.is_spinning = False
                self.spin_button.setEnabled(True)
                self.status_stat.setText("✅ Успішно!")

                self.confetti.start(config.CONFETTI_COUNT)

        animate()

    def _get_active_values(self):
        return [v for i, v in enumerate(self.all_values) if i not in self.excluded]

    def set_values(self, values):
        self.all_values = values if values else []
        self.excluded = set()
        self._update_stats()

    def set_excluded(self, excluded_indices):
        self.excluded = set(excluded_indices)
        self._update_stats()

    def _update_stats(self):
        active_count = len(self.all_values) - len(self.excluded)
        self.count_stat.setText(f"📊 {active_count} з {len(self.all_values)}")


class ExcludeTab(QWidget):
    
    def __init__(self, on_exclude_changed=None):
        super().__init__()
        self.on_exclude_changed = on_exclude_changed
        self.values = config.DEFAULT_VALUES.copy()
        self.excluded = set()
        self._init_ui()
        
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(MAIN_MARGIN_SIDES, MAIN_MARGIN_TOP, MAIN_MARGIN_SIDES, MAIN_MARGIN_BOTTOM)
        layout.setSpacing(MAIN_SPACING)
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("Виключення")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        info_card = QFrame()
        info_card.setObjectName("card")
        info_layout = QVBoxLayout(info_card)
        info_layout.setContentsMargins(40, 40, 40, 40)
        info_layout.setSpacing(30)

        info = QLabel(
            "Відмітьте людей, які НЕ будуть брати участі в рандомайзері\n"
            "Червона галочка = виключений зі списку"
        )
        info.setObjectName("info")
        info.setAlignment(Qt.AlignCenter)
        info.setWordWrap(True)
        info_layout.addWidget(info)

        layout.addWidget(info_card)

        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(25)

        heading = QLabel("Список людей")
        heading.setObjectName("heading")
        heading.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(heading)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        checkbox_container = QWidget()
        self.checkbox_layout = QVBoxLayout(checkbox_container)
        self.checkbox_layout.setContentsMargins(10, 10, 10, 10)
        self.checkbox_layout.setSpacing(10)
        self.checkbox_layout.addStretch()

        scroll.setWidget(checkbox_container)
        card_layout.addWidget(scroll)

        self._create_checkboxes()

        self.stats_label = QLabel(f"Активних: {len(self.values) - len(self.excluded)} з {len(self.values)}")
        self.stats_label.setObjectName("info")
        self.stats_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.stats_label)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)

        select_all_btn = QPushButton("Виключити всіх")
        select_all_btn.setObjectName("dangerBtn")
        select_all_btn.clicked.connect(self._exclude_all)
        select_all_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_layout.addWidget(select_all_btn)

        deselect_all_btn = QPushButton("Обрати всіх")
        deselect_all_btn.setObjectName("successBtn")
        deselect_all_btn.clicked.connect(self._include_all)
        deselect_all_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_layout.addWidget(deselect_all_btn)

        card_layout.addLayout(btn_layout)
        layout.addWidget(card)

    def _create_checkboxes(self):
        while self.checkbox_layout.count() > 1:
            item = self.checkbox_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for i, value in enumerate(self.values):
            cb = QCheckBox(value)
            cb.setChecked(i in self.excluded)
            cb.stateChanged.connect(lambda state, idx=i: self._on_checkbox_changed(idx, state))
            self.checkbox_layout.insertWidget(i, cb)

    def _on_checkbox_changed(self, index, state):
        if state == Qt.Checked:
            self.excluded.add(index)
        else:
            self.excluded.discard(index)

        self._update_stats()

        if self.on_exclude_changed:
            self.on_exclude_changed(self.excluded)

    def _update_stats(self):
        active = len(self.values) - len(self.excluded)
        self.stats_label.setText(f"Активних: {active} з {len(self.values)}")

    def _exclude_all(self):
        self.excluded = set(range(len(self.values)))
        self._create_checkboxes()
        self._update_stats()
        if self.on_exclude_changed:
            self.on_exclude_changed(self.excluded)

    def _include_all(self):
        self.excluded = set()
        self._create_checkboxes()
        self._update_stats()
        if self.on_exclude_changed:
            self.on_exclude_changed(self.excluded)

    def set_values(self, values):
        self.values = values if values else []
        self.excluded = set()
        self._create_checkboxes()
        self._update_stats()


class SettingsTab(QWidget):
    
    def __init__(self, on_theme_change=None):
        super().__init__()
        self.on_theme_change = on_theme_change
        self.is_dark = True
        self._init_ui()
        
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(MAIN_MARGIN_SIDES, MAIN_MARGIN_TOP, MAIN_MARGIN_SIDES, MAIN_MARGIN_BOTTOM)
        layout.setSpacing(MAIN_SPACING)
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("Налаштування")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(10)

        left_card = self._create_appearance_card()
        splitter.addWidget(left_card)

        right_card = self._create_developer_card()
        splitter.addWidget(right_card)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

        layout.addWidget(splitter)

    def _create_appearance_card(self):
        card = QFrame()
        card.setObjectName("card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(40, 30, 40, 40)
        layout.setSpacing(35)
        layout.setAlignment(Qt.AlignTop)

        heading = QLabel("Зовнішній вигляд")
        heading.setObjectName("heading")
        heading.setAlignment(Qt.AlignCenter)
        layout.addWidget(heading)

        btn_frame = QFrame()
        btn_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setAlignment(Qt.AlignCenter)
        
        self.theme_button = QPushButton("Темна тема")
        self.theme_button.setObjectName("secondaryBtn")
        self.theme_button.clicked.connect(self._toggle_theme)
        self.theme_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_layout.addWidget(self.theme_button)
        
        layout.addWidget(btn_frame)

        info = QLabel("Натисніть для зміни теми")
        info.setObjectName("info")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)

        return card

    def _create_developer_card(self):
        card = QFrame()
        card.setObjectName("card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(40, 30, 40, 40)
        layout.setSpacing(25)
        layout.setAlignment(Qt.AlignTop)

        heading = QLabel("Про розробника")
        heading.setObjectName("heading")
        heading.setAlignment(Qt.AlignCenter)
        layout.addWidget(heading)



        name = QLabel("Zinus & AI")
        name.setStyleSheet("color: #8b5cf6; font-size: 18px; font-weight: bold;")
        name.setAlignment(Qt.AlignCenter)
        layout.addWidget(name)

        #desc = QLabel(
        #    "\n"
        #    ""
        #)
        #desc.setObjectName("info")
        #desc.setAlignment(Qt.AlignCenter)
        #desc.setWordWrap(True)
        #layout.addWidget(desc)

        btn_frame = QFrame()
        btn_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setAlignment(Qt.AlignCenter)
        
        github_btn = QPushButton("GitHub Профіль")
        github_btn.setObjectName("secondaryBtn")
        github_btn.clicked.connect(lambda: __import__("webbrowser").open("https://github.com/Zinusss"))
        github_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_layout.addWidget(github_btn)
        
        layout.addWidget(btn_frame)

        version = QLabel("v1.0 • 2026")
        version.setStyleSheet("color: #6b7280; font-size: 10px;")
        version.setAlignment(Qt.AlignCenter)
        layout.addWidget(version)

        return card

    def _toggle_theme(self):
        self.is_dark = not self.is_dark

        if self.is_dark:
            self.theme_button.setText("Темна тема")
        else:
            self.theme_button.setText("Світла тема")

        if self.on_theme_change:
            self.on_theme_change(self.is_dark)


class ValuesTab(QWidget):
    
    def __init__(self, on_values_changed=None):
        super().__init__()
        self.on_values_changed = on_values_changed
        self.values = config.DEFAULT_VALUES.copy()
        self._init_ui()
        
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(MAIN_MARGIN_SIDES, MAIN_MARGIN_TOP, MAIN_MARGIN_SIDES, MAIN_MARGIN_BOTTOM)
        layout.setSpacing(MAIN_SPACING)
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("Значення")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 30, 40, 40)
        card_layout.setSpacing(35)
        card_layout.setAlignment(Qt.AlignTop)

        info = QLabel("Додайте значення (кожне з нового рядка) • Імпорт: .txt, .json, .csv")
        info.setObjectName("info")
        info.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(info)

        self.text_area = QTextEdit()
        self.text_area.setPlaceholderText("Введіть значення тут...")
        self.text_area.setText("\n".join(self.values))
        self.text_area.setMinimumHeight(250)
        card_layout.addWidget(self.text_area)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        btn_layout.setContentsMargins(20, 15, 20, 15)

        import_btn = QPushButton("Імпорт")
        import_btn.setObjectName("secondaryBtn")
        import_btn.clicked.connect(self._import_values)
        import_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_layout.addWidget(import_btn)

        export_btn = QPushButton("Експорт")
        export_btn.setObjectName("secondaryBtn")
        export_btn.clicked.connect(self._export_values)
        export_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_layout.addWidget(export_btn)

        btn_layout.addStretch()

        clear_btn = QPushButton("Очистити")
        clear_btn.setObjectName("dangerBtn")
        clear_btn.clicked.connect(self._clear_values)
        clear_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_layout.addWidget(clear_btn)

        save_btn = QPushButton("Зберегти")
        save_btn.setObjectName("successBtn")
        save_btn.clicked.connect(self._save_values)
        save_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_layout.addWidget(save_btn)

        card_layout.addLayout(btn_layout)

        self.count_label = QLabel(f"Всього: {len(self.values)}")
        self.count_label.setObjectName("info")
        self.count_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.count_label)

        layout.addWidget(card)

    def _import_values(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Оберіть файл", "",
            "Текстові файли (*.txt);;JSON файли (*.json);;CSV файли (*.csv);;Всі файли (*.*)"
        )

        if not filepath:
            return

        try:
            ext = os.path.splitext(filepath)[1].lower()

            if ext == ".json":
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        imported = [str(item) for item in data]
                    else:
                        QMessageBox.critical(self, "Помилка", "JSON має містити список")
                        return
            else:
                with open(filepath, "r", encoding="utf-8") as f:
                    imported = [line.strip() for line in f if line.strip()]

            if imported:
                current = self.text_area.toPlainText().strip()
                new_text = current + "\n" + "\n".join(imported) if current else "\n".join(imported)
                self.text_area.setText(new_text)
                QMessageBox.information(self, "Успіх", f"Імпортовано {len(imported)} значень!")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося імпортувати:\n{str(e)}")

    def _export_values(self):
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Зберегти у файл", "",
            "Текстові файли (*.txt);;JSON файли (*.json);;Всі файли (*.*)"
        )

        if not filepath:
            return

        try:
            values = self.text_area.toPlainText().strip().splitlines()
            ext = os.path.splitext(filepath)[1].lower()

            if ext == ".json":
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(values, f, ensure_ascii=False, indent=2)
            else:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write("\n".join(values))

            QMessageBox.information(self, "Успіх", f"Експортовано {len(values)} значень!")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Не вдалося експортувати:\n{str(e)}")

    def _save_values(self):
        text = self.text_area.toPlainText().strip()
        self.values = [line.strip() for line in text.splitlines() if line.strip()]

        self.count_label.setText(f"Всього: {len(self.values)}")

        if self.on_values_changed:
            self.on_values_changed(self.values)

        QMessageBox.information(self, "Збережено", f"Збережено {len(self.values)} значень!")

    def _clear_values(self):
        reply = QMessageBox.question(
            self, "Підтвердження",
            "Видалити всі значення?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.text_area.clear()
            self.values = []
            self.count_label.setText("Всього: 0")
            if self.on_values_changed:
                self.on_values_changed([])
