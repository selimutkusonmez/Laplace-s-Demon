from PyQt6.QtCore import pyqtSignal,Qt,QTimer
from PyQt6.QtWidgets import QWidget,QHBoxLayout,QVBoxLayout,QGroupBox,QLabel,QPushButton,QGridLayout,QTextEdit
from PyQt6.QtGui import QPixmap

class BaseHistoryUI(QWidget):
    def __init__(self,db_id,date,operation,variables,input_data,output):
        super().__init__()
        self.db_id = db_id
        self.date = date
        self.operation = operation
        self.variables = variables
        self.input_data = input_data
        self.output = output
        self.init_ui()

    def init_ui(self):

        self.setProperty("class","ui")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.upper_groupbox = QGroupBox()
        self.upper_groupbox_layout = QHBoxLayout()
        self.upper_groupbox.setLayout(self.upper_groupbox_layout)
        self.layout.addWidget(self.upper_groupbox)

        self.upper_groupbox_layout.addWidget(QLabel("DB ID: "))
        self.upper_groupbox_layout.addWidget(QLabel(self.db_id))

        self.upper_groupbox_layout.addStretch()

        self.upper_groupbox_layout.addWidget(QLabel("Date: "))
        self.upper_groupbox_layout.addWidget(QLabel(str(self.date)))

        self.upper_groupbox_layout.addStretch()

        self.upper_groupbox_layout.addWidget(QLabel("Operation: "))
        self.upper_groupbox_layout.addWidget(QLabel(self.operation))

        self.upper_groupbox_layout.addStretch()

        self.upper_groupbox_layout.addWidget(QLabel("Variables: "))
        self.upper_groupbox_layout.addWidget(QLabel(self.variables))

        self.upper_groupbox_layout.addStretch()

        self.export_to_pdf_button = QPushButton("EXPORT")
        self.upper_groupbox_layout.addWidget(self.export_to_pdf_button)

        self.layout.addStretch()

        self.middle_groupbox = QGroupBox()
        self.middle_groupbox_layout = QHBoxLayout()
        self.middle_groupbox.setLayout(self.middle_groupbox_layout)
        self.layout.addWidget(self.middle_groupbox)

        self.lower_groupbox = QGroupBox()
        self.lower_groupbox_layout = QHBoxLayout()
        self.lower_groupbox.setLayout(self.lower_groupbox_layout)
        self.layout.addWidget(self.lower_groupbox)

        self.layout.addStretch()

        self.buttons_groupbox = QGroupBox()
        self.buttons_groupbox.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.buttons_groupbox.setFixedHeight(85)
        self.buttons_groupbox_layout = QHBoxLayout()
        self.buttons_groupbox.setLayout(self.buttons_groupbox_layout)
        self.layout.addWidget(self.buttons_groupbox)

        self.toggle_upper_groupbox = QPushButton("Toggle Info")
        self.toggle_upper_groupbox.clicked.connect(self.toggle_upper_function)
        self.buttons_groupbox_layout.addWidget(self.toggle_upper_groupbox)

        self.toggle_middle_groupbox = QPushButton("Toggle Input")
        self.toggle_middle_groupbox.clicked.connect(self.toggle_middle_function)
        self.buttons_groupbox_layout.addWidget(self.toggle_middle_groupbox)

        self.toggle_lower_groupbox = QPushButton("Toggle Output")
        self.toggle_lower_groupbox.clicked.connect(self.toggle_lower_function)
        self.buttons_groupbox_layout.addWidget(self.toggle_lower_groupbox)   

        self.toggle_upper = True     
        self.toggle_middle = True  
        self.toggle_lower = True  

    def toggle_upper_function(self):
        if self.toggle_upper is True:
            self.upper_groupbox.hide()
            self.toggle_upper = False
        else:
            self.upper_groupbox.show()
            self.toggle_upper = True

    def toggle_middle_function(self):
        if self.toggle_middle is True:
            self.middle_groupbox.hide()
            self.toggle_middle = False
        else:
            self.middle_groupbox.show()
            self.toggle_middle = True

    def toggle_lower_function(self):
        if self.toggle_lower is True:
            self.lower_groupbox.hide()
            self.toggle_lower = False
        else:
            self.lower_groupbox.show()
            self.toggle_lower = True




