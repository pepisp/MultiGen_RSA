from ctypes import *
from os import chdir
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
from RSA_API import *


# C:\Tektronix\RSA_API\lib\x64 needs to be added to the
# PATH system environment variable
chdir("C:\\Tektronix\\RSA_API\\lib\\x64")
rsa = cdll.LoadLibrary("RSA_API.dll")


"""################CLASSES AND FUNCTIONS################"""
def err_check(rs):
    if ReturnStatus(rs) != ReturnStatus.noError:
        raise RSAError(ReturnStatus(rs).name)

def search_connect():
    numFound = c_int(0)
    intArray = c_int * DEVSRCH_MAX_NUM_DEVICES
    deviceIDs = intArray()
    deviceSerial = create_string_buffer(DEVSRCH_SERIAL_MAX_STRLEN)
    deviceType = create_string_buffer(DEVSRCH_TYPE_MAX_STRLEN)
    apiVersion = create_string_buffer(DEVINFO_MAX_STRLEN)

    rsa.DEVICE_GetAPIVersion(apiVersion)
    print('API Version {}'.format(apiVersion.value.decode()))

    err_check(rsa.DEVICE_Search(byref(numFound), deviceIDs,
                                deviceSerial, deviceType))

    if numFound.value < 1:
        # rsa.DEVICE_Reset(c_int(0))
        print('No instruments found. Exiting script.')
        exit()
    elif numFound.value == 1:
        print('One device found.')
        print('Device type: {}'.format(deviceType.value.decode()))
        print('Device serial number: {}'.format(deviceSerial.value.decode()))
        err_check(rsa.DEVICE_Connect(deviceIDs[0]))
    else:
        # corner case
        print('2 or more instruments found. Enumerating instruments, please wait.')
        for inst in deviceIDs:
            rsa.DEVICE_Connect(inst)
            rsa.DEVICE_GetSerialNumber(deviceSerial)
            rsa.DEVICE_GetNomenclature(deviceType)
            print('Device {}'.format(inst))
            print('Device Type: {}'.format(deviceType.value))
            print('Device serial number: {}'.format(deviceSerial.value))
            rsa.DEVICE_Disconnect()
        # note: the API can only currently access one at a time
        selection = 1024
        while (selection > numFound.value - 1) or (selection < 0):
            selection = int(input('Select device between 0 and {}\n> '.format(numFound.value - 1)))
        err_check(rsa.DEVICE_Connect(deviceIDs[selection]))
    rsa.CONFIG_Preset()


"""################SPECTRUM EXAMPLE################"""
def config_spectrum(cf=1e9, refLevel=0, span=40e6, rbw=300e3,traceLen=801):
    rsa.SPECTRUM_SetEnable(c_bool(True))
    rsa.CONFIG_SetCenterFreq(c_double(cf))
    rsa.CONFIG_SetReferenceLevel(c_double(refLevel))


    rsa.SPECTRUM_SetDefault()
    specSet = Spectrum_Settings()
    rsa.SPECTRUM_GetSettings(byref(specSet))
    specSet.window = SpectrumWindows.SpectrumWindow_Kaiser
    specSet.verticalUnit = SpectrumVerticalUnits.SpectrumVerticalUnit_dBm
    specSet.span = span
    specSet.rbw = rbw
    specSet.traceLength = traceLen
    rsa.SPECTRUM_SetSettings(specSet)
    rsa.SPECTRUM_GetSettings(byref(specSet))
    return specSet


def create_frequency_array(specSet):
    # Create array of frequency data for plotting the spectrum.
    freq = np.arange(specSet.actualStartFreq, specSet.actualStartFreq
                     + specSet.actualFreqStepSize * specSet.traceLength,
                     specSet.actualFreqStepSize)
    return freq


def acquire_spectrum(specSet):
    ready = c_bool(False)
    traceArray = c_float * specSet.traceLength
    traceData = traceArray()
    outTracePoints = c_int(0)
    traceSelector = SpectrumTraces.SpectrumTrace1

    rsa.DEVICE_Run()
    rsa.SPECTRUM_AcquireTrace()
    while not ready.value:
        rsa.SPECTRUM_WaitForDataReady(c_int(100), byref(ready))
    rsa.SPECTRUM_GetTrace(traceSelector, specSet.traceLength, byref(traceData),
                          byref(outTracePoints))
    rsa.DEVICE_Stop()
    return np.array(traceData)


def spectrum_example():
    print('\n\n########Spectrum Example########')
    search_connect()
    cf = 216.925e6
    refLevel = -40
    span = 5e6
    rbw = 10e3
    traceLen=4096
    specSet = config_spectrum(cf, refLevel, span, rbw,traceLen)
    trace = acquire_spectrum(specSet)
    freq = create_frequency_array(specSet)
    peakPower, peakFreq = peak_power_detector(freq, trace)

    plt.figure(1, figsize=(10, 7))
    ax = plt.subplot(111, facecolor='k')
    ax.plot(freq, trace, color='y')
    ax.set_title('Spectrum Trace')
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Amplitude (dBm)')
    ax.axvline(peakFreq)
    ax.text((freq[0] + specSet.span / 20), peakPower,
            'Peak power in spectrum: {:.2f} dBm @ {} MHz'.format(
                peakPower, peakFreq / 1e6), color='white')
    ax.set_xlim([freq[0], freq[-1]])
    ax.set_ylim([refLevel - 100, refLevel])
    plt.tight_layout()
    plt.show()
    rsa.DEVICE_Disconnect()

"""################MISC################"""
def config_trigger(trigMode=TriggerMode.triggered, trigLevel=-10,
                   trigSource=TriggerSource.TriggerSourceIFPowerLevel):
    rsa.TRIG_SetTriggerMode(trigMode)
    rsa.TRIG_SetIFPowerTriggerLevel(c_double(trigLevel))
    rsa.TRIG_SetTriggerSource(trigSource)
    rsa.TRIG_SetTriggerPositionPercent(c_double(10))


def peak_power_detector(freq, trace):
    peakPower = np.amax(trace)
    peakFreq = freq[np.argmax(trace)]

    return peakPower, peakFreq


def main():
    # uncomment the example you'd like to run
    spectrum_example()
    #block_iq_example()
    #dpx_example()
    # if_stream_example()
    # iq_stream_example()

if __name__ == '__main__':
    main()
