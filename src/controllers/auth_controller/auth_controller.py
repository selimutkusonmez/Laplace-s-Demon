from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QObject,pyqtSignal,QSettings,QThreadPool
from src.ui.login_ui import LoginUI
from src.ui.profile.create_new_account.create_new_account_ui import CreateNewAccountUI
from src.core.task_worker.task_worker import TaskWorker

class AuthController(QObject):

    #LoginUISignals
    add_login_ui_tab_requested = pyqtSignal(QWidget, str)
    login_successful = pyqtSignal(str, list, int)

    #CreateNewAccountUISignal
    add_create_new_account_ui_tab_requested = pyqtSignal(QWidget, str)

    #SetCurrentIndexSignal
    set_current_index_requested = pyqtSignal(str)

    #DeleteIndexSignal
    delete_index_requested = pyqtSignal(int)

    #LogOutSignal
    log_out_requested = pyqtSignal()


    def __init__(self,database_manager, threadpool : QThreadPool, settings_controller):
        super().__init__()
        self.database_manager = database_manager
        self.threadpool = threadpool
        self.settings_controller = settings_controller
        self.check_authentication_token()

    #                   LOGIN WITH TOKEN
    def check_authentication_token(self):

        auth_token = self.settings_controller.get_auth_token()
        saved_username = self.settings_controller.get_saved_username()
        remember_me_state = self.settings_controller.get_remember_me_state()
        
        if remember_me_state:
            if auth_token:
                self.username = saved_username
                self.handle_verify_auth_token(saved_username,auth_token)

            else:
                self.init_login_ui()
        else:
            self.init_login_ui()

    def handle_verify_auth_token(self,username, auth_token: str):
        worker = TaskWorker(self.database_manager.verify_auth_token,username,auth_token)
        worker.signals.result.connect(self.process_auth_token)
        self.threadpool.start(worker)

    def process_auth_token(self,db_output : dict):
        success = db_output.get("success")
        preferences = db_output.get("preferences")
        records_count = db_output.get("records_count")

        if success:

            self.login_successful.emit(self.username,preferences,records_count)

        else:
            self.init_login_ui()
            self.login_ui.set_output_text("Authentication Token Expired")

    #                   LOGIN WITHOUT TOKEN
    def init_login_ui(self):
        if hasattr(self, "login_ui"):
            self.set_current_index_requested.emit("login_ui")
        else:
            self.login_ui = LoginUI()
            
            self.login_ui.login_requested.connect(self.handle_login_without_token)
            self.login_ui.create_new_account_requested.connect(self.init_create_new_account_ui)
            
            self.add_login_ui_tab_requested.emit(self.login_ui, "Login UI")

    def handle_login_without_token(self,username : str, password : str,remember_me_state : bool):

        self.username = username
        self.remember_me_state = remember_me_state

        self.login_ui.set_button_enabled(False)

        worker = TaskWorker(self.database_manager.verify_credentials,username,password)
        worker.signals.result.connect(self.process_login_without_token)
        self.threadpool.start(worker)

    def process_login_without_token(self,db_output : dict):
        success = db_output.get("success")
        auth_token = db_output.get("auth_token")
        preferences = db_output.get("preferences")
        records_count = db_output.get("records_count")

        if not success:
            self.login_ui.set_button_enabled(True)
            self.login_ui.set_output_text(db_output.get("error"))

        else:            
            if self.remember_me_state:
                self.settings_controller.save_settings(True,self.username,auth_token)
            else:
                self.settings_controller.wipe_settings()

            self.login_ui.set_button_enabled(True)
            self.login_successful.emit(self.username,preferences,records_count)
    

    #                   CREATE NEW ACCOUNT
    def init_create_new_account_ui(self):
        if hasattr(self,"create_new_account_ui"):
            self.set_current_index_requested.emit("create_new_account_ui")
        else:
            self.create_new_account_ui = CreateNewAccountUI()
            self.create_new_account_ui.setProperty("widget_name","create_new_account_ui")
            self.create_new_account_ui.save_account_info_requested.connect(self.handle_save_account_info)

            self.add_create_new_account_ui_tab_requested.emit(self.create_new_account_ui,"Create New Account")

    def handle_save_account_info(self,username : str, password : str):
        self.create_new_account_ui.set_button_enabled(False)

        worker = TaskWorker(self.database_manager.save_account_info,username,password)
        worker.signals.result.connect(self.process_save_account_info)
        self.threadpool.start(worker)

    def process_save_account_info(self,db_output : str):
        if not hasattr(self,"create_new_account_ui"):
            return
        
        self.create_new_account_ui.set_button_enabled(True)
        self.create_new_account_ui.set_output(db_output)


    #                   LOG OUT
    def handle_log_out(self):
        self.log_out_requested.emit()
        worker = TaskWorker(self.database_manager.revoke_token,self.username)
        self.threadpool.start(worker)
        self.settings_controller.wipe_settings()
        



