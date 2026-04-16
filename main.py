import sys
from PyQt6.QtWidgets import QApplication,QTabBar,QWidget,QMessageBox
from PyQt6.QtCore import QSettings
from src.ui import MainUI,LoginUI,LaplaceArchiveUI,DatabaseManager,LaplaceLibraryUI
from src.ui.profile import *

class AppManager():

    def __init__(self):
        self.app = QApplication(sys.argv)
        
    def init_database_manager(self):
            self.database_manager = DatabaseManager()
            docker_and_db = self.database_manager.start_docker_and_connect_db()
            if docker_and_db:
                self.handle_login_with_token()
            else:
                return


    def handle_login_with_token(self):

        laplace_settings = QSettings("LaplacesDemonOrg", "LaplacesDemon")
        remember_me_state = laplace_settings.value("remember_me", False, type=bool)
        saved_username = laplace_settings.value("saved_username", "", type=str)
        self.username = saved_username
        auth_token = laplace_settings.value("auth_token", "", type=str)

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
                self.laplace_library_ui = LaplaceLibraryUI(self.current_user_preferences[3])
                self.laplace_library_ui.new_operation_requested.connect(self.handle_new_operation_request)

                self.main_ui.central_widget.addTab(self.laplace_library_ui, "Laplace's Library")
                self.main_ui.central_widget.tabBar().setTabButton(0, QTabBar.ButtonPosition.RightSide, None)

                archive_records_count_on_id = self.database_manager.count_archive_records_on_id(self.username)

                self.laplace_archive_ui = LaplaceArchiveUI(self.username, archive_records_count_on_id,self.current_user_preferences[3])
                self.laplace_archive_ui.archive_records_by_date_requested.connect(self.hanlde_archive_records_by_date)
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
        
    
    def handle_login_without_token(self,login_signal):
        self.username = login_signal[0]
        password = login_signal[1]
        remember_me_checkbox_state = login_signal[2]
        login_code, auth_token = self.database_manager.check_login(self.username,password)

        if not login_code:
            self.login_ui.error_space.setText("Invalid Username or Password")

        else:
            settings = QSettings("LaplacesDemonOrg", "LaplacesDemon")
            if remember_me_checkbox_state:
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

            archive_records_count_on_id = self.database_manager.count_archive_records_on_id(self.username) # We ask DatabaseManager how many logs under the name of self.username

            self.laplace_library_ui = LaplaceLibraryUI()
            self.laplace_library_ui.new_operation_requested.connect(self.handle_new_operation_request) # when a operation name is doubleclicked on the list take the name import the ui and emit Qwidget and the name

            self.main_ui.central_widget.addTab(self.laplace_library_ui,"Laplace's Library")
            self.main_ui.central_widget.tabBar().setTabButton(0, QTabBar.ButtonPosition.RightSide, None)

            self.laplace_archive_ui = LaplaceArchiveUI(self.username,archive_records_count_on_id)
            self.laplace_archive_ui.archive_records_by_date_requested.connect(self.hanlde_archive_records_by_date) # when user asks for a spesific date log or a range of date
            self.laplace_archive_ui.archive_record_data_by_id_requested.connect(self.handle_archive_record_data_by_id) # when a log is doubleclicked take information
            self.laplace_archive_ui.init_new_archive_record_ui_requested.connect(self.handle_add_new_archive_record_ui) #create history_ui and send it to the appmanager

            self.main_ui.central_widget.addTab(self.laplace_archive_ui,"Laplace's Archive")
            self.main_ui.central_widget.tabBar().setTabButton(1, QTabBar.ButtonPosition.RightSide, None)

            self.main_ui.set_current_user_preferences(self.current_user_preferences)

            self.login_ui.deleteLater()


    #                   LoginUI & MainUI & DatabaseManager
    def handle_create_new_account(self):
        if hasattr(self,"create_new_account_ui"):
            return
        else:
            self.create_new_account_ui = CreateNewAccountUI()
            self.create_new_account_ui.save_account_info_requested.connect(self.handle_save_account_info)
            self.main_ui.add_new_tab(self.create_new_account_ui,"Create An Account")

    def handle_save_account_info(self,create_new_account_ui_reference : QWidget,account_info : list):
        db_output = self.database_manager.save_account_info(account_info)
        create_new_account_ui_reference.output.setText(db_output)


    #                   LaplaceArchiveUI & DatabaseManager
    def handle_new_archive_record(self,new_archive_record_data : list):
        new_archive_record_db_id = self.database_manager.save_archive_record(self.username,new_archive_record_data) # log is saved in the db and db_id is returned for logs_ui
        self.laplace_archive_ui.add_new_archive_record(new_archive_record_db_id,new_archive_record_data) # when a calculation is done in the operation_ui all the variables is sent to the logs_ui

    def hanlde_archive_records_by_date(self,operation_data_date : list):
        archive_records_by_date = self.database_manager.return_archive_records_by_date(self.username,operation_data_date) # select * from history where date between operation_data_date
        self.laplace_archive_ui.list_archive_records_by_date(archive_records_by_date) # show logs within the logs_list
    
    def handle_archive_record_data_by_id(self,db_id : str):
        archive_record_data_by_id = self.database_manager.return_archive_record_data_by_id(db_id) # select * from history where id = ?
        self.laplace_archive_ui.init_new_archive_record_ui(archive_record_data_by_id) # take operation_data_by_id and give it to history_ui

    def handle_add_new_archive_record_ui(self,history_input : list):
        new_archive_record_ui = history_input[0] # QWidget
        new_archive_record_name = history_input[1] # str
        self.main_ui.add_new_tab(new_archive_record_ui,new_archive_record_name) # add new_history_ui to the main_ui.central_widget as a tab

    def handle_update_laplace_archive_ui(self):
        self.laplace_archive_ui.update_laplace_arhcive_records_count()

    #                   PreferencesUI & DatabaseManager & MainUI

    #MainUI.preferences_action_function.init_preferences_ui_requested --> AppManager.handle_init_preferences_ui --> DatabaseManager.pull_user_preferences --> PreferencesUI(user_preferences) --> MainUI.add_new_tab
    def handle_init_preferences_ui(self):
        if hasattr(self,"preferences_ui"):
            return
        else:

            self.preferences_ui = PreferencesUI(self.current_user_preferences)

            self.preferences_ui.update_preferred_language_requested.connect(self.handle_preferred_language_update)
            self.preferences_ui.update_preferred_language_requested.connect(self.main_ui.change_preferred_language_function)

            self.preferences_ui.update_preferred_theme_requested.connect(self.handle_preferred_theme_update)
            self.preferences_ui.update_preferred_theme_requested.connect(self.main_ui.change_preferred_theme_function)

            self.preferences_ui.update_preferred_font_color_requested.connect(self.handle_preferred_font_color_update)
            self.preferences_ui.update_preferred_font_color_requested.connect(self.main_ui.change_preferred_font_color_function)

            self.main_ui.add_new_tab(self.preferences_ui,"Preferences")

    def handle_color_change(self,color_code : str):
        self.laplace_library_ui.font_color = color_code
        self.laplace_archive_ui.font_color = color_code
        for i in range(self.main_ui.central_widget.count()):
            operation_widget = self.main_ui.central_widget.widget(i)
            if hasattr(operation_widget,"change_color"):
                operation_widget.change_color(color_code)

    def handle_preferred_language_update(self, preferred_language : str) -> None:
        self.database_manager.update_preferred_language(self.username, preferred_language)

    def handle_preferred_theme_update(self, preferred_theme : str) -> None:
        self.database_manager.update_preferred_theme(self.username, preferred_theme)

    def handle_preferred_font_color_update(self, preferred_font_color : str) -> None:
        self.database_manager.update_preferred_font_color(self.username, preferred_font_color)


    #                   AboutMeUI & DatabaseManager & MainUI

    #MainUI.about_me_action_function --> AppManager.handle_init_about_me_ui --> DatabaseManager.pull_user_stats --> AboutMeUI(current_user_stats)
    def handle_init_about_me_ui(self):
        if hasattr(self,"about_me_ui"):
            return
        else:
            current_user_stats = self.database_manager.pull_user_stats(self.username)
            self.about_me_ui = AboutMeUI(self.username,current_user_stats)

            self.main_ui.add_new_tab(self.about_me_ui,self.username)

    #OperationUI.calculation_success --> AppManager.handle_update_about_me_ui --> AboutMeUI.fill_user_stats(current_user_stats)
    def handle_update_about_me_ui(self):
        if hasattr(self,"about_me_ui"):
            current_user_stats = self.database_manager.pull_user_stats(self.username)
            self.about_me_ui.fill_user_stats(self.username,current_user_stats)
        else:
            return

    #                   LoginUI & MainUI
    def handle_relogin(self):
        settings = QSettings("LaplacesDemonOrg", "LaplacesDemon")
        settings.setValue("remember_me", False)
        settings.setValue("saved_username", "")
        settings.setValue("auth_token", "")

        self.database_manager.revoke_token(self.username)
        self.username = None

        self.login_ui = LoginUI(remember_me_default=False)
        self.login_ui.login_requested.connect(self.handle_login_without_token)
        self.login_ui.create_new_account_requested.connect(self.handle_create_new_account)

        self.main_ui.central_widget.addTab(self.login_ui,"Login")
        self.main_ui.central_widget.tabBar().setTabButton(0, QTabBar.ButtonPosition.RightSide, None)


    #                   OperationUI & MainUI

    #MainUI.central_widget_tab_close_function.tab_close_requested --> AppManager.handle_tab_close
    def handle_tab_close(self, index : int):
        widget = self.main_ui.central_widget.widget(index)
        
        if hasattr(widget, "is_dirty") and widget.is_dirty:
            verdict = QMessageBox.warning(
                self.main_ui,
                "Unsaved Data",
                "This tab contains uncalculated input. Are you sure you want to close it?",
                QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Cancel
            )
            
            if verdict == QMessageBox.StandardButton.Discard:
                self.main_ui.central_widget.removeTab(index)
                widget.deleteLater()
            elif verdict == QMessageBox.StandardButton.Cancel:
                return
        else:
            self.main_ui.central_widget.removeTab(index)
            widget.deleteLater()

    #                   LaplaceLibraryUI & MainUI
    def handle_new_operation_request(self,operation_input : list):
        self.new_operation_ui = operation_input[0] # QWidget
        self.new_operation_ui.calculation_success.connect(self.handle_new_archive_record) # calculate button connection
        self.new_operation_ui.calculation_success.connect(self.handle_update_about_me_ui) # calculate button connection
        self.new_operation_ui.calculation_success.connect(self.handle_update_laplace_archive_ui)
        new_operation_name = operation_input[1] # str
        self.main_ui.add_new_tab(self.new_operation_ui,new_operation_name) # add new_operation_ui to the main_ui.central_widget as a tab

if __name__ == "__main__":
        manager = AppManager()
        manager.init_database_manager()
