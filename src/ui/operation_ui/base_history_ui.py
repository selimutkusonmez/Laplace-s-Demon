from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget,QHBoxLayout,QVBoxLayout,QGroupBox,QLabel,QPushButton,QGridLayout,QTextEdit,QSizePolicy
from PyQt6.QtGui import QPixmap
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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
        self.upper_groupbox.setMaximumHeight(75)
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
        self.export_to_pdf_button.clicked.connect(self.export_to_pdf_function)
        self.upper_groupbox_layout.addWidget(self.export_to_pdf_button)

        self.middle_groupbox = QGroupBox()
        self.middle_groupbox_layout = QHBoxLayout()
        self.middle_groupbox.setLayout(self.middle_groupbox_layout)
        self.layout.addWidget(self.middle_groupbox,1)

        self.lower_groupbox = QGroupBox()
        
        self.lower_groupbox_layout = QHBoxLayout()
        self.lower_groupbox.setLayout(self.lower_groupbox_layout)
        self.layout.addWidget(self.lower_groupbox,1)

        self.output_formula = QLabel()
        self.output_formula.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.render_latex(self.output)
        self.lower_groupbox_layout.addWidget(self.output_formula)

        self.buttons_groupbox = QGroupBox()
        self.buttons_groupbox.setFixedHeight(85)
        self.buttons_groupbox_layout = QHBoxLayout()
        self.buttons_groupbox.setLayout(self.buttons_groupbox_layout)
        self.layout.addWidget(self.buttons_groupbox,Qt.AlignmentFlag.AlignBottom)

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

    def render_latex(self, formula_string: str, font_size: int = 25):
        fig = plt.figure(figsize=(4, 1), dpi=300)
        fig.patch.set_alpha(0.0)
        
        fig.text(0.5, 0.5, formula_string, fontsize=font_size, ha='center', va='center', math_fontfamily='cm')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1, transparent=True)
        plt.close(fig)
        buf.seek(0)
        
        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())
        
        self.scaled_pixmap = pixmap.scaled(
            self.lower_groupbox.width(),
            self.lower_groupbox.height(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        
        self.output_formula.setPixmap(self.scaled_pixmap)


    def toggle_upper_function(self):
        if self.toggle_upper is True:
            self.upper_groupbox.hide()
            self.toggle_upper = False
        else:
            self.upper_groupbox.show()
            self.toggle_upper = True

        if not True in  [self.toggle_upper,self.toggle_middle,self.toggle_lower]:
            self.buttons_groupbox.hide()
            self.layout.addStretch()
            self.buttons_groupbox.show()

    def toggle_upper_function(self):
        if self.toggle_upper is True:
            self.upper_groupbox.hide()
            self.toggle_upper = False
        else:
            self.upper_groupbox.show()
            self.toggle_upper = True
        self.update_layout_physics()

    def toggle_middle_function(self):
        if self.toggle_middle is True:
            self.middle_groupbox.hide()
            self.toggle_middle = False
        else:
            self.middle_groupbox.show()
            self.toggle_middle = True
        self.update_layout_physics()

    def toggle_lower_function(self):
        if self.toggle_lower is True:
            self.lower_groupbox.hide()
            self.toggle_lower = False
        else:
            self.lower_groupbox.show()
            self.toggle_lower = True
        self.update_layout_physics()

    def update_layout_physics(self):
            if not any([self.toggle_middle, self.toggle_lower]):
                self.layout.insertStretch(self.layout.indexOf(self.buttons_groupbox), 1)
            else:
                for i in reversed(range(self.layout.count())):
                    item = self.layout.itemAt(i)
                    if item and item.spacerItem():
                        self.layout.takeAt(i)
    def export_to_pdf_function(self):
        raise NotImplementedError("Subclasses must implement this!")




