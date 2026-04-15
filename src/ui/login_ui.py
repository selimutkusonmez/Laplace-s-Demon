import sys
import subprocess
from PyQt6.QtCore import Qt,pyqtSignal
from PyQt6.QtWidgets import (
     QApplication,QWidget,QLineEdit,QPushButton,QLabel,QGridLayout,QGroupBox)

class LoginUI(QWidget):
    login_requested = pyqtSignal(list)
    create_an_account_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()
       
    def init_ui(self):
        #object name and styling background permit granted
        self.setProperty("class","ui")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        #layout created
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # input groupbox created and placed
        self.central_groupbox = QGroupBox()
        self.central_groupbox.setProperty("class","login_groupbox")
        self.central_groupbox.setFixedSize(300,400)
        
        self.central_groupbox_layout = QGridLayout()
        self.central_groupbox.setLayout(self.central_groupbox_layout)
        self.layout.addWidget(self.central_groupbox,0,0)

        self.username_label = QLabel("Username")
        self.username_label.setProperty("class","login_label")
        self.central_groupbox_layout.addWidget(self.username_label,0,0)

        self.username_input = QLineEdit()
        self.username_input.setProperty("class","login_input")
        self.central_groupbox_layout.addWidget(self.username_input,0,1)

        self.password_label = QLabel("Password")
        self.password_label.setProperty("class","login_label")
        self.central_groupbox_layout.addWidget(self.password_label,1,0)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setProperty("class","login_input")
        self.central_groupbox_layout.addWidget(self.password_input,1,1)

        self.error_space = QLineEdit()
        self.error_space.setObjectName("error_space")
        self.error_space.setReadOnly(True)
        self.central_groupbox_layout.addWidget(self.error_space,2,0,1,2)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login_button_func)
        self.central_groupbox_layout.addWidget(self.login_button,3,0,1,2)

        self.portfolio_button = QPushButton("My Web Site")
        self.central_groupbox_layout.addWidget(self.portfolio_button,4,0,1,2)

        self.restart_app_button = QPushButton("Create New Account")
        self.restart_app_button.clicked.connect(self.create_an_account_button_function)
        self.central_groupbox_layout.addWidget(self.restart_app_button,5,0,1,2)

    def create_an_account_button_function(self):
        self.create_an_account_requested.emit()

    def login_button_func(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username == "" or password == "":
            self.error_space.setText("Please Fill In All Fields")
            return
        else:
            self.login_requested.emit([username,password])


