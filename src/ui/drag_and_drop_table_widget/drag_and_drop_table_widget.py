from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox,QAbstractItemView
from PyQt6.QtGui import QPainter, QColor, QFont
from PyQt6.QtCore import Qt, pyqtSignal
import pandas as pd
from src.logic.table_data_loader.table_data_loader import load_table_data

class DragAndDropTableWidget(QTableWidget):
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
                if  self.df is None:
                    return
                
                rows, columns =  self.df.shape
                self.setRowCount(rows)
                self.setColumnCount(columns)
                self.setHorizontalHeaderLabels( self.df.columns.astype(str))
                self.setVerticalHeaderLabels( self.df.index.astype(str))
                        
                for i in range(rows):
                    for j in range(columns):
                        val =  self.df.iloc[i, j]
                        value = str(val) if pd.notnull(val) else ""
                        self.setItem(i, j, QTableWidgetItem(value))
                
                self.data_loaded.emit(list(self.df.columns))

            except Exception as e:
                QMessageBox.critical(
                    self, 
                    "System Error", 
                    f"Could not populate table: {str(e)}"
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
            if column_name == "All":
                data = self.df
            else:
                data =  self.df[[column_name]]

            rows, columns =  data.shape
            self.setRowCount(rows)
            self.setColumnCount(columns)
            self.setHorizontalHeaderLabels( data.columns.astype(str))
            self.setVerticalHeaderLabels( data.index.astype(str))
                        
            for i in range(rows):
                for j in range(columns):
                    val =  data.iloc[i, j]
                    value = str(val) if pd.notnull(val) else ""
                    self.setItem(i, j, QTableWidgetItem(value))

        except Exception as e:
            return
        
    def pull_colum_data(self,column_name : str) -> list:
        try:
            if column_name == "All":
                return []
            else:
                data = list(self.df[column_name])
                return data
        except Exception as e:
            return