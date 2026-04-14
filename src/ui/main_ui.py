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
    log_out_requested = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.current_font_size = 20
        self.change_theme_function()

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


                            #Theme Menu
        theme_menu = settings_menu.addMenu("Theme")
        theme_action_group = QActionGroup(self)
        theme_action_group.triggered.connect(self.change_theme_action_function)

        #Dark Theme
        dark_theme_action = QAction("Dark Theme")
        dark_theme_action.setShortcut("Ctrl+D")
        dark_theme_action.setCheckable(True)
        dark_theme_action.setChecked(True)
        dark_theme_action.setData("dark_theme")
        theme_menu.addAction(dark_theme_action)
        theme_action_group.addAction(dark_theme_action)

        #Light Theme
        light_theme_action = QAction("Light Theme")
        light_theme_action.setShortcut("Ctrl+L")
        light_theme_action.setCheckable(True)
        light_theme_action.setData("light_theme")
        theme_menu.addAction(light_theme_action)
        theme_action_group.addAction(light_theme_action)


                            #Color Menu
        color_menu = settings_menu.addMenu("Font Color")
        color_action_group = QActionGroup(self)

        #Font Color
        change_color_action = QAction("Change Font Color")
        color_menu.addAction(change_color_action)
        color_action_group.addAction(change_color_action)
        change_color_action.triggered.connect(self.change_color_action_function)


                            #Language Menu
        language_menu = settings_menu.addMenu("Language")
        language_action_group = QActionGroup(self)
        language_action_group.triggered.connect(self.change_language_action_function)

        #English
        en_action = QAction("English")
        en_action.setCheckable(True)
        en_action.setChecked(True)
        en_action.setData("en")
        language_menu.addAction(en_action)
        language_action_group.addAction(en_action)

        #Deutch
        de_action = QAction("Deutch")
        de_action.setCheckable(True)
        language_menu.addAction(de_action)
        de_action.setData("de")
        language_action_group.addAction(de_action)

        #Turkish
        tr_action = QAction("Turkish")
        tr_action.setCheckable(True)
        language_menu.addAction(tr_action)
        tr_action.setData("tr")
        language_action_group.addAction(tr_action)


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
    def change_theme_action_function(self, action : QAction = None ):
        if action is None: 
            self.current_theme = "dark"
            self.setStyleSheet(read_style(self.current_theme))
        elif action.data() == "dark_theme":
            self.current_theme = "dark"
            self.setStyleSheet(read_style(self.current_theme))
        elif action.data() == "light_theme":
            self.current_theme = "light"
            self.setStyleSheet(read_style(self.current_theme))
        

    #Font Color Action Function
    def change_color_action_function(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.current_font_color = color.name()
            self.color_change_requested.emit(self.current_font_color)
        else:
            return
        
    def change_language_action_function(self, action : QAction):
        if action.data() == "en":
            print("en")
        elif action.data() == "de":
            print("de")
        else:
            print("tr")

    def init_profile_menu(self,current_user_name : str):
        #Profile Menu
        self.profile_button = QToolButton(self)
        self.profile_button.setText(current_user_name)
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
        print("about me")
    
    def preferences_action_function(self):
        print("preferences")
    
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
        if index != 0 and index != 1:
            self.central_widget.removeTab(index)

    # OperationsListingUI/AppManager --> MainUI.add_new_operation_tab
    def add_new_operation_tab(self, new_operation_ui : QWidget, new_operation_name : str):
        index = self.central_widget.addTab(new_operation_ui,new_operation_name)
        self.central_widget.setCurrentIndex(index)
    
    # LogsUI/AppManager --> MainUI.add_new_history_tab
    def add_new_history_tab(self, new_history_ui : QWidget ,new_history_name : str):
        self.central_widget.addTab(new_history_ui,new_history_name)