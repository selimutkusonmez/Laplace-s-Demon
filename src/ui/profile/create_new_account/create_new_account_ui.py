from PyQt6.QtWidgets import QWidget,QPushButton,QLabel,QLineEdit,QGridLayout,QGroupBox
from PyQt6.QtCore import pyqtSignal

class CreateNewAccountUI(QWidget):
    save_account_info_requested = pyqtSignal(list)
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.create_an_account_groupbox = QGroupBox()
        self.create_an_account_groupbox.setFixedSize(300,300)
        self.create_an_account_groupbox_layout = QGridLayout()
        self.create_an_account_groupbox.setLayout(self.create_an_account_groupbox_layout)
        self.layout.addWidget(self.create_an_account_groupbox)

        self.create_an_account_groupbox_layout.addWidget(QLabel("Username"),0,0)
        self.username_input = QLineEdit()
        self.create_an_account_groupbox_layout.addWidget(self.username_input,0,1)

        self.create_an_account_groupbox_layout.addWidget(QLabel("Password"),1,0)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.create_an_account_groupbox_layout.addWidget(self.password_input,1,1)

        self.output = QLineEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("""border : none;""")
        self.create_an_account_groupbox_layout.addWidget(self.output,2,0,1,2)

        self.create_my_account_button = QPushButton("Create My Account")
        self.create_my_account_button.clicked.connect(self.create_my_account_button_function)
        self.create_an_account_groupbox_layout.addWidget(self.create_my_account_button,3,0,1,2)

    # CreateNewAccountUI.create_my_account_button_function.save_account_info_requested --> AppManager.handle_save_account_info --> DatabaseManager.save_account_info
    def create_my_account_button_function(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username == "" or password == "":
            self.output.setText("Please Fill In All Fields")
            return
        self.save_account_info_requested.emit(username,password)

    def set_button_enabled(self,create_account):
        if create_account:
            self.create_my_account_button.setEnabled(True)
            self.create_my_account_button.setText("Create My Account")
        else:
            self.create_my_account_button.setEnabled(False)
            self.create_my_account_button.setText("Processing...")

    def set_output(self,output : str):
        self.output.setText(output)