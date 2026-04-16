import sys
from PyQt6.QtWidgets import QApplication,QTabBar,QWidget
from PyQt6.QtCore import QSettings
from src.ui import MainUI,LoginUI,LaplaceArchiveUI,DatabaseManager,LaplaceLibraryUI
from src.ui.profile import *

class AppManager():

    def __init__(self):
        self.app = QApplication(sys.argv)
        
    def init_database_manager(self):
        try:
            self.database_manager = DatabaseManager()
            docker_and_db = self.database_manager.start_docker_and_connect_db()
            if docker_and_db:
                self.init_main_ui()
            else:
                return
        except Exception as e:
            print(str(e))

    def init_main_ui(self):


        self.main_ui = MainUI()
        self.main_ui.color_change_requested.connect(self.handle_color_change)
        self.main_ui.log_out_requested.connect(self.handle_relogin)
        self.main_ui.init_preferences_ui_requested.connect(self.handle_init_preferences_ui)
        self.main_ui.init_about_me_ui_requested.connect(self.handle_init_about_me_ui)

        laplace_settings = QSettings("LaplacesDemonOrg", "LaplacesDemon")
        remember_me_state = laplace_settings.value("remember_me", False, type=bool)

        self.login_ui = LoginUI(remember_me_default=remember_me_state)
        self.login_ui.login_requested.connect(self.handle_login)
        self.login_ui.create_new_account_requested.connect(self.handle_create_new_account)

        self.main_ui.central_widget.addTab(self.login_ui,"Login")
        self.main_ui.central_widget.tabBar().setTabButton(0, QTabBar.ButtonPosition.RightSide, None)

        self.main_ui.showMaximized()
        sys.exit(self.app.exec())
    
    def handle_login(self,login_signal):
        self.username = login_signal[0]
        password = login_signal[1]
        remember_me_checkbox_state = login_signal[2]
        login_code = self.database_manager.check_login(self.username,password)

        if login_code == 0:
            self.login_ui.error_space.setText("Invalid Username or Password")

        else:
            settings = QSettings("LaplacesDemonOrg", "LaplacesDemon")
            if remember_me_checkbox_state:
                settings.setValue("remember_me", True)
            else:
                settings.setValue("remember_me", False)

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

            self.login_ui.deleteLater()


    #                   LoginUI & MainUI & DatabaseManager
    def handle_create_new_account(self):
        create_new_account_ui = CreateNewAccountUI()
        create_new_account_ui.save_account_info_requested.connect(self.handle_save_account_info)
        self.main_ui.add_new_tab(create_new_account_ui,"Create An Account")

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


    #                   PreferencesUI & DatabaseManager & MainUI

    #MainUI.preferences_action_function.init_preferences_ui_requested --> AppManager.handle_init_preferences_ui --> DatabaseManager.pull_user_preferences --> PreferencesUI(user_preferences) --> MainUI.add_new_tab
    def handle_init_preferences_ui(self):

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
        for i in range(self.main_ui.central_widget.count()):
            operation_widget = self.main_ui.central_widget.widget(i)
            if hasattr(operation_widget,"change_color"):
                operation_widget.change_color(color_code)

    def handle_preferred_language_update(self, preferred_language : str) -> None:
        print("language main")
        self.database_manager.update_preferred_language(self.username, preferred_language)

    def handle_preferred_theme_update(self, preferred_theme : str) -> None:
        print("theme main")
        self.database_manager.update_preferred_theme(self.username, preferred_theme)

    def handle_preferred_font_color_update(self, preferred_font_color : str) -> None:
        print("font color main")
        self.database_manager.update_preferred_font_color(self.username, preferred_font_color)


    #                   AboutMeUI & DatabaseManager & MainUI

    def handle_init_about_me_ui(self):
        self.about_me_ui = AboutMeUI(self.username)

        self.main_ui.add_new_tab(self.about_me_ui,self.username)


    #                   LoginUI & MainUI
    def handle_relogin(self):
        settings = QSettings("LaplacesDemonOrg", "LaplacesDemon")
        settings.setValue("remember_me", False)
        self.login_ui = LoginUI(remember_me_default=False)
        self.login_ui.login_requested.connect(self.handle_login)
        self.login_ui.create_new_account_requested.connect(self.handle_create_new_account)
        self.main_ui.central_widget.addTab(self.login_ui,"Login")
        self.main_ui.central_widget.tabBar().setTabButton(0, QTabBar.ButtonPosition.RightSide, None)


    #                   LaplaceLibraryUI & MainUI
    def handle_new_operation_request(self,operation_input : list):
        self.new_operation_ui = operation_input[0] # QWidget
        self.new_operation_ui.calculation_success.connect(self.handle_new_archive_record) # calculate button connection
        new_operation_name = operation_input[1] # str
        self.main_ui.add_new_tab(self.new_operation_ui,new_operation_name) # add new_operation_ui to the main_ui.central_widget as a tab

if __name__ == "__main__":
    try:
        manager = AppManager()
        manager.init_database_manager()
    except Exception as e:
        print(str(e))
