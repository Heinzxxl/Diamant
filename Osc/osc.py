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

        self.cl1 = False
        self.cl2 = False
        self.cl3 = False
        self.cl4 = False
        self.cl5 = False
        self.cl6 = False
        self.cl7 = False
        self.cl8 = False
        self.cl9 = False
        self.cl10 = False

        self._Run = True
        self._tgType = "Edge"
        self._tgMode = "Auto"
        self._tgRLength = "2K (20 us)"
        self._tgSource = "CH1"
        self._tgSlope = "Rising"
        self._tgVideo = "Scan Line"
        self._tgDelay = "Off"

        self.RSButton.clicked.connect(self.rschange)
        self.TGButton.clicked.connect(self.tgchange)
        self.DPButton.clicked.connect(self.dpchange)
        self.CRButton.clicked.connect(self.crchange)
        self.MRButton.clicked.connect(self.mrchange)
        self.UTButton.clicked.connect(self.utchange)
        self.SRButton.clicked.connect(self.srchange)
        self.AQButton.clicked.connect(self.aqchange)

        self.tgchange()

    # adding figure to mplwidget
    def addfig(self, fig):
        self.canvas = FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()
        self.toolbar = NavigationToolbar(self.canvas,
                                         self.mplwidget, coordinates=True)
        self.mplvl.addWidget(self.toolbar)

    # box disconnection
    def cldisconnect1(self):
        if self.cl1:
            self.dynBox1.activated.disconnect()
            self.cl1 = False

    def cldisconnect2(self):
        if self.cl2:
            self.dynBox2.activated.disconnect()
            self.cl2 = False

    def cldisconnect3(self):
        if self.cl3:
            self.dynBox3.activated.disconnect()
            self.cl3 = False

    def cldisconnect4(self):
        if self.cl4:
            self.dynBox4.activated.disconnect()
            self.cl4 = False

    def cldisconnect5(self):
        if self.cl5:
            self.dynBox5.activated.disconnect()
            self.cl5 = False

    def cldisconnect6(self):
        if self.cl6:
            self.dynBox6.activated.disconnect()
            self.cl6 = False

    def cldisconnect7(self):
        if self.cl7:
            self.dynBox7.activated.disconnect()
            self.cl7 = False

    def cldisconnect8(self):
        if self.cl8:
            self.dynBox8.activated.disconnect()
            self.cl8 = False

    def cldisconnect9(self):
        if self.cl9:
            self.dynBox9.activated.disconnect()
            self.cl9 = False

    def cldisconnect10(self):
        if self.cl10:
            self.dynBox10.activated.disconnect()
            self.cl10 = False

    # dynamic buttons disconnection
    def alldyndisconnect(self):
        self.cldisconnect1()
        self.cldisconnect2()
        self.cldisconnect3()
        self.cldisconnect4()
        self.cldisconnect5()
        self.cldisconnect6()
        self.cldisconnect7()
        self.cldisconnect8()
        self.cldisconnect9()
        self.cldisconnect10()

    # clear names of dynamic boxes
    def alldynclear(self):
        self.dynBox1.clear()
        self.dynBox2.clear()
        self.dynBox3.clear()
        self.dynBox4.clear()
        self.dynBox5.clear()
        self.dynBox6.clear()
        self.dynBox7.clear()
        self.dynBox8.clear()
        self.dynBox9.clear()
        self.dynBox10.clear()
        self.dynLabel1.clear()
        self.dynLabel2.clear()
        self.dynLabel3.clear()
        self.dynLabel4.clear()
        self.dynLabel5.clear()
        self.dynLabel6.clear()
        self.dynLabel7.clear()
        self.dynLabel8.clear()
        self.dynLabel9.clear()
        self.dynLabel10.clear()

    # function for Run/Stop
    def rschange(self):
        if self._Run:
            self.rsLabel.setText('Stop')
            self._Run = False
        else:
            self.rsLabel.setText('Run')
            self._Run = True

    # function for Trigger
    def tgchange(self):
        self.alldyndisconnect()
        self.alldynclear()
        self.dynBox1.activated.connect(self.tgslot1)
        self.cl1 = True
        self.dynBox2.activated.connect(self.tgslot2)
        self.cl2 = True
        self.dynBox3.activated.connect(self.tgslot3)
        self.cl3 = True
        self.dynBox4.activated.connect(self.tgslot4)
        self.cl4 = True
        self.dynBox8.activated.connect(self.tgslot8)
        self.cl8 = True
        self.dynLabel1.setText("Type")
        self.dynBox1.addItems(["Edge", "Video"])
        self.dynBox1.setCurrentText(self._tgType)
        self.dynLabel2.setText("Mode")
        self.dynBox2.addItems(["Auto", "Normal", "Single"])
        self.dynBox2.setCurrentText(self._tgMode)
        self.dynLabel3.setText("Record Length")
        self.dynBox3.addItems(["500 (20 us)", "1K (20 us)", "2K (20 us)",
                               "4K (40 us)", "8K (80 us)", "16K (160 us)",
                               "32K (320 us)", "64K (640 us)"])
        self.dynBox3.setCurrentText(self._tgRLength)
        self.dynLabel4.setText("Source")
        self.dynBox4.addItems(["CH1", "CH2", "CH3", "CH4", "CH5",
                               "CH6", "CH7", "CH8", "CH9", "CH10", "Ext"])
        self.dynBox4.setCurrentText(self._tgSource)
        self.tgchange6()
        self.dynLabel8.setText("Delay Trigger")
        self.dynBox8.addItems(["On", "Off", "Setting..."])
        self.dynBox8.setCurrentText(self._tgDelay)

    # changing box6
    def tgchange6(self):
        if str(self.dynBox1.currentText()) == "Edge":
            self.dynLabel6.setText("Slope")
            self.dynBox6.addItems(["Rising", "Falling"])
            self.dynBox6.setCurrentText(self._tgSlope)
            self.dynBox6.activated.connect(self.tgslot6a)
            self.cl6 = True
        if str(self.dynBox1.currentText()) == "Video":
            self.dynLabel6.setText("Video Trig On")
            self.dynBox6.addItems(["Scan Line", "Field",
                                   "Odd Field", "Even Field"])
            self.dynBox6.setCurrentText(self._tgVideo)
            self.dynBox6.activated.connect(self.tgslot6b)
            self.cl6 = True

    # slots for Trigger
    def tgslot1(self):
        self._tgType = self.dynBox1.currentText()
        self.cldisconnect6()
        self.hldisconnect6()
        self.dynBox6.clear()
        self.dynLabel6.clear()
        self.tgchange6()

    def tgslot2(self):
        self._tgMode = self.dynBox2.currentText()

    def tgslot3(self):
        self._tgRLength = self.dynBox3.currentText()

    def tgslot4(self):
        self._tgSource = self.dynBox4.currentText()

    def tgslot6a(self):
        self._tgSlope = self.dynBox6.currentText()

    def tgslot6b(self):
        self._tgVideo = self.dynBox6.currentText()

    def tgslot8(self):
        self._tgDelay = self.dynBox8.currentText()

    # function for Display
    def dpchange(self):
        self.alldyndisconnect()
        self.alldynclear()

    # function for Cursor
    def crchange(self):
        self.alldyndisconnect()
        self.alldynclear()

    # function for Measure
    def mrchange(self):
        self.alldyndisconnect()
        self.alldynclear()

    # function for Utility
    def utchange(self):
        self.alldyndisconnect()
        self.alldynclear()
        self.dynBox1.activated.connect(self.utslot1)
        self.cl1 = True
        self.dynLabel1.setText("Languages")
        self.dynBox1.addItems([""])
        self.dynLabel2.setText("Languages")
        self.dynBox2.addItems(["English", ])

    # slots for Utility
    def utslot1(self):
        pass

    # function for Save/Recall
    def srchange(self):
        self.alldyndisconnect()
        self.alldynclear()

    # function for Acquire
    def aqchange(self):
        self.alldyndisconnect()
        self.alldynclear()


fig1 = Figure()
ax1f1 = fig1.add_subplot(111)
ax1f1.plot(np.random.rand(5))
fig1.set_tight_layout(True)

app = QtWidgets.QApplication([])
application = MyWindow()
application.addfig(fig1)
application.show()

sys.exit(app.exec())
