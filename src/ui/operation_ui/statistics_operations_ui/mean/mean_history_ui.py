from PyQt6.QtWidgets import QTextEdit

from src.ui.operation_ui.base_history_ui import BaseHistoryUI


class MeanHistoryUI(BaseHistoryUI):
    def __init__(self, db_id, date, operation, variables, input_data, output):
        super().__init__(db_id, date, operation, variables, input_data, output)

        self.input_data_area = QTextEdit()
        self.input_data_area.setReadOnly(True)
        self.input_data_area.setText(input_data)
        self.middle_groupbox_layout.addWidget(self.input_data_area)
        