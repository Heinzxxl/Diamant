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

    def addfig(self, fig):
        self.canvas = FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()
        self.toolbar = NavigationToolbar(self.canvas,
                                         self.mplwidget, coordinates=True)
        self.mplvl.addWidget(self.toolbar)


fig1 = Figure()
ax1f1 = fig1.add_subplot(111)
ax1f1.plot(np.random.rand(5))
fig1.set_tight_layout(True)

app = QtWidgets.QApplication([])
application = MyWindow()
application.addfig(fig1)
application.show()

sys.exit(app.exec())
