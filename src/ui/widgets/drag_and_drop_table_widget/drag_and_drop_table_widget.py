from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox,QAbstractItemView,QTableView
from PyQt6.QtGui import QPainter, QColor, QFont
from PyQt6.QtCore import Qt, pyqtSignal
import pandas as pd
from src.logic.table_data_loader.table_data_loader import load_table_data
from src.ui.widgets.drag_and_drop_table_widget.table_model.table_model import TableModel

class DragAndDropTableView(QTableView):
    data_loaded = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.is_dragging = False
        QAbstractItemView.EditTrigger.NoEditTriggers

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            self.is_dragging = True
            event.accept()
            self.viewport().update()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.is_dragging = False
        self.viewport().update()

    def dropEvent(self, event):
        self.is_dragging = False
        self.viewport().update()
        
        files = event.mimeData().urls()
        if files:
            file_path = files[0].toLocalFile()
            
            try:
                self.df = load_table_data(file_path, self)
                if self.df is None:
                    return
                
                else:
                    table_model = TableModel(self.df)
                    
                    self.setModel(table_model)
                    
                    self.data_loaded.emit(list(self.df.columns))

            except Exception as e:
                QMessageBox.warning(
                    self, 
                    "System Error", 
                    "Could not populate table"
                )

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.is_dragging:
            painter = QPainter(self.viewport())
            painter.setBrush(QColor(182, 112, 50, 100)) 
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(self.viewport().rect())

            painter.setPen(QColor("white"))
            painter.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
            painter.drawText(
                self.viewport().rect(), 
                Qt.AlignmentFlag.AlignCenter, 
                "DROP INPUT DATA HERE"
            )
            painter.end()

    
    # OperationUI.column_picker.currentText() --> DragAndDropTableWidget.load_column_data
    def load_column_data(self,column_name : str):
        try:

            #If column_picker.currentText() = "All" show all data
            if column_name == "All":
                data = self.df
            else:
                #If null in data
                if self.df[column_name].isnull().any():
                            QMessageBox.warning(
                                    self,
                                    "Invalid Data",
                                    f"Error: The column '{column_name}' contains null data and cannot be used for mathematical operations."
                                )
                #If text data in data
                elif not pd.api.types.is_numeric_dtype(self.df[column_name]):
                                QMessageBox.warning(
                                    self,
                                    "Invalid Data",
                                    f"Error: The column '{column_name}' contains text and cannot be used for mathematical operations."
                                )
                                
                data = self.df[[column_name]]
                

            table_model = TableModel(data)
            self.setModel(table_model)

        except Exception as e:
                QMessageBox.warning(
                    self,
                    "System Error",
                    "An unexpected error occurred while loading the column"
                )
        
    def pull_colum_data(self,column_name : str) -> list:
        try:
            #If column_picker.currentText() = "All" return empty list
            if column_name == "All":
                return []
            else:
                #Make python list from column_data
                data = list(self.df[column_name])
                #If text data in column_data return empty list
                if self.df[column_name].isnull().any():
                    return []
                elif not pd.api.types.is_numeric_dtype(self.df[column_name]):
                    return []
                else:
                    return data
        except:
            return