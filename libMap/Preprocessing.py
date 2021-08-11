import scipy
from scipy import sparse
from scipy.sparse.linalg import spsolve
import numpy as np
from scipy import signal
import os
#import pyopenms
import xml.etree.ElementTree as ET
import base64
import struct

'''New Decoder '''
class DecoderNew():
    def __init__(self,path, region1, region2):
        if path.split(".")[-1] == "mzml":
            self.set_mzml(path,region1, region2)
        elif path.split(".")[-1] == "txt":
            self.set_txt(path,region1, region2)
        else:
            self.__mzList = None
            self.__intensityList = None
    
    def get_mz(self):
        return np.array(self.__mzList)

    def get_Int(self):
        return np.array(self.__intensityList)

    def decodeSep(self, path):
        with open(path, 'r') as sepdata:
            line = 0
            item = [" ", "\t", ","]
            sep = None
            for row in sepdata:
                if line ==10:
                    for i in item:
                        infoList = row.split(i)
                        if len(infoList) == 2:
                            sep = i
                        else:
                            pass
                else:
                    pass
                line+=1
        sepdata.close()
        if type(sep) == str:
            return (sep)
        else:
            sep = " "
            return (sep)

    def set_txt(self,path, region1, region2):
        self.__mzList = []
        self.__intensityList = []
        sep = self.decodeSep(path)
        print ("Separator in data is = ",sep)
        print (type(sep))
        with open(path, 'r') as data:
            n = 0
            for line in data:
                if n >10:
                    info = line.split(sep)
                    if float(info[0]) >=region1 and float(info[0]) <= region2:
                        self.__mzList.append(float(info[0]) )
                        self.__intensityList.append(float(info[1].rstrip("\n")) )
                    else:
                        pass
                else:
                    pass
                n+=1
        data.close()

    def set_mzml(self,path, region1, region2):
        mzml_file = ET.parse(path)
        root = mzml_file.getroot()
        Rmz = root.getchildren()[5][0][0][6][0][3]
        RI = root.getchildren()[5][0][0][6][1][3]
        mzbinArray = Rmz.text
        IbinArray = RI.text
        mz_bytes_string = base64.b64decode(mzbinArray)
        I_bytes_string = base64.b64decode(IbinArray)
        count1 = len(mz_bytes_string) // 8
        count2 = len(I_bytes_string) // 8
        self.__decoded_mz = struct.unpack('<{0}d'.format(count1), mz_bytes_string)
        self.__decoded_I = struct.unpack('<{0}d'.format(count2), I_bytes_string)
        self.__mzList = []
        self.__intensityList = []
        for i, mz in enumerate(self.__decoded_mz):
            if mz>=region1 and mz<=region2:
                self.__mzList.append(mz)
                self.__intensityList.append(self.__decoded_I[i])

'''Still need a new decoder for txt files   ---Axima data NIU'''
class DecodeText():
    def __init__(self,path, region1, region2):
        self.set_x(path,region1, region2)

    def get_mz(self):
        return np.array(self.__mzList)

    def get_Int(self):
        return np.array(self.__intensityList)

    def set_x(self,path, region1, region2):
        self.__mzList = []
        self.__intensityList = []
        data = open(path, 'r')
        n = 0
        for line in data:
            if n >7:
                info = line.split("\t")
                #info = line.split(",")
                if float(info[0]) >=region1 and float(info[0]) <= region2:
                    self.__mzList.append(float(info[0]) )
                    self.__intensityList.append(float(info[1].rstrip("\n")) )
                else:
                    pass
            else:
                pass
            n+=1
        data.close()

