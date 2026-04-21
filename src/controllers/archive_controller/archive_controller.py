from PyQt6.QtCore import QObject,pyqtSignal
from PyQt6.QtWidgets import QWidget
from src.ui.laplace_archive_ui import LaplaceArchiveUI
from src.core.task_worker.task_worker import TaskWorker

class ArchiveController(QObject):

    ui_route_requested = pyqtSignal(QWidget, str,str)

    change_tab_requested = pyqtSignal(str)

    def __init__(self,database_manager,thread_pool,username,user_records_count):
        super().__init__()
        self.database_manager = database_manager
        self.thread_pool = thread_pool
        self.username = username
        self.user_records_count = user_records_count

    def init_laplaces_archive(self):
        self.laplaces_archive = LaplaceArchiveUI(self.username,self.user_records_count)
        self.laplaces_archive.setProperty("tab_id","archive")
        self.laplaces_archive.ui_route_requested.connect(self.ui_route_requested)
        self.laplaces_archive.archive_records_by_date_requested.connect(self.handle_archive_records_by_date)
        self.laplaces_archive.archive_record_data_by_id_requested.connect(self.handle_archive_record_data_by_id)

        self.ui_route_requested.emit(self.laplaces_archive,"Laplace's Archive","archive")

    def handle_archive_records_by_date(self, start_date : str, end_date : str,):
        self.laplaces_archive.set_button_enabled(False)
        worker = TaskWorker(self.database_manager.return_archive_records_by_date,self.username,start_date,end_date)
        worker.signals.result.connect(self.process_archive_records_by_date)
        self.thread_pool.start(worker)

    def process_archive_records_by_date(self,archive_records_by_date):
        if not hasattr(self, "laplaces_archive"):
            return
        self.laplaces_archive.set_button_enabled(True)
        self.laplaces_archive.list_archive_records_by_date(archive_records_by_date)

    def handle_archive_record_data_by_id(self, db_id: str):
        worker = TaskWorker(self.database_manager.return_archive_record_data_by_id,db_id)
        worker.signals.result.connect(self.process_archive_record_data_by_id)
        self.thread_pool.start(worker)        
    
    def process_archive_record_data_by_id(self,archive_record_data_by_id):
        self.laplaces_archive.init_new_archive_record_ui(archive_record_data_by_id)
        

