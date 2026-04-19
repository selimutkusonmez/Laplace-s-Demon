from PyQt6.QtCore import QObject
from src.ui.laplace_archive_ui import LaplaceArchiveUI

class ArchiveController(QObject):
    def __init__(self):
        super().__init__()