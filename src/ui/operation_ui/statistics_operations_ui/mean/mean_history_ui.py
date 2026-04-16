from PyQt6.QtWidgets import QTableView,QAbstractItemView

from src.ui.operation_ui.base_archive_record_ui import BaseArchiveRecordUI
from src.ui.widgets.drag_and_drop_table_widget.table_model.list_table_model import ListTableModel


class MeanHistoryUI(BaseArchiveRecordUI):
    def __init__(self, db_id, date, operation, variables, input_data, output):
        super().__init__(db_id, date, operation, variables, input_data, output)

        self.input_data_area = QTableView()
        self.input_data_area.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.input_data_area.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.input_data_area.setModel(ListTableModel(input_data))
        self.middle_groupbox_layout.addWidget(self.input_data_area)
        