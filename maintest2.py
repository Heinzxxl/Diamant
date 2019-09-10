from PyQt5 import QtWidgets, QtGui, uic
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
import numpy as np
import sys

Ui_MainWindow, QMainWindow = uic.loadUiType('test2.ui')


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.figdict = {}

        self.mpllist.itemClicked.connect(self.changefig)
        self.nameButton.clicked.connect(self.changehello)
        self.quitButton.clicked.connect(self.close)

        fig = Figure()
        self.addfig(fig)

    def addfig(self, fig):
        self.canvas = FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()
        self.toolbar = NavigationToolbar(self.canvas,
                                         self.mplwindow, coordinates=True)
        self.mplvl.addWidget(self.toolbar)

    def rmfig(self):
        self.mplvl.removeWidget(self.canvas)
        self.canvas.close()
        self.mplvl.removeWidget(self.toolbar)
        self.toolbar.close()

    def addtolist(self, name, fig):
        self.figdict[name] = fig
        self.mpllist.addItem(name)

    def changefig(self, item):
        text = item.text()
        self.rmfig()
        self.addfig(self.figdict[text])

    def changehello(self):
        name = self.nameEdit.text()
        self.helloLabel.setText('Glad to see you, '+name+'!')
        self.helloLabel.setFont(QtGui.QFont('Sans serif', 10))


fig1 = Figure()
ax1f1 = fig1.add_subplot(111)
ax1f1.plot(np.random.rand(5))

fig2 = Figure()
ax1f2 = fig2.add_subplot(121)
ax1f2.plot(np.random.rand(5))
ax2f2 = fig2.add_subplot(122)
ax2f2.plot(np.random.rand(5))

app = QtWidgets.QApplication([])
application = MyWindow()
application.addtolist('Figure 1', fig1)
application.addtolist('Figure 2', fig2)
application.show()

sys.exit(app.exec())
