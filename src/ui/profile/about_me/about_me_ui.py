from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGroupBox,QLabel,QWidget,QGridLayout,QHBoxLayout,QLineEdit,QTableWidget,QTableWidgetItem

class AboutMeUI(QWidget):
    def __init__(self,username,current_user_stats):
        super().__init__()
        self.init_ui()
        self.fill_user_stats(username,current_user_stats)

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
        self.user_info_groupbox_layout.addWidget(self.username_label)

        self.user_info_groupbox_layout.addStretch()

        self.user_info_groupbox_layout.addWidget(QLabel("User ID"))
        self.username_id_label = QLineEdit()
        self.username_id_label.setReadOnly(True)
        self.user_info_groupbox_layout.addWidget(self.username_id_label)

        self.user_info_groupbox_layout.addStretch()

        self.user_info_groupbox_layout.addWidget(QLabel("Account Opening Date"))
        self.account_opening_date_label = QLineEdit()
        self.account_opening_date_label.setReadOnly(True)
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
        self.successfull_login_info_groupbox_layout.addWidget(self.last_successful_login_date_label,0,1)

        self.successfull_login_info_groupbox_layout.addWidget(QLabel("Last Successful Login IP: "),1,0)
        self.last_successful_login_ip_label = QLineEdit()
        self.last_successful_login_ip_label.setReadOnly(True)
        self.successfull_login_info_groupbox_layout.addWidget(self.last_successful_login_ip_label,1,1)

        self.successfull_login_info_groupbox_layout.addWidget(QLabel("Last Successful Login MAC: "),2,0)
        self.last_successful_login_mac_label = QLineEdit()
        self.last_successful_login_mac_label.setReadOnly(True)
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
        self.failed_login_info_groupbox_layout.addWidget(self.last_failed_login_date_label,0,1)

        self.failed_login_info_groupbox_layout.addWidget(QLabel("Last Failed Login IP: "),1,0)
        self.last_failed_login_ip_label = QLineEdit()
        self.last_failed_login_ip_label.setReadOnly(True)
        self.failed_login_info_groupbox_layout.addWidget(self.last_failed_login_ip_label,1,1)

        self.failed_login_info_groupbox_layout.addWidget(QLabel("Last Failed Login MAC: "),2,0)
        self.last_failed_login_mac_label = QLineEdit()
        self.last_failed_login_mac_label.setReadOnly(True)
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
        self.operation_usage_info_groupbox_layout.addWidget(self.total_operation_usage_count_label,0,1)

        self.operation_usage_info_groupbox_layout.addWidget(QLabel("Most Used Operation: "),1,0)
        self.most_used_operation_label = QLineEdit()
        self.most_used_operation_label.setReadOnly(True)
        self.operation_usage_info_groupbox_layout.addWidget(self.most_used_operation_label,1,1)

        self.operation_usage_info_groupbox_layout.addWidget(QLabel("Last Used Operation: "),2,0)
        self.last_used_operation_label = QLineEdit()
        self.last_used_operation_label.setReadOnly(True)
        self.operation_usage_info_groupbox_layout.addWidget(self.last_used_operation_label,2,1)



        # Operation Usage Table Groupbox
        self.operation_usage_table_groupbox = QGroupBox()
        self.operation_usage_table_groupbox.setMinimumSize(100,100)
        self.operation_usage_table_groupbox_layout = QGridLayout()
        self.operation_usage_table_groupbox.setLayout(self.operation_usage_table_groupbox_layout)
        self.layout.addWidget(self.operation_usage_table_groupbox,2,1)

        self.operation_usage_table = QTableWidget()
        self.operation_usage_table.setColumnCount(1)
        self.operation_usage_table.setHorizontalHeaderLabels(("Count",))
        self.operation_usage_table_groupbox_layout.addWidget(self.operation_usage_table)

    def fill_user_stats(self,username,current_user_stats):
        user_id = str(current_user_stats[0])
        account_opening_date = str(current_user_stats[1])
        last_successful_login_date = str(current_user_stats[2])
        last_successful_login_ip = current_user_stats[3]
        last_successful_login_mac = current_user_stats[4]
        last_failed_login_date = str(current_user_stats[5])
        last_failed_login_ip = current_user_stats[6] if current_user_stats[6] != None else "None"
        last_failed_login_mac = current_user_stats[7] if current_user_stats[7] != None else "None"
        total_operation_usage = str(current_user_stats[8]) if current_user_stats[8] != 0 else "None"
        operation_usage_counts = current_user_stats[9]
        most_used_operation = current_user_stats[10] if current_user_stats[10] != None else "None"
        last_used_operation = current_user_stats[11] if current_user_stats[11] != None else "None"

        self.username_label.setText(username)
        self.username_id_label.setText(user_id)
        self.account_opening_date_label.setText(account_opening_date)

        self.last_successful_login_date_label.setText(last_successful_login_date)
        self.last_successful_login_ip_label.setText(last_successful_login_ip)
        self.last_successful_login_mac_label.setText(last_successful_login_mac)

        self.last_failed_login_date_label.setText(last_failed_login_date)
        self.last_failed_login_ip_label.setText(last_failed_login_ip)
        self.last_failed_login_mac_label.setText(last_failed_login_mac)

        self.total_operation_usage_count_label.setText(total_operation_usage)
        self.most_used_operation_label.setText(most_used_operation)
        self.last_used_operation_label.setText(last_used_operation)

        if operation_usage_counts:
            self.operation_usage_table.setRowCount(len(operation_usage_counts))
            self.operation_usage_table.setVerticalHeaderLabels(operation_usage_counts.keys())
            
            for i, count in enumerate(operation_usage_counts.values()):
                item = QTableWidgetItem(str(count))
                self.operation_usage_table.setItem(i, 0, item)
        else:
            return













