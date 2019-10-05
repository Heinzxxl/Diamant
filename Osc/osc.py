from PyQt5 import QtWidgets, uic
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
import numpy as np
import sys

Ui_MainWindow, QMainWindow = uic.loadUiType('osc.ui')


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.isRunning = True
        self.RSButton.clicked.connect(self.rschange)

    def addfig(self, fig):
        self.canvas = FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()
        self.toolbar = NavigationToolbar(self.canvas,
                                         self.mplwidget, coordinates=True)
        self.mplvl.addWidget(self.toolbar)

    # function for button disconnection
    def cldisconnect(self, button):
        try:
            self.button.clicked.disconnect()
        except Exception:
            pass

    # temp function for testing
    def rschange(self):
        if self.isRunning:
            self.rsLabel.setText('Stop')
            self.cldisconnect(self.thatButton1)
            self.thatButton1.clicked.connect(self.tempslot1)
            self.isRunning = False
        else:
            self.rsLabel.setText('Run')
            self.cldisconnect(self.thatButton1)
            self.thatButton1.clicked.connect(self.tempslot2)
            self.isRunning = True

    # temp function for testing
    def tempslot1(self):
        self.thatButton2.setText("Push me")
        self.thatButton3.setText("")

    def tempslot2(self):
        self.thatButton2.setText("")
        self.thatButton3.setText("Push me")


fig1 = Figure()
ax1f1 = fig1.add_subplot(111)
ax1f1.plot(np.random.rand(5))
fig1.set_tight_layout(True)

app = QtWidgets.QApplication([])
application = MyWindow()
application.addfig(fig1)
application.show()

sys.exit(app.exec())
