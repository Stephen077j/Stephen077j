import sys
from PySide6.QtWidgets import QApplication,QWidget,QVBoxLayout,QLabel,QPushButton
from PySide6.QtCore import QTimer

def format_time(seconds):
    if seconds<0: raise ValueError("Negative duration")
    return f"{seconds//60:02}:{seconds%60:02}"

class FocusTimer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Focus Timer")
        self.remaining=25*60
        layout=QVBoxLayout(self)
        self.clock=QLabel(format_time(self.remaining))
        self.button=QPushButton("Start / Pause")
        reset=QPushButton("Reset")
        layout.addWidget(self.clock)
        layout.addWidget(self.button)
        layout.addWidget(reset)
        self.timer=QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.button.clicked.connect(self.toggle)
        reset.clicked.connect(self.reset)
    def toggle(self):
        self.timer.stop() if self.timer.isActive() else self.timer.start(1000)
    def tick(self):
        self.remaining=max(self.remaining-1,0)
        self.clock.setText(format_time(self.remaining))
        if not self.remaining:self.timer.stop()
    def reset(self):
        self.timer.stop()
        self.remaining=25*60
        self.clock.setText(format_time(self.remaining))

if __name__=="__main__":
    app=QApplication(sys.argv)
    widget=FocusTimer()
    widget.resize(300,180)
    widget.show()
    sys.exit(app.exec())
