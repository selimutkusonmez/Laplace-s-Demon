from PyQt6.QtWidgets import QTableWidget,QTableWidgetItem,QMessageBox
from PyQt6.QtGui import QPainter, QColor, QFont
from PyQt6.QtCore import Qt,pyqtSignal
import pandas as pd
from src.logic.table_data_reader.data_reader import read_data

class DragAndDropTableWidget(QTableWidget):
    data_loaded = pyqtSignal(list)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.is_dragging = False #

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            self.is_dragging = True
            event.accept()
            self.update()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.is_dragging = False
        self.update()

    def dropEvent(self, event):
        self.is_dragging = False
        self.update()
        
        files = event.mimeData().urls()
        if files:
            file_path = files[0].toLocalFile()
            
            try:
                df = read_data(file_path,self)
                if df is None:
                    return
                rows,columns = df.shape
                self.setRowCount(rows)
                self.setColumnCount(columns)
                self.setHorizontalHeaderLabels(df.columns.astype(str))
                self.setVerticalHeaderLabels(df.index.astype(str))
                        
                for i in range(rows):
                        for j in range(columns):
                            value = str(df.iloc[i, j]) if pd.notnull(df.iloc[i, j]) else ""
                            self.setItem(i, j, QTableWidgetItem(value))
                            
                self.data_loaded.emit(list(df.columns))

            except Exception as e:
                QMessageBox.critical(
                    self, 
                    "System Error", 
                    f"Could not make table: {str(e)}")
                return None

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