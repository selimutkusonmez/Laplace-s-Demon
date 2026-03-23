from PyQt6.QtCore import Qt, QAbstractTableModel

class ListTableModel(QAbstractTableModel):
    def __init__(self, data_list : str):
        super().__init__()
        self._data = data_list.split(",")


    def rowCount(self, parent=None):
        if self._data:
            return len(self._data)
        return 0

    def columnCount(self, parent=None):
        return 1

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
            
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._data[index.row()])
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return "data"
            elif orientation == Qt.Orientation.Vertical:
                return str(section)
        return None