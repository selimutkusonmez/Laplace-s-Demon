import importlib
import os
from PyQt6.QtCore import QSize,pyqtSignal,Qt,QDate,QTime
from PyQt6.QtWidgets import QWidget,QListWidget,QHBoxLayout,QListWidgetItem,QMessageBox,QVBoxLayout,QGroupBox,QLabel,QLineEdit,QDateEdit,QPushButton,QGridLayout
from PyQt6.QtGui import QIcon

class LogsUI(QWidget):
    logs_by_date_requested = pyqtSignal(list)
    show_history_requested = pyqtSignal(list)

    def __init__(self,username):
        super().__init__()
        self.init_ui()
        self.username = username

    def init_ui(self):

        #object name and styling background permit granted
        self.setObjectName("logs_ui")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        #layout created and set
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        #upper_groupbox and it's layout created and added to layout
        self.upper_groupbox = QGroupBox()
        self.upper_groupbox_layout = QHBoxLayout()
        self.upper_groupbox.setLayout(self.upper_groupbox_layout)
        self.layout.addWidget(self.upper_groupbox)

        self.upper_groupbox_layout.addWidget(QLabel("Username :"))
        self.username = QLabel(self.username)
        self.upper_groupbox_layout.addWidget(self.username)

        self.upper_groupbox_layout.addStretch()

        self.upper_groupbox_layout.addWidget(QLabel("Log Count :"))
        self.log_count = QLabel()
        self.upper_groupbox_layout.addWidget(self.log_count)

        self.upper_groupbox_layout.addStretch()

        today = QDate.currentDate()
        self.upper_groupbox_layout.addWidget(QLabel("Start Date :"))
        self.start_date = QDateEdit()
        self.start_date.setDate(today.addDays(-7))
        self.start_date.calendarPopup(True)
        self.start_date.setMaximumDate(today)
        self.upper_groupbox_layout.addWidget(self.start_date)

        self.upper_groupbox_layout.addStretch()

        self.upper_groupbox_layout.addWidget(QLabel("End Date :"))
        self.end_date = QDateEdit()
        self.end_date.setDate(today)
        self.end_date.setCalendarPopup(True)
        self.end_date.setMaximumDate(today)
        self.upper_groupbox_layout.addWidget(self.end_date)

        self.upper_groupbox_layout.addStretch()

        self.logs_button = QPushButton("Show Logs By Date")
        self.logs_button.clicked.connect(self.logs_button_function)
        self.upper_groupbox_layout.addWidget(self.logs_button)

        #bottom_groupbox and it's layout created and added to layout
        self.bottom_groupbox = QGroupBox()
        self.bottom_groupbox_layout = QGridLayout()
        self.bottom_groupbox.setLayout(self.bottom_groupbox_layout)
        self.layout.addWidget(self.bottom_groupbox)

        self.logs_list = QListWidget()
        self.bottom_groupbox_layout.addWidget(self.logs_list,0,0,1,2)

        self.refresh_logs_button = QPushButton("Show Current Session Logs")
        self.refresh_logs_button.clicked.connect(self.refresh_logs_button_function)
        self.bottom_groupbox_layout.addWidget(self.refresh_logs_button,1,0)

        self.clear_logs_button = QPushButton("Clear Logs")
        self.clear_logs_button.clicked.connect(self.clear_logs_button_function)
        self.bottom_groupbox_layout.addWidget(self.clear_logs_button,1,1)


    # LogsUI.logs_by_date_requested --> AppManager/DatabaseManager
    def logs_button_function(self):
        start_date = self.start_date.date().toString()
        end_date = self.end_date.date().toString()
        self.logs_by_date_requested.emit([start_date,end_date])

    # NewOperationUI/AppManager --> LogsUI.add_new_log
    def add_new_log(self, username : str, log_input : list):
        return
        # add logs came from operation_ui
    
    # DatabaseManager/AppManager --> LogsUI.show_logs_by_date
    def show_logs_by_date(self):
        self.logs_list.clear()
        # add logs came from databasemanager

    # LogsUI.show_history_requested --> AppManager/MainUI
    def init_history_ui(self,item):
        #get item text,info from item
        #create history ui
        #self.show_history_requested.emit([new_history_ui,log_db_id])
        return
    
    
    