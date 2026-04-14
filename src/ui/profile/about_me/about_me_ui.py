from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGroupBox,QLabel,QWidget,QGridLayout,QHBoxLayout,QLineEdit,QTableWidget,QListWidget,QSizePolicy,QSpacerItem

class AboutMeUI(QWidget):
    def __init__(self,current_user):
        super().__init__()
        self.current_user = "05/30/2007"
        self.init_ui()

    def init_ui(self):
        
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # User Info Groupbox
        self.user_info_groupbox = QGroupBox()
        self.user_info_groupbox.setMaximumHeight(82)
        self.user_info_groupbox_layout = QHBoxLayout()
        self.user_info_groupbox.setLayout(self.user_info_groupbox_layout)
        self.layout.addWidget(self.user_info_groupbox,0,0,1,3)

        self.user_info_groupbox_layout.addWidget(QLabel("Username"))
        self.username_label = QLineEdit()
        self.username_label.setReadOnly(True)
        self.username_label.setText(self.current_user)
        self.user_info_groupbox_layout.addWidget(self.username_label)

        self.user_info_groupbox_layout.addStretch()

        self.user_info_groupbox_layout.addWidget(QLabel("User ID"))
        self.username_id_label = QLineEdit()
        self.username_id_label.setReadOnly(True)
        self.username_id_label.setText(self.current_user)
        self.user_info_groupbox_layout.addWidget(self.username_id_label)

        self.user_info_groupbox_layout.addStretch()

        self.user_info_groupbox_layout.addWidget(QLabel("Account Opening Date"))
        self.account_opening_date_label = QLineEdit()
        self.account_opening_date_label.setReadOnly(True)
        self.account_opening_date_label.setText(self.current_user)
        self.user_info_groupbox_layout.addWidget(self.account_opening_date_label)


        # Successful Login Info Groupbox
        self.successfull_login_info_groupbox = QGroupBox()
        self.successfull_login_info_groupbox.setMaximumSize(900,300)
        self.successfull_login_info_groupbox.setMinimumSize(50,50)
        self.successfull_login_info_groupbox_layout = QGridLayout()
        self.successfull_login_info_groupbox.setLayout(self.successfull_login_info_groupbox_layout)
        self.layout.addWidget(self.successfull_login_info_groupbox,1,0)

        self.successfull_login_info_groupbox_layout.addWidget(QLabel("Last Successful Login Date: "),0,0)
        self.last_successful_login_date_label = QLineEdit()
        self.last_successful_login_date_label.setReadOnly(True)
        self.last_successful_login_date_label.setText(self.current_user)
        self.successfull_login_info_groupbox_layout.addWidget(self.last_successful_login_date_label,0,1)

        self.successfull_login_info_groupbox_layout.addWidget(QLabel("Last Successful Login IP: "),1,0)
        self.last_successful_login_ip_label = QLineEdit()
        self.last_successful_login_ip_label.setReadOnly(True)
        self.last_successful_login_ip_label.setText(self.current_user)
        self.successfull_login_info_groupbox_layout.addWidget(self.last_successful_login_ip_label,1,1)

        self.successfull_login_info_groupbox_layout.addWidget(QLabel("Last Successful Login MAC: "),2,0)
        self.last_successful_login_mac_label = QLineEdit()
        self.last_successful_login_mac_label.setReadOnly(True)
        self.last_successful_login_mac_label.setText(self.current_user)
        self.successfull_login_info_groupbox_layout.addWidget(self.last_successful_login_mac_label,2,1)


        # Failed Login Info Groupbox
        self.failed_login_info_groupbox = QGroupBox()
        self.failed_login_info_groupbox.setMaximumSize(900,350)
        self.failed_login_info_groupbox.setMinimumSize(50,50)
        self.failed_login_info_groupbox_layout = QGridLayout()
        self.failed_login_info_groupbox.setLayout(self.failed_login_info_groupbox_layout)
        self.layout.addWidget(self.failed_login_info_groupbox,1,1)

        self.failed_login_info_groupbox_layout.addWidget(QLabel("Last Failed Login Date: "),0,0)
        self.last_failed_login_date_label = QLineEdit()
        self.last_failed_login_date_label.setReadOnly(True)
        self.last_failed_login_date_label.setText(self.current_user)
        self.failed_login_info_groupbox_layout.addWidget(self.last_failed_login_date_label,0,1)

        self.failed_login_info_groupbox_layout.addWidget(QLabel("Last Failed Login IP: "),1,0)
        self.last_failed_login_ip_label = QLineEdit()
        self.last_failed_login_ip_label.setReadOnly(True)
        self.last_failed_login_ip_label.setText(self.current_user)
        self.failed_login_info_groupbox_layout.addWidget(self.last_failed_login_ip_label,1,1)

        self.failed_login_info_groupbox_layout.addWidget(QLabel("Last Failed Login MAC: "),2,0)
        self.last_failed_login_mac_label = QLineEdit()
        self.last_failed_login_mac_label.setReadOnly(True)
        self.last_failed_login_mac_label.setText(self.current_user)
        self.failed_login_info_groupbox_layout.addWidget(self.last_failed_login_mac_label,2,1)


        # Operation Usage Info Groupbox
        self.operation_usage_info_groupbox = QGroupBox()
        self.operation_usage_info_groupbox.setMinimumSize(100,100)
        self.operation_usage_info_groupbox_layout = QGridLayout()
        self.operation_usage_info_groupbox.setLayout(self.operation_usage_info_groupbox_layout)
        self.layout.addWidget(self.operation_usage_info_groupbox,2,0)

        self.operation_usage_info_groupbox_layout.addWidget(QLabel("Total Operation Usage Count: "),0,0)
        self.total_operation_usage_count_label = QLineEdit()
        self.total_operation_usage_count_label.setReadOnly(True)
        self.total_operation_usage_count_label.setText(self.current_user)
        self.operation_usage_info_groupbox_layout.addWidget(self.total_operation_usage_count_label,0,1)

        self.operation_usage_info_groupbox_layout.addWidget(QLabel("Most Used Operation: "),1,0)
        self.most_used_operation_label = QLineEdit()
        self.most_used_operation_label.setReadOnly(True)
        self.most_used_operation_label.setText(self.current_user)
        self.operation_usage_info_groupbox_layout.addWidget(self.most_used_operation_label,1,1)

        self.operation_usage_info_groupbox_layout.addWidget(QLabel("Last Used Operation: "),2,0)
        self.last_used_operation_label = QLineEdit()
        self.last_used_operation_label.setReadOnly(True)
        self.last_used_operation_label.setText(self.current_user)
        self.operation_usage_info_groupbox_layout.addWidget(self.last_used_operation_label,2,1)



        # Operation Usage Table Groupbox
        self.operation_usage_table_groupbox = QGroupBox()
        self.operation_usage_table_groupbox.setMinimumSize(100,100)
        self.operation_usage_table_groupbox_layout = QGridLayout()
        self.operation_usage_table_groupbox.setLayout(self.operation_usage_table_groupbox_layout)
        self.layout.addWidget(self.operation_usage_table_groupbox,2,1)

        self.operation_usage_table = QTableWidget()
        self.operation_usage_table_groupbox_layout.addWidget(self.operation_usage_table)










