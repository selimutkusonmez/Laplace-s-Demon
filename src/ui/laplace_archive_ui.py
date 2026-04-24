from PyQt6.QtCore import QSize,pyqtSignal,Qt,QDate
from PyQt6.QtWidgets import QWidget,QListWidget,QHBoxLayout,QListWidgetItem,QVBoxLayout,QGroupBox,QLabel,QDateEdit,QPushButton,QGridLayout
from PyQt6.QtGui import QIcon
from src.ui.operation_ui import *
from src.assets.style.style_reader.get_icon import get_archive_record_icon

class LaplaceArchiveUI(QWidget):

    archive_records_by_date_requested = pyqtSignal(str,str)
    archive_record_data_by_id_requested = pyqtSignal(str)

    ui_route_requested = pyqtSignal(QWidget,str,str)

    def __init__(self,username,laplace_archive_records_count,font_color : str = "black"):
        super().__init__()
        self.username = username
        self.laplace_archive_records_count = laplace_archive_records_count
        self.font_color = font_color

        self.init_ui()
        

    def init_ui(self):

        self.setProperty("class","ui")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.upper_groupbox = QGroupBox()
        self.upper_groupbox_layout = QHBoxLayout()
        self.upper_groupbox.setLayout(self.upper_groupbox_layout)
        self.layout.addWidget(self.upper_groupbox)

        self.upper_groupbox_layout.addWidget(QLabel("Username :"))
        self.username = QLabel(self.username)
        self.upper_groupbox_layout.addWidget(self.username)

        self.upper_groupbox_layout.addStretch()

        self.upper_groupbox_layout.addWidget(QLabel("Log Count :"))
        self.laplace_archive_records_count_label = QLabel(str(self.laplace_archive_records_count))
        self.upper_groupbox_layout.addWidget(self.laplace_archive_records_count_label)

        self.upper_groupbox_layout.addStretch()

        today = QDate.currentDate()
        self.upper_groupbox_layout.addWidget(QLabel("Start Date :"))
        self.start_date = QDateEdit()
        self.start_date.setDate(today.addDays(-7))
        self.start_date.setCalendarPopup(True)
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

        self.list_archive_records_by_date_button = QPushButton("List Archive Records By Date")
        self.list_archive_records_by_date_button.clicked.connect(self.list_archive_records_by_date_button_function)
        self.upper_groupbox_layout.addWidget(self.list_archive_records_by_date_button)

        self.lower_groupbox = QGroupBox()
        self.lower_groupbox_layout = QGridLayout()
        self.lower_groupbox.setLayout(self.lower_groupbox_layout)
        self.layout.addWidget(self.lower_groupbox)

        self.archive_records_list = QListWidget()
        self.archive_records_list.setIconSize(QSize(100,100))
        self.archive_records_list.setProperty("class","list")
        self.archive_records_list.itemDoubleClicked.connect(self.request_archive_record_data_by_id)
        self.lower_groupbox_layout.addWidget(self.archive_records_list,0,0,1,2)

        self.show_current_session_archives_button = QPushButton("Show Current Session Records")
        self.show_current_session_archives_button.clicked.connect(self.show_current_session_archives_button_function)
        self.lower_groupbox_layout.addWidget(self.show_current_session_archives_button,1,0)

        self.clear_archive_list_button = QPushButton("Clear Records List")
        self.clear_archive_list_button.clicked.connect(self.clear_archive_list_button_function)
        self.lower_groupbox_layout.addWidget(self.clear_archive_list_button,1,1)

        self.current_session_archives_records_and_datas = []


    # LaplaceArchiveUI.list_archive_records_by_date_button_function.archive_records_by_date_requested --> AppManager.hanlde_archive_records_by_date --> DatabaseManager.return_logs_by_date --> LaplaceArchiveUI.list_archive_records_by_date
    def list_archive_records_by_date_button_function(self):
        start_date = self.start_date.date().toString()
        end_date = self.end_date.date().toString()
        self.archive_records_by_date_requested.emit(start_date,end_date)

    def list_archive_records_by_date(self,logs : list):

        self.archive_records_list.clear()

        for log in logs:
                db_id = log[0]
                date = log[1]
                operation = log[2]
                variables = log[3]
                archive_record = f"{db_id} | {date} | {operation} | {variables}"
                archive_record = QListWidgetItem(archive_record)
                archive_record.setData(Qt.ItemDataRole.UserRole,db_id)
                print(operation)
                icon = get_archive_record_icon(operation)
                archive_record.setIcon(icon)
                self.archive_records_list.addItem(archive_record)



    # LaplaceArchiveUI.request_archive_record_data_by_id.archive_record_data_by_id_requested --> AppManager.handle_archive_record_data_by_id --> DatabaseManager_return_operation_data_by_id --> LaplaceArchiveUI.init_new_archive_record_ui
    def request_archive_record_data_by_id(self,item : QListWidgetItem):
        record_database_id = item.data(Qt.ItemDataRole.UserRole)
        self.archive_record_data_by_id_requested.emit(str(record_database_id))

    # LaplaceArchiveUI.request_archive_record_data_by_id --> LaplaceArchiveUI.init_new_archive_record_ui.init_new_archive_record_ui_requested --> AppManager.handle_add_new_archive_record_ui --> MainUI.add_new_archive_record_tab
    def init_new_archive_record_ui(self, operation_data_by_id: list):
        db_id = operation_data_by_id[0]
        date = operation_data_by_id[2]
        new_archive_record_operation_name = operation_data_by_id[3]
        variables = operation_data_by_id[4]
        input_data = operation_data_by_id[5].replace("{", "").replace("}", "")
        output = operation_data_by_id[6]

        history_map = {
            "Population Mean": MeanHistoryUI,
            "Sample Mean": MeanHistoryUI,
            "Population Variance": VarianceHistoryUI,
            "Sample Variance": VarianceHistoryUI,
            "Population Standard Deviation": StandardDeviationHistoryUI,
            "Sample Standard Deviation": StandardDeviationHistoryUI,
            "Percentile": PercentileHistoryUI,
            "Population Covariance": CovarianceHistoryUI,
            "Sample Covariance": CovarianceHistoryUI,
            "Correlation": CorrelationHistoryUI,
            "Mutually Exclusive": AdditionRuleHistoryUI,
            "Non Mutually Exclusive": AdditionRuleHistoryUI,
            "Independent Events": MultiplicationRuleHistoryUI,
            "Dependent Events": MultiplicationRuleHistoryUI,
            "Bayes": BayesHistoryUI,
            "Central Limit Theorem": CentralLimitTheoremHistoryUI,
            "Confidence Interval": ConfidenceIntervalHistoryUI,
            "Margin Of Error": MarginOfErrorHistoryUI,
            "Bernoulli Distribution": BernoulliDistributionHistoryUI,
            "Binomial Distribution": BinomialDistributionHistoryUI,
            "Poisson Distribution PMF": PoissonDistributionHistoryUI,
            "Poisson Distribution CDF": PoissonDistributionHistoryUI,
            "Normal Distribution PDF": NormalDistributionHistoryUI,
            "Normal Distribution CDF": NormalDistributionHistoryUI,
            "Standard Normal Distribution": StandardNormalDistributionHistoryUI,
            "Uniform Distribution PDF": UniformDistributionHistoryUI,
            "Uniform Distribution CDF": UniformDistributionHistoryUI,
            "Log Normal Distribution PDF": LogNormalDistributionHistoryUI,
            "Log Normal Distribution CDF": LogNormalDistributionHistoryUI,
            "Pareto Distribution PDF": ParetoDistributionHistoryUI,
            "Pareto Distribution CDF": ParetoDistributionHistoryUI,
            "Z Test": zTestHistoryUI,
            "Single Sample t Test": tTestHistoryUI,
            "Independent Sample t Test": tTestHistoryUI,
            "Paired Sample t test": tTestHistoryUI,
            "Chi Square Test": ChiSquareTestHistoryUI,
            "ANOVA": AnovaHistoryUI,
        }

        record_key = str(db_id)

        if not hasattr(self, "open_archive_records"):
            self.open_archive_records = {}

        if record_key in self.open_archive_records:
            existing_ui = self.open_archive_records[record_key]
            try:
                existing_ui.property("tab_id")
                self.ui_route_requested.emit(existing_ui, f"{new_archive_record_operation_name} (ID : {db_id})", record_key)
                return
            except RuntimeError:
                del self.open_archive_records[record_key]

        worker_class = history_map.get(new_archive_record_operation_name)
        new_ui = worker_class(str(db_id), date, new_archive_record_operation_name, variables, input_data, output, self.font_color)
        
        new_ui.setProperty("tab_id", record_key)
        new_ui.setProperty("db_id", db_id)
        
        self.open_archive_records[record_key] = new_ui
        self.ui_route_requested.emit(new_ui, f"{new_archive_record_operation_name} (ID : {db_id})", record_key)



    # NewOperationUI.calculation_success --> AppManager.handle_new_archive_record --> DatabaseManager.save_archive_record --> LaplaceArchiveUI.add_new_archive_record
    def add_new_archive_record(self,db_id : str, new_log : list):

        date = new_log[0]
        operation = new_log[1]
        variables = new_log[2]

        new_archive_record_text = f"{db_id} | {date} | {operation} | {variables}"
        new_archive_record_item = QListWidgetItem(new_archive_record_text)
        new_archive_record_item.setData(Qt.ItemDataRole.UserRole,db_id)
        self.archive_records_list.addItem(new_archive_record_item)
        self.current_session_archives_records_and_datas.append({"db_id" : db_id,"operation_data_text": new_archive_record_text})

        self.laplace_archive_records_count_label.setText(str(int(self.laplace_archive_records_count_label.text()) + 1))
        # add logs came from operation_ui



    # LaplaceArchiveUI.current_session_archives_records_and_datas --> LaplaceArchiveUI.archive_records_list
    def show_current_session_archives_button_function(self):
        self.archive_records_list.clear()

        for data in self.current_session_archives_records_and_datas:
            archive_item = QListWidgetItem(data["operation_data_text"])
            archive_item.setData(Qt.ItemDataRole.UserRole,data["db_id"])
            self.archive_records_list.addItem(archive_item)
    
    # Clear Archive Records List
    def clear_archive_list_button_function(self):
        self.archive_records_list.clear()
    
    
    def set_button_enabled(self,list_records_by_date):
        if list_records_by_date:
            self.list_archive_records_by_date_button.setEnabled(True)
            self.list_archive_records_by_date_button.setText("List Archive Records By Date")
        else:
            self.list_archive_records_by_date_button.setEnabled(False)
            self.list_archive_records_by_date_button.setText("Processing...")