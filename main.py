import sys
from PyQt6.QtWidgets import QApplication, QTabBar, QMessageBox,QWidget
from PyQt6.QtCore import QSettings, Qt,QThreadPool
from src.ui import MainUI, LoginUI, LaplaceArchiveUI, DatabaseManager, LaplaceLibraryUI
from src.ui.profile import *
from src.controllers import *


class AppManager():
    def __init__(self):
        self.app = QApplication(sys.argv)
        
    #                   INIT DOCKER AND POSTGRE SERVER
    def init_database_manager(self):
        self.database_manager = DatabaseManager()
        docker_and_db = self.database_manager.start_docker_and_connect_db()
        if docker_and_db:
            self.threadpool = QThreadPool()
            self.settings_controller = SettingsController()
            self.init_window_and_auth_contollers()
            #self.handle_login_with_token()
        else:
            return
        
    def init_window_and_auth_contollers(self):
        self.window_controller = WindowController(self.database_manager,self.threadpool)

        self.auth_controller = AuthController(self.database_manager,self.threadpool,self.settings_controller)

        self.auth_controller.add_login_ui_tab_requested.connect(self.handle_add_new_tab_request)
        self.auth_controller.login_successful.connect(self.init_other_controllers)

        self.auth_controller.add_create_new_account_ui_tab_requested.connect(self.handle_add_new_tab_request)
        
        self.auth_controller.set_current_index_requested.connect(self.handle_set_current_index_request)

    def init_other_controllers(self, username : str, user_preferences, user_recrods_count : int):
        self.archive_controller = ArchiveController(self.database_manager,self.threadpool,username,user_preferences,user_recrods_count)

        self.library_controller = LibraryController(self.database_manager,self.threadpool)

        self.preferenes_controller = PreferencesController(self.database_manager,self.threadpool,username,user_preferences,self.settings_controller)
        
        self.profile_controller = ProfileController(self.database_manager,self.threadpool,username,user_recrods_count)
        

    def handle_add_new_tab_request(self, widget : QWidget, tab_text : str):
        self.window_controller.handle_add_new_tab(widget,tab_text)

    def handle_set_current_index_request(self,tab_property_name : str):
        self.window_controller.handle_set_current_index(tab_property_name)
        
    #                   LOGIN
    def handle_login_with_token(self):
        laplace_settings = QSettings("LaplacesDemonOrg", "LaplacesDemon")
        remember_me_state = laplace_settings.value("remember_me", False, type=bool)
        saved_username = laplace_settings.value("saved_username", "", type=str)
        auth_token = laplace_settings.value("auth_token", "", type=str)
        
        self.username = saved_username

        self.current_user_preferences = self.database_manager.pull_user_preferences(self.username)

        self.main_ui = MainUI(self.current_user_preferences)

        self.main_ui.color_change_requested.connect(self.handle_color_change)
        self.main_ui.log_out_requested.connect(self.handle_relogin)
        self.main_ui.tab_close_requested.connect(self.handle_tab_close)
        self.main_ui.init_preferences_ui_requested.connect(self.handle_init_preferences_ui)
        self.main_ui.init_about_me_ui_requested.connect(self.handle_init_about_me_ui)

        if remember_me_state:
            login_code = self.database_manager.check_token_login(saved_username, auth_token)

            if login_code:
                self.main_ui.init_profile_menu(self.username)
                self.laplace_library_ui = LaplaceLibraryUI(self.current_user_preferences[4])
                self.laplace_library_ui.new_operation_requested.connect(self.handle_new_operation_request)

                self.main_ui.central_widget.addTab(self.laplace_library_ui, "Laplace's Library")
                self.main_ui.central_widget.tabBar().setTabButton(0, QTabBar.ButtonPosition.RightSide, None)

                archive_records_count_on_id = self.database_manager.count_archive_records_on_id(self.username)

                self.laplace_archive_ui = LaplaceArchiveUI(self.username, archive_records_count_on_id, self.current_user_preferences[4])
                self.laplace_archive_ui.archive_records_by_date_requested.connect(self.handle_archive_records_by_date)
                self.laplace_archive_ui.archive_record_data_by_id_requested.connect(self.handle_archive_record_data_by_id)
                self.laplace_archive_ui.init_new_archive_record_ui_requested.connect(self.handle_add_new_archive_record_ui)

                self.main_ui.central_widget.addTab(self.laplace_archive_ui, "Laplace's Archive")
                self.main_ui.central_widget.tabBar().setTabButton(1, QTabBar.ButtonPosition.RightSide, None)

                self.main_ui.showMaximized()
                sys.exit(self.app.exec())
        else:
            self.login_ui = LoginUI(remember_me_default=remember_me_state)
            self.login_ui.login_requested.connect(self.handle_login_without_token)
            self.login_ui.create_new_account_requested.connect(self.handle_create_new_account)

            self.main_ui.central_widget.addTab(self.login_ui,"Login")
            self.main_ui.central_widget.tabBar().setTabButton(0, QTabBar.ButtonPosition.RightSide, None)

            self.main_ui.showMaximized()
            sys.exit(self.app.exec())
        
    def handle_login_without_token(self, login_signal):
        self.login_ui.set_button_enabled(True)

        self.username_attempt = login_signal[0]
        self.password_attempt = login_signal[1]
        self.remember_me_attempt = login_signal[2]

        worker = DatabaseWorker(self.database_manager.check_login, self.username_attempt, self.password_attempt)
        worker.signals.result.connect(self.process_login_result)
        
        self.threadpool.start(worker)

    def process_login_result(self, result):
        self.login_ui.set_button_enabled(False)

        if isinstance(result, str) and result.startswith("Error"):
            self.login_ui.set_output_text("Database Connection Error")
            return

        login_code, auth_token = result

        if not login_code:
            self.login_ui.set_output_text("Invalid Username or Password")
        else:
            self.username = self.username_attempt
            settings = QSettings("LaplacesDemonOrg", "LaplacesDemon")
            
            if self.remember_me_attempt:
                settings.setValue("remember_me", True)
                settings.setValue("saved_username", self.username)
                settings.setValue("auth_token", auth_token)
            else:
                settings.setValue("remember_me", False)
                settings.setValue("saved_username", "")
                settings.setValue("auth_token", "")

            self.main_ui.init_profile_menu(self.username)
            self.current_user_preferences = self.database_manager.pull_user_preferences(self.username)
            
            self.main_ui.central_widget.removeTab(0)

            if self.main_ui.central_widget.tabText(0) == "Create An Account":
                create_new_account_ui_to_delete = self.main_ui.central_widget.widget(0)
                self.main_ui.central_widget.removeTab(0)
                create_new_account_ui_to_delete.deleteLater()

            archive_records_count_on_id = self.database_manager.count_archive_records_on_id(self.username) 

            self.laplace_library_ui = LaplaceLibraryUI()
            self.laplace_library_ui.new_operation_requested.connect(self.handle_new_operation_request) 

            self.main_ui.central_widget.addTab(self.laplace_library_ui, "Laplace's Library")
            self.main_ui.central_widget.tabBar().setTabButton(0, QTabBar.ButtonPosition.RightSide, None)

            self.laplace_archive_ui = LaplaceArchiveUI(self.username, archive_records_count_on_id)
            self.laplace_archive_ui.archive_records_by_date_requested.connect(self.handle_archive_records_by_date) 
            self.laplace_archive_ui.archive_record_data_by_id_requested.connect(self.handle_archive_record_data_by_id) 
            self.laplace_archive_ui.init_new_archive_record_ui_requested.connect(self.handle_add_new_archive_record_ui) 

            self.main_ui.central_widget.addTab(self.laplace_archive_ui, "Laplace's Archive")
            self.main_ui.central_widget.tabBar().setTabButton(1, QTabBar.ButtonPosition.RightSide, None)

            self.main_ui.set_current_user_preferences(self.current_user_preferences)

            self.login_ui.deleteLater()


    #                   CREATE NEW ACCOUNT
    def handle_create_new_account(self):
        if hasattr(self,"create_new_account_ui"):
            for i in range(self.main_ui.central_widget.count()):
                if self.main_ui.central_widget.widget(i).property("widget_name") == "create_new_account_ui":
                    self.main_ui.central_widget.setCurrentIndex(i)
        
        else:
            self.create_new_account_ui = CreateNewAccountUI()
            self.create_new_account_ui.setProperty("widget_name","create_new_account_ui")
            self.create_new_account_ui.save_account_info_requested.connect(self.handle_save_account_info)

            self.main_ui.add_new_tab(self.create_new_account_ui, "Create An Account")

    def handle_save_account_info(self, account_info: list):
        self.create_new_account_ui.set_button_enabled(True)
        worker = DatabaseWorker(self.database_manager.save_account_info,account_info)
        worker.signals.result.connect(self.process_account_info)
        self.threadpool.start(worker)

    def process_account_info(self,db_output : str):
        if not hasattr(self, "create_new_account_ui"):
            return
        self.create_new_account_ui.set_button_enabled(False)
        self.create_new_account_ui.set_output(db_output)


    #                   UPDATE AND PULL ARCHIVE RECORDS
    def handle_new_archive_record(self, new_archive_record_data: list):
        
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
        


    #                   UPDATE PULL AND APPLY PREFERENCES
    def handle_init_preferences_ui(self):
        if hasattr(self, "preferences_ui"):
            for i in range(self.main_ui.central_widget.count()):
                if self.main_ui.central_widget.widget(i).property("widget_name") == "preferences_ui":
                    self.main_ui.central_widget.setCurrentIndex(i)
        else:
            self.preferences_ui = PreferencesUI(self.current_user_preferences)
            self.preferences_ui.setProperty("widget_name","preferences_ui")

            self.preferences_ui.update_preferred_language_requested.connect(self.handle_preferred_language_update)
            self.preferences_ui.update_preferred_language_requested.connect(self.main_ui.change_preferred_language_function)

            self.preferences_ui.update_preferred_theme_requested.connect(self.handle_preferred_theme_update)
            self.preferences_ui.update_preferred_theme_requested.connect(self.main_ui.change_preferred_theme_function)

            self.preferences_ui.update_preferred_font_color_requested.connect(self.handle_preferred_font_color_update)
            self.preferences_ui.update_preferred_font_color_requested.connect(self.main_ui.change_preferred_font_color_function)

            self.main_ui.add_new_tab(self.preferences_ui, "Preferences")

    def handle_color_change(self, color_code: str):
        self.laplace_library_ui.font_color = color_code
        self.laplace_archive_ui.font_color = color_code
        for i in range(self.main_ui.central_widget.count()):
            operation_widget = self.main_ui.central_widget.widget(i)
            if hasattr(operation_widget, "change_color"):
                operation_widget.change_color(color_code)

    def handle_preferred_language_update(self, preferred_language: str) -> None:
        worker = DatabaseWorker(self.database_manager.update_preferred_language,self.username,preferred_language)
        self.threadpool.start(worker)
        
    def handle_preferred_theme_update(self, preferred_theme: str) -> None:
        worker = DatabaseWorker(self.database_manager.update_preferred_theme,self.username,preferred_theme)
        self.threadpool.start(worker)

    def handle_preferred_font_color_update(self, preferred_font_color: str) -> None:
        worker = DatabaseWorker(self.database_manager.update_preferred_font_color,self.username,preferred_font_color)
        self.threadpool.start(worker)


    #                   INIT AND UPDATE ABOUT ME
    def handle_init_about_me_ui(self):
        if hasattr(self, "about_me_ui"):
            for i in range(self.main_ui.central_widget.count()):
                if self.main_ui.central_widget.widget(i).property("widget_name") == "about_me_ui":
                    self.main_ui.central_widget.setCurrentIndex(i)
        else:
            self.about_me_ui = AboutMeUI(self.username, [None for i in range(13)])
            self.about_me_ui.setProperty("widget_name","about_me_ui")
            self.main_ui.add_new_tab(self.about_me_ui, "About Me")

            worker = DatabaseWorker(self.database_manager.pull_user_stats,self.username)
            worker.signals.result.connect(self.process_init_about_me_ui)
            self.threadpool.start(worker)

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
        self.main_ui.add_new_tab(operation_input[0], operation_input[1]) 

if __name__ == "__main__":
    manager = AppManager()
    manager.init_database_manager()