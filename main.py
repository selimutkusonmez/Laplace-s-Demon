import sys
from PyQt6.QtWidgets import QApplication,QTabBar
from src.ui import MainUI,LoginUI,LogsUI,DatabaseManager,OperationsListingUI

class AppManager():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_ui = MainUI()
        self.database_manager = DatabaseManager()
        self.login_ui = LoginUI()
        self.login_ui.login_signal.connect(self.handle_login)
        
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
            self.main_ui.central_widget.removeTab(0)

            self.logs_ui = LogsUI(self.username)
            self.logs_ui.show_history_requested.connect(self.handle_new_history) # when a log is doubleclicked take information,create history_ui and send it to the appmanager
            self.logs_ui.logs_by_date_requested.connect(self.handle_logs_by_date) # when user asks for a spesific date log or a range of date

            self.operations_listing_ui = OperationsListingUI()
            self.operations_listing_ui.new_operation_requested.connect(self.handle_new_operation_request) # when a operation name is doubleclicked on the list take the name import the ui and emit Qwidget and the name

            self.main_ui.central_widget.addTab(self.operations_listing_ui,"Operations")
            self.main_ui.central_widget.tabBar().setTabButton(0, QTabBar.ButtonPosition.RightSide, None)

            self.main_ui.central_widget.addTab(self.logs_ui,"Logs")
            self.main_ui.central_widget.tabBar().setTabButton(1, QTabBar.ButtonPosition.RightSide, None)

    def handle_new_operation_request(self,operation_input : list):
        new_operation_ui = operation_input[0] # QWidget
        new_operation_ui.calculation_success.connect(self.handle_log) # calculate button connection
        new_operation_name = operation_input[1] # str
        self.main_ui.add_new_operation_tab(new_operation_ui,new_operation_name) # add new_operation_ui to the main_ui.central_widget as a tab

    def handle_log(self,log_input):
        self.logs_ui.add_new_log(self.username,log_input) # when a calculation is done in the operation_ui all the variables is sent to the logs_ui
        self.database_manager.save_log(self.username,log_input) # log is saved in the db

    def handle_logs_by_date(self,log_date : list):
        logs_by_date = self.database_manager.brings_logs_by_date(self.username,log_date) # select * from logs where date ?
        self.logs_ui.show_logs_by_date(logs_by_date) # show logs within the logs_list
    
    def handle_new_history(self,history_input : list):
        new_history_ui = history_input[0] # QWidget
        new_history_name = history_input[1] # History db_id
        self.main_ui.add_new_history_tab(new_history_ui,new_history_name) # add new_history_ui to the main_ui.central_widget as a tab

if __name__ == "__main__":
    manager = AppManager()
    manager.init_main_ui()
