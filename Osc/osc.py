from PyQt5 import QtWidgets, QtCore, uic
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

        self.settings = QtCore.QSettings("MySoft", "Osc")
        self.load_settings()
        self.initconnect()

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

        self.bcl1 = False
        self.bcl2 = False
        self.bcl3 = False
        self.bcl4 = False
        self.bcl5 = False
        self.bcl6 = False
        self.bcl7 = False
        self.bcl8 = False
        self.bcl9 = False
        self.bcl10 = False

        self.lcl1 = False
        self.lcl2 = False
        self.lcl3 = False
        self.lcl4 = False
        self.lcl5 = False
        self.lcl6 = False
        self.lcl7 = False
        self.lcl8 = False
        self.lcl9 = False
        self.lcl10 = False

        if self._GlMode == "Trigger":
            self.tgchange()
        if self._GlMode == "Display":
            self.dpchange()
        if self._GlMode == "Cursor":
            self.crchange()
        if self._GlMode == "Measure":
            self.mrchange()
        if self._GlMode == "Utility":
            self.utchange()
        if self._GlMode == "SR":
            self.srchange()
        if self._GlMode == "Acquire":
            self.aqchange()

    # saving settings
    def save_settings(self):
        self.settings.setValue("CurrentMode", self._GlMode)

        self.settings.beginGroup("Trigger")
        self.settings.setValue("Type", self._tgType)
        self.settings.setValue("Mode", self._tgMode)
        self.settings.setValue("RLength", self._tgRLength)
        self.settings.setValue("Source", self._tgSource)
        self.settings.setValue("Slope", self._tgSlope)
        self.settings.setValue("Video", self._tgVideo)
        self.settings.endGroup()

        self.settings.beginGroup("Utility")
        self.settings.setValue("Language", self._utLang)
        self.settings.setValue("Page", self._utPage)
        self.settings.endGroup()

    # loading settings
    def load_settings(self):
        # Run/Stop condition
        self._Run = True
        # Trigger conditions
        self.settings.beginGroup("Trigger")
        self._tgType = self.settings.value("Type", "Edge")
        self._tgMode = self.settings.value("Mode", "Auto")
        self._tgRLength = self.settings.value("RLength", "2K (20 us)")
        self._tgSource = self.settings.value("Source", "CH1")
        self._tgSlope = self.settings.value("Slope", "Rising")
        self._tgVideo = self.settings.value("Video", "Scan Line")
        self._tgDelay = "Off"
        self.settings.endGroup()
        # Utility conditions
        self.settings.beginGroup("Utility")
        self._utLang = self.settings.value("Language", "English")
        self._utCalib = "Off"
        self._utLog = "Off"
        self._utTCP = "Off"
        self._utPsFl = "Off"
        self._utVMon = "Off"
        self._utPage = self.settings.value("Page", "Next Page")
        self.settings.endGroup()

        self._GlMode = self.settings.value("CurrentMode", "Trigger")

    # closing'n'saving
    def closeEvent(self, event):
        self.save_settings()
        sys.exit()

    # initial connections
    def initconnect(self):
        self.RSButton.clicked.connect(self.rschange)
        self.TGButton.clicked.connect(self.tgchange)
        self.DPButton.clicked.connect(self.dpchange)
        self.CRButton.clicked.connect(self.crchange)
        self.MRButton.clicked.connect(self.mrchange)
        self.UTButton.clicked.connect(self.utchange)
        self.SRButton.clicked.connect(self.srchange)
        self.AQButton.clicked.connect(self.aqchange)

    # adding figure to mplwidget
    def addfig(self, fig):
        self.canvas = FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()
        self.toolbar = NavigationToolbar(self.canvas,
                                         self.mplwidget, coordinates=True)
        self.mplvl.addWidget(self.toolbar)

    # box disconnection ("clicked disonnect")
    def cldisconnect1(self):
        if self.cl1:
            self.dynBox1.activated.disconnect()
            self.dynBox1.setStyleSheet(
                    "QComboBox::drop-down {border-width: 0px}" +
                    "QComboBox::down-arrow {image: none; border-width: 0px}" +
                    "QComboBox{ border-top: 0px solid rgb(85, 0, 255);" +
                    "background:rgb(225, 225, 225)}")
            self.cl1 = False
        if self.bcl1:
            self.dynBox1.clicked.disconnect()
            self.bcl1 = False

    def cldisconnect2(self):
        if self.cl2:
            self.dynBox2.activated.disconnect()
            self.dynBox2.setStyleSheet(
                    "QComboBox::drop-down {border-width: 0px}" +
                    "QComboBox::down-arrow {image: none; border-width: 0px}" +
                    "QComboBox{ border-top: 0px solid rgb(85, 0, 255);" +
                    "background:rgb(225, 225, 225)}")
            self.cl2 = False
        if self.bcl2:
            self.dynBox2.clicked.disconnect()
            self.bcl2 = False

    def cldisconnect3(self):
        if self.cl3:
            self.dynBox3.activated.disconnect()
            self.dynBox3.setStyleSheet(
                    "QComboBox::drop-down {border-width: 0px}" +
                    "QComboBox::down-arrow {image: none; border-width: 0px}" +
                    "QComboBox{ border-top: 0px solid rgb(85, 0, 255);" +
                    "background:rgb(225, 225, 225)}")
            self.cl3 = False
        if self.bcl3:
            self.dynBox3.clicked.disconnect()
            self.bcl3 = False

    def cldisconnect4(self):
        if self.cl4:
            self.dynBox4.activated.disconnect()
            self.dynBox4.setStyleSheet(
                    "QComboBox::drop-down {border-width: 0px}" +
                    "QComboBox::down-arrow {image: none; border-width: 0px}" +
                    "QComboBox{ border-top: 0px solid rgb(85, 0, 255);" +
                    "background:rgb(225, 225, 225)}")
            self.cl4 = False
        if self.bcl4:
            self.dynBox4.clicked.disconnect()
            self.bcl4 = False

    def cldisconnect5(self):
        if self.cl5:
            self.dynBox5.activated.disconnect()
            self.dynBox5.setStyleSheet(
                    "QComboBox::drop-down {border-width: 0px}" +
                    "QComboBox::down-arrow {image: none; border-width: 0px}" +
                    "QComboBox{ border-top: 0px solid rgb(85, 0, 255);" +
                    "background:rgb(225, 225, 225)}")
            self.cl5 = False
        if self.bcl5:
            self.dynBox5.clicked.disconnect()
            self.bcl5 = False

    def cldisconnect6(self):
        if self.cl6:
            self.dynBox6.activated.disconnect()
            self.dynBox6.setStyleSheet(
                    "QComboBox::drop-down {border-width: 0px}" +
                    "QComboBox::down-arrow {image: none; border-width: 0px}" +
                    "QComboBox{ border-top: 0px solid rgb(85, 0, 255);" +
                    "background:rgb(225, 225, 225)}")
            self.cl6 = False
        if self.bcl6:
            self.dynBox6.clicked.disconnect()
            self.bcl6 = False

    def cldisconnect7(self):
        if self.cl7:
            self.dynBox7.activated.disconnect()
            self.dynBox7.setStyleSheet(
                    "QComboBox::drop-down {border-width: 0px}" +
                    "QComboBox::down-arrow {image: none; border-width: 0px}" +
                    "QComboBox{ border-top: 0px solid rgb(85, 0, 255);" +
                    "background:rgb(225, 225, 225)}")
            self.cl7 = False
        if self.bcl7:
            self.dynBox7.clicked.disconnect()
            self.bcl7 = False

    def cldisconnect8(self):
        if self.cl8:
            self.dynBox8.activated.disconnect()
            self.dynBox8.setStyleSheet(
                    "QComboBox::drop-down {border-width: 0px}" +
                    "QComboBox::down-arrow {image: none; border-width: 0px}" +
                    "QComboBox{ border-top: 0px solid rgb(85, 0, 255);" +
                    "background:rgb(225, 225, 225)}")
            self.cl8 = False
        if self.bcl8:
            self.dynBox8.clicked.disconnect()
            self.bcl8 = False

    def cldisconnect9(self):
        if self.cl9:
            self.dynBox9.activated.disconnect()
            self.dynBox9.setStyleSheet(
                    "QComboBox::drop-down {border-width: 0px}" +
                    "QComboBox::down-arrow {image: none; border-width: 0px}" +
                    "QComboBox{ border-top: 0px solid rgb(85, 0, 255);" +
                    "background:rgb(225, 225, 225)}")
            self.cl9 = False
        if self.bcl9:
            self.dynBox9.clicked.disconnect()
            self.bcl9 = False

    def cldisconnect10(self):
        if self.cl10:
            self.dynBox10.activated.disconnect()
            self.dynBox10.setStyleSheet(
                    "QComboBox::drop-down {border-width: 0px}" +
                    "QComboBox::down-arrow {image: none; border-width: 0px}" +
                    "QComboBox{ border-top: 0px solid rgb(85, 0, 255);" +
                    "background:rgb(225, 225, 225)}")
            self.cl10 = False
        if self.bcl10:
            self.dynBox10.clicked.disconnect()
            self.bcl10 = False

    # pushlabel disconnection ("label clicked disconnect")
    def lcldisconnect1(self):
        if self.lcl1:
            self.dynLabel1.clicked.disconnect()
            self.lcl1 = False

    def lcldisconnect2(self):
        if self.lcl2:
            self.dynLabel2.clicked.disconnect()
            self.lcl2 = False

    def lcldisconnect3(self):
        if self.lcl3:
            self.dynLabel3.clicked.disconnect()
            self.lcl3 = False

    def lcldisconnect4(self):
        if self.lcl4:
            self.dynLabel4.clicked.disconnect()
            self.lcl4 = False

    def lcldisconnect5(self):
        if self.lcl5:
            self.dynLabel5.clicked.disconnect()
            self.lcl5 = False

    def lcldisconnect6(self):
        if self.lcl6:
            self.dynLabel6.clicked.disconnect()
            self.lcl6 = False

    def lcldisconnect7(self):
        if self.lcl7:
            self.dynLabel7.clicked.disconnect()
            self.lcl7 = False

    def lcldisconnect8(self):
        if self.lcl8:
            self.dynLabel8.clicked.disconnect()
            self.lcl8 = False

    def lcldisconnect9(self):
        if self.lcl9:
            self.dynLabel9.clicked.disconnect()
            self.lcl9 = False

    def lcldisconnect10(self):
        if self.lcl10:
            self.dynLabel10.clicked.disconnect()
            self.lcl10 = False

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
        self.lcldisconnect1()
        self.lcldisconnect2()
        self.lcldisconnect3()
        self.lcldisconnect4()
        self.lcldisconnect5()
        self.lcldisconnect6()
        self.lcldisconnect7()
        self.lcldisconnect8()
        self.lcldisconnect9()
        self.lcldisconnect10()

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

    # dynBox proper connection (signal "activated")
    def abconnect(self, box, slot):
        box.activated.connect(slot)
        box.setStyleSheet(
                "QComboBox{ border-top: 0px solid rgb(85, 0, 255);" +
                "background:rgb(225, 225, 225);}")

    # dynBox proper connection (signal "clicked")
    def cbconnect(self, box, slot):
        box.clicked.connect(slot)

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
        self._GlMode = "Trigger"
        self.alldyndisconnect()
        self.alldynclear()
        self.abconnect(self.dynBox1, self.tgslot1)
        self.cl1 = True
        self.abconnect(self.dynBox2, self.tgslot2)
        self.cl2 = True
        self.abconnect(self.dynBox3, self.tgslot3)
        self.cl3 = True
        self.abconnect(self.dynBox4, self.tgslot4)
        self.cl4 = True
        self.abconnect(self.dynBox8, self.tgslot8)
        self.cl8 = True
        self.dynLabel1.setText("Type")
        self.dynBox1.addItems(["Edge", "Video"])
        self.dynBox1.setCurrentIndex(self.dynBox1.findText(self._tgType))
        self.dynLabel2.setText("Mode")
        self.dynBox2.addItems(["Auto", "Normal", "Single"])
        self.dynBox2.setCurrentIndex(self.dynBox2.findText(self._tgMode))
        self.dynLabel3.setText("Record Length")
        self.dynBox3.addItems(["500 (20 us)", "1K (20 us)", "2K (20 us)",
                               "4K (40 us)", "8K (80 us)", "16K (160 us)",
                               "32K (320 us)", "64K (640 us)"])
        self.dynBox3.setCurrentIndex(self.dynBox3.findText(self._tgRLength))
        self.dynLabel4.setText("Source")
        self.dynBox4.addItems(["CH1", "CH2", "CH3", "CH4", "CH5",
                               "CH6", "CH7", "CH8", "CH9", "CH10", "Ext"])
        self.dynBox4.setCurrentIndex(self.dynBox4.findText(self._tgSource))
        self.tgchange6()
        self.dynLabel8.setText("Delay Trigger")
        self.dynBox8.addItems(["Off", "On", "Setting..."])
        self.dynBox8.setCurrentIndex(self.dynBox8.findText(self._tgDelay))

    # changing box6
    def tgchange6(self):
        if self._tgType == "Edge":
            self.dynLabel6.setText("Slope")
            self.dynBox6.addItems(["Rising", "Falling"])
            self.dynBox6.setCurrentIndex(self.dynBox6.findText(self._tgSlope))
            self.abconnect(self.dynBox6, self.tgslot6a)
            self.cl6 = True
        if self._tgType == "Video":
            self.dynLabel6.setText("Video Trig On")
            self.dynBox6.addItems(["Scan Line", "Field",
                                   "Odd Field", "Even Field"])
            self.dynBox6.setCurrentIndex(self.dynBox6.findText(self._tgVideo))
            self.abconnect(self.dynBox6, self.tgslot6b)
            self.cl6 = True

    # slots for Trigger
    def tgslot1(self):
        self._tgType = self.dynBox1.currentText()
        self.cldisconnect6()
        self.lcldisconnect6()
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
        self._GlMode = "Display"
        self.alldyndisconnect()
        self.alldynclear()

    # function for Cursor
    def crchange(self):
        self._GlMode = "Cursor"
        self.alldyndisconnect()
        self.alldynclear()

    # function for Measure
    def mrchange(self):
        self._GlMode = "Measure"
        self.alldyndisconnect()
        self.alldynclear()

    # function for Utility
    def utchange(self):
        self._GlMode = "Utility"
        self.alldyndisconnect()
        self.alldynclear()
        self.dynLabel10.clicked.connect(self.utslot10)
        self.lcl10 = True
        self.dynLabel10.setText(self._utPage)
        self.cbconnect(self.dynBox10, self.utslot10)
        self.bcl10 = True
        if self._utPage == "Next Page":
            self.abconnect(self.dynBox1, self.utslot1a)
            self.cl1 = True
            self.dynLabel1.setText("Languages")
            self.dynBox1.addItems(["English", "Russian"])
            self.dynBox1.setCurrentIndex(self.dynBox1.findText(self._utLang))
            self.dynLabel2.setText("Factory Reset")
            self.dynLabel2.clicked.connect(self.utslot2a)
            self.lcl2 = True
            self.cbconnect(self.dynBox2, self.utslot2a)
            self.bcl2 = True
            self.abconnect(self.dynBox3, self.utslot3a)
            self.cl3 = True
            self.dynLabel3.setText("Calibration")
            self.dynBox3.addItems(["Off", "On"])
            self.dynBox3.setCurrentIndex(self.dynBox3.findText(self._utCalib))
            self.abconnect(self.dynBox4, self.utslot4a)
            self.cl4 = True
            self.dynLabel4.setText("Logger")
            self.dynBox4.addItems(["Off", "On"])
            self.dynBox4.setCurrentIndex(self.dynBox4.findText(self._utLog))
            self.abconnect(self.dynBox5, self.utslot5a)
            self.cl5 = True
            self.dynLabel5.setText("Export Data")
            self.dynBox5.addItems(["", "Text", "HTML", "Current Setup",
                                   "All Setups", "DSO"])
            self.dynBox5.setCurrentIndex(0)
            self.abconnect(self.dynBox6, self.utslot6a)
            self.cl6 = True
            self.dynLabel6.setText("Import Data")
            self.dynBox6.addItems(["", "Logger", "Current Setup",
                                   "All Setups", "DSO"])
            self.dynBox6.setCurrentIndex(0)
            self.abconnect(self.dynBox7, self.utslot7a)
            self.cl7 = True
            self.dynLabel7.setText("TCP/IP")
            self.dynBox7.addItems(["Off", "On"])
            self.dynBox7.setCurrentIndex(self.dynBox7.findText(self._utTCP))
            self.dynLabel9.setText("Launch")
            self.dynLabel9.clicked.connect(self.utslot9a)
            self.lcl9 = True
            self.cbconnect(self.dynBox9, self.utslot9a)
            self.bcl9 = True
        if self._utPage == "Prior Page":
            self.dynLabel1.setText("Product Info")
            self.dynLabel1.clicked.connect(self.utslot1b)
            self.lcl1 = True
            self.cbconnect(self.dynBox1, self.utslot1b)
            self.bcl1 = True
            self.abconnect(self.dynBox2, self.utslot2b)
            self.cl2 = True
            self.dynLabel2.setText("Pass/Fail")
            self.dynBox2.addItems(["Off", "On"])
            self.dynBox2.setCurrentIndex(self.dynBox2.findText(self._utPsFl))
            self.dynLabel3.setText("Hot Keys")
            self.dynLabel3.clicked.connect(self.utslot3b)
            self.lcl3 = True
            self.cbconnect(self.dynBox3, self.utslot3b)
            self.bcl3 = True
            self.abconnect(self.dynBox7, self.utslot7b)
            self.cl7 = True
            self.dynLabel7.setText("VISA Monitor")
            self.dynBox7.addItems(["Off", "On"])
            self.dynBox7.setCurrentIndex(self.dynBox7.findText(self._utVMon))
            self.dynLabel8.setText("Online Update")
            self.dynLabel8.clicked.connect(self.utslot8b)
            self.lcl8 = True
            self.cbconnect(self.dynBox8, self.utslot8b)
            self.bcl8 = True
            self.dynLabel9.setText("Customize")
            self.dynLabel9.clicked.connect(self.utslot9b)
            self.lcl9 = True
            self.cbconnect(self.dynBox9, self.utslot9b)
            self.bcl9 = True

    # slots for Utility
    def utslot10(self):
        if self._utPage == "Next Page":
            self._utPage = "Prior Page"
        else:
            self._utPage = "Next Page"
        self.utchange()

    def utslot1a(self):
        self._utLang = self.dynBox1.currentText()

    def utslot2a(self):
        pass

    def utslot3a(self):
        self._utCalib = self.dynBox3.currentText()

    def utslot4a(self):
        self._utLog = self.dynBox4.currentText()

    def utslot5a(self):
        self.dynBox5.setCurrentIndex(0)

    def utslot6a(self):
        self.dynBox6.setCurrentIndex(0)

    def utslot7a(self):
        self._utTCP = self.dynBox7.currentText()

    def utslot9a(self):
        pass

    def utslot1b(self):
        pass

    def utslot2b(self):
        self._utPsFl = self.dynBox2.currentText()

    def utslot3b(self):
        pass

    def utslot7b(self):
        self._utVMon = self.dynBox7.currentText()

    def utslot8b(self):
        pass

    def utslot9b(self):
        pass

    # function for Save/Recall
    def srchange(self):
        self._GlMode = "SR"
        self.alldyndisconnect()
        self.alldynclear()

    # function for Acquire
    def aqchange(self):
        self._GlMode = "Acquire"
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
