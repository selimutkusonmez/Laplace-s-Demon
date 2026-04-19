import sys
import subprocess
from PyQt6.QtCore import Qt,pyqtSignal
from PyQt6.QtWidgets import QWidget,QLineEdit,QPushButton,QLabel,QGridLayout,QGroupBox,QCheckBox

class LoginUI(QWidget):

    login_requested = pyqtSignal(list)
    create_new_account_requested = pyqtSignal()

    def __init__(self,remember_me_default : bool = False):
        super().__init__()
        self.init_ui(remember_me_default)
       
    def init_ui(self,remember_me_default):

        #object name and styling background permit granted
        self.setProperty("class","ui")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        #layout created
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # input groupbox created and placed
        self.login_groupbox = QGroupBox()
        self.login_groupbox.setProperty("class","login_groupbox")
        self.login_groupbox.setFixedSize(300,400)
        
        self.login_groupbox_layout = QGridLayout()
        self.login_groupbox.setLayout(self.login_groupbox_layout)
        self.layout.addWidget(self.login_groupbox,0,0)

        self.username_label = QLabel("Username")
        self.username_label.setProperty("class","login_label")
        self.login_groupbox_layout.addWidget(self.username_label,0,0)

        self.username_input = QLineEdit()
        self.username_input.setProperty("class","login_input")
        self.login_groupbox_layout.addWidget(self.username_input,0,1)

        self.password_label = QLabel("Password")
        self.password_label.setProperty("class","login_label")
        self.login_groupbox_layout.addWidget(self.password_label,1,0)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setProperty("class","login_input")
        self.login_groupbox_layout.addWidget(self.password_input,1,1)

        self.remember_me_checkbox = QCheckBox("Remember Me")
        self.remember_me_checkbox.setChecked(remember_me_default)
        self.login_groupbox_layout.addWidget(self.remember_me_checkbox,2,0,1,2,Qt.AlignmentFlag.AlignRight)

        self.error_space = QLineEdit()
        self.error_space.setObjectName("error_space")
        self.error_space.setReadOnly(True)
        self.login_groupbox_layout.addWidget(self.error_space,3,0,1,2)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login_button_function)
        self.login_groupbox_layout.addWidget(self.login_button,4,0,1,2)

        self.portfolio_button = QPushButton("My Web Site")
        self.login_groupbox_layout.addWidget(self.portfolio_button,5,0,1,2)

        self.create_new_account_button = QPushButton("Create New Account")
        self.create_new_account_button.clicked.connect(self.create_new_account_button_function)
        self.login_groupbox_layout.addWidget(self.create_new_account_button,6,0,1,2)

    #LoginUI.create_new_account_button_function.create_new_account_requested --> AppManager.handle_create_new_account
    def create_new_account_button_function(self):
        self.create_new_account_requested.emit()

    #LoginUI.login_button_function.login_requested --> AppManager.handle_login --> DatabaseManager.check_login --> DatabaseManager.save_user_log --> login_code --> AppManager.handle_login
    def login_button_function(self):
        username = self.username_input.text()
        password = self.password_input.text()
        remember_me_checkbox_state = self.remember_me_checkbox.isChecked()
        if username == "" or password == "":
            self.error_space.setText("Please Fill In All Fields")
            return
        else:
            self.login_requested.emit([username,password,remember_me_checkbox_state])

    def set_button_enabled(self,logging_in):
        if logging_in:
            self.login_button.setEnabled(True)
            self.login_button.setText("Login")
        else:
            self.login_button.setEnabled(False)
            self.login_button.setText("Authenticating...")

    def set_output_text(self,output_text):
        self.error_space.setText(output_text)


