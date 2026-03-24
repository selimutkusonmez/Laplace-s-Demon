from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtGui import QPainter, QColor, QFont
from PyQt6.QtCore import Qt
from src.logic.text_data_loader.text_data_loader import load_text_data

class DragAndDropTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.is_dragging = False #
        self.setPlaceholderText("The data : numbers separated by commas")
        self.setToolTip("The data must contain only numbers separated by commas or newlines.")
        self.setToolTipDuration(4000)

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
            
            self.setText(load_text_data(file_path,self))

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


    def pull_text_data(self):
        try:
            #Get text from self
            text = self.toPlainText()

            #Replace newlines with commas
            text = text.replace("\n",",")
            #Split data by comma
            raw_items = text.split(",")
            
            #Float data
            valid_numbers = []
            for item in raw_items:
                cleaned_item = item.strip()
                if cleaned_item:
                    valid_numbers.append(float(cleaned_item))
            
            return valid_numbers
        
        except ValueError:
            return None

