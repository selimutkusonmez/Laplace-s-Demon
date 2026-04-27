from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QTimer
import pandas as pd
import datetime

from src.ui.operation_ui.core_operation_ui.base_operation_tab_ui import BaseOperationTabUI
from src.ui.widgets.drag_and_drop_table_widget.table_model.df_table_model import DFTableModel


class OperationUI(BaseOperationTabUI):
    def __init__(self, operation_name,color_code : str):
        super().__init__(operation_name,color_code)       

        # Variables Info
        self.fill_right_groupbox("<b>&sigma;</b>",
                                "<b>&sigma; (Population Standard Deviation):</b><br>"
                                "It is the square root of the population variance. It represents the average distance "
                                "between each data point and the population mean in the original units of the data.",0,0)
        self.fill_right_groupbox("<i><b>&mu;</b></i>","<b>&mu; (Population Mean):</b> The average value of all observations in the entire population.",1,0)
        self.fill_right_groupbox("<b>N</b>","<b>N (Population Size):</b> The total number of observations or data points in the entire population.",2,0)

        QTimer.singleShot(0, self.update_display)

        self.data = []
        self.table_data = False

    def update_display(self):
        index = self.inputs_tab_widget.currentIndex()
        if hasattr(self, "population_size"):
            del self.population_size
        if hasattr(self, "population_mean"):
            del self.population_mean
        if index == 0:
            self.data = self.text_data_input.pull_text_data()
            if self.data:
                self.population_size = len(self.data)
                self.population_mean = sum(self.data) / self.population_size
                self.render_latex(rf"$\sigma = \sqrt{{\frac{{\sum (x_i - {self.population_mean:.3f})^2}}{{{self.population_size}}}}} = Waiting...$", font_color=self.font_color)
            else:
                self.render_latex(r"$\sigma = \sqrt{\frac{\sum (x_i - \mu)^2}{N}} = Waiting...$", font_color=self.font_color)
        else:
            if self.table_data:
                self.data = self.table_data_input.pull_colum_data(self.column_picker.currentText())
                if not self.data:
                    self.render_latex(r"$\sigma = \sqrt{\frac{\sum (x_i - \mu)^2}{N}} = Waiting...$", font_color=self.font_color)
                else:
                    self.population_size = len(self.data)  
                    self.population_mean = sum(self.data) / self.population_size
                    self.render_latex(rf"$\sigma = \sqrt{{\frac{{\sum (x_i - {self.population_mean:.3f})^2}}{{{self.population_size}}}}} = Waiting...$", font_color=self.font_color)
            else:
                self.render_latex(r"$\sigma = \sqrt{\frac{\sum (x_i - \mu)^2}{N}} = Waiting...$", font_color=self.font_color)

    def calculate_function(self):
        try:
            result = self.demon_engine.calculate(self.operation_name, [self.population_mean, self.population_size, self.data])
            self.render_latex(rf"$\sigma = \sqrt{{\frac{{\sum (x_i - {self.population_mean})^2}}{{{self.population_size}}}}} = {result:.4f}$", font_color=self.font_color)
            log = [
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                self.operation_name,
                f"Population Mean : {self.population_mean}, Population Size : {self.population_size}",
                self.data,
                rf"$\sigma = \sqrt{{\frac{{\sum (x_i - {self.population_mean})^2}}{{{self.population_size}}}}} = {result}$"
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
    

            