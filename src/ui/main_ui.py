import sys
import os
import subprocess
from PyQt6.QtCore import pyqtSignal,Qt
from PyQt6.QtWidgets import QApplication,QMainWindow,QMessageBox,QTabWidget,QStatusBar,QColorDialog,QWidget,QToolButton,QMenu
from PyQt6.QtGui import QAction,QActionGroup,QIcon
from src.assets.style.style_reader.style_reader import read_style
from config import JPG_PATH

from src.ui.profile.about_me.about_me_ui import AboutMeUI
from src.ui.profile.preferences.preferences_ui import PreferencesUI

class MainUI(QMainWindow):

    color_change_requested = pyqtSignal(str)
    log_out_requested = pyqtSignal()

    #PreferencesUI.signals --> MainUI.signals --> AppManager --> DatabaseManager
    change_preferred_language_request = pyqtSignal(str)
    change_preferred_theme_request = pyqtSignal(str)
    change_preferred_font_color_request = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.current_font_size = 20
        self.change_preferred_theme_function()

    def init_ui(self):
        
        self.setMinimumSize(1000,550)
        self.setWindowTitle("Laplace's Demon")
        logo_path = os.path.join(JPG_PATH,"logo","logo.png")
        self.setWindowIcon(QIcon(logo_path))
        self.setObjectName("main_ui")

        #Central Widget
        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)

        self.central_widget.setTabsClosable(True)
        self.central_widget.tabCloseRequested.connect(self.central_widget_tab_close_function)   
           
        #MenuBar
        menu_bar = self.menuBar()

                            #File Menu
        file_menu = menu_bar.addMenu("File")

        about_action = QAction("About",self)
        about_action.triggered.connect(self.about_action_function)
        file_menu.addAction(about_action)

        restart_app_action = QAction("Restart App",self)
        restart_app_action.setShortcut("Ctrl+R")
        restart_app_action.triggered.connect(self.restart_app_action_function)
        file_menu.addAction(restart_app_action)

        close_tab_action = QAction("Close Tab",self)
        file_menu.addAction(close_tab_action)
        close_tab_action.setShortcut("Ctrl+W")
        close_tab_action.triggered.connect(self.close_tab_action_function)

    #About Action Function
    def about_action_function(self):
        about_text = """
                    <h2>Laplace's Demon/h2>
                    """
        QMessageBox.about(self, "", about_text) 

    #Restart App(Ctrl+R) Action Function
    def restart_app_action_function(self):
        QApplication.quit()
        subprocess.Popen([sys.executable, *sys.argv])

    #Close Tab(Ctrl+W) Action Function
    def close_tab_action_function(self):
        current_index = self.central_widget.currentIndex()
        if current_index != 0 and current_index != 1:
            self.central_widget.removeTab(self.central_widget.currentIndex())

    #Change Theme Function
    def change_preferred_theme_function(self,preferred_theme : str = None):
        if preferred_theme is None: 
            self.current_theme = "dark"
            self.setStyleSheet(read_style(self.current_theme))
        elif preferred_theme == "dark":
            self.current_theme = "dark"
            self.setStyleSheet(read_style(self.current_theme))
        elif preferred_theme == "light":
            self.current_theme = "light"
            self.setStyleSheet(read_style(self.current_theme))
        
    #Font Color Action Function
    def change_preferred_font_color_function(self,preferred_color : str):
        self.color_change_requested.emit(preferred_color)
        
    def change_preferred_language_function(self,preferred_language : str):
        if preferred_language == "en":
            print("en")
        elif preferred_language == "de":
            print("de")
        else:
            print("tr")


    def init_profile_menu(self,current_user : str):

        self.current_user = current_user

        #Profile Menu
        self.profile_button = QToolButton(self)
        self.profile_button.setText(self.current_user)
        self.profile_button.setAutoRaise(True)
        self.profile_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        self.profile_menu = QMenu()

        self.about_me_action = QAction("About Me",self)
        self.about_me_action.triggered.connect(self.about_me_action_function)
        self.profile_menu.addAction(self.about_me_action)

        self.preferences_action = QAction("Preferences",self)
        self.preferences_action.triggered.connect(self.preferences_action_function)
        self.profile_menu.addAction(self.preferences_action)

        self.profile_menu.addSeparator()

        self.log_out_action = QAction("Log Out",self)
        self.log_out_action.triggered.connect(self.log_out_action_function)
        self.profile_menu.addAction(self.log_out_action)

        self.profile_button.setMenu(self.profile_menu)

        self.menuBar().setCornerWidget(self.profile_button, Qt.Corner.TopRightCorner)

        self.profile_button.show()

    def about_me_action_function(self):
        about_me_ui = AboutMeUI(self.current_user)
        index = self.central_widget.addTab(about_me_ui,"About Me")
        self.central_widget.setCurrentIndex(index)
    
    def preferences_action_function(self):
        preferences_ui = PreferencesUI()

        preferences_ui.change_preferred_language_request.connect(self.change_preferred_language_function)
        preferences_ui.change_preferred_language_request.connect(self.change_preferred_language_request)
        
        preferences_ui.change_preferred_theme_request.connect(self.change_preferred_theme_function)
        preferences_ui.change_preferred_theme_request.connect(self.change_preferred_theme_request)

        preferences_ui.change_preferred_font_color_request.connect(self.change_preferred_font_color_function)
        preferences_ui.change_preferred_font_color_request.connect(self.change_preferred_font_color_request)

        index = self.central_widget.addTab(preferences_ui,"Preferences")
        self.central_widget.setCurrentIndex(index)
    
    #Log Out Action Function
    def log_out_action_function(self):
        while self.central_widget.count() > 0:
            widget = self.central_widget.widget(0)
            self.central_widget.removeTab(0)
            if widget is not None:
                widget.deleteLater()
                
        if hasattr(self, 'profile_button') and self.profile_button is not None:
            self.menuBar().setCornerWidget(None, Qt.Corner.TopRightCorner)
            self.profile_button.deleteLater()
            
        self.log_out_requested.emit()

    # Central Widget Tab Close Function
    def central_widget_tab_close_function(self,index):
        self.central_widget.removeTab(index)

    # OperationsListingUI/AppManager --> MainUI.add_new_operation_tab
    def add_new_operation_tab(self, new_operation_ui : QWidget, new_operation_name : str):
        index = self.central_widget.addTab(new_operation_ui,new_operation_name)
        self.central_widget.setCurrentIndex(index)
    
    # LogsUI/AppManager --> MainUI.add_new_history_tab
    def add_new_history_tab(self, new_history_ui : QWidget ,new_history_name : str):
        self.central_widget.addTab(new_history_ui,new_history_name)

    def add_create_new_account_tab(self, create_new_account_ui : QWidget):
        index = self.central_widget.addTab(create_new_account_ui,"Create An Account")
        self.central_widget.setCurrentIndex(index)