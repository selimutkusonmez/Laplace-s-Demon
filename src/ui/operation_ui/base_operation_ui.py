from PyQt6.QtCore import pyqtSignal,Qt,QTimer
from PyQt6.QtWidgets import QWidget,QHBoxLayout,QVBoxLayout,QGroupBox,QLabel,QPushButton,QGridLayout
from PyQt6.QtGui import QPixmap
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.engine.demon_engine import DemonEngine

class BaseOperation(QWidget):
    calculation_success = pyqtSignal(list)

    def __init__(self, operation_name : str):
        super().__init__()
        self.operation_name = operation_name
        self.demon_engine = DemonEngine()
        self.init_ui()

        # We set the timer 400ms before it starts to draw formula
        self.debounce_timer = QTimer()
        self.debounce_timer.setSingleShot(True)
        self.debounce_timer.setInterval(400)
        self.debounce_timer.timeout.connect(self.update_display)


    
    def init_ui(self):

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.setObjectName("operation_widget")

        #Left GroupBox
        self.left_groupbox = QGroupBox()
        self.left_groupbox.setProperty("class","left_groupbox")
        self.left_groupbox_layout = QGridLayout()
        self.left_groupbox.setLayout(self.left_groupbox_layout)
        self.layout.addWidget(self.left_groupbox)

        self.left_groupbox.setFixedWidth(340)

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.handle_calculation)


        #Middle GroupBox
        self.middle_groupbox = QGroupBox()
        self.middle_groupbox.setProperty("class","middle_groupbox")
        self.middle_groupbox_layout = QVBoxLayout()
        self.middle_groupbox.setLayout(self.middle_groupbox_layout)
        self.layout.addWidget(self.middle_groupbox)

        self.operation_name_label = QLabel(self.operation_name)
        self.operation_name_label.setObjectName("operation_name")
        self.operation_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.middle_groupbox_layout.addWidget(self.operation_name_label)

        self.middle_groupbox_layout.addStretch()

        self.dynamic_formula = QLabel()
        self.dynamic_formula.setObjectName("dynamic_formula")
        self.dynamic_formula.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.middle_groupbox_layout.addWidget(self.dynamic_formula)

        self.middle_groupbox_layout.addStretch()

        self.bottom_groupbox = QGroupBox()
        self.bottom_groupbox.setProperty("class","bottom_groupbox")
        self.bottom_groupbox_layout = QHBoxLayout()
        self.bottom_groupbox.setLayout(self.bottom_groupbox_layout)
        self.middle_groupbox_layout.addWidget(self.bottom_groupbox)

        self.toggle_left_button = QPushButton("Toggle Inputs")
        self.toggle_left_button.clicked.connect(self.toggle_left_function)
        self.bottom_groupbox_layout.addWidget(self.toggle_left_button)

        self.bottom_groupbox_layout.addStretch()

        self.toggle_right_button = QPushButton("Toggle Info")
        self.toggle_right_button.clicked.connect(self.toggle_right_function)
        self.bottom_groupbox_layout.addWidget(self.toggle_right_button)


        #Right GroupBox
        self.right_groupbox = QGroupBox()
        self.right_groupbox_layout = QGridLayout()
        self.right_groupbox.setLayout(self.right_groupbox_layout)
        self.layout.addWidget(self.right_groupbox)

        self.right_groupbox.setFixedWidth(300)

        self.toggle_right = True
        self.toggle_left = True


    # This is out Matplotlib.mathtext
    def render_latex(self, formula_string: str, font_size: int = 25):
        fig = plt.figure(figsize=(4, 1), dpi=300)
        fig.patch.set_alpha(0.0)
        
        fig.text(0.3, 0.3, formula_string, fontsize=font_size, ha='center', va='center', math_fontfamily='cm')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1, transparent=True)
        plt.close(fig)
        buf.seek(0)
        
        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())
        
        scaled_pixmap = pixmap.scaled(
            self.middle_groupbox.width() - 20,
            self.middle_groupbox.height() - 100,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        
        self.dynamic_formula.setPixmap(scaled_pixmap)

    # All childs must have update_display
    def update_display(self):
        raise NotImplementedError("Subclasses must implement this!")


    # All childs must have calculate_function
    def calculate_function(self):
        raise NotImplementedError("Subclasses must implement this!")
    

    # OperationUI.calculate_function --> AppManager/DatabaseManager
    def handle_calculation(self):
        result = self.calculate_function()
        if result is False:
            return
        else:
            self.calculation_success.emit(result)


    # Toggle Left Groupbox
    def toggle_left_function(self):
        if self.toggle_left is True:
            self.left_groupbox.hide()
            self.toggle_left = False
        else:
            self.left_groupbox.show()
            self.toggle_left = True


    # Toggle Right Groupbox
    def toggle_right_function(self):
        if self.toggle_right is True:
            self.right_groupbox.hide()
            self.toggle_right = False
        else:
            self.right_groupbox.show()
            self.toggle_right = True