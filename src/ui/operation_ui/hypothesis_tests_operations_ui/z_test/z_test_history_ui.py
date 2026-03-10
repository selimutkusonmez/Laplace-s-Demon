from PyQt6.QtWidgets import QTextEdit,QLabel
from PyQt6.QtGui import QPixmap

from src.ui.operation_ui.base_history_ui import BaseHistoryUI


class zTestHistoryUI(BaseHistoryUI):
    def __init__(self, db_id, date, operation, variables, input_data, output):
        super().__init__(db_id, date, operation, variables, input_data, output)


        self.input_data_area = QTextEdit()
        self.input_data_area.setText(input_data)
        self.middle_groupbox_layout.addWidget(self.input_data_area)

        self.output_data_area = QLabel()
        self.output_data_area.setPixmap(output)
        self.middle_groupbox_layout.addWidget(self.output_data_area)
        