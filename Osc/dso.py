import win32gui
import ctypes

import numpy as np
import matplotlib.pyplot as plt

from ctypes import *
from ctypes.wintypes import HWND, LPCSTR, LPSTR

class

# importing acute-library
def lib_import():
    DSOSDK_dll = WinDLL("DSOSDK.dll")
    fInit = False
    fRepeat = False
    fDataReady = False
    iRecLength = int()
    iVoltDiv = int()
    dbWaveData = float()
    iProbe = int()

    # int uDsoSDKInit()
    uDsoSDKInit = DSOSDK_dll.uDsoSDKInit
    # int uDsoSDKInitStack(LPSTR lpszSN)
    uDsoSDKInitStack = DSOSDK_dll.uDsoSDKInitStack
    # BOOL uDsoSDKSelectGroup(int iGroup)
    uDsoSDKSelectGroup = DSOSDK_dll.uDsoSDKSelectGroup

    # BOOL uDsoSDKCaptureEx()
    uDsoSDKCaptureEx = DSOSDK_dll.uDsoSDKCaptureEx

    # int uDsoSDKStop()
    uDsoSDKStop = DSOSDK_dll.uDsoSDKStop
    uDsoSDKShutdown = DSOSDK_dll.uDsoSDKShutdown  # bool

    # BOOL uDsoSDKSetEdgeTrig(int iSrc, int iSlope, __int64 i64Threshold_uV)
    uDsoSDKSetEdgeTrig = DSOSDK_dll.uDsoSDKSetEdgeTrig

    # BOOL uDsoSDKSetWaitMode(int iWaitMode, __int64 i64CustomWaitTime_ps)
    uDsoSDKSetWaitMode = DSOSDK_dll.uDsoSDKSetWaitMode
    # BOOL uDsoSDKGetWaitMode(int iWaitMode, __int64 &i64CustomWaitTime_ps)
    uDsoSDKGetWaitMode = DSOSDK_dll.uDsoSDKGetWaitMode

    uDsoSDKDataReady = DSOSDK_dll.uDsoSDKDataReady  # BOOL
    # int uDsoSDKGetStatus( int iDev )
    uDsoSDKGetStatus = DSOSDK_dll.uDsoSDKGetStatus

    # BOOL uDsoSDKGetTrigPos(__int64 i64TrigPosition)
    uDsoSDKSetTrigPos = DSOSDK_dll.uDsoSDKSetTrigPos
    # BOOL uDsoSDKGetTrigPos(__int64 & i64TrigPosition)
    uDsoSDKGetTrigPos = DSOSDK_dll.uDsoSDKGetTrigPos

    # uDsoSDKSetRecordLength(ByVal iRecordLength As Integer) As Boolean
    uDsoSDKSetRecordLength = DSOSDK_dll.uDsoSDKSetRecordLength
    # uDsoSDKGetRecordLength(ByRef iRecordLength As IntPtr) As Boolean
    uDsoSDKGetRecordLength = DSOSDK_dll.uDsoSDKGetRecordLength

    # BOOL uDsoSDKSetSampleRate(__int64 i64SampleRate)
    uDsoSDKSetSampleRate = DSOSDK_dll.uDsoSDKSetSampleRate
    # BOOL uDsoSDKGetSampleRate(__int64 & i64SampleRate)
    uDsoSDKGetSampleRate = DSOSDK_dll.uDsoSDKGetSampleRate

    # uDsoSDKReadDbl_uv(ByVal iDev As Integer, ByRef iFlag As IntPtr,
    # ByVal lpdbDst As Double(), ByVal iProbe As Integer()) As Boolean
    uDsoSDKReadDbl_uv = DSOSDK_dll.uDsoSDKReadDbl_uv

    # BOOL uDsoSDKSetVoltDiv(int iCh, int iVoltDiv_uV)
    uDsoSDKSetVoltDiv = DSOSDK_dll.uDsoSDKSetVoltDiv
    # BOOL uDsoSDKGetVoltDiv(int iCh, int & iVoltDiv_uV)
    uDsoSDKGetVoltDiv = DSOSDK_dll.uDsoSDKGetVoltDiv

    # Acquire Mode
    # BOOL uDsoSDKSetAcquireMode(int iCh, int iAcquireMode)
    uDsoSDKSetAcquireMode = DSOSDK_dll.uDsoSDKSetAcquireMode
    # BOOL uDsoSDKSetAcquireMode(int iCh, int & iAcquireMode)
    uDsoSDKGetAcquireMode = DSOSDK_dll.uDsoSDKGetAcquireMode

    # Get Hardware Information functions
    # BOOL uDsoSDKGetVendorName( int iDev, LPSTR lpszData)
    uDsoSDKGetVendorName = DSOSDK_dll.uDsoSDKGetVendorName
    # BOOL uDsoSDKGetProductName( int iDev, LPSTR lpszData)
    uDsoSDKGetProductName = DSOSDK_dll.uDsoSDKGetProductName
    # BOOL uDsoSDKGetSerialNum( int iDev, LPSTR lpszData)
    uDsoSDKGetSerialNum = DSOSDK_dll.uDsoSDKGetSerialNum


def _uDsoSDKInit_():
    uDsoSDKInit()

def _uDsoSDKSetRecordLength_():
    uDsoSDKSetRecordLength.argtypes = (c_int, )
    uDsoSDKSetRecordLength.restype = c_bool
    
    iRecordLength = c_int(10000)  # value for TS2202E (memory 10kB)
    uDsoSDKSetRecordLength(iRecordLength)
    iRecordLength_value = iRecordLength.value

