
from PyQt6.QtCore import QSize,pyqtSignal,Qt,QDate
from PyQt6.QtWidgets import QWidget,QListWidget,QHBoxLayout,QListWidgetItem,QVBoxLayout,QGroupBox,QLabel,QDateEdit,QPushButton,QGridLayout
from PyQt6.QtGui import QIcon
from src.ui.operation_ui import *


class LogsUI(QWidget):
    logs_by_date_requested = pyqtSignal(list)
    create_history_requested = pyqtSignal(list)
    log_by_id_requested = pyqtSignal(str)

    def __init__(self,username,log_count):
        super().__init__()
        self.username = username
        self.log_count = log_count
        self.init_ui()
        

    def init_ui(self):

        #object name and styling background permit granted
        self.setProperty("class","ui")
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
        self.log_count = QLabel(str(self.log_count))
        self.upper_groupbox_layout.addWidget(self.log_count)

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

        self.logs_button = QPushButton("Show Logs By Date")
        self.logs_button.clicked.connect(self.logs_button_function)
        self.upper_groupbox_layout.addWidget(self.logs_button)

        #lower_groupbox and it's layout created and added to layout
        self.lower_groupbox = QGroupBox()
        self.lower_groupbox_layout = QGridLayout()
        self.lower_groupbox.setLayout(self.lower_groupbox_layout)
        self.layout.addWidget(self.lower_groupbox)

        self.logs_list = QListWidget()
        self.logs_list.setProperty("class","list")
        self.logs_list.itemDoubleClicked.connect(self.show_log_by_id)
        self.lower_groupbox_layout.addWidget(self.logs_list,0,0,1,2)

        self.refresh_logs_button = QPushButton("Show Current Session Logs")
        self.refresh_logs_button.clicked.connect(self.show_current_session_logs_function)
        self.lower_groupbox_layout.addWidget(self.refresh_logs_button,1,0)

        self.clear_logs_button = QPushButton("Clear Logs")
        self.clear_logs_button.clicked.connect(self.clear_logs_button_function)
        self.lower_groupbox_layout.addWidget(self.clear_logs_button,1,1)

        self.current_session_logs = []


    # LogsUI.logs_button_function.logs_by_date_requested --> AppManager --> DatabaseManager.return_logs_by_date --> LogsUI.show_logs_by_date
    def logs_button_function(self):
        start_date = self.start_date.date().toString()
        end_date = self.end_date.date().toString()
        self.logs_by_date_requested.emit([start_date,end_date])

    # LogsUI.logs_button_function.logs_by_date_requested --> AppManager --> DatabaseManager.return_logs_by_date --> AppManager --> LogsUI.show_logs_by_date
    def show_logs_by_date(self,logs : list):
        self.logs_list.clear()
        for log in logs:
                db_id = log[0]
                date = log[1]
                operation = log[2]
                variables = log[3]
                log_text = f"{db_id} | {date} | {operation} | {variables}"
                log_item = QListWidgetItem(log_text)
                log_item.setData(Qt.ItemDataRole.UserRole,db_id)
                self.logs_list.addItem(log_item)
        # add logs came from databasemanager

    # NewOperationUI.calculation_success --> AppManager --> DatabaseManager.save_log --> AppManager --> LogsUI.add_new_log
    def add_new_log(self,db_id : str, new_log : list):
        date = new_log[0]
        operation = new_log[1]
        variables = new_log[2]
        log_text = f"{db_id} | {date} | {operation} | {variables}"
        log_item = QListWidgetItem(log_text)
        log_item.setData(Qt.ItemDataRole.UserRole,db_id)
        self.logs_list.addItem(log_item)
        self.current_session_logs.append({"db_id" : db_id,"log_text": log_text})
        # add logs came from operation_ui

    # LogsUI.show_log_by_id.log_by_id_requested --> AppManager --> DatabaseManager_return_log_by_id --> AppManager --> LogsUI.show_log_by_id
    def show_log_by_id(self,item : QListWidgetItem):
        db_id = item.data(Qt.ItemDataRole.UserRole)
        self.log_by_id_requested.emit(str(db_id))

    # LogsUI.show_log_by_id.log_by_id_requested --> AppManager --> DatabaseManager_return_log_by_id --> AppManager --> LogsUI.init_history_ui --> AppManager --> MainUI.add_new_history_tab
    def init_history_ui(self,log_by_id : list):
        db_id = log_by_id[0]
        date = log_by_id[2]
        operation = log_by_id[3]
        variables = log_by_id[4]
        input_data = log_by_id[5].replace("{","").replace("}","")
        output = log_by_id[6]
        self.history_map = {
            "Population Mean" : MeanHistoryUI,
            "Sample Mean" : MeanHistoryUI,
            "Population Variance" : VarianceHistoryUI,
            "Sample Variance" : VarianceHistoryUI,
            "Population Standard Deviation" : StandardDeviationHistoryUI,
            "Sample Standard Deviation" : StandardDeviationHistoryUI,
            "Percentile" : PercentileHistoryUI,
            "Population Covariance" : CovarianceHistoryUI,
            "Sample Covariance" : CovarianceHistoryUI,
            "Correlation" : CorrelationHistoryUI,
            "Mutually Exclusive" : AdditionRuleHistoryUI,
            "Non Mutually Exclusive" : AdditionRuleHistoryUI,
            "Independent Events" : MultiplicationRuleHistoryUI,
            "Dependent Events" : MultiplicationRuleHistoryUI,
            "Bayes" : BayesHistoryUI,
            "Central Limit Theorem" : CentralLimitTheoremHistoryUI,
            "Confidence Interval" : ConfidenceIntervalHistoryUI,
            "Margin Of Error" : MarginOfErrorHistoryUI,
            "Bernoulli Distribution" : BernoulliDistributionHistoryUI,
            "Binomial Distribution" : BinomialDistributionHistoryUI,
            "Poisson Distribution PMF" : PoissonDistributionHistoryUI,
            "Poisson Distribution CDF" : PoissonDistributionHistoryUI,
            "Normal Distribution PDF" : NormalDistributionHistoryUI,
            "Normal Distribution CDF" : NormalDistributionHistoryUI,
            "Standard Normal Distribution" : StandardNormalDistributionHistoryUI,
            "Uniform Distribution PDF" : UniformDistributionHistoryUI,
            "Uniform Distribution CDF" : UniformDistributionHistoryUI,
            "Log Normal Distribution PDF" : LogNormalDistributionHistoryUI,
            "Log Normal Distribution CDF" : LogNormalDistributionHistoryUI,
            "Pareto Distribution PDF" : ParetoDistributionHistoryUI,
            "Pareto Distribution CDF" : ParetoDistributionHistoryUI,
            "Z Test" : zTestHistoryUI,
            "Single Sample t Test" : tTestHistoryUI,
            "Independent Sample t Test" : tTestHistoryUI,
            "Paired Sample t test" : tTestHistoryUI,
            "Chi Square Test" : ChiSquareTestHistoryUI,
            "ANOVA" : AnovaHistoryUI,
        }
        worker_class = self.history_map.get(operation)
        self.history_ui = worker_class(str(db_id),date,operation,variables,input_data,output)
        self.create_history_requested.emit([self.history_ui,operation])

    # self.current_session_logs --> self.logs_list
    def show_current_session_logs_function(self):
        self.logs_list.clear()
        for log in self.current_session_logs:
            log_item = QListWidgetItem(log["log_text"])
            log_item.setData(Qt.ItemDataRole.UserRole,log["db_id"])
            self.logs_list.addItem(log_item)
    
    # Clear Logs
    def clear_logs_button_function(self):
        self.logs_list.clear()
    
    
    