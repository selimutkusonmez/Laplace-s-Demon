from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QLabel,QTextEdit
from src.ui.operation_ui.base_operation_ui import BaseOperation
from src.ui.drag_and_drop_text_edit.drag_and_drop_text_edit import DragAndDropTextEdit

class OperationUI(BaseOperation):
    calculation_success = pyqtSignal(list)
    def __init__(self, operation_name):
        super().__init__(operation_name)

        self.left_groupbox_layout.addWidget(QLabel("Data"))

        self.data_input = DragAndDropTextEdit()
        self.left_groupbox_layout.addWidget(self.data_input)

        