import importlib
import os
from PyQt6.QtCore import QSize,pyqtSignal,Qt
from PyQt6.QtWidgets import QWidget,QListWidget,QHBoxLayout,QListWidgetItem,QMessageBox
from PyQt6.QtGui import QIcon


from config import JPG_PATH

class OperationsListingUI(QWidget):

    new_operation_requested = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.icons_dir = os.path.join(JPG_PATH,"icons")
        self.init_ui()
     
    def init_ui(self):
        
        #object name and styling background permit granted
        self.setProperty("class","ui")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        #Layout created
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # Subjects Dict
        self.subjects_dict = {
                                "Statistics" : [
                                        ["Mean","Population Mean","Sample Mean"],
                                        ["Variance","Population Variance","Sample Variance"],
                                        ["Standard Deviation","Population Standard Deviation", "Sample Standard Deviation"],
                                        ["Percentile","Percentile"],
                                        ["Covariance","Population Covariance","Sample Covariance"],
                                        ["Correlation","Correlation"],
                                ],

                                "Probability" : [
                                        ["Addition Rule","Mutually Exclusive","Non Mutually Exclusive"],
                                        ["Multiplication Rule","Independent Events", "Dependent Events"],
                                        ["Bayes","Bayes"],
                                ],

                                "Estimation & Theory": [
                                        ["Central Limit Theorem","Central Limit Theorem"],
                                        ["Confidence Interval","Confidence Interval"],
                                        ["Margin Of Error","Margin Of Error"],
                                ],

                                "Distribution Functions" : [
                                        ["Bernoulli Distribution","Bernoulli Distribution"],
                                        ["Binomial Distribution","Binomial Distribution"],
                                        ["Poisson Distribution","Poisson Distribution PMF","Poisson Distribution CDF"],
                                        ["Normal Distribution","Normal Distribution PDF","Normal Distribution CDF"],
                                        ["Standard Normal Distribution","Standard Normal Distribution"],
                                        ["Uniform Distribution","Uniform Distribution PDF","Uniform Distribution CDF"],
                                        ["Log Normal Distribution","Log Normal Distribution PDF","Log Normal Distribution CDF"],
                                        ["Pareto Distribution","Pareto Distribution PDF","Pareto Distribution CDF"],
                                ],

                                "Hypothesis Tests" : [
                                        ["Z Test","Z Test"],
                                        ["t Test","Single Sample t Test","Independent Sample t Test","Paired Sample t test"],
                                        ["Chi Square Test","Chi Square Test"],
                                        ["ANOVA","ANOVA"],
                                ],
                                }
          
        # First Layer of Dict
        self.subjects_list_1 = QListWidget()
        self.subjects_list_1.setProperty("class","list")
        self.subjects_list_1.setIconSize(QSize(150,150))
        self.subjects_list_1.itemDoubleClicked.connect(self.subjects_list_1_item_double_clicked)
        self.layout.addWidget(self.subjects_list_1)

        # Applying Icons
        for key in self.subjects_dict.keys():
            list_1_item = QListWidgetItem(key)
            icon = self.get_icon(key,"main_subjects")
            list_1_item.setIcon(icon)
            self.subjects_list_1.addItem(list_1_item)

    # When first layer item is chosed find it on the dict and bring the second layer
    def subjects_list_1_item_double_clicked(self,item):
        # if already remove them
        if hasattr(self, "subjects_list_3"):
            try:
                self.layout.removeWidget(self.subjects_list_3)
                self.subjects_list_3.deleteLater()
                del self.subjects_list_3
            except :
                pass
          
        if hasattr(self, "subjects_list_2"):
            try:
                self.layout.removeWidget(self.subjects_list_2)
                self.subjects_list_2.deleteLater()
                del self.subjects_list_2
            except : 
                pass
        
        #subjects_list_2 created and connected to the func
        self.subjects_list_2 = QListWidget()
        self.subjects_list_2.setProperty("class","list")
        self.subjects_list_2.setIconSize(QSize(150,150))
        self.subjects_list_2.itemDoubleClicked.connect(self.subjects_list_2_item_double_clicked)
        self.layout.addWidget(self.subjects_list_2)

        self.main_subject = item.text()
        
        # sub subjects added to the subjects_list_2 with icons
        for i in self.subjects_dict[item.text()]:
            list_2_item = QListWidgetItem(i[0])
            icon = self.get_icon(i[0],"sub_subjects")
            list_2_item.setIcon(icon)
            self.subjects_list_2.addItem(list_2_item)

    # When second layer item is chosed find it on the dict and bring the third layer
    def subjects_list_2_item_double_clicked(self,item):
        if hasattr(self, "subjects_list_3"):
            try:
                self.layout.removeWidget(self.subjects_list_3)
                self.subjects_list_3.deleteLater()
                del self.subjects_list_3
            except :
                pass

        #subjects_list_2 created and connected to the func  
        self.subjects_list_3 = QListWidget()
        self.subjects_list_3.setProperty("class","list")
        self.subjects_list_3.setIconSize(QSize(150,150))
        self.subjects_list_3.itemDoubleClicked.connect(self.subjects_list_3_item_double_clicked)
        self.layout.addWidget(self.subjects_list_3)

        self.sub_subject = item.text()

        # operations added to the subjects_list_3 with icons
        for i in self.subjects_dict[self.main_subject][self.subjects_list_2.row(item)][1:]:
            list_3_item = QListWidgetItem(i)
            icon = self.get_icon("operations","operations")
            list_3_item.setIcon(icon)
            self.subjects_list_3.addItem(list_3_item)


    # When third layer item is chosed find it on the dict, import it and send it to the appmanager
    def subjects_list_3_item_double_clicked(self,item):
        operation_name = item.text()
        main_folder = self.main_subject.lower().replace(" ","_")
        sub_folder = self.sub_subject.lower().replace(" ","_")
        file_name = operation_name.lower().replace(" ","_")
        
        #module_path glued together
        module_path = f"src.ui.operation_ui.{main_folder}_operations_ui.{sub_folder}.{file_name}_ui"

        try:
            #module imported
            module = importlib.import_module(module_path)
            widget = module.OperationUI(operation_name)

            # OperationListingUI.new_operation_requested --> AppManager/MainUI
            self.new_operation_requested.emit([widget,operation_name])

        except Exception as e:
            QMessageBox.critical(self, "Module Error", f"Could not load operation:\n{str(e)}")

    # get icon
    def get_icon(self, name, sub_folder):
        safe_name = name.lower().replace(" ", "_") + ".png"
        icon_path = os.path.join(self.icons_dir, sub_folder, safe_name)
        if os.path.exists(icon_path):
            return QIcon(icon_path)
        else:
            return QIcon()
