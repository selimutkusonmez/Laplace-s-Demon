from PyQt6.QtWidgets import QFrame, QVBoxLayout,QLabel, QProgressBar
from PyQt6.QtCore import Qt

class LoadingCurtain(QFrame):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.logo_label = QLabel("LAPLACE'S DEMON")
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.logo_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedSize(300, 4)
        self.layout.addWidget(self.progress_bar)

        self.curtain_label = QLabel("Initializing System...")
        self.curtain_label.setAlignment(Qt.AlignmentFlag.AlignCenter)        
        self.layout.addWidget(self.curtain_label)

    def update_curtain(self, text: str):
        self.curtain_label.setText(text)