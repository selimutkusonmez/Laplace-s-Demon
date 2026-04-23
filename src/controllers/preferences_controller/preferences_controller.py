from PyQt6.QtCore import QObject,pyqtSignal
from PyQt6.QtWidgets import QWidget
from src.ui.profile.preferences.preferences_ui import PreferencesUI
from src.core.task_worker.task_worker import TaskWorker

class PreferencesController(QObject):

    ui_route_requested = pyqtSignal(QWidget,str,str)
    preferred_language_update_requested = pyqtSignal(str)
    preferred_theme_update_requested = pyqtSignal(str)
    preferred_font_color_update_requested = pyqtSignal(str)
    remember_me_state_update_requested = pyqtSignal(bool)

    def __init__(self,database_manager,thread_pool,settings_controller,username,user_preferences,remember_me_state,auth_token):
        super().__init__()
        self.database_manager = database_manager
        self.thread_pool = thread_pool
        self.settings_controller = settings_controller
        self.username = username
        self.user_preferences = user_preferences
        self.remember_me_state = remember_me_state
        self.auth_token = auth_token

    def handle_apply_preferences(self):
        self.preferences_ui.set_preferences(self.user_preferences,self.remember_me_state)

    def init_preferences_ui(self):
        self.preferences_ui = PreferencesUI()

        self.preferences_ui.preferred_language_update_requested.connect(self.handle_referred_language_update)
        self.preferences_ui.preferred_language_update_requested.connect(self.preferred_language_update_requested)

        self.preferences_ui.preferred_theme_update_requested.connect(self.handle_preferred_theme_update)
        self.preferences_ui.preferred_theme_update_requested.connect(self.preferred_theme_update_requested)

        self.preferences_ui.preferred_font_color_update_requested.connect(self.handle_preferred_font_color_update)
        self.preferences_ui.preferred_font_color_update_requested.connect(self.preferred_font_color_update_requested)

        self.preferences_ui.remember_me_state_update_requested.connect(self.handle_remember_state_update)

        self.preferences_ui.setProperty("tab_id","preferences")

        self.handle_apply_preferences()

        self.ui_route_requested.emit(self.preferences_ui,"Preferences","preferences")


    def handle_referred_language_update(self, new_prefered_language : str):
        self.user_preferences[0] = new_prefered_language
        self.settings_controller.save_new_user_preferences(self.user_preferences)
        worker = TaskWorker(self.database_manager.update_preferred_language,self.username,new_prefered_language)
        self.thread_pool.start(worker)

    def handle_preferred_theme_update(self, new_prefered_theme : str):
        self.user_preferences[1] = new_prefered_theme
        self.settings_controller.save_new_user_preferences(self.user_preferences)
        worker = TaskWorker(self.database_manager.update_preferred_theme,self.username,new_prefered_theme)
        self.thread_pool.start(worker)
        
    def handle_preferred_font_color_update(self, new_prefered_font_color : str):
        self.user_preferences[2] = new_prefered_font_color
        self.settings_controller.save_new_user_preferences(self.user_preferences)
        worker = TaskWorker(self.database_manager.update_preferred_font_color,self.username,new_prefered_font_color)
        self.thread_pool.start(worker)

    def handle_remember_state_update(self,new_remember_state : bool):
        if new_remember_state:
            self.settings_controller.save_remember_me_state(new_remember_state)
            self.settings_controller.save_auth_token(self.auth_token)
            self.settings_controller.save_new_saved_username(self.username)
        else:
            self.settings_controller.wipe_settings()

        
