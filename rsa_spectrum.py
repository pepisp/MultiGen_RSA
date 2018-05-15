from ctypes import *
from os import chdir
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
from RSA_API import *

class RSA_DEVICE():
    def __init__(self):
        # C:\Tektronix\RSA_API\lib\x64 needs to be added to the
        # PATH system environment variable
        #chdir("C:\\Tektronix\\RSA_API\\lib\\x64")
        self.rsa = cdll.LoadLibrary('RSA_API.dll')
        self.connectionStatus=False
        self.deviceID = 1024 #no device

    def search(self):
        numFound = c_int(0)
        intArray = c_int * DEVSRCH_MAX_NUM_DEVICES
        deviceIDs = intArray()
        deviceSerial = create_string_buffer(DEVSRCH_SERIAL_MAX_STRLEN)
        deviceType = create_string_buffer(DEVSRCH_TYPE_MAX_STRLEN)
        apiVersion = create_string_buffer(DEVINFO_MAX_STRLEN)

        self.rsa.DEVICE_GetAPIVersion(apiVersion)
        print('API Version {}'.format(apiVersion.value.decode()))

        try:
            self.err_check(self.rsa.DEVICE_Search(byref(numFound), deviceIDs,deviceSerial, deviceType))
        except: return False
        if numFound.value < 1:
            # rsa.DEVICE_Reset(c_int(0))
            print('No instruments found. Exiting script.')
            return False

        elif numFound.value == 1:
            print('One device found.')
            print('Device type: {}'.format(deviceType.value.decode()))
            print('Device serial number: {}'.format(deviceSerial.value.decode()))
            self.deviceID=deviceIDs[0]
            print(self.deviceID)
        else:
            # corner case
            print('2 or more instruments found. Enumerating instruments, please wait.')
            for inst in deviceIDs:
                self.rsa.DEVICE_Connect(inst)
                self.rsa.DEVICE_GetSerialNumber(deviceSerial)
                self.rsa.DEVICE_GetNomenclature(deviceType)
                print('Device {}'.format(inst))
                print('Device Type: {}'.format(deviceType.value))
                print('Device serial number: {}'.format(deviceSerial.value))
                self.rsa.DEVICE_Disconnect()
                # note: the API can only currently access one at a time
                # selection = 1024
                # while (selection > numFound.value - 1) or (selection < 0):
                #     selection = int(input('Select device between 0 and {}\n> '.format(numFound.value - 1)))

    def connect(self):
        if self.deviceID==1024:
            print('Search the device befor connect')
        else:
            try:
                self.err_check(self.rsa.DEVICE_Connect(self.deviceID))
            except:
                self.connectionStatus=False
                return False
            self.connectionStatus=True
            self.rsa.CONFIG_Preset()

    def disconnect(self):
        if self.connectionStatus:
            self.rsa.DEVICE_Disconnect()
            self.connectionStatus=False

    def err_check(self,rs):
        if ReturnStatus(rs) != ReturnStatus.noError:
            raise RSAError(ReturnStatus(rs).name)
