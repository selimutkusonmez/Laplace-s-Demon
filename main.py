import sys
from PyQt6.QtWidgets import QApplication,QTabBar
from src.ui import MainUI,LoginUI,OperationHistoryUI,DatabaseManager,OperationsListingUI

class AppManager():
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.main_ui = MainUI()
        self.main_ui.color_change_requested.connect(self.handle_color_change)
        self.main_ui.log_out_requested.connect(self.handle_relogin)
        self.main_ui.change_preferred_language_request.connect(self.handle_preferred_language_change)
        self.main_ui.change_preferred_theme_request.connect(self.handle_preferred_theme_change)
        self.main_ui.change_preferred_font_color_request.connect(self.handle_preffered_font_color_change)

        self.login_ui = LoginUI()
        self.login_ui.login_signal.connect(self.handle_login)
        
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

        self.main_ui.central_widget.addTab(self.login_ui,"Login")
        self.main_ui.central_widget.tabBar().setTabButton(0, QTabBar.ButtonPosition.RightSide, None)

        self.main_ui.showMaximized()
        sys.exit(self.app.exec())
    
    def handle_login(self,login_signal):
        self.username = login_signal[0]
        password = login_signal[1]
        login_code = self.database_manager.check_login(self.username,password)

        if login_code == 0:
            self.login_ui.error_space.setText("Invalid Username or Password")

        else:
            self.main_ui.init_profile_menu(self.username)
            
            self.main_ui.central_widget.removeTab(0)

            self.operation_data_count = self.database_manager.count_operation_data(self.username) # We ask DatabaseManager how many logs under the name of self.username
            self.operation_history_ui = OperationHistoryUI(self.username,self.operation_data_count)
            self.operation_history_ui.create_history_requested.connect(self.handle_create_new_history) #create history_ui and send it to the appmanager
            self.operation_history_ui.operation_data_by_id_requested.connect(self.handle_operation_data_by_id) # when a log is doubleclicked take information
            self.operation_history_ui.operation_data_by_date_requested.connect(self.handle_logs_by_date) # when user asks for a spesific date log or a range of date

            self.operations_listing_ui = OperationsListingUI()
            self.operations_listing_ui.new_operation_requested.connect(self.handle_new_operation_request) # when a operation name is doubleclicked on the list take the name import the ui and emit Qwidget and the name

            self.main_ui.central_widget.addTab(self.operations_listing_ui,"Operations")
            self.main_ui.central_widget.tabBar().setTabButton(0, QTabBar.ButtonPosition.RightSide, None)

            self.main_ui.central_widget.addTab(self.operation_history_ui,"Logs")
            self.main_ui.central_widget.tabBar().setTabButton(1, QTabBar.ButtonPosition.RightSide, None)

            del self.login_ui

    def handle_new_operation_request(self,operation_input : list):
        self.new_operation_ui = operation_input[0] # QWidget
        self.new_operation_ui.calculation_success.connect(self.handle_new_operation_data) # calculate button connection
        new_operation_name = operation_input[1] # str
        self.main_ui.add_new_operation_tab(self.new_operation_ui,new_operation_name) # add new_operation_ui to the main_ui.central_widget as a tab

    def handle_new_operation_data(self,new_operation_data : list):
        db_id = self.database_manager.save_operation_data_to_db(self.username,new_operation_data) # log is saved in the db and db_id is returned for logs_ui
        self.operation_history_ui.add_new_operation_data(db_id,new_operation_data) # when a calculation is done in the operation_ui all the variables is sent to the logs_ui

    def handle_logs_by_date(self,operation_data_date : list):
        logs_by_date = self.database_manager.return_operation_data_by_date(self.username,operation_data_date) # select * from history where date between operation_data_date
        self.operation_history_ui.show_operation_data_by_date(logs_by_date) # show logs within the logs_list
    
    def handle_operation_data_by_id(self,db_id : str):
        operation_data_by_id = self.database_manager.return_operation_data_by_id(db_id) # select * from history where id = ?
        self.operation_history_ui.init_history_ui(operation_data_by_id) # take operation_data_by_id and give it to history_ui

    def handle_create_new_history(self,history_input : list):
        new_history_ui = history_input[0] # QWidget
        new_history_name = history_input[1] # History db_id
        self.main_ui.add_new_history_tab(new_history_ui,new_history_name) # add new_history_ui to the main_ui.central_widget as a tab

    def handle_color_change(self,color_code : str): # main_ui.change_color_action_function --> AppManager --> handle_color_change --> operation_ui
        self.operations_listing_ui.font_color = color_code
        for i in range(self.main_ui.central_widget.count()):
            operation_widget = self.main_ui.central_widget.widget(i)
            if hasattr(operation_widget,"change_color"):
                operation_widget.change_color(color_code)

    def handle_relogin(self):
        self.login_ui = LoginUI()
        self.login_ui.login_signal.connect(self.handle_login)
        self.main_ui.central_widget.addTab(self.login_ui,"Login")
        self.main_ui.central_widget.tabBar().setTabButton(0, QTabBar.ButtonPosition.RightSide, None)

    def handle_preferred_language_change(self, preferred_language : str) -> None:
        print("language main")
        self.database_manager.update_preferred_language(self.username, preferred_language)

    def handle_preferred_theme_change(self, preferred_theme : str) -> None:
        print("theme main")
        self.database_manager.update_preferred_theme(self.username, preferred_theme)

    def handle_preffered_font_color_change(self, preferred_font_color : str) -> None:
        print("font color main")
        self.database_manager.update_preferred_font_color(self.username, preferred_font_color)

if __name__ == "__main__":
    manager = AppManager()
    manager.init_database_manager()