class DecodeMzml():
    def __init__(self,path, region1, region2):
        self.set_x(path,region1, region2)

    def get_mz(self):
        return np.array(self.__mzList)

    def get_Int(self):
        return np.array(self.__intensityList)
    
    def set_x(self,path, region1, region2):
        mzml_file = ET.parse(path)
        root = mzml_file.getroot()
        Rmz = root.getchildren()[5][0][0][6][0][3]
        RI = root.getchildren()[5][0][0][6][1][3]
        mzbinArray = Rmz.text
        IbinArray = RI.text
        mz_bytes_string = base64.b64decode(mzbinArray)
        I_bytes_string = base64.b64decode(IbinArray)
        count1 = len(mz_bytes_string) // 8
        count2 = len(I_bytes_string) // 8
        self.__decoded_mz = struct.unpack('<{0}d'.format(count1), mz_bytes_string)
        self.__decoded_I = struct.unpack('<{0}d'.format(count2), I_bytes_string)
        self.__mzList = []
        self.__intensityList = []
        for i, mz in enumerate(self.__decoded_mz):
            if mz>=region1 and mz<=region2:
                self.__mzList.append(mz)
                self.__intensityList.append(self.__decoded_I[i])
    
    '''
    def set_x(self,path, region1, region2):
        print ("new decoder")
        exp = pyopenms.MSExperiment()
        pyopenms.MzMLFile().load(path, exp)
        spectrum_data = exp.getSpectrum(0).get_peaks()
        self.__mzList = []
        self.__intensityList = []
        for i,mz in enumerate(spectrum_data[0]):
            if mz>=region1 and mz<=region2:
                self.__mzList.append(mz)
                self.__intensityList.append(spectrum_data[1][i])
    '''

class decodeBrukerText():
    def __init__(self,path, region1, region2):
        self.set_x(path,region1, region2)

    def get_mz(self):
        return np.array(self.__mzList)

    def get_Int(self):
        return np.array(self.__intensityList)

    def set_x(self,path, region1, region2):
        self.__mzList = []
        self.__intensityList = []
        data = open(path, 'r')
        n = 0
        for line in data:
            info = line.split(" ")
            #info = line.split(",")
            if float(info[0]) >=region1 and float(info[0]) <= region2:
                self.__mzList.append(float(info[0]) )
                self.__intensityList.append(float(info[1].rstrip("\n")) )
            else:
                pass
            n+=1
        data.close()

class Smoothing():
    '''gets Int region; bloodtype selected (.isChecked() ==True) '''
    def __init__(self, intensitylist,windowsize,cycle):
        self.set_x(intensitylist, windowsize, cycle)

    def get_x(self):
        return self.__SmoothInt

    def set_x(self, int,windowsize,cycle):
        ''' need to specify if blood type is ?? to determine windowsize, numberofcycles'''
        self.__SmoothInt = scipy.signal.savgol_filter(np.array(int), windowsize, cycle)

class Normalise():
    def __init__(self, SmIntensity):
        self.set_x(SmIntensity)

    def get_x(self):
        return np.array(self.__NormIntensity)

    def set_x(self, In):
        maxValue = max(In)
        self.__NormIntensity = []
        for I in In:
            self.__NormIntensity.append(float(I)/maxValue)

class Baseline():
    def __init__(self,y, lam, p):

        self.__baseline = self.set_baseline_als(y, lam, p)

    def get_baseline(self):
        return self.__baseline

    def set_baseline_als(self ,y, lam, p, niter=10):
        L = len(y)
        D = sparse.diags([1,-2,1],[0,-1,-2], shape=(L,L-2))
        w = np.ones(L)
        for i in range(niter):
            W = sparse.spdiags(w, 0, L, L)
            Z = W + lam * D.dot(D.transpose())
            z = spsolve(Z, w*y)
            w = p * (y > z) + (1-p) * (y < z)
        return z

class LocalNoise():
    def __init__(self, Intensities, mzdata,regionlow, regionhigh):
        self.__noise = self.set_calLocalNoise(Intensities, mzdata,regionlow, regionhigh)
        self.__avgNoise = self.set_avgNoise(self.__noise, axis=0, ddof=0)

    def get_LocalNoise(self):
        return self.__noise

    def get_AvgNoise(self):
        return self.__avgNoise

    def set_calLocalNoise(self, Intensities, mzdata,regionlow, regionhigh):
        noise = []
        for i, mz in enumerate(mzdata):
            if mz>= regionlow and mz<= regionhigh:
                noise.append(Intensities[i])
        return (noise)

    def set_avgNoise(self, a, axis, ddof):
        a = np.asanyarray(a)
        m = a.mean(axis)
        sd = a.std(axis=axis, ddof=ddof)
        if m < 0.0:
            m = 0.001
        return (m)
