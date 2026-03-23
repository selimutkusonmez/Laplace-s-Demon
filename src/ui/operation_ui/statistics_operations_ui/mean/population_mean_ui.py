from PyQt6.QtWidgets import QMessageBox
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

    

            