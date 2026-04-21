from PyQt6.QtCore import QObject,pyqtSignal
from PyQt6.QtWidgets import QWidget
from src.ui.profile.about_me.about_me_ui import AboutMeUI
from src.core.task_worker.task_worker import TaskWorker

class ProfileController(QObject):

    ui_route_requested = pyqtSignal(QWidget,str,str)

    def __init__(self,database_manager,thread_pool,username):
        super().__init__()
        self.database_manager = database_manager
        self.thread_pool = thread_pool
        self.username = username

    def handle_pull_user_stats(self):
        worker = TaskWorker(self.database_manager.pull_user_stats,self.username)
        worker.signals.result.connect(self.handle_apply_user_stats)
        self.thread_pool.start(worker)

    def handle_apply_user_stats(self,user_stats):
        self.about_me_ui.fill_user_stats(self.username,user_stats)
    
    def init_about_me_ui(self):
        self.about_me_ui = AboutMeUI()
        self.about_me_ui.setProperty("tab_id","about_me")
        self.handle_pull_user_stats()
        self.ui_route_requested.emit(self.about_me_ui,"About Me","about_me")
