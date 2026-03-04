import sys
import os
import subprocess
from PyQt6.QtWidgets import (
     QApplication,QMainWindow,QMessageBox,QTabWidget,QStatusBar,QColorDialog)
from PyQt6.QtGui import QAction,QActionGroup,QIcon
from src.assets.style.style_reader.style_reader import read_style
from config import JPG_PATH

class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.current_theme = "dark"
        self.current_font_size = 20
        self.current_font_color = "#E6DACA"
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

        font_menu = settings_menu.addMenu("Font Size")
        font_action_group = QActionGroup(self)

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

        #Increase Font Size
        increase_font_size_action = QAction("Increase Font Size")
        increase_font_size_action.setShortcut("Ctrl++")
        font_menu.addAction(increase_font_size_action)
        font_action_group.addAction(increase_font_size_action)
        increase_font_size_action.triggered.connect(self.increase_font_size_action_function)

        #Decrease Font Size
        decrease_font_size_action = QAction("Decrease Font Size")
        decrease_font_size_action.setShortcut("Ctrl+-")
        font_menu.addAction(decrease_font_size_action)
        font_action_group.addAction(decrease_font_size_action)
        decrease_font_size_action.triggered.connect(self.decrease_font_size_action_function)

        #Font Color
        change_color_action = QAction("Change Font Color")
        color_menu.addAction(change_color_action)
        color_action_group.addAction(change_color_action)
        change_color_action.triggered.connect(self.change_color_action_function)


    #About Action Function
    def about_action_function(self):
        about_text = """
        <h2>Statistical Calculator v1.0</h2>
        <p>A comprehensive and interactive statistical analysis tool designed to simplify complex calculations. From basic descriptive statistics to advanced hypothesis testing, this application provides accurate results alongside real-time dynamic formula rendering.</p>
        <p><b>Developer:</b> Selim Utku Sönmez, Computer Engineering Student<br>
        <b>Powered by:</b> Python, PyQt6</p>
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
        if self.current_font_color == "#ADBAC7":
            self.current_font_color = "#24292F"
        self.setStyleSheet(read_style(self.current_theme,self.current_font_size,self.current_font_color))

    # Dark Action Function
    def dark_theme_action_function(self):
        self.current_theme = "dark"
        if self.current_font_color =="#24292F" :
            self.current_font_color = "#ADBAC7"
        self.setStyleSheet(read_style(self.current_theme,self.current_font_size,self.current_font_color))  

    #Increase Font Size Action Functions
    def increase_font_size_action_function(self):
        if 25 <= self.current_font_size < 60:
            self.current_font_size += 1
        else:
            return
        self.setStyleSheet(read_style(self.current_theme,self.current_font_size,self.current_font_color))

    #Decrease Font Size Action Function
    def decrease_font_size_action_function(self):
        if 25 < self.current_font_size <= 60:
            self.current_font_size -= 1
        else:
            return
        self.setStyleSheet(read_style(self.current_theme,self.current_font_size,self.current_font_color))

    #Font Color Action Function
    def change_color_action_function(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.current_font_color = color.name()
            self.setStyleSheet(read_style(self.current_theme,self.current_font_size,self.current_font_color))
        else:
            return


    # Central Widget Tab Close Function
    def central_widget_tab_close_function(self,index):
        return

    #Add New Operation Tab
    def add_new_operation_tab(self,new_operation_ui,new_operation_name):
        return
    
    #Add New History Tab
    def add_new_history_tab(self,new_history_ui,new_history_name):
        return