from PyQt6.QtCore import QObject,pyqtSignal
from PyQt6.QtWidgets import QWidget
from src.ui.laplace_library_ui import LaplaceLibraryUI

class LibraryController(QObject):

    ui_route_requested = pyqtSignal(QWidget,str,str)

    def __init__(self):
        super().__init__()

    def init_laplaces_library(self):
        self.laplaces_library = LaplaceLibraryUI()
        self.laplaces_library.setProperty("tab_id","library")
        self.laplaces_library.ui_route_requested.connect(self.handle_new_operation_tab)
        self.ui_route_requested.emit(self.laplaces_library,"Laplace's Library","library")

    def handle_new_operation_tab(self,widget : QWidget, tab_text : str, tab_id : str):
        widget.calculation_success.connect(self.handle_calculation)
        self.ui_route_requested.emit(widget,tab_text,tab_id)

    def handle_calculation(self):
        return

