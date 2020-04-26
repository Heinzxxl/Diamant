import numpy as np
import ctypes
import os.path

from ctypes import *

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject
from PyQt5.QtCore import QCoreApplication


class uDso(QObject):
    def __init__(self, parent=None):
        super().__init__()
        self.lib_import()
        self.isInterrupted = False
        self.isDemo = False

        self.uDsoSDKInit.restype = c_bool
        if self._uDsoSDKInit_() is False:
            print("No DSO found. Entering Demo Mode...")
            self.isDemo = True
            return

        self.uDsoSDKSetRecordLength.argtypes = (c_int, )
        self.uDsoSDKSetRecordLength.restype = c_bool
        self._uDsoSDKSetRecordLength_(10000)

        self.uDsoSDKSetEdgeTrig.argtypes = (c_int, c_int, c_int64)
        self.uDsoSDKSetEdgeTrig.restype = c_bool
        self._uDsoSDKSetEdgeTrig_(0, 0, 50000)

        self.uDsoSDKSetVoltDiv.argtypes = (c_int, c_int)
        self.uDsoSDKSetVoltDiv.restype = c_bool
        self._uDsoSDKSetVoltDiv_(0, 200000)

        self.uDsoSDKSetSampleRate.argtypes = (c_int64, )
        self.uDsoSDKSetSampleRate.restype = c_bool
        self._uDsoSDKSetSampleRate_(1000000)
        
        self.uDsoSDKGetSampleRate.argtypes = (POINTER(c_int), )
        self.uDsoSDKGetSampleRate.restype = c_bool

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

    # importing acute-library
    def lib_import(self):
        dll_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "DSOSDK.dll")
        dll_file_2 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "DsoRun.dll")
        DSOSDK_dll = WinDLL(dll_file)
        DsoRun_dll = WinDLL(dll_file_2)
        self.fInit = False
        self.fRepeat = False
        self.fDataReady = False
        self.iRecLength = int()
        self.iVoltDiv = int()
        self.dbWaveData = float()
        self.iProbe = int()

        # int uDsoSDKInit()
        self.uDsoSDKInit = DSOSDK_dll.uDsoSDKInit
        # int uDsoSDKInitStack(LPSTR lpszSN)
        self.uDsoSDKInitStack = DSOSDK_dll.uDsoSDKInitStack
        # BOOL uDsoSDKSelectGroup(int iGroup)
        self.uDsoSDKSelectGroup = DSOSDK_dll.uDsoSDKSelectGroup

        # BOOL uDsoSDKCaptureEx()
        self.uDsoSDKCaptureEx = DSOSDK_dll.uDsoSDKCaptureEx

        # int uDsoSDKStop()
        self.uDsoSDKStop = DSOSDK_dll.uDsoSDKStop
        self.uDsoSDKShutdown = DSOSDK_dll.uDsoSDKShutdown  # bool

        # BOOL uDsoSDKSetEdgeTrig(int iSrc, int iSlope,
        #                         __int64 i64Threshold_uV)
        self.uDsoSDKSetEdgeTrig = DSOSDK_dll.uDsoSDKSetEdgeTrig

        # BOOL uDsoSDKSetWaitMode(int iWaitMode, __int64 i64CustomWaitTime_ps)
        self.uDsoSDKSetWaitMode = DSOSDK_dll.uDsoSDKSetWaitMode
        # BOOL uDsoSDKGetWaitMode(int iWaitMode, __int64 &i64CustomWaitTime_ps)
        self.uDsoSDKGetWaitMode = DSOSDK_dll.uDsoSDKGetWaitMode

        self.uDsoSDKDataReady = DSOSDK_dll.uDsoSDKDataReady  # BOOL
        # int uDsoSDKGetStatus( int iDev )
        self.uDsoSDKGetStatus = DSOSDK_dll.uDsoSDKGetStatus

        # BOOL uDsoSDKGetTrigPos(__int64 i64TrigPosition)
        self.uDsoSDKSetTrigPos = DSOSDK_dll.uDsoSDKSetTrigPos
        # BOOL uDsoSDKGetTrigPos(__int64 & i64TrigPosition)
        self.uDsoSDKGetTrigPos = DSOSDK_dll.uDsoSDKGetTrigPos

        # uDsoSDKSetRecordLength(ByVal iRecordLength As Integer) As Boolean
        self.uDsoSDKSetRecordLength = DSOSDK_dll.uDsoSDKSetRecordLength
        # uDsoSDKGetRecordLength(ByRef iRecordLength As IntPtr) As Boolean
        self.uDsoSDKGetRecordLength = DSOSDK_dll.uDsoSDKGetRecordLength

        # BOOL uDsoSDKSetSampleRate(__int64 i64SampleRate)
        self.uDsoSDKSetSampleRate = DSOSDK_dll.uDsoSDKSetSampleRate
        # BOOL uDsoSDKGetSampleRate(__int64 & i64SampleRate)
        self.uDsoSDKGetSampleRate = DSOSDK_dll.uDsoSDKGetSampleRate

        # uDsoSDKReadDbl_uv(ByVal iDev As Integer, ByRef iFlag As IntPtr,
        # ByVal lpdbDst As Double(), ByVal iProbe As Integer()) As Boolean
        self.uDsoSDKReadDbl_uv = DSOSDK_dll.uDsoSDKReadDbl_uv

        # BOOL uDsoSDKSetVoltDiv(int iCh, int iVoltDiv_uV)
        self.uDsoSDKSetVoltDiv = DSOSDK_dll.uDsoSDKSetVoltDiv
        # BOOL uDsoSDKGetVoltDiv(int iCh, int & iVoltDiv_uV)
        self.uDsoSDKGetVoltDiv = DSOSDK_dll.uDsoSDKGetVoltDiv

        # Acquire Mode
        # BOOL uDsoSDKSetAcquireMode(int iCh, int iAcquireMode)
        self.uDsoSDKSetAcquireMode = DSOSDK_dll.uDsoSDKSetAcquireMode
        # BOOL uDsoSDKSetAcquireMode(int iCh, int & iAcquireMode)
        self.uDsoSDKGetAcquireMode = DSOSDK_dll.uDsoSDKGetAcquireMode

        # Get Hardware Information functions
        # BOOL uDsoSDKGetVendorName( int iDev, LPSTR lpszData)
        self.uDsoSDKGetVendorName = DSOSDK_dll.uDsoSDKGetVendorName
        # BOOL uDsoSDKGetProductName( int iDev, LPSTR lpszData)
        self.uDsoSDKGetProductName = DSOSDK_dll.uDsoSDKGetProductName
        # BOOL uDsoSDKGetSerialNum( int iDev, LPSTR lpszData)
        self.uDsoSDKGetSerialNum = DSOSDK_dll.uDsoSDKGetSerialNum

    def _uDsoSDKInit_(self):
        return self.uDsoSDKInit()

    # uDsoSDKSetRecordLength(ByVal iRecordLength As Integer) As Boolean
    def _uDsoSDKSetRecordLength_(self, RecordLength):
        self.iRecordLength = c_int(RecordLength)  # value for TS2202E (10kB)
        self.uDsoSDKSetRecordLength(self.iRecordLength)
        self.iRecordLength_value = self.iRecordLength.value

    # BOOL uDsoSDKSetEdgeTrig(int iSrc, int iSlope, __int64 i64Threshold_uV)
    def _uDsoSDKSetEdgeTrig_(self, Src, Slope, Threshold_uV):
        self.iSrc = c_int(Src)  # 0 - Trigger source from channel 1.
        self.iSlope = c_int(Slope)  #  0 - Rising edge
        self.i64Threshold_uV = c_int64(Threshold_uV)  # 90 mV = 90 * 1e3 uV

        self.uDsoSDKSetEdgeTrig(self.iSrc, self.iSlope, self.i64Threshold_uV)

    # BOOL uDsoSDKSetVoltDiv(int iCh, int iVoltDiv_uV)
    def _uDsoSDKSetVoltDiv_(self, Ch, VoltDiv_uV):
        # iVoltDiv_uV_value = 2000000 # 2,000,000 uV = 2,000 mV
        # iVoltDiv_uV_value = 1000000 # 1,000,000 uV = 1,000 mV
        # iVoltDiv_uV_value = 500000 # 500,000 uV = 500 mV
        self.iVoltDiv_uV_value = VoltDiv_uV  # 200,000 uV = 200 mV
        self.iVoltDiv_uV = c_int(VoltDiv_uV)
        self.iCh = c_int(Ch)

        self.uDsoSDKSetVoltDiv(self.iCh, self.iVoltDiv_uV)

    # BOOL uDsoSDKSetSampleRate(__int64 i64SampleRate)
    def _uDsoSDKSetSampleRate_(self, SampleRate):
        self.i64SampleRate = c_int64(SampleRate)

        self.uDsoSDKSetSampleRate(self.i64SampleRate)
        
    # uDsoSDKReadDbl_uv(ByVal iDev As Integer, 
    #                   ByRef iFlag As IntPtr, 
    #                   ByVal lpdbDst As Double(), 
    #                   ByVal iProbe As Integer()) As Boolean
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