from PyQt6.QtCore import QObject
from src.ui.profile.preferences.preferences_ui import PreferencesUI

class PreferencesController(QObject):
    def __init__(self):
        super().__init__()