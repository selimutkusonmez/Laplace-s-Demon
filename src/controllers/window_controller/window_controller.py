from PyQt6.QtCore import QObject,pyqtSignal
from src.ui.main_ui import MainUI
from src.ui.loading_curtain.loading_curtain import LoadingCurtain

class WindowController(QObject):

    preferences_ui_requested = pyqtSignal()
    about_me_ui_requested = pyqtSignal()

    log_out_requested = pyqtSignal()

    def __init__(self,saved_username,settings_controller):
        super().__init__()
        self.settings_controller = settings_controller
        self.saved_username = saved_username

    def init_loading_curtain(self):
        self.loading_curtain = LoadingCurtain()
        self.loading_curtain.setProperty("tab_id","curtain")

    def init_main_ui(self):

        self.main_ui = MainUI()

        self.main_ui.add_or_set_tab(self.loading_curtain,"Laplace's Demon","curtain")
        
        self.main_ui.preferences_ui_requested.connect(self.preferences_ui_requested)
        self.main_ui.about_me_ui_requested.connect(self.about_me_ui_requested)
        self.main_ui.log_out_requested.connect(self.log_out_requested)

    def handle_add_new_tab(self,widget, tab_text : str,tab_id ) -> None:
        self.main_ui.add_or_set_tab(widget,tab_text,tab_id)

    def handle_clear_tabs(self):
        self.main_ui.clear_tabs()

    def apply_user_preferences(self,saved_username,user_preferences):
        self.main_ui.apply_user_preferences(saved_username,user_preferences)

    def show_main_ui(self):
        self.main_ui.showMaximized()


    def handle_update_curtain(self,curtain_text : str):
        self.loading_curtain.update_curtain(curtain_text)

    def handle_log_out_request(self):
        self.log_out_requested.emit()

    def handle_init_profile_menu(self,username):
        if self.saved_username != "":
            self.main_ui.init_profile_menu(self.saved_username)
        else:
            self.main_ui.init_profile_menu(username)

    def handle_delete_profile_menu(self):
        self.main_ui.delete_profile_menu()

    def handle_preferred_languge_update(self,new_preferred_language : str):
        self.main_ui.change_preferred_language_function(new_preferred_language)
    
    def handle_preferred_theme_update(self,new_preferred_theme : str):
        self.main_ui.change_preferred_theme_function(new_preferred_theme)
    
    def handle_preferred_font_color_update(self,new_preferred_font_color : str):
        self.main_ui.change_preferred_font_color_function(new_preferred_font_color)

