from PyQt6.QtWidgets import QLabel,QTextEdit,QTabWidget,QVBoxLayout,QWidget,QComboBox,qAbstra

from src.ui.operation_ui.base_operation_ui import BaseOperation

from src.ui.drag_and_drop_text_edit.drag_and_drop_text_edit import DragAndDropTextEdit
from src.ui.drag_and_drop_table_widget.drag_and_drop_table_widget import DragAndDropTableWidget

from src.engine.demon_engine import DemonEngine

class OperationUI(BaseOperation):
    def __init__(self, operation_name):
        super().__init__(operation_name)       

        self.inputs_tab_widget = QTabWidget()

        self.text_data_input = DragAndDropTextEdit()
        self.inputs_tab_widget.addTab(self.text_data_input,"Text Data")

        self.table_layout = QVBoxLayout()
        self.table_widget = QWidget()
        self.table_widget.setLayout(self.table_layout)

        self.column_picker = QComboBox()
        self.column_picker.currentTextChanged.connect(self.column_chosen)
        self.table_layout.addWidget(self.column_picker)

        self.table_data_input = DragAndDropTableWidget()
        self.table_data_input.data_loaded.connect(self.load_column_names)
        self.table_layout.addWidget(self.table_data_input)

        self.inputs_tab_widget.addTab(self.table_widget,"Table Data")

        self.left_groupbox_layout.addWidget(self.inputs_tab_widget)

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

        self.text_data_input.textChanged.connect(self.reset_and_update_display)
        self.table_data_input.itemChanged.connect(self.reset_and_update_display)

        self.render_latex(r"$\mu = \frac{\sum x_i}{N} = Waiting...$")

        self.data = []
        self.table_data = False

    def reset_and_update_display(self):
        self.current_result = "Waiting..."
        self.update_display()
    
    def update_display(self):

        index = self.inputs_tab_widget.currentIndex()
        if index == 0:
            self.data = self.text_data_input.pull_text_data()
            self.population_sum = sum(self.data)
            self.population_size = len(self.data)
        else:
            if self.table_data:
                self.data = self.table_data_input.pull_colum_data(self.column_picker.currentText())
                self.population_sum = sum(self.data)
                self.population_size = len(self.data)

        if self.data == []:
            self.render_latex(r"$\mu = \frac{\sum x_i}{N} = Waiting...$")
        
        else:
            self.render_latex(rf"$\mu = \frac{{{self.population_sum}}}{{{self.population_size}}} = {{{self.current_result}}}$")


    def calculate_function(self):
        result = DemonEngine(self.operation_name,[self.population_sum,self.population_size])
        self.render_latex(rf"$\mu = \frac{{{self.population_sum}}}{{{self.population_size}}} = {{{result}}}$")
            

    # DragAndDropTableWidget.df.columns --> OperationUI.load_column_names
    def load_column_names(self,columns : list):
        self.column_picker.clear()
        self.column_picker.addItem("All")
        self.column_picker.addItems(columns)
        self.column_picker.setCurrentIndex(1)

    # OperationUI.column_picker.currentText() --> DragAndDropTableWidget.load_column_data
    def column_chosen(self):
        column = self.column_picker.currentText()
        self.table_data_input.load_column_data(column)
        self.data = self.table_data_input.pull_colum_data(self.column_picker.currentText())
        self.population_sum = sum(self.data)
        self.population_size = len(self.data)
        self.table_data = True
        self.reset_and_update_display()
        

    


        