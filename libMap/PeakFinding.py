
import numpy as np
import scipy
#from scipy import signal
from scipy.signal import find_peaks, peak_widths, peak_prominences

class PeakDetection():
    #Peakutils
    def __init__(self, Intensity, prom):
        self.set_x(Intensity, prom)

    def get_Peaks(self):
        return self.__Peaks

    def get_Valleys(self):
        return self.__Valleys

    def get_Widths(self):
        return self.__Widths[0]    #for actual values

    def get_WidthsRD(self):
        return self.__Widths

    def get_Prominence(self):
        return self.__Prominence

    def set_x(self, In, prom):
        self.__Peaks ,_= scipy.signal.find_peaks(np.array(In), prominence=prom )
        self.__Valleys, _ = scipy.signal.find_peaks(-(np.array(In)), prominence=prom )
        self.__Prominence = peak_prominences(np.array(In), self.__Peaks)[0]
        #print (self.__Prominence)
        self.__Widths = peak_widths(np.array(In), self.__Peaks, rel_height=0.5)
        #print (self.__Widths[0])

class PeakExtraction():
    #Getdetected Vakues
    def __init__(self, Mzml, NormIntensity, Peaks):
        self.set_PeakMz(Mzml, Peaks)
        self.set_PeakInt(NormIntensity, Peaks)

    def get_PeakMzList(self):
        return self.__Peakmz

    def get_PeakIntList(self):
        return self.__PeakInt

    def set_PeakMz(self, Mzml, Peaks):
        self.__Peakmz = []
        for i in Peaks:
            self.__Peakmz.append(Mzml[i])

    def set_PeakInt(self, NormIntensity, Peaks):
        self.__PeakInt = []
        for i in Peaks:
            self.__PeakInt.append(NormIntensity[i])

class ValleyExtraction():
    #Getdetected Vakues
    def __init__(self,Mzml, NormIntensity, Valleys ):
        self.set_ValleyMz(Mzml, Valleys)
        self.set_ValleyInt(NormIntensity, Valleys)

    def get_ValleyMzList(self):
        return self.__Valleymz

    def get_ValleyIntList(self):
        return self.__ValleyInt

    def set_ValleyMz(self,Mzml, Valleys):
        self.__Valleymz = []
        for i in Valleys:
            self.__Valleymz.append(Mzml[i])

    def set_ValleyInt(self,NormIntensity, Valleys):
        self.__ValleyInt = []
        for i in Valleys:
            self.__ValleyInt.append(NormIntensity[i])
