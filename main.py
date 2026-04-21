import sys
from PyQt6.QtWidgets import QApplication, QTabBar, QMessageBox,QWidget
from PyQt6.QtCore import QSettings, Qt,QThreadPool
from src.database.database_manager import DatabaseManager
from src.ui.profile import *
from src.controllers import *
from src.core.task_worker.task_worker import TaskWorker


class AppManager():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.database_manager = DatabaseManager()
        self.database_manager.update_curtain_text_requested.connect(self.handle_update_update_curtain_request)
        self.thread_pool = QThreadPool()

    def run_app(self):
        
        self.init_settings_and_window_controller()

        self.init_docker_and_database()

        sys.exit(self.app.exec())

    def init_settings_and_window_controller(self):
        self.settings_controller = SettingsController()
        saved_user_preferenes = self.settings_controller.get_user_preferences()
        saved_username = self.settings_controller.get_saved_username()
        
        self.window_controller = WindowController(saved_username,saved_user_preferenes,self.settings_controller)
        self.window_controller.preferences_ui_requested.connect(self.init_preferences_controller)
        self.window_controller.about_me_ui_requested.connect(self.init_profile_controller)
        self.window_controller.log_out_requested.connect(self.handle_log_out_request)

        self.window_controller.show_main_ui()
        
    #                   INIT DOCKER AND POSTGRE SERVER
    def init_docker_and_database(self):
        worker = TaskWorker(self.database_manager.start_docker_and_connect_db)
        worker.signals.result.connect(self.init_auth_contoller)
        self.thread_pool.start(worker)
        
    def init_auth_contoller(self, docker_and_db_status : bool):
        if docker_and_db_status:
            self.auth_controller = AuthController(self.database_manager,self.thread_pool,self.settings_controller)
            self.auth_controller.ui_route_requested.connect(self.handle_add_new_tab_request)
            self.auth_controller.login_successful.connect(self.init_library_and_archive_controllers)
            self.auth_controller.update_curtain_text_requested.connect(self.handle_update_update_curtain_request)
            self.auth_controller.check_authentication_token()
        else:
            return

    def init_library_and_archive_controllers(self, username : str, user_preferences, user_records_count : int):
        self.username = username
        self.user_preferences = user_preferences
        self.user_records_count = user_records_count

        self.window_controller.apply_user_preferences(user_preferences)
        self.window_controller.handle_init_profile_menu(self.username)
        
        self.window_controller.handle_clear_tabs()

        self.library_controller = LibraryController()
        self.library_controller.ui_route_requested.connect(self.handle_add_new_tab_request)
        self.library_controller.init_laplaces_library()

        self.archive_controller = ArchiveController(self.database_manager,self.thread_pool,self.username,self.user_records_count)
        self.archive_controller.ui_route_requested.connect(self.handle_add_new_tab_request)
        self.archive_controller.init_laplaces_archive()


    def init_preferences_controller(self):

        self.preferences_controller = PreferencesController(self.database_manager,self.thread_pool,self.settings_controller,self.username,self.user_preferences)
        self.preferences_controller.ui_route_requested.connect(self.handle_add_new_tab_request)

    def init_profile_controller(self):

        self.profile_controller = ProfileController(self.database_manager,self.thread_pool,self.username)
        self.profile_controller.ui_route_requested.connect(self.handle_add_new_tab_request)
        

    def handle_add_new_tab_request(self, widget : QWidget, tab_text : str,tab_id):
        self.window_controller.handle_add_new_tab(widget,tab_text,tab_id)

    
    def handle_log_out_request(self):
        self.auth_controller.handle_revoke_auth_token()
        self.settings_controller.wipe_settings()
        self.window_controller.handle_delete_profile_menu()
        self.window_controller.handle_clear_tabs()
        self.auth_controller.init_login_ui()

    def handle_update_update_curtain_request(self,curtain_text):
        self.window_controller.handle_update_curtain(curtain_text)
        

if __name__ == "__main__":
    manager = AppManager()
    manager.run_app()