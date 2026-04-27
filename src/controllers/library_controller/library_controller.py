from PyQt6.QtCore import QObject,pyqtSignal
from PyQt6.QtWidgets import QWidget
from src.ui.laplace_library_ui import LaplaceLibraryUI
from src.core.task_worker.task_worker import TaskWorker

class LibraryController(QObject):

    ui_route_requested = pyqtSignal(QWidget,str,str)

    calculation_successful = pyqtSignal(int, list)

    def __init__(self,database_manager,thread_pool,username,font_color):
        super().__init__()
        self.database_manager = database_manager
        self.thread_pool = thread_pool
        self.username = username
        self.font_color = font_color
        

    def init_laplaces_library(self):
        self.laplaces_library = LaplaceLibraryUI(self.font_color)
        self.laplaces_library.setProperty("tab_id","library")
        self.laplaces_library.ui_route_requested.connect(self.handle_new_operation_tab)
        self.ui_route_requested.emit(self.laplaces_library,"Laplace's Library","library")

    def handle_new_operation_tab(self,widget : QWidget, tab_text : str, tab_id : str):
        widget.calculation_success.connect(self.handle_calculation)
        self.ui_route_requested.emit(widget,tab_text,tab_id)

    def handle_calculation(self, operation_data : list):
        self.operation_data = operation_data
        worker = TaskWorker(self.database_manager.save_archive_record,self.username,operation_data)
        worker.signals.result.connect(self.handle_calculation_success)
        self.thread_pool.start(worker)

    def handle_calculation_success(self,db_id : int):
        self.calculation_successful.emit(db_id,self.operation_data)

    

