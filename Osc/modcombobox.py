from PyQt5 import QtCore, QtWidgets


class ModComboBox(QtWidgets.QComboBox):
    clicked = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.signalClickedIsConnected = False
        self.signalActivatedIsConnected = False

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)
