from PyQt5 import QtCore, QtWidgets


class ModComboBox(QtWidgets.QComboBox):
    clicked = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.lineEdit().setAlignment(QtCore.Qt.AlignHCenter)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)
