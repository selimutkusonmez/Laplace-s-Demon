import sys
import traceback
from PyQt6.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal

class WorkerSignals(QObject):
    result = pyqtSignal(object)
    error = pyqtSignal(tuple)

class TaskWorker(QRunnable):
    def __init__(self, fn, *args):
        super().__init__()
        self.fn = fn
        self.args = args
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            # The *self.args magic unpacks the variables 
            # exactly as you passed them in the Controller.
            result = self.fn(*self.args)
        except:
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)