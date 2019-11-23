from PyQt5 import QtWidgets, QtCore, uic
from matplotlib.backends.backend_qt5agg import (
        NavigationToolbar2QT as NavigationToolbar)
import sys
from animatedmplcanvas import AnimatedMplCanvas

Ui_MainWindow, QMainWindow = uic.loadUiType('osc.ui')


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # loading settings
        self.settings = QtCore.QSettings("MySoft", "Osc")
        self.load_settings()

        # current setup
        self.init_connection()
        self.set_GlMode()
        self.add_canvas()

    # saving settings
    def save_settings(self):
        # Global Mode condition
        self.settings.setValue("CurrentMode", self._GlMode)
        # Trigger conditions
        self.settings.beginGroup("Trigger")
        self.settings.setValue("Type", self._tgType)
        self.settings.setValue("Mode", self._tgMode)
        self.settings.setValue("RLength", self._tgRLength)
        self.settings.setValue("Source", self._tgSource)
        self.settings.setValue("Slope", self._tgSlope)
        self.settings.setValue("Video", self._tgVideo)
        self.settings.endGroup()
        # Utility conditions
        self.settings.beginGroup("Utility")
        self.settings.setValue("Language", self._utLang)
        self.settings.setValue("Page", self._utPage)
        self.settings.endGroup()

    # loading settings
    def load_settings(self):
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
        # Global Mode condition
        self._GlMode = self.settings.value("CurrentMode", "Trigger")

    # closing'n'saving
    def closeEvent(self, event):
        self.save_settings()
        sys.exit()

    # initial connections
    def init_connection(self):
        self.RSButton.clicked.connect(self.rschange)
        self.TGButton.clicked.connect(self.tgchange)
        self.DPButton.clicked.connect(self.dpchange)
        self.CRButton.clicked.connect(self.crchange)
        self.MRButton.clicked.connect(self.mrchange)
        self.UTButton.clicked.connect(self.utchange)
        self.SRButton.clicked.connect(self.srchange)
        self.AQButton.clicked.connect(self.aqchange)

    # initial global mode setting
    def set_GlMode(self):
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

    # adding canvas to mplwidget
    def add_canvas(self):
        self.canvas = AnimatedMplCanvas()
        self.mplvl.addWidget(self.canvas)
        self.toolbar = NavigationToolbar(self.canvas,
                                         self.mplwidget, coordinates=True)
        self.mplvl.addWidget(self.toolbar)

    # box disconnection
    def disconnect_box(self, box):
        if box.signalActivatedIsConnected:
            box.activated.disconnect()
            box.setStyleSheet(
                    "QComboBox::drop-down {border-width: 0px}" +
                    "QComboBox::down-arrow {image: none; border-width: 0px}" +
                    "QComboBox{ border-top: 0px solid rgb(85, 0, 255);" +
                    "background:rgb(225, 225, 225)}")
            box.signalActivatedIsConnected = False
        if box.signalClickedIsConnected:
            box.clicked.disconnect()
            box.signalClickedIsConnected = False

    # pushlabel disconnection
    def disconnect_label(self, label):
        if label.signalClickedIsConnected:
            label.clicked.disconnect()
            label.signalClickedIsConnected = False

    # dynamic buttons disconnection
    def alldyndisconnect(self):
        self.disconnect_box(self.dynBox1)
        self.disconnect_box(self.dynBox2)
        self.disconnect_box(self.dynBox3)
        self.disconnect_box(self.dynBox4)
        self.disconnect_box(self.dynBox5)
        self.disconnect_box(self.dynBox6)
        self.disconnect_box(self.dynBox7)
        self.disconnect_box(self.dynBox8)
        self.disconnect_box(self.dynBox9)
        self.disconnect_box(self.dynBox10)
        self.disconnect_label(self.dynLabel1)
        self.disconnect_label(self.dynLabel2)
        self.disconnect_label(self.dynLabel3)
        self.disconnect_label(self.dynLabel4)
        self.disconnect_label(self.dynLabel5)
        self.disconnect_label(self.dynLabel6)
        self.disconnect_label(self.dynLabel7)
        self.disconnect_label(self.dynLabel8)
        self.disconnect_label(self.dynLabel9)
        self.disconnect_label(self.dynLabel10)

    # clear names of dynamic boxes
    def clear_all_fields(self):
        widgets = (self.dynvl.itemAt(i).widget()
                   for i in range(self.dynvl.count()))
        for widget in widgets:
            widget.clear()

    # dynBox proper connection (signal "activated")
    def abconnect(self, box, slot):
        box.activated.connect(slot)
        box.signalActivatedIsConnected = True
        box.setStyleSheet(
                "QComboBox{ border-top: 0px solid rgb(85, 0, 255);" +
                "background:rgb(225, 225, 225);}")

    # dynBox proper connection (signal "clicked")
    def cbconnect(self, box, slot):
        box.clicked.connect(slot)
        box.signalClickedIsConnected = True

    # dynLabel proper connection (signal "clicked")
    def lclconnect(self, label, slot):
        label.clicked.connect(slot)
        label.signalClickedIsConnected = True

    # function for Run/Stop
    def rschange(self):
        if self.canvas.animation_is_running:
            self.rsLabel.setText('Stop')
            self.canvas.anim.event_source.stop()
            self.canvas.animation_is_running = False
        else:
            self.rsLabel.setText('Run')
            self.canvas.anim.event_source.start()
            self.canvas.animation_is_running = True

    # function for Trigger
    def tgchange(self):
        self._GlMode = "Trigger"
        self.alldyndisconnect()
        self.clear_all_fields()

        self.abconnect(self.dynBox1, self.tgslot1)
        self.abconnect(self.dynBox2, self.tgslot2)
        self.abconnect(self.dynBox3, self.tgslot3)
        self.abconnect(self.dynBox4, self.tgslot4)
        self.abconnect(self.dynBox8, self.tgslot8)

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
        if self._tgType == "Video":
            self.dynLabel6.setText("Video Trig On")
            self.dynBox6.addItems(["Scan Line", "Field",
                                   "Odd Field", "Even Field"])
            self.dynBox6.setCurrentIndex(self.dynBox6.findText(self._tgVideo))
            self.abconnect(self.dynBox6, self.tgslot6b)

    # slots for Trigger
    def tgslot1(self):
        self._tgType = self.dynBox1.currentText()
        self.disconnect_box(self.dynBox6)
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
        self.clear_all_fields()

    # function for Cursor
    def crchange(self):
        self._GlMode = "Cursor"
        self.alldyndisconnect()
        self.clear_all_fields()

    # function for Measure
    def mrchange(self):
        self._GlMode = "Measure"
        self.alldyndisconnect()
        self.clear_all_fields()

    # function for Utility
    def utchange(self):
        self._GlMode = "Utility"
        self.alldyndisconnect()
        self.clear_all_fields()

        self.lclconnect(self.dynLabel10, self.utslot10)
        self.dynLabel10.setText(self._utPage)
        self.cbconnect(self.dynBox10, self.utslot10)

        if self._utPage == "Next Page":
            self.abconnect(self.dynBox1, self.utslot1a)
            self.dynLabel1.setText("Languages")
            self.dynBox1.addItems(["English", "Russian"])
            self.dynBox1.setCurrentIndex(self.dynBox1.findText(self._utLang))

            self.dynLabel2.setText("Factory Reset")
            self.lclconnect(self.dynLabel2, self.utslot2a)
            self.cbconnect(self.dynBox2, self.utslot2a)

            self.abconnect(self.dynBox3, self.utslot3a)
            self.dynLabel3.setText("Calibration")
            self.dynBox3.addItems(["Off", "On"])
            self.dynBox3.setCurrentIndex(self.dynBox3.findText(self._utCalib))

            self.abconnect(self.dynBox4, self.utslot4a)
            self.dynLabel4.setText("Logger")
            self.dynBox4.addItems(["Off", "On"])
            self.dynBox4.setCurrentIndex(self.dynBox4.findText(self._utLog))

            self.abconnect(self.dynBox5, self.utslot5a)
            self.dynLabel5.setText("Export Data")
            self.dynBox5.addItems(["", "Text", "HTML", "Current Setup",
                                   "All Setups", "DSO"])
            self.dynBox5.setCurrentIndex(0)

            self.abconnect(self.dynBox6, self.utslot6a)
            self.dynLabel6.setText("Import Data")
            self.dynBox6.addItems(["", "Logger", "Current Setup",
                                   "All Setups", "DSO"])
            self.dynBox6.setCurrentIndex(0)

            self.abconnect(self.dynBox7, self.utslot7a)
            self.dynLabel7.setText("TCP/IP")
            self.dynBox7.addItems(["Off", "On"])
            self.dynBox7.setCurrentIndex(self.dynBox7.findText(self._utTCP))

            self.dynLabel9.setText("Launch")
            self.lclconnect(self.dynLabel9, self.utslot9a)
            self.cbconnect(self.dynBox9, self.utslot9a)

        if self._utPage == "Prior Page":
            self.dynLabel1.setText("Product Info")
            self.lclconnect(self.dynLabel1, self.utslot1b)
            self.cbconnect(self.dynBox1, self.utslot1b)

            self.abconnect(self.dynBox2, self.utslot2b)
            self.dynLabel2.setText("Pass/Fail")
            self.dynBox2.addItems(["Off", "On"])
            self.dynBox2.setCurrentIndex(self.dynBox2.findText(self._utPsFl))

            self.dynLabel3.setText("Hot Keys")
            self.lclconnect(self.dynLabel3, self.utslot3b)
            self.cbconnect(self.dynBox3, self.utslot3b)

            self.abconnect(self.dynBox7, self.utslot7b)
            self.dynLabel7.setText("VISA Monitor")
            self.dynBox7.addItems(["Off", "On"])
            self.dynBox7.setCurrentIndex(self.dynBox7.findText(self._utVMon))

            self.dynLabel8.setText("Online Update")
            self.lclconnect(self.dynLabel8, self.utslot8b)
            self.cbconnect(self.dynBox8, self.utslot8b)

            self.dynLabel9.setText("Customize")
            self.lclconnect(self.dynLabel9, self.utslot9b)
            self.cbconnect(self.dynBox9, self.utslot9b)

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
        self.clear_all_fields()

    # function for Acquire
    def aqchange(self):
        self._GlMode = "Acquire"
        self.alldyndisconnect()
        self.clear_all_fields()


app = QtWidgets.QApplication([])
application = MyWindow()
application.show()

sys.exit(app.exec())
