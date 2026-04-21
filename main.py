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
        
        self.window_controller = WindowController(saved_user_preferenes,self.settings_controller)
        self.window_controller.preferences_ui_requested.connect(self.init_preferences_controller)
        self.window_controller.about_me_ui_requested.connect(self.init_profile_controller)
        self.window_controller.log_out_requested.connect(self.handle_log_out_request)

        self.window_controller.show_main_ui()
        
    #                   INIT DOCKER AND POSTGRE SERVER
    def init_docker_and_database(self):
        worker = TaskWorker(self.database_manager.start_docker_and_connect_db)
        worker.signals.result.connect(self.init_auth_contoller)
        self.thread_pool.start(worker)
        
    def init_auth_contoller(self, docer_and_db_status : bool):
        if docer_and_db_status:
            self.auth_controller = AuthController(self.database_manager,self.thread_pool,self.settings_controller)
            self.auth_controller.ui_route_requested.connect(self.handle_add_new_tab_request)
            self.auth_controller.login_successful.connect(self.init_library_and_archive_controllers)
            self.auth_controller.update_curtain_text_requested.connect(self.handle_update_update_curtain_request)
        else:
            return

    def init_library_and_archive_controllers(self, username : str, user_preferences, user_records_count : int):
        self.username = username
        self.user_preferences = user_preferences
        self.user_records_count = user_records_count

        self.window_controller.apply_user_preferences(user_preferences)
        
        self.window_controller.handle_clear_tabs()

        self.library_controller = LibraryController(self.database_manager,self.thread_pool)
        self.library_controller.ui_route_requested.connect(self.handle_add_new_tab_request)

        self.archive_controller = ArchiveController(self.database_manager,self.thread_pool,self.username,self.user_preferences,self.user_records_count)
        self.archive_controller.ui_route_requested.connect(self.handle_add_new_tab_request)

    def init_preferences_controller(self):

        self.preferences_controller = PreferencesController(self.database_manager,self.thread_pool,self.settings_controller,self.username,self.user_preferences)
        self.preferences_controller.ui_route_requested.connect(self.handle_add_new_tab_request)

    def init_profile_controller(self):

        self.profile_controller = ProfileController(self.database_manager,self.thread_pool,self.username)
        self.profile_controller.ui_route_requested.connect(self.handle_add_new_tab_request)
        

    def handle_add_new_tab_request(self, widget : QWidget, tab_text : str):
        print(widget)
        print(tab_text)
        self.window_controller.handle_add_new_tab(widget,tab_text)

    
    def handle_log_out_request(self):
        self.window_controller.handle_clear_tabs()
        self.auth_controller.init_login_ui()

    def handle_update_update_curtain_request(self,curtain_text):
        self.window_controller.handle_update_curtain(curtain_text)
        

    #                   UPDATE AND PULL ARCHIVE RECORDS
    """def handle_new_archive_record(self, new_archive_record_data: list):
        
        worker = DatabaseWorker(self.database_manager.save_archive_record,self.username,new_archive_record_data)
        worker.signals.result.connect(lambda result, data=new_archive_record_data: self.process_new_archive_record(result, data))
        self.threadpool.start(worker)
        
    def process_new_archive_record(self,new_record_data_db_id,new_archive_record_data):
        if not hasattr(self, "laplace_archive_ui"):
            return
        self.laplace_archive_ui.add_new_archive_record(new_record_data_db_id, new_archive_record_data)


    def handle_archive_records_by_date(self, operation_data_date: list):
        self.laplace_archive_ui.set_button_enabled(True)
        worker = DatabaseWorker(self.database_manager.return_archive_records_by_date,self.username,operation_data_date)
        worker.signals.result.connect(self.process_archive_records_by_date)
        self.threadpool.start(worker)

    def process_archive_records_by_date(self,archive_records_by_date):
        if not hasattr(self, "laplace_archive_ui"):
            return
        self.laplace_archive_ui.set_button_enabled(False)
        self.laplace_archive_ui.list_archive_records_by_date(archive_records_by_date)
    

    def handle_archive_record_data_by_id(self, db_id: str):
        for i in range(self.main_ui.central_widget.count()):
            if self.main_ui.central_widget.tabText(i).endswith(f"(ID : {db_id})"):
                self.main_ui.central_widget.setCurrentIndex(i)
                return
        worker = DatabaseWorker(self.database_manager.return_archive_record_data_by_id,db_id)
        worker.signals.result.connect(self.process_archive_record_data_by_id)
        self.threadpool.start(worker)        
    
    def process_archive_record_data_by_id(self,archive_record_data_by_id):
        self.laplace_archive_ui.init_new_archive_record_ui(archive_record_data_by_id)


    def handle_add_new_archive_record_ui(self, history_input: list):
        self.main_ui.add_new_tab(history_input[0], history_input[1])


    def handle_update_laplace_archive_ui(self):
        worker = DatabaseWorker(self.database_manager.count_archive_records_on_id,self.username)
        worker.signals.result.connect(self.process_update_laplace_archive_ui)
        self.threadpool.start(worker)

    def process_update_laplace_archive_ui(self,archive_records_count_on_id):
        if not hasattr(self,"laplace_archive_ui"):
            return
        self.laplace_archive_ui.update_laplace_arhcive_records_count(archive_records_count_on_id)
        



    def handle_color_change(self, color_code: str):
        self.laplace_library_ui.font_color = color_code
        self.laplace_archive_ui.font_color = color_code
        for i in range(self.main_ui.central_widget.count()):
            operation_widget = self.main_ui.central_widget.widget(i)
            if hasattr(operation_widget, "change_color"):
                operation_widget.change_color(color_code)


    def process_init_about_me_ui(self,current_user_stats):
        if hasattr(self,"about_me_ui"):
            self.about_me_ui.fill_user_stats(self.username,current_user_stats)

    def handle_update_about_me_ui(self):
        if hasattr(self, "about_me_ui"):
            worker = DatabaseWorker(self.database_manager.pull_user_stats,self.username)
            worker.signals.result.connect(self.process_update_about_me_ui)
            self.threadpool.start(worker)            
        else:
            return
        
    def process_update_about_me_ui(self,current_user_stats):
        if not hasattr(self,"about_me_ui"):
            return
        self.about_me_ui.fill_user_stats(self.username, current_user_stats)

    #                   RELOGIN
    def handle_relogin(self):
        ui_singletons = [
            "preferences_ui", 
            "about_me_ui", 
            "laplace_library_ui", 
            "laplace_archive_ui", 
            "login_ui"
        ]
        
        for ui_name in ui_singletons:
            if hasattr(self, ui_name):
                delattr(self, ui_name)

        while self.main_ui.central_widget.count() > 0:
            widget = self.main_ui.central_widget.widget(0)
            self.main_ui.central_widget.removeTab(0)
            if widget is not None:
                widget.deleteLater()

        if hasattr(self.main_ui, 'profile_button') and self.main_ui.profile_button is not None:
            self.main_ui.menuBar().setCornerWidget(None, Qt.Corner.TopRightCorner)
            self.main_ui.profile_button.deleteLater()

        settings = QSettings("LaplacesDemonOrg", "LaplacesDemon")
        settings.setValue("remember_me", False)
        settings.setValue("saved_username", "")
        settings.setValue("auth_token", "")

        worker = DatabaseWorker(self.database_manager.revoke_token,self.username)
        self.threadpool.start(worker)
        self.username = None

        self.login_ui = LoginUI(remember_me_default=False)
        self.login_ui.login_requested.connect(self.handle_login_without_token)
        self.login_ui.create_new_account_requested.connect(self.handle_create_new_account)

        self.main_ui.central_widget.addTab(self.login_ui, "Login")
        self.main_ui.central_widget.tabBar().setTabButton(0, QTabBar.ButtonPosition.RightSide, None)


    #                   TAB CLOSE
    def handle_tab_close(self, index: int):
        widget = self.main_ui.central_widget.widget(index)
        
        if hasattr(widget, "is_dirty") and widget.is_dirty:
            verdict = QMessageBox.warning(
                self.main_ui,
                "Unsaved Data",
                "This tab contains uncalculated input. Are you sure you want to close it?",
                QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Cancel
            )
            
            if verdict == QMessageBox.StandardButton.Cancel:
                return

        try:
            if widget is self.preferences_ui:
                delattr(self, "preferences_ui")
        except AttributeError:
            pass

        try:
            if widget is self.about_me_ui:
                delattr(self, "about_me_ui")
        except AttributeError:
            pass

        self.main_ui.central_widget.removeTab(index)
        widget.deleteLater()


    #                   ADD NEW OPERATION
    def handle_new_operation_request(self, operation_input: list):
        operation_input[0].calculation_success.connect(self.handle_new_archive_record) 
        operation_input[0].calculation_success.connect(self.handle_update_about_me_ui) 
        operation_input[0].calculation_success.connect(self.handle_update_laplace_archive_ui)
        self.main_ui.add_new_tab(operation_input[0], operation_input[1]) """

if __name__ == "__main__":
    manager = AppManager()
    manager.run_app()