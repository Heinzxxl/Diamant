from PyQt5 import QtWidgets, QtCore, uic
import sys
import ctypes
import numpy as np

from datetime import datetime
from animatedmplcanvas import AnimatedMplCanvas
from udso import uDso
from capt import Capt

Ui_MainWindow, QMainWindow = uic.loadUiType('osc.ui')


class MyWindow(QMainWindow, Ui_MainWindow):

    ceaseCapturing = QtCore.pyqtSignal()
    restartCapturing = QtCore.pyqtSignal()
    startDrawing = QtCore.pyqtSignal()
    ceaseFurtherCapture = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # loading settings
        self.settings = QtCore.QSettings("MySoft", "Osc")
        self.load_settings()

        # uDso
        self.osc = uDso()

        # current setup
        self.init_button_connection()
        self.set_GlMode()
        self.add_canvas()
        self.ch_connection()
        self.rsLabel.setText('Stop')
        self.startDrawing.connect(self.canvas.enable_drawing)
        self.ceaseFurtherCapture.connect(self.canvas.stopFurtherCapture)
        self.canvas.runAgain.connect(self.new_capture)
        if self.osc.isDemo is False:
            self.setupDso()

        # mutex
        self.mutex = QtCore.QMutex()

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
        # Measure conditions
        self.settings.beginGroup("Measure")
        self.settings.setValue("SelectedChannel", self._mrCH)
        self.settings.endGroup()
        # Display conditions
        self.settings.beginGroup("Display")
        self.settings.setValue("CH1Probe", self._ch1Probe[0])
        self.settings.setValue("CH2Probe", self._ch2Probe[0])
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
        # Measure conditions
        self.settings.beginGroup("Measure")
        self._mrCH = self.settings.value("SelectedChannel", "CH1")
        self.settings.endGroup()
        # Display conditions
        self.settings.beginGroup("Display")
        self._ch1Probe = [self.settings.value("CH1Probe", "10x")]
        self._ch2Probe = [self.settings.value("CH2Probe", "10x")]
        self.settings.endGroup()
        # Global Mode condition
        self._GlMode = self.settings.value("CurrentMode", "Trigger")
        # Necessary data
        self.ch_number = {"CH1": 0, "CH2": 1}
        self.slope_number = {"Rising": 0, "Falling": 1}
        self.probe_mult = {"1x": 1, "10x": 10}
        self.probe_num = {"CH1": self._ch1Probe, "CH2": self._ch2Probe}
        self.ch_boxes = {"CH1": self.CH1Box, "CH2": self.CH2Box}
        self.first_run = True

    # closing'n'saving
    def closeEvent(self, event):
        self.save_settings()
        self.osc.uDsoSDKShutdown()
        if self.osc.isDemo is False:
            self.logFile.close()
        sys.exit()

    # setting up Dso
    def setupDso(self):
        self.change_threshold()
        self.change_volt_div()
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
        self.logFile = open('Log/' + dt_string + ".txt",'ab')

    def process_data(self):
        if self.cptr.isInterrupted is True:
            print(self.cptr.isInterrupted)
            self.canvas.animation_is_running = False
            self.rsLabel.setText('Stop')
            self.mutex.unlock()
            return
       # print(self.cptr.isInterrupted)
        length = self.cptr.dbWaveData_Length
        temp1 = np.arange(-length/4, length/4)
        temp2 = self.cptr.data_
        temp2_spl = np.split(temp2, 2)
        tempCH1 = temp2_spl[0]
        tempCH2 = temp2_spl[1]
        self.i64SampleRate = ctypes.c_int()
        self.osc.uDsoSDKGetSampleRate(ctypes.pointer(self.i64SampleRate))
        self.timeFactor = 1./self.i64SampleRate.value
        self.canvas.drawDataX = [i*self.timeFactor for i in temp1]
        self.canvas.drawDataY_1 = [i*1e-6 for i in tempCH1]
        self.canvas.drawDataY_2 = [i*1e-6 for i in tempCH2]
        self.startDrawing.emit()
        wr_data = np.c_[self.canvas.drawDataY_1, self.canvas.drawDataY_2]
        np.savetxt(self.logFile, wr_data)
        self.mutex.unlock()

    def re_capture(self):
        self.startDrawing.emit()
        self.mutex.unlock()


    # initial connections
    def init_button_connection(self):
        self.RSButton.clicked.connect(self.rschange)
        self.TGButton.clicked.connect(self.tgchange)
        self.DPButton.clicked.connect(self.dpchange)
        self.CRButton.clicked.connect(self.crchange)
        self.MRButton.clicked.connect(self.mrchange)
        self.UTButton.clicked.connect(self.utchange)
        self.SRButton.clicked.connect(self.srchange)
        self.AQButton.clicked.connect(self.aqchange)

        self.plusVButton.clicked.connect(self.zoom_in_volts)
        self.minusVButton.clicked.connect(self.zoom_out_volts)
        self.plusSecButton.clicked.connect(self.zoom_in_seconds)
        self.minusSecButton.clicked.connect(self.zoom_out_seconds)
        
        self.trigEdit.returnPressed.connect(self.change_threshold)

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
        if self.osc.isDemo is True:
            self.canvas = AnimatedMplCanvas(demoFlag=True)
        else:
            self.canvas = AnimatedMplCanvas(demoFlag=False)
        self.mplvl.addWidget(self.canvas)
        tscaleNumber = self.canvas.currentSecondsScaleNumber
        self.timeLabel.setText("M " + self.canvas.sPDiv[tscaleNumber])
   #     self.toolbar = NavigationToolbar(self.canvas,
    #                                     self.mplwidget, coordinates=True)
    #    self.mplvl.addWidget(self.toolbar)

    # checkboxes connection and binding channel labels with channel numbers
    def ch_connection(self):
        self.CH1Box.stateChanged.connect(self.CH1_ctrl)
        self.CH2Box.stateChanged.connect(self.CH2_ctrl)
        self.CHLabels = {"CH1": self.CH1Label, "CH2": self.CH2Label}

    def CH1_ctrl(self):
        if self.CH1Box.isChecked():
            self.canvas.enable_channel("CH1")
            self.CH1Box.setStyleSheet("QCheckBox{border: 2px solid " +
                                      self.canvas.colors["CH1"] + ";}")
            scaleNumber = self.canvas.currentVoltsScaleNumber["CH1"]
            textmult = self.probe_num["CH1"][0]
            print("textmult: ", textmult)
            if textmult == "10x":
                vPD = self.canvas.vPDiv[scaleNumber]
                print("10x worked")
            if textmult == "1x":
                vPD = self.canvas.altvPDiv[scaleNumber]
                print("1x worked")
            self.CH1Label.setText("CH1 " + vPD)
        else:
            self.canvas.disable_channel("CH1")
            self.CH1Box.setStyleSheet("")
            self.CH1Label.clear()

    def CH2_ctrl(self):
        if self.CH2Box.isChecked():
            self.canvas.enable_channel("CH2")
            self.CH2Box.setStyleSheet("QCheckBox{border: 2px solid " +
                                      self.canvas.colors["CH2"] + ";}")
            scaleNumber = self.canvas.currentVoltsScaleNumber["CH2"]
            textmult = self.probe_num["CH2"][0]
            print("textmult: ", textmult)
            if textmult == "10x":
                vPD = self.canvas.vPDiv[scaleNumber]
                print("10x worked")
            if textmult == "1x":
                vPD = self.canvas.altvPDiv[scaleNumber]
                print("1x worked")
            self.CH2Label.setText("CH2 " + vPD)
        else:
            self.canvas.disable_channel("CH2")
            self.CH2Box.setStyleSheet("")
            self.CH2Label.clear()
            
    def change_threshold(self):
        if self.osc.isDemo is False:
            if self.first_run is False:
                print("Stop to change")
                self.restartCapturing.emit()
            num = int(self.trigEdit.text())
            sourceCh = self.ch_number[self._tgSource]
            trigSlope = self.slope_number[self._tgSlope]
            mult = self.probe_mult[self.probe_num[self._tgSource][0]]
            level = int(num*1000/mult)
            self.osc._uDsoSDKSetEdgeTrig_(sourceCh, trigSlope, level)
            print("New Threshold level: ", int(num/mult))

    def change_volt_div(self):
        scaleNumber = self.canvas.currentVoltsScaleNumber[self._mrCH]
        textmult = self.probe_num[self._mrCH][0]
        print("textmult: ", textmult)
        if textmult == "10x":
            vPD = self.canvas.vPDiv[scaleNumber]
            print("10x worked")
        if textmult == "1x":
            vPD = self.canvas.altvPDiv[scaleNumber]
            print("1x worked")
        vPD_num = self.canvas.vPDiv_num[scaleNumber]
        ch_num = self.canvas.channelNum[self._mrCH]
        if self.osc.isDemo is False:
            if self.first_run is False:
                print("Stop to change")
                self.restartCapturing.emit()
            self.osc._uDsoSDKSetVoltDiv_(ch_num, int(vPD_num/10))
            self.osc._uDsoSDKGetVoltDiv_(ch_num)
        if self.ch_boxes[self._mrCH].isChecked():
            self.CHLabels[self._mrCH].setText(self._mrCH + " " + vPD)

    # zooming in/out
    def zoom_in_volts(self):
        if self.canvas.channel_is_enabled[self._mrCH]:
            if self.canvas.currentVoltsScaleNumber[self._mrCH] > 0:
                self.canvas.currentVoltsScaleNumber[self._mrCH] -= 1
                self.change_volt_div()
                self.canvas.rescale_axes()

    def zoom_out_volts(self):
        if self.canvas.channel_is_enabled[self._mrCH]:
            if self.canvas.currentVoltsScaleNumber[self._mrCH] < 11:
                self.canvas.currentVoltsScaleNumber[self._mrCH] += 1
                self.change_volt_div()
                self.canvas.rescale_axes()

    def zoom_in_seconds(self):
        if self.canvas.currentSecondsScaleNumber > 0:
            self.canvas.currentSecondsScaleNumber -= 1
            tscaleNumber = self.canvas.currentSecondsScaleNumber
            sampleRate = self.canvas.sPDiv_num[tscaleNumber]
            if self.osc.isDemo is False:
                self.osc._uDsoSDKSetSampleRate_(sampleRate)
            self.timeLabel.setText("M " + self.canvas.sPDiv[tscaleNumber])
            self.canvas.rescale_axes()

    def zoom_out_seconds(self):
        if self.canvas.currentSecondsScaleNumber < 26:
            self.canvas.currentSecondsScaleNumber += 1
            tscaleNumber = self.canvas.currentSecondsScaleNumber
            sampleRate = self.canvas.sPDiv_num[tscaleNumber]
            if self.osc.isDemo is False:
                self.osc._uDsoSDKSetSampleRate_(sampleRate)
            self.timeLabel.setText("M " + self.canvas.sPDiv[tscaleNumber])
            self.canvas.rescale_axes()

    # box disconnection
    def disconnect_box(self, box):
        if box.signalActivatedIsConnected:
            box.activated.disconnect()
            box.setStyleSheet(
                    "QComboBox::drop-down {border-width: 0px}" +
                    "QComboBox::down-arrow {image: none; border-width: 0px}" +
                    "QComboBox{border-top: 0px solid rgb(85, 0, 255);" +
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

    # function for capturing
    def new_capture(self):
        if self.osc.isDemo is True:
            if self.canvas.animation_is_running is False:
                self.canvas.animation_is_running = True
                self.rsLabel.setText('Run')
                self.canvas.saved_lines_data = {"CH1": [[], []], 
                                                "CH2": [[], []]}
            else:
                self.canvas.animation_is_running = False
                self.rsLabel.setText('Stop')
            return
        if self.canvas.animation_is_running is False:
            if self.mutex.tryLock() is False:
                print("not good")
                return
            self.canvas.animation_is_running = True
            self.rsLabel.setText('Run')
            self.canvas.saved_lines_data = {"CH1": [[], []], "CH2": [[], []]}

            # QThread and capt
            self.thr = QtCore.QThread()
            self.cptr = Capt()
            self.cptr.moveToThread(self.thr)

            # connections
            self.thr.started.connect(self.cptr.SingleShot)
            self.thr.finished.connect(self.thr.deleteLater)
            self.thr.finished.connect(self.cptr.deleteLater)
            self.cptr.dataIsReady.connect(self.thr.quit)
            self.cptr.dataIsReady.connect(self.cptr.deleteLater)
            self.cptr.dataIsReady.connect(self.process_data)
            self.cptr.readyToRestart.connect(self.re_capture)
            self.cptr.readyToRestart.connect(self.thr.quit)
            self.cptr.readyToRestart.connect(self.cptr.deleteLater)
            self.ceaseCapturing.connect(self.cptr.stopCapturing)
            self.restartCapturing.connect(self.cptr.newCapturing)

            self.thr.start()

        else:
            if self.mutex.tryLock() is True:
                self.mutex.unlock()
                print("WOWWWWWWWWWWWWWWWWWWWWWWWWWWW")
                return
            self.ceaseCapturing.emit()
            while(self.canvas.animation_is_running):
                QtCore.QCoreApplication.processEvents()

    # function for Run/Stop
    def rschange(self):
        if self.first_run is True:
            self.canvas.readyToRunAgain = True
            self.first_run = False
            self.new_capture()
        else:
            if self.mutex.tryLock() is True:
                self.ceaseFurtherCapture.emit()
                self.mutex.unlock()
            else:
                self.ceaseCapturing.emit()
                while(self.canvas.animation_is_running):
                    QtCore.QCoreApplication.processEvents()
            self.rsLabel.setText('Stop')
            self.first_run = True

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
        self.dynBox3.addItems(["10K"])
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
        self.change_threshold()

    def tgslot6a(self):
        self._tgSlope = self.dynBox6.currentText()
        self.change_threshold()

    def tgslot6b(self):
        self._tgVideo = self.dynBox6.currentText()

    def tgslot8(self):
        self._tgDelay = self.dynBox8.currentText()

    # function for Display
    def dpchange(self):
        self._GlMode = "Display"
        self.alldyndisconnect()
        self.clear_all_fields()
        
        if self._mrCH == "CH1":
            self.abconnect(self.dynBox7, self.dpslot7a)
            self.dynLabel7.setText("CH1 Probe")
            self.dynBox7.addItems(["1x", "10x"])
            self.dynBox7.setCurrentIndex(self.dynBox7.findText(self._ch1Probe[0]))

        if self._mrCH == "CH2":
            self.abconnect(self.dynBox7, self.dpslot7b)
            self.dynLabel7.setText("CH2 Probe")
            self.dynBox7.addItems(["1x", "10x"])
            self.dynBox7.setCurrentIndex(self.dynBox7.findText(self._ch2Probe[0]))

    def dpslot7a(self):
        self._ch1Probe[0] = self.dynBox7.currentText()
        print("current text: ", self._ch1Probe)
        self.change_volt_div()
        self.change_threshold()

    def dpslot7b(self):
        self._ch2Probe[0] = self.dynBox7.currentText()
        print("current text: ", self._ch2Probe)
        self.change_volt_div()
        self.change_threshold()

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

        self.abconnect(self.dynBox1, self.mrslot1)
        self.dynLabel1.setText("Selected Channel")
        self.dynBox1.addItems(["CH1", "CH2"])
        self.dynBox1.setCurrentIndex(self.dynBox1.findText(self._mrCH))

    # slots for Measure
    def mrslot1(self):
        self._mrCH = self.dynBox1.currentText()

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
