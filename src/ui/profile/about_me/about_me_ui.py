from PyQt6.QtWidgets import QGroupBox,QLabel,QWidget,QGridLayout,QHBoxLayout,QLineEdit,QListWidget,QListWidgetItem
from PyQt6.QtCore import QSize
from src.assets.style.style_reader.get_icon import get_archive_record_icon
class AboutMeUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # User Info Groupbox
        self.user_info_groupbox = QGroupBox()
        self.user_info_groupbox.setMaximumHeight(85)
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
        self.operation_usage_list_groupbox = QGroupBox()
        self.operation_usage_list_groupbox.setMinimumSize(100,100)
        self.operation_usage_list_groupbox_layout = QGridLayout()
        self.operation_usage_list_groupbox.setLayout(self.operation_usage_list_groupbox_layout)
        self.layout.addWidget(self.operation_usage_list_groupbox,2,1)

        self.operation_usage_list = QListWidget()
        self.operation_usage_list.setProperty("class","list")
        self.operation_usage_list.setIconSize(QSize(100,100))
        self.operation_usage_list_groupbox_layout.addWidget(self.operation_usage_list)


    #MainUI.about_me_action_function --> AppManager.handle_init_about_me_ui --> DatabaseManager.pull_user_stats --> AboutMeUI(current_user_stats)
    #OperationUI.calculation_success --> AppManager.handle_update_about_me_ui --> AboutMeUI.fill_user_stats(current_user_stats)
    def fill_user_stats(self,username,current_user_stats):
        user_id = str(current_user_stats[1])
        account_opening_date = str(current_user_stats[2])
        last_successful_login_date = str(current_user_stats[3])
        last_failed_login_date = str(current_user_stats[4])
        total_operation_usage = str(current_user_stats[5]) if current_user_stats[5] != 0 else "None"
        operation_usage_counts = current_user_stats[6]
        most_used_operation = current_user_stats[7] if current_user_stats[7] != None else "None"
        last_used_operation = current_user_stats[8] if current_user_stats[8] != None else "None"

        self.username_label.setText(username)
        self.username_id_label.setText(user_id)
        self.account_opening_date_label.setText(account_opening_date)

        self.last_successful_login_date_label.setText(last_successful_login_date)

        self.last_failed_login_date_label.setText(last_failed_login_date)

        self.total_operation_usage_count_label.setText(total_operation_usage)
        self.most_used_operation_label.setText(most_used_operation)
        self.last_used_operation_label.setText(last_used_operation)

        if operation_usage_counts:
            for operation,count in operation_usage_counts.items():
                operation_count = f"{operation} ----> {count}"
                operation_count = QListWidgetItem(operation_count)
                icon = get_archive_record_icon(operation)
                operation_count.setIcon(icon)
                self.operation_usage_list.addItem(operation_count)

        













