from PyQt5.QtWidgets import QFrame, QLabel, QHBoxLayout, QWidget, QGraphicsDropShadowEffect, QSizePolicy
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor, QPainter, QFont
import random


class GlowFrame(QFrame):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.glow_intensity = 0
        self.is_spinning = False
        
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(30)
        self.shadow.setColor(QColor("#8b5cf6"))
        self.shadow.setOffset(0, 0)
        self.setGraphicsEffect(self.shadow)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self._animate_glow)
        
    def start_spin(self):
        self.is_spinning = True
        self.timer.start(50)
        
    def stop_spin(self):
        self.is_spinning = False
        self.timer.stop()
        self.glow_intensity = 0
        self.shadow.setBlurRadius(30)
        
    def _animate_glow(self):
        self.glow_intensity = (self.glow_intensity + 10) % 360
        intensity = 20 + 15 * abs(((self.glow_intensity % 720) - 360) / 360)
        self.shadow.setBlurRadius(int(intensity))


class ResultDisplay(QFrame):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setMinimumHeight(220)
        self.setMaximumHeight(320)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(50)
        self.shadow.setColor(QColor("#8b5cf6"))
        self.shadow.setOffset(0, 0)
        self.setGraphicsEffect(self.shadow)
        
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(50, 30, 50, 30)
        
        self.result_label = QLabel("?")
        self.result_label.setObjectName("result")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setWordWrap(False)
        self.result_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.result_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(self.result_label)
        
        self.glow_timer = QTimer()
        self.glow_timer.timeout.connect(self._animate)
        self.glow_angle = 0
        
    def set_result(self, text):
        text = str(text)
        
        if len(text) > 50:
            font_size = 24
        elif len(text) > 35:
            font_size = 28
        elif len(text) > 25:
            font_size = 32
        else:
            font_size = 36
            
        self.result_label.setFont(QFont("Segoe UI", font_size, QFont.Bold))
        self.result_label.setText(text)
        
    def start_spin(self):
        self.glow_timer.start(50)
        
    def stop_spin(self):
        self.glow_timer.stop()
        self.shadow.setBlurRadius(40)
        
    def _animate(self):
        self.glow_angle = (self.glow_angle + 15) % 360
        intensity = 30 + 20 * abs(((self.glow_angle % 720) - 360) / 360)
        self.shadow.setBlurRadius(int(intensity))


class ConfettiWidget(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.particles = []
        self.colors = [
            QColor("#f472b6"), QColor("#a78bfa"), QColor("#60a5fa"),
            QColor("#34d399"), QColor("#fbbf24"), QColor("#f87171")
        ]
        self.timer = QTimer()
        self.timer.timeout.connect(self._update)
        
    def start(self, count=80):
        self.particles = []
        width = self.parent().width() if self.parent() else 800
        
        for _ in range(count):
            self.particles.append({
                'x': random.randint(0, max(100, width - 100)),
                'y': random.randint(-50, 100),
                'vx': random.uniform(-3, 3),
                'vy': random.uniform(3, 8),
                'size': random.randint(8, 15),
                'color': random.choice(self.colors),
                'rotation': random.randint(0, 360)
            })
            
        self.timer.start(16)
        self.show()
        
    def _update(self):
        height = self.height()
        self.particles = [p for p in self.particles if p['y'] < height]
        
        if not self.particles:
            self.timer.stop()
            self.hide()
            return
            
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['rotation'] += 10
            
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        for p in self.particles:
            painter.save()
            painter.translate(p['x'], p['y'])
            painter.rotate(p['rotation'])
            painter.setBrush(p['color'])
            painter.setPen(Qt.NoPen)
            painter.drawRect(-p['size']//2, -p['size']//2, p['size'], p['size'])
            painter.restore()
