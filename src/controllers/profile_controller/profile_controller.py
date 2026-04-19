from PyQt6.QtCore import QObject
from src.ui.profile.about_me.about_me_ui import AboutMeUI

class ProfileController(QObject):
    def __init__(self):
        super().__init__()