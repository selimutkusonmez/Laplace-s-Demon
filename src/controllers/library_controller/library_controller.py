from PyQt6.QtCore import QObject
from src.ui.laplace_library_ui import LaplaceLibraryUI

class LibraryController(QObject):
    def __init__(self):
        super().__init__()