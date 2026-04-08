from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QTimer
import pandas as pd
import datetime

from src.ui.operation_ui.core_operation_ui.base_operation_tab_ui import BaseOperationTabUI
from src.ui.widgets.drag_and_drop_table_widget.table_model.df_table_model import DFTableModel


class OperationUI(BaseOperationTabUI):
    def __init__(self, operation_name):
        super().__init__(operation_name)

        # Variables Info
        self.fill_right_groupbox("<i><b>&mu;</b></i>","<b>&mu; (Population Mean):</b> The average value of all observations in the entire population.<br><br>",0,0)
        self.fill_right_groupbox("<b>&Sigma;x<sub>i</sub></b>","<b>&Sigma;x<sub>i</sub> (Sum of Values):</b> The total sum of all individual values in the population dataset.<br><br>",1,0)
        self.fill_right_groupbox("<b>N</b>","<b>N (Population Size):</b> The total number of observations or data points in the entire population.",2,0)

        QTimer.singleShot(0, self.update_display)

        self.data = []
        self.table_data = False

    def update_display(self):
        index = self.inputs_tab_widget.currentIndex()
        if hasattr(self, "population_sum"):
            del self.population_sum
        if hasattr(self, "population_size"):
            del self.population_size
        if index == 0:
            self.data = self.text_data_input.pull_text_data()
            if self.data:
                self.population_sum = sum(self.data)
                self.population_size = len(self.data)
                self.render_latex(rf"$\mu = \frac{{{self.population_sum}}}{{{self.population_size}}} = Waiting...$", font_color=self.font_color)
            else:
                self.render_latex(r"$\mu = \frac{\sum x_i}{N} = Waiting...$", font_color=self.font_color)
        else:
            if self.table_data:
                self.data = self.table_data_input.pull_colum_data(self.column_picker.currentText())
                if not self.data:
                    self.render_latex(r"$\mu = \frac{\sum x_i}{N} = Waiting...$", font_color=self.font_color)
                else:
                    self.population_sum = sum(self.data)
                    self.population_size = len(self.data)  
                    self.render_latex(rf"$\mu = \frac{{{self.population_sum}}}{{{self.population_size}}} = Waiting...$", font_color=self.font_color)
            else:
                self.render_latex(r"$\mu = \frac{\sum x_i}{N} = Waiting...$", font_color=self.font_color)

    def calculate_function(self):
        try:
            result = self.demon_engine.calculate(self.operation_name, [self.population_sum, self.population_size])
            self.render_latex(rf"$\mu = \frac{{{self.population_sum}}}{{{self.population_size}}} = {{{result:.4f}}}$", font_color=self.font_color)
            log = [
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                self.operation_name,
                f"Population Sum : {self.population_sum}, Population Size : {self.population_size}",
                self.data,
                rf"$\mu = \frac{{{self.population_sum}}}{{{self.population_size}}} = {{{result:.4f}}}$"
            ]
            return log
        
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
    

            