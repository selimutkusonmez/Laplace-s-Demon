import sys
import os
import subprocess
from PyQt6.QtCore import pyqtSignal,Qt
from PyQt6.QtWidgets import QApplication,QMainWindow,QMessageBox,QTabWidget,QStatusBar,QColorDialog,QWidget,QToolButton,QMenu,QTabBar
from PyQt6.QtGui import QAction,QActionGroup,QIcon
from src.assets.style.style_reader.style_reader import read_style
from config import JPG_PATH

from src.ui.profile.about_me.about_me_ui import AboutMeUI
from src.ui.profile.preferences.preferences_ui import PreferencesUI

class MainUI(QMainWindow):

    preferences_ui_requested = pyqtSignal()
    about_me_ui_requested = pyqtSignal()

    log_out_requested = pyqtSignal()
    

    def __init__(self):
        super().__init__()
        self.init_ui()

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


    #                   FILE MENU
    def about_action_function(self):
        about_text = """
                    <h2>Laplace's Demon/h2>
                    """
        QMessageBox.about(self, "", about_text) 

    def restart_app_action_function(self):
        QApplication.quit()
        subprocess.Popen([sys.executable, *sys.argv])

    def close_tab_action_function(self):
        current_index = self.central_widget.currentIndex()
        if current_index != 0 and current_index != 1:
            self.central_widget.widget(current_index).deleteLater()
            self.central_widget.removeTab(current_index)
            


    #                   PROFILE MENU
    def init_profile_menu(self,username : str):

        #Profile Menu
        self.profile_button = QToolButton(self)
        self.profile_button.setText(username)
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

    def delete_profile_menu(self):
        if hasattr(self, 'profile_button') and self.profile_button is not None:
            self.menuBar().setCornerWidget(None, Qt.Corner.TopRightCorner)
            self.profile_button.deleteLater()

    #                   ABOUT ME UI
    def about_me_action_function(self):
        self.about_me_ui_requested.emit()


    #                   PREFERENCES UI

    #PreferencesUI.save_preferred_language.change_preferred_language_request --> MainUI.change_preferred_language_function
    def change_preferred_language_function(self,preferred_language : str):
        if preferred_language == "en":
            return
        elif preferred_language == "de":
            return
        else:
            return

    #PreferencesUI.save_preferred_theme.change_preferred_theme_request --> MainUI.change_preferred_theme_function
    def change_preferred_theme_function(self,preferred_theme : str):
        if preferred_theme is None: 
            self.current_theme = "dark"
            self.setStyleSheet(read_style(self.current_theme))
        elif preferred_theme == "dark":
            self.current_theme = "dark"
            self.setStyleSheet(read_style(self.current_theme))
        elif preferred_theme == "light":
            self.current_theme = "light"
            self.setStyleSheet(read_style(self.current_theme))
        
    #PreferencesUI.save_preferred_language.change_preferred_font_color_request --> MainUI.change_preferred_font_color_function
    def change_preferred_font_color_function(self,preferred_color : str):
        return
        self.color_change_requested.emit(preferred_color)

    def preferences_action_function(self):
        self.preferences_ui_requested.emit()

    def apply_user_preferences(self,saved_username,user_preferences):
        if saved_username != "":
            self.change_preferred_language_function(user_preferences[0])
            self.change_preferred_theme_function(user_preferences[1])
            self.change_preferred_font_color_function(user_preferences[2])
        else:
            self.change_preferred_language_function("en")
            self.change_preferred_theme_function("dark")
            self.change_preferred_font_color_function("black")


    #                   CENTRAL WIDGET FUNCTIONS

    #                   NEW TAB FUNCTION
    def add_or_set_tab(self, widget : QWidget, tab_text : str,tab_id):
        if tab_id == "login":
            self.clear_tabs()
            self.central_widget.addTab(widget, tab_text)
            self.central_widget.tabBar().setTabButton(0, QTabBar.ButtonPosition.RightSide, None)
            return

        widget.setProperty("tab_id",tab_id)
        for i in range(self.central_widget.count()):
            existing_widget = self.central_widget.widget(i)
            existing_tab_id = existing_widget.property("tab_id")
            if existing_tab_id == tab_id:
                self.central_widget.setCurrentIndex(i)
                widget.deleteLater()
                return         
                  
        if widget.property("tab_id") in ["library","archive","curtain"]:
            self.central_widget.addTab(widget, tab_text)
            self.central_widget.tabBar().setTabButton(0, QTabBar.ButtonPosition.RightSide, None)
            self.central_widget.tabBar().setTabButton(1, QTabBar.ButtonPosition.RightSide, None)

        else:
            index = self.central_widget.addTab(widget, tab_text)
            self.central_widget.setCurrentIndex(index)

    #                   CLOSE TAB
    def central_widget_tab_close_function(self,index : int):
        self.central_widget.widget(index).deleteLater()
        self.central_widget.removeTab(index)

    #                   CLEAR TABS
    def clear_tabs(self):
        for i in range(self.central_widget.count()):
            self.central_widget.widget(i).deleteLater()
        self.central_widget.clear()

    #                   LOG OUT
    def log_out_action_function(self):          
        self.log_out_requested.emit()

    
