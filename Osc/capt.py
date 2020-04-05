import numpy as np
import ctypes
import os.path

from ctypes import *
from PyQt5 import QtCore


class Capt(QtCore.QObject):

    dataIsReady = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        self.import_lib()

        self.uDsoSDKSetRecordLength.argtypes = (c_int, )
        self.uDsoSDKSetRecordLength.restype = c_bool
        self._uDsoSDKSetRecordLength_(10000)

        self.uDsoSDKCaptureEx.restype = c_bool
        self.uDsoSDKDataReady.restype = c_bool

        self.uDsoSDKReadDbl_uv.argtypes = (c_int, POINTER(c_int),
                                           POINTER(c_double), POINTER(c_int))
        self.uDsoSDKReadDbl_uv.restype = c_bool

        self.dbWaveData_Length = self.iRecordLength_value * 2
        self.dbWaveData = (c_double * self.dbWaveData_Length)()
        self.iVoltDiv_Length = 2
        self.iVoltDiv = (c_int * self.iVoltDiv_Length)()
        self.iProbe_CHs = 2
        self.iProbe = (c_int * self.iProbe_CHs)()
        self.iProbe[0] = self.iProbe[1] = c_int(10)

        ctypes.cast(self.dbWaveData, ctypes.POINTER(ctypes.c_double))
        ctypes.cast(self.iProbe, ctypes.POINTER(ctypes.c_int))

        self.uDsoSDKSetWaitMode.argtypes = (c_int, c_int64, )
        self.uDsoSDKSetWaitMode.restype = c_bool

        self.isInterrupted = False

    def import_lib(self):
        dll_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "DSOSDK.dll")
        DSOSDK_dll = WinDLL(dll_file)

        # BOOL uDsoSDKCaptureEx()
        self.uDsoSDKCaptureEx = DSOSDK_dll.uDsoSDKCaptureEx
        self.uDsoSDKDataReady = DSOSDK_dll.uDsoSDKDataReady  # BOOL

        # int uDsoSDKStop()
        self.uDsoSDKStop = DSOSDK_dll.uDsoSDKStop

        # BOOL uDsoSDKSetWaitMode(int iWaitMode, __int64 i64CustomWaitTime_ps)
        self.uDsoSDKSetWaitMode = DSOSDK_dll.uDsoSDKSetWaitMode

        # uDsoSDKSetRecordLength(ByVal iRecordLength As Integer) As Boolean
        self.uDsoSDKSetRecordLength = DSOSDK_dll.uDsoSDKSetRecordLength

        # uDsoSDKReadDbl_uv(ByVal iDev As Integer, ByRef iFlag As IntPtr,
        # ByVal lpdbDst As Double(), ByVal iProbe As Integer()) As Boolean
        self.uDsoSDKReadDbl_uv = DSOSDK_dll.uDsoSDKReadDbl_uv

    def _uDsoSDKReadDbl_uv_(self, Dev, Flag):
        self.iDev = c_int(Dev)
        self.iFlag = c_int(Flag)

        self.uDsoSDKReadDbl_uv(self.iDev, pointer(self.iFlag),
                               self.dbWaveData, self.iProbe)

    # BOOL uDsoSDKSetWaitMode(int iWaitMode, __int64 i64CustomWaitTime_ps)
    def _uDsoSDKSetWaitMode_(self, WaitMode, CustomWaitTime_ps = 0):      
        self.iWaitMode = c_int(WaitMode) # WAIT_FOREVER 2 
        self.i64CustomWaitTime_ps = c_int64(CustomWaitTime_ps)
        self.uDsoSDKSetWaitMode(self.iWaitMode, self.i64CustomWaitTime_ps)

    # uDsoSDKSetRecordLength(ByVal iRecordLength As Integer) As Boolean
    def _uDsoSDKSetRecordLength_(self, RecordLength):
        self.iRecordLength = c_int(RecordLength)  # value for TS2202E (10kB)
        self.uDsoSDKSetRecordLength(self.iRecordLength)
        self.iRecordLength_value = self.iRecordLength.value


    def SingleShot(self):
        self.isInterrupted = False
        self._uDsoSDKSetWaitMode_(2)
        self.uDsoSDKCaptureEx()
        while self.uDsoSDKDataReady() is False:
            QtCore.QCoreApplication.processEvents()
            if self.isInterrupted is True:
                break
            pass

        if self.isInterrupted is True:
            self.uDsoSDKStop()
            self.dataIsReady.emit()
            return
        self._uDsoSDKReadDbl_uv_(0, 0)
        self.data_ = np.frombuffer(self.dbWaveData, float)
        self.uDsoSDKStop()
        self.dataIsReady.emit()

    def stopCapturing(self):
        self.isInterrupted = True
