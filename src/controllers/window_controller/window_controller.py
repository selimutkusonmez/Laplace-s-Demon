from PyQt6.QtCore import QObject
from src.ui.main_ui import MainUI

class WindowController(QObject):
    def __init__(self):
        super().__init__()