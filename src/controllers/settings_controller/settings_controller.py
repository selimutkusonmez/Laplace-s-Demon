from PyQt6.QtCore import QSettings

class SettingsController():
    def __init__(self):
        self.init_settings()

    #                   INIT QSETTINGS
    def init_settings(self):
        self.laplace_settings = QSettings("LaplacesDemonOrg","LaplacesDemon")

    #                   SETTINGS GETTER
    def get_auth_token(self):
        return self.laplace_settings.value("auth_token", "", type=str)

    def get_saved_username(self):
        return self.laplace_settings.value("saved_username", "", type=str)

    def get_remember_me_state(self):
        return self.laplace_settings.value("remember_me", False, type=bool)
    
    def get_user_preferences(self):
        return self.laplace_settings.value("saved_preferences", {}, type=dict)
    
    #                   WIPE SETTINGS
    def wipe_settings(self):
        self.laplace_settings.setValue("remember_me", False)
        self.laplace_settings.setValue("saved_username", "")
        self.laplace_settings.setValue("auth_token", "")
        self.laplace_settings.setValue("saved_preferences",{})

    #                   SAVE SETTINGS
    def save_settings(self,new_remember_me_state : bool,new_saved_username : str, new_auth_token : str, user_preferences : dict):
        self.laplace_settings.setValue("remember_me", new_remember_me_state)
        self.laplace_settings.setValue("saved_username", new_saved_username)
        self.laplace_settings.setValue("auth_token", new_auth_token)
        self.laplace_settings.setValue("saved_preferences",user_preferences)
