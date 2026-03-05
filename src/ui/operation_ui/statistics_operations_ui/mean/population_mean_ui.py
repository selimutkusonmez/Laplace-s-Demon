from PyQt6.QtCore import pyqtSignal,Qt
from PyQt6.QtWidgets import QLabel,QTextEdit
from src.ui.operation_ui.base_operation_ui import BaseOperation
from src.ui.drag_and_drop_text_edit.drag_and_drop_text_edit import DragAndDropTextEdit
from src.engine.demon_engine import DemonEngine
class OperationUI(BaseOperation):
    def __init__(self, operation_name):
        super().__init__(operation_name)

        self.left_groupbox_layout.addWidget(QLabel("Data"),0,0,Qt.AlignmentFlag.AlignCenter)
        

        self.data_input = DragAndDropTextEdit()
        self.left_groupbox_layout.addWidget(self.data_input)

        self.left_groupbox_layout.addWidget(self.calculate_button)

        self.right_groupbox_layout.addWidget(QLabel(""))

        self.variable_1_info_label = QLabel("<i><b>&mu;</b></i>")
        self.right_groupbox_layout.addWidget(self.variable_1_info_label,0,0)

        self.variable_1_info = QTextEdit("<b>&mu; (Population Mean):</b> The average value of all observations in the entire population.<br><br>")
        self.variable_1_info.setReadOnly(True)
        self.right_groupbox_layout.addWidget(self.variable_1_info,0,1)


        self.variable_2_info_label = QLabel("&Sigma;x<sub>i</sub>")
        self.right_groupbox_layout.addWidget(self.variable_2_info_label,1,0)

        self.variable_2_info = QTextEdit("<b>&Sigma;x<sub>i</sub> (Sum of Values):</b> The total sum of all individual values in the population dataset.<br><br>")
        self.variable_2_info.setReadOnly(True)
        self.right_groupbox_layout.addWidget(self.variable_2_info,1,1)


        self.variable_3_info_label = QLabel("N")
        self.right_groupbox_layout.addWidget(self.variable_3_info_label,2,0)

        self.variable_3_info = QTextEdit("<b>N (Population Size):</b> The total number of observations or data points in the entire population.")
        self.variable_3_info.setReadOnly(True)
        self.right_groupbox_layout.addWidget(self.variable_3_info,2,1)

    def reset_and_update_display(self):
        return
    
    def update_display(self):
        return
    
    def calculate_function(self):
        return
        