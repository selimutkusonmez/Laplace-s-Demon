import sys
import os
import subprocess
from PyQt6.QtCore import pyqtSignal,Qt
from PyQt6.QtWidgets import QApplication,QMainWindow,QMessageBox,QTabWidget,QStatusBar,QColorDialog,QWidget,QToolButton,QMenu
from PyQt6.QtGui import QAction,QActionGroup,QIcon
from src.assets.style.style_reader.style_reader import read_style
from config import JPG_PATH

class MainUI(QMainWindow):
    color_change_requested = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.current_font_size = 20
        self.dark_theme_action_function()

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

        #StatusBar
        self.setStatusBar(QStatusBar())

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

        #Settings Menu
        settings_menu = menu_bar.addMenu("Settings")

        theme_menu = settings_menu.addMenu("Theme")
        theme_action_group = QActionGroup(self)

        color_menu = settings_menu.addMenu("Font Color")
        color_action_group = QActionGroup(self)

        #Light Theme
        light_theme_action = QAction("Light Theme")
        light_theme_action.setShortcut("Ctrl+L")
        light_theme_action.setCheckable(True)
        theme_menu.addAction(light_theme_action)
        theme_action_group.addAction(light_theme_action)
        light_theme_action.triggered.connect(self.light_theme_action_function)

        #Dark Theme
        dark_theme_action = QAction("Dark Theme")
        dark_theme_action.setShortcut("Ctrl+D")
        dark_theme_action.setCheckable(True)
        dark_theme_action.setChecked(True)
        theme_menu.addAction(dark_theme_action)
        theme_action_group.addAction(dark_theme_action)
        dark_theme_action.triggered.connect(self.dark_theme_action_function)

        #Font Color
        change_color_action = QAction("Change Font Color")
        color_menu.addAction(change_color_action)
        color_action_group.addAction(change_color_action)
        change_color_action.triggered.connect(self.change_color_action_function)

        #Profile Menu
        self.profile_button = QToolButton()
        self.profile_button.setText("Profile")
        self.profile_button.setAutoRaise(True)
        self.profile_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        self.profile_menu = QMenu()

        about_me_action = QAction("About Me",self)
        self.profile_menu.addAction(about_me_action)

        preferences_action = QAction("Preferences",self)
        self.profile_menu.addAction(preferences_action)

        self.profile_menu.addSeparator()

        log_out_action = QAction("Log Out",self)
        self.profile_menu.addAction(log_out_action)

        self.profile_button.setMenu(self.profile_menu)

        self.menuBar().setCornerWidget(self.profile_button, Qt.Corner.TopRightCorner)


    #About Action Function
    def about_action_function(self):
        about_text = """
        <h2>Laplace's Demon/h2>
        <p>/p>
        """
        QMessageBox.about(self, "About Statistical Calculator", about_text) 

    #Restart App(Ctrl+R) Action Function
    def restart_app_action_function(self):
        QApplication.quit()
        subprocess.Popen([sys.executable, *sys.argv])

    #Close Tab(Ctrl+W) Action Function
    def close_tab_action_function(self):
        current_index = self.central_widget.currentIndex()
        if current_index != 0 and current_index != 1:
            self.central_widget.removeTab(self.central_widget.currentIndex())

    # Light Action Function
    def light_theme_action_function(self):
        self.current_theme = "light"
        self.setStyleSheet(read_style(self.current_theme))

    # Dark Action Function
    def dark_theme_action_function(self):
        self.current_theme = "dark"
        self.setStyleSheet(read_style(self.current_theme))  

    #Font Color Action Function
    def change_color_action_function(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.current_font_color = color.name()
            self.color_change_requested.emit(self.current_font_color)
        else:
            return

    # Central Widget Tab Close Function
    def central_widget_tab_close_function(self,index):
        if index != 0 and index != 1:
            self.central_widget.removeTab(index)

    # OperationsListingUI/AppManager --> MainUI.add_new_operation_tab
    def add_new_operation_tab(self, new_operation_ui : QWidget, new_operation_name : str):
        index = self.central_widget.addTab(new_operation_ui,new_operation_name)
        self.central_widget.setCurrentIndex(index)
    
    # LogsUI/AppManager --> MainUI.add_new_history_tab
    def add_new_history_tab(self, new_history_ui : QWidget ,new_history_name : str):
        self.central_widget.addTab(new_history_ui,new_history_name)