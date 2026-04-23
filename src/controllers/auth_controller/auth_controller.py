from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QObject,pyqtSignal,QThreadPool,QTimer
from src.ui.login_ui import LoginUI
from src.ui.profile.create_new_account.create_new_account_ui import CreateNewAccountUI
from src.core.task_worker.task_worker import TaskWorker

class AuthController(QObject):

    #Universal UIRouteRequestedSignal
    ui_route_requested = pyqtSignal(QWidget, str, str)

    #LoginSuccessfulSignal
    login_successful = pyqtSignal(str, list, int,bool,str)

    curtain_text_update_requested = pyqtSignal(str)


    def __init__(self,database_manager, thread_pool : QThreadPool, settings_controller):
        super().__init__()
        self.database_manager = database_manager
        self.thread_pool = thread_pool
        self.settings_controller = settings_controller

    #                   LOGIN WITH TOKEN
    def check_authentication_token(self):
        self.curtain_text_update_requested.emit("Checking Auth Token...")
        QTimer.singleShot(1000, self.verify_local_settings)

    def verify_local_settings(self):
        self.auth_token = self.settings_controller.get_auth_token()
        saved_username = self.settings_controller.get_saved_username()
        remember_me_state = self.settings_controller.get_remember_me_state()
        if remember_me_state:
            if self.auth_token:
                self.username = saved_username
                self.curtain_text_update_requested.emit("Auth Token Found")
                QTimer.singleShot(1000, lambda: self.handle_verify_auth_token(saved_username, self.auth_token))
            else:
                self.curtain_text_update_requested.emit("Auth Token Could Not Be Found")
                QTimer.singleShot(1000, self.init_login_ui)
        else:
            self.curtain_text_update_requested.emit("Auth Token Could Not Be Found")
            QTimer.singleShot(1000, self.init_login_ui)

    def handle_verify_auth_token(self, username : str, auth_token: str):
        self.curtain_text_update_requested.emit("Verifying Auth Token...")
        QTimer.singleShot(1000, lambda: self.dispatch_auth_worker(username, auth_token))

    def dispatch_auth_worker(self, username : str, auth_token: str):
        worker = TaskWorker(self.database_manager.verify_auth_token, username, auth_token)
        worker.signals.result.connect(self.process_auth_token)
        self.thread_pool.start(worker)

    def process_auth_token(self, db_output: dict):
        success = db_output.get("success")
        preferences = db_output.get("preferences")
        records_count = db_output.get("records_count")

        if success:
            self.curtain_text_update_requested.emit("Login Successful")
            QTimer.singleShot(1000, lambda: self.login_successful.emit(self.username, preferences, records_count,True,self.auth_token))
        else:
            self.curtain_text_update_requested.emit("Authentication Token Expired")
            QTimer.singleShot(1000, self.init_login_ui)

    #                   LOGIN WITHOUT TOKEN
    def init_login_ui(self):
        if hasattr(self, "login_ui"):
            del self.login_ui
            self.init_login_ui()
        else:
            self.login_ui = LoginUI()
            
            self.login_ui.login_requested.connect(self.handle_login_without_token)
            self.login_ui.create_new_account_requested.connect(self.init_create_new_account_ui)
            
            self.ui_route_requested.emit(self.login_ui, "Login","login")

    def handle_login_without_token(self,username : str, password : str,remember_me_state : bool):

        self.username = username
        self.remember_me_state = remember_me_state

        self.login_ui.set_button_enabled(False)

        worker = TaskWorker(self.database_manager.verify_credentials,username,password)
        worker.signals.result.connect(self.process_login_without_token)
        self.thread_pool.start(worker)

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
                self.settings_controller.save_settings(True,self.username,auth_token,preferences)
            else:
                self.settings_controller.wipe_settings()

            self.login_ui.set_button_enabled(True)
            self.login_successful.emit(self.username,preferences,records_count,self.remember_me_state,auth_token)

            del self.login_ui
    
    def handle_revoke_auth_token(self):
        worker = TaskWorker(self.database_manager.revoke_token,self.username)
        self.thread_pool.start(worker)

    #                   CREATE NEW ACCOUNT
    def init_create_new_account_ui(self):
        if hasattr(self,"create_new_account_ui"):
            self.ui_route_requested.emit(None,"create_new_account_ui")
        else:
            self.create_new_account_ui = CreateNewAccountUI()
            self.create_new_account_ui.setProperty("widget_name","create_new_account_ui")
            self.create_new_account_ui.save_account_info_requested.connect(self.handle_save_account_info)

            self.ui_route_requested.emit(self.create_new_account_ui,"Create New Account","create_new_account")
            
    def handle_save_account_info(self,username : str, password : str):
        self.create_new_account_ui.set_button_enabled(False)

        worker = TaskWorker(self.database_manager.save_account_info,username,password)
        worker.signals.result.connect(self.process_save_account_info)
        self.thread_pool.start(worker)

    def process_save_account_info(self,db_output : str):
        if not hasattr(self,"create_new_account_ui"):
            return
        
        self.create_new_account_ui.set_button_enabled(True)
        self.create_new_account_ui.set_output(db_output)

    



