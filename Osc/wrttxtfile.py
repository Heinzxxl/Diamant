from PyQt5 import QtCore


class WrtTxtFile(QtCore.QObject):

    inputDone = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        
    def write_shot(self):
        self.logtxtFile.write(self.data)
        self.logtxtFile.write('\n')
        self.inputDone.emit()