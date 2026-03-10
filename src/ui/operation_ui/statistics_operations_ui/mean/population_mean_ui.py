from PyQt6.QtWidgets import QLabel,QTextEdit,QTabWidget,QVBoxLayout,QWidget,QComboBox,QPushButton,QMessageBox
import pandas as pd
import datetime

from src.ui.operation_ui.base_operation_ui import BaseOperation

from src.ui.widgets.drag_and_drop_text_edit.drag_and_drop_text_edit import DragAndDropTextEdit
from src.ui.widgets.drag_and_drop_table_widget.drag_and_drop_table_widget import DragAndDropTableView
from src.ui.widgets.drag_and_drop_table_widget.table_model.table_model import TableModel


class OperationUI(BaseOperation):
    def __init__(self, operation_name):
        super().__init__(operation_name)       

        self.inputs_tab_widget = QTabWidget()
        self.left_groupbox_layout.addWidget(self.inputs_tab_widget)

        #Text Tab
        self.text_tab = QWidget()
        self.text_tab_layout = QVBoxLayout()
        self.text_tab.setLayout(self.text_tab_layout)

        self.text_data_input = DragAndDropTextEdit()
        self.text_tab_layout.addWidget(self.text_data_input)

        self.reset_text_data_input_button = QPushButton("Reset Input")
        self.reset_text_data_input_button.clicked.connect(self.reset_text_data_input_function)
        self.text_tab_layout.addWidget(self.reset_text_data_input_button)

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

        self.reset_table_data_input_button = QPushButton("Reset Input")
        self.reset_table_data_input_button.clicked.connect(self.reset_table_data_input_function)
        self.table_tab_layout.addWidget(self.reset_table_data_input_button)

        self.inputs_tab_widget.addTab(self.table_tab,"Table Data")


        self.left_groupbox_layout.addWidget(self.calculate_button)

        # Variables Info
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

        self.text_data_input.textChanged.connect(self.update_display)
        self.inputs_tab_widget.currentChanged.connect(self.update_display)
        

        self.render_latex(r"$\mu = \frac{\sum x_i}{N} = Waiting...$")

        self.data = []
        self.table_data = False
    
    def update_display(self):
        #Get currentIndex from inputs_tab_widget
        index = self.inputs_tab_widget.currentIndex()
        if index == 0:
            #If Text Data tab is chosen call pull_text_data
            self.data = self.text_data_input.pull_text_data()
            self.population_sum = sum(self.data)
            self.population_size = len(self.data)
        else:
            #If Table Data is chosen
            #If column_chosen called and table_data is True
            if self.table_data:
                #Call pull_column_data
                self.data = self.table_data_input.pull_colum_data(self.column_picker.currentText())
                #If data is an empty list caused by text data or another reason
                if self.data == []:
                    self.render_latex(r"$\mu = \frac{\sum x_i}{N} = Waiting...$")
                else:
                    self.population_sum = sum(self.data)
                    self.population_size = len(self.data)
            else:return

        #If no self data or self data is and empty list caused by any error
        if self.data == []:
            self.render_latex(r"$\mu = \frac{\sum x_i}{N} = Waiting...$")
        
        else:
            self.render_latex(rf"$\mu = \frac{{{self.population_sum}}}{{{self.population_size}}} = Waiting...$")

    # self.calculate_function --> BaseOperation.handle_calculation --> AppManager --> DatabaseManager.save_log / LogsUI.add_new_log
    def calculate_function(self):
        try:
            result = self.demon_engine.calculate(self.operation_name,[self.population_sum,self.population_size])
            self.render_latex(rf"$\mu = \frac{{{self.population_sum}}}{{{self.population_size}}} = {{{result:.4f}}}$")
            log = [
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                self.operation_name,
                f"Population Sum : {self.population_sum}, Population Size : {self.population_size}",
                "input_data",
                result
                ]
            return log
        
        #If no or missing input
        except AttributeError:
            QMessageBox.warning(
                self,
                "No Data",
                "Please remember to fill all the inputs"
            )
            return [False]
        
        except ZeroDivisionError:
            QMessageBox.warning(
                self,
                "No Data",
                "Please remember to fill all the inputs"
            )
            return [False]

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
            if self.data == []:
                self.render_latex(r"$\mu = \frac{\sum x_i}{N} = Waiting...$")
            else:
                self.population_sum = sum(self.data)
                self.population_size = len(self.data)
                self.table_data = True
                self.render_latex(rf"$\mu = \frac{{{self.population_sum}}}{{{self.population_size}}} = Waiting...$")
        except:
            return
        
    #Clear Text Data and delete variables
    def reset_text_data_input_function(self):
        self.text_data_input.setText("")
        if hasattr(self,"population_sum") and hasattr(self,"population_size"):
            del self.population_sum
            del self.population_size
        else:
            return

    #Set and empty df model to the table_data_input clear column_picker and delete variables
    def reset_table_data_input_function(self):
        self.table_data_input.setModel(TableModel(pd.DataFrame()))
        self.column_picker.clear()
        self.render_latex(r"$\mu = \frac{\sum x_i}{N} = Waiting...$")
        self.table_data = False
        if hasattr(self,"population_sum") and hasattr(self,"population_size"):
            del self.population_sum
            del self.population_size
        else:
            return
            