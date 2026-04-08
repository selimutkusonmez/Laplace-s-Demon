from PyQt6.QtWidgets import QTabWidget,QVBoxLayout,QWidget,QComboBox,QPushButton
import pandas as pd
from src.ui.widgets.drag_and_drop_text_edit.drag_and_drop_text_edit import DragAndDropTextEdit
from src.ui.widgets.drag_and_drop_table_widget.drag_and_drop_table_widget import DragAndDropTableView
from src.ui.widgets.drag_and_drop_table_widget.table_model.df_table_model import DFTableModel

from src.ui.operation_ui.core_operation_ui.demon_core_ui import DemonCore

class BaseOperationTabUI(DemonCore):
    def __init__(self, operation_name,color_code : str):
        super().__init__(operation_name,color_code)

        self.inputs_tab_widget = QTabWidget()
        self.left_groupbox_layout.addWidget(self.inputs_tab_widget,0,0,1,2)

        #Text Tab
        self.text_tab = QWidget()
        self.text_tab_layout = QVBoxLayout()
        self.text_tab.setLayout(self.text_tab_layout)

        self.text_data_input = DragAndDropTextEdit()
        self.text_tab_layout.addWidget(self.text_data_input)

        self.inputs_tab_widget.addTab(self.text_tab,"Text Data")

        #Table Tab
        self.table_tab = QWidget()
        self.table_tab_layout = QVBoxLayout()
        self.table_tab.setLayout(self.table_tab_layout)

        self.column_picker = QComboBox()
        self.column_picker.activated.connect(self.column_chosen)
        self.table_tab_layout.addWidget(self.column_picker)

        self.table_data_input = DragAndDropTableView()
        self.table_data_input.data_loaded.connect(self.load_column_names)
        self.table_tab_layout.addWidget(self.table_data_input)

        self.choose_file_button = QPushButton("Choose File")
        self.table_tab_layout.addWidget(self.choose_file_button)

        self.inputs_tab_widget.addTab(self.table_tab,"Table Data")

        self.reset_input_button = QPushButton("Reset Current Input")
        self.reset_input_button.clicked.connect(self.reset_input_function)
        self.left_groupbox_layout.addWidget(self.reset_input_button,1,0)

        self.left_groupbox_layout.addWidget(self.calculate_button,1,1)

        self.text_data_input.textChanged.connect(self.update_display)
        self.inputs_tab_widget.currentChanged.connect(self.update_display)

        self.change_color(color_code)

    # DragAndDropTableWidget.df.columns --> OperationUI.load_column_names
    def load_column_names(self,columns : list):
        self.column_picker.clear()
        self.column_picker.addItem("All")
        self.column_picker.addItems(columns)

    # OperationUI.column_picker.currentText() --> DragAndDropTableWidget.load_column_data
    def column_chosen(self):
            try:
                column_name = self.column_picker.currentText()
                self.table_data_input.load_column_data(column_name)
                self.data = self.table_data_input.pull_colum_data(column_name)
                if self.data:
                    self.table_data = True
                self.update_display()
            except:
                return
            
    # Reset input based on tab index 0 = text, 1 = table
    def reset_input_function(self):
        index = self.inputs_tab_widget.currentIndex()
        if index == 0:
            self.text_data_input.setText("")
            self.data = None
            self.update_display()
        elif index == 1:
            self.table_data_input.setModel(DFTableModel(pd.DataFrame()))
            self.column_picker.clear()
            self.table_data = False
            self.data = None
            self.update_display()
        


    