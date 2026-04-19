from PyQt6.QtCore import QRunnable,pyqtSlot,QObject,pyqtSignal

class DatabaseWorkerSignals(QObject):
    result = pyqtSignal(object)
    error = pyqtSignal(str)

class TaskWorker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = DatabaseWorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
            self.signals.result.emit(result)
        except Exception as e:
            self.signals.error.emit(str(e))