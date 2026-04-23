from PyQt6.QtCore import QSettings

class SettingsController():
    def __init__(self):
        self.init_settings()

    #                   INIT QSETTINGS
    def init_settings(self):
        self.laplace_settings = QSettings("LaplacesDemonOrg","LaplacesDemon")
        print("----------naked settings---------")
        print(self.get_auth_token())
        print(self.get_saved_username())
        print(self.get_remember_me_state())
        print(self.get_user_preferences())

    #                   SETTINGS GETTER
    def get_auth_token(self):
        return self.laplace_settings.value("auth_token", "", type=str)
    
    def get_saved_username(self):
        return self.laplace_settings.value("saved_username", "", type=str)

    def get_remember_me_state(self):
        return self.laplace_settings.value("remember_me", False, type=bool)
    
    def get_user_preferences(self):
        return self.laplace_settings.value("saved_preferences", [], type=list)

    #                   WIPE SETTINGS
    def wipe_settings(self):
        self.laplace_settings.setValue("remember_me", False)
        self.laplace_settings.setValue("saved_username", "")
        self.laplace_settings.setValue("auth_token", "")
        self.laplace_settings.setValue("saved_preferences",[])
        print(self.get_auth_token())
        print(self.get_saved_username())
        print(self.get_remember_me_state())
        print(self.get_user_preferences())
    #                   SAVE SETTINGS
    def save_settings(self,new_remember_me_state : bool,new_saved_username : str, new_auth_token : str, user_preferences : list):
        self.laplace_settings.setValue("remember_me", new_remember_me_state)
        self.laplace_settings.setValue("saved_username", new_saved_username)
        self.laplace_settings.setValue("auth_token", new_auth_token)
        self.laplace_settings.setValue("saved_preferences",user_preferences)

    def save_remember_me_state(self,new_remember_me_state : bool):
        print("\n")
        print("----- save remember me -----")
        print(new_remember_me_state)
        self.laplace_settings.setValue("remember_me", new_remember_me_state)

        print("----- get saved -----")
        print(self.laplace_settings.value("remember_me", False, type=bool))

        print("\n")

    def save_auth_token(self,new_auth_token : str):
        print("----- save auth token -----")
        print(new_auth_token)
        self.laplace_settings.setValue("auth_token", new_auth_token)

        print("----- get saved -----")
        print(self.laplace_settings.value("auth_token", "", type=str))

        print("\n")

    def save_new_saved_username(self,new_saved_username : str):
        print("----- save useranme -----")
        print(new_saved_username)
        self.laplace_settings.setValue("saved_username", new_saved_username)

        print("----- get saved -----")
        print(self.laplace_settings.value("saved_username", "", type=str))

        print("\n")

    def save_new_user_preferences(self,user_preferences : list):
        print("----- save preferences -----")
        print(user_preferences)
        self.laplace_settings.setValue("saved_preferences",user_preferences)

        print("----- get save -----")
        print(self.laplace_settings.value("saved_preferences", [], type=list))


    
